---
name: kamivision-recorder
version: 2.0.0
description: "RTSP/RTMP multi-camera stream recording with AI-powered video search. Start/stop recording, check status, search clips by natural language, list recent events, view logs. Supports multiple cameras simultaneously."
user-invocable: true
disable-model-invocation: false
homepage: https://kamiclaw-skill.kamihome.com
metadata: { "openclaw": { "emoji": "📹", "requires": { "bins": ["python3"], "env": [] }, "hardware": { "required": { "camera": "RTSP-compatible camera", "storage": "30GB available space" }, "optional": { "ram": "8GB minimum, 16GB recommended" } } } }
---
# Kamivision Video Recorder & Search

Record camera streams 24/7 and search footage by natural language description. Supports multiple cameras simultaneously. Setup takes 2 minutes. Sign up at https://kamiclaw-skill.kamihome.com for 200 free credits.

## Capabilities

1. **Start recording** — launch background stream recording (one or more cameras)
2. **Stop recording** — stop background recording (one or more cameras)
3. **Check status** — view recording process status (one or more cameras)
4. **Search video** — find clips by natural language (with optional time range, across cameras)
5. **List recent events** — show recent non-static video events (across cameras)
6. **View logs** — display recording logs

## Trigger Words

| Intent          | Trigger Words                                                             |
| --------------- | ------------------------------------------------------------------------- |
| Start recording | start record, start recording, start camera, start monitor, launch stream |
| Stop recording  | stop record, stop recording, stop camera, stop monitor, kill recording    |
| Check status    | recording status, camera status, is recording, check status               |
| Search video    | search video, find video, find clip, look for, search footage             |
| List recent     | recent events, recent clips, list events, what happened, show recent      |
| View logs       | show logs, view logs, recording logs, check logs                          |

If no trigger word matches, use semantic understanding to route to the closest intent.

## First-Time Setup

Run the setup script to create the virtual environment (Python 3.10+) and install dependencies:

```bash
bash {baseDir}/setup.sh
```

## Pre-Recording Configuration

Before EVERY recording start, follow this flow to confirm camera configuration with the user.

### Flow

1. **Read config** from `{baseDir}/stream_config.json`
2. **Check KAMI_API_KEY** - if empty, tell user to get one at https://kamiclaw-skill.kamihome.com
3. **Ask user**: "How many cameras do you want to record?"
4. **For each camera**, confirm or collect:
   - `DEVICE_ID`: Camera location identifier (e.g., `front-door`, `living-room`, `garage`)
   - `STREAM_URL`: Camera RTSP stream URL (e.g., `rtsp://admin:pass@192.168.1.100:554/stream1`)
5. **Display summary** of all cameras to be recorded, ask for confirmation
6. **Update config** if needed, write back to `{baseDir}/stream_config.json`
7. **Only after user confirms** → start recording

### Required Parameters

#### KAMI_API_KEY (top-level, shared by all cameras)

- **Purpose**: Auth key for Kamivision API (`X-API-Key` header). Required for video description and search.
- **Format**: String starting with `sk_live_`
- **How to get**: Sign up at https://kamiclaw-skill.kamihome.com → API Keys → create/copy key
- **Error behavior**: Invalid key → API returns 401/403, retries up to `KAMI_API_RETRY` times. All fail → recording stops.

#### cameras (array)

Each camera in the `cameras` array requires:

##### DEVICE_ID

- **Purpose**: Unique identifier for the camera, used as folder name and file prefix
- **Format**: English only, no spaces. Use lowercase with hyphens. Examples: `front-door`, `living-room`, `garage`, `backyard`
- **Constraint**: Must be ASCII alphanumeric + hyphens only (used in file paths)

##### STREAM_URL

- **Purpose**: RTSP/RTMP stream URL passed to `cv2.VideoCapture()`
- **Format**: `rtsp://username:password@IP:port/path`
- **How to get**: Check camera admin interface for RTSP URL (Hikvision: `rtsp://user:pass@ip:554/Streaming/Channels/1`, Dahua: `rtsp://user:pass@ip:554/cam/realmonitor?channel=1&subtype=0`)
- **Error behavior**: After 100 consecutive frame failures → reconnect (up to `MAX_RECONNECT` times). All retries fail → that camera's recording stops.

### Configuration Scenarios

**Scenario A: First-time setup (no cameras configured)**
- Tell user: "No cameras configured yet. Need to add camera information."
- Ask: "How many cameras do you want to record?"
- For each camera, ask for DEVICE_ID and STREAM_URL
- Add entries to `cameras` array

**Scenario B: Partial config (some cameras missing info)**
- Show existing configured cameras
- Ask: "Are these camera details correct? Need to modify or add new ones?"
- Update/add as needed

**Scenario C: All cameras already configured**
- Display all configured cameras with their DEVICE_ID and STREAM_URL
- Ask: "Confirm to start recording these cameras? Or need to modify?"
- Proceed only after user confirms

### Config Structure Example

```json
{
  "KAMI_API_KEY": "sk_live_xxx",
  "KAMI_API_URL": "https://kamiclaw-skill-api.kamihome.com/v1/detect",
  "RETENTION_DAYS": 3,
  "cameras": [
    {
      "DEVICE_ID": "front-door",
      "STREAM_URL": "rtsp://admin:pass@192.168.1.100:554/stream1"
    },
    {
      "DEVICE_ID": "living-room",
      "STREAM_URL": "rtsp://admin:pass@192.168.1.101:554/stream1"
    }
  ]
}
```

