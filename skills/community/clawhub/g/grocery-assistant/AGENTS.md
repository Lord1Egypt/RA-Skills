# Grocery Checklist Agent Notes

- Keep OpenClaw as the source of truth.
- Treat Telegram as the checklist UI.
- Button callbacks start with `gchk:`.
- Use the local shell wrapper in `scripts/grocery.sh`.
- For clear grocery intents, execute directly and keep replies brief.
- For Telegram checklist rendering, prefer updating one message in place.
