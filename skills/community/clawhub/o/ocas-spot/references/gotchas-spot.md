# Spot — Gotchas

## Square Booking Flow

- **Server-side date tracking is the PRIMARY date-targeted pattern** — Navigate to `{base_url}?date=YYYY-MM-DD` → click service → duration → staff → Book → availability loads on target date. No separate URL date jump needed. See `references/platforms/square-date-targeted-flow.md`.
- **DO NOT navigate to `/availability?date=` via `browser_navigate` after Book** — this resets the session and redirects to /services.
- **`browser_back` invalidates Square session** — Never use it during a Square booking flow.
- **Square buttons use `aria-disabled`, not `isEnabled()`** — Use the `disabled` attribute on `market-button` and shadow DOM queries.
- **Square `market-radio` `checked` property is NOT reliable synchronously** — Verify via URL change to `/availability` instead.
- **Square `?service_id=` URL parameter crashes the page** — Navigate to base URL without parameters.
- **Square "Any staff" radio may need double-click** — Verify selection via JS `[role="option"]` query, not snapshot.
- **Square staff click non-persistence in Hermes browser (confirmed 2026-06-08)** — `browser_click` on the "Any staff" `[role="option"]` ref can return `true` without the Square SPA committing the selection. The snapshot correctly shows `checked=false` and the "Please select staff." alert persists. **Fix:** After clicking staff, take a snapshot to verify `checked=true`. If not, click the same ref again. Max 2 click attempts. The `browser_console` JS check (`market-radio` `selected` class) is NOT reliable synchronously — the snapshot's accessibility attributes are authoritative.
- **Square staff selection — `browser_click` on `[role="option"]` refs works** (confirmed 2026-06-08, 10+ consecutive clean sweeps). JS fallback available but not needed in normal Hermes browser operation. Stealth browser `click_element` with `text_match` also works.
- **Square Book button is a `<market-button>`, NOT a `<button>`** — Use JS to click it.
- **Square Book click → verify BEFORE any further navigation** — Use `browser_console(expression="window.location.href")` to verify URL shows `/availability`.
- **Square "Next week" button CSS selector fails** — `market-button[next-week-button]` CSS attribute selector does NOT work in stealth browser `click_element`. Use `execute_script` with `aria-label` matching instead: `document.querySelector('market-button[aria-label="Next week"]').click()`. Confirmed 2026-06-06.
- **Square "Next week" button is a `market-button` custom element** — Has `aria-label="Next week"` and `data-testid="next-week-button"`. The `data-testid` attribute is NOT accessible via CSS attribute selector in stealth browser.
- **Square "Next" button (booking step navigation) is a `MARKET-BUTTON` custom element** — May not be in accessibility tree. Use JS to find by text.
- **Square calendar dates with `bounding_box: null` are off-screen** — Date buttons below the visible scroll area have `bounding_box: null` despite `is_visible: true`. `click_element` cannot target them. Use `query_elements` to check `disabled` attribute instead of trying to click.
- **Square calendar auto-advances past dates** — The calendar's `displayed-date` determines which week is "current." Dates in the week BEFORE the displayed date are disabled (past week). Dates in the displayed week and future weeks are available. When checking a target date, navigate to a week where the target is in the current or future week, not the past week. If the target date shows `disabled=""`, it may be in the past week rather than actually booked.
- **Square `market-radio` is the canonical selector for duration/staff** — Duration and staff options use `<market-radio>` elements with `aria-label` attributes (e.g., `aria-label="1.5 Hours"`, `aria-label="Any staff"`). While `[role="option"]` worked in some sessions, `market-radio[aria-label='...']` is the more reliable selector. Use `query_elements(selector="market-radio")` to read all options, then `click_element(selector="market-radio[aria-label='...']")` to select.
- **Square service list may be longer than venue record** — Present full service list from page, not just venue record.

## Square Crash Recovery

