# Omi Wearable Setup

## What is Omi?

Omi is an open-source AI wearable pendant that captures ambient audio and streams transcripts via webhook. Percept uses it for real-time meeting capture without any meeting software integration needed.

## Setup

1. **Get an Omi device** — [omi.me](https://omi.me)
2. **Pair with phone** via Omi mobile app
3. **Start Percept receiver**:
   ```bash
   percept serve --port 8900
   ```
4. **Configure webhook** in Omi app:
   - Settings → Developer → Webhook URL
   - URL: `https://your-host/webhook/transcript?token=YOUR_TOKEN`
   - Set `PERCEPT_WEBHOOK_SECRET` to match your token

## How It Works

1. Omi captures audio → transcribes on-device or via Omi cloud
2. Sends transcript segments to Percept webhook
3. Percept buffers segments, detects conversation boundaries (3s silence)
4. Runs through CIL pipeline: speaker identification, entity extraction, summary generation
5. Stored in Percept DB, searchable immediately

## Security

- **Speaker authorization**: Only approved speakers trigger voice commands
- **Webhook auth**: Bearer token required on all incoming webhooks
- **All blocked attempts logged** in security audit trail

```bash
# Authorize a speaker
percept authorize-speaker SPEAKER_0 --name "David"

# View security log
percept security-log
```

## Tips

- Omi works in any meeting — Zoom, Teams, in-person, phone calls
- No calendar integration needed — it captures everything ambient
- Speaker IDs are consistent within sessions but may vary across sessions
- Name speakers via `percept authorize-speaker` for better context
