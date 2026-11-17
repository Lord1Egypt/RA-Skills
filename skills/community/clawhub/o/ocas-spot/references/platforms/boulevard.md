# Boulevard

**Status:** ⚠️ Working (Browser automation required)
**Method:** Direct browser automation (React SPA)
**Last Tested:** Not yet tested — research-based documentation
**Domains:** `*.blvdup.com`, `blvdup.com`, `book.boulevard.io`
**Example Site:** Upscale salons and spas

---

## Platform Overview

Boulevard is a premium salon and spa booking platform focused on upscale businesses. It provides a polished, brand-forward booking experience. The platform uses a React-based SPA with sophisticated UI.

**Key insight:** Boulevard targets the premium segment — high-end salons, med spas, and wellness centers. It's known for beautiful booking interfaces and strong brand customization.

---

## URL Patterns

```
# Business booking page
https://{business}.blvdup.com
https://book.boulevard.io/{business-slug}

# Custom domain (premium feature)
https://book.{business-domain}.com
```

---

## Happy Path (What Works)

### 1. Initial Navigation

```python
page.goto(blvd_url, wait_until='domcontentloaded', timeout=30000)
page.wait_for_timeout(4000)
```

### 2. Service Selection

```python
# Services displayed as elegant cards
page.locator('text=Haircut & Style').first.click()
page.wait_for_timeout(2000)

# Or browse by category
category = page.locator('[class*="category"]:has-text("Hair")').first
if category.is_visible():
    category.click()
    page.wait_for_timeout(1500)
```

### 3. Staff Selection

```python
# Boulevard emphasizes staff profiles with photos
any_staff = page.locator('text=Any Stylist, text=Any Professional, text=No Preference').first
if any_staff.is_visible():
    any_staff.click()
    page.wait_for_timeout(1500)

# Or select specific staff
page.locator('[class*="staff"]:has-text("Jane")').first.click()
page.wait_for_timeout(1500)
```

### 4. Date/Time Selection

```python
# Boulevard has a polished calendar UI
def get_available_times(page):
    return page.evaluate('''() => {
        const times = [];
        document.querySelectorAll('[class*="time-slot"], [class*="time-button"], button').forEach(el => {
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

### ❌ Direct API calls
- Boulevard does not offer a public API for availability checks
- **DO:** Use browser automation

### ❌ Booking without account
- Boulevard requires creating an account to complete booking
- Availability checks work without auth

---

## Platform Quirks

1. **Premium UI** — Boulevard's booking interface is highly polished; selectors may use custom CSS classes
2. **Staff-centric** — Emphasizes staff profiles and specialties
3. **Service add-ons** — Services may have add-ons (e.g., "Add deep conditioning")
4. **Membership integration** — Some businesses have membership programs that affect availability
5. **Strong brand customization** — Each business can heavily customize the look and feel

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

Boulevard uses Cloudflare on some deployments. If blocked:
- Route through ocas-vpn for non-US exit IP
- Use realistic user agent and interaction timing