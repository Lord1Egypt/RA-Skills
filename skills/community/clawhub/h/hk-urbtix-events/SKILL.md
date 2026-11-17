# HK URBTIX Events Skill

Fetches upcoming event data from URBTIX (Hong Kong) and detects changes, filtering out noise.

## Tools

### `queryEvents`

Answers natural language questions about URBTIX events by parsing the query, fetching the appropriate batch XML, and returning matching performances. Handles date parsing (HK time), venue/name extraction, and validation.

**Parameters:**
- `question` (required): Natural language question about events, e.g., "When is Medea showing?", "Where is 美狄亞 on April 8?", "What performances are on 2026-04-10?"
- `force_refresh` (optional): If true, ignore cached XML and re-download. Default: false.
- `language` (optional): Response language - "en" for English, "zh" for Traditional Chinese. Default: "en".

**Returns:** A dictionary with:
- `answer`: Human-readable answer in **markdown table format** (Time | Event | Venue | Ticket Link) or clarification message in the requested language
- `matches`: List of matching events (each with event_name_en, event_name_tc, venue, venue_tc, date, time, reference_link)
- `clarification_needed`: If unable to match, what additional info is needed

See README.md for full details.

## Installation

Place the skill directory under your OpenClaw workspace `skills/` and add `"hk-urbtix-events"` to the desired agent's `skills` array.

## Notes

- Fetches from the official URBTIX cloud distribution endpoint (Tencent COS). The XML includes a `<SYSTEM>URBTIX</SYSTEM>` marker that is verified upon download to ensure authenticity.
- Respectful polling: Do not call more than once per hour without `force_refresh`.
- Caches daily batches in `$OPENCLAW_WORKSPACE/urbtix_cache/` to reduce load.
- No external dependencies (Python standard library only).
- **Security**: Downloads are validated with XML structure verification, source authenticity checks (SYSTEM tag), SEND_DATE matching, and TOTAL count verification. Rate limiting enforced per HK day. Temporary files used for atomic writes. Cache purging with optional verbose notification.

## Version

1.0.4 — Security hardening: fixed dead code in download validation, corrected rate-limit logic, added language parameter (en/zh), cache purge notifications, timezone-aware datetime handling, atomic file writes.
