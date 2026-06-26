---
name: minimax-skill
description: Unified MiniMax media generation skill for Token Plan workflows. Use when the user asks to generate audio, speech, TTS, narration, images, illustrations, posters, covers, thumbnails, videos, motion clips, text-to-video, image-to-video, or needs MiniMax API setup instructions across Linux, macOS, Windows, Docker, or CI.
---

# MiniMax Media Generation

Use this skill to generate MiniMax audio, images, and videos from one command surface.

## Requirements

- Python 3
- `requests` package
- `MINIMAX_API_KEY` environment variable

For system-specific API key setup, read `references/setup.md`.

## Unified Command

Run `scripts/minimax.py` with one mode: `audio`, `image`, or `video`.

```bash
python scripts/minimax.py {audio|image|video} [options]
```

## Audio

Generate an MP3 file from text:

```bash
python scripts/minimax.py audio \
  --text "你好，今天我们聊一下 MiniMax。" \
  --output /tmp/minimax-audio.mp3
```

Useful options:

- `--model speech-2.8-turbo` for lower latency
- `--model speech-2.8-hd` for higher fidelity
- `--voice-id <voice_id>` to select a voice when available

## Image

Generate images into a directory:

```bash
python scripts/minimax.py image \
  --prompt "一只穿西装的橘猫，电影感，柔光" \
  --output /tmp/minimax-images \
  --aspect-ratio 1:1
```

Useful options:

- `--model image-01`
- `--model image-01-live` for stronger style control when available
- `--n 2` to request multiple images
- `--image-file <url_or_base64>` for image-to-image workflows when supported

Outputs are saved as `output-0.jpeg`, `output-1.jpeg`, etc.

## Video

Generate a video file:

```bash
python scripts/minimax.py video \
  --prompt "镜头缓慢推进，一只橘猫走过雨夜街道，霓虹灯反光" \
  --output /tmp/minimax-video.mp4
```

Useful options:

- `--model MiniMax-Hailuo-2.3`
- `--first-frame-image <url_or_base64>` for image-to-video
- `--last-frame-image <url_or_base64>` for start/end-frame video
- `--subject-reference '<json>'` for subject reference workflows
- `--timeout 1800` to control polling timeout in seconds

## Direct Scripts

The unified command delegates to standalone scripts in the same skill:

- `scripts/generate_audio.py`
- `scripts/generate_image.py`
- `scripts/generate_video.py`

Use these directly only when a narrower, mode-specific command is preferred.

## Safe Sharing Notes

- Do not include a real API key in the skill package.
- Ask users to configure `MINIMAX_API_KEY` locally.
- Keep generated media outside the skill folder, for example under `/tmp` or a project output directory.
