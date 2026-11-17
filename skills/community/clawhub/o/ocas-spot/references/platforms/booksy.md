# Booksy

**Status:** ⚠️ Working (Browser automation required)
**Method:** Direct browser automation (React SPA)
**Last Tested:** Not yet tested — research-based documentation
**Domains:** `*.booksy.com`, `booksy.com`
**Example Site:** Various salon/spa/wellness professionals

---

## Platform Overview

Booksy is a popular booking platform for beauty, wellness, and health professionals. It has a strong consumer-facing app and web presence. Each professional has their own Booksy booking page. The platform uses a React-based SPA for the booking flow.

**Key insight:** Booksy is one of the top 3 salon/spa booking platforms (alongside Fresha and Vagaro), with particularly strong adoption among independent professionals and small salons.

---

## URL Patterns

```
# Professional booking page
https://booksy.com/en-us/{professional-id}/{professional-slug}
https://booksy.com/en-us/{service-type}/{location}/{professional-slug}

# Business page (B2B)
https://biz.booksy.com
```

---

## Happy Path (What Works)

### 1. Initial Navigation

```python
page.goto(booksy_url, wait_until='domcontentloaded', timeout=30000)
page.wait_for_timeout(4000)  # React SPA needs hydration time
```

### 2. Service Selection

Services are displayed as cards with name, duration, and price:

```python
# Click a specific service
page.locator('text=Haircut').first.click()
page.wait_for_timeout(2000)

# Or find by service card
service_card = page.locator('[class*="service"]:has-text("Massage")').first
if service_card.is_visible():
    service_card.click()
    page.wait_for_timeout(2000)
```

### 3. Staff/Provider Selection

```python
# Select "Any Staff" or specific provider
any_staff = page.locator('text=Any Staff, text=Any Professional, text=No Preference').first
if any_staff.is_visible():
    any_staff.click()
    page.wait_for_timeout(1500)

# Click Continue/Next
page.locator('button:has-text("Continue"), button:has-text("Next"), button:has-text("Book")').first.click()
page.wait_for_timeout(3000)
```

### 4. Date/Time Selection

```python
# Navigate calendar
def navigate_to_month(page, target_month_year):
    for _ in range(12):
        header = page.locator('[class*="calendar-header"], [class*="month-header"]').first
        header_text = header.text_content() or ''
        if target_month_year.lower() in header_text.lower():
            return True
        next_btn = page.locator('[class*="next-month"], [aria-label*="Next month"]').first
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

---

## What Does NOT Work

### ❌ Direct API calls
- Booksy does not offer a public API for availability checks
- Internal endpoints require session authentication
- **DO:** Use browser automation

### ❌ Booking without consumer account
- Booksy requires creating an account to complete a booking
- Availability checks work without auth
- **DO:** Prompt user to provide Booksy credentials for booking

---

## Platform Quirks

1. **Consumer-first design** — Booksy is designed for consumer mobile app; web booking is secondary
2. **Service categories** — Services organized by category; may need to expand category first
3. **Location-based** — Booksy often starts with location selection
4. **Review integration** — Reviews and ratings shown on booking page
5. **Multi-step flow** — Service → Provider → Date → Time → Confirm

---

## Detection Summary

| Check | Element Type | Method |
|-------|--------------|--------|
| Service available? | Card/Button | `text=` selector |
| Date available? | Calendar cell | Check if clickable |
| Time available? | Button | Check `disabled` attribute |
| Page loaded? | Body | Wait for booking widget |

---

## Bot Detection & VPN Fallback

Booksy uses Cloudflare on some deployments. If blocked:
- Route through ocas-vpn for non-US exit IP
- Slow down interaction timing
- Use realistic user agent