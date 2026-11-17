# Cron Sweep Pattern

The stable pattern for `spot.watch.sweep` when running as a scheduled cron job. Confirmed working 2026-05-30 through 2026-06-08 (consecutive).

## Pre-sweep

1. Read `watch.jsonl` via `terminal(command="cat ...")` — never `read_file` (line-number prefixes corrupt parsing)
2. If no active records, write skipped journal + metrics, return `[SILENT]`
3. Read `venues.jsonl` for venue details (booking URLs, platforms)
4. Read `config.json` for defaults

**IMPORTANT: In cron mode, `read_file` can fail for ALL files** (not just JSONL) due to path resolution issues — the tool may prepend `/home/` to already-absolute paths, causing "File not found" errors for files that exist. Always use `terminal(command="cat ...")` with absolute paths as the reliable fallback for any file read in cron mode.

## Per-record dispatch

For each active WatchRecord:

### Square — Stealth Browser PRIMARY (as of 2026-06-08)

**RECOMMENDED: Use stealth browser first for Square.** The stealth browser loads Square pages reliably on the first navigate (no SPA hydration failures). Spawn time is ~2s vs ~35-45s for Hermes kill+restart. Confirmed working 2026-06-08 17:16 PDT — all 5 interactions (service, duration, staff, Book, calendar) completed cleanly with no CDP drops or timeouts.

**Stealth Browser Flow (verified 2026-06-08 — navigate to /services, not ?date=):**

This is the current working flow. Navigate to `/services` (not `?date=`) and use the calendar date-picker after the Book click. This avoids the SPA hydration issues that the `?date=` URL pattern can trigger.

1. `mcp_stealth_browser_spawn_browser(headless=true, sandbox=false)` → `instance_id`
2. `mcp_stealth_browser_navigate(instance_id, url="{booking_url}/services", wait_until="domcontentloaded")` → services page loads
3. `mcp_stealth_browser_click_element(instance_id, selector="button", text_match="Accept all cookies")` → dismiss cookie banner
4. `mcp_stealth_browser_click_element(instance_id, selector="label[slot="label"]", text_match="<service_name>")` → page transitions to duration/staff. **NOTE:** XPath `//*[contains(text(), '...')]` can fail with "Element not found" — use `label[slot="label"]` with `text_match` as the reliable selector.
5. `mcp_stealth_browser_click_element(instance_id, selector="label[slot="label"]", text_match="<duration>")` → duration selected
6. `mcp_stealth_browser_click_element(instance_id, selector="label[slot="label"]", text_match="Any staff")` → staff selected
7. `mcp_stealth_browser_click_element(instance_id, selector="market-button", text_match="Book")` → clicked, transitions to calendar
8. `mcp_stealth_browser_query_elements(instance_id, selector="market-button[data-testid^='date-']")` → read calendar dates
9. If target date not visible: `mcp_stealth_browser_click_element(instance_id, selector="market-button[data-testid='next-week-button']")` → advance calendar. Repeat until target date is in view.
10. Check target date's `disabled` attribute — if present, date is unavailable (outside booking window or fully booked). If no time slots appear after clicking, date has zero availability.
11. `mcp_stealth_browser_click_element(instance_id, selector="market-button[data-testid='date-{day}']")` → click target date
12. `mcp_stealth_browser_query_elements(instance_id, selector="market-button[data-testid='time-slot']")` → read all available time slots. Empty array = no availability.
13. `mcp_stealth_browser_close_instance(instance_id)`

