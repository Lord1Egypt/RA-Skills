# Discord Bot Planning

Use this reference when the user asks for a new Discord bot from scratch or a substantial multi-feature bot.

## Scope Checklist

Clarify or infer:
- Primary purpose of the bot
- Target server size and audience
- Required features
- Whether slash commands, prefix commands, or both are needed
- Whether persistent storage is required
- Whether dashboard/webhook/external API integration is required
- Hosting target: local, VPS, Docker, PaaS, serverless worker, etc.

## Safe Defaults

Prefer:
- slash commands
- modular command/event layout
- environment variable secrets
- guild-scoped command registration during development
- least-privilege intents
- SQLite for small persistent bots unless the project already uses something else

## Common Feature Sets

### Utility Bot
- ping
- info
- role tools
- reminders
- logging

### Moderation Bot
- timeout
- warn
- kick/ban
- purge
- mod logs
- appeal/ticket flow

### Community Bot
- welcome
- auto-role
- reaction roles or button roles
- leveling or reputation
- FAQ/help

### Support Bot
- tickets
- transcripts
- close/reopen flow
- staff claims
- feedback collection

## Delivery Pattern

For new bots, usually provide:
- project skeleton
- dependency list
- environment variable template
- startup command
- command registration command or script
- short deploy notes
