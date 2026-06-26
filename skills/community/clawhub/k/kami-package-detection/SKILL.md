---
name: kami-package-detection
description: A free skill by Kami SmartHome. Continuously monitors RTSP camera streams for packages, parcels, and bags using YOLO-World ONNX. Smart deduplication only triggers alerts when a genuinely new or moved package appears.
version: 1.1.0
author: kami-smarthome
tags:
  - smart-home
  - kami
  - home-assistant
  - smarthome
  - detect
  - object-detection
  - yolo
  - package-detection
  - parcel-detection
  - iot
  - camera
  - rtsp
  - onnx
  - edge-ai
  - delivery
  - monitoring
  - notification
triggers:
  - smart home
  - kami
  - home assistant
  - detect
  - detect packages
  - detect parcels
  - kami package
  - kami smart home
  - home assistant package
  - smart home delivery
  - check doorstep
  - delivery notification
  - check for deliveries
  - package detection
  - is there a package
  - monitor packages
  - check camera for packages
  - any deliveries at the door
  - parcel alert
metadata:
  openclaw:
    requires:
      bins:
        - python3.10
      hardware:
        cpu: "2+ cores (x86_64 / ARM64)"
        memory: "2 GB+"
        storage: "2 GB+"
        gpu: "optional (speeds up ONNX inference)"
      network:
        - "RTSP camera access (LAN)"
        - "Internet (KamiClaw API)"
      devices:
        - "RTSP IP camera"
    emoji: "📦"
---

# Kami Package Detection

> Continuously monitors your camera and sends instant notifications when a new package arrives.

Continuously monitors RTSP camera streams for packages, parcels, backpacks, and suitcases. People and handbags are recognized by the model but suppressed at the alert layer to cut down on false alarms. When a **new** package is detected (position/size significantly different from the last alert), sends push notifications. Static frames are automatically skipped to save compute.

### Features

- 📦 Continuous package & parcel monitoring (not one-shot)
- 🔔 Push notifications via Feishu / Telegram / Discord
- 🧠 Smart deduplication — only alerts for new or moved packages (IoU + area change), with a **24-hour tracking window** to silence repeated alerts on the same parcel
- ⚡ Static frame filtering — skips inference when camera scene is unchanged
- 📷 Multi-camera support with independent background processes
- 🧳 Suitcase / backpack recognition
- 🏠 Doorstep & reception monitoring

### Scenarios

- Doorstep delivery waiting
- Office reception package management
- Warehouse cargo monitoring
- Temporary item watch

## Installation

```bash
bash setup.sh
```

Creates `.venv/` and installs `onnxruntime`, `opencv-python-headless`, `numpy`, `requests`. Idempotent.

## Prerequisites

- `python3` and `python3-venv` installed
- RTSP camera(s) online and reachable
- Internet access on first run (to download `yolov8s-worldv2.pt` if not bundled)

### Model

The `yolov8s-worldv2.onnx` model file is auto-prepared by `setup.sh` using a download-first, export-fallback strategy:

