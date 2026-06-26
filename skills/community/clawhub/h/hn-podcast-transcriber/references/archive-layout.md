# HN Podcast Archive Directory Layout

```
hn-podcast-archive/
├── state.json                          # Tracked episode IDs (prevents re-download)
├── 2026-05-07_When_Speed_Outruns_Judgment/
│   ├── episode.mp3                     # Downloaded audio
│   ├── episode.txt                     # Whisper raw transcript
│   ├── transcript.md                   # Cleaned markdown transcript
│   └── metadata.json                   # Title, date, description, audio URL
├── 2026-05-06_The_Rust_Effect/
│   └── ...
└── ...
```

## state.json Schema

```json
{
  "a1b2c3d4e5f6": {
    "transcribed": true,
    "title": "Episode Title",
    "dir": "2026-05-07_Episode_Title"
  }
}
```

Keys are first 12 hex chars of SHA-256 of the audio enclosure URL.

## Scheduling with cron

Run daily to catch new episodes:

```bash
# Example: check for new episodes at 9 AM daily
# Use OpenClaw cron with an agentTurn job that runs:
#   bash /path/to/skills/hn-podcast-transcriber/scripts/fetch_and_transcribe.sh --archive ~/hn-podcast-archive
```