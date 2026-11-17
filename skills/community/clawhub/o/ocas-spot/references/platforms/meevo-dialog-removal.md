# Meevo — Hidden Dialog Removal Pattern

**Added:** 2026-05-30

## Empty/Hidden Dialog Blocking Flow

After closing add-on dialogs and cookie consent on the service selection step, Meevo may leave a **hidden empty dialog** (`[role="dialog"]` with empty innerText) in the DOM. This invisible overlay blocks the "Next" button click.

### Symptom
- `[role="dialog"]` returns `true` but `innerText` is empty
- Clicking "Next" has no effect
- The dialog has no visible buttons to dismiss

### Fix
Force-remove all dialog elements from the DOM:

```javascript
(() => {
  document.querySelectorAll('[role="dialog"]').forEach(d => {
    d.style.display = 'none';
    d.remove();
  });
  return 'removed dialogs';
})();
```

After removal, verify: `document.querySelector('[role="dialog"]')` returns `null`, then click "Next".

## Scan Next Counting — June 19 Example

On 2026-05-30, the initial scan window was "Sat May 30 - Sat Jun 13" (14 days). "Scan next 7 days" was clicked **once**, advancing the window to "Sun Jun 14 - Sat Jun 20", which included Friday June 19. 

**Strategy**: Each click advances by exactly 7 days. Count carefully — there is NO "Scan previous" button. If you overshoot, you must restart the entire booking flow from the beginning.