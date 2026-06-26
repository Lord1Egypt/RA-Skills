# Exemplos de Payloads JSON para Mensagens

O comando `openclaw message send` aceita payloads complexos via JSON para botões, cards adaptativos e componentes específicos (como os do Discord).

## Botões (Telegram e outros compatíveis)
Use o parâmetro `--buttons '<json>'`. O JSON deve ser um array de linhas (rows), onde cada linha contém um array de botões.

### Exemplo: Botões em Linha (Inline Buttons)
```json
[
  [
    { "text": "Google", "url": "https://google.com" },
    { "text": "Ajuda", "callback_data": "help_command" }
  ],
  [
    { "text": "Cancelar", "callback_data": "cancel" }
  ]
]
```

## Adaptive Cards (Google Chat, Teams e outros)
Use o parâmetro `--card '<json>'`. O JSON deve seguir a especificação oficial do Adaptive Cards.

### Exemplo: Card Simples com Texto e Imagem
```json
{
  "type": "AdaptiveCard",
  "body": [
    { "type": "TextBlock", "size": "Medium", "weight": "Bolder", "text": "Título do Card" },
    { "type": "Image", "url": "https://example.com/image.png", "size": "Small" },
    { "type": "TextBlock", "text": "Descrição breve do conteúdo.", "wrap": true }
  ],
  "actions": [
    { "type": "Action.OpenUrl", "title": "Ver Mais", "url": "https://example.com" }
  ],
  "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
  "version": "1.3"
}
```

## Componentes do Discord
Use o parâmetro `--components '<json>'`. O JSON deve seguir a estrutura de componentes do Discord.

### Exemplo: Botões no Discord
```json
[
  {
    "type": 1,
    "components": [
      { "type": 2, "label": "Aceitar", "style": 1, "custom_id": "accept" },
      { "type": 2, "label": "Recusar", "style": 4, "custom_id": "reject" }
    ]
  }
]
```

## Dica: Escapando JSON no Terminal
Ao usar o CLI, prefira utilizar aspas simples (`'`) para envolver o JSON e aspas duplas (`"`) dentro do JSON:
```bash
openclaw message send --channel telegram --target @user --message "Escolha:" --buttons '[[{"text":"Sim","callback_data":"yes"}]]'
```
