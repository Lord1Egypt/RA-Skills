# Square Availability — Date-Targeted Flow (Verified 2026-05-30, 2026-06-01x2, 2026-06-03)

**Pattern:** Navigate to base URL with `?date=` parameter → full flow → availability loads on target date directly.

## Discovery

On 2026-06-01, after a failed `browser_navigate` to `/availability?date=2026-06-19` (which redirected to `/services`), the subsequent full flow (click service → duration → staff → Book) landed the availability page directly on `/availability?date=2026-06-19` showing June 19 — **without a separate URL date jump step**.

**Root cause:** Square's server-side session tracks the `?date=` parameter from the initial navigation URL, even though the browser redirects to `/services`. The date is preserved through the entire booking flow server-side. When Book is clicked, Square constructs the availability URL with the remembered date.

## Confirmation History

| Date | Session | Result | Notes |
|------|---------|--------|-------|
| 2026-05-30 | interactive | ✅ Success | First clean run, no OneTrust overlay |
| 2026-06-01 AM | interactive | ✅ Success | Book→snapshot-verify→navigate pattern |
| 2026-06-01 PM (cron) | cron | ✅ Success | Server-side date tracking, double-click staff, month grid view |
| 2026-06-01 PM (cron 2) | cron | ✅ Success | Clean run, double-click Any staff (first checked=false, second checked=true), no OneTrust, 6 slots in 3:30-5:00 PM window unchanged |
| 2026-06-01 PM (cron 3) | cron | ✅ Success | Clean run, selections confirmed via `[selected]` attribute in single snapshot, no OneTrust, 6 slots in window unchanged. Service list shows 8+ options (more than venue record). |
| 2026-06-03 (cron) | cron | ✅ Success | Clean run. Service row clicked via JS `document.querySelectorAll('MARKET-ROW')` (browser_click silently fails). Duration 1.5hr selected via browser_click (worked). Staff "Any staff" required JS click + setAttribute('selected','true') + setAttribute('aria-selected','true') — browser_click double-click returned checked=false both times. URL date jump unnecessary — server-side date tracking loaded June 19 directly. No OneTrust overlay. |
| 2026-06-03 (cron 2) | cron | ✅ Success (retry) | First attempt: Book click → `about:blank` (transient navigation failure). `browser_snapshot` returned empty page. Recovery: re-navigated to base URL with `?date=`, re-ran full flow, succeeded on second attempt. No Chrome kill needed — `about:blank` is a transient server-side failure, not a browser crash. |
|| 2026-06-03 (cron 3) | cron | ✅ Success | Clean run. JS MARKET-ROW click for service, browser_click for duration, JS [role="option"] + setAttribute for staff, Book → /availability verified via browser_console URL check. Server-side date tracking loaded June 19 directly. No OneTrust overlay. 6 slots in 3:30-5:00 PM window unchanged. |
|| 2026-06-03 (cron 4) | cron | ✅ Success | Clean run. Service row text-matching required excluding packaged tier names (Buachompoo/Sarocha/Pairin/Orracha) that also contain "Swedish Massage" in description. JS MARKET-ROW click with exclusion pattern worked. Duration via browser_click, staff via JS+setAttribute, Book→/availability verified. Server-side date tracking loaded June 19 directly. No OneTrust overlay. 6 slots in window unchanged. |
| 2026-06-03 (cron 5) | cron | ✅ Success | Clean run. JS MARKET-ROW click for Swedish Massage (with packaged tier exclusion), browser_click for 1.5hr duration, JS [role=option]+setAttribute for Any staff, Book→/availability verified via browser_console URL check. Server-side date tracking loaded June 19 directly. No OneTrust overlay. 34 total slots (Morning 8, Afternoon 20, Evening 6). 6 slots in 3:30-5:00 PM window unchanged. |
| 2026-06-03 (cron 6) | cron | ✅ Success | Clean run. JS MARKET-ROW click for Swedish Massage (with packaged tier exclusion), browser_click for 1.5hr duration, JS [role=option]+setAttribute for Any staff, Book→/availability verified via browser_console URL check. Server-side date tracking loaded June 19 directly. No OneTrust overlay. 34 total slots (Morning 8, Afternoon 20, Evening 6). 6 slots in 3:30-5:00 PM window unchanged. |
| 2026-06-04 (cron) | cron | ✅ Success | Clean run. JS MARKET-ROW click for Swedish Massage (with packaged tier exclusion), browser_click for 1.5hr duration, JS [role=option]+setAttribute for Any staff, Book→/availability verified via browser_console URL check. Server-side date tracking loaded June 19 directly. No OneTrust overlay. 34 total slots. 7 slots in 3:30-5:00 PM window unchanged. 22nd+ consecutive clean Square run. |
| 2026-06-04 (cron 2) | cron | ✅ Success | Clean run. JS MARKET-ROW click for Swedish Massage (with packaged tier exclusion), browser_click for 1.5hr duration (ref=e16), JS [role=option]+setAttribute for Any staff, Book→/availability verified via browser_console URL check. Server-side date tracking loaded June 19 directly. No OneTrust overlay. 34 total slots (Morning 8, Afternoon 20, Evening 6). 7 slots in 3:30-5:00 PM window unchanged. 24th+ consecutive clean Square run. |

