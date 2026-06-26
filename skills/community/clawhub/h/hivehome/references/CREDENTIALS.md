# Credentials – where to set them

Skills that need credentials document required env vars; set them in your environment or your agent’s config. Never commit secrets.

## Hive Home

| Variable | Required | Notes |
|----------|----------|--------|
| `HIVE_USERNAME` | Yes | Hive account email |
| `HIVE_PASSWORD` | Yes | Hive account password |
| `HIVE_DEVICE_GROUP_KEY` | For automation | Set after first login with 2FA; use with device key/password to skip 2FA |
| `HIVE_DEVICE_KEY` | For automation | From `session.auth.getDeviceData()` after first login |
| `HIVE_DEVICE_PASSWORD` | For automation | From same device data |

## By platform

| Platform | Where to set |
|----------|---------------|
| **OpenClaw** | `~/.openclaw/openclaw.json` → `skills.entries.hivehome.env` (object of name → value). Optional: `apiKey` with SecretRef for one primary secret. Injected per agent run; not in prompts or logs. |
| **Cursor / generic** | Shell `export` or a local `.env` file (do not commit). Ensure the process that runs the script has these set. |
| **Other agents** | Use the agent’s recommended secret or env injection so the script sees vars at runtime. |

Never paste credentials in chat or store them in the skill directory.
