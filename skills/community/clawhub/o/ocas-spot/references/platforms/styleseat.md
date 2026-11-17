# StyleSeat

**Status:** ⚠️ Working (Browser automation required)
**Method:** Direct browser automation (React SPA)
**Last Tested:** 2026-05-18
**Domains:** `*.styleseat.com`
**Example Site:** Various salon/spa professionals

---

## Platform Overview

StyleSeat is a booking platform for beauty and wellness professionals. Each professional has their own booking page. The platform uses a React SPA for the booking flow. StyleSeat does not offer a public API for availability checks.

---

## Happy Path (What Works)

### 1. Initial Navigation

StyleSeat booking pages follow this URL pattern:

```
https://www.styleseat.com/m/{professional-slug}
https://www.styleseat.com/book/{professional-id}
```

```python
page.goto(url, wait_until='domcontentloaded', timeout=30000)
page.wait_for_timeout(4000)
```

### 2. Service Selection

Services are listed on the professional's profile page. Click "Book" on the desired service:

```python
# Click Book button for a specific service
page.locator('text=Book').first.click()
page.wait_for_timeout(2000)

# Or find by service name
service_section = page.locator('[class*="service"]:has-text("Haircut")').first
if service_section.is_visible():
    service_section.locator('text=Book').first.click()
    page.wait_for_timeout(2000)
```

### 3. Date/Time Selection

After selecting a service, a calendar appears:

```python
# Navigate to target month
def navigate_month(page, target_month):
    for _ in range(12):
        header = page.locator('[class*="month"], [class*="calendar-header"]').first
        if target_month.lower() in (header.text_content() or '').lower():
            return True
        next_btn = page.locator('[class*="next"], button:has-text("›")').first
        if next_btn.is_visible():
            next_btn.click()
            page.wait_for_timeout(2000)
    return False

# Get available times
def get_available_times(page):
    return page.evaluate('''() => {
        const times = [];
        document.querySelectorAll('[class*="time"], button').forEach(el => {
            const text = el.textContent.trim();
            if (/^\d{1,2}:\d{2}\s*(AM|PM)$/i.test(text)) {
                const disabled = el.hasAttribute('disabled') || 
                    el.className.includes('disabled') ||
                    el.className.includes('unavailable');
                if (!disabled) times.push(text);
            }
        });
        return times;
    }''')
```

### 4. Full Flow

```python
from playwright.sync_api import sync_playwright

def check_styleseat_availability(url, service_name=None):
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

        # Select service if specified
        if service_name:
            service_btn = page.locator(f'[class*="service"]:has-text("{service_name}")').first
            if service_btn.is_visible():
                service_btn.locator('text=Book').first.click()
                page.wait_for_timeout(3000)

        # Get available times
        times = get_available_times(page)
        browser.close()
        return {'available': len(times) > 0, 'times': times}
```

---

## What Does NOT Work

### ❌ Direct API calls
- StyleSeat does not offer a public API
- Internal endpoints require session authentication
- **DO:** Use browser automation

### ❌ Booking without account
- StyleSeat requires creating an account to complete a booking
- Availability checks work without auth, but booking requires login
- **DO:** Prompt user to provide StyleSeat credentials for booking

### ❌ Assuming all professionals use the same layout
- StyleSeat allows customization of booking pages
- Some professionals may have different service structures
- **DO:** Handle missing elements gracefully

---

## Platform Quirks

1. **Account required for booking** — Can check availability without auth, but booking requires login
2. **Service-first flow** — Must select a service before seeing availability
3. **Professional-specific** — Each professional has their own page; no central directory
4. **Mobile-optimized** — StyleSeat is heavily mobile-optimized; desktop selectors may differ
5. **Review integration** — Reviews and ratings are shown on the booking page

---

## Detection Summary

| Check | Element Type | Method |
|-------|--------------|--------|
| Service available? | Card/Button | `text=Book` near service name |
| Date available? | Calendar cell | Clickable date |
| Time available? | Button | Check `disabled` class |
| Page loaded? | Body | Wait for booking widget |

---

## Bot Detection & VPN Fallback

StyleSeat uses standard bot detection. If blocked:
- Route through ocas-vpn for non-US exit IP
- Slow down interaction timing
- Use realistic user agent