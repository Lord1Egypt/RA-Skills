# Calendly

**Status:** ✅ Working (API + Browser automation)
**Method:** REST API (preferred) or browser automation (fallback)
**Last Tested:** 2026-05-18
**Domains:** `calendly.com`, `*.calendly.com`

---

## Platform Overview

Calendly is a scheduling platform primarily used for meetings and consultations (not traditional spa/restaurant bookings). It has a well-documented REST API that makes availability checks straightforward without browser automation. Calendly is relevant for booking professional services, consultations, and meetings.

---

## Method 1: REST API (Preferred)

### Authentication

Calendly API uses personal access tokens or OAuth. For personal use:

1. Go to https://calendly.com/integrations/api_keys
2. Generate a personal access token
3. Store in environment: `CALENDLY_API_TOKEN=your_token_here`

### API Endpoints

**Get current user:**
```
GET https://api.calendly.com/v2/users/me
Authorization: Bearer {token}
```

**Get event types for a user:**
```
GET https://api.calendly.com/v2/event_types?user={user_uri}
Authorization: Bearer {token}
```

**Get available times for an event type:**
```
GET https://api.calendly.com/v2/event_type_available_times?event_type={event_type_uri}&start_time={ISO8601}&end_time={ISO8601}
Authorization: Bearer {token}
```

### Implementation

```python
import requests
from datetime import datetime, timedelta

class CalendlyChecker:
    BASE = 'https://api.calendly.com/v2'
    
    def __init__(self, api_token):
        self.headers = {'Authorization': f'Bearer {api_token}'}
    
    def get_user(self):
        r = requests.get(f'{self.BASE}/users/me', headers=self.headers)
        r.raise_for_status()
        return r.json()['resource']
    
    def get_event_types(self, user_uri):
        r = requests.get(
            f'{self.BASE}/event_types',
            params={'user': user_uri, 'active': 'true'},
            headers=self.headers
        )
        r.raise_for_status()
        return r.json()['collection']
    
    def get_available_times(self, event_type_uri, start_date, end_date):
        """Get available time slots for an event type in a date range."""
        r = requests.get(
            f'{self.BASE}/event_type_available_times',
            params={
                'event_type': event_type_uri,
                'start_time': start_date.isoformat() + 'Z',
                'end_time': end_date.isoformat() + 'Z',
            },
            headers=self.headers
        )
        r.raise_for_status()
        slots = r.json()['collection']
        return [{
            'start': s['start_time'],
            'end': s['end_time'],
            'status': s.get('status', 'available')
        } for s in slots]
    
    def check_availability(self, calendly_url, days_ahead=30):
        """Full flow: given a Calendly URL, return available slots."""
        user = self.get_user()
        event_types = self.get_event_types(user['uri'])
        
        # Find matching event type by URL
        matching = [et for et in event_types 
                    if calendly_url in et.get('scheduling_url', '')]
        
        if not matching:
            # If URL doesn't match, return all event types
            return {'event_types': [{'name': et['name'], 'url': et['scheduling_url']} for et in event_types]}
        
        et = matching[0]
        start = datetime.utcnow()
        end = start + timedelta(days=days_ahead)
        slots = self.get_available_times(et['uri'], start, end)
        
        return {
            'event_type': et['name'],
            'duration': et.get('duration'),
            'url': et['scheduling_url'],
            'available_slots': slots,
            'total_available': len(slots)
        }
```

---

## Method 2: Browser Automation (Fallback)

For cases where API token is not available, use browser automation:

```python
from playwright.sync_api import sync_playwright

def check_calendly_browser(calendly_url, days_ahead=14):
    """Check Calendly availability via browser automation."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
        context = browser.new_context(
            viewport={'width': 1280, 'height': 800},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        )
        page = context.new_page()
        page.goto(calendly_url, wait_until='domcontentloaded', timeout=30000)
        page.wait_for_timeout(4000)
        
        # Calendly shows a calendar with available dates
        # Navigate through months and collect available dates
        available_dates = []
        for _ in range(days_ahead // 7):
            # Extract available dates from current month view
            dates = page.evaluate('''() => {
                const results = [];
                document.querySelectorAll('[class*="calendar-day"], [data-testid*="day"], td button').forEach(el => {
                    const text = el.textContent.trim();
                    const day = parseInt(text);
                    if (day >= 1 && day <= 31) {
                        const disabled = el.hasAttribute('disabled') || 
                            el.getAttribute('aria-disabled') === 'true';
                        if (!disabled) results.push(day);
                    }
                });
                return [...new Set(results)];
            }''')
            available_dates.extend(dates)
            
            # Click next month
            next_btn = page.locator('[class*="next"], [aria-label*="Next month"]').first
            if next_btn.is_visible():
                next_btn.click()
                page.wait_for_timeout(2000)
            else:
                break
        
        browser.close()
        return {'available_dates': available_dates}
```

---

## URL Patterns

Calendly URLs follow these patterns:

```
https://calendly.com/{username}                    # All event types
https://calendly.com/{username}/{event-type-slug}  # Specific event type
```

---

## What Does NOT Work

### ❌ API without authentication
- All Calendly API endpoints require a valid token
- Unauthenticated requests return 401
- **DO:** Set `CALENDLY_API_TOKEN` environment variable

### ❌ Assuming all Calendly pages are the same
- Different event types have different durations and availability
- Group events vs. one-on-one have different booking flows
- **DO:** Check the specific event type URL

### ❌ Ignoring timezone
- Calendly returns times in the event type's timezone
- **DO:** Convert to local timezone for display

---

## Platform Quirks

1. **API rate limits** — Calendly API has rate limits (typically 2000/hour for personal tokens)
2. **Event type variations** — One-on-one, group, and collective events have different availability logic
3. **Buffer time** — Event types may have buffer time before/after meetings
4. **Minimum notice** — Some event types require advance booking (e.g., 24 hours)
5. **Timezone handling** — Always specify timezone when querying availability

---

## Detection Summary

| Check | Element Type | Method |
|-------|--------------|--------|
| API working? | HTTP | Status 200 from `/v2/users/me` |
| Event type found? | API response | Match URL against `scheduling_url` |
| Date available? | Calendar cell | Clickable date in browser |
| Time available? | API response | Slot in `event_type_available_times` |

---

## When to Use Calendly

Calendly is best for:
- Professional service bookings (consultants, coaches, therapists)
- Meeting scheduling
- Appointment-based services with fixed durations

Not ideal for:
- Restaurant reservations
- Spa/salon multi-service bookings
- Walk-in availability checks