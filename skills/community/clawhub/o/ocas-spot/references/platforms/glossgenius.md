# GlossGenius

**Status:** ⚠️ Working (Browser automation required)
**Method:** Direct browser automation (React SPA)
**Last Tested:** Not yet tested — research-based documentation
**Domains:** `*.glossgenius.com`, `glossgenius.com/booking/*`
**Example Site:** Various independent beauty professionals

---

## Platform Overview

GlossGenius is a booking and business management platform designed for independent beauty professionals (hair stylists, nail artists, lash technicians, etc.). It provides a branded booking page for each professional. The platform uses a React-based SPA.

**Key insight:** GlossGenius is particularly popular among independent professionals who don't have a physical salon location — mobile stylists, home-based professionals, and suite renters.

---

## URL Patterns

```
# Professional booking page
https://{professional}.glossgenius.com
https://glossgenius.com/booking/{professional-slug}

# Branded booking link
https://book.glossgenius.com/{professional-id}
```

---

## Happy Path (What Works)

### 1. Initial Navigation

```python
page.goto(glossgenius_url, wait_until='domcontentloaded', timeout=30000)
page.wait_for_timeout(4000)
```

### 2. Service Selection

```python
# Services listed as cards or list items
page.locator('text=Haircut & Style').first.click()
page.wait_for_timeout(2000)

# Or find service card
service_card = page.locator('[class*="service-card"]:has-text("Color")').first
if service_card.is_visible():
    service_card.click()
    page.wait_for_timeout(2000)
```

### 3. Date/Time Selection

```python
# GlossGenius shows available dates in a calendar
def get_available_dates(page):
    return page.evaluate('''() => {
        const dates = [];
        document.querySelectorAll('[class*="calendar-day"], [class*="date-button"], td button').forEach(el => {
            const text = el.textContent.trim();
            const day = parseInt(text);
            if (day >= 1 && day <= 31) {
                const disabled = el.hasAttribute('disabled') ||
                    el.className.includes('disabled') ||
                    el.className.includes('unavailable');
                if (!disabled) dates.push(day);
            }
        });
        return [...new Set(dates)];
    }''')

# Get available times for selected date
def get_available_times(page):
    return page.evaluate('''() => {
        const times = [];
        document.querySelectorAll('[class*="time"], button').forEach(el => {
            const text = el.textContent.trim();
            if (/^\d{1,2}:\d{2}\s*(AM|PM)$/i.test(text)) {
                const disabled = el.hasAttribute('disabled') ||
                    el.className.includes('disabled');
                if (!disabled) times.push(text);
            }
        });
        return times;
    }''')
```

---

## What Does NOT Work

### ❌ Direct API calls
- No public API for availability checks
- **DO:** Use browser automation

### ❌ Booking without account
- GlossGenius requires creating an account to complete booking
- Availability checks work without auth

---

## Platform Quirks

1. **Branded pages** — Each professional has a unique URL; no central directory
2. **Service-first flow** — Must select service before seeing availability
3. **Independent professionals** — Many are mobile/home-based; location may vary
4. **Integrated payments** — GlossGenius handles payments; booking flow includes payment step
5. **Minimal bot detection** — Generally accessible without VPN

---

## Detection Summary

| Check | Element Type | Method |
|-------|--------------|--------|
| Service available? | Card/Button | `text=` selector |
| Date available? | Calendar cell | Clickable date |
| Time available? | Button | Check `disabled` attribute |
| Page loaded? | Body | Wait for booking widget |

---

## Bot Detection & VPN Fallback

GlossGenius has minimal bot detection. VPN generally not needed.
If blocked, route through ocas-vpn as fallback.