**This pattern is now the recommended PRIMARY approach for Square date-targeted availability checks.** Reliability: 13/13 across interactive and cron sessions (including 1 retry).

## Optimized Flow

```
1. browser_navigate(url="{base_booking_url}?date=YYYY-MM-DD")   ← browser WILL redirect to /services — this is NORMAL, not a failure
2. Click service row via JS: document.querySelectorAll('MARKET-ROW') → find by text → .click()
   ← browser_click on service row refs silently fails — JS click is the PRIMARY method
3. Click duration option via browser_click on [role="option"] ref ← works fine
4. Click "Any staff" via JS: document.querySelectorAll('[role="option"]') → find "Any staff" → .click() + setAttribute('selected','true') + setAttribute('aria-selected','true')
   ← browser_click on staff [role="option"] refs reliably fails even with double-click — JS is the PRIMARY method
5. Click "Book" via browser_click on button ref ← works fine
6. CRITICAL GATE: check URL via `browser_console(expression="window.location.href")` — verify it shows /availability
   - If yes → read slots directly (month grid showing target date)
   - If no (redirected to /services or about:blank) → session was truly lost, re-do full flow from step 1
   - **Use `browser_console`, NOT `browser_snapshot`** for the gate check: `browser_snapshot` can return an empty page during transient states, while `browser_console` returns the actual URL immediately
```

**No separate URL date jump needed.** The `?date=` parameter from the original `browser_navigate` call is preserved server-side through the entire flow.

**Summary of interaction method by step:**
| Step | Method | Why |
|------|--------|-----|
| Service row click | JS `MARKET-ROW` querySelector | `browser_click` on ref silently fails |
| Duration selection | `browser_click` on ref | Works — standard ARIA option |
| Staff selection | JS `[role="option"]` + setAttribute | `browser_click` fails even with double-click |
| Book button | `browser_click` on ref | Works — standard button element |

**⚠️ Service name text-matching**: Some venues list packaged/multi-service tiers (e.g., "Buachompoo", "Sarocha") that include the base service name in their description. When searching `MARKET-ROW` elements by text content, the query may match a packaged tier instead of the standalone service row or fail to find an exact match. **Fix**: Exclude packaged tier names from the text search (they're usually capitalized proper nouns), or match on the service name alone AND exclude rows whose text also contains known tier names. If the first click doesn't navigate to `/services/{serviceId}`, retry with a more specific query.

## Comparison with Two-Step Approach

| Approach | Steps | Reliability |
|----------|-------|-------------|
| **Two-step** (go to availability, then URL date jump) | Navigate → flow → Book → /availability → browser_navigate(/availability?date=YYYY-MM-DD) | URL jump can redirect to /services if session was reset by browser_navigate |
| **Server-side date tracking** (this pattern) | browser_navigate(?date=) → flow → Book → availability on target date | **Recommended** — avoids extra navigation that resets session |

## Favor This Pattern

When checking availability for a specific date, use the server-side date tracking pattern instead of the two-step URL jump approach. It avoids the extra `browser_navigate` call that can reset the session.

**Note:** The `?date=` parameter on the initial `browser_navigate` call doesn't prevent the page from loading the services listing. It just sets a server-side cookie/session value. This is different from `?service_id=` which crashes the page.

## Month Grid View

When this pattern works, the availability page renders in **month grid view** (not week view) with:
- Full month calendar grid (buttons for days 1-30)
- A heading for the target date (e.g., "Friday, Jun 19, 2026")
- Time slots listed below the grid, grouped by Morning / Afternoon / Evening

This avoids the need for "Next week" clicks entirely. The month heading (e.g., "Jun 2026") confirms the correct month loaded.