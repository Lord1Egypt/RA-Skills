# Square Appointments — Cookie Consent & Book Button

**Added:** 2026-05-30
**Last Updated:** 2026-05-30 (confirmed working end-to-end flow)

## ⚠️ KNOWN INSTABILITY (Added 2026-05-30)

The OneTrust DOM removal on `/services/{id}` can crash the browser session, even though this is the documented correct page for the operation. Observed May 30 2026: two consecutive attempts both hung the Chrome process (renderer at 100%+ CPU).

**Recovery protocol**:
1. If `browser_click` or `browser_console` times out after OneTrust removal, kill Chrome: `pkill -f "google-chrome"`
2. Wait 3 seconds for Hermes browser tool to auto-restart
3. Re-navigate to base URL and retry the full flow
4. If it crashes again on retry, **skip the venue** for this sweep cycle. Log "blocked — Square crash" in the watch note.

**Do NOT attempt more than 2 OneTrust removal runs per sweep per venue.** The session cost of repeated crashes exceeds the value.

## `market-radio` checked property unreliable

`input.checked` may return `false` synchronously after `.click()` inside the shadow DOM. The actual selection may take effect asynchronously. **Do not rely on `input.checked` as verification** — proceed with the Book click and check the resulting URL instead.

## OpenTable requires Firefox

As of May 2026, Square booking pages load a OneTrust cookie consent overlay that **intercepts all clicks** on the "Book" `market-button`. This is the #1 blocker for Square automation.

### What happens
- The consent overlay (`[aria-label="Close preference center"]`) appears on every page load
- After accepting cookies ("Accept all cookies" or "Confirm my choices"), the overlay sometimes reappears after subsequent JS interactions
- After the overlay is dismissed, the page **re-renders**, causing radio button selections (market-radio) to reset to unchecked
- The Book button click via the host element `.click()` does NOT trigger navigation — it only works via the **inner shadow DOM button**
- Clicking the inner shadow DOM button also fails when the overlay is present, even if visually hidden

## ⚠️ CRITICAL: Do NOT Use `?service_id=` URL Parameter (UPDATED May 2026)

As of late May 2026, `?service_id=` Square booking page returns **"We're sorry, but something went wrong."** error page. This breaks the previously documented URL-based navigation.

**Correct approach**: Navigate to the base booking URL **without** parameters:
```
https://book.squareup.com/appointments/{appointmentId}/location/{locationId}
```
This loads the services list. Then click the desired service row to navigate to the service detail page.

## ⚠️ CRITICAL: OneTrust DOM Removal Only on Service Detail Page (UPDATED May 2026)

OneTrust DOM removal at the **services list page** (URL: `/location/{id}/services`) crashes the page to "something went wrong". 

**Correct approach**: 
1. Navigate to base URL → services list loads
2. Click service row → navigates to `/services/{serviceId}` (service detail page)
3. **Only then** execute OneTrust DOM removal + radio selection + Book click

Do NOT remove OneTrust elements until you are on the service detail page with `market-radio` and `market-button` elements present.

## ✅ CORRECT WORKING FLOW (Updated May 2026)

### Step 1: Navigate to Base URL (no params)
```
mcp_stealth_browser_navigate → https://book.squareup.com/appointments/{id}/location/{id}
```

### Step 2: Click Service Row
```javascript
(() => {
  const rows = Array.from(document.querySelectorAll('market-row.service-row'));
  const row = rows.find(r => r.textContent?.includes('Traditional Thai Massage'));
  if (row) { row.click(); return 'clicked'; }
  return 'not found';
})()
```
This navigates to `/services/{serviceId}`.

### Step 3: DOM Removal + Selections + Book (single synchronous script)
Execute ALL steps in ONE synchronous call on the service detail page only:

