# Meevo — Employee Radio Behavior (Updated Observation)

**Added:** 2026-05-30

## Employee Radios: Standard Click Works (Contradicts Prior Guidance)

The skill's Gotchas section states: *"Meevo employee radios need native input click — Angular Material radio buttons don't respond to container div or label clicks."*

**Observed May 30 2026**: On the Service/Employee Selection step, the employee filter radios ("Any Employee", "Any Male", "Any Female") **did respond to standard `browser_click` on the snapshot ref**:

```
browser_click(ref=e37) → "clicked"
browser_console(verify) → [{checked: true, label: ""}]  ← radio is selected
```

The radios are standard `input[type="radio"]` elements inside `.mat-mdc-radio-button` wrappers, but clicking the **snapshot ref** (which points to the `<generic>` wrapper element) was sufficient — Angular's change detection fired and the radio was checked.

**Hypothesis**: The earlier failure mode (container clicks not working) may have been specific to the *employee checkboxes* (Jameson, Joanna, Kristy, Matthew, Rachel, Torreyanna) or a different Meevo version. The **filter radios** (Any Employee/Male/Female) appear to work with standard clicks.

## Service Item Radios (Add-on Dialog Handling Confirmed)

When clicking a Swedish Massage service item:
- Add-on dialog appeared (`.mil-modal-dialog__header`)
- Dismissed via `.mil-close-icon` click ✅
- Hidden `[role="dialog"]` remained — removed via DOM removal ✅
- Cookie consent ("Accept All") appeared — dismissed ✅
- Next button became clickable after all dialogs cleared ✅

## Scan Window Navigation

Window started at "Sat May 30 - Sat Jun 13". One click of "Scan next 7 days" advanced to "Sun Jun 14 - Sat Jun 20", which included Friday June 19. Full flow completed successfully.

## Full Flow Steps (Verified May 30 2026)

1. Navigate to booking URL → cookie consent appears → Accept All
2. Guest Information → "Me Only" pre-selected → Click Next
3. Service/Employee Selection:
   a. Click category (Massages) via `.category-item` dispatchEvent pattern
   b. Click service item (`Swedish Massage - 60 Minute`) — triggers add-on dialog
   c. Dismiss add-on dialog (`.mil-close-icon`)
   d. Remove hidden `[role="dialog"]` elements
   e. Dismiss cookie consent if reappeared
   f. Click employee filter radio ("Any Employee") — standard click works
   g. Click Next
4. Date & Time → Click "Scan next 7 days" as needed → read availability