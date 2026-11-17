# Meevo — Service Category & Item Click Patterns

**Added:** 2026-05-30

## Category Selection (CRITICAL)

Meevo's service categories are Angular components. `browser_click` on the `<li>` element is **NOT reliable**. The click must be dispatched on the inner `.category-item` div.

### Symptom
- `browser_click` on the `li` (found by text content) returns "clicked" but nothing happens
- Category sub-services don't load
- `.category-selected` div doesn't change

### Fix — Category Click Pattern

```javascript
(() => {
  const items = Array.from(document.querySelectorAll('li'));
  const item = items.find(i => i.textContent?.trim() === 'Massages');
  if (item) {
    // Must dispatch on the inner .category-item div, not the li
    const div = item.querySelector('.category-item');
    if (div) {
      div.dispatchEvent(new MouseEvent('mousedown', {bubbles: true, cancelable: true}));
      div.dispatchEvent(new MouseEvent('mouseup', {bubbles: true, cancelable: true}));
      div.dispatchEvent(new MouseEvent('click', {bubbles: true, cancelable: true}));
      return 'dispatched events on .category-item';
    }
    item.click();
    return 'clicked li (fallback)';
  }
  return 'not found';
})();
```

**Verify**: Check that `.category-selected` span text changes to the category name.

## Service Radio Selection — Angular Model Persistence Issue (2026-05-30)

After successfully expanding a category via `.category-item` dispatchEvent, the sub-service radio buttons appear with `<input type="radio">` elements. However, clicking these radios (either via `browser_click` or JS `r.checked = true` + `dispatchEvent`) may show `checked=true` in the DOM snapshot while Angular's internal model still shows "Service not selected."

### Symptoms
- Snapshot shows `checked=true` on the target radio ref
- Page status still reads "Service not selected"
- "Next" button may remain functionally disabled

### Attempted Fixes (Both Failed)
1. `browser_click` on the radio ref → `checked=false` in snapshot, selection lost after add-on dialog
2. JS: `r.checked = true` + `dispatchEvent(new Event('change'))` + `dispatchEvent(new Event('input'))` → `checked=true` in DOM but Angular model unchanged

### Recommendation
When category expansion succeeds but service radio selection doesn't persist after 2 attempts, **defer and use prior sweep data**. Do not burn more than 2 attempts per sweep. This is an intermittent Angular (v2+) change detection issue that sometimes resolves (verified working end-to-end on 2026-05-30 in a prior run) but often doesn't.

## Service Item Selection

After selecting a category, sub-service items appear with class `service-item-container`. These are `<div>` elements. Click them directly:

```javascript
(() => {
  const items = Array.from(document.querySelectorAll('[class*="service-item"]'));
  const swedish = items.find(i => i.textContent?.includes('Swedish Massage - 60 Minute'));
  if (swedish) {
    swedish.click();
    return 'clicked Swedish Massage - 60 Minute';
  }
  return 'not found';
})();
```

**Known issue**: Clicking a service item may trigger an **add-on dialog** (`.mil-modal-dialog__header`). See `meevo-addon-dialog.md` for the dismiss pattern. The add-on dialog MUST be dismissed before the "Next" button can proceed.

## Full Category → Service Selection Flow

```javascript
(() => {
  // 1. Click category (e.g., Massages)
  const items = Array.from(document.querySelectorAll('li'));
  const catItem = items.find(i => i.textContent?.trim() === 'Massages');
  if (catItem) {
    const div = catItem.querySelector('.category-item');
    if (div) {
      div.dispatchEvent(new MouseEvent('click', {bubbles: true, cancelable: true}));
    }
  }
  
  // Small delay to let sub-services render
  return 'clicked category, waiting for services...';
})();

// Then separately: click service item, dismiss add-on dialog, handle cookies
// See meevo-addon-dialog.md for the full add-on/cookie dismiss sequence
```