Per-camera entries can also override any top-level parameter (e.g. different resolution for a specific camera):

```json
{
  "DEVICE_ID": "garage",
  "STREAM_URL": "rtsp://admin:pass@192.168.1.102:554/stream1",
  "OUTPUT_WIDTH": 1280,
  "OUTPUT_HEIGHT": 720
}
```

### Config Update

After user confirms: read config → update changed fields → write back → start recording.

### Backward Compatibility

If the config has no `cameras` array but has top-level `STREAM_URL` and `DEVICE_ID`, treat it as a single-camera setup (legacy mode).

### Common Brand RTSP Templates

**MUST show this table to the user** when configuring cameras, so they can pick a URL pattern based on their brand:

| Brand key | Brand | URL pattern |
|-----------|-------|-------------|
| `hikvision` | Hikvision | `rtsp://{user}:{pwd}@{ip}:554/Streaming/Channels/101` (`101`=ch1 main, `102`=ch1 sub) |
| `dahua` | Dahua | `rtsp://{user}:{pwd}@{ip}:554/cam/realmonitor?channel=1&subtype=0` (`subtype=0` main, `1` sub) |
| `tplink` | TP-Link | `rtsp://{user}:{pwd}@{ip}:554/stream1` (`stream1` main, `stream2` sub) |
| `ezviz` | EZVIZ | `rtsp://admin:{verify_code}@{ip}:554/H264/ch1/main/av_stream` |
| `uniview` | Uniview | `rtsp://{user}:{pwd}@{ip}:554/media/video1` |
| `reolink` | Reolink | `rtsp://{user}:{pwd}@{ip}:554/h264Preview_01_main` |

For 24/7 recording prefer the **main stream** (better quality for later playback).

## Command Execution

All commands use `.venv/bin/python` and `stream_recoder2.py` with `--config {baseDir}/stream_config.json`.

The `--device` parameter is optional and accepts comma-separated DEVICE_IDs. If omitted, the command operates on ALL configured cameras.

### Start Recording

Start all cameras:
```bash
{baseDir}/.venv/bin/python {baseDir}/stream_recoder2.py --config {baseDir}/stream_config.json --start-daemon --log-file {baseDir}/stream_recorder.log
```

Start specific camera(s):
```bash
{baseDir}/.venv/bin/python {baseDir}/stream_recoder2.py --config {baseDir}/stream_config.json --start-daemon --log-file {baseDir}/stream_recorder.log --device front-door
```

```bash
{baseDir}/.venv/bin/python {baseDir}/stream_recoder2.py --config {baseDir}/stream_config.json --start-daemon --log-file {baseDir}/stream_recorder.log --device front-door,living-room
```

Parse JSON output: `status: "started"` → show PID; `status: "already_running"` → show PID; error → show message. For multiple cameras, output contains a `cameras` array with per-camera results.

### Stop Recording

Stop all cameras:
```bash
{baseDir}/.venv/bin/python {baseDir}/stream_recoder2.py --config {baseDir}/stream_config.json --stop-daemon
```

Stop specific camera(s):
```bash
{baseDir}/.venv/bin/python {baseDir}/stream_recoder2.py --config {baseDir}/stream_config.json --stop-daemon --device front-door
```

### Check Status

All cameras:
```bash
{baseDir}/.venv/bin/python {baseDir}/stream_recoder2.py --config {baseDir}/stream_config.json --status
```

Specific camera(s):
```bash
{baseDir}/.venv/bin/python {baseDir}/stream_recoder2.py --config {baseDir}/stream_config.json --status --device front-door,living-room
```

### Search Video

Search across all cameras:
```bash
{baseDir}/.venv/bin/python {baseDir}/stream_recoder2.py --config {baseDir}/stream_config.json --search "QUERY" --json
```

Search specific camera(s):
```bash
{baseDir}/.venv/bin/python {baseDir}/stream_recoder2.py --config {baseDir}/stream_config.json --search "QUERY" --json --device front-door
```

With time range (format `YYYY-MM-DD_HH:MM:SS`):
```bash
{baseDir}/.venv/bin/python {baseDir}/stream_recoder2.py --config {baseDir}/stream_config.json --search "QUERY" --time-start "START" --time-end "END" --json
```

Natural language time ("today morning", "yesterday afternoon") → convert to `YYYY-MM-DD_HH:MM:SS`.

### List Recent Events

```bash
{baseDir}/.venv/bin/python {baseDir}/stream_recoder2.py --config {baseDir}/stream_config.json --list HOURS --json
```

With device filter:
```bash
{baseDir}/.venv/bin/python {baseDir}/stream_recoder2.py --config {baseDir}/stream_config.json --list HOURS --json --device front-door
```

Default HOURS to 24 if not specified.

### View Logs

```bash
tail -100 {baseDir}/stream_recorder.log
```

## Privacy

For privacy policy and data handling details, visit https://kamiclaw-skill.kamihome.com/privacy

## Language

Respond in the same language the user uses.
