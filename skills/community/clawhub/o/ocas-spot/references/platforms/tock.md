# Tock

**Status:** ✅ Working
**Last tested:** 2026-03-31
**Method:** URL-based date iteration

---

## Overview

Tock uses Cloudflare Turnstile bot detection that **triggers on calendar interactions**, but page loads work fine with stealth scripts. The key insight: **rewrite URLs instead of clicking the calendar**.

---

## Implementation Status

**File:** `scripts/joujou_working_tock.py`

**Working:**
- ✅ Navigate to experience page with stealth scripts
- ✅ Close blocking modal
- ✅ Extract time slots from DOM
- ✅ Iterate dates via URL parameters
- ✅ Detect availability by checking for times in page content

---

## Working Architecture

```
1. Load experience URL with date parameter
   URL: /experience/{id}?cameFrom=search_modal&date=YYYY-MM-DD&size=2
   ↓
2. Close modal dialog
   ↓
3. Extract times from DOM
   Look for container with "4:00 PM" through "10:00 PM"
   ↓
4. If times found → availability exists
   If no times → no availability for that date
```

**Critical discovery:** Don't click the calendar. JavaScript clicks trigger Cloudflare bot detection. URL-based iteration works because it's just page loads.

---

## Working Implementation

```python
from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
    context = browser.new_context(
        viewport={'width': 1280, 'height': 800},
        user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    )
    context.add_init_script('Object.defineProperty(navigator, "webdriver", {get: () => undefined})')
    
    page = context.new_page()
    
    # URL pattern that works
    base = 'https://www.exploretock.com/joujousf/experience/583810/joujou-dinner-reservation'
    url = f'{base}?cameFrom=search_modal&date=2026-04-04&showExclusives=true&size=2'
    
    page.goto(url, wait_until='domcontentloaded', timeout=30000)
    page.wait_for_timeout(4000)
    
    # Close modal
    try:
        close_btn = page.locator('button[aria-label*="Close"]').first
        if close_btn.is_visible():
            close_btn.click()
            page.wait_for_timeout(1500)
    except:
        pass
    
    # Extract times
    result = page.evaluate('''() => {
        const allElements = [...document.querySelectorAll('*')];
        const container = allElements.find(el => {
            const text = el.textContent || '';
            return text.includes('4:00 PM') && text.includes('10:00 PM');
        });
        
        let times = [];
        if (container) {
            const text = container.textContent;
            times = text.match(/\\d{1,2}:\\d{2}\\s*(AM|PM)/g) || [];
        }
        
        return { times, hasAvailability: times.length > 0 };
    }''')
    
    # result['times'] = ['4:00 PM', '4:15 PM', '4:30 PM', ...]
```

---

## Key Findings

### 1. Cloudflare Behavior
- ✅ **Page loads** with stealth scripts work fine
- ❌ **JavaScript clicks** trigger bot verification
- ✅ **URL-based navigation** avoids detection

### 2. Time Extraction
Times appear as text in a container element containing multiple time strings like "4:00 PM4:15 PM4:30 PM...". Use regex to split them.

### 3. Modal Handling
The experience modal must be closed, but this doesn't trigger Cloudflare if done via Playwright locator (not JavaScript).

### 4. Date Iteration
Instead of clicking calendar dates, iterate by loading new URLs:
```python
current = datetime(2026, 4, 4)  # Start Saturday
for i in range(8):  # Check 8 Saturdays
    date_str = current.strftime('%Y-%m-%d')
    url = f'{base}?cameFrom=search_modal&date={date_str}&size=2'
    # Load page, extract times, iterate
    current += timedelta(days=7)
```

---

## Tested Results

**JouJou SF:**
- First available Saturday: **April 4, 2026**
- Times: 26 slots (4:00 PM - 10:00 PM)

---

## Previous Failed Approaches

| Approach | Result |
|----------|--------|
| Clicking calendar dates | ❌ Cloudflare verification |
| JavaScript-based clicking | ❌ Bot detection |
| Network API capture | ❌ No public API found |
| Headed browser | ❌ Same Cloudflare issues |
| Calendar widget interaction | ❌ Blocked |

---

## DOM Structure

**Time Container (after modal close):**
```html
<div>
  4:00 PM4:15 PM4:30 PM4:45 PM5:00 PM...
  <!-- Times concatenated as text -->
</div>
```

**Date Button:**
```html
<button data-testid="reservation-date-button" aria-label="Desired reservation date, current selection is 3/31/2026">
  DateMar 31, 2026
</button>
```

---

## Related

- See `square.md` for modal handling patterns
- See `sevenrooms.md` for date iteration approaches
- GitHub: `azoff/tockstalk` (Cypress-based, uses headed mode)