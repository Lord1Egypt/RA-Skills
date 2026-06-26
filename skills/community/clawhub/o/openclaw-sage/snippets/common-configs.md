# Common Config Snippets for OpenClaw

## Provider Setup

### Discord
```json
{
  "discord": {
    "token": "${DISCORD_TOKEN}",
    "guilds": {
      "*": {
        "requireMention": false
      }
    }
  }
}
```

### Discord (mention-only mode)
```json
{
  "discord": {
    "token": "${DISCORD_TOKEN}",
    "guilds": {
      "*": {
        "requireMention": true
      }
    }
  }
}
```

### Telegram
```json
{
  "telegram": {
    "token": "${TELEGRAM_TOKEN}"
  }
}
```

### WhatsApp
```json
{
  "whatsapp": {
    "sessionPath": "./whatsapp-sessions"
  }
}
```

### Slack
```json
{
  "slack": {
    "token": "${SLACK_BOT_TOKEN}",
    "appToken": "${SLACK_APP_TOKEN}"
  }
}
```

### Signal
```json
{
  "signal": {
    "phoneNumber": "${SIGNAL_PHONE_NUMBER}"
  }
}
```

### iMessage
```json
{
  "imessage": {
    "handle": "${IMESSAGE_HANDLE}"
  }
}
```

### MS Teams
```json
{
  "msteams": {
    "appId": "${MSTEAMS_APP_ID}",
    "appPassword": "${MSTEAMS_APP_PASSWORD}"
  }
}
```

## Gateway Configuration
```json
{
  "gateway": {
    "host": "0.0.0.0",
    "port": 8080
  }
}
```

## Agent Defaults
```json
{
  "agents": {
    "defaults": {
      "model": "anthropic/claude-sonnet-4-6"
    }
  }
}
```

## Retry Settings
```json
{
  "agents": {
    "defaults": {
      "retry": {
        "maxAttempts": 3,
        "delay": 1000
      }
    }
  }
}
```

## Cron Jobs
```json
{
  "cron": [
    {
      "id": "daily-summary",
      "schedule": "0 9 * * *",
      "task": "summary"
    }
  ]
}
```

## Skills Configuration
```json
{
  "agents": {
    "defaults": {
      "skills": ["bash", "browser"]
    }
  }
}
```

## Tools Configuration
```json
{
  "agents": {
    "defaults": {
      "tools": {
        "bash": { "enabled": true },
        "browser": { "enabled": true }
      }
    }
  }
}
```
