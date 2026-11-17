# ResDiary

**Status:** ⚠️ Working (Browser automation required)
**Method:** Direct browser automation (React SPA)
**Last Tested:** Not yet tested — research-based documentation
**Domains:** `*.resdiary.com`, `resdiary.com`
**Example Site:** Restaurants (particularly UK, Europe, Asia)

---

## Platform Overview

ResDiary is a restaurant reservation platform popular in the UK, Europe, and Asia. It's a no-cover-charge reservation system used by many 5-star hotel chains and independent restaurants. The booking widget is a React-based SPA.

**Key insight:** ResDiary is the dominant reservation platform in the UK and has strong presence in Southeast Asia and Europe. It's particularly common in hotel restaurants.

---

## URL Patterns

```
# Restaurant booking page
https://www.resdiary.com/restaurant/{restaurant-slug}
https://bookings.resdiary.com/{restaurant-id}

# Embedded widget on restaurant website
https://{restaurant-website}.com (widget embedded)
```

---

## Happy Path (What Works)

### 1. Initial Navigation

```python
page.goto(resdiary_url, wait_until='domcontentloaded', timeout=30000)
page.wait_for_timeout(4000)
```

### 2. Party Size Selection

```python
# ResDiary typically starts with party size
party_btn = page.locator('button:has-text("2"), [class*="party-size"]').first
if party_btn.is_visible():
    party_btn.click()
    page.wait_for_timeout(1000)
```

### 3. Date/Time Selection

```python
# Navigate calendar
def navigate_to_date(page, target_date):
    for _ in range(12):
        header = page.locator('[class*="calendar-header"], [class*="month"]').first
        header_text = header.text_content() or ''
        if target_date.strftime('%B') in header_text:
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
        document.querySelectorAll('[class*="time-slot"], [class*="time-button"], button').forEach(el => {
            const text = el.textContent.trim();
            if (/^\d{1,2}:\d{2}$/.test(text) || /^\d{1,2}:\d{2}\s*(AM|PM)$/i.test(text)) {
                const disabled = el.hasAttribute('disabled') ||
                    el.getAttribute('aria-disabled') === 'true' ||
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
- ResDiary does not offer a public API for availability checks
- **DO:** Use browser automation

### ❌ Assuming US availability
- ResDiary is primarily UK/Europe/Asia; fewer US restaurants use it
- **DO:** Check if the restaurant is in a ResDiary-supported region

---

## Platform Quirks

1. **24-hour time format** — ResDiary often uses 24-hour format (14:00 instead of 2:00 PM)
2. **UK-centric** — Date format is DD/MM/YYYY; be careful with date parsing
3. **Hotel restaurant focus** — Many ResDiary restaurants are in hotels
4. **No cover charge** — ResDiary's selling point is no cover charge for reservations
5. **Widget embedding** — Many restaurants embed the ResDiary widget on their own website

---

## Detection Summary

| Check | Element Type | Method |
|-------|--------------|--------|
| Restaurant uses ResDiary? | Widget | Look for ResDiary branding or booking widget |
| Date available? | Calendar cell | Clickable date |
| Time available? | Button | Check `disabled` attribute |
| Party size selected? | Button/Dropdown | Party size visible |

---

## Bot Detection & VPN Fallback

ResDiary has minimal bot detection. VPN generally not needed.
If accessing from outside UK/Europe, some restaurants may be geo-restricted.