**Date availability interpretation:**
- `disabled=""` on a **past** date → normal, date has passed
- `disabled=""` on a **future** date → date is outside the booking window (venue hasn't opened bookings that far out) OR fully booked. Check back in a few days.
- No `disabled` attribute → date is in the booking window and clickable
- Clicking a date and getting zero `time-slot` elements → date has no available slots (fully booked or not yet opened)

**If the stealth browser flow fails (CDP drop, timeout):**
- If `click_element` or `navigate` fails with `[Errno 111]`: spawn a NEW stealth browser instance. Do NOT fall back to Hermes browser for mid-flow failures. The second instance typically connects fine — the first instance's CDP transport dropped but the MCP server itself is healthy.
- If `spawn_browser` succeeds but `navigate` fails with `[Errno 111]`: the MCP transport is down. Switch to Hermes browser immediately.
- If all retries fail: use `last_known` data from the WatchRecord.
- **Confirmed 2026-06-09:** First stealth browser instance dropped CDP connection after cookie banner click (`[Errno 111]` on `get_page_content`). Second instance spawned and completed the full flow without issues.

**Dual browser failure (confirmed 2026-06-09):** Both the stealth browser MCP transport AND the Hermes browser CDP can fail simultaneously. Symptom: stealth browser `navigate` fails with `[Errno 111]` AND Hermes browser `browser_navigate` fails with `502 Bad Gateway`. When this happens:
1. Do NOT retry either browser — both transports are down.
2. Use `last_found` data from the WatchRecord for ALL venues that require browser automation.
3. Still update `last_checked` timestamps and write the journal (mark status as `"browser_unavailable"`).
4. Report the dual failure in the sweep output so the user knows both backends need attention.
5. Meevo/Vagaro skips are unaffected (they skip browsers regardless).

**Hermes Browser Flow (primary as of 2026-06-08 — confirmed working):**
The Hermes browser is the de facto primary method for Square sweeps as of 2026-06-08. It successfully executes the full Square flow end-to-end. **All interactions (service, duration, staff, Book, calendar navigation, date selection, slot reading) work via `browser_click` on snapshot refs** — no JS fallbacks needed in the normal case.

**Calendar navigation (confirmed 2026-06-08):** After clicking Book, the calendar shows ~3 weeks. Use `browser_snapshot` to find the "Next week" button ref, click it to advance. Repeat until target date is visible. Then click the target date button ref (e.g., "Friday 19"). Time slots render immediately after date click — read via `browser_snapshot`. All calendar interactions (Next week, date click) work via `browser_click` on snapshot refs.

1. `browser_navigate(url="{booking_url}?date=YYYY-MM-DD")` — server-side date tracking.
   - If snapshot returns empty/zero elements, retry `browser_navigate` to the same URL up to **3 times total**. Do NOT kill Chrome between retries — the SPA self-resolves.
2. `browser_snapshot` → read services list → `browser_click` on service ref (e.g., ref=e27 for "Swedish Massage")
3. `browser_console(expression="window.location.href")` — verify URL changed to `/services/{serviceId}`
4. `browser_snapshot` → `browser_click` on duration ref (e.g., "1.5 Hours" ref=e16)
5. `browser_snapshot` → `browser_click` on "Any staff" (ref=e18)
6. **`browser_snapshot` — verify staff selection persisted:** Check that "Any staff" shows `checked=true` and `selected`. If `checked=false` or "Please select staff." alert present → click "Any staff" ref again, re-verify (max 2 attempts). If `browser_click` still doesn't persist after 2 attempts, **use JS fallback**: `browser_console(expression="(() => { const opts = document.querySelectorAll('[role=\"option\"]'); for (const o of opts) { if (o.textContent.includes('Any staff')) { o.click(); return 'clicked'; } } return 'not found'; })()")` — then re-verify via snapshot. **Snapshot is authoritative; do NOT rely solely on `browser_console` JS** — `market-radio` state is not reliably readable via synchronous JS.
7. `browser_click` on Book button ref (ref=e26)
8. **IMMEDIATELY** `browser_console(expression="window.location.href")` — must show `/availability`
9. If `/availability`: `browser_snapshot` → read all time slot buttons, filter to time_window
10. If `/services` or `about:blank`: session lost, re-do full flow (no Chrome kill needed for `about:blank`)

**JS fallbacks** (only if `browser_click` returns "Unknown ref" or similar):
- Service: `browser_console` JS `document.querySelectorAll('[role="option"]')` or MARKET-ROW → `.click()`
- Staff: `browser_console` JS `document.querySelectorAll('[role="option"]')` → find "Any staff" → `.click()` + setAttribute
- Book: `browser_console` JS `document.querySelectorAll('market-button')` → find by text → `.click()`

**Summary of Square interaction reliability via Hermes browser (as of 2026-06-08):**
- Service, duration, staff, Book clicks: **`browser_click` on refs works** (confirmed 2026-06-08, 10+ consecutive clean sweeps)
- **Staff selection requires snapshot verification** — first click may not persist; re-click if snapshot shows `checked=false` (confirmed 2026-06-08: first click showed `checked=false` + "Please select staff." alert, second click succeeded)
- JS fallbacks available but not needed in normal operation
- URL verification: `browser_console` expression (never use `browser_snapshot` for URL check)

**Counting slots on the availability page:** After Book→/availability, the snapshot shows time slots grouped into Morning/Afternoon/Evening lists. Count ALL `<button>` elements within `<li>` items across all time groups for the total. Filter to the watch's time_window for the window count. Each time group is a `<list>` with an accessible name like "Available time slots, Morning, select a time to proceed".

### Meevo (cron mode — skip if 3+ consecutive failures)
- Skip browser attempt entirely
- Use `last_found` data from WatchRecord
- Update `last_checked` timestamp
- Log "skipped — N+ consecutive Angular change detection failures"

### Vagaro (cron mode — skip if 3+ consecutive failures)
- Skip browser attempt entirely
- Use `last_found` data from WatchRecord (likely null)
- Update `last_checked` timestamp
- Log "skipped — N+ consecutive JS handler failures"

## Post-sweep

0. **Verify system date** — Run `date` before writing any journal. Pre-existing journal directories from prior runs can mislead you (e.g., a `2026-06-08/` directory existing while the actual system date is `2026-06-06`). Write ALL sweep output (journal, metrics, watch updates) using the VERIFIED system date, NOT the date implied by existing directories.

1. Update all WatchRecords in `watch.jsonl` with new `last_checked` timestamps via Python. **IMPORTANT**: The raw file on disk may contain line-number prefixes (`1|`, `2|`, etc.) if a previous write went through `read_file` output. Always detect and strip prefixes before parsing:
   ```python
   # Read raw bytes, strip prefixes, parse
   with open(path, 'rb') as f:
       raw_lines = f.readlines()
   records = []
   for line in raw_lines:
       line = line.strip()
       if not line:
           continue
       s = line.decode('utf-8')
       # Strip line-number prefix if present (e.g., "1|{...}" → "{...}")
       if s and s[0].isdigit() and '|' in s:
           idx = s.index('|')
           after = s[idx+1:]
           if after.startswith('{'):
               s = after
       if s.startswith('{'):
           records.append(json.loads(s))
   ```
   Write back with `json.dumps(record) + "\n"` — never write prefixes. See `references/data-file-access.md` for full repair pattern.
2. Write journal to `{agent_root}/commons/journals/ocas-spot/YYYY-MM-DD/{run_id}.json` via `write_file()` — create directory with `terminal(command="mkdir -p ...")` first
3. **Append** metrics line to `metrics.jsonl` — **CRITICAL**: `write_file()` OVERWRITES the entire file. For `metrics.jsonl` (append-only), you MUST either:
   - **Preferred**: Use `terminal(command="echo '{json}' >> /path/to/metrics.jsonl")` — this appends a single line safely without reading the file first.
   - **Alternative** (if you need atomic read-modify-write): Read current content: `terminal(command="cat /path/to/metrics.jsonl")`, write back ALL existing lines PLUS the new line.
   - Verify with `terminal(command="tail -3 /path/to/metrics.jsonl")`
   - Writing a single line to `metrics.jsonl` via `write_file()` destroys all prior sweep history
4. Report results (or `[SILENT]` if nothing new)

## Key constraints

- `execute_code` is **blocked** in cron mode — use `terminal()` + Python one-liners
- `write_file()` may emit false-positive `_warning` about "sibling subagent" — ignore it
- Never use `read_file` for any file in cron mode — use `terminal(command="cat ...")` with absolute paths. `read_file` can fail due to path resolution issues (prepends `/home/` to absolute paths) AND line-number prefixes corrupt JSONL parsing.
- Never use `browser_back` during Square flow
- Never navigate to `/availability?date=` after Book — session reset
- Always verify Book→/availability via `browser_console` URL check, not `browser_snapshot`
- **`metrics.jsonl` is append-only** — never `write_file()` a single record; always read-all-then-write-all-plus-new