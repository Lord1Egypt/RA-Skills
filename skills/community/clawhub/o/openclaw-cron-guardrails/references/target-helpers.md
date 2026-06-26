# Target Helpers

Use explicit targets whenever possible.

## Discord

Prefer explicit prefixes:

- Channel: `channel:<id>`
- User: `user:<id>`

Examples:

- `channel:1480624517117247561`
- `user:753247108445896725`

If the channel uses multiple bot accounts, also set `accountId` explicitly.

## Telegram

Examples:

- Chat only: `-1001234567890`
- Topic (preferred): `-1001234567890:topic:123`
- Topic shorthand: `-1001234567890:123`

## Feishu / Lark

Prefer explicit chat/user ids that match the deployed account and target type.

## WhatsApp

Use normalized recipient format expected by your workspace/account policy.

## Rule of thumb

If the output must go somewhere specific, do not rely on `last`.
Use an explicit target string and, when needed, an explicit account id.