# Tables and Forms Reference

## Table of Contents
1. Sortable Tables
2. Responsive Tables
3. Inline Editing
4. Multi-Select Patterns
5. Form Validation
6. Multi-Step Forms
7. Complex Inputs
8. Common Mistakes

---

## 1. Sortable Tables

```html
<table>
  <thead>
    <tr>
      <th aria-sort="ascending">
        <button>Name <span aria-hidden="true">↑</span></button>
      </th>
      <th aria-sort="none">
        <button>Date <span aria-hidden="true">↕</span></button>
      </th>
    </tr>
  </thead>
</table>
```

- Use `aria-sort` on `<th>`: `ascending`, `descending`, or `none`.
- Sort icon: `↑` ascending, `↓` descending, `↕` unsorted. Use `aria-hidden="true"` on the icon.
- Sortable headers must be `<button>` inside `<th>`, not clickable `<th>`.
- Default sort: most recent first for dates, alphabetical for names.

---

## 2. Responsive Tables

**Option A: Horizontal scroll** (preferred for data tables)

```css
.table-container {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  border: 1px solid var(--border);
  border-radius: 8px;
}

/* Fade edge to hint scrollability */
.table-container::after {
  content: '';
  position: absolute;
  right: 0;
  top: 0;
  bottom: 0;
  width: 40px;
  background: linear-gradient(to left, var(--surface-1), transparent);
  pointer-events: none;
}
```

**Option B: Stacked cards** (for simple tables on mobile)

```css
@media (max-width: 640px) {
  table, thead, tbody, th, td, tr { display: block; }
  thead { display: none; }
  td { padding: 8px 16px; text-align: right; }
  td::before {
    content: attr(data-label);
    float: left;
    font-weight: 600;
    color: var(--text-secondary);
  }
}
```

---

## 3. Inline Editing

Click to edit pattern: display text, click reveals input, blur/Enter saves.

```jsx
function EditableCell({ value, onSave }) {
  const [editing, setEditing] = useState(false);
  const [draft, setDraft] = useState(value);

  if (!editing) return (
    <span onClick={() => setEditing(true)} className="cursor-text hover:bg-surface-2 px-2 py-1 rounded">
      {value}
    </span>
  );

  return (
    <input
      value={draft}
      onChange={e => setDraft(e.target.value)}
      onBlur={() => { onSave(draft); setEditing(false); }}
      onKeyDown={e => { if (e.key === 'Enter') { onSave(draft); setEditing(false); } if (e.key === 'Escape') setEditing(false); }}
      autoFocus
      className="input-base w-full"
    />
  );
}
```

Show a subtle pencil icon on row hover. Use `opacity-0 group-hover:opacity-100` pattern.

---

## 4. Multi-Select Patterns

- **Checkbox column**: leftmost column, always visible.
- **Shift-click range select**: select from last checked to current.
- **Select all**: checkbox in header, toggles all visible (filtered) rows.
- **Bulk action bar**: appears when 1+ rows selected. Shows count + actions.

```jsx
<div className={`fixed bottom-4 left-1/2 -translate-x-1/2 bg-surface-2 rounded-xl px-4 py-2
  flex items-center gap-4 shadow-lg border border-border transition-transform
  ${selectedCount > 0 ? 'translate-y-0' : 'translate-y-[200%]'}`}>
  <span className="text-sm font-medium">{selectedCount} selected</span>
  <button className="btn-ghost text-sm">Export</button>
  <button className="btn-ghost text-sm text-red">Delete</button>
</div>
```

---

## 5. Form Validation

**When to validate:**

| Trigger | Use For |
|---|---|
| On blur | Email format, required fields, min/max length |
| On submit | All fields, server-side checks |
| Real-time (on change) | Password strength, username availability |
| Never on keystroke | Don't interrupt typing. Wait for blur or 500ms debounce. |

```jsx
<div className="space-y-1.5">
  <label htmlFor="email" className="text-sm font-medium">Email</label>
  <input
    id="email"
    type="email"
    aria-invalid={error ? "true" : undefined}
    aria-describedby={error ? "email-error" : undefined}
    className={`input-base ${error ? 'border-red' : ''}`}
  />
  {error && (
    <p id="email-error" role="alert" className="text-xs text-red flex items-center gap-1">
      <svg className="w-3.5 h-3.5" aria-hidden="true">...</svg>
      {error}
    </p>
  )}
</div>
```

Error messages: specific and helpful. "Enter a valid email" not "Invalid input."

---

## 6. Multi-Step Forms

Show a progress indicator. Allow back navigation. Validate per step, not all at once.

```jsx
<div className="flex items-center gap-2 mb-8">
  {steps.map((step, i) => (
    <Fragment key={i}>
      <div className={`flex items-center justify-center h-8 w-8 rounded-full text-sm font-bold
        ${i < currentStep ? 'bg-accent text-white' :
          i === currentStep ? 'border-2 border-accent text-accent' :
          'border border-border text-muted'}`}>
        {i < currentStep ? '✓' : i + 1}
      </div>
      {i < steps.length - 1 && (
        <div className={`flex-1 h-0.5 ${i < currentStep ? 'bg-accent' : 'bg-border'}`} />
      )}
    </Fragment>
  ))}
</div>
```

Rules:
- Save progress per step (don't lose data on back).
- Validate step before advancing (disable Next if invalid).
- Show step count: "Step 2 of 4".
- Allow clicking completed steps to go back.
- Final step: show summary before submit.

---

## 7. Complex Inputs

**Date pickers:** Use native `<input type="date">` first. Custom picker only if design requires it. Always allow manual text entry as fallback.

**File upload:** Show progress, preview (for images), allow removal.

```jsx
<label className="flex flex-col items-center gap-2 p-8 border-2 border-dashed border-border
  rounded-xl cursor-pointer hover:border-accent hover:bg-accent/5 transition-colors">
  <svg>...</svg>
  <span className="text-sm text-secondary">Drop files or click to upload</span>
  <input type="file" className="hidden" onChange={handleUpload} />
</label>
```

**Address autocomplete:** Use Google Places API or similar. Show suggestions in a dropdown. Parse into structured fields (street, city, state, zip).

---

## 8. Common Mistakes

- **Sortable `<th>` without `<button>`.** Clicking a `<th>` isn't keyboard accessible.
- **No `aria-sort` on sortable columns.** Screen readers can't announce sort state.
- **Validating on every keystroke.** Annoying. Use blur or 500ms debounce.
- **Error messages without `role="alert"`.** Screen readers won't announce them.
- **Multi-step form losing data on back.** Save each step's state.
- **No horizontal scroll hint on tables.** Users don't know content is hidden. Add fade gradient.
- **Custom date picker without text input fallback.** Some users prefer typing dates.
- **Select all selecting ALL rows, not just filtered.** Only select what's visible.
- **Labels as placeholder text.** Labels must be visible above the input, always.
