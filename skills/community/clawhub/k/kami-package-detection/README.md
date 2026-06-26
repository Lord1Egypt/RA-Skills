# 📦 Kami Package Detection

> A free skill by **Kami SmartHome** — get notified the moment a package arrives at your door.

Monitor your RTSP camera feed for packages, parcels, backpacks, and suitcases using YOLOv8-World ONNX inference. People and handbags are recognized by the model but suppressed at the alert layer (so a person carrying their bag past the door does **not** trigger an alarm). When a delivery target is detected, outputs the object class and bounding box as structured JSON to stdout.

### Features

- 📦 Package & parcel detection
- 🧳 Suitcase / backpack recognition
- 🏠 Doorstep & reception monitoring
- ⏱ Configurable detection duration
- 🔔 JSON output for easy integration
- 🖥 CPU-only inference via `onnxruntime` — no GPU required
- 🐍 Isolated `.venv` — zero impact on system Python

### Scenarios

- Doorstep delivery waiting
- Office reception package management
- Warehouse cargo monitoring
- Temporary item watch

## Quick Start

```bash
# 1. Run setup (one-time)
bash setup.sh

# 2. Place your ONNX model file
cp /path/to/yolov8s-worldv2.onnx .

# 3a. Foreground single-run (exits on first detection or timeout)
.venv/bin/python yolo_world_onnx.py \
  --rtsp_url rtsp://192.168.1.100/live/camera01 \
  --conf_threshold 0.25 \
  --class_names parcel package "delivery box" person "Cardboard box" "Packaging Box" backpack handbag suitcase \
  --run_time 120

# 3b. Background daemon for one or more cameras (uses config.json)
.venv/bin/python yolo_world_onnx.py --start-detect
.venv/bin/python yolo_world_onnx.py --status
.venv/bin/python yolo_world_onnx.py --stop-detect
```

## Installation

```bash
bash setup.sh
```

The setup script automatically:
1. Detects system Python (`python3` or `python`), exits with error if not found
2. Creates an isolated virtual environment at `.venv/`
3. Installs Python dependencies from `requirements.txt`

> Idempotent — safe to run multiple times. Won't reinstall existing dependencies.

### Requirements

| Dependency | Version | Purpose |
|------------|---------|---------|
| `onnxruntime` | latest | ONNX model inference engine |
| `opencv-python-headless` | latest | Video capture and image processing |
| `numpy` | latest | Array operations |

### System Prerequisites

- **Python 3.8+** and **python3-venv** (`sudo apt install python3 python3-venv`)
- **ONNX model file**: `yolov8s-worldv2.onnx` in the skill directory
- **RTSP camera**: online and network-reachable

## Usage

### Basic Detection

Parameters can be supplied via either `config.json` (recommended) or command-line flags. CLI flags > `config.json` > built-in defaults.

```bash
# Option 1: Edit config.json once, then just run
.venv/bin/python yolo_world_onnx.py

# Option 2: Override via CLI
.venv/bin/python yolo_world_onnx.py \
  --rtsp_url rtsp://127.0.0.1/live/TNPUSAQ-757597-DRFMY \
  --conf_threshold 0.25 \
  --class_names parcel package "delivery box" person "Cardboard box" "Packaging Box" backpack handbag suitcase \
  --run_time 60
```

### Multi-Camera Configuration

`config.json` supports a `cameras` array so multiple RTSP feeds can run as independent background processes:

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
      "conf_threshold": 0.3,
      "run_time": 120
    }
  ],
  "conf_threshold": 0.25,
  "run_time": 60
}
```

- `device_id` must be unique across all cameras
- Per-camera `conf_threshold` and `run_time` override global values
- Without `--device`, all cameras start/stop together
- Legacy single-camera config (flat `rtsp_url` at top level) is still supported

### Daemon Mode (Multi-Camera)

```bash
# Start all cameras
.venv/bin/python yolo_world_onnx.py --start-detect

# Start a specific camera
.venv/bin/python yolo_world_onnx.py --start-detect --device CAM-FRONT

# Status (all cameras or a specific one)
.venv/bin/python yolo_world_onnx.py --status
.venv/bin/python yolo_world_onnx.py --status --device CAM-FRONT

# Stop (all cameras or a specific one)
.venv/bin/python yolo_world_onnx.py --stop-detect
.venv/bin/python yolo_world_onnx.py --stop-detect --device CAM-FRONT

# List all configured cameras
.venv/bin/python yolo_world_onnx.py --list-devices
```

### Parameters

| Parameter | `config.json` field | Type | Required | Default | Description |
|-----------|---------------------|------|----------|---------|-------------|
| `--rtsp_url` | `rtsp_url` / `cameras[].rtsp_url` | string | No | `rtsp://127.0.0.1/live/TNPUSAQ-757597-DRFMY` | RTSP camera stream URL (overrides camera selection when used directly) |
| `--device` | *(selects from `cameras` array)* | string | No | first camera | Target camera `device_id` (foreground or daemon mode) |
| `--conf_threshold` | `conf_threshold` | float | No | `0.25` | Detection confidence threshold (0.0–1.0) |
| `--class_names` | *(not in config.json)* | string[] | No | `parcel package "delivery box" person "Cardboard box" "Packaging Box" backpack handbag suitcase` | Space-separated class names to detect (CLI only) |
| `--run_time` | `run_time` | int | No | `60` | Max run time in seconds. `0` = unlimited |
| `--start-detect` | — | flag | No | — | Start background detection (all cameras, or one with `--device`) |
| `--stop-detect` | — | flag | No | — | Stop background detection (all cameras, or one with `--device`) |
| `--status` | — | flag | No | — | Check detection process status |
| `--list-devices` | — | flag | No | — | List all configured cameras and exit |

