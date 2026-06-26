---
name: imessage-notify
description: Send iMessage notifications to iPhone via Mac's Messages app. Supports text, images, videos, audio, files, and URLs. Use when the user wants to send notifications, alerts, or messages to their iPhone from Clawdbot tasks. Triggers on phrases like "send notification to phone", "notify me via iMessage", "message my iPhone", or any request to send iMessage alerts from automated tasks.
---

# iMessage Notification Skill

Send iMessage notifications to your iPhone using Mac's Messages app via AppleScript.
**Features**: Text, Images, Videos, Audio, Files, URLs (with preview)

## Prerequisites

- Mac mini (or Mac) with Messages app open and signed in
- iPhone signed into the same Apple ID (iMessage)
- Apple ID: fan.xia@qq.com

## Quick Usage

### Simple Text Message
```bash
./scripts/send-imessage.sh "Your notification message"
# Or shortcut:
~/Document/code/clawd/notify "Hello!"
```

### Multimedia Messages
```bash
# Text only
./scripts/send-imessage-media.sh -t "Task completed!"

# Send image
./scripts/send-imessage-media.sh -i ~/Desktop/screenshot.png

# Send video
./scripts/send-imessage-media.sh -v ~/Movies/clip.mp4

# Send audio/voice
./scripts/send-imessage-media.sh -a ~/Desktop/recording.m4a

# Send any file
./scripts/send-imessage-media.sh -f ~/Documents/report.pdf

# Send URL (displays preview)
./scripts/send-imessage-media.sh -u "https://www.apple.com"

# Combined: Text + Image
./scripts/send-imessage-media.sh -t "Check this:" -i ~/Desktop/chart.png

# Combined: Text + Link
./scripts/send-imessage-media.sh -t "Found this:" -u "https://example.com"
```

### Shortcuts
```bash
# Quick text
cd ~/Document/code/clawd && ./notify "Hello"

# Quick multimedia
cd ~/Document/code/clawd && ./notify-media -t "Done!" -i result.png
```

## From Clawdbot Tasks

### Simple notification
```bash
# At the end of a task:
~/Document/code/clawd/notify "🎉 Build finished!"
```

### With screenshot
```bash
# Take screenshot and send
screencapture -i ~/Desktop/result.png
~/Document/code/clawd/notify-media -t "Error occurred:" -i ~/Desktop/result.png
```

### Task completion with file
```bash
# Generate report and notify
./generate-report.sh
~/Document/code/clawd/notify-media -t "Report ready:" -f ~/output/report.pdf
```

## Options Reference

| Option | Description | Example |
|--------|-------------|---------|
| `-t, --text` | Text message | `-t "Hello"` |
| `-i, --image` | Image file | `-i photo.jpg` |
| `-v, --video` | Video file | `-v clip.mp4` |
| `-a, --audio` | Audio file | `-a voice.m4a` |
| `-f, --file` | Any file | `-f doc.pdf` |
| `-u, --url` | URL with preview | `-u "https://..."` |
| `-r, --recipient` | Override recipient | `-r "other@icloud.com"` |
| `-h, --help` | Show help | `-h` |

## Script Reference

- [scripts/send-imessage.sh](scripts/send-imessage.sh) - Simple text messages
- [scripts/send-imessage-media.sh](scripts/send-imessage-media.sh) - Full multimedia support
