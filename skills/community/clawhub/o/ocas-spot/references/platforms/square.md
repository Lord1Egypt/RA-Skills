# Square Appointments

**Status:** ⚠️ Working (Browser automation required)
**Method:** Playwright / stealth browser with custom element handling
**Last Updated:** 2026-05-21
**Example Sites:** Shade Nail Spa (app.squareup.com), Russamee Traditional Thai Massage (book.squareup.com)

> **IMPORTANT (May 2026):** The booking flow and calendar navigation differ significantly from earlier documentation. Read this entire file before implementing.

---

## Booking Flow (Updated May 2026)

### Step 0: Accept Cookies

When the booking page loads, a cookie consent overlay appears. Accept cookies FIRST before any other interaction:

```javascript
// Via stealth browser JS execution
(function() {
  var btns = document.querySelectorAll('button');
  for (var i = 0; i < btns.length; i++) {
    if (btns[i].textContent?.trim() === 'Accept all cookies') {
      btns[i].click();
      return 'clicked';
    }
  }
  return 'not found';
})()
```

### Step 1: Navigate to Service Selection

Navigate to the booking URL (the location URL, NOT with service_id — the old `?service_id=` param pattern caused "something went wrong" errors in testing):

```
https://book.squareup.com/appointments/{location_id}/location/{location_hash}
```

This redirects to `/services` where all services are listed. Do NOT try to skip this step.

### Step 2: Click a Service

Services are in `market-row.service-row` elements. Click the anchor inside:

```javascript
(function() {
  var rows = document.querySelectorAll('market-row.service-row');
  for (var i = 0; i < rows.length; i++) {
    var text = rows[i].textContent?.trim() || '';
    if (text.startsWith('Traditional Thai Massage') && !text.includes('Combination')) {
      var anchor = rows[i].querySelector('a') || rows[i].shadowRoot?.querySelector('a');
      if (anchor) { anchor.click(); return 'clicked anchor'; }
      rows[i].click(); return 'clicked row';
    }
  }
  return 'not found';
})()
```

URL changes to `/services/{SERVICE_ID}` confirming selection.

### Step 3: Select Duration and Staff

On the service detail page, select duration and staff via `market-radio` elements:

```javascript
(function() {
  var radios = document.querySelectorAll('market-radio');
  for (var i = 0; i < radios.length; i++) {
    if (radios[i].getAttribute('aria-label') === '1 Hour') { radios[i].click(); break; }
  }
  for (var j = 0; j < radios.length; j++) {
    if (radios[j].getAttribute('aria-label') === 'Any staff') { radios[j].click(); break; }
  }
  return 'selected 1 Hour + Any staff';
})()
```

### Step 4: Click "Book"

The "Book" button is a `market-button` with NO aria-label — only text content:

```javascript
(function() {
  var allEl = document.querySelectorAll('market-button');
  for (var i = 0; allEl.length; i++) {
    if (allEl[i].textContent?.trim() === 'Book') {
      allEl[i].click();
      return 'clicked Book';
    }
  }
  return 'not found';
})()
```

URL changes to `/availability`.

### Step 5: Navigate Calendar (CRITICAL — Week-by-Week)

**⚠️ CRITICAL UPDATE (May 2026):** Even in month view, Square's calendar has **NO month-level navigation buttons**. There is no "Next month" button. The calendar header `flex` div contains only:
- `h2` with month name (e.g. "May 2026")
- `market-button[aria-label="Previous week"]`
- `market-button[aria-label="Next week"]`

The "Expand to show month view" button shows ~3 weeks spanning two months, but navigation is always **week-by-week**.

```javascript
// Navigate to target week
(function() {
  var mb = document.querySelectorAll('market-button');
  for (var i = 0; i < mb.length; i++) {
    if (mb[i].getAttribute('aria-label') === 'Expand to show month view') {
      mb[i].click(); return 'expanded to month view';
    }
  }
  var collapse = document.querySelector('market-button[aria-label="Collapse to show week view"]');
  if (collapse) return 'already in month view';
  return 'month view toggle not found';
})()
```

Then click "Next week" repeatedly:

```javascript
(function() {
  var mb = document.querySelectorAll('market-button');
  for (var i = 0; i < mb.length; i++) {
    if (mb[i].getAttribute('aria-label') === 'Next week') {
      mb[i].click();
      return 'clicked Next week';
    }
  }
  return 'not found';
})()
```

Verify navigation via the `h2.flex-grow` heading:

```javascript
(function() {
  var h2 = document.querySelector('h2.flex-grow');
  return h2 ? h2.textContent?.trim() : 'unknown';
})()
```

**Note:** Month view shows approximately 3 weeks spanning the current and next month (e.g., May 17 - June 6). When a date range spans two months, the dates from each month are rendered separately — check both the first and second week of dates carefully.

### Step 6: Check Date Availability (CRITICAL PATTERN)

