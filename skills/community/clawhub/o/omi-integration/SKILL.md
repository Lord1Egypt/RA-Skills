---
name: omi
description: Sync recordings from Omi AI wearables (Omi, Limitless, etc.) via API and webhooks. Auto-sync transcripts, process recordings, and organize by device/date.
homepage: https://github.com/BasedHardware/omi
metadata: {"clawdbot":{"emoji":"🎙️","requires":{"bins":["curl","jq"]}}}
---

# Omi Integration

Sync and manage recordings from Omi AI wearables (Omi, Limitless pendant, etc.).

## Features

- Auto-sync recordings from Omi backend
- Webhook support for real-time transcripts
- Multi-device support (tag by device)
- Local storage with metadata
- Summary and action item extraction

## Setup

1. Get your Omi API key from https://omi.me/developer or your self-hosted backend
2. Store it securely:
```bash
mkdir -p ~/.config/omi
echo "YOUR_API_KEY" > ~/.config/omi/api_key
chmod 600 ~/.config/omi/api_key
```

3. Configure backend URL (defaults to https://api.omi.me):
```bash
echo "https://api.omi.me" > ~/.config/omi/backend_url
# Or for self-hosted:
echo "https://your-backend.com" > ~/.config/omi/backend_url
```

## Usage

### Sync All Recordings
```bash
omi-sync
```

### Sync Recent (Last 7 Days)
```bash
omi-sync --days 7
```

### List Recordings
```bash
omi-list
```

### Get Recording Details
```bash
omi-get <recording-id>
```

### Process Webhook Payload
```bash
cat webhook-payload.json | omi-webhook-handler
```

## Storage

Recordings are stored in:
```
~/omi_recordings/
├── YYYY-MM-DD/
│   ├── <recording-id>/
│   │   ├── metadata.json
│   │   ├── transcript.txt
│   │   ├── audio.wav (if available)
│   │   └── summary.md
└── index.json
```

## Webhook Setup

Configure your Omi app to send webhooks to your endpoint:
1. Open Omi app → Settings → Developer
2. Create new webhook
3. Enter your webhook URL
4. Select events: `recording.created`, `transcript.updated`

The skill includes a handler (`omi-webhook-handler`) that processes real-time events.

## Multi-Device Support

Recordings are automatically tagged by device:
```json
{
  "recording_id": "rec_123",
  "device_id": "limitless-001",
  "device_name": "Limitless Pendant",
  "device_type": "wearable",
  "context": "work",
  "transcript": "Meeting notes...",
  "created_at": "2026-02-02T15:38:00Z"
}
```

## API Endpoints

Base URL: `https://api.omi.me/v1` (configurable)

- `GET /recordings` - List all recordings
- `GET /recordings/:id` - Get recording details
- `GET /recordings/:id/transcript` - Get transcript
- `GET /recordings/:id/summary` - Get AI summary
- `POST /webhooks/register` - Register webhook endpoint

## Privacy

- All data stored locally
- API key encrypted at rest
- Self-hosted backend supported
- No telemetry or tracking
- Webhook payloads logged for debugging (optional)

## Cron Setup

Auto-sync every hour:
```bash
0 * * * * /path/to/omi-sync --days 1 >> ~/.local/share/omi/sync.log 2>&1
```

Or use Clawdbot cron for integrated scheduling.