> When installed as part of `kami-smarthome-suite`, `cameras[]`, `conf_threshold` and `run_time` are auto-distributed into `config.json` from the central `kami_config.json`. `class_names` is a per-skill default and not distributed.

## Output Format

When a delivery target is detected, the skill outputs JSON to **stdout** and exits with code `0`:

```json
{
  "detections": [
    {
      "class_name": "parcel",
      "bbox": {"x1": 100, "y1": 200, "x2": 300, "y2": 400}
    }
  ]
}
```

### Field Reference

| Field | Type | Description |
|-------|------|-------------|
| `detections` | array | List of detected objects |
| `detections[].class_name` | string | Detected object class |
| `detections[].bbox.x1` | int | Bounding box left x |
| `detections[].bbox.y1` | int | Bounding box top y |
| `detections[].bbox.x2` | int | Bounding box right x |
| `detections[].bbox.y2` | int | Bounding box bottom y |

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Target detected and JSON output written |
| `1` | Model file missing, RTSP connection failure, or runtime error |
| `2` | Run time exceeded, no target detected (timeout) |

> Exit code `0` = detection success, `2` = timeout with no detection, `1` = error.

## Architecture

```
RTSP Camera → [yolo_world_onnx.py] → JSON stdout
                    │
                    ├── letterbox (preprocessing)
                    ├── ONNX inference (YOLOv8-World)
                    ├── parse_output + NMS (post-processing)
                    └── format_detection_result (JSON output)
```

The skill follows a single-pass detection model:
1. Read frames from RTSP stream
2. Preprocess each frame (letterbox resize to 320×320)
3. Run ONNX inference
4. Parse detections, apply NMS
5. On first delivery-target detection (excluding `person` / `handbag`) → output JSON → exit
6. New detections matching an already-tracked package within the **24-hour tracking window** are silently suppressed (no re-alert), so the same parcel sitting at the door does not spam notifications.

## Error Handling

| Scenario | Behavior | Exit Code |
|----------|----------|-----------|
| Model file (`yolov8s-worldv2.onnx`) not found | Log error, exit immediately | `1` |
| RTSP stream cannot connect | Log error, exit immediately | `1` |
| Model load failure (corrupt ONNX) | Log error, exit immediately | `1` |
| Run time exceeded | Log timeout info, exit | `2` |
| Video stream ends (no more frames) | Log warning, exit | `2` |

## Troubleshooting

### Virtual environment not found
```
bash: .venv/bin/python: No such file or directory
```
**Fix**: Run `bash setup.sh` to initialize the environment.

### Model file missing
```
Model file not found: .../yolov8s-worldv2.onnx
```
**Fix**: `bash setup.sh` will first try to download the pre-built archive from
<https://publicfiles.xiaoyi.com/kami-package-detection.zip> and unpack `yolov8s-worldv2.onnx` automatically.
If the host is unreachable (offline / firewall), it falls back to a local export from `.pt` via
`export_model.py`. As a last resort you can also drop `yolov8s-worldv2.onnx` into the skill directory
manually.

### RTSP connection failure
```
Cannot open video: rtsp://...
```
**Fix**: Verify the camera is online, check the `--rtsp_url` value, and confirm network connectivity.

### Low detection rate
- Try lowering `--conf_threshold` (e.g., `0.15`)
- Ensure the target object class is included in `--class_names`
- Check camera angle and lighting conditions

## File Structure

```
kami-package-detection/
├── .gitignore
├── requirements.txt          # onnxruntime, opencv-python-headless, numpy
├── setup.sh                  # Environment setup with Python auto-detection
├── SKILL.md                  # AI agent instructions + metadata
├── README.md                 # This file
├── yolo_world_onnx.py        # Main detection script
├── yolov8s-worldv2.onnx      # ONNX model file (not included, user-provided)
└── tests/
    └── test_parcel_detection.py
```

## Privacy Notice

This skill processes camera video stream frames for object detection. Please review the following privacy information before use:

### Pure Local Inference

- Detection runs entirely on-device via the YOLOv8-World ONNX model — **no API key, no cloud calls, no external network traffic**
- The only outbound traffic is the RTSP pull from your own camera (LAN)

### Local Data Storage

- Frames are held in memory only and discarded after each inference — **nothing is persisted to disk**
- The skill emits a single JSON object to **stdout**; if you need history, the caller is responsible for storing it

### User Control

- Camera URL is supplied by the user; this skill will not auto-discover or connect to cameras
- You can stop the skill at any time — there is no background daemon, no cache, and no residual data
- Removing the skill directory wipes everything (model file + venv); nothing else is touched on the host

> For more details on our privacy policy, visit: https://kamiclaw-skill.kamihome.com/privacy

## License

MIT-0
