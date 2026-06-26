# discord.py Patterns

Use this reference when working in Python with discord.py or close forks.

## Preferred Structure

- `bot.py` or `main.py`
- `cogs/` for modular features
- `utils/` for helpers

## Command Guidance

Prefer:
- app commands for modern UX
- hybrid commands when both slash and prefix support are useful
- cogs for grouped features

## Safety

- Request only required intents.
- Validate permissions and role hierarchy before moderation actions.
- Avoid long blocking work in command handlers.

## Common Pitfalls

- Missing `message_content` intent for prefix commands
- Syncing app commands incorrectly
- Not awaiting async calls
- Mixing examples from incompatible forks
