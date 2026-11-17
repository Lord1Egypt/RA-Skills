# Vagaro

**Status:** ⚠️ Partial (Browser automation, API-dependent)
**Method:** Direct browser automation
**Last Tested:** 2026-05-18
**Domains:** `*.vagaro.com`
**Example Site:** Rin Wellness & Spa (`https://www.vagaro.com/rinwellnessandspa`)

---

## Platform Overview

Vagaro is a spa/salon booking platform. The booking flow involves: Services page → Book Now → Add-Ons modal → Date/Time selection. The platform uses Bootstrap modals and has API dependencies that can fail in headless/browser automation environments.

---

## Happy Path (What Works)

### 1. Services Page

```
URL: https://www.vagaro.com/{business}/services
```

Services are listed with "Book Now" buttons. Each service has a button with ref like `e112`.

### 2. Clicking "Book Now"

Click the "Book Now" button for the desired service. This typically opens an "Add-Ons Available" modal.

### 3. Add-Ons Modal

An "Add-Ons Available" modal appears with checkboxes for add-ons. Close it to proceed:
```javascript
// Close add-on modal
document.querySelectorAll('.createaddOn-pop').forEach(modal => {
  const closeBtn = modal.querySelector('[class*="close"], button.close, .modal-header button, [data-dismiss="modal"]');
  if (closeBtn) closeBtn.click();
});
```

**Note:** After closing the add-on modal, the page may or may not proceed to date/time selection. In testing, the Vagaro API (`/api/v2/public/promotion/getallpromotiondetailsbybus`) returned errors, preventing the booking flow from completing.

---

## What Does NOT Work

### ❌ Full booking flow via browser automation
- Vagaro's booking flow depends on API calls that may fail in browser automation environments
- Error modal "Oops! An Error Has Occurred" with API URL `https://api.vagaro.com/US02/api/v2/public/promotion/getallpromotiondetailsbybus` blocks the flow
- **Workaround:** Check the services page for service names and prices, but date/time availability may not be checkable

### ❌ Direct API access blocked by Incapsula
- `api.vagaro.com` endpoints return Incapsula challenge pages (HTTP 403 with iframe redirect)
- Even from the browser context, cross-origin fetch to `api.vagaro.com` is blocked
- **DO NOT** attempt direct API calls; they will always fail from a non-residential IP

### ❌ Vagaro "Book Now" button on services page
- Clicking "Book Now" may open stacked "Add-Ons Available" modals that error out
- After closing error modals, the booking widget often fails to load
- The `/booking` URL with `?date=` and `?service=` query params does NOT pre-select the service
- **WORKAROUND:** If the booking widget fails to load after 2 attempts, fall back to reporting the service/pricing info visible on the services page

### ❌ Vagaro "Choose Date And Time" button on /booking page
- On the `/booking` page, clicking "Choose Date And Time" may not open a date picker
- The page requires a service to be selected first through the widget flow
- Without a working widget, date selection is not possible

### ❌ Closing Vagaro modals
- Multiple stacked modals (cookie consent, add-ons, errors) can appear simultaneously
- Close error modals first: `document.querySelectorAll('.bootbox .btn-primary')`
- Then close add-on modals: `document.querySelectorAll('[role="dialog"] button')`

### ❌ Direct booking URL navigation
- Navigating to `/booking` redirects back to the main page
- The booking flow must start from the services page

---

## Platform Quirks

1. **API-dependent** — Booking flow requires working API endpoints; fails if API returns errors
2. **Bootstrap modals** — Uses Bootstrap modal system for add-ons; multiple modals can stack
3. **Service list on services page** — All services with prices are visible on `/services` page without needing to go through the booking flow
4. **Cookie consent** — May show cookie consent banner on first visit

---

## Detection Summary

| Check | Element Type | Method |
|-------|--------------|--------|
| Service available? | Button | "Book Now" button exists on `/services` page |
| Price visible? | StaticText | Price shown next to service name |
| API working? | Error modal | Look for "Oops! An Error Has Occurred" modal |