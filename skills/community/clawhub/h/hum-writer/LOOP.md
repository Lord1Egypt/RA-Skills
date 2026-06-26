# Hum Daily Loop

Run every morning via `python3 scripts/loop.py` or `/hum loop`. Follow each step in order. If a step fails, note it and continue.

Python: `python3` (system default)
Scripts: `skills/hum/scripts`

## Step 1 — Feed Digest

Runs the full feed pipeline: fetch → rank → format → send.

All sources fetch directly via API — no browser automation:
- **X home feed**: Bird API (`filter:follows since:<last_crawled>`)
- **X profiles**: Bird API (`from:<handle> since:<last_crawled>`)
- **Hacker News**: Algolia public API
- **YouTube**: yt-dlp (for `sources.json` YouTube channels)
- **Knowledge sources**: RSS, sitemaps, YouTube transcripts, and podcasts from `knowledge/index.md` — saves full articles to `knowledge/<source>/` and generates feed items

All items merge into `feeds.json`, then rank and format a digest sent via Telegram.

```bash
python3 scripts/loop.py --step digest
```

Or run the full pipeline manually:
```bash
python3 scripts/feed/refresh.py --type all
python3 scripts/feed/ranker.py --input <feeds_file> --output <ranked_file>
python3 scripts/feed/digest.py --input <feeds_file> --youtube-input <youtube_file> --max-posts 12
```

Requires `AUTH_TOKEN` and `CT0` session cookies in `~/.hum/credentials/x.json` (or `HUM_X_AUTH_TOKEN` / `HUM_X_CT0` env vars) for X sources. If missing, X fetch is skipped and the rest still runs.

## Step 2 — Engage (parallel with digest)

Suggest accounts to follow and draft replies for approval. Opens X and LinkedIn in browser for comment/reply checking.

```bash
python3 scripts/loop.py --step engage
```

## Step 3 — Brainstorm

Run `scripts/create/brainstorm.py --max 8`. Present top ideas and ask:
- "Any topics to add to the pipeline?"
- "Want to work on any posts today?"

```bash
python3 scripts/loop.py --step brainstorm
```

## Step 4 — Learn (Sundays only)

Run `/hum learn` as defined in COMMANDS.md. Analyze feed trends, research platform algorithms, update context files.

```bash
python3 scripts/loop.py --step learn
```

## Full loop

```bash
python3 scripts/loop.py                     # full daily loop
python3 scripts/loop.py --dry-run           # format output but don't send
python3 scripts/loop.py --max-posts 15      # override digest size
python3 scripts/loop.py --skip-youtube      # skip YouTube fetch
```
