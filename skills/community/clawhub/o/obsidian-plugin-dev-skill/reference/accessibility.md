# Accessibility (A11y) — MANDATORY

All accessibility requirements are **mandatory** for community plugin submission. Plugins that fail accessibility checks will be rejected.

## Keyboard Navigation (MANDATORY)

Every interactive element must be reachable and operable via keyboard.

### Interactive Elements Checklist

| Element | Tab Accessible | Enter/Space Action |
|---------|---------------|-------------------|
| `<button>` | ✅ automatic | ✅ automatic |
| `<input>` | ✅ automatic | ✅ automatic |
| `<select>` | ✅ automatic | ✅ automatic |
| Custom clickable `<div>` | ❌ must add `tabIndex={0}` | ❌ must add keydown handler |
| Custom clickable `<span>` | ❌ must add `tabIndex={0}` | ❌ must add keydown handler |
| Icon-only buttons | ✅ if `<button>` | ✅ automatic |

### Custom Interactive Elements

```typescript
// ✅ MANDATORY pattern for custom interactive elements
const card = containerEl.createDiv({ cls: 'my-plugin-card' })
card.tabIndex = 0
card.setAttribute('role', 'button')
card.setAttribute('aria-label', 'Open note details')

card.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' || e.key === ' ') {
    e.preventDefault()
    handleCardClick()
  }
})
```

### Focus Trapping (for custom panels/modals)

```typescript
function trapFocus(container: HTMLElement) {
  const focusable = container.querySelectorAll<HTMLElement>(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  )
  const first = focusable[0]
  const last = focusable[focusable.length - 1]

  container.addEventListener('keydown', (e) => {
    if (e.key === 'Tab') {
      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault()
        last.focus()
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault()
        first.focus()
      }
    }
  })
}
```

## ARIA Labels (MANDATORY)

All icon-only buttons and controls **must** have ARIA labels.

```typescript
// ✅ Icon-only button with ARIA label
const closeBtn = headerEl.createEl('button')
closeBtn.setAttribute('aria-label', 'Close dialog')
closeBtn.createEl('span', { cls: 'lucide-x' })

// ✅ With tooltip position
const settingsBtn = toolbarEl.createEl('button')
settingsBtn.setAttribute('aria-label', 'Open settings')
settingsBtn.setAttribute('data-tooltip-position', 'top')
settingsBtn.createEl('span', { cls: 'lucide-settings' })

// ✅ Complex widgets
const list = containerEl.createEl('ul')
list.setAttribute('role', 'listbox')
list.setAttribute('aria-label', 'Available files')
list.setAttribute('aria-activedescendant', 'item-0')
```

### Common ARIA Roles

| Role | Use Case |
|------|----------|
| `button` | Custom clickable elements |
| `listbox` | Dropdown/select-like lists |
| `option` | Items in a listbox |
| `tab` / `tabpanel` | Tab interfaces |
| `dialog` | Custom modal/panel |
| `status` | Live status updates |
| `progressbar` | Progress indicators |
| `menu` / `menuitem` | Context menus |

## Focus Indicators (MANDATORY)

All interactive elements must have visible focus indicators.

```css
/* ✅ MANDATORY — use :focus-visible with Obsidian CSS variables */
.my-plugin-button:focus-visible {
  outline: 2px solid var(--interactive-accent);
  outline-offset: 2px;
}

/* ✅ For custom card elements */
.my-plugin-card:focus-visible {
  outline: 2px solid var(--interactive-accent);
  outline-offset: 2px;
  box-shadow: 0 0 0 4px rgba(var(--interactive-accent-rgb), 0.2);
}

/* ❌ NEVER do this */
.my-plugin-button:focus {
  outline: none;  /* REMOVING FOCUS = REJECTION */
}
```

**Key rules:**
- Use `:focus-visible` (not `:focus`) — shows focus ring only for keyboard navigation
- Use `var(--interactive-accent)` for the outline color
- Minimum `outline-offset: 2px` for visibility
- Never remove focus outlines

## Touch Targets (MANDATORY)

All interactive elements must be at least **44×44px** on mobile.

```css
/* ✅ MANDATORY minimum touch target */
.my-plugin-button {
  min-width: 44px;
  min-height: 44px;
  padding: var(--size-4-2);  /* 8px padding helps reach 44px */
}

/* ✅ For icon-only buttons */
.my-plugin-icon-btn {
  width: 44px;
  height: 44px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

/* ✅ Verify with mobile testing */
.is-mobile .my-plugin-button {
  min-width: 44px;
  min-height: 44px;
}
```

## Screen Reader Support

### Live Regions

```typescript
// Announce dynamic content changes
const status = containerEl.createDiv()
status.setAttribute('role', 'status')
status.setAttribute('aria-live', 'polite')

// Update content — screen reader announces it
status.setText('3 files found')
```

### Labels for Form Controls

```typescript
// ✅ Always associate labels with inputs
const setting = new Setting(containerEl)
  .setName('API key')          // visible label
  .setDesc('Your API key')     // description
  .addText((text) => text
    .setPlaceholder('sk-...')
    .setValue(this.plugin.settings.apiKey)
  )
// Setting class automatically handles label association

// ✅ Manual label association
const label = containerEl.createEl('label', { text: 'Search query' })
const input = containerEl.createEl('input', { type: 'text' })
label.setAttribute('for', 'search-input')
input.id = 'search-input'
```

## Color Contrast

Use Obsidian CSS variables — they guarantee proper contrast ratios.

| Variable Pair | Contrast | Use |
|--------------|----------|-----|
| `var(--text-normal)` on `var(--background-primary)` | AAA | Primary text |
| `var(--text-muted)` on `var(--background-primary)` | AA | Secondary text |
| `var(--text-faint)` on `var(--background-primary)` | Low | Avoid for important info |
| `var(--interactive-accent)` on `var(--text-on-accent)` | AAA | Buttons, accents |

**Never hardcode colors** — always use CSS variables to respect user themes and maintain contrast.

## Accessibility Audit Checklist

Before submission, verify:

- [ ] Can you navigate the entire plugin UI using only Tab, Enter, Space, and Escape?
- [ ] Do all icon-only buttons have `aria-label`?
- [ ] Is `:focus-visible` styled on all interactive elements?
- [ ] Are touch targets at least 44×44px?
- [ ] Can you use the plugin without a mouse?
- [ ] Do all dynamic updates use `aria-live` regions?
- [ ] Are form controls properly labeled?
- [ ] Does the plugin work with screen readers?
- [ ] Is color contrast sufficient using Obsidian CSS variables?

## Testing

1. **Keyboard test**: Tab through all interactive elements. Every one should receive focus and respond to Enter/Space.
2. **Screen reader test**: Enable VoiceOver (macOS) or Narrator (Windows) and navigate the plugin.
3. **Mobile test**: Test on Obsidian mobile — all touch targets should be tappable.
4. **High contrast**: Enable high contrast mode and verify UI remains usable.
