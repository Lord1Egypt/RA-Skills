---
name: photo-capture
description: Capture a fresh webcam image on macOS, Windows, or Linux. Prefer direct camera capture via ffmpeg so the workflow does not depend on screen-recording, accessibility, or UI automation permissions. Use when the user says things like "拍照", "拍一张", "帮我拍", "take photo", "snap a photo", "capture webcam", "open camera", or asks for a fresh camera-view image.
---

# Photo Capture

Use this skill when the user wants a live camera image captured and sent back.

## Default Behavior

1. Prefer direct webcam capture with `scripts/capture_webcam.py`.
2. Save output under `tmp/` inside the workspace.
3. Reply with `MEDIA:./relative/path.png` or `MEDIA:./relative/path.jpg` so the image is sent back.
4. Only use the old macOS app-window screenshot path when direct camera capture is unavailable.

## Why This Path

Direct camera capture is the default because it works across macOS, Windows, and Linux and does not require pre-configuring screen recording, accessibility, or automation permissions.

The OS may still show a normal one-time camera permission prompt for the terminal or Python process. That is expected and lighter than the old screenshot-based setup.

## Primary Command Path

**Note**: Replace `<skill-dir>` with the actual path where this skill is installed (e.g., `~/.agents/skills/photo-capture` or `~/.openclaw/workspace/skills/photo-capture`).

List available cameras:

```bash
python3 <skill-dir>/scripts/capture_webcam.py --list-devices
```

Capture from the default camera on any supported OS:

```bash
python3 <skill-dir>/scripts/capture_webcam.py --output ./tmp/webcam.jpg
```

Capture from a specific device:

```bash
python3 <skill-dir>/scripts/capture_webcam.py \
  --device "0" \
  --output ./tmp/webcam.jpg
```

Higher resolution capture:

```bash
python3 <skill-dir>/scripts/capture_webcam.py \
  --width 1920 \
  --height 1080 \
  --output ./tmp/webcam-1080p.jpg
```

## Platform Notes

- `macOS`: Uses `ffmpeg` with `avfoundation`. Auto-selects camera index `0` by default.
- `Windows`: Uses `ffmpeg` with `dshow`. Auto-selects the first detected video device.
- `Linux`: Uses `ffmpeg` with `v4l2`. Auto-selects `/dev/video0`-style devices.

## Requirements

- `ffmpeg` must be available in `PATH`.
- A webcam device must be present.
- If multiple cameras exist, use `--list-devices` and then pass `--device` explicitly.

## macOS Fallback

Keep the old app-window screenshot path only as a fallback for macOS environments where direct webcam capture fails.

Photo Booth fallback:

```bash
bash <skill-dir>/scripts/capture_via_app.sh \
  --app "Photo Booth" \
  --layout large \
  --capture window \
  --output ./tmp/photobooth-window-large.png
```

Use that fallback only if the direct `ffmpeg` path fails or the user explicitly wants the Photo Booth or FaceTime UI visible in the image.

## Validation

When updating or debugging this skill:

1. Run `--list-devices` on the target OS.
2. Capture one frame to `tmp/`.
3. Confirm the output file exists and is not empty.
4. On macOS, only reach for the screenshot fallback if direct capture is blocked.