# Stealth Browser Square Flow — 2026-06-10 Update

## execute_script — Use Selectively (UPDATED 2026-06-10)

On 2026-06-08, `execute_script` returned null for DOM queries. **As of 2026-06-10, `execute_script` works for `window.location.href`** (returns correct URL string) but should still NOT be used for DOM queries or clicks — use `query_elements` + `click_element` for all DOM interaction.

**Safe to use `execute_script` for:**
- `window.location.href` — URL verification after navigation (e.g., confirming Book → /availability transition)

**Do NOT use `execute_script` for:**
- DOM queries (`document.querySelectorAll`) — use `query_elements` instead
- Clicking elements — use `click_element` instead
- Any interaction with Square's `market-*` custom elements

**Note:** Calling `execute_script` with the same script string twice in one session may trigger a false-positive "repeated_exact_failure_warning" from the tool loop detector. This is a detector artifact — if the script actually succeeded (check the result), ignore the warning.

## Stealth Browser Instance Connection Failure (2026-06-10)

The first `navigate` call on a freshly spawned stealth browser instance can fail with:
```
[Errno 111] Connect call failed ('127.0.0.1', 42631)
```

**Fix:** Re-spawn a new instance (`spawn_browser` → new instance_id) and navigate again. The second instance typically connects immediately. This appears to be a race condition where the browser process hasn't finished starting when the first CDP connection attempt is made.

## Built-in Browser Fails on Square — Use Stealth Browser

The built-in `browser_navigate` tool can fail on Square booking pages with:
```
net::ERR_INSUFFICIENT_RESOURCES
```

This occurs when the built-in browser session has accumulated too much state. **Always use the MCP stealth browser (`mcp_stealth_browser_*` tools) for Square Appointments.** Do not attempt `browser_navigate` as a first approach.

## Service Row Selection — CSS nth-child Approach (2026-06-08 cron)

The XPath text match approach (`//*[contains(text(), 'Swedish Massage')]`) for service selection can fail in stealth browser `click_element`. The reliable alternative is CSS `nth-child` on `market-row` elements:

```
click_element(selector="div[data-testid='services-page'] > market-row:nth-child(7)")
```

**Why nth-child(7) for the 6th service:** The first child of `div[data-testid='services-page']` is an `h2.sr-only` heading ("Services"). The `market-row` service elements start at child 2. So the Nth service row is at `nth-child(N+1)`.

**Service row structure (confirmed 2026-06-08):**
- `market-row` elements with `class*="service-row"`
- Each has an `href` attribute containing the service ID path
- `role="option"` is NOT set on service rows (unlike duration/staff options)
- `is_clickable: false` in query_elements (stealth browser reporting artifact — click_element still works)

**Full working flow with CSS nth-child (2026-06-08 20:15 PT — cron sweep):**

1. `spawn_browser(headless=true)` → instance_id
2. `navigate(instance_id, url="{booking_url}/services", wait_until="networkidle")` → services page
3. `click_element(instance_id, selector="button", text_match="Accept all cookies")` → dismiss cookie banner
4. `click_element(instance_id, selector="div[data-testid='services-page'] > market-row:nth-child(N)")` → select Nth service (accounting for h2 offset)
5. Page transitions to options/staff. `query_elements(instance_id, selector="market-list[aria-labelledby='service-variations-header'] > *")` → read duration options
6. `click_element(instance_id, selector="market-list[aria-labelledby='service-variations-header'] > market-row:nth-child(M)")` → select Mth duration option
7. `query_elements(instance_id, selector="market-list[aria-label='Staff'] > *")` → read staff options
8. `click_element(instance_id, selector="market-list[aria-label='Staff'] > market-row:nth-child(1)")` → select "Any staff" (first option)
9. `click_element(instance_id, selector="market-button", text_match="Book")` → proceed to calendar
10. `query_elements(instance_id, selector="market-button[data-testid^='date-']")` → read all date buttons
11. Check target date's `disabled` attribute
12. `close_instance(instance_id)`

**Primary: label[slot="label"] with text_match (2026-06-09, confirmed working)**

The XPath text-match approach (`//*[contains(text(), 'Swedish Massage')]`) can fail in stealth browser `click_element` with "Element not found" even when the element is visible. The reliable approach is CSS attribute selector targeting the `label` element inside the `market-row` shadow DOM:

```
click_element(selector="label[slot="label"]", text_match="Swedish Massage") → true
click_element(selector="label[slot="label"]", text_match="1.5 Hours") → true
click_element(selector="label[slot="label"]", text_match="Any staff") → true
```

