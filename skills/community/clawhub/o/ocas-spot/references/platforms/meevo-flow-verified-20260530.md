# Meevo Full Flow — Verified 2026-05-30

**Venue:** Rockridge Day Spa  
**URL:** `https://login.meevo.com/rockridgedayspa/ob?locationId=203379`  
**Service:** Swedish Massage - 60 Minute ($119-$149)  
**Date checked:** Friday, June 19, 2026  
**Result:** ✅ Full flow completed end-to-end

## Cookie Consent Mid-Flow (NEW 2026-05-31)

After closing the add-on dialog on the service selection step, a consent dialog ("Customise Consent Preferences") may appear OVER the booking flow. This is separate from the initial page-load cookie consent and the add-on dialog. When it appears mid-flow:

1. Try clicking "Accept All" or close button via JS
2. If that doesn't dismiss it, remove ALL elements matching `[class*="cookie"], [id*="cookie"], [class*="consent"]` via JS DOM removal
3. Also remove any remaining hidden `[role="dialog"]` elements: `document.querySelectorAll('[role="dialog"]').forEach(d => d.remove())`
4. Verify "Service not selected" is gone before proceeding with Next

**Important**: DOM removal of consent elements did NOT cause a crash in this session (unlike Square OneTrust). Proceed confidently.

**Note (May 31 21:00 PT cron sweep):** On two consecutive attempts in the same sweep, the cookie consent dialog appeared after add-on dialog close BOTH times. Dismissing it via JS "Accept All" worked, but the Angular model had already reset by that point — "Service not selected" persisted after consent dismissal. The cookie consent appearing is a symptom, not the cause — the root issue is Angular's model resetting when the add-on dialog closes. Dismissing cookie consent is still necessary to proceed, but don't expect it to fix the underlying selection persistence issue.

## 2026-05-31 Successful Run (14:46 PT cron sweep) — Angular Issue Resolved

- Full flow completed: category expand → service click (full JS sequence) → add-on dialog → cookie consent appeared → DOM removal → re-click service (full JS sequence) → add-on dialog → **selection persisted** → employee selection → Next → Date & Time
- **Key difference from prior failures**: Cookie consent was dismissed via DOM removal (not Accept All click), then service was RE-CLICKED with the full JS event sequence. This two-pass approach (click → dialog → cookie removal → re-click → dialog → persist) is the verified working pattern.
- Angular change detection issue RESOLVED with this approach after 9+ consecutive failures
- Scan window "Mon Jun 15 - Sun Jun 21" reached via one "Scan next 7 days" click
- June 19 openings: 10:00 AM, 1:15 PM, 2:00 PM, 2:30 PM, 3:15 PM (5 total, none in 3:30-5:00 PM window)

## Cookie Consent vs Add-On Dialog (Updated 2026-05-31)

The mid-flow dialog that appears after a service click can be EITHER:
1. **Add-on dialog** (the "would you like to add..." prompt) — close via `.mil-close-icon` or "No, thanks"
2. **Cookie consent dialog** ("Customise Consent Preferences") — dismiss via "Accept All" button

Both variants cause Angular's model to reset after dismissal. The cookie consent variant has become more frequent in recent sweeps (May 31). The handling differs:
- For add-on dialog: close via JS loop (Save/No thanks/Close/Cancel/OK)
- For cookie consent: click "Accept All" inside the dialog via JS

Regardless of which appears, **service selection does not persist** after dialog dismissal. This is the root Angular change detection issue. See `references/meevo-angular-change-detection.md`.

## Steps That Worked

### 1. Initial Navigation
Navigate to booking URL → redirects to `na1.meevo.com/CustomerPortal/onlinebooking/booking/guestinfo`

### 2. Cookie Consent (First)
Dismiss `[role="dialog"]` → "Accept All" via `browser_click(ref=e5)`

### 3. Guest Information
"Me Only" pre-selected → click "Next"

### 4. Service Selection
- Click "Massages" category via JS: `document.querySelectorAll('li.category-item-li')` → inner `div.category-item` click
- Sub-services appear with radio buttons
- Click "Swedish Massage - 60 Minute" radio via `browser_click(ref=e16)` → add-on dialog appears
- **Cookie consent dialog reappeared** — dismissed via JS: `[role="dialog"]` → "Accept All"
- Close add-on dialog via JS loop (5 rounds: Save/No thanks/Close/Cancel/OK/Accept All/Reject All)
- Remove hidden dialogs: `document.querySelectorAll('[role="dialog"]').forEach(d => d.remove())`
- **Verify via snapshot:** Look for service name + price in guest summary area, `checked=true` on the radio

### 5. Employee Selection
Click "Next" → employee radios appear → click "Any Employee" via JS:
```javascript
document.querySelectorAll('.mat-mdc-radio-button input[type="radio"]')
  .forEach(r => { if (r.closest('.mat-mdc-radio-button').textContent.trim() === 'Any Employee') r.click(); })
```
Click "Next"

### 6. Date/Time
Default scan window: "Sat May 30 - Sat Jun 13"  
Click "Scan next 7 days" once → "Sun Jun 14 - Sat Jun 20" (includes June 19)

### 7. June 19 Results
5 Openings: 10:00 AM, 1:15 PM, 2:00 PM, 2:30 PM, 3:15 PM (none in 3:30-5:00 PM window)

## Key Finding
Service selection **persisted** through add-on dialog dismissal when cookie consent was dismissed first. This was the first successful full flow completion in multiple sweeps. The cookie consent reappearing mid-flow was the main new obstacle.