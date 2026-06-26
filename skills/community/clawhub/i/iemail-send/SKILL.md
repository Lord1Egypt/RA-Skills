---
name: iemail-send
description: Send transactional email via Iemail OpenAPI. Configure via OpenClaw skill env only.
homepage: https://app.dmartech.cn/
metadata:
  {"openclaw":{"emoji":"📧","requires":{"anyBins":["python3"],"env":["IEMAIL_ACCESS_KEY","IEMAIL_ACCESS_KEY_SECRET","IEMAIL_SENDER"]},"primaryEnv":"IEMAIL_ACCESS_KEY"}}
---

# Iemail Send

Send transactional single email via Dmartech/Iemail OpenAPI using Python.

## Configuration

Configure in `~/.openclaw/openclaw.json`:

```json
"skills": {
  "entries": {
    "iemail-send": {
      "enabled": true,
      "env": {
        "IEMAIL_ACCESS_KEY": "your-access-key",
        "IEMAIL_ACCESS_KEY_SECRET": "your-access-key-secret",
        "IEMAIL_SENDER": "your-sender@example.com"
      }
    }
  }
}
```

| Variable | Description |
|----------|-------------|
| IEMAIL_ACCESS_KEY | OpenAPI access key |
| IEMAIL_ACCESS_KEY_SECRET | OpenAPI access key secret |
| IEMAIL_SENDER | Sender email address (required) |
| IEMAIL_TO | Default recipient (optional) |

## Agent instructions

1. Credentials: Read `~/.openclaw/openclaw.json` or workspace config files. OpenClaw injects env at runtime.
2. Send mail: Run script in workspace:
   ```bash
   python3 {baseDir}/send_email.py --to "recipient@example.com" --subject "Subject" --content "Body"
   ```

## Usage examples

```bash
python3 {baseDir}/send_email.py --to "recipient@example.com" --subject "Hello" --content "Hello from Iemail"
python3 {baseDir}/send_email.py "recipient@example.com" "Hello" "Hello from Iemail"
```

## Troubleshooting

- 401 Unauthorized: Check IP whitelist, key/secret, and system time.
- cannot find senderAddressSn: Check `IEMAIL_SENDER` matches a configured sender address.
