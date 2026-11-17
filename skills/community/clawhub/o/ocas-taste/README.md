# ⚙️ Taste

  <img src="./assets/readme/hero.jpg" width="100%" alt="Taste">

Behavior-driven taste model built from real consumption signals. Scans

**Skill name:** `ocas-taste`
**Version:** 3.6.4
**Type:** 
**Layer:** data-science
**Author:** <agent-name>

---

## 📖 Overview

Behavior-driven taste model built from real consumption signals. Scans

---

## 🔧 Capabilities

- `taste.scan` — scan the user's email and calendar for consumption signals; extract, deduplicate, and promote to signals; queue new items for enrichment
- `taste.scan.calendar` — scan Google Calendar for consumption signals (restaurant reservations, hotel bookings, travel); use for historical backfill of calendar data
- `taste.scan.report` — summarize last scan: extractions processed, signals created, cancellations, dedup matches pending review
- `taste.ingest.signal` — manually record a consumption signal (purchase, visit, play, watch, stay)
- `taste.enrich.item` — enrich an item with taste-relevant attributes via Google Maps lookup and web search
- `taste.query.recommend` — generate recommendations grounded in consumption history, enriched attributes, and frequency patterns; respects dietary restrictions; only suggests new places
- `taste.query.serendipity` — find novel but defensible cross-domain connections
- `taste.model.status` — return model state: signal count, domains active, enrichment coverage, staleness
- `taste.report.weekly` — generate a weekly taste pattern summary
- `taste.journal` — write journal for the current run; called at end of every run
- `taste.update` — pull latest from GitHub source; preserves journals and data
- `taste.sync.spotify` — pull recent Spotify listening history via `scripts/spotify_history_puller.py` (direct API, not MCP); creates/updates music ConsumptionSignals; runs daily via scheduled task. Requires `SPOTIFY_REFRESH_TOKEN` env var.
- **`taste_full_enrich.py` does NOT persist `enriched: true` on source items** — After running the script, verify with: `python3 -c \"import json; items=[json.loads(l) for l in open('items.jsonl') if l.strip()]; print(sum(1 for i in items if not i.get('enriched',False)))\"`. If count unchanged, the enrichment data was effectively lost. Use inline Python enrichment (direct urllib calls to legacy Places API) for reliable persistence. See gotcha \"taste_full_enrich.py enriches items but doesn't set enriched: true\".
- **`scan-calendar` output `signals_created` conflates Styx delta with calendar signals** — The JSON output's `signals_created` field reports the count from the Styx delta step, **not** the calendar promotion step. Calendar signals are promoted to the root `signals.jsonl` via `_process_extractions()` but the output number reflects Styx purchases. To find actual calendar signal count, query `signals.jsonl` for `extraction_source == 'calendar'`. See `references/storage_layout.md` for the two-store architecture.
- **`scan-calendar` is calendar-only — NOT the full pipeline** — `taste_scan.py scan-calendar N` only scans Google Calendar. It does NOT run Styx delta or email scan. Its `signals_created` output field correctly reflects only calendar signals (unlike the `taste:scan` cron job which chains calendar + Styx delta and reports Styx's count). For calendar-only historical backfill, use `scan-calendar 365`. For the full pipeline, use `taste_full_enrich.py`.
- **`scan-historical` DATE BUG — stamps every signal with the scan time (CRITICAL)** — `_extract_from_email` parses the email `Date` header with one rigid `strptime("%a, %d %b %Y %H:%M:%S %z")` and falls back to `datetime.now()` on ANY parse failure. In practice the fallback fires for the vast majority of emails (their `Date` headers don't match that exact format), so all emitted signals get `event_date` = the scan timestamp, NOT the real consumption date. Confirmed 2026-07-07: a 365-day run produced 137/141 signals dated `2026-07-07T09:06:23.xxx` (microsecond-spaced = the loop time). This **maximizes recency bias** — the opposite of the goal — and corrupts the model's temporal decay. **Do NOT use `scan-historical` for historical coverage.** Use `scripts/taste_backfill_v2.py` (designated historical backfill; emits correctly-dated signals, as the existing 5,133-signal dataset shows). Fix: replace the strptime with `email.utils.parsedate_to_datetime()` (robust to varied Date formats). See `references/scan_historical_date_bug.md`.
- **`scan-historical` is email-only — NOT the full pipeline** — `taste_scan.py scan-historical N` only scans Gmail. It does NOT run Styx delta or enrichment. For the full pipeline (Styx delta + enrichment of unenriched items), use `taste_full_enrich.py` instead. The daily `taste:scan` cron (13:12) runs email/calendar scan then delegates to `taste_full_enrich.py` for Styx delta + enrichment. If OAuth is broken, `scan-historical` fails entirely but `taste_full_enrich.py` still works.
- **`scan-historical` output is NOT dedupable by `taste_signals_dedup.py`** — The dedup tool's `signal_key` reads `name`/`normalized_name`, but scan signals use `venue_name` and lack `name`/`normalized_name`. All scan signals get an empty venue key and are silently skipped (false "0 dupes" on `--dry-run`). Combined with the date bug above, re-running `scan-historical` over an already-populated dataset silently pollutes it with un-dedupable, mis-dated signals. If you must run it, verify against the actual signal schema (not the tool's count) and revert if dates are wrong.
- **`taste_scan.py status` and `data-quality` report 0 when run outside the venv** — Both commands use the `TasteSkill` class which resolves `data_dir` differently than the actual data location. Always run via the venv Python (`<hermes-home>/commons/data/ocas-taste/venv/bin/python3`) and verify the data path. For a quick count, use `wc -l signals.jsonl items.jsonl` directly. The `data-quality` subcommand has the same bug as `status` — it is NOT documented in `--help` but it exists and returns 0 for all counts when run outside the venv.
- **`taste_full_enrich.py` schema drift — prefer inline enrichment** — The script at `<hermes-home>/profiles/indigo/skills/ocas-taste/scripts/taste_full_enrich.py` generates `item_id` as `item-{safe_name}` (not UUID), uses `strength` field (not `signal_type`), and produces signals with `source: 'enrichment'` that lack the full schema from `references/styx_delta.md`. Items created by this script have `domain: 'restaurant'` instead of `'food'`. **Preferred approach for cron:** write inline Python via `terminal()` that calls Places API directly via `urllib.request` and writes properly structured records. Confirmed 100% enrichment rate with inline approach (2026-06-16, 36/36 transactions).

---

## 📊 Outputs

See `SKILL.md` for outputs, journals, and persistence rules.

---

## 📄 Files

| File | Purpose |
|---|---|
| `SKILL.md` | Skill definition |
| `references/` | Supporting documentation |
| `scripts/` | Helper scripts |


## Changelog

- [3.6.1] - 2026-05-23
- Security
- Quality
- [3.5.2] - 2026-04-26
- Removed
- [3.5.1] - 2026-04-26
- Security
- [3.5.0] - 2026-04-18

---

## 📚 Documentation

Read `SKILL.md` for operational details, schemas, and validation rules.

Read `references/` for detailed specifications and examples.


---

## 📄 License

MIT License — see `LICENSE` for details.