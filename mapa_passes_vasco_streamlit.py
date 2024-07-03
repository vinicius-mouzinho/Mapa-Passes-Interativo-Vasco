import altair as alt
import pandas as pd
import streamlit as st
import math
import numpy as np
import mplsoccer

def map_player(player_id):
    player_mapping = {
        303689: 'Vegetti',
        43931: 'Maicon',
        416790: 'Paulo Henrique',
        241049: 'Léo Jardim',
        383997: 'Paulinho',
        337815: 'Rossi',
        373513: 'Piton',
        397505: 'Praxedes',
        378588: 'Zé Gabriel',
        29390: 'Medel',
        14058: 'Payet',
        388576: 'Puma',
        137484: 'Jair',
        468025: 'Erick Marcus',
        137316: 'Léo',
        423092: 'Serginho',
        482037: 'Mateus Carvalho',
        317762: 'David',
        405839: 'Sforza',
        142436: 'Galdames',
        373848: 'João Victor',
        472122: 'Rayan',
        416895: 'Adson',
        369266: 'Robert Rojas',
        515816: 'JP',
        436559: 'Clayton',
        373449: 'Hugo Moura',
        149574: 'Victor Luís',
        515814: 'Estrella'
    }
    return player_mapping.get(player_id, 'Unknown')

def distance_to_goal(x, y):
    goal_x, goal_y = 110, 50
    return math.sqrt((x - goal_x)**2 + (y - goal_y)**2)

def is_deep_completion(x, y):
    return distance_to_goal(x, y) <= 35

def calculate_total_xT(group):
    return group['xT'].sum()

st.set_page_config(page_title="Mapas de passe do Vasco", page_icon="💢")
st.title("💢 Mapas de passe do Vasco")
st.write(
    """
    Esse aplicativo mostra mapas de passe dos jogadores do Vasco no Brasileirão 2024.
    Ele mostra também o número de passes certos, de passes progressivos certos e a 
    porcentagem de conclusão dos passes. Explore-o abaixo!
    """
)

# Leitura dos dados
df1 = pd.read_csv("result Vasco da Gama 2 - 1 Grêmio.csv")
df2 = pd.read_csv("result Red Bull Bragantino 2 - 1 Vasco da Gama.csv")
df3 = pd.read_csv("result Fluminense 2 - 1 Vasco da Gama.csv")
df4 = pd.read_csv("result Vasco da Gama 0 - 4 Criciúma.csv")
df5 = pd.read_csv("result Athletico-PR 1 - 0 Vasco da Gama.csv")
df6 = pd.read_csv("result Vasco da Gama 2 - 1 Vitória.csv")
df7 = pd.read_csv("result Flamengo 6 - 1 Vasco da Gama.csv")
df8 = pd.read_csv("result Palmeiras 2 - 0 Vasco da Gama.csv")
df9 = pd.read_csv("result Vasco da Gama 0 - 0 Cruzeiro.csv")
df10 = pd.read_csv("result Juventude 2 - 0 Vasco da Gama.csv")
df11 = pd.read_csv("result Vasco da Gama 4 - 1 São Paulo.csv")
df12 = pd.read_csv("result Bahia 2 - 1 Vasco da Gama.csv")
df13 = pd.read_csv("result Vasco da Gama 1 - 1 Botafogo.csv")

dataframes = [
    ("Rodada 1 - Vasco da Gama 2 - 1 Grêmio", df1),
    ("Rodada 2 - Red Bull Bragantino 2 - 1 Vasco da Gama", df2),
    ("Rodada 3 - Fluminense 2 - 1 Vasco da Gama", df3),
    ("Rodada 4 - Vasco da Gama 0 - 4 Criciúma", df4),
    ("Rodada 5 - Athletico-PR 1 - 0 Vasco da Gama", df5),
    ("Rodada 6 - Vasco da Gama 2 - 1 Vitória", df6),
    ("Rodada 7 - Vasco da Gama 1 - 6 Flamengo", df7),
    ("Rodada 8 - Palmeiras 2 - 0 Vasco da Gama", df8),
    ("Rodada 9 - Vasco da Gama 0 - 0 Cruzeiro", df9),
    ("Rodada 10 - Juventude 2 - 0 Vasco da Gama", df10),
    ("Rodada 11 - Vasco da Gama 4 - 1 São Paulo", df11),
    ("Rodada 12 - Bahia 2 - 1 Vasco da Gama", df12),
    ("Rodada 13 - Vasco da Gama 1 - 1 Botafogo", df13)
]

# Concatenar todos os dataframes para obter a lista completa de jogadores
all_dfs = [df for _, df in dataframes]
df_all = pd.concat(all_dfs, ignore_index=True)
df_all['Player'] = df_all['playerId'].apply(map_player)

# Seleção do jogador
players = sorted(df_all['Player'].unique().tolist())
selected_player = st.selectbox('Selecione o jogador que deseja visualizar:', players, format_func=lambda x: x)

# Filtrar dataframes para o jogador selecionado
selected_player_id = df_all[df_all['Player'] == selected_player]['playerId'].unique()[0]
filtered_dataframes = []
for name, df in dataframes:
    filtered_df = df[df['playerId'] == selected_player_id]
    if not filtered_df.empty:
        filtered_dataframes.append((name, filtered_df))

# Opção de seleção múltipla para as partidas
selected_options = st.multiselect(
    'Selecione as partidas que deseja visualizar (ou selecione todas no botão abaixo):',
    [name for name, df in filtered_dataframes],
    format_func=lambda x: x
)

# Botão para selecionar todos os dataframes
if st.button('Selecionar Todos'):
    selected_options = [name for name, df in filtered_dataframes]

