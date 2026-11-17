# Mindbody

**Status:** ⚠️ Working (Browser automation required)
**Method:** Direct browser automation (SPA with API backend)
**Last Tested:** 2026-05-18
**Domains:** `*.mindbodyonline.com`, `*.mindbody.io`
**Example Site:** Various spa/salon clients

---

## Platform Overview

Mindbody is a large spa/salon/fitness booking platform. The consumer booking flow is a JavaScript SPA that loads service menus, staff, and availability from Mindbody's API. The platform uses bot detection (PerimeterX/HUMAN) on some deployments, but standard stealth browser automation works for most venues.

---

## Happy Path (What Works)

### 1. Initial Navigation

Mindbody booking pages follow a consistent URL pattern:

```
https://{business}.mindbodyonline.com/{service-type}
https://clients.mindbodyonline.com/ASP/main_shop.asp?studioid={id}
```

Or the newer embedded widget:
```
https://{business}.mindbody.io/
```

Navigate to the booking page and wait for the SPA to fully render:

```python
page.goto(url, wait_until='domcontentloaded', timeout=30000)
page.wait_for_timeout(5000)  # SPA needs time to hydrate
```

### 2. Service Selection

Services are typically listed in a sidebar or grid. Click the desired service category, then the specific service:

```python
# Click service category
page.locator('text=Massage').first.click()
page.wait_for_timeout(2000)

# Click specific service
page.locator('text=Swedish Massage 60 min').first.click()
page.wait_for_timeout(2000)
```

### 3. Staff Selection

After selecting a service, a staff selection screen appears. "Any Staff" is typically available:

```python
# Select "Any Staff" or first available staff
any_staff = page.locator('text=Any Staff, text=Any Employee, text=No Preference').first
if any_staff.is_visible():
    any_staff.click()
    page.wait_for_timeout(1500)

# Click Next/Continue
page.locator('button:has-text("Next"), button:has-text("Continue")').first.click()
page.wait_for_timeout(3000)
```

### 4. Date/Time Selection

The calendar shows available dates. Available dates are clickable buttons; unavailable dates are grayed out or absent:

```python
# Check if a specific date is available
def is_date_available(page, day_number):
    date_btn = page.locator(f'[data-testid*="date-{day_number}"], td:has-text("{day_number}") button, .calendar-day:has-text("{day_number}")').first
    if date_btn.is_visible():
        classes = date_btn.get_attribute('class') or ''
        return 'disabled' not in classes and 'unavailable' not in classes
    return False

# Extract available times for selected date
def get_available_times(page):
    times = page.evaluate('''() => {
        const results = [];
        document.querySelectorAll('button, [role="button"]').forEach(el => {
            const text = el.textContent.trim();
            if (/^\d{1,2}:\d{2}\s*(AM|PM)$/i.test(text)) {
                const disabled = el.hasAttribute('disabled') || el.getAttribute('aria-disabled') === 'true';
                results.push({time: text, available: !disabled});
            }
        });
        return results;
    }''')
    return [t for t in results if t['available']]
```

### 5. Full Availability Check Flow

```python
from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta

def check_mindbody_availability(url, service_name, weeks_ahead=4):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
        context = browser.new_context(
            viewport={'width': 1280, 'height': 800},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        )
        context.add_init_script(
            'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
        )
        page = context.new_page()
        page.goto(url, wait_until='domcontentloaded', timeout=30000)
        page.wait_for_timeout(5000)

        # Select service
        page.locator(f'text={service_name}').first.click()
        page.wait_for_timeout(2000)

        # Select staff
        any_staff = page.locator('text=Any Staff, text=Any Employee').first
        if any_staff.is_visible():
            any_staff.click()
            page.wait_for_timeout(1500)

        page.locator('button:has-text("Next"), button:has-text("Continue")').first.click()
        page.wait_for_timeout(3000)

        # Scan dates across weeks
        available_slots = []
        for week in range(weeks_ahead):
            # Check each day in current week view
            for day in range(1, 32):
                day_slots = page.evaluate('''() => {
                    const times = [];
                    document.querySelectorAll('button, [role="button"]').forEach(el => {
                        const text = el.textContent.trim();
                        if (/^\d{1,2}:\d{2}\s*(AM|PM)$/i.test(text)) {
                            const disabled = el.hasAttribute('disabled');
                            if (!disabled) times.push(text);
                        }
                    });
                    return times;
                }''')
                if day_slots:
                    available_slots.append({'week': week, 'day': day, 'times': day_slots})

            # Click next week
            next_btn = page.locator('button:has-text("Next"), [aria-label*="Next"]').first
            if next_btn.is_visible():
                next_btn.click()
                page.wait_for_timeout(3000)
            else:
                break

        browser.close()
        return available_slots
```

---

## What Does NOT Work

### ❌ Direct API calls without auth
- Mindbody's API requires OAuth or API keys for server-side calls
- Public booking pages don't expose unauthenticated availability endpoints
- **DO:** Use browser automation for public bookings

### ❌ Fast navigation
- Mindbody's SPA needs time to hydrate between steps
- Clicking too fast causes stale element references
- **DO:** Wait 2-3 seconds between major navigation steps

### ❌ Ignoring bot detection
- Some Mindbody deployments use PerimeterX bot detection
- Headless Chrome without stealth scripts may be blocked
- **DO:** Use stealth scripts and realistic user agent

---

## Platform Quirks

1. **SPA hydration delay** — The page loads HTML quickly but JavaScript needs 3-5 seconds to render the booking widget
2. **Multiple booking flows** — Mindbody has several booking UI versions (classic, widget, embedded); selectors may vary
3. **Class vs. Appointment** — Classes (yoga, fitness) have a different booking flow than appointments (massage, spa)
4. **Location selection** — Multi-location businesses require selecting a location first
5. **Session timeout** — Booking sessions expire after ~10 minutes of inactivity

---

## Detection Summary

| Check | Element Type | Method |
|-------|--------------|--------|
| Service available? | Button/Link | `text=` selector, check visibility |
| Date available? | Calendar cell | Check for clickable button (not grayed out) |
| Time available? | Button | Check `disabled` attribute |
| Staff selected? | Radio/Button | "Any Staff" or specific name visible |
| Page loaded? | Body | Wait for booking widget to render |

---

## Bot Detection & VPN Fallback

Mindbody uses PerimeterX (HUMAN Security) on some deployments. Signs of bot block:
- Page loads but booking widget never appears
- CAPTCHA challenge appears
- "Access denied" or "Please verify you are human" message

**VPN fallback:** If bot detection blocks access, route through ocas-vpn to get a non-US exit IP. See `ocas-vpn` skill for setup. Japan or EU exit nodes typically work.

```bash
# Check if VPN is needed
curl -s https://ipinfo.io/json  # If US, and site blocks, start VPN

# After VPN connection, verify
curl -s https://ipinfo.io/json  # Should show non-US
```