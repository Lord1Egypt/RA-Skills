# Acuity Scheduling

**Status:** ✅ Production Ready
**Method:** REST API (no authentication required)
**Last Tested:** 2026-03-30
**Example Site:** Buddha Raksa (raksa.as.me)

---

## Happy Path (What Works)

### 1. Identify Parameters

From the booking page HTML or by intercepting network requests:

```javascript
// Extract from page or network calls
const params = {
  owner: 'a73e3599',              // Business identifier
  appointmentTypeId: '66903512', // Service ID
  calendarId: '5949533',          // Provider/staff ID
  timezone: 'America/Los_Angeles'
};
```

**Where to find:**
- `owner`: In booking URL path or `window.Acuity` object
- `appointmentTypeId`: In URL when selecting service
- `calendarId`: In provider selection dropdown or URL

### 2. Check Monthly Availability

```javascript
async function getMonthlyAvailability(params, month) {
  const url = `https://app.acuityscheduling.com/api/scheduling/v1/availability/month?` +
    `owner=${params.owner}&` +
    `appointmentTypeId=${params.appointmentTypeId}&` +
    `calendarId=${params.calendarId}&` +
    `timezone=${encodeURIComponent(params.timezone)}&` +
    `month=${month}`;  // YYYY-MM format

  const response = await fetch(url);
  return await response.json();
}

// Returns: { "2026-04-01": false, "2026-04-07": true, ... }
```

### 3. Get Daily Time Slots

```javascript
async function getDailyTimes(params, date) {
  const url = `https://app.acuityscheduling.com/api/scheduling/v1/availability/times?` +
    `owner=${params.owner}&` +
    `appointmentTypeId=${params.appointmentTypeId}&` +
    `calendarId=${params.calendarId}&` +
    `timezone=${encodeURIComponent(params.timezone)}&` +
    `startDate=${date}`;  // YYYY-MM-DD format

  const response = await fetch(url);
  const data = await response.json();
  
  // Returns array of slots
  return data[date];  // [{ time: "2026-04-07T10:30:00-0700", slotsAvailable: 1 }, ...]
}
```

### 4. Complete Working Example

```javascript
const { chromium } = require('playwright');

async function checkAcuityAvailability(config) {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  
  // Extract params from page if needed
  await page.goto(config.bookingUrl);
  
  const params = await page.evaluate(() => ({
    owner: window.Acuity?.business?.owner || '',
    appointmentTypeId: window.Acuity?.appointmentType?.id || '',
    // calendarId may need to be extracted from provider selection
  }));
  
  // Get monthly availability
  const availability = await page.evaluate(async (p) => {
    const url = `https://app.acuityscheduling.com/api/scheduling/v1/availability/month?` +
      `owner=${p.owner}&appointmentTypeId=${p.appointmentTypeId}&calendarId=${p.calendarId}&month=2026-04`;
    const res = await fetch(url);
    return res.json();
  }, params);
  
  // Get times for first available date
  const firstAvailable = Object.entries(availability)
    .find(([date, available]) => available);
  
  if (firstAvailable) {
    const [date] = firstAvailable;
    const times = await page.evaluate(async (p, d) => {
      const url = `https://app.acuityscheduling.com/api/scheduling/v1/availability/times?` +
        `owner=${p.owner}&appointmentTypeId=${p.appointmentTypeId}&calendarId=${p.calendarId}&startDate=${d}`;
      const res = await fetch(url);
      return res.json();
    }, params, date);
    
    console.log(`Available on ${date}:`, times[date]);
  }
  
  await browser.close();
}
```

---

## What Does NOT Work (Don't Try These)

### ❌ Browser scraping
- HTML doesn't contain availability data
- JavaScript renders calendar dynamically from API
- **DO:** Use API directly

### ❌ Missing `calendarId`
- Without provider ID, returns no availability
- **DO:** Always include `calendarId` (even for "any provider")

### ❌ Wrong date format
- API expects `YYYY-MM-DD` for daily queries
- Monthly expects `YYYY-MM`
- **DO:** Use exact formats, don't guess

### ❌ Timezone issues
- Server returns times in requested timezone
- Must URL-encode (e.g., `America%2FLos_Angeles`)
- **DO:** Always specify timezone explicitly

---

## Platform Quirks

1. **Rolling availability** - Only releases ~30-60 days ahead
2. **No auth required** - Public API for consumer bookings
3. **Rate limiting** - Be polite, don't hammer endpoints
4. **Calendar ID required** - Even for "any staff" you need a calendar ID

---

## Parameters Reference

| Parameter | Required | Description |
|-----------|----------|-------------|
| `owner` | ✅ | Business account identifier |
| `appointmentTypeId` | ✅ | Service/appointment type ID |
| `calendarId` | ✅ | Provider/staff calendar ID |
| `timezone` | ✅ | Client timezone (URL-encoded) |
| `month` | For monthly | Format: `YYYY-MM` |
| `startDate` | For daily | Format: `YYYY-MM-DD` |