Each `market-row` contains a `label` element with `slot="label"` holding the display text. These are directly queryable via CSS attribute selectors and respond reliably to `click_element`. The `text_match` parameter disambiguates when multiple labels exist.

**Full working flow with label selectors (2026-06-09 01:03 PT — cron sweep):**

1. `spawn_browser(headless=true)` → instance_id
2. `navigate(instance_id, url="{booking_url}/services", wait_until="domcontentloaded")` → services page
3. `click_element(instance_id, selector="button", text_match="Accept all cookies")` → dismiss cookie banner
4. `click_element(instance_id, selector="label[slot="label"]", text_match="Swedish Massage")` → page transitions to duration/staff
5. `click_element(instance_id, selector="label[slot="label"]", text_match="1.5 Hours")` → duration selected
6. `click_element(instance_id, selector="label[slot="label"]", text_match="Any staff")` → staff selected
7. `click_element(instance_id, selector="market-button", text_match="Book")` → proceed to calendar
8. `query_elements(instance_id, selector="market-button[data-testid^='date-']")` → read all date buttons
9. Check target date's `disabled` attribute
10. `close_instance(instance_id)`

**Fallback if label selector doesn't work:** Use CSS `nth-child` on `market-row` elements (see below).

## Duration/Staff Selection via [role="option"][value="..."] (2026-06-10, confirmed)

The most reliable approach for selecting duration and staff options uses CSS attribute selectors targeting `role="option"` with the `value` attribute:

```python
# Select duration by value (from query_elements attributes.value)
click_element(selector="[role=\"option\"][value=\"HE3ILSU3JFOUZYTV4DZLFSRO\"]")  # 1.5 Hours

# Select "Any staff"
click_element(selector="[role=\"option\"][value=\"ANY_STAFF\"]")
```

**How to find the value:** First call `query_elements(selector="[role=\"option\"]")` to list all options. Each result has an `attributes.value` field. Match by text content (e.g., "1.5 Hours $145.00・1 hr 30 min") and extract the `value` for the `click_element` call.

**Why this is preferred over label[slot="label"]:** The `value` attribute is a stable identifier that doesn't depend on display text formatting. It works even when the label text is truncated or contains special characters.

**Full working flow with value selectors (2026-06-10 23:21 PT — cron sweep):**

1. `spawn_browser(headless=true)` → instance_id
2. `navigate(instance_id, url="{booking_url}?date=YYYY-MM-DD", wait_until="networkidle")` → services page
3. `click_element(instance_id, selector="#accept-recommended-btn-handler")` → dismiss cookie banner (use CSS ID selector, faster than text_match)
4. `query_elements(instance_id, selector="market-row")` → list all services, find target by text
5. `click_element(instance_id, selector="market-row[href*=\"SERVICE_ID\"]")` → select service by href containing service ID
6. `query_elements(instance_id, selector="[role=\"option\"]")` → list duration + staff options
7. `click_element(instance_id, selector="[role=\"option\"][value=\"DURATION_VALUE\"]")` → select duration
8. `click_element(instance_id, selector="[role=\"option\"][value=\"ANY_STAFF\"]")` → select any staff
9. `query_elements(instance_id, selector="[role=\"option\"][aria-selected=\"true\"]")` → verify both selections show `aria-selected="true"` and `selected=""`
10. `click_element(instance_id, selector="market-button[rank=\"primary\"][type=\"button\"]")` → click Book
11. `execute_script(instance_id, script="window.location.href")` → verify URL contains `/availability`
12. `query_elements(instance_id, selector="[data-testid^='date-']")` → read all date buttons
13. Verify target date is selected (`data-testid="date-N-selected"`, `aria-pressed="true"`)
14. `query_elements(instance_id, selector="[data-testid='time-slot']")` → read all available time slots
15. Filter slots to time_window, compare with last_found
16. `close_instance(instance_id)`

## Calendar Navigation via click_element (2026-06-08)

The "Next week" button on Square's calendar CAN be clicked via `click_element` with a CSS attribute selector:

```
click_element(selector="market-button[data-testid='next-week-button']") → true
```

## Complete Verified Flow (2026-06-08 14:15 PDT — cron sweep)

