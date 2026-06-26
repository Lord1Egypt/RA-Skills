name: local-life
description: Fornece um dashboard visual com informações locais em tempo real. Ative esta skill quando o usuário perguntar sobre o clima, temperatura, cotação de moedas, ou pedir um resumo geral do dia para uma cidade específica. Gatilhos comuns incluem: "como está o dia em Goiânia?", "resumo do dia", "status local", "local-life", "qual a previsão do tempo para hoje?".



Skill: L

ocal Life

Esta skill transforma o agente em um assistente de contexto local, compilando dados de múltiplas fontes gratuitas em um dashboard formatado e de fácil leitura.

📋 Instruções para o Agente

1. 📍 Localização

•
Identifique a cidade do usuário. Se a cidade não for informada, use Goiânia como padrão.

•
Armazene o nome da cidade em uma variável (ex: CIDADE) para usar nas APIs.

2. ☁️ Coleta de Dados

•
Clima, Astronomia e Fase da Lua:

•
Use curl "https://wttr.in/{CIDADE}?format=j1".

•
Extraia os seguintes dados:

•
current_condition: temp_C, FeelsLikeC, windspeedKmph, humidity, uvIndex.

•
weather -> hourly: chanceofrain.

•
weather -> astronomy: sunrise, sunset, moon_phase.





•
Cotações de Moedas:

•
Use curl "https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL".



•
Feriados Nacionais:

•
Use curl "https://date.nager.at/api/v3/PublicHolidays/2026/BR".

•
Verifique se há algum feriado para a data atual.



3. 🔎 Pesquisa Adicional (Fallback )

•
Qualidade do Ar (AQI): A API wttr.in não fornece este dado. Use uma ferramenta de pesquisa (como a API da Brave) para buscar "qualidade do ar em {CIDADE} hoje" e extraia o status (ex: "Boa", "Moderada", "Ruim").

4. 💡 Lógica de Dicas Contextuais

•
Com base nos dados coletados, gere uma dica contextual (DICA_CONTEXTUAL):

•
Se a chance de chuva for > 30%: "Leve guarda-chuva se sair!"

•
Se o índice UV for > 6: "Use protetor solar hoje."

•
Se a qualidade do ar for "Ruim" ou "Muito Ruim": "Evite exercícios ao ar livre hoje."

•
Se a variação do dólar for > 1%: "O mercado está volátil hoje."



•
Se nenhuma das condições acima for atendida, não exiba a dica.

5. ⚙️ Regras de Formatação

•
Bloco de Código: O output final DEVE ser gerado dentro de um bloco de código (usando ```) para preservar o alinhamento e a formatação ASCII.

•
Tradução: Traduza os nomes das fases da lua (ex: "New Moon" -> "Lua Nova") e as descrições do clima para o Português.

•
Template: Siga rigorosamente o template de saída abaixo, preenchendo as variáveis com os dados coletados.

💻 Template de Saída

O agente deve preencher as variáveis e manter este layout:

Plain Text


🏠 local-life - Tudo sobre onde você mora
------------------------------------------------
📍 [CIDADE] - [DATA ATUAL], [HORA]

☀️ CLIMA AGORA
🌡️ [TEMP]°C (sensação [FEEL]°C)
💨 Vento: [VENTO] km/h
💧 Umidade: [UMIDADE]%
🌦️ Previsão: [PREVISÃO_TEXTO]

📊 ÍNDICES DO DIA
☀️ UV: [UV_INDEX] ([RISCO]) - [DICA_UV]!
🌬️ Qualidade do ar: [AQI_STATUS]
🌅 Sol nasce: [SUNRISE] | põe: [SUNSET]

💰 COTAÇÕES
💵 Dólar: R$ [USD] ([USD_VAR]%)
💶 Euro: R$ [EUR] ([EUR_VAR]%)
₿ Bitcoin: R$ [BTC] ([BTC_VAR]%)

🗓️ HOJE
- [FERIADO_STATUS]
- Lua: [LUA_NOME] [LUA_EMOJI]

💡 DICA: [DICA_CONTEXTUAL]



