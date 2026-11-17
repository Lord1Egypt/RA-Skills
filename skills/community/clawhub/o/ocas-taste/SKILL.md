---
description: Behavior-driven taste model built from real consumption signals. Scans
  email and calendar for consumption data (restaurant reservations, food delivery,
  hotel bookings, purchases), enriches entities with taste-relevant attributes via
  Google Maps, and generates discovery-focused recommendations that respect dietary
  restrictions. Not for generic search, editorial top-10 lists, or ad-copy
  generation.
includes:
- references/**
- evals/**
- scripts/**
license: MIT
metadata:
  author: Indigo Karasu (indigokarasu)
  version: "3.7.0"
  hermes:
    category: data-science
    config:
      - key: SPOTIFY_REFRESH_TOKEN
        description: OAuth refresh token for Spotify listening-history sync
        default: ""
      - key: GOOGLE_PLACES_API_KEY
        description: Google Places API key used by Styx delta ingestion (no OAuth)
        default: ""
      - key: GOOGLE_MCP_CREDENTIALS
        description: Directory containing Google OAuth token JSON files
        default: ~/.google_workspace_mcp/credentials
    tags:
    - preferences
    - recommendations
    - consumption-signals
    - OCAS-core
name: ocas-taste
source: https://github.com/<agent-handle>/taste
tags:
- preferences
- recommendations
- behavior
- consumption
- OCAS-core
triggers:
- taste model
- consumption signals
- user preferences
- behavioral taste
- preference profile
---

Taste builds a personalized taste model from real consumption signals — purchases, restaurant visits, food delivery orders, hotel stays, music plays, and movie watches. It scans the user's email and calendar to automatically extract these signals, enriches venue entities with taste-relevant attributes (cuisine, price point, neighborhood, vibe) via Google Maps and web search, and uses temporal decay so recent behavior outweighs stale history. Every recommendation names the specific prior consumption that justifies it, respects dietary restrictions, and only suggests places the user hasn't been.

## Interactive Menu

When invoked interactively, present a two-level menu. See `references/interactive-menu.md` for the menu structure and response parsing logic.

## When to Use

- Scanning email and calendar for consumption signals (restaurant bookings, delivery orders, hotel stays, purchases)
- Personalized recommendations grounded in real prior behavior (example: "You liked X, try Y because...")
- Cross-domain discovery based on actual taste signals
- "What else would I like" reasoning with named evidence
- Enriching venue/item entities with taste-relevant attributes
- Taste model status check
- Weekly or periodic taste pattern summary
- Styx→Taste delta ingestion (new restaurant transactions from bank data)

## When NOT to Use

- Generic web research — use Sift
- Editorial/top-10 style recommendations without personalization
- Ad-copy or sales-oriented product suggestions
- Inference of sensitive identity traits from behavior

## Responsibility boundary

Taste owns behavior-driven preference modeling, consumption signal extraction from email/calendar, entity enrichment for taste profiling, and evidence-backed recommendations.

Taste does not own: web research (Sift), social graph (Weave), pattern analysis, browsing interpretation (Thread).

## Ontology types

Taste works with these types from `spec-ocas-ontology.md`:

- **Place** — venues (restaurants, cafes, bars, retail, entertainment spaces). Extracted from consumption events; enriched via Google Maps or Sift.
- **Thing/DigitalArtifact** — consumed media items (articles, videos, podcasts, books, albums). Stored as ItemRecords.
- **Concept/Action** — behavioral actions (consumed, saved, skipped, dismissed, rated). Used as signal types in ConsumptionSignal.
- **Concept/Idea** — cuisines, genres, categories, and other taste dimensions.
- **Entity/Person** — chefs, artists, creators, and other individuals the user likes or follows.

Taste maintains its own preference model in `{agent_root}/commons/data/ocas-taste/`. See `spec-ocas-shared-schemas.md` for ConsumptionSignal and ItemRecord schemas.

## Commands

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

**Script invocations (for cron/headless use):**
- Full pipeline (Styx delta + enrichment): `/usr/bin/python3 <hermes-home>/profiles/indigo/skills/ocas-taste/scripts/taste_full_enrich.py --limit 200`
- Styx merchant enrichment (all categories): `cd <hermes-home>/profiles/indigo/skills/ocas-styx/scripts && /usr/bin/python3 styx_universal_enrich.py`
- Enrichment fix (persist `enriched: true`): `cd <hermes-home>/profiles/indigo/commons/data/ocas-taste && /usr/bin/python3 scripts/taste_enrich_fix.py`
- Email-only historical scan: `/usr/bin/python3 <hermes-home>/profiles/indigo/skills/ocas-taste/scripts/taste_scan.py scan-historical 365`
- Calendar historical scan: `<hermes-venv>/bin/python3.13 <hermes-home>/profiles/indigo/skills/ocas-taste/scripts/taste_scan.py scan-calendar 365`
- Signal dedup: `/usr/bin/python3 scripts/taste_signals_dedup.py` — deduplicates signals after enrichment runs. **Takes no arguments** — runs against the default data path. Confirmed working 2026-06-18 (0 dupes found on 4,056 signals; 46 dupes removed on prior run). Must be run from the data directory: `cd <hermes-home>/profiles/indigo/commons/data/ocas-taste`.
- **Enrichment fix (persist `enriched: true`):** `/usr/bin/python3 scripts/taste_enrich_fix.py` — reliably enriches food/restaurant items via Google Places legacy GET API and persists `enriched: true` on source items. Use after `taste_full_enrich.py` reports success but items remain unenriched. Fixes the `update_item_enriched()` name-matching bug. Supports `--dry-run` and `--limit N`. Confirmed 2026-06-26: fixed The Butcher's Son and Hard Knox Cafe after `taste_full_enrich.py` reported success but left `enriched: false` on disk.
- **Dispatch-wave dedup:** `/usr/bin/python3 <hermes-home>/profiles/indigo/skills/ocas-taste/scripts/dispatch_taste_dedup.py` — broader dedup for dispatch-wave duplicates. Uses key `(venue_name, event_date[:10], extraction_source)`. Run after EVERY dispatch-triggered scan. Confirmed 2026-06-25: removed 74 dupes (4777 → 4703) that `taste_signals_dedup.py` missed. Supports `--dry-run`. **Must be run from the data directory:** `cd <hermes-home>/profiles/indigo/commons/data/ocas-taste && /usr/bin/python3 <hermes-home>/profiles/indigo/skills/ocas-taste/scripts/dispatch_taste_dedup.py`. Confirmed 2026-06-26: relative path `scripts/dispatch_taste_dedup.py` does NOT exist from the data directory — script lives under `skills/`, not `commons/data/`.
- Signal cleanup (generic meal titles): `/usr/bin/python3 <hermes-home>/profiles/indigo/skills/ocas-taste/scripts/clean_signals.py <hermes-home>/profiles/indigo/commons/data/ocas-taste/signals.jsonl` — removes generic meal titles (Breakfast, Lunch, Dinner, Brunch) and deduplicates on `(venue_name, event_date, extraction_source, domain)`. On 2026-06-16 it removed 5,605 duplicate signals (9,310 → 3,705).
- Status check: `wc -l <hermes-home>/commons/data/ocas-taste/signals.jsonl <hermes-home>/commons/data/ocas-taste/items.jsonl` (the `taste_scan.py status` command may report 0 due to path resolution issues — use `wc -l` for ground truth)

**IMPORTANT:** `taste_scan.py` must be run with Python 3.13 (`<hermes-venv>/bin/python3.13`), NOT the ocas-taste venv's Python 3.14 (which lacks `googleapiclient`).

- **Python runtime (confirmed 2026-06-25):** Must use `/usr/bin/python3` (system Python 3.14, has `googleapiclient` after install). NOT `<hermes-venv>/bin/python3.13` — path does not exist. NOT ocas-taste venv's Python — symlinks to system 3.14 but lacks googleapiclient.
  - **Script location:** `<hermes-home>/profiles/indigo/skills/ocas-taste/scripts/taste_scan.py`
  - **Data directory:** `<hermes-home>/profiles/indigo/commons/data/ocas-taste`

**Script location:** The active scripts are under the indigo profile:
```
<hermes-home>/profiles/indigo/skills/ocas-taste/scripts/taste_scan.py
```
Also present (byte-identical, symlink/hardlink-resolved) at `<hermes-home>/skills/ocas-taste/scripts/taste_scan.py` — either path works. The script hardcodes `data_dir = <hermes-home>/commons/data/ocas-taste`; on this system `<hermes-home>/commons` is a symlink to `<hermes-home>/profiles/indigo/commons`, so it resolves to the live dataset (no data split). The older claim that `<hermes-home>/skills/ocas-taste/scripts/` "does not exist" is stale — it does.

## Workflows

All workflows follow a consistent pattern: **extract → dedup → enrich → recommend**.

### Email/calendar scan (`taste.scan`)

**Purpose:** Extract consumption signals from email and calendar, deduplicate, and queue for enrichment.

**Pre-flight:**
- [ ] Load Google OAuth credentials per `references/api_auth.md`. Use the user profile for email; fall back to agent profile only for calendar.
- [ ] **Repair token expiry format:** Before validating tokens, repair any timezone suffix or float expiry using the combined script in `references/token-repair.md`. This must be done immediately before the scan to avoid race conditions with token refresh.
- [ ] If token file is 0 bytes or token still fails with `invalid_grant` after repair, follow `references/cron_failure.md` — don't silently skip. Report auth failure in output.
- [ ] **Gmail/Calendar access check:** When accessing Gmail or Google Calendar, first verify connectivity. If access fails, fall back to standalone `google_auth.py` scripts. A 0-byte token produces an explicit error with re-auth URL. When using standalone scripts, the helper may silently fall back to a different account — always check which account was actually loaded.

**Extract:**
- [ ] Build Gmail query per configured service. Correct form: `({sender_query}) after:{date_str}` — wrong form returns every email after the date.
- [ ] Enumerate writable calendars via `calendarList().list()` (not just `primary`). Filter `accessRole in ('owner', 'writer')`.
- [ ] Extract structured data into ExtractionRecords. Validate: drop records with empty `venue_name` or `from` addresses not matching configured `sender_patterns`.

**Normalize:**
- [ ] Strip `Reservation at ` prefix and city suffixes (` - San Francisco`, ` - SF`, etc.).
- [ ] Apply venue-detection heuristics: exclude medical/video calls/generic meetings; include meal keywords, hotel brands, event types.
- [ ] Classify email_type: confirmation, reminder, update, cancellation, receipt.

**Dedup & persist:**
- [ ] Cross-calendar dedup key: `{service}:{normalized_venue}:{event_date[:10]}`. Same venue on different dates = separate signals.
- [ ] Exclude cancelled events. Promote valid extractions to ConsumptionSignals.
- [ ] Create/update ItemRecords, queue unenriched items.
- [ ] Write journal.

**Edge cases:**
- Empty scan (no new signals): still write evidence record with `not_activity_reason: no_new_signals`.
- Partial parse failure: log error, continue with successfully parsed records.
- Calendar API returns empty: check `accessRole` filter isn't too restrictive; fall back to `primary` only if needed.

See `references/email_extraction.md` for sender allowlist and extraction rules.

### Styx delta ingestion (`taste.styx.delta`)

**Purpose:** Pull new restaurant/food transactions from Styx that aren't yet in Taste, enrich via Google Places API, and persist. This is a **standalone workflow** that does NOT require Google OAuth — it uses the GOOGLE_PLACES_API_KEY env var instead. Runs as part of the daily `taste:scan` cron job.

**Key advantage:** Works even when email/calendar OAuth is broken. Confirmed 2026-05-30: 124 venues enriched, 188 signals created while <operator>'s Gmail token was 0 bytes.

See `references/styx_delta.md` for the full procedure including:
- SQL query for food transactions from styx.db
- Deduplication against existing Taste items and signals
- Google Places text search enrichment (handles Styx's truncated merchant names)
- ItemRecord and ConsumptionSignal schema
- Reporting format

**⚠️ CRITICAL — dedup by canonical `place_id`, NOT by name (incident 2026-07-15):**
When checking whether a Styx transaction is "already in Taste", compare the **Google
`place_id`** returned from Places textsearch against existing items' `place_id`. Do NOT
dedup by normalized `name` or `item_id` — near-names like `"Taco Bell"` vs `"Taco Bell
Cantina"` share one `place_id`, and name-only checks silently create duplicate items
+ signals. If an existing item already has that `place_id`, **LINK** the signal to it
(bump `visit_count`, append `visit_dates`, recompute `avg_amount`) — create no item.
Otherwise create exactly one canonical item for that `place_id`.
**Always run `scripts/verify_taste_delta.py` after the write.** A "N created" success
return is testimony, not proof — verify asserted zero `place_id` collisions, zero
`item_id` duplicates, zero orphaned signals, zero `(merchant,date)` styx dupes. Full
recipe + reconciliation: `references/styx_delta_placeid_dedup.md`.

### Enrichment (`taste.enrich.item`)

**Purpose:** Add taste-relevant attributes (cuisine, price, neighborhood, vibe) to items via Google Maps.

1. Look up unenriched items on Google Maps via Styx (`styx_places_enrich.py`).
2. Extract attributes per `references/enrichment.md`.
3. Use web search to fill gaps if Google Maps data is insufficient: invoke **Sift with `--format=concise`** for item enrichment (high-signal title/url/snippet; ~60–80% token savings). If **Sift is absent**, fall back gracefully to the local SearXNG instance (`http://localhost:8888`) or a plain web search without the Sift tier — never fail the enrichment over a missing Sift skill. See `references/plans/preference-scan.plan.md`.
4. Update ItemRecord metadata, set `enriched: true` and `enriched_at`.
5. Create LinkRecords between items sharing attributes. Persist.

**⚠️ CRITICAL:** Dedup check uses `venue_name`, not `name`. Verify when modifying item schema.

**Edge cases:**
- Google Maps returns no results: fall back to web search, mark with lower confidence.
- Duplicate venue names after normalization: merge only if same normalized name AND same date range.
- **`taste_full_enrich.py` does NOT persist `enriched: true` on source items** — After running the script, verify with: `python3 -c \"import json; items=[json.loads(l) for l in open('items.jsonl') if l.strip()]; print(sum(1 for i in items if not i.get('enriched',False)))\"`. If count unchanged, the enrichment data was effectively lost. Use inline Python enrichment (direct urllib calls to legacy Places API) for reliable persistence. See gotcha \"taste_full_enrich.py enriches items but doesn't set enriched: true\".

Bulk enrich: `python {skill_root}/scripts/styx_places_enrich.py --limit 200`

### Signal ingestion (`taste.ingest.signal`)

1. Receive/normalize input signal. Validate domain and structure.
2. Persist signal, create/update ItemRecord, queue for enrichment if new. Write journal.

### Recommendation (`taste.query.recommend`)

**Purpose:** Generate personalized restaurant/venue recommendations grounded in proven consumption history.

1. Load active signals, apply temporal decay (see `references/signal_policy.md`).
2. Compute effective item strength with frequency and recency bonuses (see `references/strength_model.md`).
3. Rank items by strength within each domain. Identify taste patterns from enriched attributes.
4. Search external sources (Eater SF, Michelin Guide, local food guides) for candidate venues matching identified patterns. See `references/recommendation_analysis.md` for the full analysis procedure including Python code for computing strengths, building the visited venue set, and cross-referencing candidates.
5. Cross-reference every candidate against the visited venue set — never recommend a venue in the user's signal history.
6. Verify against dietary restrictions and that user hasn't visited.
7. Format per `references/recommendation_style.md`. Include evidence-linked explanation citing specific consumed items. Write journal.

**Edge cases:**
- No enriched items available: explain to user that recommendations need enrichment first, trigger a scan.
- All matching venues already visited: expand search radius or relax pattern constraints, explain trade-off to user.
- Dietary restriction matches zero venues: report honestly, don't suggest violating restrictions.

## Cron fallback

Error handling and recovery: See `references/cron_failure.md` for the full fallback procedure. Key points:
- When `invalid_grant` occurs, full re-auth is required — no retry will help.
- When token file is 0 bytes: MCP tools fail visibly with `ACTION REQUIRED`; standalone `google_auth.py` silently falls back.
- Always output the re-auth URL in the scan report when auth fails.
- **Styx delta still runs** even when auth fails — it uses a separate API key.

## Operating invariants

- Evidence-first: recommendations must reference specific consumed items
- Discovery-only: never recommend places the user has already been (exception: seasonal menu changes)
- Dietary safety: never recommend venues that conflict with stated dietary restrictions
- Signal decay: older signals degrade unless reinforced; frequency matters: repeat visits are a strong signal
- No speculative identity inference from taste signals
- Explainability: every recommendation explains the link to prior consumption
- First-party signals outrank enriched metadata
- Confidence reflects actual evidence strength, not rhetorical certainty
- Always use the user's email account, never the agent's account

## Signal weighting and decay

See `references/signal_weighting.md` and `references/strength_model.md` for full model.

## Recovery Behavior

See `references/recovery.md` for the full recovery contract.

## Storage layout

See `references/storage_layout.md` for data directory structure and enrichment pipeline.

## Spotify sync (`taste.sync.spotify`)

See `references/spotify_sync.md` for the full sync procedure.

**Interactive OAuth helper (one-time setup):** When `SPOTIFY_REFRESH_TOKEN` is absent from `.env`, the cron job cannot be fixed headlessly. The staged fix path is:
1. `scripts/spotify_auth_helper.py` — performs the interactive Spotify OAuth Authorization Code flow (auto mode: opens browser + local callback server on port 8888; `--manual` mode: prints URL, paste redirect). Writes `commons/data/ocas-taste/music/spotify_token.json`.
2. `scripts/apply_spotify_token_to_env.py` — bridges the file token into `$HERMES_HOME/../indigo/.env` as `SPOTIFY_REFRESH_TOKEN`.
3. `hermes cron run e0a126b6c9f7` — verify the cron resumes cleanly.

See `references/spotify_oauth_fix.md` for the full manual procedure.

## Journal outputs

See `references/journal.md` for journal format. All signal ingestion, scan, enrichment, query, and report runs write observation journals.

Taste entities default to `user` relevance since they reflect actual preferences and consumption patterns.

## Initialization

See `references/initialization.md` for the full `taste.init` procedure.

## Historical Backfill

For gap-filling historical consumption signals (when cron scans were failing):

- **Don't use `taste_full_enrich.py`** — it only covers Styx→Taste delta, not email/calendar history.
- **Don't use `taste_scan.py scan-historical N`** — it's email-only, no Styx delta, no calendar, AND it has a date-extraction bug that stamps every signal with the scan time (see Gotchas: `scan-historical` DATE BUG). Use `taste_backfill_v2.py`.
- **Use the custom backfill script:** `scripts/taste_backfill_v2.py` — scans Gmail (food-related queries) and Calendar (restaurant/venue-filtered) in monthly chunks, deduplicates against existing signals, writes to `signals.jsonl` and `extractions.jsonl`.
- **Calendar filtering is critical** — without it, ~70% of signals are non-food noise (appointments, meetings, etc.). The backfill script uses positive food keywords and negative skip keywords.
- **Backfill results (2026-06-04):** 1,333 email messages → 265 signals; 517 calendar events → 277 signals (2,275 non-food skipped); 719 previously-inserted bad calendar signals cleaned up.

The 13:12 `taste:scan` job runs the full pipeline: email/calendar scan → **Styx delta** → enrichment → journal. Email/calendar steps may fail independently (OAuth) while Styx delta succeeds (API key).

### Dispatch-triggered scan (cron/dispatch)

When the dispatcher triggers a taste scan (via `taste_new_data` dispatch or cron), the workflow is:

1. **Token repair** — run the combined repair script (see Pre-Scan Token Repair above) BEFORE the scan. Race condition: OAuth refreshes the token between separate terminal calls, re-adding the `+00:00` suffix. Chain repair + scan in a single `terminal()` invocation.
2. **Run `taste_scan.py scan-incremental 24`** — email-only incremental scan for the last 24h. Do NOT use `taste_full_enrich.py` (Styx delta only, not email/calendar) or `scan-historical` (date bug, see Gotchas).
3. **Run `dispatch_taste_dedup.py --dry-run`** — broader dedup for dispatch-wave duplicates. The key `(venue_name, event_date[:10], extraction_source)` catches dupes that `taste_signals_dedup.py` misses. ALWAYS run `--dry-run` first and confirm it opens `signals.jsonl` (printed `Total signals: N`) before applying. If dry-run can't find the file, the applied run also silently no-ops and the journal's `dedup_removed` lies.
4. **Run `dispatch_taste_dedup.py --apply-taste`** — apply the dedup. Check the output for `Written.` confirmation.
5. **Verify counts** — `wc -l signals.jsonl items.jsonl` for ground truth. The `taste_scan.py status` command may report 0 due to path resolution issues.

**⚠️ dispatch_taste_dedup.py path:** Script lives under `skills/ocas-taste/scripts/`, NOT `commons/data/`. Always use absolute path: `/usr/bin/python3 <hermes-home>/profiles/indigo/skills/ocas-taste/scripts/dispatch_taste_dedup.py`. Must be run from the data directory (`cd <data_dir>`) but the script is NOT in the data directory — it resolves paths internally via `AGENT_ROOT`. Placeholder-bug detection rules: see the Gotchas entry.

## Pre-Scan Token Repair (REQUIRED)

Before running ANY taste scan, validate and repair token format. **Five** failure modes exist (confirmed across 2026-06 through 2026-07-27):

1. **Timezone suffix** (`+00:00` or `Z`): `google.auth2.credentials.Credentials` parser fails with `"unconverted data remains: +00:00"`. Fix: `d['expiry'] = d['expiry'][:19]`
2. **Float expiry** (Unix timestamp instead of ISO string): `.rstrip()` call fails with `'float' object has no attribute 'rstrip'`. Fix: `d['expiry'] = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(time.time() + 3600))`
3. **Microsecond suffix** (`.811606`): NOT matched by the `+`/`Z` check; still crashes on `from_authorized_user_file()`. Fix: strip `.NNNNNN` before `[:19]`.
4. **Numeric-string expiry** (Unix timestamp stored as a *quoted* JSON string, e.g. `"1784952387"`): `json.load` yields `str`, so the float branch misses it and the suffix branch passes it through untouched → crashes. Fix: detect a pure-digit string and convert via `time.localtime(int(s))`. **Confirmed 2026-07-26** (`mx.indigo.karasu@gmail.com.json`).
5. **Microsecond fraction + Z suffix** (e.g. `"2026-07-27T18:23:50.151160Z"`): Both microsecond fraction AND `Z` present simultaneously. The combined repair script handles this — strip `Z` first, then strip `.` and fractional seconds — but if you hand-roll a fix, the ordering matters. **Confirmed 2026-07-27** (`mx.indigo.karasu@gmail.com.json`).

The combined repair script in `references/token-repair.md` handles ALL FIVE modes. Use that script — do not hand-roll a partial fix.

**⚠️ CRITICAL RACE CONDITION (confirmed 2026-06-25 dispatch #65):** The OAuth library refreshes the token on every `google_auth.py` initialization. If you run the repair as one `terminal()` call and the scan as a SEPARATE call, the OAuth refresh happens between them — re-adding the `+00:00` suffix. You MUST chain repair + scan in a SINGLE `terminal()` invocation:
```bash
python3 -c "<repair script>" && cd <data_dir> && /usr/bin/python3 <scan_script>
```
Two separate calls WILL fail. The suffix reappears on EVERY OAuth refresh — repair is mandatory before every scan, not a one-time fix.

**Combined repair script:** use the hardened script in `references/token-repair.md` — it handles all five modes above, including the ordering-sensitive microsecond+Z combo. Do not hand-roll a partial fix.
## Command Pattern

```bash
cd <hermes-home>/profiles/indigo/commons/data/ocas-taste && /usr/bin/python3 <hermes-home>/profiles/indigo/skills/ocas-taste/scripts/taste_scan.py scan-incremental 24
```

Output: JSON with `signals_created`, `cancellations`, `services_scanned`, plus detailed `extractions` array.

**Why not `taste_full_enrich.py`?** The full pipeline is for the daily cron job (13:12) that chains email/calendar → Styx delta → enrichment. Dispatch-triggered scans only need the email/calendar incremental pass. If enrichment is needed for new items, run it as a separate step after the scan.

**Why not `scan-historical`?** Historical backfill scans ALL messages in the last N days, which is wasteful when only the last 24h of new data needs processing. Use `scan-incremental 24` for dispatch waves.

## Self-Update

See `references/self-update-taste.md`.

## Gotchas

- **Empty or corrupt token file (0 bytes)** — If the token file is empty or 0 bytes, `json.loads()` fails with \"Expecting value: line 1 column 1\". The `google_auth.py` helper skips that account and silently falls back to the next account in the list (the agent's), which has zero consumption emails. The scan then reports 0 messages across all services with no obvious error. **Diagnosis:** Check file size with `wc -c` on the token file before assuming auth is valid. **Fix:** Re-authorize with the same procedure as `invalid_grant`.
- **Scripts may fall back silently** — When a token is invalid or 0 bytes, standalone auth helpers may silently fall back to a different account. Always verify which account was actually loaded.
- **Styx delta works without Google OAuth** — The Styx→Taste delta ingestion uses GOOGLE_PLACES_API_KEY (env var), not OAuth tokens. It runs successfully even when email/calendar auth is broken. Confirmed 2026-05-30: 124 venues enriched, 188 signals created, $8,174 tracked — all while OAuth token was 0 bytes.
- **Styx merchant names are truncated; Places handles it** — Styx truncates merchant names to ~15 characters. Google Places fuzzy text search resolves these correctly — tested at 100% match rate (124/124). Use `{merchant_name} restaurant` as the query, take the first result. See `references/styx_delta.md`.
- **Styx truncation creates duplicate items** — The enrichment pipeline creates separate items for each truncated Styx variant instead of canonicalizing via Google Places. This results in duplicate items (e.g., Milos split across 3 items, Kasa Indian Eatery across 5). The dedup in `styx_delta.md` Step 2 only checks `name.lower().strip()` (raw Styx name), not Places canonical name/address. **Fix:** Batch Places search first, group by place_id, create ONE ItemRecord per canonical venue. See `references/styx_truncation_fix.md`. Cleanup script: `scripts/fix_styx_dedup.py` (always run `--dry-run` first).
- **Styx delta creates `place_id`-sibling duplicates if dedup checks name only (incident 2026-07-15)** — Near-name venues already in Taste (`"Taco Bell"` vs `"Taco Bell Cantina"`, `"Sidewalk Juice"` SF vs `"Sidewalk Juice- San Mateo"`) share one Google `place_id`. If the pre-check compares `name`/`item_id` instead of `place_id`, the ingestion writes duplicate items + signals and still reports "success". **Rule:** dedup by canonical `place_id`; LINK the signal when the place exists; create exactly one item otherwise. **Verification is mandatory and separate from the ingestion return** — run `scripts/verify_taste_delta.py` (asserts zero `place_id` collisions, zero `item_id` dupes, zero orphaned signals, zero `(merchant,date)` styx dupes). Reconciliation recipe: `references/styx_delta_placeid_dedup.md`. Note this is a DIFFERENT shape from `fix_styx_dedup.py` (truncation variants), which will not catch it.
- **Signal-item linkage is broken** — Styx-sourced signals have `item_id=None`. They use `venue_name` (raw truncated Styx name) not `item_id` for linkage to items. The item-signal graph is broken: recommendations can't properly aggregate signal strength per venue. After creating canonical items, signals must be updated to set `item_id` to the canonical item_id. See `references/styx_truncation_fix.md`.
- **execute_code is blocked in cron mode** — Cron jobs run without a user present to approve `execute_code`. Use `terminal()` with heredoc (`python3 << 'PYEOF'`) for inline Python, or invoke standalone scripts via `terminal()` / `skill_manage(action='write_file')`.
- **Legacy data path is stale** — An old data path may exist but is STALE. Active data is ONLY under `{agent_root}/commons/data/ocas-taste/`. Scripts referencing the old path will read outdated data.
- **Dedup key includes service + venue + date** — The cross-calendar dedup key is `{service}:{normalized_venue}:{event_date[:10]}`. Two extractions from different sources for the same venue on the same day are correctly deduplicated, but the same venue on different dates creates separate signals.
- **Enrichment script dedup uses `venue_name`, not `name`** — The enrichment pipeline's dedup check looks at `venue_name`, not the generic `name` field. Verify dedup logic when modifying the item schema.
- **Calendar scan enumerates writable calendars** — The scan calls `calendarList().list()` and filters for `accessRole in ('owner', 'writer')`, not just `primary`. Some consumption signals may come from shared or secondary calendars the user didn't expect.
- **Calendar scan can silently succeed with wrong account's data** — When <operator>'s token is empty and the script falls back to the agent's credentials, the calendar scan may still \"succeed\" if the agent has access to the same shared calendars (Personal, Family via email delegation). The scan report looks normal (events processed, signals created) but the data flows through the wrong OAuth client. Gmail scans fail visibly; calendar scans can mask the problem. Always verify the authenticated account in scan output — the `Initialized Gmail and Calendar with <file>` line shows which account was actually used.
- **`scan-calendar` output `signals_created` conflates Styx delta with calendar signals** — The JSON output's `signals_created` field reports the count from the Styx delta step, **not** the calendar promotion step. Calendar signals are promoted to the root `signals.jsonl` via `_process_extractions()` but the output number reflects Styx purchases. To find actual calendar signal count, query `signals.jsonl` for `extraction_source == 'calendar'`. See `references/storage_layout.md` for the two-store architecture.
- **`scan-calendar` is calendar-only — NOT the full pipeline** — `taste_scan.py scan-calendar N` only scans Google Calendar. It does NOT run Styx delta or email scan. Its `signals_created` output field correctly reflects only calendar signals (unlike the `taste:scan` cron job which chains calendar + Styx delta and reports Styx's count). For calendar-only historical backfill, use `scan-calendar 365`. For the full pipeline, use `taste_full_enrich.py`.
- **`scan-historical` DATE BUG — stamps every signal with the scan time (CRITICAL)** — `_extract_from_email` parses the email `Date` header with one rigid `strptime("%a, %d %b %Y %H:%M:%S %z")` and falls back to `datetime.now()` on ANY parse failure. In practice the fallback fires for the vast majority of emails (their `Date` headers don't match that exact format), so all emitted signals get `event_date` = the scan timestamp, NOT the real consumption date. Confirmed 2026-07-07: a 365-day run produced 137/141 signals dated `2026-07-07T09:06:23.xxx` (microsecond-spaced = the loop time). This **maximizes recency bias** — the opposite of the goal — and corrupts the model's temporal decay. **Do NOT use `scan-historical` for historical coverage.** Use `scripts/taste_backfill_v2.py` (designated historical backfill; emits correctly-dated signals, as the existing 5,133-signal dataset shows). Fix: replace the strptime with `email.utils.parsedate_to_datetime()` (robust to varied Date formats). See `references/scan_historical_date_bug.md`.
- **`scan-historical` is email-only — NOT the full pipeline** — `taste_scan.py scan-historical N` only scans Gmail. It does NOT run Styx delta or enrichment. For the full pipeline (Styx delta + enrichment of unenriched items), use `taste_full_enrich.py` instead. The daily `taste:scan` cron (13:12) runs email/calendar scan then delegates to `taste_full_enrich.py` for Styx delta + enrichment. If OAuth is broken, `scan-historical` fails entirely but `taste_full_enrich.py` still works.
- **`scan-historical` output is NOT dedupable by `taste_signals_dedup.py`** — The dedup tool's `signal_key` reads `name`/`normalized_name`, but scan signals use `venue_name` and lack `name`/`normalized_name`. All scan signals get an empty venue key and are silently skipped (false "0 dupes" on `--dry-run`). Combined with the date bug above, re-running `scan-historical` over an already-populated dataset silently pollutes it with un-dedupable, mis-dated signals. If you must run it, verify against the actual signal schema (not the tool's count) and revert if dates are wrong.
- **`taste_scan.py status` and `data-quality` report 0 when run outside the venv** — Both commands use the `TasteSkill` class which resolves `data_dir` differently than the actual data location. Always run via the venv Python (`<hermes-home>/commons/data/ocas-taste/venv/bin/python3`) and verify the data path. For a quick count, use `wc -l signals.jsonl items.jsonl` directly. The `data-quality` subcommand has the same bug as `status` — it is NOT documented in `--help` but it exists and returns 0 for all counts when run outside the venv.
- **`taste_full_enrich.py` schema drift — prefer inline enrichment** — The script at `<hermes-home>/profiles/indigo/skills/ocas-taste/scripts/taste_full_enrich.py` generates `item_id` as `item-{safe_name}` (not UUID), uses `strength` field (not `signal_type`), and produces signals with `source: 'enrichment'` that lack the full schema from `references/styx_delta.md`. Items created by this script have `domain: 'restaurant'` instead of `'food'`. **Preferred approach for cron:** write inline Python via `terminal()` that calls Places API directly via `urllib.request` and writes properly structured records. Confirmed 100% enrichment rate with inline approach (2026-06-16, 36/36 transactions).
- **`taste_scan.py` default `data_dir` was the literal `<hermes-home>` placeholder (NOT fixed until 2026-07-26)** — The constructor default `Path("<hermes-home>/commons/data/ocas-taste")` was still present and never resolved (the "Path.home() already fixed on line 30" note was WRONG — the file literally contained the placeholder string). Symptom: scan initializes Gmail/Calendar fine, then crashes at `_save_config()` / `FileNotFoundError: '<hermes-home>/commons/data/ocas-taste/config.json'`. **Fix applied 2026-07-26:** the constructor now resolves `os.environ.get("AGENT_ROOT", "$AGENT_ROOT")` + `commons/data/ocas-taste` when no `data_dir` is passed. If you see the literal `<hermes-home>` path in a traceback, re-apply that patch. The SAME placeholder defect lives in `verify_taste_delta.py` (its default `DATA = "<hermes-home>/commons/data/ocas-taste"`) — it only runs if you pass `--data-dir <real-path>`. `dispatch_taste_dedup.py` had the same bug (fixed 2026-07-26, see its gotcha below).
- **`email_scan.py` and `run_historical_scans.py` have the same `google_auth_mcp` path issue** — Both scripts use `AGENT_ROOT / 'scripts'` which resolves to the indigo profile home. **Fix:** Hardcode `sys.path.insert(0, str(Path('<hermes-home>/scripts')))` — same pattern as the dispatch scripts.
- **`verify_taste_delta.py` default `DATA` is the `<hermes-home>` placeholder** — Running it bare crashes: `FileNotFoundError: '<hermes-home>/commons/data/ocas-taste/items.jsonl'`. **Always invoke with `--data-dir <real-path>`:** `/usr/bin/python3 scripts/verify_taste_delta.py --data-dir $AGENT_ROOT/commons/data/ocas-taste`. It exits 0 with `VERIFY PASSED` on success; non-zero on any integrity violation. A "N created" return from the delta script is testimony, not proof — this verify step is the proof.

- **`scan_email_incremental` silently creates 0 signals if `config.json` (email_sources) is absent** — The scan reads its sender allowlist from `config.json` under `email_sources`. If that key (or the file) is missing, the service loop iterates zero services → `services_scanned: []`, `signals_created: 0`, and the only trace is a missing `config.json`. **Contract:** `config.json` MUST exist with an `email_sources` block (see `references/email_extraction.md` for the 8-service allowlist shape). If a daily scan reports 0 email signals with no error, check `config.json` exists before assuming "no new mail." Calendar scan is independent of this (it enumerates calendars directly).

- **`taste_scan.py` token paths are absolute** — The script uses hardcoded absolute paths for token files (`<gworkspace-creds>/credentials/<user-google-email>.json` and `<third-party-or-user-email>.json`). If these paths are wrong, update them directly in the script. The script also reads scopes from the token file JSON, so scope mismatches are handled automatically.

- **Styx enrichment is universal; non-food merchants not Places-enrichable** — Enrichment scripts are under `<hermes-home>/profiles/indigo/skills/ocas-styx/scripts/`. Food merchants: 100% coverage via inline Places API. Non-food merchants (financial: loan_payments, income, transfers, bank_fees) return no Places results — use `enrich.py` for name resolution instead.

- **Mini App ratings feed into Taste as `signal_type: \"rating\"`** — The restaurant-rater Mini App writes ConsumptionSignals with `source: \"miniapp\"` and `signal_type: \"rating\"`. Dedup key: `miniapp:{venue_name}:{date}`. These are high-confidence (confidence=1.0) first-party signals that include `likert_score` (1-5) and `go_back_choice` (\"No\", \"Special Occasions\", \"If Menu Updates\", \"Yes\"). They create/update ItemRecords with `user_rating` and `user_would_go_back` fields. See `restaurant-rater` skill and `taste_bridge.py` for the write pattern.

- **Historical backfill & calendar filtering** — Use `scripts/taste_backfill_v2.py` for historical email/calendar scans (not `taste_full_enrich.py` which is Styx-only). Calendar signals require aggressive food/venue filtering (positive: restaurant, dinner, lunch; negative: appointment, meeting, zoom) — without it ~70% are noise. Bad calendar signals can be cleaned post-hoc by scanning `signals.jsonl` for `source == 'calendar'` against a non-food blocklist.

- **Styx food merchant enrichment: 100% coverage via inline Places API** — All food merchants in styx.db have Google Places enrichment via direct `urllib.request` calls (100% match rate). Produces ItemRecords with `cuisine`, `rating`, `price_level`, `formatted_address`, `place_id`. The `styx_places_enrich.py` script is an alternative but inline gives better schema control.
- **Spotify puller & Python venv issues** — Spotify puller fails silently on missing `SPOTIFY_REFRESH_TOKEN` (check `music/spotify_sync_checkpoint.json`). The ocas-taste venv uses Python 3.14 lacking `googleapiclient` — use `<hermes-venv>/bin/python3.13` instead.

- **Re-auth, dedup scripts** — `google_oauth_init.py` only handles the agent's account (hardcoded line 141). For <operator>'s re-auth, build the OAuth URL manually with PKCE. `taste_signals_dedup.py` is the correct post-enrichment dedup tool (not `clean_signals.py`). `dispatch_taste_dedup.py` lives under `skills/ocas-taste/scripts/` (NOT `commons/data/`) — always use absolute path.
- **`dispatch_taste_dedup.py` `<hermes-home>` placeholder bug (FIXED 2026-07-26):** Until that date the script hardcoded `DATA_DIR = Path("<hermes-home>/profiles/<profile>/commons/data/ocas-taste")` — the SAME literal `<hermes-home>` / `profiles/<profile>` defect that hit the ocas-forge closure scripts (see `references/closure-scripts-hermes-home-placeholder-bug.md` in ocas-forge). Every run printed `ERROR: <hermes-home>/profiles/<profile>/commons/data/ocas-taste/signals.jsonl not found` and SILENTLY SKIPPED dedup — so a `dispatch-wave` taste journal reporting `dedup_removed: 0` / `signals_total_after == signals_total_before` was NOT proof of a clean signal store; real duplicates persisted across waves. Fixed by resolving `os.environ.get("AGENT_ROOT", "$AGENT_ROOT")` + `profiles/indigo/commons/data/ocas-taste` and adding `import os`. **Detection / re-occurrence guard:** if you ever see `ERROR: <hermes-home>/profiles/<profile>/.../signals.jsonl not found` from this script, it still carries the placeholder — patch line 26 the same way; do NOT trust a `dedup_removed: 0` journal line as evidence of no duplicates. Always run `--dry-run` FIRST and confirm it actually opens `signals.jsonl` (printed `Total signals: N`) before applying. The dispatch runner (`run_mixed_wave_closure.py`) invokes it with `--dry-run` then `--apply-taste`; if the dry-run can't find the file, the applied run also silently no-ops and the journal's `dedup_removed` lies.

- **Google Places API key, inline enrichment, schema drift** — API key is in `<hermes-home>/secrets/plaid.env` (not env var). Inline enrichment (direct urllib to legacy GET API) preferred over `taste_full_enrich.py` which has schema drift (`item-{safe_name}` not UUID, `strength` not `signal_type`). The v1 POST API returns 400 from inline Python — use legacy GET. `taste_full_enrich.py` also enriches existing unenriched items but doesn't set `enriched: true` (use `taste_enrich_fix.py` after).

- **Token expiry timezone suffix breaks `from_authorized_user_file()`** — Google OAuth token files may contain `expiry: \"2026-06-17T17:41:40+00:00\"` (ISO 8601 with timezone). The `google.oauth2.credentials.Credentials.from_authorized_user_file()` parser uses `strptime` with `%Y-%m-%dT%H:%M:%S` and fails with `\"unconverted data remains: +00:00\"`. **Diagnosis:** Check `expiry` field format with `python3 -c \"import json; d=json.load(open('<gworkspace-creds>/credentials/<email>.json')); print(repr(d.get('expiry')))\"`. **Fix:** Strip the timezone suffix: `d['expiry'] = d['expiry'][:19]` and rewrite the file. This is a one-time fix per token file — the refreshed token will get a new `expiry` field that may or may not include the suffix depending on the OAuth library version. **Always check and fix the token expiry before running `taste_scan.py`** — the scan will fail silently or produce 0 results if the token can't be loaded. Also check for float expiry values (see next gotcha).
- **Token expiry stored as float instead of string** — Some token files store `expiry` as a Unix timestamp float (e.g., `1782328557.213807`) instead of an ISO string. The Taste script calls `.rstrip()` on this and crashes with `AttributeError: 'float' object has no attribute 'rstrip'`. **Fix:** Replace with ISO string: `d['expiry'] = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(time.time() + 3600))`. See `references/token-repair.md` for the combined repair script.

- **`scan-historical` creates signals in two schemas** — The email extraction produces signals with `signal_id`, `venue_name`, `extraction_source` (old schema). The enrichment pipeline that runs alongside produces signals with `name`, `source: \"enrichment\"`, `visit_count`, `strength` (new schema) — no `signal_id`, no `item_id`, no `extraction_source`. The two schemas coexist in `signals.jsonl`. The enrichment-schema signals may have duplicate venue names within a single scan run. This is a known issue; the enrichment pipeline should be deduplicated against existing signals before writing.

## Support File Map

| File | When to read |
|---|---|
| `references/api_specifics.md` | During scan or enrichment; API-specific query syntax and rate limits |
| `references/api_auth.md` | Before Gmail/Calendar/Spotify API calls; OAuth patterns and token pitfalls |
| `references/automation.md` | When troubleshooting cron jobs or backup failures |
| `references/backup.md` | Backup/restore procedures, LFS tracking, disk space management |
| `references/config.default.json` | On `taste.init`; template for a fresh config.json |
| `references/token-repair.md` | **Token repair patterns** — five failure modes (timezone suffix, float expiry, microsecond suffix, numeric-string expiry, microsecond+fraction+Z combo), hardened combined repair script with real credential paths, confirmed incidents. Run before every scan. |
| `references/email_extraction.md` | Before running taste.scan; sender allowlist and dedup rules |
| `references/enrichment.md` | Before running taste.enrich.item; what to extract per domain, false-positive filtering, dedup |
| `references/plans/preference-scan.plan.md` | Before a multi-step preference-scan workflow; ingest recent activity → update preference model |
| `references/historical_scan_auth.md` | Before running historical email or calendar scans |
| `references/initialization.md` | On first invocation of any Taste command |
| `references/journal.md` | Before taste.journal; at end of every run |
| `references/okrs.md` | During performance review or model status reporting |
| `references/recommendation_style.md` | Before generating recommendations or reports |
| `references/recommendation_analysis.md` | During recommendation analysis; Python code for computing strengths, visited set, pattern identification, candidate cross-ref |
| `references/recovery.md` | On every wake; gap detection and degraded mode logic |
| `references/schemas.md` | Before creating signals, items, links, extractions, or recommendations |
| `references/self_update.md` | Before `taste.update`; full pull/install procedure |
| `references/signal_dedup.md` | After enrichment runs to dedup same-day signals from multiple sources |
| `references/signal_policy.md` | Before decay calculations or domain gating |
| `references/signal_weighting.md` | Before computing signal strength or computing temporal decay |
| `references/spotify_sync.md` | Before `taste.sync.spotify`; music playback history procedure |
| `references/storage_layout.md` | When debugging data path issues or managing disk |
| `references/strength_model.md` | Before computing signal strength or ranking items |
| `references/styx_delta.md` | During Styx→Taste delta ingestion; SQL query, enrichment, dedup, schemas |
| `references/styx_truncation_fix.md` | When debugging duplicate items from Styx truncation; dedup fix, signal-item linkage repair |
| `references/session-20260625-dispatch-1846-taste.md` | **Dispatch 18:46 (2026-06-25):** Taste scan + Styx enrichment results, OAuth token repair confirmation, email triage summary |
| `references/session-20260626-dispatch-taste.md` | **Dispatch wave (2026-06-26T14:34Z):** Genuine mixed dispatch — email flag (AlphaSights), taste success (2 signals), journal second-wave. `dispatch_taste_dedup.py` path fix (skills/ not data/). |
| `references/cron_pipeline_pattern.md` | For daily cron runs — full pipeline order, API key location, enrichment approach, dedup format, rate limiting |
| `references/scan_execution_patterns.md` | Concrete command patterns for all scan types; post-run verification; OAuth account table |
| `references/scan_historical_date_bug.md` | **CRITICAL:** `scan-historical` stamps every signal with the scan time (strptime fallback bug); root cause, fix (`parsedate_to_datetime`), dedup-incompatibility, and revert recipe. |
| `references/script_inventory.md` | When choosing which script to run; what each script does and its auth requirements |
| `scripts/taste_full_enrich.py` | Full pipeline: styx + email + existing unenriched items |
| `scripts/taste_enrich_fix.py` | Fix failed enrichment persistence — re-enriches items and sets `enriched: true`. Use after `taste_full_enrich.py` reports success but items remain unenriched. |
| `scripts/taste_signals_dedup.py` | Signal deduplication — run after enrichment passes. **Actual path:** `<hermes-home>/profiles/indigo/commons/data/ocas-taste/scripts/taste_signals_dedup.py`. Takes no arguments. Confirmed working 2026-06-18. |
| `scripts/taste_cleanup_and_enrich.py` | Cross-source dedup + retry failed enrichments |
| `scripts/safe_taste_dedup.py` | **Styx-safe** dispatch-wave dedup — keys on `event_date or date`, backs up, refuses to write if Styx count would drop. Run after every dispatch scan (`--dry-run` supported). |
| `scripts/fix_styx_dedup.py` | Merge Styx truncation duplicates + remap signals; always run `--dry-run` first |
| `scripts/verify_taste_delta.py` | **Run after every Styx delta write.** Asserts zero `place_id` collisions, zero `item_id` dupes, zero orphaned signals, zero `(merchant,date)` styx dupes. Exits non-zero on violation. `--expect-place-ids` claims exactly-one-item per place_id. |
| `scripts/styx_delta_corrected.py` | **Corrected daily Styx delta** (2026-07-22). Deduplicates candidates by `(name,date)`, links by `place_id`/name, self-heals orphans, writes signals+items atomically. Use this instead of hand-rolled delta code. NEVER chain `dispatch_taste_dedup.py` onto it — see `references/dispatch_dedup_styx_corruption.md`. |
| `references/styx_delta_placeid_dedup.md` | `place_id`-sibling duplicate incident (2026-07-15): why name-only dedup fails, the canonical-`place_id` rule, and the manual reconciliation recipe |
| `references/dispatch_dedup_styx_corruption.md` | **CRITICAL (2026-07-22):** `dispatch_taste_dedup.py` silently deletes Styx signals on the daily job (keys on `event_date`, which Styx signals lack). Incident, recovery recipe (restore `signals.jsonl.bak.delta.*`), and the rule to never chain it onto the daily delta. |