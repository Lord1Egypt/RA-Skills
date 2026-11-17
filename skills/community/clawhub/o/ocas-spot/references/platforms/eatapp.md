# Eat App

**Status:** ⚠️ Working (Browser automation required)
**Method:** Direct browser automation (React SPA)
**Last Tested:** Not yet tested — research-based documentation
**Domains:** `*.eatapp.co`, `eatapp.co`
**Example Site:** Restaurants (particularly Middle East, Europe, US)

---

## Platform Overview

Eat App is a restaurant reservation and table management platform with strong presence in the Middle East, Europe, and growing US market. It provides both a consumer booking interface and a restaurant management system. The booking widget is a React-based SPA.

**Key insight:** Eat App is particularly dominant in the Middle East (Dubai, Riyadh, etc.) and is expanding rapidly in the US. It's known for being a strong OpenTable alternative.

---

## URL Patterns

```
# Restaurant booking page
https://restaurant.eatapp.co/{restaurant-slug}
https://eatapp.co/book/{restaurant-id}

# Embedded widget on restaurant website
https://{restaurant-website}.com (widget embedded)
```

---

## Happy Path (What Works)

### 1. Initial Navigation

```python
page.goto(eatapp_url, wait_until='domcontentloaded', timeout=30000)
page.wait_for_timeout(4000)
```

### 2. Party Size Selection

```python
party_btn = page.locator('button:has-text("2"), [class*="party-size"], [class*="guests"]').first
if party_btn.is_visible():
    party_btn.click()
    page.wait_for_timeout(1000)
```

### 3. Date/Time Selection

```python
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

def get_available_times(page):
    return page.evaluate('''() => {
        const times = [];
        document.querySelectorAll('[class*="time-slot"], [class*="time-button"], button').forEach(el => {
            const text = el.textContent.trim();
            if (/^\d{1,2}:\d{2}\s*(AM|PM)$/i.test(text) || /^\d{1,2}:\d{2}$/.test(text)) {
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
- Eat App does not offer a public API for availability checks
- **DO:** Use browser automation

---

## Platform Quirks

1. **Middle East focus** — Many Eat App restaurants are in UAE, Saudi Arabia, etc.
2. **24-hour time format** — May use 24-hour format in some regions
3. **Widget embedding** — Many restaurants embed the Eat App widget on their own website
4. **Multi-language** — Supports Arabic, English, and other languages
5. **Minimal bot detection** — Generally accessible without VPN

---

## Detection Summary

| Check | Element Type | Method |
|-------|--------------|--------|
| Restaurant uses Eat App? | Widget | Look for Eat App branding |
| Date available? | Calendar cell | Clickable date |
| Time available? | Button | Check `disabled` attribute |
| Party size selected? | Button/Dropdown | Party size visible |

---

## Bot Detection & VPN Fallback

Eat App has minimal bot detection. VPN generally not needed.
If accessing Middle East restaurants from US, some may be geo-restricted.