---
name: nate-b-jones-digest
description: Monitor Nate B Jones's YouTube channel, pull each new video transcript (YouTube captions or auto-transcribed audio), summarize it with an abstract + bullet highlights + reference links, and distribute the digest via email, chat, and/or a document per user-configured outputs.
---

## Overview
Use this skill whenever you need to keep Richard (or any configured subscriber) up to date on new Nate B Jones videos. The workflow:

1. Detect a new upload on https://www.youtube.com/@NateBJones.
2. Retrieve the transcript (official captions first, Whisper fallback if missing).
3. Summarize the video into an abstract, bullet highlights, and a "References & Links" list.
4. Publish according to the installation's config: email, Control UI/Telegram chat, Google Doc, Markdown file, etc.

All runtime options live in `references/config-example.yml`. Copy that file, rename it (e.g. `config.yml`), fill in your preferences, and point the workflow to it.

## 1. Configure
1. Copy `references/config-example.yml` to `config.yml` (or any path you prefer).
2. Fill in:
   - `channel_url` or `channel_id` (the example already targets @NateBJones).
   - `poll_cron` (default daily at 09:00 local).
   - `outputs.email.to`, `outputs.chat.targets`, `outputs.doc.type/path`.
   - API credentials: YouTube Data API key (for upload polling), Gmail/Google Docs auth handled via `gog` skill.
3. Store the config path somewhere easy to reference (e.g. `skills/nate-b-jones-digest/config.yml`).

## 2. Poll for new videos
- Preferred: use the YouTube Data API `playlistItems` endpoint for the channel's uploads playlist. Example:
  ```bash
  curl "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet,contentDetails&maxResults=5&playlistId=UPLOADS_PLAYLIST_ID&key=$YOUTUBE_API_KEY"
  ```
- Lightweight alternative: use `yt-dlp` to check the latest upload ID without downloading video:
  ```bash
  yt-dlp --flat-playlist --dump-json "https://www.youtube.com/@NateBJones/videos" | head -n 1 > latest.json
  jq -r '.id' latest.json
  ```
- Compare the discovered video ID with the last processed ID stored in your run logs (e.g., a simple `last_video.txt` or a Notion/Sheets tracker). Only proceed if it's new.

## 3. Fetch transcripts
1. Try official captions via `youtube_transcript_api`:
   ```python
   from youtube_transcript_api import YouTubeTranscriptApi
   transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
   text = '\n'.join([chunk['text'] for chunk in transcript])
   ```
2. If captions are unavailable, download audio and run Whisper:
   ```bash
   yt-dlp -f 140 -o audio.m4a "https://www.youtube.com/watch?v=$VIDEO_ID"
   whisper audio.m4a --model medium --language en --task transcribe --output_format txt
   ```
3. Save the raw transcript alongside metadata (title, URL, publish date, duration). Keep it in your logs for traceability but do not distribute it by default.

## 4. Summarize
Produce:
- **Abstract (2–3 sentences)** summarizing the thesis of the video.
- **Highlights** – 4–6 bullets (verb-led). Mention timestamps where possible (e.g., `[05:42] Key insight`).
- **References & Links** – always include the YouTube URL and any external resources the video mentions.

Template:
```
# Nate B Jones Daily Digest — {{DATE}}

**Video:** {{TITLE}} ({{DURATION}}) → {{URL}}
**Abstract:** ...

## Highlights
- ...

## References & Links
- {{URL}}
- ...
```

## 5. Publish per config
### Email (uses gog skill)
Do not attach the transcript unless someone explicitly asks for it—email only the digest body linked above.
```bash
GOG_KEYRING_PASSWORD=... gog gmail send \
  --to "{{config.outputs.email.to}}" \
  --subject "Nate B Jones Digest — {{DATE}}" \
  --body-file summary.txt \
  --body-html summary.html
```

### Chat
- **Control UI / Telegram:** paste the summary or use the relevant messaging command (e.g., `message action=send ...`).
- Respect `config.outputs.chat.targets` (list of surfaces).

### Document archive
- **Google Docs:**
  ```bash
  gog docs create "Nate B Jones Digest {{DATE}}" --body summary.md
  gog docs share <docId> --email {{config.outputs.doc.share_with}}
  ```
- **Markdown on disk:** write to the specified path in `outputs.doc.path`.

## 6. Automate (optional)
- Create a cron job or OpenClaw cron entry using `poll_cron` from config. Each run should:
  1. Poll for new video.
  2. If found, fetch transcript, summarize, publish, log the video ID.
- Keep lightweight audit logs (CSV or JSON) so you can prove what was sent and avoid duplicate emails.

## References
- `references/config-example.yml` — copy/edit this to match each installation.
- `youtube_transcript_api` docs: https://pypi.org/project/youtube-transcript-api/
- Whisper CLI: https://github.com/openai/whisper

Stick to the playbook format every time so downstream consumers get consistent digests, and always fall back to Whisper if captions are missing.