```javascript
(function() {
  var results = {};
  document.querySelectorAll('market-button[data-testid^="date-"]').forEach(function(btn) {
    var testId = btn.getAttribute('data-testid');
    var day = parseInt(testId.replace('date-', ''));
    if (!isNaN(day)) {
      results[day] = {
        available: !btn.hasAttribute('disabled'),
        selected: testId.includes('-selected'),
        text: btn.textContent?.trim() || ''
      };
    }
  });
  return results;
})()
```

In month view spanning two months, dates may have the same day number from two different months (e.g., May 24 and June 24). The calendar renders them all with `data-testid="date-N"` where N is the day number, making them **ambiguous**. To disambiguate:
- Dates in the first month show with older/past dates disabled
- Dates in the second month show with future availability
- Use the surrounding dates (month header) to determine which month a given date belongs to

### Step 7: Extract Times for Available Date

```javascript
// Click date
document.querySelector('market-button[data-testid="date-19"]')?.click();

// After 5s wait, extract times
(function() {
  var times = [];
  document.querySelectorAll('market-button').forEach(function(btn) {
    var text = btn.textContent?.trim() || '';
    if (/^\d{1,2}:\d{2}\s*[AP]M$/i.test(text)) {
      times.push({time: text, disabled: btn.hasAttribute('disabled')});
    }
  });
  return times;
})()
```

---

## What Does NOT Work (Learned Painfully)

### ❌ Playwright `isEnabled()` / `isDisabled()` on custom elements
```javascript
// Returns WRONG results for market-button
const btn = await page.locator('[data-testid="date-29"]');
await btn.isEnabled();   // Returns true (WRONG!)
await btn.isDisabled();  // Returns false (WRONG!)

// The button has disabled="" attribute but Playwright doesn't detect it
// on custom elements (web components/shadow DOM)
```

### ❌ Direct API calls
- Square's internal APIs require OAuth authentication
- Consumer bookings can't use the GraphQL endpoints
- Returns "An error has occurred" without proper auth tokens

### ❌ `networkidle` wait condition
```javascript
// ❌ Times out - SPA never reaches networkidle
await page.goto(url, { waitUntil: 'networkidle' });

// ✅ Use domcontentloaded + manual waits
await page.goto(url, { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(4000);
```

### ❌ Standard button selectors
- Square uses `market-button` custom elements
- Standard `page.click('button')` won't work
- **DO:** Use `aria-label` or `data-testid` selectors

### ❌ Assuming availability is consistent
- April 29 showed DISABLED in automation but AVAILABLE in manual browser
- Same service ID, same timezone, not logged in
- **DO:** Always verify with manual check; discrepancy cause unknown

### ❌ Relying on coordinates
- Coordinate-based clicking is fragile
- Different screen sizes break positions
- **DO:** Use semantic selectors as primary, coordinates as fallback only

### ❌ Clicking service items without shadow DOM traversal
- Square service list items use `market-row` custom elements with shadow DOM
- Standard `el.click()` on the `<a>` tag inside shadow DOM often does nothing
- **DO:** Use `el.shadowRoot?.querySelector('a')?.click()` or click the `market-row` host element
- **DO:** After clicking a service, verify the URL changed to `/services/{ID}` before proceeding

### ❌ Assuming "Next month" button works on first click
- The "Next month" button sometimes requires **two clicks** to actually advance the month
- After first click, the calendar grid may update to show dates from the next month but the header still shows the old month
- **DO:** Click "Next month", then verify the `<h2>` heading changed before proceeding
- **DO:** Use `document.querySelector('h2').textContent` to verify the current month, not the grid dates

---

## Platform Quirks

1. **Custom Elements Everywhere** - `market-*` tags replace standard HTML
2. **Shadow DOM** - Some elements inaccessible to standard selectors; use `el.shadowRoot?.querySelector()` to traverse
3. **URL Structure** - `/availability` only appears after flow completion
4. **OAuth Required for API** - No public consumer API, must use browser automation
5. **Availability Discrepancies** - Automation vs manual browser can show different results
6. **Month Navigation** - "Next month" button may require two clicks; always verify via `<h2>` heading text
7. **Date Availability Detection** - Dates that are NOT available appear as `StaticText` (not `<button>` elements) in the accessibility tree; available dates are `<button>` elements. This is the most reliable way to check availability.

---

## Detection Summary

| Check | Element Type | Method |
|-------|--------------|--------|
| Date available? | `market-button` | `hasAttribute('disabled')` in page.evaluate() |
| Time available? | `market-button` | `hasAttribute('disabled')` in page.evaluate() |
| Staff selected? | `market-radio` | `aria-pressed="true"` |
| Page loaded? | URL | Contains `/availability` |

---

## Service ID Format

Square service IDs are 24-character alphanumeric:
```
XA4S2WKU7HYBHTWNKCPBIBDJ
```

Found in:
- URL after clicking service: `/services/{ID}`
- `service_id` query parameter
