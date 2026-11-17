# SimplyBook.me

**Status:** ⚠️ Working (Browser automation required)
**Method:** Direct browser automation (React SPA)
**Last Tested:** Not yet tested — research-based documentation
**Domains:** `*.simplybook.me`, `simplybook.me`
**Example Site:** Various service businesses

---

## Platform Overview

SimplyBook.me is a versatile online booking system used by a wide range of service businesses — salons, spas, clinics, fitness studios, consultants, and more. Each business gets a customizable booking page. The platform uses a React-based SPA.

**Key insight:** SimplyBook.me is one of the most widely-used booking platforms globally, particularly popular in Europe and among small-to-medium service businesses. It supports more customization than most competitors.

---

## URL Patterns

```
# Business booking page
https://{business}.simplybook.me
https://simplybook.me/en/{business-id}/booking

# Custom domain (some businesses use their own domain)
https://booking.{business-domain}.com
```

---

## Happy Path (What Works)

### 1. Initial Navigation

```python
page.goto(simplybook_url, wait_until='domcontentloaded', timeout=30000)
page.wait_for_timeout(4000)
```

### 2. Service Selection

```python
# Services listed in a list or grid
page.locator('text=Massage').first.click()
page.wait_for_timeout(2000)

# Or find by service category
category = page.locator('[class*="category"]:has-text("Spa Services")').first
if category.is_visible():
    category.click()
    page.wait_for_timeout(1500)
    page.locator('text=Swedish Massage').first.click()
    page.wait_for_timeout(2000)
```

### 3. Provider Selection

```python
# Select provider (if multiple)
any_provider = page.locator('text=Any Provider, text=Any Staff, text=No Preference').first
if any_provider.is_visible():
    any_provider.click()
    page.wait_for_timeout(1500)

# Click Next/Continue
page.locator('button:has-text("Next"), button:has-text("Continue")').first.click()
page.wait_for_timeout(3000)
```

### 4. Date/Time Selection

```python
# Navigate calendar
def navigate_to_month(page, target_month_year):
    for _ in range(12):
        header = page.locator('[class*="calendar-header"], [class*="month"]').first
        header_text = header.text_content() or ''
        if target_month_year.lower() in header_text.lower():
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
- SimplyBook.me has an API but it requires authentication
- Public booking pages don't expose unauthenticated availability endpoints
- **DO:** Use browser automation for public bookings

### ❌ Assuming uniform layout
- SimplyBook.me is highly customizable; each business can customize their booking page
- Selectors may vary significantly between businesses
- **DO:** Use flexible selectors and handle missing elements gracefully

---

## Platform Quirks

1. **High customization** — Each business can customize colors, layout, and flow
2. **Multi-language** — SimplyBook.me supports many languages; page text may vary
3. **Custom domains** — Some businesses use custom domains for their booking pages
4. **Plugin system** — Businesses can add custom plugins that modify the booking flow
5. **Feature-rich** — Supports coupons, packages, memberships, and more

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

SimplyBook.me has minimal bot detection on most deployments.
If blocked, route through ocas-vpn as fallback.