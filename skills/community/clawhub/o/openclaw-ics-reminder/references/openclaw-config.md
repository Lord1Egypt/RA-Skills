# OpenClaw Config

OpenClaw loads workspace skills from `<workspace>/skills`. Configure this skill under `~/.openclaw/openclaw.json`.

## Example

```json5
{
  skills: {
    entries: {
      "ics-reminder": {
        enabled: true,
        apiKey: "your-reminder-api-token",
        env: {
          REMINDER_API_BASE_URL: "https://your-worker.example.workers.dev"
        }
      }
    }
  }
}
```

## Notes

- The entry key is `ics-reminder` because the skill uses `metadata.clawdbot.skillKey`.
- `apiKey` maps to `REMINDER_API_TOKEN` because the skill declares `metadata.clawdbot.primaryEnv`.
- Set `REMINDER_API_BASE_URL` for every user or environment because each worker deployment can differ.
- For local development, set `REMINDER_API_BASE_URL` explicitly, for example `http://127.0.0.1:8787`.
- Skill and config changes are picked up on the next session, or on the next turn if skill watching is enabled.
