# Fresha

**Status:** ⚠️ Working (Browser automation required)
**Method:** Direct browser automation (React SPA)
**Last Tested:** 2026-05-18
**Domains:** `*.fresha.com`, `*.fresha.io`
**Example Site:** Various salon/spa clients

---

## Platform Overview

Fresha (formerly Shedul) is a popular free booking platform for salons, spas, and wellness businesses. The consumer booking flow is a React-based SPA. Fresha does not offer a public API for availability checks — browser automation is the only approach.

---

## Happy Path (What Works)

### 1. Initial Navigation

Fresha booking pages follow this URL pattern:

```
https://{business}.fresha.com/booking
https://{business}.fresha.com/services
```

Or the generic booking page:
```
https://www.fresha.com/book-now/{business-slug}
```

```python
page.goto(url, wait_until='domcontentloaded', timeout=30000)
page.wait_for_timeout(4000)  # React SPA needs hydration time
```

### 2. Service Selection

Services are displayed as cards or a list. Each service shows name, duration, and price:

```python
# Click a specific service
page.locator('text=Haircut & Style').first.click()
page.wait_for_timeout(2000)

# Or select by service card
service_card = page.locator('[class*="service-card"]:has-text("Massage")').first
if service_card.is_visible():
    service_card.click()
    page.wait_for_timeout(2000)
```

### 3. Staff/Provider Selection

After selecting a service, a staff selection screen appears:

```python
# Select "Any Staff" or specific staff member
any_staff = page.locator('text=Any Staff, text=Any Professional, text=No Preference').first
if any_staff.is_visible():
    any_staff.click()
    page.wait_for_timeout(1500)

# Or select specific staff
page.locator('text=Jane Smith').first.click()
page.wait_for_timeout(1500)

# Click Continue/Next
page.locator('button:has-text("Continue"), button:has-text("Next"), button:has-text("Book")').first.click()
page.wait_for_timeout(3000)
```

### 4. Date/Time Selection

Fresha shows a calendar with available dates. Available dates are highlighted; unavailable dates are grayed out:

```python
# Navigate to target month
def navigate_to_month(page, target_month_year):
    """Navigate calendar to target month. target_month_year like 'May 2026'"""
    for _ in range(12):  # Max 12 months forward
        header = page.locator('[class*="calendar-header"], [class*="month-header"]').first
        header_text = header.text_content() or ''
        if target_month_year.lower() in header_text.lower():
            return True
        next_btn = page.locator('[class*="next-month"], [aria-label*="Next month"], button:has-text("›")').first
        if next_btn.is_visible():
            next_btn.click()
            page.wait_for_timeout(2000)
    return False

# Extract available times
def get_available_times(page):
    return page.evaluate('''() => {
        const times = [];
        document.querySelectorAll('[class*="time-slot"], [class*="time-button"], button').forEach(el => {
            const text = el.textContent.trim();
            if (/^\d{1,2}:\d{2}\s*(AM|PM)$/i.test(text)) {
                const disabled = el.hasAttribute('disabled') || 
                    el.getAttribute('aria-disabled') === 'true' ||
                    el.className.includes('disabled');
                if (!disabled) times.push(text);
            }
        });
        return times;
    }''')
```

### 5. Full Availability Check

```python
from playwright.sync_api import sync_playwright

def check_fresha_availability(url, service_name, target_date=None):
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
        page.wait_for_timeout(4000)

        # Select service
        page.locator(f'text={service_name}').first.click()
        page.wait_for_timeout(2000)

        # Select staff
        any_staff = page.locator('text=Any Staff, text=Any Professional').first
        if any_staff.is_visible():
            any_staff.click()
            page.wait_for_timeout(1500)

        page.locator('button:has-text("Continue"), button:has-text("Next")').first.click()
        page.wait_for_timeout(3000)

        # Navigate to target date if specified
        if target_date:
            navigate_to_month(page, target_date.strftime('%B %Y'))
            page.locator(f'text={target_date.day}').first.click()
            page.wait_for_timeout(2000)

        times = get_available_times(page)
        browser.close()
        return {'available': len(times) > 0, 'times': times}
```

---

## What Does NOT Work

### ❌ Direct API calls
- Fresha does not offer a public API for availability checks
- Internal API endpoints require session cookies from the browser
- **DO:** Use browser automation

### ❌ Skipping service selection
- The booking flow requires selecting a service before showing availability
- **DO:** Always select a service first, even if checking general availability

### ❌ Fast clicking
- React SPA needs time to re-render between steps
- **DO:** Wait 2-3 seconds after each click

---

## Platform Quirks

1. **React SPA** — Standard DOM selectors may not work during hydration; wait for elements
2. **Service categories** — Some businesses organize services into categories; may need to expand category first
3. **Multi-step flow** — Service → Staff → Date → Time → Confirm; each step must complete
4. **Calendar pagination** — Calendar shows one month at a time; use next/prev to navigate
5. **Time slot density** — Popular businesses may show 20+ time slots; scroll to see all

---

## Detection Summary

| Check | Element Type | Method |
|-------|--------------|--------|
| Service available? | Card/Button | `text=` selector |
| Date available? | Calendar cell | Check if clickable (not grayed out) |
| Time available? | Button | Check `disabled` class/attribute |
| Staff selected? | Radio/Text | Staff name visible in summary |
| Page loaded? | Body | Wait for booking widget |

---

## Bot Detection & VPN Fallback

Fresha uses Cloudflare on some deployments. Signs of bot block:
- "Checking your browser before accessing" page
- CAPTCHA challenge
- Booking widget fails to load after 10+ seconds

**VPN fallback:** Route through ocas-vpn for non-US exit IP. See `ocas-vpn` skill.