1. `spawn_browser(headless=true)` → instance_id
2. `navigate(instance_id, url="{booking_url}/services", wait_until="domcontentloaded")` → services page loads
3. `click_element(instance_id, selector="button", text_match="Accept all cookies")` → dismiss cookie banner
4. `click_element(instance_id, selector="//*[contains(text(), 'Swedish Massage')]", text_match="Swedish Massage")` → page transitions to duration/staff
5. `click_element(instance_id, selector="//*[contains(text(), '1.5 Hours')]/ancestor::label", text_match="1.5 Hours")` → duration selected
6. `click_element(instance_id, selector="//*[contains(text(), 'Any staff')]", text_match="Any staff")` → staff selected
7. `click_element(instance_id, selector="//button[contains(text(), 'Book')] | //market-button[contains(text(), 'Book')]", text_match="Book")` → clicked
8. `query_elements(instance_id, selector="market-button[data-testid^='date-']")` → read calendar dates (shows current week)
9. `click_element(instance_id, selector="market-button[data-testid='next-week-button']")` → advance to next week
10. `query_elements(instance_id, selector="market-button[data-testid^='date-']")` → read dates again (now shows week containing target)
11. Check target date's `disabled` attribute — no attribute = available
12. `click_element(instance_id, selector="market-button[data-testid='date-19']")` → click target date
13. `query_elements(instance_id, selector="market-button[data-testid='time-slot']")` → read all available time slots
14. `close_instance(instance_id)`

**Result**: June 19 (Fri) — 26 total slots (10:00 AM – 5:15 PM). 7 in 3:30–5:00 PM window (3:30, 3:45, 4:00, 4:15, 4:30, 4:45, 5:00) — unchanged from prior sweep.

## XPath vs CSS Selectors for Square Custom Elements

Square uses `market-*` custom elements (web components). Both XPath and CSS selectors work with `click_element`:

| Approach | Example | Works? |
|----------|---------|--------|
| CSS attribute selector | `market-button[data-testid='next-week-button']` | ✅ Yes |
| XPath text match | `//*[contains(text(), 'Swedish Massage')]` | ✅ Yes |
| CSS class selector | `market-row.service-row` | ✅ Yes |
| XPath ancestor | `//*[contains(text(), '1.5 Hours')]/ancestor::label` | ✅ Yes |

**Recommendation**: Use CSS attribute selectors for `data-testid` elements (dates, time slots, navigation buttons). Use XPath with `text_match` for elements identified by text content (services, durations, staff, Book button).

## Square Calendar Viewport Behavior (2026-06-10)

The date strip extends beyond the 1920px viewport. In the 2026-06-10 sweep, date elements had x positions ranging from -104 (past dates) to 1592 (future dates). **No scrolling is needed** — all dates are in the DOM and queryable via `query_elements` even when partially off-screen. The stealth browser renders them all; `query_elements` returns them regardless of viewport position.

The calendar auto-shows ~3 weeks: past days (disabled), current week, and future weeks up to the booking window. If the target date is not in the initial view, use the "Next week" button (`market-button[data-testid='next-week-button']`) to advance.

## Time Slot Interpretation

- `market-button[data-testid='time-slot']` elements appear for ALL available slots on the selected date
- Time slots do NOT use `disabled` attribute — if listed, the slot is bookable
- If clicking a date produces zero time-slot elements, the date has no availability
- Time slot text format: `"4:45 PM"`, `"5:00 PM"` etc. — use these directly for comparison with `last_found`

## Square Calendar Date State Interpretation

- `disabled=""` attribute present → date is unavailable. For **past** dates this is normal. For **future** dates this means the date is outside the booking window (venue hasn't opened bookings that far out) OR fully booked.
- No `disabled` attribute → date is available and clickable
- `aria-pressed="true"` → date is currently selected
- `data-testid="date-N-selected"` → selected date (vs `data-testid="date-N"` for unselected)

**Booking window behavior (confirmed 2026-06-08):** Square calendars show ~3 weeks but future dates beyond the venue's booking window render as `disabled`. Russamee Traditional Thai Massage showed dates 14-20 as disabled on June 8, meaning the booking window extended only ~1 week out. When a target date is disabled, preserve `last_found` data and re-check in a few days — the date may become available as the window advances.

When the calendar spans two months in month view, dates with the same day number from different months both render with the same `data-testid="date-N"`. Use the surrounding context (which dates are disabled vs. enabled) to disambiguate.

## Cookie Banner

Always dismiss the OneTrust cookie banner as step 3 (after navigation, before clicking any service). Without dismissing it, subsequent clicks may not register on overlapping elements.

**Fastest selector:** `click_element(selector="#accept-recommended-btn-handler")` — uses the button's CSS ID directly, no text matching needed.

**Fallback:** `click_element(selector="button", text_match="Accept all cookies")` — works but slower due to text search.