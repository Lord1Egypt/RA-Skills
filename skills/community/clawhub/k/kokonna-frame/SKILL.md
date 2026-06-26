---
name: kokonna-frame
description: Control KoKonna AI e-ink art frames. Upload images, query device info, and manage multiple frames. Use when user asks to "push to frame", "send to frame", "display on frame", or "upload image to frame".
version: 1.2.0
author: KoKonna
tags:
  - smart-home
  - e-ink
  - art-frame
  - image-upload
triggers:
  - "push to frame"
  - "send to frame"
  - "display on frame"
  - "upload to frame"
  - "show on KoKonna"
---

# KoKonna Frame Control

Control KoKonna AI e-ink art frames. Upload images, query device status, and manage multiple frames.

---

## Configuration

Before using this skill, configure your KoKonna devices in `~/.openclaw/skills/kokonna-frame/config.yaml`:

```yaml
api_base_url: "https://api.galaxyguide.cn/openapi"
devices:
  living_room: "your-api-key-here"
  bedroom: "your-api-key-here"
  # Add more devices as needed
```

Get your API key from your KoKonna frame settings at [kokonna.art](https://kokonna.art).

---

## Usage

### Command Line

```bash
# Upload image to a frame (auto-resize)
python3 scripts/upload.py --device living_room --image /path/to/image.jpg

# Upload with custom name
python3 scripts/upload.py --device living_room --image /path/to/image.jpg --name "Sunset"

# Query device info
python3 scripts/device_info.py --device living_room

# Push to all frames
python3 scripts/upload.py --device all --image /path/to/image.jpg --name "Art"
```

### Python API

```python
from kokonna import KoKonnaFrame

# Initialize frame
frame = KoKonnaFrame(device="living_room")

# Upload image
frame.upload_image("/path/to/image.jpg", name="Sunset")

# Get device info
info = frame.get_device_info()
print(info)
```

---

## Features

- **Automatic Resizing**: Images are automatically cropped and resized to match frame display
- **Custom Naming**: Give images meaningful names that display on the frame
- **Multi-Frame Support**: Manage multiple KoKonna frames from one agent
- **Device Status**: Check battery level, online status, and firmware version

---

## Requirements

- Python 3.7+
- `requests` library
- `Pillow` library

Install: `pip install requests Pillow`

---

## About KoKonna

KoKonna is an AI-powered e-ink art frame that brings art, information, and personality into your space.

- **E-ink Display**: Paper-like, low power, beautiful in any light
- **AI Art Generation**: Automatically creates artwork based on preferences
- **Smart Home Integration**: Works with your AI assistant

Learn more at [kokonna.art](https://kokonna.art).
