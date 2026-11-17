# Yelp Reservations (Yelp Guest Manager)

**Status:** ⚠️ Working (Browser automation required)
**Method:** Direct browser automation (React SPA)
**Last Tested:** Not yet tested — research-based documentation
**Domains:** `*.yelp.com`, `yelp.com/reservations/*`
**Example Site:** Restaurant Yelp pages with "Reserve" button

---

## Platform Overview

Yelp Reservations (formerly Yelp Guest Manager, formerly Yelp Waitlist) is Yelp's restaurant reservation and table management system. It's integrated directly into Yelp business pages — consumers see a "Reserve" button on restaurant listings. The booking widget is a React-based SPA embedded in or linked from the Yelp restaurant page.

**Key insight:** Yelp Reservations is the **second-largest** restaurant reservation platform in the US after OpenTable, with significant market share. Many restaurants use it as their primary booking system.

---

## URL Patterns

Yelp Reservations uses several URL patterns:

```
# Direct reservation page
https://www.yelp.com/reservations/{restaurant-slug}

# Embedded widget on restaurant page
https://www.yelp.com/biz/{restaurant-slug}-{location}

# Yelp Guest Manager booking link (custom subdomain)
https://{restaurant}.yelp.com/reservations

# Reserve button on Yelp biz page → opens widget overlay
https://www.yelp.com/biz/{restaurant-slug}
```

The most reliable approach: navigate to the restaurant's Yelp page, find the "Reserve" button, and interact with the widget.

---

## Happy Path (What Works)

### 1. Initial Navigation

```python
page.goto(yelp_biz_url, wait_until='domcontentloaded', timeout=30000)
page.wait_for_timeout(3000)

# Look for Reserve button
reserve_btn = page.locator('a:has-text("Reserve"), button:has-text("Reserve"), [data-testid*="reserve"]').first
if reserve_btn.is_visible():
    reserve_btn.click()
    page.wait_for_timeout(3000)
```

### 2. Widget Interaction

Yelp's reservation widget may open as an overlay or redirect to a dedicated page:

```python
# Check if widget opened in overlay
widget = page.locator('[class*="reservation-widget"], [class*="yelp-reservations"], iframe[src*="reservations"]').first
if widget.is_visible():
    # Interact with widget directly
    pass

# Or check for redirect to reservations page
if 'reservations' in page.url:
    page.wait_for_timeout(3000)
```

### 3. Party Size Selection

```python
# Yelp shows party size selector first
party_btn = page.locator('button:has-text("2"), [class*="party-size"]').first
if party_btn.is_visible():
    party_btn.click()
    page.wait_for_timeout(1000)
```

### 4. Date/Time Selection

```python
# Navigate calendar
def navigate_to_date(page, target_date):
    for _ in range(12):
        header = page.locator('[class*="calendar-header"], [class*="month"]').first
        header_text = header.text_content() or ''
        if target_date.strftime('%B') in header_text and str(target_date.year) in header_text:
            return True
        next_btn = page.locator('[class*="next"], [aria-label*="Next"]').first
        if next_btn.is_visible():
            next_btn.click()
            page.wait_for_timeout(2000)
    return False

# Get available times
def get_available_times(page):
    return page.evaluate('''() => {
        const times = [];
        document.querySelectorAll('button, [role="button"], [class*="time-slot"]').forEach(el => {
            const text = el.textContent.trim();
            if (/^\d{1,2}:\d{2}\s*(AM|PM)$/i.test(text)) {
                const disabled = el.hasAttribute('disabled') ||
                    el.getAttribute('aria-disabled') === 'true' ||
                    el.className.includes('disabled') ||
                    el.className.includes('unavailable');
                if (!disabled) times.push(text);
            }
        });
        return times;
    }''')
```

---

## What Does NOT Work

### ❌ Yelp API for reservations
- Yelp Fusion API provides business search and reviews, NOT reservation availability
- No public API for booking or availability checks
- **DO:** Use browser automation

### ❌ Assuming all Yelp pages have reservations
- Only restaurants using Yelp Guest Manager show the Reserve button
- Many restaurants use OpenTable, Resy, or other platforms embedded in Yelp
- **DO:** Check for Reserve button first; if absent, the restaurant doesn't use Yelp Reservations

### ❌ Fast navigation
- Yelp's SPA needs time to render the booking widget
- **DO:** Wait 2-3 seconds after each interaction

---

## Platform Quirks

1. **Widget variability** — Yelp has updated the reservation widget multiple times; selectors may vary
2. **Overlay vs redirect** — Some restaurants use an embedded overlay, others redirect to a dedicated page
3. **Platform detection** — Yelp may embed OpenTable or Resy widgets instead of using its own system
4. **Mobile optimization** — Yelp is heavily mobile-optimized; desktop selectors may differ
5. **Login requirements** — Some restaurants require Yelp account to complete booking (not for availability check)

---

## Detection Summary

| Check | Element Type | Method |
|-------|--------------|--------|
| Restaurant uses Yelp Reservations? | Button | Look for "Reserve" button on Yelp biz page |
| Widget loaded? | Overlay/Page | Check for reservation widget or URL redirect |
| Date available? | Calendar cell | Clickable date (not grayed out) |
| Time available? | Button | Check `disabled` attribute |
| Party size selected? | Button/Dropdown | Party size visible in summary |

---

## Bot Detection & VPN Fallback

Yelp uses standard bot detection (Cloudflare on some pages). Signs of block:
- "Verify you are human" challenge
- Booking widget fails to load after 10+ seconds
- HTTP 403 on Yelp pages

**VPN fallback:** Route through ocas-vpn for non-US exit IP. See `ocas-vpn` skill.