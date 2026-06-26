# ohmytoken-tracker

This skill tracks LLM token consumption and reports it to ohmytoken.dev for visualization.

## Setup

1. Sign up at https://ohmytoken.dev (Google/GitHub login)
2. Copy your API Key from the welcome screen or Settings page
3. Set the `OHMYTOKEN_API_KEY` environment variable in your OpenClaw config

## What it does

After each LLM response, this tracker automatically:
- Extracts the model name, prompt tokens, and completion tokens
- Reports them to the ohmytoken API
- Your bead board updates in real-time at https://ohmytoken.dev

## Configuration

Add to your `openclaw.json`:

```json
{
  "skills": {
    "ohmytoken-tracker": {
      "enabled": true,
      "config": {
        "api_key": "omt_your_key_here",
        "endpoint": "https://api.ohmytoken.dev/api/v1/ingest"
      }
    }
  }
}
```

No other configuration needed. The tracker runs silently in the background.