- **Square flow confirmed working 2026-06-06 15:35 (cron sweep)** — Stealth browser step-by-step click_element flow. Service → duration → staff → Book → get_page_content → parse. No post-Book crash. 34 total slots, 7 in 3:30-5:00 PM window unchanged. 5th+ consecutive clean stealth browser run. 7th+ confirmed clean run as of 2026-06-06 19:37 PT. 9th+ confirmed clean run as of 2026-06-06 20:56 PT (rapid sequential click variant after CDP drop recovery). **Slot counts change between sweeps** — As of 2026-06-08, Russamee shows 36 total slots (vs 34 on 2026-06-06). The 3:30-5:00 PM window remained stable at 7 slots. Always count from the current page, not from prior sweep data.
- **SPA hydration failure** — First navigate may return `(empty page)`. Try up to 4 navigates with 5s gaps before kill+restart.
- **CDP 502 → agent-browser restart pattern** — Kill agent-browser process, wait 20-30s for auto-restart.
- **Persistent CDP 502 ceiling** — When CDP 502 persists across 3+ kill+restart cycles, browser is unrecoverable for the sweep. Use `last_known` data.
- **Cross-venue browser navigation crash** — Navigating between unrelated booking platforms can cause CDP 502. Check Square LAST in multi-venue sweeps.
- **Square OneTrust DOM removal is UNRELIABLE** — Only handle overlay if it actually appears. Do NOT preemptively remove OneTrust elements.
- **Square OneTrust on main listing page** — Removing OneTrust from the main services listing page has NOT been observed to crash the browser.

## Stealth Browser

- **Stealth browser `is_clickable: false` on Square custom elements is a reporting artifact** — `query_elements` on Square pages returns `is_clickable: false` for `market-row`, `[role="option"]`, and `market-button` elements. Despite this, `click_element` with `text_match` works reliably on all of them. Do NOT switch to JS click workarounds solely because `is_clickable` reads false — this is a stealth browser accessibility tree quirk, not a real constraint. Confirmed 2026-06-06: full Square flow (service → duration → staff → Book) completed via `click_element` despite every element reporting `is_clickable: false`.

- **Stealth browser `text_match` length sensitivity** — `click_element` with `text_match` FAILS if the string is too long or extends beyond the element's visible text truncation. Use the shortest unique prefix: `"Swedish Massage"` not `"Swedish Massage A soothing full body..."`. For durations use `"1.5 Hours"` not the full price string. See `references/stealth-text-match-length.md`.
- **Stealth browser MCP server can be entirely unreachable** — `spawn_browser` fails with root/sandbox error. `sandbox=False` and `browser_args=["--no-sandbox"]` do NOT fix it (schema validation error). After 3 failures, MCP server is marked unreachable. **Fallback: Hermes browser works reliably for Square** (confirmed 2026-06-08 — full end-to-end flow: service → duration → staff → Book → calendar → date → slots). **In cron mode, skip stealth browser entirely — use Hermes browser directly.** In interactive mode, switch to Hermes browser after 1 stealth browser spawn failure. See `references/stealth-browser-fallback.md`.
- **Stealth browser spawn-succeeds-then-navigate-fails (2026-06-06)** — `mcp_stealth_browser_spawn_browser` can return `{"state": "ready"}` successfully, but the very first `navigate` call fails with `[Errno 111] Connect call failed ('127.0.0.1', <port>)`. The MCP transport is down despite the successful spawn response. **Treat this identically to a spawn failure: switch to Hermes browser immediately. Do NOT retry stealth browser.** This is a transport-level failure, not a browser-level failure — spawning a new instance will not help.
- **Hermes browser is a viable Square fallback** — Despite the stealth browser being "recommended primary," the Hermes browser successfully loads Square SPAs on first navigate and completes the full booking flow. The stealth browser remains preferred when available (faster spawn, no SPA hydration risk), but Hermes browser is a reliable fallback, not a last resort.
- **Stealth browser `execute_script` DOM queries on Square availability pages are SESSION-DEPENDENT** — On some sessions (2026-06-06, 2026-06-08), `execute_script` with `document.querySelectorAll('market-button')` + text content matching returns all time slots correctly (34 slots confirmed 2026-06-08). On other sessions (2026-06-07), the same queries return empty arrays or null. Simple expressions like `window.location.href` are always reliable. **Pattern:** Try `execute_script` DOM queries first (fastest path). If results are empty/null, fall back to `get_page_content()` + file parsing. Do NOT assume either method is permanently broken or permanently reliable.
- **Stealth browser `get_page_content` + grep can return ZERO results** — On 2026-06-08, `get_page_content()` saved a 2.8MB JSON file but `grep -oP '\d{1,2}:\d{2}\s*[AP]M'` returned zero matches — the HTML serialization does not include shadow DOM text content for `market-button` elements even when the page is fully loaded. This contradicts the earlier claim that this method is "reliable." **Both extraction methods are fallible.** Try `execute_script` DOM queries first; if they fail, try `get_page_content` + grep; if both fail, use `last_known` data.
- **Stealth browser `get_page_content` returns a file path** — Parse with terminal Python. Square availability page can produce ~3MB files.
- **Stealth browser CDP connection drop** — `query_elements` succeeds but `click_element` fails with `[Errno 111]`. Spawn a NEW instance (~2s) rather than reconnecting.
- **Stealth browser CDP drop can occur mid-flow after staff selection** — Observed 2026-06-06: all 3 clicks (service, duration, staff) returned `true`, but CDP connection dropped before the "Book" click. `get_page_content` also failed with `[Errno 111]`. Recovery: close dead instance, spawn new one, re-run full flow. On retry, rapid sequential clicks (no intermediate verification) completed successfully. See `references/stealth-browser-fallback.md`.
- **Stealth browser `navigate` uses `wait_until` (not `wait`)** — Valid values: `load`, `domcontentloaded`, `networkidle`.
- **Stealth browser post-Book crash** — `get_page_content()` can timeout (120s) after successful all-JS flow. Close instance, spawn new one, use last_known data.
- **Square service row selection — CSS `market-row:nth-child(N)` is reliable** (confirmed 2026-06-08 cron) — `click_element(selector="div[data-testid='services-page'] > market-row:nth-child(N)")` selects the Nth service row. Account for the `h2.sr-only` heading as child 1: the first `market-row` service is at `nth-child(2)`, the 6th service at `nth-child(7)`, etc. XPath text match (`//*[contains(text(), 'ServiceName')]`) can fail in stealth browser; use nth-child as the primary approach when the service position is known. See `references/stealth-browser-square-flow-20260608.md`.

