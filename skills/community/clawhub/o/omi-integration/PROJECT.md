# Omi Integration & Unified Voice Capture - Project Documentation

**Status:** ✅ Complete  
**Completed:** 2026-02-02  
**Owner:** Doc + Clawdia  

---

## 🎯 Project Overview

A complete voice capture system supporting multiple devices from Plaud and Omi families, with real-time webhook support and unified storage.

### Problem Solved

**Before:** 
- Couldn't connect multiple Plaud devices simultaneously (NotePin + Note)
- Had to disconnect one device to use another in Omi app
- No unified view of recordings across devices

**After:**
- Each device has independent profile and sync
- Multiple devices of same type work simultaneously
- Unified storage and search across all devices

---

## 📦 What Was Built

### Task 1: Omi Integration Skill ✅

**Location:** `/home/doc/clawd-opencode/omi-integration/`

**Scripts:**
- `omi-sync.sh` - Sync recordings from Omi API
- `omi-webhook-handler.sh` - Process webhook payloads
- `omi-list.sh` - List and preview recordings
- `SKILL.md` - Full documentation

**Features:**
- Pull recordings from Omi backend API
- Process metadata, transcripts, and summaries
- Store locally in `~/omi_recordings/`
- Support for multiple Omi-compatible devices

**Storage Structure:**
```
~/omi_recordings/
├── YYYY-MM-DD/
│   └── <recording-id>/
│       ├── metadata.json
│       ├── transcript.txt
│       └── summary.md
└── index.json
```

---

### Task 2: Webhook Endpoint ✅

**Location:** `/home/doc/clawd-opencode/omi-integration/`

**Components:**

#### 1. Webhook Server (`webhook-server.py`)
- **Language:** Python 3
- **Port:** 8765 (configurable via `OMI_WEBHOOK_PORT`)
- **Protocol:** HTTP POST
- **Endpoints:**
  - `POST /omi/webhook` - Receive Omi webhooks
  - `GET /health` - Health check

**Security:**
- Optional webhook secret (`OMI_WEBHOOK_SECRET`)
- Bearer token authentication
- Payload validation

**Event Types Supported:**
- `recording.created` - New recording started
- `transcript.updated` - Real-time transcript updates
- `recording.completed` - Recording finalized

**Process Flow:**
1. Omi device → Webhook server (via ngrok)
2. Server validates payload
3. Calls `omi-webhook-handler.sh`
4. Handler saves to `~/omi_recordings/`
5. Returns success response

#### 2. Management Scripts

**`start-webhook-server.sh`**
- Starts webhook server in background
- Creates PID file at `~/.config/omi/webhook-server.pid`
- Logs to `~/omi_recordings/.webhook-server.log`
- Checks for existing server before starting

**`stop-webhook-server.sh`**
- Stops running webhook server
- Cleans up PID file
- Optionally stops ngrok tunnel

**`setup-ngrok.sh`**
- Creates ngrok tunnel to expose webhook
- Generates public URL for Omi app configuration
- Saves URL to `~/.config/omi/ngrok_url`
- Provides setup instructions

#### 3. Configuration

**Environment Variables:**
```bash
OMI_WEBHOOK_PORT=8765           # Server port (default: 8765)
OMI_WEBHOOK_SECRET=your-secret  # Optional auth secret
```

**File Locations:**
- Server PID: `~/.config/omi/webhook-server.pid`
- ngrok URL: `~/.config/omi/ngrok_url`
- Server logs: `~/omi_recordings/.webhook-server.log`
- Webhook logs: `~/omi_recordings/.webhook.log`

#### 4. Deployment Instructions

**Start webhook server:**
```bash
cd /home/doc/clawd-opencode/omi-integration
./start-webhook-server.sh
```

**Expose to internet:**
```bash
./setup-ngrok.sh
```

**Configure in Omi app:**
1. Open Omi app → Settings → Developer
2. Create new webhook
3. Enter ngrok URL (e.g., `https://abc123.ngrok-free.app/omi/webhook`)
4. Select events: `recording.created`, `transcript.updated`

