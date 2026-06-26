# Omi Integration for Clawdbot

Auto-sync and manage recordings from Omi AI wearables (Omi, Limitless pendant, etc.)

## ✅ Task 1: Omi Integration Skill - COMPLETE

**Status:** Ready to use!

### What's Included

1. **`omi-sync.sh`** - Sync recordings from Omi API
2. **`omi-webhook-handler.sh`** - Process real-time webhook events
3. **`omi-list.sh`** - List and preview recordings
4. **`SKILL.md`** - Full documentation

### Quick Start

**Step 1: Get your Omi API key**
- Go to https://omi.me/developer (or your self-hosted backend)
- Create API key
- Store it:
```bash
mkdir -p ~/.config/omi
echo "YOUR_API_KEY" > ~/.config/omi/api_key
chmod 600 ~/.config/omi/api_key
```

**Step 2: Sync your recordings**
```bash
cd /home/doc/clawd-opencode/omi-integration
./omi-sync.sh --days 7
```

**Step 3: View recordings**
```bash
./omi-list.sh --days 7
```

### Storage Location

All recordings are stored in:
```
~/omi_recordings/
├── 2026-02-02/
│   ├── rec_abc123/
│   │   ├── metadata.json
│   │   ├── transcript.txt
│   │   └── summary.md
└── index.json
```

### Features

✅ **Multi-device support** - Works with Omi, Limitless, and other compatible wearables
✅ **Real-time sync** - Webhook support for instant transcripts
✅ **Local storage** - All data stored privately on your machine
✅ **Metadata rich** - Device info, timestamps, summaries
✅ **Easy to use** - Simple bash scripts, no dependencies beyond curl/jq

## ✅ Task 2: Webhook Endpoint Setup - COMPLETE

**Status:** Ready to deploy!

### What's Included

1. **`webhook-server.py`** - Python HTTP server for receiving Omi webhooks
2. **`start-webhook-server.sh`** - Start the webhook server
3. **`stop-webhook-server.sh`** - Stop the webhook server
4. **`setup-ngrok.sh`** - Expose webhook to internet via ngrok

### Quick Start (Webhook)

**Step 1: Start the webhook server**
```bash
./start-webhook-server.sh
```

**Step 2: Expose to internet with ngrok**
```bash
./setup-ngrok.sh
```

**Step 3: Configure in Omi app**
- Open Omi app → Settings → Developer
- Create new webhook
- Enter the ngrok URL from Step 2
- Select events: `recording.created`, `transcript.updated`

**Step 4: Test it!**
- Speak into your Omi/Limitless device
- Watch real-time transcripts arrive
- Check logs: `tail -f ~/omi_recordings/.webhook.log`

### Features

✅ **Real-time transcripts** - Get transcripts as you speak
✅ **Secure** - Optional webhook secret authentication
✅ **Health monitoring** - `/health` endpoint for status checks
✅ **Auto-processing** - Uses existing `omi-webhook-handler.sh`
✅ **Background service** - Runs continuously in background

## Next Steps

**Task 3: Unified Voice Capture Interface** - Coming next!

---

**Created:** 2026-02-02  
**Updated:** 2026-02-02  
**Location:** `/home/doc/clawd-opencode/omi-integration/`  
**Status:** ✅ Task 1 & 2 Complete!
