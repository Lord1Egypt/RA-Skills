# DaySmart Salon

**Status:** ⚠️ Working (Browser automation required)
**Method:** Direct browser automation (React SPA)
**Last Tested:** Not yet tested — research-based documentation
**Domains:** `*.daysmart.com`, `daysmart.com`
**Example Site:** Salons and spas

---

## Platform Overview

DaySmart Salon (formerly Rosy Salon Software) is a salon management and booking platform. It provides online booking for salons and spas. The platform uses a React-based SPA.

---

## URL Patterns

```
# Business booking page
https://{business}.daysmart.com
https://daysmart.com/book/{business-id}
```

---

## Happy Path (What Works)

### 1. Initial Navigation

```python
page.goto(daysmart_url, wait_until='domcontentloaded', timeout=30000)
page.wait_for_timeout(4000)
```

### 2. Service Selection

```python
page.locator('text=Haircut').first.click()
page.wait_for_timeout(2000)
```

### 3. Staff Selection

```python
any_staff = page.locator('text=Any Staff, text=Any Professional').first
if any_staff.is_visible():
    any_staff.click()
    page.wait_for_timeout(1500)
```

### 4. Date/Time Selection

```python
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

## Platform Quirks

1. **Salon-focused** — Designed specifically for salons; service categories reflect this
2. **Multi-location support** — Businesses with multiple locations require location selection first
3. **Minimal bot detection** — Generally accessible without VPN

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

DaySmart has minimal bot detection. VPN generally not needed.