**Monitor activity:**
```bash
# Watch server logs
tail -f ~/omi_recordings/.webhook-server.log

# Watch webhook events
tail -f ~/omi_recordings/.webhook.log

# Check ngrok dashboard
open http://localhost:4040
```

**Stop server:**
```bash
./stop-webhook-server.sh
```

---

### Task 3: Unified Voice Capture Interface ✅

**Location:** `/home/doc/clawd-opencode/voice-capture-hub/`

**Core Concept:**
Device registry system where each physical device gets its own profile, credentials, and storage directory.

**Components:**

#### 1. Device Registration (`register-device.sh`)

**Purpose:** Add new voice capture devices to the system

**Usage:**
```bash
./register-device.sh --type TYPE --name NAME --model MODEL --context CONTEXT
```

**Arguments:**
- `--type` - Device type: `plaud` or `omi`
- `--name` - Unique identifier (e.g., `notepin-work`)
- `--model` - Device model (NotePin, Note, Limitless, Omi)
- `--context` - Context tag (work, personal, meeting)
- `--color` - Display color (optional)

**What it creates:**
- Entry in `~/voice_recordings/devices.json`
- Storage directory: `~/voice_recordings/{type}/{name}/`
- Config directory: `~/.config/voice-capture/{type}/{name}/`

**Example:**
```bash
# Register work NotePin
./register-device.sh --type plaud --name notepin-work \
  --model NotePin --context work --color blue

# Register personal Note
./register-device.sh --type plaud --name note-personal \
  --model Note --context personal --color green
```

#### 2. Device Sync (`sync-device.sh`)

**Purpose:** Sync recordings from a specific device

**Usage:**
```bash
./sync-device.sh DEVICE_NAME [--days N]
```

**Process:**
1. Reads device profile from `devices.json`
2. Loads device-specific credentials
3. Calls appropriate sync script (Plaud or Omi)
4. Saves to device-specific directory
5. Updates last sync timestamp

**Credential Files:**

**For Plaud devices:**
```
~/.config/voice-capture/plaud/{device-name}/email
~/.config/voice-capture/plaud/{device-name}/password
```

**For Omi devices:**
```
~/.config/voice-capture/omi/{device-name}/api_key
```

#### 3. Sync All Devices (`sync-all.sh`)

**Purpose:** Sync all registered devices in parallel

**Usage:**
```bash
./sync-all.sh [--type plaud|omi] [--days N]
```

**Features:**
- Syncs all enabled devices
- Optional type filter (only plaud or only omi)
- Shows success/failure count
- Rebuilds unified index after sync

#### 4. List Recordings (`list-recordings.sh`)

**Purpose:** View recordings across all devices with filtering

**Usage:**
```bash
./list-recordings.sh [OPTIONS]

Options:
  --device DEVICE    Filter by device name
  --context CONTEXT  Filter by context (work, personal)
  --days N          Show last N days (default: 7)
  --all             Show all recordings
```

**Display Format:**
```
📱 Device: notepin-work (plaud)
   Context: work

  🎙️  Meeting with team
     Date: 2026-02-02T14:30:00Z
     Duration: 1800s
     ID: rec_abc123
     Preview: Discussed project timeline...
```

#### 5. Unified Index (`rebuild-index.sh`)

**Purpose:** Create searchable index of all recordings

**Output:** `~/voice_recordings/index.json`

**Structure:**
```json
[
  {
    "id": "rec_123",
    "title": "Meeting notes",
    "created_at": "2026-02-02T14:30:00Z",
    "device_id": "notepin-work",
    "device_type": "plaud",
    "context": "work",
    "transcript": "...",
    "duration": 1800
  }
]
```

---

## 📁 Storage Architecture

### Unified Storage Location
```
~/voice_recordings/
├── devices.json          # Device registry
├── index.json            # Unified search index
├── plaud/                # Plaud devices
│   ├── notepin-work/     # Device-specific storage
│   │   └── 2026-02-02/
│   │       └── <rec-id>/
│   │           ├── metadata.json
│   │           └── transcript.txt
│   └── note-personal/
│       └── 2026-02-02/
└── omi/                  # Omi devices
    ├── limitless-work/
    │   └── 2026-02-02/
    └── omi-personal/
        └── 2026-02-02/
```

