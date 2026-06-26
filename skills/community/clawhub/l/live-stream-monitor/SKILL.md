---
name: live-stream-monitor
description: "Monitor live streams (YouTube, Bilibili) and get notified when specific keywords are mentioned. Uses browser SpeechRecognition API for real-time transcription. Trigger when: (1) User wants to monitor a stream for keywords, (2) Need live transcription of streams, (3) Alert when specific words are mentioned."
---

# live-stream-monitor

Monitor live streams and get notified when keywords are mentioned!

## What It Does

- Monitor live streams in real-time
- Alert when your keywords are mentioned
- Speech-to-text transcription via browser

## Features

- ⭐ **Keyword Alerts** - Set keywords, get instant notifications
- **Live Detection** - Auto-detect stream start/end
- **Speech Transcription** - Real-time speech-to-text

## Supported Platforms

- YouTube Live
- Bilibili Live

## Usage

```
Monitor [keyword] on [stream URL]
Example: Monitor "discount" on https://youtube.com/watch?v=xxx
```

## Requirements

- Browser with microphone access
- SpeechRecognition API support (Chrome/Edge)

## Note

Uses browser's built-in SpeechRecognition API for transcription - no external APIs needed!