```javascript
(() => {
  // Step 1: Force-remove ALL OneTrust elements from DOM
  document.querySelectorAll('[class*="onetrust"], [id*="onetrust"]').forEach(el => el.remove());

  // Step 2: Select duration radio (find by aria-label on host, click native input in shadow DOM)
  document.querySelectorAll('market-radio').forEach(r => {
    if (r.getAttribute('aria-label') === '1 Hour') {
      const inp = r.shadowRoot?.querySelector('input[type="radio"]');
      if (inp) inp.click();
    }
  });

  // Step 3: Select staff radio
  document.querySelectorAll('market-radio').forEach(r => {
    if (r.getAttribute('aria-label') === 'Any staff') {
      const inp = r.shadowRoot?.querySelector('input[type="radio"]');
      if (inp) inp.click();
    }
  });

  // Step 4: Click Book button via inner shadow DOM button
  const bookBtn = Array.from(document.querySelectorAll('market-button')).find(b => b.textContent?.trim() === 'Book');
  if (bookBtn) {
    const inner = bookBtn.shadowRoot?.querySelector('button');
    if (inner) inner.click();
  }

  return { overlayGone: !document.querySelector('[class*="onetrust"]') };
})()
```

### Step 4: URL Date Jump (after reaching /availability)

Once on `/availability`, navigate to the target date via URL parameter:

```
mcp_stealth_browser_navigate → {base_url}/availability?service_id={SERVICE_ID}&date=YYYY-MM-DD
```

Once on `/availability`, navigate to the target date via URL parameter:

```
mcp_stealth_browser_navigate → {base_url}/availability?service_id={SERVICE_ID}&date=YYYY-MM-DD
```

**CRITICAL**: URL date jump ONLY works from an established session after completing Phase 1. It silently redirects back to `/services/` from a fresh browser instance.

After URL navigation, the cookie dialog may reappear — dismiss again via DOM removal.

## market-radio Shadow DOM Pattern (CONFIRMED)

`market-radio` labels are on the **host** element via `aria-label` (Light DOM). Shadow DOM contains only `<input type="radio">` with NO text:

```javascript
// CORRECT:
document.querySelectorAll('market-radio').forEach(r => {
  const label = r.getAttribute('aria-label'); // "1 Hour", "Any staff", etc.
  const inp = r.shadowRoot?.querySelector('input[type="radio"]');
  if (inp) inp.click();
});

// WRONG: r.textContent?.trim() returns "" for all radios
// WRONG: shadowRoot.textContent returns "" — no text in shadow DOM
```

Verify via `input.checked === true`, NOT `aria-pressed` (stays null).

## Persistent Browser Session

Using `user_data_dir` does NOT prevent OneTrust overlay reappearance. The overlay is session-based. Always include DOM removal in the automation flow.

## Previous Attempts that FAILED

| Approach | Result |
|----------|--------|
| Accept cookies → select radios → click Book host `.click()` | Book doesn't navigate |
| Accept cookies → select radios → dispatchEvent on Book | Book doesn't navigate |
| Accept cookies → select radios → shadow DOM Book click | Fails after overlay dismissal resets radios |
| Remove overlay → select radios → click Book in **separate** scripts | Page re-renders between scripts, loses selections |
| Hide overlay via CSS (`display:none`) | Overlay still captures events |
| `[aria-label="Close preference center"].click()` | Reappears on next interaction |
| URL date jump from fresh browser instance | Redirects to `/services/` silently |
| URL date jump with wrong service_id format | "Something went wrong" error |
| Navigate to base URL with `?service_id=` param | "Something went wrong" error — page crashes immediately |
| OneTrust DOM removal at services list page (`/location/{id}/services`) | Page crashes to "something went wrong" — only remove on service detail page |
| OneTrust DOM removal in separate script from radio selection | Page re-renders between scripts, loses selections |

## "Update" Button Fallback Path

If DOM removal stops working:
1. Click service row → navigates to `/services/{ID}`
2. Page shows "Update" and "Remove" buttons (service in cart)
3. Click "Update" → navigates to `/availability`

The "Update" button bypasses cookie overlay because cart state persists.