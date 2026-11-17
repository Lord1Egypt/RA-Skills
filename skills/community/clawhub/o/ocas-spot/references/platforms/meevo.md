# Meevo (Millennium)

**Status:** ⚠️ Working (Browser automation required)
**Method:** Direct browser automation (Angular SPA)
**Last Tested:** 2026-05-18
**Domains:** `*.meevo.com`
**Example Site:** Rockridge Day Spa (`login.meevo.com/rockridgedayspa/ob?locationId=203379`)

---

## Platform Overview

Meevo is Angular-based SPA booking software used by salons and spas. The booking flow is a multi-step wizard: Location → Guest Info → Service Selection → Employee Selection → Date/Time.

---

## Happy Path (What Works)

### 1. Initial Navigation

Navigate to the booking URL. A cookie consent banner may appear — click "Accept All" first.

```
URL pattern: https://login.meevo.com/{business}/ob?locationId={id}
Redirects to: https://na1.meevo.com/CustomerPortal/onlinebooking?tenantId={t}&locationId={l}
```

### 2. Guest Information (Step 1)

Click "Next" to proceed with default "Me Only" selection.

### 3. Service Selection (Step 2) — CRITICAL

**Category selection:** Service categories appear as `<li class="category-item-li">` elements. These do NOT respond to standard click events on the `<li>` itself.

**DO:** Find the inner `div.category-item` and click it:
```javascript
document.querySelectorAll('div.category-item').forEach(el => {
  if (el.textContent.trim() === 'Massages') el.click();
});
```

**Sub-service selection:** After clicking a category, sub-services appear. Each sub-service has a `div.service-header` containing the name. Clicking this opens an "Add-Ons Available" dialog.

**Add-Ons dialog:** After clicking a service, a modal "Service Add-Ons available for {service}" appears. Multiple stacked dialogs may appear. Close them all:
```javascript
document.querySelectorAll('[role="dialog"]').forEach(d => {
  d.querySelectorAll('button').forEach(btn => {
    const text = btn.textContent.trim();
    if (text === 'Save' || text === 'No, thanks') btn.click();
  });
});
```

**Verify selection:** After closing add-on dialogs, verify the service name appears in `document.body.innerText`. Do NOT rely on the "Service not selected" text — it may persist even after successful selection.

### 4. Employee Selection

After service selection, click "Next" to proceed to employee selection. Employees are listed with radio buttons. "Any Employee" is typically pre-selected. Click "Next" again.

### 5. Date/Time Selection

**Date navigation:** Meevo shows a 7-day scan window. Use "Scan next 7 days" button to advance forward. The current scan range is shown as "Scan Date: {start} - {end}".

**"Specific" date dropdown:** BROKEN in browser automation. Angular rendering doesn't propagate JS click events properly. **DO:** Use "Scan next 7 days" repeatedly instead.

**Reading availability:** Each date shows "N Openings" with time slots listing time, duration, service, employee, price, and a "Select" button.

```javascript
// Extract all dates and opening counts from page text
const lines = document.body.innerText.split('\n');
const results = [];
let currentDate = null;
for (const line of lines) {
  const dateMatch = line.match(/^(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday), ([A-Z][a-z]+ \d+, \d{4})$/);
  if (dateMatch) { currentDate = line; continue; }
  const openingsMatch = line.match(/^(\d+) Opening/);
  if (openingsMatch && currentDate) {
    results.push({date: currentDate, openings: parseInt(openingsMatch[1])});
  }
}
```

---

## What Does NOT Work

### ❌ Standard `browser_click` or JS `.click()` on sub-service radio buttons
- Meevo's Angular SPA does NOT propagate standard click events on `<input type="radio">` elements
- `browser_click` on the radio ref, `r.click()`, and `r.dispatchEvent(new Event('change'))` all FAIL
- **WORKAROUND:** Dispatch pointer events on the radio AND click the parent `div.flex`:
  ```javascript
  // Step 1: Dispatch pointer events on the radio input
  const radios = document.querySelectorAll('input[type="radio"]');
  for (const r of radios) {
    const label = r.closest('label') || r.parentElement;
    if (label && label.textContent.includes('Swedish Massage - 90 Minute')) {
      r.focus();
      r.checked = true;
      r.dispatchEvent(new PointerEvent('pointerdown', {bubbles: true, cancelable: true, view: window}));
      r.dispatchEvent(new PointerEvent('pointerup', {bubbles: true, cancelable: true, view: window}));
      r.dispatchEvent(new MouseEvent('click', {bubbles: true, cancelable: true, view: window}));
      break;
    }
  }
  // Step 2: Also click the parent div.flex container
  for (const r of radios) {
    const label = r.closest('label') || r.parentElement;
    if (label && label.textContent.includes('Swedish Massage - 90 Minute')) {
      const parent = r.closest('div.flex');
      if (parent) parent.click();
      break;
    }
  }
  ```
- **VERIFY:** Check `r.checked === true` after the click sequence
- **NOTE:** Even with `checked=true` in the DOM, the Angular model may not update, and "Next" may still not advance. This is a fundamental limitation of Meevo's Angular SPA with browser automation.

### ❌ Meevo "Next" button after programmatic service selection
- Even when `r.checked === true` is confirmed via JS, the Angular model's internal state may not reflect the change
- The "Next" button click (both `browser_click` and JS `.click()`) may NOT advance to the next step
- The UI continues to show "Service not selected"
- **This is a known hard failure mode.** If the Next button doesn't advance after 2 attempts with the pointer-event workaround, the venue cannot be checked via automation. Fall back to reporting the service/pricing info visible on the page and noting that availability could not be confirmed.

### ❌ Standard click on category `<li>` elements
- `li.category-item-li` doesn't respond to click
- **DO:** Click the inner `div.category-item` instead

### ❌ Relying on "Service not selected" text
- This text may persist even after successful service selection
- **DO:** Search `document.body.innerText` for the service name instead

### ❌ "Specific" date dropdown via JS click
- Angular rendering doesn't propagate the click properly
- **DO:** Use "Scan next 7 days" button repeatedly

### ❌ Single click on add-on dialog buttons
- Multiple stacked dialogs may appear
- **DO:** Close ALL dialog buttons in a loop

---

## Platform Quirks

1. **Angular SPA** — Standard DOM clicks often don't trigger Angular event handlers; target the correct inner element
2. **Multi-step wizard** — Each step must complete before the next is enabled; tabs show step numbers
3. **Stacked modals** — Multiple add-on dialogs can stack; all must be closed
4. **7-day scan window** — Date navigation is paginated in 7-day chunks, not month-by-month
5. **Employee-specific pricing** — Prices vary by employee; "Any Employee" may not show a price until selected
6. **Scan persists filters** — Time-of-day filter persists across scans

---

## Detection Summary

| Check | Element Type | Method |
|-------|--------------|--------|
| Service selected? | Body text | Search `body.innerText` for service name |
| Date available? | Heading | Look for "N Openings" under date heading |
| Time slot available? | Button | "Select" button exists for each slot |
| Current scan range? | LabelText | "Scan Date: {start} - {end}" |