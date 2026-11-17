# Stealth Browser Square Flow — 2026-06-06 Update

## Text Match Length Sensitivity (NEW)

When using `click_element(instance_id, selector, text_match="...")` on elements with long visible text (e.g., Square's `market-row` which contains service name + description), **the match FAILS if the text_match string is too long or includes a partial description suffix**.

**Failure pattern (confirmed 2026-06-06):**
```
text_match="Swedish Massage A soothing"  → "Element not found: market-row"
text_match="Swedish Massage"             → success ✓
```

**Rule: Use the shortest unique prefix for `text_match`.**

| Element | Good `text_match` | Bad `text_match` |
|---------|-------------------|------------------|
| Service (e.g., Swedish Massage) | `"Swedish Massage"` | `"Swedish Massage A soothing..."` |
| Service (e.g., Thai Combination & Foot Massage) | `"Thai Combination & Foot"` | `"Thai Combination & Foot Massage Full body..."` |
| Duration | `"1.5 Hours"` | `"1.5 Hours $145.00・1 hr 30 min"` |
| Staff | `"Any staff"` | `"Any staff\n$0.00"` |
| Book button | `"Book"` | (full string is fine — short text) |

## Confirmed Clean Flow (2026-06-06 03:14 PDT)

1. `spawn_browser(headless=true, sandbox=false)` → instance_id
2. `navigate(instance_id, url="{booking_url}?date=2026-06-19", wait_until="networkidle")` → redirects to `/services?date=` (expected)
3. `query_elements(instance_id, selector="market-row", limit=20)` → read all services
4. `click_element(instance_id, selector="market-row", text_match="Swedish Massage")` → page transitions to duration/staff
5. `query_elements(instance_id, selector="[role=\"option\"]", limit=20)` → read options
6. `click_element(instance_id, selector="[role=\"option\"]", text_match="1.5 Hours")`
7. `click_element(instance_id, selector="[role=\"option\"]", text_match="Any staff")`
8. `query_elements(instance_id, selector="[role=\"option\"]")` → verify `aria-selected="true"` + `selected` on both
9. `query_elements(instance_id, selector="market-button", limit=10)` → find Book
10. `click_element(instance_id, selector="market-button", text_match="Book")`
11. `get_page_content(instance_id)` → parse file path → verify `/availability` + read slots
12. `close_instance(instance_id)`

**Result**: 34 total slots (Morning 8, Afternoon 16, Evening 10). 7 in 3:30-5:00 PM window unchanged.

## All-JS Variant (2026-06-06 03:43 PDT — crashed post-Book)

An alternative approach using `execute_script` for all interactions in fewer round-trips. This reduces the window for CDP connection drops but does NOT prevent the post-Book `get_page_content` timeout crash.

**Flow:**
```
1. spawn_browser → instance_id
2. navigate(instance_id, url="{booking_url}?date=YYYY-MM-DD")
3. execute_script: click MARKET-ROW for service
4. wait_for_element(selector="[role='option']")
5. execute_script: click duration [role="option"] + click staff [role="option"] + setAttribute selected/aria-selected + click market-button Book
6. get_page_content(instance_id) → TIMEOUT (120s) ← CRASH POINT
```

**Result**: All 4 JS interactions succeeded (service click, duration click, staff setAttribute, Book click all returned `bookClicked: true`), but `get_page_content` timed out. Browser was dead. Used last_known data.

**Trade-off**: The all-JS variant is faster (fewer round-trips) but has the same post-Book crash rate. The step-by-step `click_element` variant allows verification between each step and can recover from a CDP drop mid-flow by spawning a new instance. **Recommend the step-by-step variant for reliability; use all-JS only when speed matters more than verification.**

## Confirmed Clean Flow (2026-06-06 05:52 PDT — cron sweep)

Same step-by-step pattern as the 03:14 run. Full flow completed cleanly:

1. `spawn_browser(headless=true, sandbox=false)` → instance_id
2. `navigate(instance_id, url="{booking_url}?date=2026-06-19", wait_until="networkidle")` → redirects to `/services?date=` (expected)
3. `query_elements(instance_id, selector="market-row")` → 13 services found
4. `click_element(instance_id, selector="market-row", text_match="Swedish Massage")` → page transitions
5. `query_elements(instance_id, selector="[role=\"option\"]")` → 9 options (3 durations + 6 staff)
6. `click_element(instance_id, selector="[role=\"option\"]", text_match="1.5 Hours")` → duration selected
7. `click_element(instance_id, selector="[role=\"option\"]", text_match="Any staff")` → staff selected
8. `query_elements(instance_id, selector="[role=\"option\"]")` → verified `aria-selected="true"` + `selected` on both
9. `click_element(instance_id, selector="market-button", text_match="Book")` → clicked
10. `get_page_content(instance_id)` → 2990 KB file → parsed with Python
11. `close_instance(instance_id)`

**Result**: 34 total slots. 7 in 3:30-5:00 PM window (3:30, 3:45, 4:00, 4:15, 4:30, 4:45, 5:00) — unchanged from prior sweep.

**Note**: `wait_until="networkidle"` is the correct parameter name for stealth browser `navigate` (not `wait` which is the Hermes browser parameter name). Using `wait` causes a validation error.

## Confirmed Clean Flow (2026-06-06 06:56 PDT — cron sweep, autonomous)

Same step-by-step pattern. Full flow completed cleanly in autonomous cron mode (no human intervention):

1. `spawn_browser(headless=true, sandbox=false)` → instance_id
2. `navigate(instance_id, url="{booking_url}?date=2026-06-19", wait_until="load")` → page loads on first try
3. `query_elements(instance_id, selector="market-row")` → 13 services found
4. `click_element(instance_id, selector="market-row", text_match="Swedish Massage")` → page transitions
5. `query_elements(instance_id, selector="[role='option']")` → 9 options (3 durations + 6 staff)
6. `click_element(instance_id, selector="[role='option']", text_match="1.5 Hours")` → duration selected
7. `click_element(instance_id, selector="[role='option']", text_match="Any staff")` → staff selected
8. `query_elements(instance_id, selector="[role='option']")` → verified `aria-selected="true"` + `selected` on both
9. `click_element(instance_id, selector="market-button", text_match="Book")` → clicked
10. `get_page_content(instance_id)` → 2990 KB file → parsed with Python
11. `close_instance(instance_id)`

**Result**: 34 total slots (Morning 8, Afternoon 20, Evening 6). 7 in 3:30-5:00 PM window (3:30, 3:45, 4:00, 4:15, 4:30, 4:45, 5:00) — unchanged.

**Significance**: This was a fully autonomous cron sweep — the stealth browser Square flow completed end-to-end without any human intervention, including file parsing and watch record updates. This validates the stealth browser as the definitive primary method for Square in cron mode.

## Alternative Flow: Base URL + Calendar Navigation (2026-06-06 19:00 PDT — cron sweep)

When the `?date=` parameter approach is not used (e.g., when the skill references weren't loaded in a cron session), the base URL approach also works but requires extra calendar navigation steps:

1. `spawn_browser(headless=true, sandbox=false)` → instance_id
2. `navigate(instance_id, url="{booking_url}", wait_until="networkidle")` → redirects to `/services`
3. `click_element(instance_id, selector="button", text_match="Accept all cookies")` → dismiss cookie banner
4. `click_element(instance_id, selector="market-row", text_match="Swedish Massage")` → page transitions to duration/staff
5. `click_element(instance_id, selector="market-row", text_match="1.5 Hours")` → duration selected
6. `click_element(instance_id, selector="market-row", text_match="Any staff")` → staff selected
7. `click_element(instance_id, selector="market-button", text_match="Book")` → clicked
8. `wait_for_element(instance_id, selector="market-button[data-testid^='date-']")` → calendar loads (shows current week)
9. **Navigate to target week**: Use `execute_script` to click "Next week" button (CSS selector fails — see gotchas):
   ```javascript
   (function() {
     const btns = document.querySelectorAll('market-button');
     for (const btn of btns) {
       if (btn.getAttribute('aria-label') === 'Next week') { btn.click(); return 'clicked'; }
     }
     return 'not found';
   })()
   ```
10. Repeat step 9 as needed to reach target date's week
11. `execute_script` to read date button states:
    ```javascript
    (function() {
      const dateButtons = document.querySelectorAll('market-button[data-testid^="date-"]');
      const dates = [];
      dateButtons.forEach(btn => {
        const day = parseInt(btn.getAttribute('data-testid').replace('date-', '').replace('-selected', ''));
        const disabled = btn.hasAttribute('disabled');
        dates.push({ day, disabled });
      });
      return dates;
    })()
    ```
12. Check if target date `disabled === true` (fully booked) or `false` (available)
13. `close_instance(instance_id)`

**Result (2026-06-19 check)**: June 19 date-button `disabled=true` — fully booked, no availability.

**Trade-off**: The base URL approach requires 2+ extra round-trips for calendar navigation and the `execute_script` workaround for the "Next week" button. The `?date=` parameter approach is more direct and should be preferred when the skill references are available.

## Confirmed Clean Flow (2026-06-06 12:03 PDT — cron sweep, autonomous)

Same step-by-step pattern. Full flow completed cleanly in autonomous cron mode:

1. `spawn_browser(headless=true, sandbox=false)` → instance_id
2. `navigate(instance_id, url="{booking_url}?date=2026-06-19", wait_until="networkidle")` → redirects to `/services?date=` (expected)
3. `query_elements(instance_id, selector="market-row")` → 13 services found
4. `click_element(instance_id, selector="market-row", text_match="Swedish Massage")` → page transitions
5. `query_elements(instance_id, selector="[role='option']")` → 9 options (3 durations + 6 staff)
6. `click_element(instance_id, selector="[role='option']", text_match="1.5 Hours")` → duration selected
7. `click_element(instance_id, selector="[role='option']", text_match="Any staff")` → staff selected
8. `query_elements(instance_id, selector="[role='option']")` → verified `aria-selected="true"` + `selected` on both
9. `click_element(instance_id, selector="market-button", text_match="Book")` → clicked
10. `get_page_content(instance_id)` → 2990 KB file → parsed with Python
11. `close_instance(instance_id)`

**Result**: 34 total slots. 7 in 3:30-5:00 PM window (3:30, 3:45, 4:00, 4:15, 4:30, 4:45, 5:00) — unchanged.

**Significance**: 4th consecutive clean stealth browser Square sweep on the same day. The flow is stable and reliable in autonomous cron mode.

## Confirmed Clean Flow (2026-06-06 12:35 PDT — cron sweep, autonomous)

Same step-by-step pattern. Full flow completed cleanly in autonomous cron mode:

1. `spawn_browser(headless=true, sandbox=false)` → instance_id
2. `navigate(instance_id, url="{booking_url}?date=2026-06-19", wait_until="networkidle")` → redirects to `/services?date=` (expected)
3. `query_elements(instance_id, selector="market-row")` → 13 services found
4. `click_element(instance_id, selector="market-row", text_match="Swedish Massage")` → page transitions
5. `query_elements(instance_id, selector="[role='option']")` → 9 options (3 durations + 6 staff)
6. `click_element(instance_id, selector="[role='option']", text_match="1.5 Hours")` → duration selected
7. `click_element(instance_id, selector="[role='option']", text_match="Any staff")` → staff selected
8. `query_elements(instance_id, selector="[role='option']")` → verified `aria-selected="true"` + `selected` on both
9. `click_element(instance_id, selector="market-button", text_match="Book")` → clicked
10. `get_page_content(instance_id)` → 2990 KB file → parsed with Python
11. `close_instance(instance_id)`

**Result**: 34 total slots (Morning 8, Afternoon 20, Evening 6). 7 in 3:30-5:00 PM window (3:30, 3:45, 4:00, 4:15, 4:30, 4:45, 5:00) — unchanged.

**Significance**: 5th consecutive clean stealth browser Square sweep on the same day. The flow is stable and reliable in autonomous cron mode.

## Confirmed Clean Flow (2026-06-06 13:21 PDT — cron sweep, autonomous)

Same step-by-step pattern. Full flow completed cleanly in autonomous cron mode:

1. `spawn_browser(headless=true, sandbox=false)` → instance_id
2. `navigate(instance_id, url="{booking_url}?date=2026-06-19", wait_until="networkidle")` → redirects to `/services?date=` (expected)
3. `query_elements(instance_id, selector="market-row")` → 13 services found
4. `click_element(instance_id, selector="market-row", text_match="Swedish Massage")` → page transitions
5. `query_elements(instance_id, selector="[role='option']")` → 9 options (3 durations + 6 staff)
6. `click_element(instance_id, selector="[role='option']", text_match="1.5 Hours")` → duration selected
7. `click_element(instance_id, selector="[role='option']", text_match="Any staff")` → staff selected
8. `query_elements(instance_id, selector="[role='option']")` → verified `aria-selected="true"` + `selected` on both
9. `click_element(instance_id, selector="market-button", text_match="Book")` → clicked
10. `get_page_content(instance_id)` → 2990 KB file → parsed with Python
11. `close_instance(instance_id)`

**Result**: 34 total slots (Morning 8, Afternoon 20, Evening 6). 7 in 3:30-5:00 PM window (3:30, 3:45, 4:00, 4:15, 4:30, 4:45, 5:00) — unchanged.

**Significance**: 6th consecutive clean stealth browser Square sweep on the same day. The flow is fully stable and reliable in autonomous cron mode.

## Hermes Browser Flow (2026-06-06 22:00 PDT — cron sweep)

This sweep used the Hermes browser (built-in browser tools) instead of stealth browser, confirming the Hermes browser as a viable primary method:

1. `browser_navigate(url="{booking_url}?date=2026-06-19")` → page loads on first try, redirects to `/services?date=`
2. `browser_snapshot` → 13 services found, clicked "Swedish Massage" ref
3. `browser_snapshot` → 9 options (3 durations + 6 staff), clicked "1.5 Hours" ref → `checked=true` ✓
4. `browser_snapshot` → clicked "Any staff" ref → **`checked=false` ✗ (silent failure)**
5. `browser_console` JS fallback: `document.querySelectorAll('[role="option"]')` → find "Any staff" → `.click()` + `setAttribute('selected','true')` + `setAttribute('aria-selected','true')` → success
6. Verified both selections via snapshot
7. `browser_click` on Book button ref
8. `browser_console(expression="window.location.href")` → `/availability` ✓
9. `browser_snapshot` → read all time slots

**Result**: 34 total slots (Morning 8, Afternoon 20, Evening 6). 7 in 3:30-5:00 PM window (3:30, 3:45, 4:00, 4:15, 4:30, 4:45, 5:00) — unchanged.

**Key learning**: `browser_click` on `[role="option"]` refs for staff selection silently fails in Hermes browser too. The JS fallback is required for both stealth and Hermes browser flows. Duration selection via `browser_click` works reliably in both.

## Base URL + Calendar Navigation (2026-06-07 00:55 PDT — cron sweep)

When using the base URL (no `?date=` parameter), the calendar navigation flow requires extra steps. This session confirmed the full base-URL flow:

1. `spawn_browser(headless=true, sandbox=false)` → instance_id
2. `navigate(instance_id, url="{booking_url}", wait_until="domcontentloaded")` → redirects to `/services`
3. `click_element(instance_id, selector="button", text_match="Accept all cookies")` → dismiss cookie banner
4. `click_element(instance_id, selector="market-row", text_match="Swedish Massage")` → page transitions to duration/staff
5. **Duration/staff selection via `market-radio`**: `query_elements(selector="market-radio")` → read all options with `aria-label` attributes. Then `click_element(selector="market-radio[aria-label='1.5 Hours']")` and `click_element(selector="market-radio[aria-label='Any staff']")`. Note: `market-radio` elements have `selected=""` attribute when selected.
6. `click_element(instance_id, selector="market-button[rank='primary']")` → clicked "Book"
7. Calendar loads showing current week. Use `query_elements(selector="market-button[data-testid^='date-']")` to read all date buttons.
8. **Navigate to target week**: Click `[data-testid='next-week-button']` repeatedly until target date's week is visible. Each click advances one week.
9. **Check date availability**: Read `disabled` attribute on target date button. `disabled=""` = not available (either past or fully booked). No `disabled` attribute = available.
10. **Critical**: `execute_script` returned null for ALL DOM queries in this session. Do NOT use it for data extraction. Use `query_elements` for reading element states.
11. `close_instance(instance_id)`

**Result (2026-06-19 check)**: June 19 showed `disabled=""` — the calendar had auto-advanced to display-date June 21, making June 19 part of the "past week" (dates 14-20 all disabled). Available dates started June 21. The target date was not actually booked — it was simply in the past relative to the calendar's displayed date.

**Key learning**: When a target date shows as disabled, check the calendar's `displayed-date` (from `market-date-picker` element) to determine if the date is actually unavailable or just in the past week. If the target date is before the displayed date, advance the calendar forward and recheck.