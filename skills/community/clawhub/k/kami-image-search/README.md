# Kami Image Search

Capture frames from video streams or import local images. Uses the Kamivision cloud API to generate image descriptions + text embeddings (2048-dim) in a single call, with FAISS vector indexing for natural language image retrieval.

## Architecture

```
Camera RTSP stream / Local image import
        │
        ▼
   Frame capture & dedup (pixel diff detection)
        │
        ▼
   Kamivision SUMMARY API (returns description + embedding)
        │
        ▼
   FAISS IndexFlatIP + SQLite storage
        │
        ▼
   Natural language query → Kamivision EMBED API → vector matching → ranked results
```

## Quick Start

### 1. Setup

```bash
bash setup.sh
```

Checks Python 3.10 (auto-installs via conda/pyenv if missing), creates Python virtual environment, installs dependencies.

### 2. Configure

Edit `image_config.json` (multi-camera example):

```json
{
  "cameras": [
    {
      "STREAM_URL": "rtsp://admin:password@192.168.1.100:554/stream1",
      "DEVICE_ID": "CAM-FRONT",
      "CAPTURE_INTERVAL": 10
    },
    {
      "STREAM_URL": "rtsp://admin:password@192.168.1.101:554/stream1",
      "DEVICE_ID": "CAM-BACK",
      "CAPTURE_INTERVAL": 15
    }
  ],
  "KAMIVISION_API_KEY": "your-api-key-here"
}
```

Each camera runs as an independent background process; `DEVICE_ID` must be unique. Legacy single-camera config (flat `STREAM_URL` / `DEVICE_ID` at top level, without the `cameras` array) is still supported.

> `KAMIVISION_API_KEY` is required. If you don't have one, register at [Kamivision Flow](https://kamiclaw-skill.kamihome.com/) to obtain it.

### 3. Usage

```bash
# Start background frame capture (all cameras)
python image_search.py --start-capture

# Start a specific camera
python image_search.py --start-capture --device CAM-FRONT

# Check capture status (all cameras or a specific one)
python image_search.py --status
python image_search.py --status --device CAM-FRONT

# Stop capture (all cameras or a specific one)
python image_search.py --stop-capture
python image_search.py --stop-capture --device CAM-FRONT

# Import local images
python image_search.py --import /path/to/photos/ --json

# Natural language search across all cameras
python image_search.py --search "person in blue jacket" --json

# Search a specific camera only
python image_search.py --search "keys on the table" --device CAM-FRONT --json

# Search with time range
python image_search.py --search "keys" --time-start 1777010000 --time-end 1777013000 --json

# List images from the last 24 hours
python image_search.py --list 24
```

## Configuration

| Field | Description | Default |
|-------|-------------|---------|
| `cameras` | Camera list (array). Each entry requires `STREAM_URL` and `DEVICE_ID` | — |
| `cameras[].STREAM_URL` | Per-camera video stream URL (RTSP/RTMP/HTTP) | `""` |
| `cameras[].DEVICE_ID` | Per-camera unique identifier | `CAM-001` |
| `cameras[].CAPTURE_INTERVAL` | Per-camera capture interval (overrides global, seconds) | `10` |
| `STREAM_URL` | Legacy single-camera stream URL (when `cameras` array is absent) | `""` |
| `DEVICE_ID` | Legacy single-camera identifier (when `cameras` array is absent) | `CAM-001` |
| `CAPTURE_INTERVAL` | Global default capture interval (seconds) | `10` |
| `OUTPUT_WIDTH` / `OUTPUT_HEIGHT` | Output image dimensions | `640` × `360` |
| `ENABLE_DESCRIPTION` | Enable image description generation | `true` |
| `VLM_PROMPT` | Custom prompt (empty = cloud default) | `""` |
| `KAMIVISION_API_URL` | Kamivision API endpoint | `https://kamiclaw-skill-api.kamihome.com/v1/detect` |
| `KAMIVISION_API_KEY` | Kamivision API key (shared across all cameras) | — |
| `SIMILARITY_THRESHOLD` | Search similarity threshold | `0.35` |
| `SEARCH_TOP_K` | Max results returned | `5` |
| `DATA_DIR` | Data storage directory | `./image_data` |
| `RETENTION_DAYS` | Data retention days (0 = keep forever) | `30` |
| `SKIP_DUPLICATE` | Skip duplicate frames | `true` |
| `DUPLICATE_THRESHOLD` | Duplicate frame pixel diff threshold | `5.0` |
| `TIME_ZONE_OFFSET` | Timezone offset (hours) | `-12` |

## Cloud API

All AI capabilities are provided by the Kamivision cloud API — no local models required:

- `SUMMARY`: Takes image base64, returns description (summary) + text embedding (2048-dim)
- `EMBED`: Takes query text, returns text embedding (2048-dim)

Both operate in the same text vector space, enabling direct similarity matching.

## Data Storage Structure

Each camera owns its own subdirectory named after its `DEVICE_ID`:

```
image_data/
├── CAM-FRONT/
│   ├── 20260423/
│   │   ├── CAM-FRONT_1777010097.jpg
│   │   └── ...
│   ├── imported/          # Images from --import
│   ├── metadata.db        # SQLite metadata
│   ├── faiss.index        # FAISS vector index
│   └── capturer.pid       # Background daemon PID
└── CAM-BACK/
    └── ...
```

## CLI Parameters

| Parameter | Description |
|-----------|-------------|
| `--start-capture` | Start background frame capture (all cameras, or one when paired with `--device`) |
| `--stop-capture` | Stop background capture (all cameras, or one when paired with `--device`) |
| `--status` | Check capture process status (all cameras, or one when paired with `--device`) |
| `--device DEVICE_ID` | Target a specific camera for the operation above |
| `--import PATH` | Import image file or directory |
| `--search TEXT` | Natural language search (optionally narrowed by `--device`) |
| `--list HOURS` | List images from last N hours |
| `--json` | JSON output format |
| `--time-start TS` | Search start time (unix timestamp) |
| `--time-end TS` | Search end time (unix timestamp) |
| `--config PATH` | Config file path |
| `--log-file PATH` | Log file path |
| `--log-level LEVEL` | Log level (DEBUG/INFO/WARNING/ERROR) |
| `--export-config` | Export current config to JSON |

## Dependencies

- Python 3.10 (setup.sh auto-installs via conda/pyenv if missing)
- Kamivision API key

Python packages (setup.sh installs into .venv):
- opencv-python-headless
- numpy
- requests
- Pillow
- faiss-cpu
