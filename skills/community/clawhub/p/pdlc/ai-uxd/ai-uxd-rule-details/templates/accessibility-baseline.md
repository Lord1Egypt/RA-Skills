<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-UXD
generatedVersion: "{version}"
source: "{upstream-doc-path}"
generatedOn: "{ISO-date}"
ownership: hybrid
---

# Accessibility Baseline

## Conformance Target

| Scope | Target | Standard |
|-------|--------|----------|
| Full product | Level {AA} | WCAG 2.2 |
| {specific area, if AAA} | Level {AAA} | WCAG 2.2 |

---

## Perceivable

### Text Alternatives (SC 1.1.1)
| Requirement | Implementation | Components Affected |
|-------------|---------------|-------------------|
| All meaningful images have descriptive alt text | `alt="{description}"` | Image, Avatar |
| Decorative images are hidden from AT | `aria-hidden="true"` or `alt=""` | Icon (decorative) |
| Complex visuals have extended description | `aria-describedby` or adjacent text | Charts, diagrams |
| Icon buttons have accessible names | `aria-label="{action}"` | Icon Button |

### Color & Contrast (SC 1.4.1, 1.4.3, 1.4.6, 1.4.11)
| Requirement | Standard | Verification Method |
|-------------|----------|-------------------|
| Text contrast ≥4.5:1 (normal <18px) | AA 1.4.3 | Token contrast table |
| Text contrast ≥3:1 (large ≥18px / bold ≥14px) | AA 1.4.3 | Token contrast table |
| UI component contrast ≥3:1 | AA 1.4.11 | Borders, icons, focus |
| Color not sole conveyor of information | AA 1.4.1 | Icon + text for errors |

### Adaptable (SC 1.3.1–1.3.5)
| Requirement | Implementation |
|-------------|---------------|
| Info and relationships conveyed through structure | Semantic HTML headings, lists, tables |
| Meaningful reading sequence | DOM order = visual order |
| Orientation not restricted | Works portrait AND landscape |
| Input purpose identifiable | `autocomplete` on form fields |

### Distinguishable (SC 1.4.4, 1.4.10, 1.4.12, 1.4.13)
| Requirement | Implementation |
|-------------|---------------|
| Text resizable to 200% without loss | Responsive/fluid layout |
| Content reflows at 320px width (no horizontal scroll) | Single-column at mobile |
| Text spacing adjustable | No fixed heights on text containers |
| Content on hover/focus dismissible, hoverable, persistent | Tooltips/popovers behavior |

---

## Operable

### Keyboard (SC 2.1.1–2.1.4)
| Requirement | Implementation |
|-------------|---------------|
| All functionality keyboard-accessible | Tab, Enter, Space, Escape, Arrows |
| No keyboard traps | Escape always exits |
| Keyboard shortcuts documented | If custom shortcuts exist |

### Focus (SC 2.4.3, 2.4.7, 2.4.11)
| Requirement | Implementation |
|-------------|---------------|
| Focus order logical and predictable | DOM matches visual layout |
| Focus indicator visible (≥2px, ≥3:1 contrast) | `shadow.focus` token |
| Focus not obscured by other content | Z-index management |

### Timing (SC 2.2.1–2.2.2)
| Requirement | Implementation |
|-------------|---------------|
| No essential time limits | Or: warn + option to extend |
| Moving/auto-updating content pausable | User control for carousels, live feeds |

### Motion (SC 2.3.1, 2.3.3)
| Requirement | Implementation |
|-------------|---------------|
| No flashes >3 per second | Animation constraints |
| Motion can be disabled | Respect `prefers-reduced-motion` |
| Non-essential motion off when preference set | CSS media query |

---

## Understandable

### Readable (SC 3.1.1–3.1.2)
| Requirement | Implementation |
|-------------|---------------|
| Page language declared | `<html lang="{locale}">` |
| Language changes identified | `lang` attribute on changed sections |

### Predictable (SC 3.2.1–3.2.4)
| Requirement | Implementation |
|-------------|---------------|
| No context change on focus alone | Focus never triggers navigation |
| No context change on input alone | Typing doesn't submit (except search) |
| Consistent navigation | Same nav on every page |
| Consistent identification | Same function = same name |

### Input Assistance (SC 3.3.1–3.3.4)
| Requirement | Implementation |
|-------------|---------------|
| Errors auto-identified | Highlight + message on invalid input |
| Labels / instructions present | Every input has visible label |
| Error suggestions provided | Suggest correct format |
| Error prevention (legal, financial, data) | Confirm before submit |

---

## Robust

### Compatible (SC 4.1.2–4.1.3)
| Requirement | Implementation |
|-------------|---------------|
| All components have name + role + value | ARIA where native semantics insufficient |
| Status messages programmatically determinable | `role="status"` or live regions for toasts |

---

## Keyboard Interaction Patterns

| Component | Tab | Enter | Space | Escape | Arrows | Home/End |
|-----------|-----|-------|-------|--------|--------|----------|
| Button | Focus | Activate | Activate | — | — | — |
| Link | Focus | Navigate | — | — | — | — |
| Input | Focus | — | — | — | — | — |
| Checkbox | Focus | — | Toggle | — | — | — |
| Radio group | Focus group | — | Select | — | Move within | First/Last |
| Select/Dropdown | Focus | Open | Open | Close | Navigate | First/Last |
| Tab list | Focus list | — | Activate tab | — | Switch tab | First/Last |
| Menu | Focus trigger | Select | Select | Close | Navigate | First/Last |
| Modal | Focus first | — | — | Close | — | — |
| Accordion | Focus header | Toggle | Toggle | — | — | — |
| Slider | Focus | — | — | — | Adjust value | Min/Max |

---

## Component Accessibility Matrix

| Component | ARIA Role | Required ARIA | Keyboard | Focus Visible | Touch Target |
|-----------|-----------|--------------|----------|:-------------:|:------------:|
| Button | `button` | — (native) | Enter/Space | ✅ 2px ring | 44×44px |
| Link | `link` | — (native) | Enter | ✅ 2px ring | 44×44px |
| Input | `textbox` | `aria-label` if no visible label | Tab | ✅ ring | — |
| Select | `combobox` | `aria-expanded`, `aria-activedescendant` | Full pattern | ✅ | 44×44px |
| Modal | `dialog` | `aria-modal`, `aria-labelledby` | Focus trap + Escape | ✅ first element | — |
| Toast | `status` | `aria-live="polite"` | — (auto-announce) | — | — |
| Alert | `alert` | `aria-live="assertive"` | — (auto-announce) | — | — |
| Tab | `tab` / `tabpanel` | `aria-selected`, `aria-controls` | Arrows + Enter | ✅ | 44×44px |
| Progress | `progressbar` | `aria-valuenow`, `aria-valuemin/max` | — | — | — |

---

## Testing Requirements

| Method | Coverage | Frequency |
|--------|----------|-----------|
| Automated (axe, Lighthouse) | ~30-40% of issues | Every build |
| Manual keyboard testing | All interactive components | Per component release |
| Screen reader (NVDA/VoiceOver) | Reading order, announcements, landmarks | Per feature |
| Zoom 200% | Layout integrity | Per responsive change |
| High contrast mode | Visibility of all elements | Per theme change |

---

## Exclusions (if any)

| SC | Exclusion Reason | Mitigation |
|----|-----------------|-----------|
| {criterion number} | {justified reason} | {alternative provided} |
