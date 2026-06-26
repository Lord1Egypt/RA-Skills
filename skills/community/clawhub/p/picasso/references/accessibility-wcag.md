# Accessibility & WCAG 2.2 Reference

## 1. ARIA Patterns Catalog

### Dialog / Modal
- `role="dialog"`, `aria-modal="true"`, `aria-labelledby` (title)
- Tab/Shift+Tab cycle within dialog (focus trap), Escape closes
- On open: focus first focusable element. On close: return focus to trigger.

```html
<div role="dialog" aria-modal="true" aria-labelledby="dlg-title">
  <h2 id="dlg-title">Confirm Delete</h2>
  <p>This action cannot be undone.</p>
  <button>Cancel</button>
  <button>Delete</button>
</div>
```

### Tabs
- `tablist` > `tab` + `tabpanel`
- `aria-selected="true|false"` on each tab, `aria-controls` linking tab to panel
- Left/Right arrows between tabs, Home/End to first/last

### Accordion
- Heading elements containing `<button>` triggers
- `aria-expanded="true|false"` on button, `aria-controls` pointing to content
- Enter/Space toggles section

### Combobox / Autocomplete
- `role="combobox"` on input, popup uses `listbox`
- `aria-expanded`, `aria-controls`, `aria-activedescendant`, `aria-autocomplete`
- Down Arrow opens/navigates popup, Escape closes, Enter selects

### Menu / Menubar
- `menu`/`menubar` > `menuitem`, `menuitemcheckbox`, `menuitemradio`
- `aria-haspopup`, `aria-expanded` on submenu triggers
- Arrow keys navigate, Enter/Space activates, Escape closes submenu

### Listbox
- `listbox` > `option`
- `aria-selected`, `aria-multiselectable` for multi-select
- Up/Down arrows, Home/End, type-ahead character navigation

### Tree View
- `tree` > `treeitem` (nested groups use `group` role)
- `aria-expanded` on parent nodes, `aria-level`, `aria-setsize`, `aria-posinset`
- Right expands/enters child, Left collapses/moves to parent

### Toolbar
- `toolbar` on container, `aria-orientation`
- Arrow keys between controls (roving tabindex), Tab moves out entirely

### Feed
- `feed` > `article` on each entry
- `aria-busy` while loading, `aria-setsize`/`aria-posinset` on articles
- Page Down/Up between articles

### Alert / Alert Dialog
- `role="alert"` (non-modal): implicitly `aria-live="assertive"`. No focus change.
- `role="alertdialog"` (modal): follows dialog focus trap pattern.

### Breadcrumb
- `<nav aria-label="Breadcrumb">` with ordered list
- `aria-current="page"` on current page link

### Disclosure
- `<button aria-expanded="false" aria-controls="content-id">` toggles content
- Enter/Space toggles expansion

---

## 2. Focus Management for SPAs

### Route Change Announcements
```html
<div aria-live="polite" class="sr-only" id="route-announcer"></div>
```
Update textContent on route change: "Products page loaded".

### Focus Restoration
Move focus to `<h1>` of new view (add `tabindex="-1"`) or main content landmark. On modal close, restore focus to trigger element.

### Skip Links
```html
<a href="#main" class="skip-link">Skip to main content</a>
<main id="main" tabindex="-1">...</main>
```

### Focus Trapping
Contain Tab/Shift+Tab within overlays. Use `inert` attribute on background content (modern browsers) or manage via JS. On last focusable element, Tab wraps to first.

### Roving Tabindex
Only one child has `tabindex="0"` at a time; all others `tabindex="-1"`. On arrow key, swap values and `.focus()`. Alternative: `aria-activedescendant` on container.

---

## 3. Accessible Forms

### Error Handling
```html
<input id="email" aria-invalid="true" aria-describedby="email-err" aria-required="true">
<span id="email-err" role="alert">Please enter a valid email address.</span>
```

- `aria-invalid="true"` on fields with errors.
- `aria-describedby` linking to error message.
- `role="alert"` for immediate screen reader announcement.
- On submit, move focus to first invalid field.

### Required Fields
Use both `required` (native) and `aria-required="true"`. Pair with visible asterisk + legend.