### Device Registry (`devices.json`)
```json
{
  "devices": [
    {
      "id": "notepin-work",
      "type": "plaud",
      "model": "NotePin",
      "name": "Work NotePin",
      "context": "work",
      "color": "blue",
      "enabled": true,
      "created": "2026-02-02T15:57:00Z",
      "last_sync": "2026-02-02T16:00:00Z"
    }
  ]
}
```

---

## 🔐 Security & Privacy

### Data Storage
- ✅ All recordings stored locally
- ✅ No cloud storage required
- ✅ Self-hosted backend supported (Omi)

### Credentials
- ✅ Device-specific credential storage
- ✅ File permissions: 600 (owner read/write only)
- ✅ Encrypted at rest via filesystem

### Webhook Security
- ✅ Optional webhook secret
- ✅ Bearer token authentication
- ✅ Payload validation
- ✅ Isolated handler execution

---

## 🚀 Usage Guide

### Initial Setup

**1. Register your devices:**
```bash
cd /home/doc/clawd-opencode/voice-capture-hub

# Plaud NotePin (work)
./register-device.sh --type plaud --name notepin-work \
  --model NotePin --context work

# Plaud Note (personal)
./register-device.sh --type plaud --name note-personal \
  --model Note --context personal

# Limitless (work)
./register-device.sh --type omi --name limitless-work \
  --model Limitless --context work
```

**2. Add credentials:**
```bash
# For each Plaud device
echo "your-email@example.com" > ~/.config/voice-capture/plaud/notepin-work/email
echo "your-password" > ~/.config/voice-capture/plaud/notepin-work/password
chmod 600 ~/.config/voice-capture/plaud/notepin-work/*

# For each Omi device
echo "your-api-key" > ~/.config/voice-capture/omi/limitless-work/api_key
chmod 600 ~/.config/voice-capture/omi/limitless-work/api_key
```

**3. Start webhook server (for real-time):**
```bash
cd /home/doc/clawd-opencode/omi-integration
./start-webhook-server.sh
./setup-ngrok.sh
```

**4. Initial sync:**
```bash
cd /home/doc/clawd-opencode/voice-capture-hub
./sync-all.sh --days 30
```

### Daily Usage

**Sync all devices:**
```bash
./sync-all.sh
```

**View recent recordings:**
```bash
./list-recordings.sh --days 7
```

**View work recordings only:**
```bash
./list-recordings.sh --context work
```

**View specific device:**
```bash
./list-recordings.sh --device notepin-work
```

---

## 🔧 Troubleshooting

### Webhook Server Won't Start

**Check logs:**
```bash
cat ~/omi_recordings/.webhook-server.log
```

**Common issues:**
- Port 8765 already in use
- Python 3 not installed
- Handler script not executable

### ngrok Tunnel Fails

**Check ngrok status:**
```bash
curl http://localhost:4040/api/tunnels
```

**Common issues:**
- ngrok not authenticated (run `ngrok config add-authtoken`)
- Free plan URL expired (restart tunnel)

### Device Sync Fails

**Check device config:**
```bash
ls -la ~/.config/voice-capture/plaud/notepin-work/
```

**Common issues:**
- Missing credentials
- Incorrect permissions (should be 600)
- Device disabled in devices.json

---

## 📊 Monitoring

### Webhook Activity
```bash
tail -f ~/omi_recordings/.webhook.log
```

### Server Status
```bash
curl http://localhost:8765/health
```

### ngrok Dashboard
```bash
open http://localhost:4040
```

### Sync Logs
```bash
cat ~/voice_recordings/.sync.log
```

---

## 🎯 Success Metrics

✅ **All 3 tasks complete**  
✅ **Multiple Plaud devices supported**  
✅ **Multiple Omi devices supported**  
✅ **Real-time webhooks working**  
✅ **Unified storage implemented**  
✅ **Independent sync per device**  
✅ **No connection conflicts**  

---

**Project Complete:** 2026-02-02  
**Ready for:** Production deployment and testing  
**Documentation:** Complete and up-to-date  
