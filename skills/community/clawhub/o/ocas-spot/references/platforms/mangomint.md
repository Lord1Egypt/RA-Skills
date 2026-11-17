# Mangomint

**Status:** ⚠️ Working (Browser automation required)
**Method:** Direct browser automation (React SPA)
**Last Tested:** Not yet tested — research-based documentation
**Domains:** `*.mangomint.com`, `mangomint.com`
**Example Site:** Salons and spas

---

## Platform Overview

Mangomint is a salon and spa booking platform with a focus on modern, Instagram-friendly booking experiences. It's popular among trendy salons and beauty businesses. The platform uses a React-based SPA.

---

## URL Patterns

```
# Business booking page
https://{business}.mangomint.com
https://mangomint.com/book/{business-slug}
```

---

## Happy Path (What Works)

### 1. Initial Navigation

```python
page.goto(mangomint_url, wait_until='domcontentloaded', timeout=30000)
page.wait_for_timeout(4000)
```

### 2. Service Selection

```python
# Services displayed as visual cards (Instagram-style)
page.locator('text=Haircut').first.click()
page.wait_for_timeout(2000)
```

### 3. Staff Selection

```python
any_staff = page.locator('text=Any Stylist, text=Any Professional').first
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

1. **Visual-first design** — Mangomint emphasizes visual service cards with photos
2. **Social media integration** — Strong Instagram/social media integration
3. **Modern UI** — Clean, minimal interface; may use custom CSS frameworks
4. **Minimal bot detection** — Generally accessible without VPN

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

Mangomint has minimal bot detection. VPN generally not needed.