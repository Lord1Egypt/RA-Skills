# OpenClaw automation template

Use a cron job to run the pipeline periodically after installing runtime dependencies.

## Suggested isolated cron job

```json
{
  "name": "hn-podcast-archive-sync",
  "schedule": { "kind": "cron", "expr": "17 */6 * * *", "tz": "Asia/Shanghai" },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "Run the hn-podcast-archive skill pipeline using python3 skills/hn-podcast-archive/scripts/hn_podcast_archive.py --feed-url <RSS_URL> --output-dir /root/.openclaw/workspace/data/hn-podcast-archive --whisper-model turbo. Summarize processed/skipped/failed counts. If ffmpeg/whisper/feedparser are missing, report that clearly and stop.",
    "timeoutSeconds": 3600
  },
  "delivery": { "mode": "announce" }
}
```

## Why isolated

Isolated runs keep recurring archive maintenance separate from the main conversation context and make failures easier to inspect.

## First-run checklist

1. Replace `<RSS_URL>`.
2. Install `ffmpeg`.
3. Install `whisper`.
4. Install `feedparser` into the Python environment used by `python3`.
5. Test the command manually before scheduling.