1. If `yolov8s-worldv2.onnx` is already present → reused as-is.
2. Otherwise, `setup.sh` downloads the pre-built archive `kami-package-detection.zip` from <https://publicfiles.xiaoyi.com/kami-package-detection.zip> and extracts `yolov8s-worldv2.onnx` out of it (fast path, no extra dependencies).
3. If the download or extraction fails (offline / mirror unreachable), `setup.sh` falls back to installing `ultralytics` into the venv (one-time, ~500 MB with torch) and runs [export_model.py](file:///./export_model.py), which loads `yolov8s-worldv2.pt` (auto-downloaded by Ultralytics if absent), injects the custom vocabulary via `set_classes()`, and exports to ONNX with `imgsz=320`.

Manual export / re-export:

```bash
# Re-export even if the ONNX already exists
.venv/bin/python export_model.py --force

# Custom image size
.venv/bin/python export_model.py --imgsz 320
```

If you change the class list, edit `CLASS_NAMES` in **both** [export_model.py](file:///./export_model.py) and `DEFAULT_CLASS_NAMES` in [yolo_world_onnx.py](file:///./yolo_world_onnx.py) to keep them in sync (same order, same length), then re-export with `--force`.

## Parameter Confirmation

Parameters can be supplied via either `config.json` (recommended for repeated use) or command-line flags. Command-line flags override `config.json`, which overrides built-in defaults.

| Parameter | `config.json` field | Default | Description |
|-----------|---------------------|---------|-------------|
| `--device` | *(selects from cameras array)* | first camera | Target camera DEVICE_ID |
| `--rtsp_url` | `cameras[].rtsp_url` | — | RTSP camera URL (overrides camera selection) |
| `--conf_threshold` | `conf_threshold` | `0.25` | Confidence threshold (0.0–1.0) |
| `--class_names` | *(not in config.json)* | `parcel package "delivery box" person "Cardboard box" "Packaging Box" backpack handbag suitcase` | Classes to detect (CLI only) |
| `--run_time` | `run_time` | `0` | Max seconds; `0` = unlimited (continuous monitoring) |
| `--start-detect` | — | — | Start background detection (all cameras or `--device`) |
| `--stop-detect` | — | — | Stop background detection (all cameras or `--device`) |
| `--status` | — | — | Check detection process status |
| `--list-devices` | — | — | List all configured cameras and exit |
| — | `alarm_cooldown` | `60` | Min seconds between notifications for different packages |
| — | `feishu_webhook_url` | — | Feishu Webhook URL for push notifications |
| — | `telegram_bot_token` | — | Telegram Bot token |
| — | `telegram_chat_id` | — | Telegram chat ID |
| — | `discord_webhook_url` | — | Discord Webhook URL |
| — | `discord_bot_token` | — | Discord Bot token |
| — | `discord_channel_id` | — | Discord channel ID |

### Multi-Camera Configuration

`config.json` supports a `cameras` array for multiple cameras:

```json
{
  "cameras": [
    {
      "rtsp_url": "rtsp://192.168.1.100/stream",
      "device_id": "CAM-FRONT"
    },
    {
      "rtsp_url": "rtsp://192.168.1.101/stream",
      "device_id": "CAM-BACK",
      "conf_threshold": 0.3
    }
  ],
  "conf_threshold": 0.25,
  "run_time": 0,
  "alarm_cooldown": 60,
  "feishu_webhook_url": "",
  "telegram_bot_token": "",
  "telegram_chat_id": "",
  "discord_webhook_url": ""
}
```

- `device_id` must be unique across all cameras
- Per-camera `conf_threshold` and `run_time` override global values
- Without `--device`, all cameras are started/stopped together
- Each camera runs as an independent background process
- Legacy single-camera config (flat `rtsp_url` at top level) is still supported

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

**Ask the user: do any parameters need to be changed?**

## Usage

### Start Detection (Background)

```bash
# Start all cameras
.venv/bin/python yolo_world_onnx.py --start-detect

# Start a specific camera
.venv/bin/python yolo_world_onnx.py --start-detect --device CAM-FRONT
```

### Stop Detection

```bash
# Stop all cameras
.venv/bin/python yolo_world_onnx.py --stop-detect

# Stop a specific camera
.venv/bin/python yolo_world_onnx.py --stop-detect --device CAM-FRONT
```

### Check Status

```bash
# Status of all cameras
.venv/bin/python yolo_world_onnx.py --status

# Status of a specific camera
.venv/bin/python yolo_world_onnx.py --status --device CAM-FRONT
```

### Single-Run Mode (Foreground)

```bash
# Run continuous monitoring on a specific camera (foreground)
.venv/bin/python yolo_world_onnx.py --device CAM-FRONT

# Override via CLI (runs for 120 seconds then stops)
.venv/bin/python yolo_world_onnx.py \
  --rtsp_url rtsp://your-camera-address \
  --run_time 120

# List configured cameras
.venv/bin/python yolo_world_onnx.py --list-devices
```

## Output (stdout JSON)

When a new package is detected, outputs an alarm JSON to stdout:

```json
{
  "alarm": true,
  "type": "package",
  "class_name": "parcel",
  "confidence": 0.87,
  "camera_name": "CAM-FRONT",
  "frame": 1523,
  "snapshot": "/path/to/snapshots/CAM-FRONT/20260604_153012_482.jpg",
  "detections": [
    {
      "class_name": "parcel",
      "bbox": {"x1": 100, "y1": 200, "x2": 300, "y2": 400}
    }
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `alarm` | bool | Always `true` for alarm output |
| `type` | string | Always `"package"` |
| `class_name` | string | Detected object class |
| `confidence` | float | Detection confidence (0.0–1.0) |
| `camera_name` | string | Source camera device_id |
| `frame` | int | Frame number when detected |
| `snapshot` | string | Absolute path to the annotated JPG (with bounding box drawn) |
| `bbox.x1, y1, x2, y2` | int | Bounding box coordinates |

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Normal exit (run_time reached or manual stop via signal) |
| `1` | Error (model missing, RTSP failure, runtime exception) |

## Troubleshooting

- `bash: .venv/bin/python: No such file or directory` → Run `bash setup.sh`
- `Model file not found` → Place `yolov8s-worldv2.onnx` in the skill directory
- `Cannot open video` → Check camera is online and `--rtsp_url` is correct

## Privacy Notice

This skill processes camera video stream frames for object detection. Please review the following privacy information before use:

### Pure Local Inference

- Detection runs entirely on-device via the YOLOv8-World ONNX model — **no cloud API calls for inference**
- The only outbound traffic is: RTSP pull from your camera (LAN) + notification push to your configured channels (Feishu / Telegram / Discord)

### Local Data Storage

- Frames are held in memory only and discarded after each inference — **nothing is persisted to disk by default**
- When an alarm fires, the annotated frame is saved as a JPEG under `snapshots/<camera_device_id>/` for evidence; nothing else is persisted
- The skill emits alarm JSON objects to **stdout**; if you need history, the caller is responsible for storing it

### Notification Channels

- Push notifications are sent only when configured (all channels are optional)
- Notification content includes: detected class name, confidence, camera name, and timestamp
- No images or video frames are sent in notifications

### User Control

- Camera URL is supplied by the user; this skill will not auto-discover or connect to cameras
- You can stop the skill at any time via `--stop-detect` or SIGTERM
- Removing the skill directory wipes everything (model file + venv); nothing else is touched on the host

> For more details on our privacy policy, visit: https://kamiclaw-skill.kamihome.com/privacy