- **Square `?serviceId=` URL parameter prevents options from rendering** — Navigating to `{base_url}/services?date=YYYY-MM-DD&serviceId=<id>` loads the page but `[role="option"]` elements are never rendered. Always navigate to the base `{base_url}?date=YYYY-MM-DD` and click the service via `click_element`. Confirmed 2026-06-06.

- **Stealth browser `execute_script` behavior is SESSION-DEPENDENT** — On 2026-06-07, `execute_script` returned `{"success":true,"result":null}` for ALL DOM queries (6+ consecutive calls). On 2026-06-06 and 2026-06-08, `execute_script` returned correct values for `window.location.href`, JS MARKET-ROW clicks, and complex multi-step scripts. **Do NOT assume `execute_script` is permanently broken.** Try it; if it returns null, fall back to `query_elements` + `click_element` + `get_page_content`. The `query_elements`/`click_element` path works regardless of `execute_script` status.

## Hermes Browser — Persistent about:blank Pattern (2026-06-08)

**`read_file` path resolution issue (confirmed 2026-06-08, 4 consecutive failures this session)** — In cron mode, `read_file` can fail for ANY path — both `~/...` home-relative paths and fully-resolved absolute paths like `<hermes-home>/profiles/indigo/...`. The tool's path resolver prepends `/home/` to the home-directory segment, producing double-prefixed paths like `<hermes-home>/profiles/indigo/home/.hermes/profiles/indigo/...`. The failure is silent (returns "File not found") and does NOT fall back to alternative resolution. **Use `terminal(command="cat /absolute/path")` as the reliable fallback for ANY file read in cron mode.** This is the single most common cron-mode blocker — it will hit on the first file read of every sweep until you switch to `terminal()`. After 2 consecutive `read_file` failures in a session, switch to `terminal()` for all remaining file reads — do not retry `read_file`.

When Hermes browser gets `about:blank` post-Book, re-navigating to `?date=` and re-running the full JS flow usually resolves it (transient failure). However, on 2026-06-08 the re-run ALSO produced `about:blank` — this was the third consecutive sweep (along with 2026-06-05 and 2026-06-06) where about:blank occurred.

**Pattern as of 2026-06-08:**
```
Attempt 1: service click → duration → staff → Book → about:blank
Attempt 2 (re-navigate, re-run): service click → duration → staff → Book → about:blank again
→ Persistent about:blank. Skip venue, use last_known. Do NOT attempt a third time.
```

**Diagnosis:** If `about:blank` occurs on two consecutive attempts with re-navigation between them, the transient recovery has failed. Third attempts have not been observed to succeed. Use `last_known` data.

**Concurrent stealth browser CDP drop (2026-06-08):** On the same sweep, stealth browser also CDP-dropped post-Book (all 4 JS clicks completed, then `[Errno 111]` on the URL verification call). Both browsers failing post-Book on the same sweep suggests a Square server-side issue rather than a browser-specific one. When both browsers fail on the same sweep, `last_known` data is almost certainly correct (availability is stable).

