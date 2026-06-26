---
name: material-design-components-overview
description: Google Material Design 3 组件库总览，列出所有组件及平台可用性。
source: https://m3.material.io/components
---

# Material Design 3 Components Overview

Components are interactive building blocks for creating a user interface. They can be organized into categories based on their purpose: Action, containment, communication, navigation, selection, and text input.

---

## Platform Availability Key

| Platform | Badge |
|----------|-------|
| Flutter | F |
| Jetpack Compose | C |
| MDC-Android | A |
| Web | W |

**Note:** Some components have an "Expressive" variant (marked as F✗, C✗, A✗, W✗) which is a May 2025 update with expanded features and visual design changes. Components marked as "No longer recommended" are being phased out in favor of newer alternatives.

---

## Categories

### [Buttons](./buttons.md)

Buttons prompt most actions in a UI.

| Component | F | C | A | W | Status |
|-----------|---|---|---|---|--------|
| [Buttons](./buttons.md) | ✓ | ✓ | ✓ | ✓ | |
| [Button groups](./buttons.md#button-groups) | ✓ | ✓ | ✓ | ✓ | |
| [Extended FABs](./extended-fabs.md) | ✓ | ✓ | ✓ | ✓ | |
| [FAB menu](./fab-menu.md) | — | — | — | — | Not indexed |
| [Floating action buttons](./fabs.md) | ✓ | ✓ | ✓ | ✓ | |
| [Icon buttons](./icon-buttons.md) | — | — | — | — | Not indexed |
| [Segmented buttons](./segmented-buttons.md) | ✓ | ✓ | ✓ | ✗ | No longer recommended (use connected button group) |
| [Split buttons](./split-buttons.md) | — | — | — | — | Not indexed |

---

### [Date & Time Pickers](./date-pickers.md)

| Component | F | C | A | W | Status |
|-----------|---|---|---|---|--------|
| [Date pickers](./date-pickers.md) | — | — | — | — | Not indexed |
| [Time pickers](./time-pickers.md) | — | — | — | — | Not indexed |

---

### [Loading & Progress](./loading-progress.md)

| Component | F | C | A | W | Status |
|-----------|---|---|---|---|--------|
| [Loading indicators](./loading-indicators.md) | — | — | — | — | Not indexed |
| [Progress indicators](./progress-indicators.md) | — | — | — | — | Not indexed |

---

### [Navigation](./navigation.md)

| Component | F | C | A | W | Status |
|-----------|---|---|---|---|--------|
| [Navigation bar](./navigation-bar.md) | ✓ | ✓ | ✓ | ✗ | Flexible variant available (May 2025) |
| [Navigation drawer](./navigation-drawer.md) | ✓ | ✓ | ✓ | ✗ | No longer recommended (use expanded navigation rail) |
| [Navigation rail](./navigation-rail.md) | ✓ | ✓ | ✓ | ✗ | Expanded variant available (May 2025) |

---

### [Sheets](./sheets.md)

| Component | F | C | A | W | Status |
|-----------|---|---|---|---|--------|
| [Bottom sheets](./bottom-sheets.md) | ✓ | ✓ | ✓ | ✗ | |
| [Side sheets](./side-sheets.md) | — | — | — | — | Not indexed |

---

### [Selection](./selection.md)

| Component | F | C | A | W | Status |
|-----------|---|---|---|---|--------|
| [Checkboxes](./checkboxes.md) | ✓ | ✓ | ✓ | ✓ | |
| [Chips](./chips.md) | ✓ | ✓ | ✓ | ✓ | |
| [Radio buttons](./radio-buttons.md) | ✓ | ✓ | ✓ | ✓ | |
| [Switches](./switches.md) | ✓ | ✓ | ✓ | ✓ | |

---

### [Text Input](./text-fields.md)

| Component | F | C | A | W | Status |
|-----------|---|---|---|---|--------|
| [Text fields](./text-fields.md) | ✓ | ✓ | ✓ | ✓ | |

---

### [Containment](./containment.md)

| Component | F | C | A | W | Status |
|-----------|---|---|---|---|--------|
| [App bars (Top app bar)](./app-bars.md) | ✓ | ✓ | ✓ | ✗ | Flexible variants available (May 2025) |
| [Cards](./cards.md) | ✓ | ✓ | ✓ | ✗ | |
| [Dialogs](./dialogs.md) | ✓ | ✓ | ✓ | ✓ | |
| [Lists](./lists.md) | ✓ | ✓ | ✓ | ✓ | Expressive variant available (Dec 2025) |
| [Sheets](./sheets.md) | — | — | — | — | See Navigation category |

---

### [Communication](./communication.md)

| Component | F | C | A | W | Status |
|-----------|---|---|---|---|--------|
| [Snackbars](./snackbars.md) | ✓ | ✓ | ✓ | ✗ | |

---

## Component Status Summary

### Fully Available (All Platforms)
- Buttons
- Checkboxes
- Chips
- Dialogs
- Lists
- Radio buttons
- Switches
- Text fields

### Desktop/Web Unavailable
- App bars (Web ✗)
- Bottom sheets (Web ✗)
- Cards (Web ✗)
- FABs (Web ✗)
- Extended FABs (Web ✗)
- Navigation bar (Web ✗)
- Navigation drawer (Web ✗)
- Navigation rail (Web ✗)
- Segmented buttons (Web ✗)
- Snackbars (Web ✗)

### No Longer Recommended (M3 Expressive May 2025)
- Navigation drawer → Use expanded navigation rail
- Segmented buttons → Use connected button group
- Baseline navigation bar → Use flexible navigation bar
- Baseline navigation rail → Use collapsed/expanded navigation rail

### New Expressive Variants Available (May 2025)
- Lists: Expressive variant with segmented visual style
- Navigation bar: Flexible variant
- Navigation rail: Collapsed and expanded variants
- App bars: Medium flexible and large flexible variants

---

## M3 Expressive Update (May 2025)

The May 2025 M3 Expressive update introduced:
- New component sizes and shapes
- Toggle functionality for buttons
- Shape morphs when selected or pressed
- Expanded navigation components
- Improved typography

---

## Quick Reference Table

| Component | Category | F | C | A | W |
|-----------|----------|---|---|---|---|
| App bars | Containment | ✓ | ✓ | ✓ | ✗ |
| Bottom sheets | Sheets | ✓ | ✓ | ✓ | ✗ |
| Button groups | Buttons | ✓ | ✓ | ✓ | ✓ |
| Buttons | Buttons | ✓ | ✓ | ✓ | ✓ |
| Cards | Containment | ✓ | ✓ | ✓ | ✗ |
| Checkboxes | Selection | ✓ | ✓ | ✓ | ✓ |
| Chips | Selection | ✓ | ✓ | ✓ | ✓ |
| Date pickers | Date & Time | — | — | — | — |
| Dialogs | Containment | ✓ | ✓ | ✓ | ✓ |
| Extended FABs | Buttons | ✓ | ✓ | ✓ | ✓ |
| FAB menu | Buttons | — | — | — | — |
| Floating action buttons | Buttons | ✓ | ✓ | ✓ | ✓ |
| Icon buttons | Buttons | — | — | — | — |
| Lists | Containment | ✓ | ✓ | ✓ | ✓ |
| Loading indicators | Loading | — | — | — | — |
| Navigation bar | Navigation | ✓ | ✓ | ✓ | ✗ |
| Navigation drawer | Navigation | ✓ | ✓ | ✓ | ✗ |
| Navigation rail | Navigation | ✓ | ✓ | ✓ | ✗ |
| Progress indicators | Loading | — | — | — | — |
| Radio buttons | Selection | ✓ | ✓ | ✓ | ✓ |
| Segmented buttons | Buttons | ✓ | ✓ | ✓ | ✗ |
| Side sheets | Sheets | — | — | — | — |
| Snackbars | Communication | ✓ | ✓ | ✓ | ✗ |
| Split buttons | Buttons | — | — | — | — |
| Switches | Selection | ✓ | ✓ | ✓ | ✓ |
| Text fields | Text Input | ✓ | ✓ | ✓ | ✓ |
| Time pickers | Date & Time | — | — | — | — |

---

## Related References

- [Motion System](../foundations/motion-system.md)
- [Color Overview](../foundations/color-overview.md)
- [Typography Overview](../foundations/typography-overview.md)
- [Elevation Overview](../foundations/elevation-overview.md)
- [Shape Overview](../foundations/shape-overview.md)
