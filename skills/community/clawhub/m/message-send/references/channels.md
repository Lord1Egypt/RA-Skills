# Canais Suportados pelo OpenClaw

O OpenClaw suporta uma ampla variedade de canais de chat. Cada canal possui suas próprias particularidades para o parâmetro `--target`.

## Resumo dos Canais e Alvos

| Canal | Tipo de Target (Alvo) | Notas |
| :--- | :--- | :--- |
| **whatsapp** | Número de telefone (E.164) ou Group ID | Ex: `+5511999999999` ou `12036302...` |
| **telegram** | Chat ID (numérico) ou @username | Ex: `12345678` ou `@usuario` |
| **discord** | Channel ID ou User ID | Requer IDs numéricos longos do Discord. |
| **slack** | Channel ID (ex: `C12345`) ou User ID | Use `openclaw directory` para obter IDs. |
| **signal** | Número de telefone (E.164) | Ex: `+5511999999999` |
| **imessage** | Apple ID ou Número (E.164) | Funciona apenas em macOS. |
| **googlechat** | Space ID ou User ID | Formato: `spaces/AAAAA...` |
| **matrix** | Room ID ou User ID | Ex: `!room:matrix.org` ou `@user:matrix.org` |

## Como encontrar o ID correto?

Sempre utilize o comando `openclaw directory` antes de enviar para garantir que o ID do alvo está correto.

- Para contatos (usuários): `openclaw directory peers list --channel <canal> --query "<nome>"`
- Para grupos/canais: `openclaw directory groups list --channel <canal>`

## Contas Múltiplas

Se você possuir mais de uma conta conectada ao mesmo canal, utilize o parâmetro `--account <id>` para especificar por qual conta a mensagem deve ser enviada. Você pode ver os IDs das contas em `openclaw config get channels`.