### Field Descriptions
```html
<label for="pw">Password</label>
<input id="pw" type="password" aria-describedby="pw-hint">
<p id="pw-hint">Must be at least 8 characters with one number.</p>
```

### Autocomplete Attributes
Use `autocomplete` values: `name`, `email`, `tel`, `street-address`, `postal-code`, `cc-number`, etc.

### Group Labeling
```html
<fieldset>
  <legend>Payment Method</legend>
  <label><input type="radio" name="pay" value="card"> Credit Card</label>
  <label><input type="radio" name="pay" value="paypal"> PayPal</label>
</fieldset>
```

### Accessible Date Pickers
Prefer native `<input type="date">`. For custom: `role="grid"` calendar, arrow key navigation, Enter to select, Escape to close, label each cell with full date.

---

## 4. WCAG 2.2 New Criteria

### Target Size Minimum (2.5.8 -- Level AA)
All interactive targets must be at least **24x24 CSS pixels**.

```css
button, a, input, select, [role="button"] {
  min-width: 24px;
  min-height: 24px;
}
```

### Dragging Alternatives (2.5.7 -- Level AA)
Every drag-and-drop operation must have a single-pointer alternative (click/tap). Sortable lists must also support "Move Up"/"Move Down" buttons.

### Focus Appearance (2.4.11 -- Level AA)
Focus indicators: minimum **2px perimeter outline** with **3:1 contrast ratio** between focused and unfocused states.

```css
:focus-visible {
  outline: 2px solid #005fcc;
  outline-offset: 2px;
}
```

### Consistent Help (3.2.6 -- Level A)
Help mechanisms must appear in the **same relative order** across all pages.

---

## 5. Screen Reader Dynamic Content

### aria-live Regions
```html
<div aria-live="polite" aria-atomic="true">3 results found</div>
<div aria-live="assertive">Session expiring in 30 seconds</div>
```
- `polite`: announced after current speech.
- `assertive`: interrupts (use sparingly).
- `aria-atomic="true"`: reads entire region, not just changed text.

### Status Messages (WCAG 4.1.3)
```html
<div role="status">File uploaded successfully.</div>
```

### Loading States
```html
<div role="status" aria-live="polite">Loading results...</div>
<table aria-busy="true">...</table>
```
Set `aria-busy="true"` during update, `false` when complete.

### Progress Updates
```html
<div role="progressbar" aria-valuenow="65" aria-valuemin="0" aria-valuemax="100"
     aria-label="Upload progress">65%</div>
```

---

## 6. Accessible Data Tables

### Complex Headers
```html
<th id="q1" scope="col">Q1</th>
<th id="revenue" scope="row">Revenue</th>
<td headers="q1 revenue">$1.2M</td>
```

### Sortable Columns
```html
<th aria-sort="ascending" scope="col">
  <button>Name <span aria-hidden="true">&uarr;</span></button>
</th>
```
Values: `ascending`, `descending`, `none`. Only one column sorted at a time.

### Expandable Rows
Parent row: `aria-expanded="true|false"`. Use `aria-level`, `aria-setsize`, `aria-posinset` for treegrid.

### Responsive Tables
- **Reflow:** Transform cells into stacked blocks with `data-label` + CSS `::before` for headers.
- **Scroll:** `tabindex="0"`, `role="region"`, `aria-label="Scrollable table"`.

---

## 7. Accessible Drag and Drop

### Keyboard Alternatives (WCAG 2.5.7)
```html
<li aria-roledescription="sortable item">
  Item A
  <button aria-label="Move Item A up">Up</button>
  <button aria-label="Move Item A down">Down</button>
</li>
```

### Live Region Announcements
```html
<div aria-live="assertive" class="sr-only" id="dnd-status"></div>
```
- On grab: "Grabbed Item A. Current position 2 of 5."
- On move: "Item A moved to position 3 of 5."
- On drop: "Item A dropped at position 3 of 5."
- On cancel: "Reorder cancelled. Item A returned to position 2."

### Modern Pattern
`aria-grabbed`/`aria-dropeffect` are deprecated. Use `aria-roledescription="draggable"`, `aria-pressed`/`aria-selected` for state, and live regions for announcements. Space/Enter to grab/drop, arrow keys to reposition, Escape to cancel.
