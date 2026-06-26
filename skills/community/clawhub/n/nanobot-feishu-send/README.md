# nanobot-feishu-send

 Send images, files, audio, and video to Feishu via **nanobot**. This skill uses nanobot's `message` tool; uploads and message type selection are handled automatically by the Feishu channel.

[中文说明](README.zh-CN.md)

## What This Skill Does

- Sends **local files** as Feishu attachments
- Supports **images, files, audio (opus), and video**
- Works in the **current Feishu chat** or a specified `chat_id`

## Prerequisites

1. Feishu channel is enabled in `~/.nanobot/config.json`
2. `nanobot gateway` is running
3. The file exists on the **same machine** where nanobot runs

## Installation

- If installed from ClawHub, it will appear under:
  `~/.nanobot/workspace/skills/nanobot-feishu-send`
- Or copy this folder into `~/.nanobot/workspace/skills/`

## Usage (message tool)

**Rule:** Put file paths in `media`, not in `content`.

### Send an image

```json
{
  "content": "Here is the image",
  "media": ["/path/to/photo.png"]
}
```

### Send a file

```json
{
  "content": "Report attached",
  "media": ["/path/to/report.pdf"]
}
```

### Send audio (voice message)

```json
{
  "content": "Voice message",
  "media": ["/path/to/voice.opus"]
}
```

### Send video

```json
{
  "content": "Video attached",
  "media": ["/path/to/video.mp4"]
}
```

### Send to a specific chat (optional)

```json
{
  "channel": "feishu",
  "chat_id": "ou_xxxxx",
  "content": "File sent",
  "media": ["/path/to/report.pdf"]
}
```

## File Type Mapping

- Images: `.png .jpg .jpeg .gif .bmp .webp .ico .tiff .tif`
- Audio: `.opus` (sent as voice message)
- Video: `.mp4 .mov .avi`
- Other: sent as file attachment

## Troubleshooting

- **Only a path is sent**: you put the path in `content`. Move it to `media`.
- **Broken image**: file is empty or not a real image. Replace the file.
- **No message**: file path does not exist on the nanobot machine.

## Security Notes

- Do not send sensitive files by mistake.
- Keep `~/.nanobot/config.json` private.
