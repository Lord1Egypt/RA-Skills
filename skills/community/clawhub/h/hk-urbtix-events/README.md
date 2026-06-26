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

**Returns:** A dictionary with:
- `answer`: Human-readable answer in **markdown table format** with columns: 時間 | 節目 | 場地 | 購票連結. Includes ticket links where available.
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

1.0.3 — Improved date filtering (performance-level), markdown table output format with ticket links, expanded stop words (events/event), bug fixes.

## Security & Authenticity

- The skill downloads batch XML files from the official URBTIX cloud distribution endpoint.
- Upon download, it verifies the XML contains `<SYSTEM>URBTIX</SYSTEM>` to ensure the data is authentic.
- Files are cached in `$OPENCLAW_WORKSPACE/urbtix_cache/` to minimize network calls.
- No credentials are used; only environment variable `OPENCLAW_WORKSPACE` (standard).

## Notes

- Respectful polling: Do not call more than once per hour without `force_refresh`.
- This skill uses the official URBTIX batch distribution endpoint; data is authoritative but may be delayed.
- Event data is subject to change; always verify with official source before purchasing tickets.
