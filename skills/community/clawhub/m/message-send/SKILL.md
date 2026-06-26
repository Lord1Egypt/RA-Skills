---
name: message-send
description: Instruções e fluxo de trabalho para o comando openclaw message send. Utilize para enviar mensagens, mídias e payloads complexos (botões/cards) para múltiplos canais de chat como WhatsApp, Telegram, Discord e Slack.
---

# Skill: message-send

Esta skill fornece orientação procedural para o envio de mensagens através do comando `openclaw message send`.

## Fluxo de Trabalho Recomendado

Siga estes passos para garantir que a mensagem seja enviada corretamente para o destino desejado:

1.  **Verificar Canais Ativos**: Execute `openclaw channels list` para confirmar quais canais estão configurados e habilitados.
2.  **Identificar o Alvo (Target)**: Se não possuir o ID exato do contato ou grupo, utilize o comando `openclaw directory` para pesquisar.
    -   `openclaw directory peers list --channel <canal> --query "<nome>"`
    -   `openclaw directory groups list --channel <canal>`
3.  **Enviar a Mensagem**: Execute o comando de envio com os parâmetros necessários.
    -   **Simples**: `openclaw message send --channel <canal> --target <id> --message "Sua mensagem aqui"`
    -   **Com Mídia**: `openclaw message send --channel <canal> --target <id> --media "/caminho/para/arquivo.png"` (opcional: inclua `--message` para legenda).
    -   **Com Botões**: Utilize `--buttons '<json>'`. Veja exemplos em [references/payloads.md](references/payloads.md).

## Opções Comuns

-   `--channel`: O serviço de chat (ex: `whatsapp`, `telegram`, `discord`, `slack`).
-   `--target`: O ID do destino (E.164 para números, @username ou ID numérico para outros). Veja detalhes em [references/channels.md](references/channels.md).
-   `--message`: O texto da mensagem.
-   `--reply-to`: O ID de uma mensagem para responder (se suportado pelo canal).
-   `--silent`: Envia sem notificação (suportado no Telegram e Discord).
-   `--dry-run`: Exibe o payload mas não envia a mensagem. Útil para depurar JSONs complexos.

## Casos Especiais e Referências

-   **Detalhes de Canais**: Para saber os tipos de IDs aceitos por cada canal, consulte [references/channels.md](references/channels.md).
-   **JSONs para Cards e Botões**: Para enviar botões, adaptive cards ou componentes do Discord, consulte [references/payloads.md](references/payloads.md).
-   **Multi-contas**: Se houver mais de uma conta no mesmo canal, especifique a conta com `--account <id>`.
