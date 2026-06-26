---
name: Display Components
description: Material Design 3 display components including FAB, Cards, Dialogs, Snackbars, Bottom Sheets, and Lists
source: https://m3.material.io/components/extended-fab/overview
---

# Display Components

## FAB (Floating Action Button)

**Description:** FABs provide quick access to primary actions on a screen. Use for the most common or important action.

**Source:** https://m3.material.io/components/extended-fab/overview

### Variants

| Variant | Size | Description |
|---------|------|-------------|
| Small | 56dp | Compact FAB |
| Medium | 80dp | Standard extended FAB |
| Large | 96dp | Large extended FAB |

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
- Extended FAB now has three sizes: small, medium, large with updated type styles
- Baseline extended FAB (56dp) no longer recommended
- Surface FAB no longer recommended
- Adjusted typography to be larger

---

## Cards

**Description:** Cards display content and actions about a single subject.

**Source:** https://m3.material.io/components/cards/overview

### Variants

| Variant | Description |
|---------|-------------|
| Elevated | Shadow elevation, on-surface background |
| Filled | Filled container background |
| Outlined | Outlined border, transparent background |

### Platform Availability

| Platform | Resource | Status |
|----------|----------|--------|
| Design | Figma Design Kit | Available |
| Flutter | Flutter | Available |
| Android | Jetpack Compose | Available |
| Android | MDC-Android | Available |
| Web | Web | Unavailable |

### Design Guidelines
- Use cards to contain related elements
- Contents can include images, headlines, supporting text, buttons, and lists
- Can also contain other components
- Flexible layouts based on contents

### Key Updates (M3)
- Lower elevation, no shadow by default
- New color mappings with dynamic color support

---

## Dialogs

**Description:** Dialogs provide important prompts in a user flow.

**Source:** https://m3.material.io/components/dialogs/overview

### Variants

| Variant | Description |
|---------|-------------|
| Basic | Standard dialog |
| Full-screen | Full-screen dialog |

### Platform Availability

| Platform | Resource | Status |
|----------|----------|--------|
| Design | Figma Design Kit | Available |
| Flutter | Flutter | Available |
| Android | Jetpack Compose | Available |
| Android | MDC-Android | Available |
| Web | Web | Available |

### Design Guidelines
- Use dialogs to make sure users act on information
- Should be dedicated to completing a single task
- Can display information relevant to the task
- Commonly used to confirm high-risk actions (e.g., deleting progress)

### Key Updates (M3)
- Greater padding for increased corner-radius and title size
- Option for custom basic dialog positioning
- Increased corner-radius
- Larger and darker headline
- New color mappings with dynamic color support

---

## Snackbars

**Description:** Snackbars show short updates about app processes at the bottom of the screen.

**Source:** https://m3.material.io/components/snackbar/overview

### Platform Availability

| Platform | Resource | Status |
|----------|----------|--------|
| Design | Figma Design Kit | Available |
| Flutter | Flutter | Available |
| Android | Jetpack Compose | Available |
| Android | MDC-Android | Available |
| Web | Web | Unavailable |

### Design Guidelines
- Should not interrupt user's experience
- Usually appear at the bottom of the UI
- Can disappear on their own (dismissive) or remain until user takes action (non-dismissive)

### Key Updates (M3)
- Clarified behavior: snackbars can be dismissive or non-dismissive
- New color mappings with dynamic color support

---

## Bottom Sheets

**Description:** Bottom sheets show secondary content anchored to the bottom of the screen.

**Source:** https://m3.material.io/components/bottom-sheets/overview

### Variants

| Variant | Description |
|---------|-------------|
| Standard | Standard bottom sheet |
| Modal | Modal bottom sheet |

### Platform Availability

| Platform | Resource | Status |
|----------|----------|--------|
| Design | Figma Design Kit | Available |
| Flutter | Flutter | Available |
| Android | Jetpack Compose | Available |
| Android | MDC-Android | Available |
| Web | Web | Unavailable |

### Design Guidelines
- Use in compact and medium window sizes
- Content should be additional or secondary (not main content)
- Can be dismissed to interact with main content

### Key Updates (M3)
- 28dp top corner radius
- New max-width of 640dp
- Optional drag handle with 48dp hit target
- New color mappings with dynamic color support

---

## Lists

**Description:** Lists help people find a specific item and act on it.

**Source:** https://m3.material.io/components/lists/overview

### List Item Elements (Customizable)
- Label text
- Supporting text
- Leading image
- Trailing icon

### Visual Styles

| Style | Description |
|-------|-------------|
| Standard | Standard list appearance |
| Segmented | New segmented visual style |

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

### Design Guidelines
- Order list items in logical ways (alphabetical, numerical, etc.)
- Keep items short and easy to scan
- Show icons, text, and actions in a consistent format

### Key Updates (M3 Expressive)
- New segmented visual style
- Improved selection treatment
- Flexible slots support
- Expressive list is recommended for new designs
- Baseline list still available
