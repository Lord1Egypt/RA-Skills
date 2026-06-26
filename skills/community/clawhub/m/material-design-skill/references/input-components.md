---
name: Input Components
description: Material Design 3 input components including Buttons, Text Fields, Chips, Segmented Buttons, Switches, Checkboxes, and Radio Buttons
source: https://m3.material.io/components/buttons/overview
---

# Input Components

## Buttons

**Description:** Buttons prompt most actions in a UI.

**Source:** https://m3.material.io/components/buttons/overview

### Variants

| Variant | Description |
|---------|-------------|
| Default | Standard button actions |
| Toggle | Selection functionality |

### Color Styles

| Style | Use Case |
|-------|----------|
| Elevated | Secondary emphasis |
| Filled | Primary emphasis |
| Tonal | Moderate emphasis |
| Outlined | Tertiary emphasis |
| Text | Minimal emphasis |

### Sizes

| Size | Description |
|------|-------------|
| Extra Small | Compact spaces |
| Small (Default) | Standard compact |
| Medium | Standard |
| Large | Prominent |
| Extra Large | Maximum emphasis |

### Shapes
- Round
- Square (shape morphs when pressed/selected)

### Platform Availability

| Platform | Resource | Status |
|----------|----------|--------|
| Design | Figma Design Kit | Available |
| Flutter | Flutter | Available |
| Android | Jetpack Compose | Available |
| Android | Jetpack Compose: Expressive | Available |
| Android | MDC-Android | Available |
| Android | MDC-Android: Expressive | Available |
| Web | Web | Available |

### Key Updates (M3 Expressive)
- Wider variety of shapes and sizes
- Toggle functionality added
- Shape morphs when selected
- New small button padding: 16dp (recommended)

---

## Text Fields

**Description:** Text fields let users enter text into a UI.

**Source:** https://m3.material.io/components/text-fields/overview

### Variants

| Variant | Description |
|---------|-------------|
| Filled | Filled background style |
| Outlined | Outlined border style |

### Platform Availability

| Platform | Resource | Status |
|----------|----------|--------|
| Design | Figma Design Kit | Available |
| Flutter | Flutter | Available |
| Android | Jetpack Compose | Available |
| Android | MDC-Android | Available |
| Web | Web | Available |

### Design Guidelines
- Make text fields look interactive
- State (blank, with input, error, etc.) should be visible at a glance
- Keep labels and error messages brief and easy to act on
- Commonly appear in forms and dialogs

---

## Chips

**Description:** Chips help people enter information, make selections, filter content, or trigger actions.

**Source:** https://m3.material.io/components/chips/overview

### Variants

| Variant | Description |
|---------|-------------|
| Assist | Trigger actions |
| Filter | Filter content |
| Input | Enter information |
| Suggestion | Provide suggestions |

### Platform Availability

| Platform | Resource | Status |
|----------|----------|--------|
| Design | Figma Design Kit | Available |
| Flutter | Flutter | Available |
| Android | Jetpack Compose | Available |
| Android | MDC-Android | Available |
| Web | Web | Available |

### Design Guidelines
- Use chips to show options for a specific context
- Chip elevation defaults to 0 but can be elevated if more visual separation is needed

### Key Updates (Aug 2024)
- Stroke color changed from outline to outline variant for improved visual hierarchy

---

## Segmented Buttons

**Description:** Segmented buttons help people select options, switch views, or sort elements.

**Source:** https://m3.material.io/components/segmented-buttons/overview

### Variants

| Variant | Description |
|---------|-------------|
| Single-select | Select one option |
| Multi-select | Select multiple options |

### Platform Availability

| Platform | Resource | Status |
|----------|----------|--------|
| Design | Figma Design Kit | Available |
| Flutter | Flutter | Available |
| Android | Jetpack Compose | Available |
| Android | MDC-Android | Available |
| Web | Web | Unavailable |

### Key Updates (M3 Expressive)
- **Deprecated:** Segmented buttons are no longer recommended
- **Replacement:** Use connected button group instead (same functionality, updated visual design)

### Design Guidelines
- Can contain icons, label text, or both
- Use for simple choices between 2-5 items
- For more items or complex choices, use chips instead

---

## Switches

**Description:** Switches toggle the selection of an item on or off.

**Source:** https://m3.material.io/components/switch/overview

### Platform Availability

| Platform | Resource | Status |
|----------|----------|--------|
| Design | Figma Design Kit | Available |
| Flutter | Flutter | Available |
| Android | Jetpack Compose | Available |
| Android | MDC-Android | Available |
| Web | Web | Available |

### Design Guidelines
- Use switches (not radio buttons) if items in a list can be independently controlled
- Best way to let people adjust settings
- Selection state (on/off) should be visible at a glance

### Key Differences from M2
- Taller and wider track
- Optional icon within switch handle
- New color mappings with dynamic color support
- Improved accessibility

---

## Checkboxes

**Description:** Checkboxes let users select one or more items from a list, or turn an item on or off.

**Source:** https://m3.material.io/components/checkbox/overview

### States

| State | Description |
|-------|-------------|
| Unselected | Default unchecked |
| Selected | Checked |
| Indeterminate | Partial selection |

### Platform Availability

| Platform | Resource | Status |
|----------|----------|--------|
| Design | Figma Design Kit | Available |
| Flutter | Flutter | Available |
| Android | Jetpack Compose | Available |
| Android | MDC-Android | Available |
| Web | Web | Available |

### Design Guidelines
- Use checkboxes when multiple options can be selected from a list
- Label should be scannable
- Selected items more prominent than unselected

### Key Updates (M3)
- New indeterminate states
- Error states for unselected, selected, and indeterminate
- New color mappings with dynamic color support

---

## Radio Buttons

**Description:** Radio buttons let people select one option from a set of options.

**Source:** https://m3.material.io/components/radio-button/overview

### Platform Availability

| Platform | Resource | Status |
|----------|----------|--------|
| Design | Figma Design Kit | Available |
| Flutter | Flutter | Available |
| Android | Jetpack Compose | Available |
| Android | MDC-Android | Available |
| Web | Web | Available |

### Design Guidelines
- Use radio buttons (not switches) when only one item can be selected from a list
- Label should be scannable
- Selected items more prominent than unselected

### Key Updates (M3)
- New color mappings with dynamic color support