# Filtragem dos dataframes selecionados
selected_dfs = [df for name, df in filtered_dataframes if name in selected_options]

# Concatenar dataframes selecionados em um único dataframe
if selected_dfs:
    dfV = pd.concat(selected_dfs, ignore_index=True)
    dfV['Player'] = dfV['playerId'].apply(map_player)
else:
    dfV = pd.DataFrame()  # Cria um DataFrame vazio se nenhum foi selecionado

if not dfV.empty:
    dfPass = dfV[dfV['type/displayName'] == 'Pass']
    dfCRVGPass = dfPass[dfPass['teamId'] == 1226]

    successful_passes = dfCRVGPass[dfCRVGPass['outcomeType/displayName'] == 'Successful']

    correct_pass_count = successful_passes.groupby('Player').size()
    sorted_correct_pass_count = correct_pass_count.sort_values(ascending=False)

    dfCRVGPass['dist_to_goal_before'] = dfCRVGPass.apply(lambda row: distance_to_goal(row['x'], row['y']), axis=1)
    dfCRVGPass['dist_to_goal_after'] = dfCRVGPass.apply(lambda row: distance_to_goal(row['endX'], row['endY']), axis=1)

    progressive_threshold = 0.75
    dfCRVGPass['progressive_pass'] = (dfCRVGPass['dist_to_goal_after'] < progressive_threshold * dfCRVGPass['dist_to_goal_before']) | \
                                    ((dfCRVGPass['endX'].between(83, 100)) & (dfCRVGPass['endY'].between(21.1, 78.9)))

    correct_progressive_pass = dfCRVGPass[(dfCRVGPass['progressive_pass'] == True) & (dfCRVGPass['outcomeType/displayName'] == 'Successful')]
    progressive_pass_count = correct_progressive_pass.groupby('Player')['progressive_pass'].sum()
    sorted_progressive_pass_count = progressive_pass_count.sort_values(ascending=False)

    st.success(f"Jogador {selected_player} foi selecionado.")

    player_passes = dfCRVGPass[dfCRVGPass['Player'] == selected_player]

    num_passesCJ1 = player_passes[player_passes['outcomeType/displayName'] == 'Successful'].shape[0]
    num_passesJ1 = player_passes.shape[0]
    num_passesPJ1 = len(player_passes[(player_passes['progressive_pass']) & (player_passes['outcomeType/displayName'] == 'Successful')])
    taxa_acertoJ1 = round(((num_passesCJ1 / num_passesJ1) * 100), 1)
    dfPass1 = player_passes[(player_passes['outcomeType/displayName'] == 'Successful') & (~player_passes['progressive_pass'])]
    dfPass1P = player_passes[(player_passes['progressive_pass']) & (player_passes['outcomeType/displayName'] == 'Successful')]

    pitch = mplsoccer.VerticalPitch(positional=False, pitch_type='opta', pitch_color='#222222', line_color='white', line_zorder=2)
    fig, axs = pitch.grid(ncols=1, axis=False, figheight=10, endnote_height=0, endnote_space=0, title_height=0.01, grid_height=0.75)

    pitch.lines(dfPass1['x'], dfPass1['y'], dfPass1['endX'], dfPass1['endY'], color='gray',
                comet=True, transparent=True, alpha_start=0.2, alpha_end=0.8,
                zorder=2, ax=axs['pitch'])

    pitch.scatter(dfPass1['endX'], dfPass1['endY'], color='black', edgecolor='gray', ax=axs['pitch'],
                  s=50, lw=1, zorder=2)

    pitch.lines(dfPass1P['x'], dfPass1P['y'], dfPass1P['endX'], dfPass1P['endY'], color='#97c1e7',
                comet=True, transparent=True, alpha_start=0.2, alpha_end=0.8,
                zorder=2, ax=axs['pitch'])

    pitch.scatter(dfPass1P['endX'], dfPass1P['endY'], color='black', edgecolor='#97c1e7', ax=axs['pitch'],
                  s=50, lw=1, zorder=2)
    

    selected_rounds = ", ".join([name.split(" ")[1] for name in selected_options])
    fig.suptitle(f'Brasileirão 2024 | Vasco da Gama', fontsize=20, fontweight='bold', color='white')
    subtitle = (f'Rodadas: {selected_rounds}')
    fig.text(0.5, 0.93, subtitle, ha='center', fontsize = 14, color='white')

    axs['pitch'].set_title(f'Passes certos do {selected_player}', fontsize=18, color='white', pad=10)

    axs['pitch'].text(0.03, -0.02, f'Passes: {num_passesCJ1}/{num_passesJ1} ({taxa_acertoJ1}% de acerto)', fontsize=14, color='white', ha='left', va='bottom', fontweight='bold', transform=axs['pitch'].transAxes)
    axs['pitch'].text(0.03, -0.05, f'{num_passesPJ1} passes progressivos', fontsize=14, color='#97c1e7', ha='left', va='bottom', fontweight='bold', transform=axs['pitch'].transAxes)

    note_text = "@Vasco_Analytics | Dados: Opta via WhoScored"
    note_text_2 = "Passe progressivo: com ponto final no mínimo 25% mais próximo do gol do que o ponto inicial"
    fig.text(-0.12, 0.04, note_text, fontsize=12, color='gray', ha='left', va='center', weight='bold')
    fig.text(-0.12, 0.02, note_text_2, fontsize=9.5, color='gray', ha='left', va='center')

    fig.patch.set_facecolor('#222222')

    st.pyplot(fig)
else:
    st.write("Nenhum conjunto de dados selecionado ou os dados estão vazios.")
