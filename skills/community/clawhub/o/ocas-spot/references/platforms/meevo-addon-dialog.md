# Meevo — Service Add-On Dialog

**Added:** 2026-05-30

## Add-On Dialog Blocking Flow (CRITICAL)

After selecting a service on Meevo's service/employee selection step, an **add-on dialog** may appear:
- Header: `.mil-modal-dialog__header.modal-header`
- Title: "Service Add-Ons available for {Service Name}"
- Contains a close button: `mat-icon.mil-close-icon` (SVG icon, no text)

### Symptom
- Dialog appears after clicking a service header (`div.service-header`)
- "Next" button becomes unclickable
- The dialog must be dismissed before proceeding to employee selection

### Fix
Click the close icon to dismiss:

```javascript
(() => {
  const closeIcon = document.querySelector('.mil-close-icon');
  if (closeIcon) {
    closeIcon.click();
    return 'dismissed add-on dialog';
  }
  // Fallback: remove all hidden dialogs
  document.querySelectorAll('[role="dialog"]').forEach(d => d.remove());
  return 'removed dialogs';
})();
```

### Full Service Selection Pattern

After clicking a service (which triggers the add-on dialog):

```javascript
(() => {
  // Dismiss add-on dialog
  const closeIcon = document.querySelector('.mil-close-icon');
  if (closeIcon) closeIcon.click();
  
  // Remove any leftover hidden dialogs
  document.querySelectorAll('[role="dialog"]').forEach(d => {
    if (!d.innerText?.trim()) d.remove();
  });
  
  return 'cleaned';
})();
```

Then proceed to employee selection and click Next.

### Notes
- Cookie consent dialog ("Accept All" / "Reject All") may also appear after add-on dismissal
- Handle cookie consent BEFORE dismissing hidden dialogs, or handle both in sequence
- The cookie consent can appear at unexpected points mid-flow, not just at the start