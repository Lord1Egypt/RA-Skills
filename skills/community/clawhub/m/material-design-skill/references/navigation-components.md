---
name: Navigation Components
description: Material Design 3 navigation components including Navigation Bar, Navigation Drawer, Navigation Rail, and App Bars
source: https://m3.material.io/components/navigation-bar/overview
---

# Navigation Components

## Navigation Bar

**Description:** Navigation bars let people switch between UI views on smaller devices. Use in compact or medium window sizes with 3-5 destinations of equal importance.

**Source:** https://m3.material.io/components/navigation-bar/overview

### Variants

| Variant | Description |
|---------|-------------|
| Flexible (New) | Shorter height, supports horizontal navigation items in medium windows |
| Baseline (Legacy) | No longer recommended |

### Platform Availability

| Platform | Resource | Status |
|----------|----------|--------|
| Design | Figma Design Kit | Available |
| Flutter | Flutter | Available |
| Android | Jetpack Compose | Available |
| Android | Jetpack Compose: Expressive | Available |
| Android | MDC-Android | Available |
| Android | MDC-Android: Expressive | Available |
| Web | Web | Unavailable |

### Key Updates (M3 Expressive)
- Active label color changed from `on-surface-variant` to `secondary`
- Flexible navigation bar is shorter and supports horizontal nav items

---

## Navigation Drawer

**Description:** Navigation drawers let people switch between UI views on larger devices.

**Source:** https://m3.material.io/components/navigation-drawer/overview

### Variants

| Variant | Window Size |
|---------|-------------|
| Standard | Expanded, large, extra-large |
| Modal | Compact and medium |

### Platform Availability

| Platform | Resource | Status |
|----------|----------|--------|
| Design | Figma Design Kit | Available |
| Flutter | Flutter | Available |
| Android | Jetpack Compose | Available |
| Android | MDC-Android | Available |
| Web | Web | Unavailable |

### Key Updates (M3 Expressive)
- **Deprecated:** Navigation drawer is no longer recommended
- **Replacement:** Use expanded navigation rail instead, which has mostly the same functionality

---

## Navigation Rail

**Description:** Navigation rails let people switch between UI views on mid-sized devices. Use in medium, expanded, large, or extra-large window sizes with 3-7 destinations plus an optional FAB.

**Source:** https://m3.material.io/components/navigation-rail/overview

### Variants

| Variant | Description |
|---------|-------------|
| Collapsed | Replaces baseline nav rail |
| Expanded | Replaces navigation drawer |

### Platform Availability

| Platform | Resource | Status |
|----------|----------|--------|
| Design | Figma Design Kit | Available |
| Flutter | Flutter | Available |
| Android | Jetpack Compose | Available |
| Android | Jetpack Compose: Expressive | Available |
| Android | MDC-Android | Available |
| Android | MDC-Android: Expressive | Available |
| Web | Web | Unavailable |

### Key Updates (M3 Expressive)
- Collapsed and expanded rail introduced to replace baseline nav rail
- Expanded rail meant to replace navigation drawer

---

## App Bars

**Description:** App bars are placed at the top of the screen to help people navigate through a product. Display labels and page navigation controls.

**Source:** https://m3.material.io/components/app-bars/overview

### Variants

| Variant | Description |
|---------|-------------|
| Small | Standard app bar |
| Medium Flexible (New) | Replaces medium, with flexible improvements |
| Large Flexible (New) | Replaces large, with flexible improvements |
| Search App Bar (New) | Supports icons inside/outside search bar, centered text |

### Platform Availability

| Platform | Resource | Status |
|----------|----------|--------|
| Design | Figma Design Kit | Available |
| Flutter | Flutter | Available |
| Android | Jetpack Compose | Available |
| Android | Jetpack Compose: Expressive | Available |
| Android | MDC-Android | Available |
| Android | MDC-Android: Expressive | Available |
| Web | Web | Unavailable |

### Key Updates (M3 Expressive)
- Search app bar supports icons inside/outside and centered text
- Opens search view component when selected
- Medium and large flexible app bars replace medium/large (no longer recommended)
- Small app bar updated with flexible improvements

### Design Guidelines
- Focus on describing the current page
- Provide 1-2 essential actions
- On scroll, apply fill color to separate from body content
- Can animate on/off screen with another bar of controls
