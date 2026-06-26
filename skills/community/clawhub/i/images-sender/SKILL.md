---
name: images-sender
description: Send images from Mac to phone via iMessage
---

# Send Image via iMessage

## Function

Send images from Mac to phone number via iMessage/Messages app.

## Usage

### Send Image

When user requests to send an image, automatically send via iMessage to the phone.

### Manual Commands

```bash
# Send image to phone number
python3 ~/.openclaw/workspace/skills/images-sender/scripts/send.py send "phone_number" "/path/to/image.png"
```

## First Time Setup

Set the recipient phone number:

```bash
python3 ~/.openclaw/workspace/skills/images-sender/scripts/send.py config set "your_phone_number"
```

## Image Storage

All images will be automatically copied to:
```
~/Pictures/openclaw-send/
```

The script automatically copies images to this directory before sending to avoid path issues.
