# URBTIX Events Skill

Fetches upcoming event data from URBTIX (Hong Kong) and detects changes, filtering out noise.

## Prerequisites

Ensure the agent's workspace directory is writable; the skill creates a `urbtix_cache` subfolder for caching.

## Data Source

Official URBTIX batch XML distribution via Tencent COS CDN:
`https://fs-open-1304240968.cos.ap-hongkong.myqcloud.com/prod/gprd/URBTIX_eventBatch_YYYYMMDD.xml`

The XML includes a `<SYSTEM>URBTIX</SYSTEM>` marker that is verified upon download.

## Tools

### `queryEvents`

Answers natural language questions about URBTIX events by parsing the query, fetching the appropriate batch XML, and returning matching performances. Handles date parsing (HK time), venue/name extraction, and validation.

**Parameters:**
- `question` (required): Natural language question about events, e.g., "When is Medea showing?", "Where is 美狄亞 on April 8?", "What performances are on 2026-04-10?"
- `force_refresh` (optional): If true, ignore cached XML and re-download. Default: false.
- `language` (optional): Response language - "en" for English, "zh" for Traditional Chinese. Default: "en".

**Returns:** A dictionary with:
- `answer`: Human-readable answer in **markdown table format** with columns: Time | Event | Venue | Ticket Link (English) or 時間 | 節目 | 場地 | 購票連結 (Traditional Chinese). Includes ticket links where available.
- `matches`: List of matching events, each containing:
  - `event_name_en`: English event title
  - `event_name_tc`: Traditional Chinese event title
  - `venue`: Venue name (English)
  - `venue_tc`: Venue name (Traditional Chinese)
  - `date`: Performance date (YYYY-MM-DD)
  - `time`: Performance time (HH:MM)
  - `reference_link`: URL to official booking page
- `clarification_needed`: If unable to match, what additional info is needed

## Caching & Performance

- Caches raw XML batches per day to reduce load on URBTIX servers
- Cache location: `$OPENCLAW_WORKSPACE/urbtix_cache/URBTIX_eventBatch_YYYYMMDD.xml`
- Cache TTL: 1 day by default
- Network fetch timeout: 10s

## Installation

1. Ensure skill directory exists: `$OPENCLAW_WORKSPACE/skills/hk-urbtix-events/`
2. No dependencies required (uses Python standard library)
3. Add `"hk-urbtix-events"` to the desired agent's `skills` array (Jax recommended)

## Version

1.0.4 — Security hardening: fixed dead code in download validation, corrected rate-limit logic, added language parameter (en/zh), cache purge notifications, timezone-aware datetime handling, atomic file writes.

## Security & Authenticity

- The skill downloads batch XML files from the official URBTIX cloud distribution endpoint.
- Upon download, it verifies the XML contains `<SYSTEM>URBTIX</SYSTEM>` to ensure the data is authentic.
- Additional validation: SEND_DATE matching, TOTAL count verification, XML structure parsing.
- Rate limiting: At most one download attempt per batch date per HK day (enforced via lock files with actual attempt date tracking).
- Atomic writes: Downloads use temporary files renamed on success to prevent partial/corrupt cache.
- Files are cached in `$OPENCLAW_WORKSPACE/urbtix_cache/` to minimize network calls.
- No credentials are used; only environment variable `OPENCLAW_WORKSPACE` (standard).
- Cache purging: Optional verbose notification when old files are removed (default silent for background use).

## Notes

- Respectful polling: Do not call more than once per hour without `force_refresh`.
- This skill uses the official URBTIX batch distribution endpoint; data is authoritative but may be delayed.
- Event data is subject to change; always verify with official source before purchasing tickets.
- Language support: Both English and Traditional Chinese output formats available via `language` parameter.

## Fast CLI Tool

A standalone CLI tool `urbtix_fast.py` is included for quick lookups:

```bash
cd /opt/data/.hermes/skills/hk-urbtix-events
python3 urbtix_fast.py "Andy Lau"
python3 urbtix_fast.py --lang zh "劉德華"
python3 urbtix_fast.py "Leon Lai" "黎明"
```

The CLI tool auto-downloads today's XML batch to `~/.urbtix_cache/urbtix_cache/` on first run, then searches locally.
