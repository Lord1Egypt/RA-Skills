# New Platform Onboarding Guide

Step-by-step workflow for pressure testing a new scheduling/booking platform.

---

## Phase 1: Discovery (15 minutes)

### 1.1 Load the booking page
```javascript
const page = await browser.newPage();
await page.goto('https://{platform}.com/book', { 
  waitUntil: 'domcontentloaded' 
});
await page.waitForTimeout(3000);
```

### 1.2 Capture initial state
```javascript
const fingerprint = await page.evaluate(() => ({
  url: window.location.href,
  title: document.title,
  hasShadowDOM: !!document.querySelector('*').shadowRoot,
  customElements: [...new Set(
    Array.from(document.querySelectorAll('*'))
      .map(el => el.tagName.toLowerCase())
      .filter(tag => tag.includes('-'))
  )].slice(0, 10),
  frameworks: {
    react: !!window.__REACT_ROOT__,
    vue: !!window.__VUE__,
    angular: !!window.angular
  }
}));
```

### 1.3 Check for API endpoints
```javascript
const apiCalls = [];
page.on('request', req => {
  const url = req.url();
  if (url.includes('api') || url.includes('availability') || url.includes('booking')) {
    apiCalls.push({
      url: url.substring(0, 100),
      method: req.method()
    });
  }
});
```

**Decision point:**
- API calls found with JSON responses? → Go to **Phase 2: API Route**
- No API calls, SPA behavior? → Go to **Phase 3: Browser Automation Route**

---

## Phase 2: API Route (Acuity Pattern)

### 2.1 Identify endpoints
Look for patterns like:
- `/api/scheduling/v1/availability/month`
- `/api/v1/booking/slots`
- `/graphql` with booking queries

### 2.2 Test endpoint directly
```javascript
const response = await page.evaluate(async (endpoint) => {
  const res = await fetch(endpoint);
  return res.json();
}, 'https://platform.com/api/availability');
```

### 2.3 Document parameters
Extract from network tab or HTML:
- `owner` / `business_id`
- `service_id` / `appointmentTypeId`
- `provider_id` / `calendar_id`
- `date` / `start_date`

### 2.4 Verify with manual check
Compare automation output with manual browser availability.

---

## Phase 3: Browser Automation Route

### 3.1 Identify element types
```javascript
const elementTypes = await page.evaluate(() => {
  const selectors = ['button', 'input', '[role="button"]', 'a'];
  const results = {};
  selectors.forEach(sel => {
    results[sel] = document.querySelectorAll(sel).length;
  });
  return results;
});
```

### 3.2 Check for custom elements
If you see tags like `market-button`, `booking-calendar`, etc:
- These are **web components**
- Standard selectors may not work
- Check `disabled` attribute via DOM directly

### 3.3 Find semantic selectors
```javascript
const semanticElements = await page.evaluate(() => {
  const results = [];
  document.querySelectorAll('[aria-label], [data-testid]').forEach(el => {
    results.push({
      tag: el.tagName,
      ariaLabel: el.getAttribute('aria-label'),
      dataTestId: el.getAttribute('data-testid'),
      text: el.textContent?.trim().substring(0, 30)
    });
  });
  return results.slice(0, 20);
});
```

### 3.4 Test availability detection
```javascript
// For standard elements:
const isAvailable = await btn.isEnabled();

// For custom elements:
const isAvailable = await page.evaluate(() => {
  const btn = document.querySelector('custom-element');
  return !btn.hasAttribute('disabled');
});
```

---

## Phase 4: Validation

### 4.1 Compare with manual browser
**CRITICAL:** Always verify automation shows same availability as manual check.

```javascript
// Run automation
const autoResults = await checkAvailability();

// Compare with what you see in browser
console.log('Automation shows:', autoResults);
console.log('Manual shows: ???'); // You verify this
```

### 4.2 Test full flow
Pick one available date and time, walk through:
1. Service selection
2. Staff/provider selection
3. Date selection
4. Time selection
5. Confirmation/checkout

### 4.3 Document findings
Create platform file with:
- Happy path (working code)
- Pitfalls (what NOT to do)
- Quirks (platform-specific weirdness)

---

## Phase 5: Documentation Template

Create `{platform}.md`:

```markdown
# {Platform} Scheduling

**Status:** ✅ Production / ⚠️ Working / ❌ Blocked
**Last tested:** YYYY-MM-DD

## Quick Start
```javascript
// Working code here
```

## What Works (Happy Path)
1. Step-by-step...

## What Does NOT Work (Learned Painfully)
1. Failed approach...
2. Another failure...

## Platform Quirks
- Weird thing #1
- Weird thing #2
```

---

## Troubleshooting Checklist

- [ ] Page loads without errors
- [ ] Can identify service/appointment type
- [ ] Can navigate to calendar
- [ ] Availability detection matches manual browser
- [ ] Can select available date
- [ ] Can extract time slots
- [ ] Can select time
- [ ] Reaches confirmation/checkout

---

## Emergency Escapes

If stuck on a platform:
1. Try mobile user agent
2. Try disabling JavaScript
3. Check for GraphQL introspection
4. Look for `/swagger` or `/api/docs`
5. Search GitHub for "{platform} api" or "{platform} booking"
6. Check if there's a public API documentation
