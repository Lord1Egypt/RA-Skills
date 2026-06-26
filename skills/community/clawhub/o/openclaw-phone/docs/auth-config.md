# Auth and Config

This skill follows OpenClaw key handling best practice.

## Resolution order

1. Environment variable: `CALLMYCALL_API_KEY`
2. User config: `~/.openclaw/openclaw.json` at `skills.openclaw-phone.apiKey`
3. If missing, prompt for an API key for one-time use in the current task.

## Persist behavior

When the key is provided interactively:

- Use it for the current task only.
- Do not auto-write to config.
- If the user wants persistence, provide manual config instructions:
  - Store at `skills.openclaw-phone.apiKey` in `~/.openclaw/openclaw.json`.

## Security rules

- Never store API keys in this skill repository (`SKILL.md`, `README.md`, `examples/`, `references/`).
- Never store API keys in call memory/state such as `recent_calls`.
- Never echo the full key in chat output.
- Never create scheduler jobs/background tasks to run later with stored credentials.

## Example config shape

```json
{
  "skills": {
    "openclaw-phone": {
      "apiKey": "<redacted>"
    }
  }
}
```
