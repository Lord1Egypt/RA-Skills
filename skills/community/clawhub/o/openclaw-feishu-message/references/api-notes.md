# API notes

This plugin assumes Feishu scopes are already granted for:
- employee lookup
- chat creation
- bot message sending

Key scopes observed in this environment include:
- `directory:employee:search`
- `im:chat:create`
- `im:chat:read`
- `im:message:send_as_bot`
- `contact:user.base:readonly`

Practical caveat:
Having scopes does not always guarantee that the bot may DM every user. Tenant policy, app visibility, and bot availability can still block delivery.
