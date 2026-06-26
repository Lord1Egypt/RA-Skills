# Iemail Send Skill

OpenClaw skill for sending transactional emails through Iemail OpenAPI.

## Features

- Python script with runtime env support
- Supports OpenClaw injected env only
- Auto-query for `emailConfigSn`, `senderAddressSn`, `replyAddressSn`
- Sender enforced as required configuration

## Installation

Place this skill in `workspace/skills/iemail-send/`.

## Configuration

Set env in `~/.openclaw/openclaw.json`:

```json
{
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
}
```

The agent runs `python3 {baseDir}/send_email.py`; OpenClaw injects env at runtime.

## Usage

```bash
python3 {baseDir}/send_email.py --to "recipient@example.com" --subject "Subject" --content "Body text"
python3 {baseDir}/send_email.py "recipient@example.com" "Subject" "Body text"
```
