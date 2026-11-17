---
name: hotbee-transcript
description: Use when a user wants audio or video converted to text through HotBee speechToText, including file URL transcription, video URL transcription, or transcript extraction from parsed social videos.
---

# HotBee Audio/Video Transcript

中文名：HotBee 音视频转文字

Only submit media the user owns, is authorized to process, or can lawfully access. Before a live call, explain that it may consume HotBee quota and confirm intent unless already approved. Read `HOTBEE_API_KEY` from the local environment only. Do not echo the key or expose signed/private media query parameters in logs or errors.

Use the package CLI:

```bash
npx -y github:shanye1402-hash/hotbee-social-data-skills#v1.1.0 call transcript --file-url "https://example.com/video.mp4"
```

Use `HOTBEE_API_KEY` only.

Read `references/api.md` for endpoint and parameter details.

Official capability directory: [HotBee Skills](https://www.hotbee.cn/skills)
