# Acuity Scheduling Availability Extraction

**Date learned:** 2026-03-30
**Source:** Buddha Raksa (raksa.as.me)
**Provider:** Anya
**Service:** Thai Aroma 90 mins ($220)

## What I Learned

Acuity Scheduling exposes an internal REST API that returns JSON availability data without authentication (for public booking pages).

### Key Endpoints

**1. Monthly Availability Check**
```
GET https://app.acuityscheduling.com/api/scheduling/v1/availability/month?owner={OWNER_KEY}&appointmentTypeId={SERVICE_ID}&calendarId={PROVIDER_ID}&timezone={TIMEZONE}&month={YYYY-MM}
```

Returns:
```json
{
  "2026-04-01": false,
  "2026-04-07": true,
  ...
}
```

**2. Daily Time Slots**
```
GET https://app.acuityscheduling.com/api/scheduling/v1/availability/times?owner={OWNER_KEY}&appointmentTypeId={SERVICE_ID}&calendarId={PROVIDER_ID}&timezone={TIMEZONE}&startDate={YYYY-MM-DD}
```

Returns:
```json
{
  "2026-04-07": [
    {"time": "2026-04-07T10:30:00-0700", "slotsAvailable": 1},
    ...
  ]
}
```

### Parameters to Extract

From the booking page HTML or by intercepting network requests:

1. **owner** (OWNER_KEY): Business identifier (e.g., `a73e3599`)
2. **appointmentTypeId**: Service ID (e.g., `66903512` for Thai Aroma 90 min)
3. **calendarId**: Provider/staff ID (e.g., `5949533` for Anya)
4. **timezone**: Client timezone (e.g., `America%2FLos_Angeles`)

### Finding Parameters

**Method 1: Browser Network Tab**
1. Open booking page in browser
2. Open DevTools → Network tab
3. Look for XHR requests to `api/scheduling/v1/`
4. Extract parameters from request URLs

**Method 2: HTML Source Inspection**
- Search booking page HTML for `ownerKey`, `appointmentType`, `calendarId`
- These are often embedded in JavaScript variables or data attributes

### Limitations

- **Rolling window:** API rejects queries for months before current month
- **Provider-specific:** Each provider has separate calendarId
- **Service-specific:** Different services have different appointmentTypeId
- **Limited lookahead:** Typically 30-60 days of availability released

### Pattern for Automation

```python
import requests

def get_acuity_availability(owner_key, service_id, provider_id, timezone):
    # Get monthly availability
    month_url = f"https://app.acuityscheduling.com/api/scheduling/v1/availability/month?owner={owner_key}&appointmentTypeId={service_id}&calendarId={provider_id}&timezone={timezone}&month=2026-04"
    
    response = requests.get(month_url)
    available_dates = [k for k, v in response.json().items() if v]
    
    # Get time slots for available dates
    for date in available_dates[:5]:  # Limit to first 5 dates
        times_url = f"https://app.acuityscheduling.com/api/scheduling/v1/availability/times?owner={owner_key}&appointmentTypeId={service_id}&calendarId={provider_id}&timezone={timezone}&startDate={date}"
        times_response = requests.get(times_url)
        slots = times_response.json().get(date, [])
        # Process slots...
```

### Reusable for Other Acuity Businesses

This pattern works for any Acuity Scheduling business:
1. Navigate to booking URL (e.g., `business.as.me`)
2. Extract owner key from HTML or network calls
3. Identify service and provider IDs
4. Query availability endpoints directly

No authentication needed — endpoints are public for booking purposes.

### Tools Available

- **Playwright + Stealth:** For initial parameter extraction from JS-heavy pages
- **curl:** For direct API queries once parameters known
- **Python requests:** For scripted availability monitoring

### Next Steps / Enhancements

- Create skill: `acuity-availability` that accepts business URL, provider name, service name
- Auto-extract parameters from booking page
- Cache provider/service IDs for reuse
- Schedule periodic checks (weekly) for new availability
- Alert when preferred provider has new slots