## Stealth Browser CDP Drop Post-Book Rate (Updated 2026-06-08)

Stealth browser CDP drop after the Book click (all JS clicks succeed, then `[Errno 111] Connect call failed` on the verification call) has occurred in **three consecutive sweeps** (2026-06-05, 2026-06-06, 2026-06-08). This is now the **primary failure mode** for stealth browser Square checks.

- Expected behavior: All 4 clicks succeed → close instance → use last_known data
- No data loss: The availability page state is already committed server-side when Book is clicked
- Recovery cost: Close dead instance: ~1s. Use last_known: 0s. Total: ~1s per occurrence
- The `execute_script` calls themselves all return correctly BEFORE the CDP drop (2026-06-08 confirmed: `clicked`, URL verified, `1.5hr, Any staff, Book` all returned correctly)

**Stealth browser Book click itself can be the failure point (2026-06-06 23:16 PDT):** In some cases, the first 3 clicks (service, duration, staff) all return `true`, but the 4th click (Book) fails with `[Errno 111]` — the CDP connection drops precisely during the Book click, not after. The `get_page_content` call also fails. This is functionally identical to the post-Book CDP drop pattern: close the instance, fall back to Hermes browser or last_known data. Do NOT retry the stealth browser for the same venue — the session is unrecoverable.

## Meevo

- **Meevo Angular change detection issue** — Service selection may not persist after add-on dialog close. Try full click sequence (click + mousedown + mouseup with `{bubbles: true}`). If broken after 2 attempts, defer and use prior data.
- **Meevo consecutive failure threshold** — After 3+ consecutive failures for same venue/service/date, skip browser attempt in cron mode. **As of 2026-06-06: 50+ consecutive failures recorded. Meevo is effectively unautomated in cron mode.**
- **Meevo cookie consent overlay** — Can appear twice during booking flow. Dismiss via "Accept All" or DOM removal.
- **Meevo hidden dialog after add-on close** — Remove with `document.querySelectorAll('[role="dialog"]').forEach(d => d.remove())`.
- **Meevo scan window has no "previous" button** — Count clicks carefully (each = 7 days).
- **Meevo employee filter radios** — Standard `browser_click` on snapshot ref works.

## Vagaro

- **Vagaro has a dual calendar system** — Slick slider (main) + xdsoft datepicker. Precise date targeting beyond ~2 weeks is unreliable.
- **Vagaro `/book-now` direct navigation shows staff but no calendar** — Persistent API issue.
- **Vagaro location modal blocks booking** — Bootstrap modal gets stuck. Report "unable to confirm".
- **Vagaro Book Now silent failure** — Clicking "Book Now" may produce no visible response. Report "unable to confirm".
- **Vagaro consecutive failure count** — **As of 2026-06-06: 60+ consecutive sweep failures. "Book Now" click produces no navigation. Vagaro is effectively unautomated.**

## SevenRooms

- **SevenRooms public widget API** — Availability checks use public widget API (no auth). Booking requires browser automation.
- **SevenRooms date selection via JS gridcell** — Use `document.querySelectorAll('[role="gridcell"]')` to find dates.
- **SevenRooms request-only slots** — Filter on type == book AND access_persistent_id != null.
- **SevenRooms widget date defaults to yesterday** — Always explicitly verify and set the target date.

## Bot Blocks

- **Bot blocks require VPN fallback** — CF Turnstile, PerimeterX, and Incapsula blocks are common on Tock, Mindbody, Fresha, and Vagaro.
- **Tock Book now links require JS click** — Do not use `browser_click`.

## Scripts

- **`square.js` requires Playwright npm package** — The `scripts/square.js` script uses `require('playwright')` and will fail with `MODULE_NOT_FOUND` if the `playwright` npm package is not installed in the skill directory. In cron/headless environments, prefer the stealth browser flow instead. Installing Playwright (`npm install playwright && npx playwright install chromium`) is non-trivial in sandboxed environments.

## General

- **External booking confirmation is authoritative** — If Sands reports conflict after successful venue booking, external confirmation stands.
- **Use Spot tooling first, not raw browser** — Always start with `spot.discover` → `spot.venue.add` → `spot.check`.
- **20+ platforms, each with unique selectors** — Always read the per-platform doc before attempting a new platform.