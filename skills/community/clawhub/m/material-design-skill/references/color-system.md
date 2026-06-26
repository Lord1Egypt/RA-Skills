---
name: material-design-color
description: Google Material Design 3 色彩系统完整参考，覆盖动态配色、色板构建、主题配置。
source: https://m3.material.io/styles/color/overview
---

# Material Design 3 Color System Reference

> 官方文档: https://m3.material.io/styles/color/overview

## Overview

The Material 3 color system provides:

- **Built-in set of accessible color relationships** - colors designed to work together with proper contrast
- **26+ color roles** mapped to Material Components
- **Built-in dark theme colors** - automatically generated from baseline scheme
- **Static baseline color scheme** - default colors assigned to each role
- **Dynamic color features** - user-generated and content-based color schemes (Material You)

### Baseline vs Dynamic Color Schemes

| Aspect | Baseline (Static) | Dynamic |
|--------|------------------|---------|
| Colors change based on wallpaper | No | Yes |
| Personalized experience | No | Yes |
| User-controlled contrast | No | Yes |
| Accessible contrast | Yes | Yes |
| M2 compatibility | Yes | No |

---

## Color Roles System

### Core Color Roles

| Role | Purpose | Light Theme Default | Dark Theme Default |
|------|---------|---------------------|-------------------|
| **Primary** | Main brand color, key actions | #6750A4 | #D0BCFF |
| **On Primary** | Text/icons on primary | #FFFFFF | #381E72 |
| **Primary Container** | Secondary primary surfaces | #EADDFF | #4F378B |
| **On Primary Container** | Text on primary container | #21005D | #EADDFF |
| **Secondary** | Supporting UI elements | #625B71 | #CCC2DC |
| **On Secondary** | Text/icons on secondary | #FFFFFF | #332D41 |
| **Secondary Container** | Tertiary secondary surfaces | #E8DEF8 | #4A4458 |
| **On Secondary Container** | Text on secondary container | #1D192B | #E8DEF8 |
| **Tertiary** | Accent color for variety | #7D5260 | #EFB8C8 |
| **On Tertiary** | Text/icons on tertiary | #FFFFFF | #492532 |
| **Tertiary Container** | Tertiary surface color | #FFD8E4 | #633B48 |
| **On Tertiary Container** | Text on tertiary container | #31111D | #FFD8E4 |
| **Error** | Error states, destructive actions | #B3261E | #F2B8B5 |
| **On Error** | Text/icons on error | #FFFFFF | #601410 |
| **Error Container** | Error surface color | #F9DEDC | #8C1D18 |
| **On Error Container** | Text on error container | #410E0B | #F9DEDC |
| **Background** | Page background | #FFFBFE | #1C1B1F |
| **On Background** | Text on background | #1C1B1F | #E6E1E5 |
| **Surface** | Card/component backgrounds | #FFFBFE | #1C1B1F |
| **On Surface** | Text on surface | #1C1B1F | #E6E1E5 |
| **Surface Variant** | Subtle surface differentiation | #E7E0EC | #49454F |
| **On Surface Variant** | Text on surface variant | #49454F | #CAC4D0 |
| **Outline** | Borders, dividers | #79747E | #938F99 |
| **Outline Variant** | Subtle borders | #CAC4D0 | #49454F |
| **Inverse Surface** | Surfaces for inverse colors | #313033 | #E6E1E5 |
| **Inverse On Surface** | Text for inverse surface | #F4EFF4 | #313033 |
| **Inverse Primary** | Inverse of primary | #D0BCFF | #6750A4 |
| **Surface Tint** | Tint applied to surfaces | #6750A4 | #D0BCFF |

### Surface Roles

| Role | Usage |
|------|-------|
| Surface | Default card/component background |
| Surface Container | Container-level surfaces (closer to outline) |
| Surface Container Low | Lower elevation containers |
| Surface Container High | Higher elevation containers |
| Surface Container Highest | Highest elevation containers |
| Surface Container Center | Center-height containers |

---

## Dynamic Color (Material You)

### Overview

Dynamic color changes UI colors based on:
- **User-generated source**: Wallpaper on Android
- **Content-based source**: In-app content (album art, book covers, photos)

### User-Generated Color (Wallpaper-based)

```
Source: User's wallpaper on Android
Availability: Android 12+ (API 31+)
```

**When to use:**
- Products wanting personalized experience
- Showcase latest Material features
- Consumer apps benefiting from personalization

### Content-Based Color

```
Source: In-app content (images, media)
Availability: Android 12+ (API 31+), Flutter, Web
```

**When to use:**
- Content is front-and-center (media players, readers)
- Team can do advanced customization
- Contained screen elements adjacent to source image

### Multiple Color Sources

Products can combine multiple schemes:
- Baseline + User-generated
- Baseline + Content-based
- User-generated + Content-based

---

## Color Scheme Construction

### Light Theme Construction

```
Primary → Primary Container (lighter) → On Primary Container
Primary → Surface Tint (for subtle tinting)

Secondary → Secondary Container (lighter) → On Secondary Container
Tertiary → Tertiary Container (lighter) → On Tertiary Container

Error → Error Container (lighter) → On Error Container
```

### Dark Theme Construction

The dark theme is generated from the light theme:
- Primary tones shift darker
- Surface colors become darker
- Contrast is maintained for accessibility

### Contrast Levels

Color roles support **three levels of contrast** (May 2025 update):
- Default
- Medium (increased)
- High (maximum)

Users can select their preferred contrast level in system settings.

---

## Platform-Specific Implementation

### Flutter / Dart

```dart
import 'package:flutter/material.dart';

// Using Material 3 with dynamic color
MaterialApp(
  theme: ThemeData(
    colorScheme: ColorScheme.fromSeed(
      seedColor: Color(0x6750A4), // Primary seed color
      brightness: Brightness.light,
    ),
    useMaterial3: true,
  ),
);

// Dynamic color on Android 12+
MaterialApp(
  theme: ThemeData(
    colorScheme: ColorScheme.fromDynamicBrightness(
      brightness: Brightness.light,
    ),
    useMaterial3: true,
  ),
);

// Manual M3 color scheme
final colorScheme = ColorScheme(
  primary: Color(0x6750A4),
  onPrimary: Color(0xFFFFFFFF),
  primaryContainer: Color(0xFFEADDFF),
  onPrimaryContainer: Color(0xFF21005D),
  // ... other roles
);
```

### Jetpack Compose

```kotlin
import androidx.compose.material3.*
import androidx.compose.ui.graphics.Color

// Using dynamic color (Android 12+)
val colorScheme = when {
    dynamicColor && Build.VERSION.SDK_INT >= Build.VERSION_CODES.S -> {
        val context = ContextAmbient.current
        if (darkTheme) dynamicDarkColorScheme(context) else dynamicLightColorScheme(context)
    }
    else -> lightColorScheme() // or custom scheme
}

// Baseline color scheme
private val LightColorScheme = lightColorScheme(
    primary = Color(0x6750A4),
    onPrimary = Color(0xFFFFFFFF),
    primaryContainer = Color(0xFFEADDFF),
    onPrimaryContainer = Color(0xFF21005D),
    secondary = Color(0x625B71),
    onSecondary = Color(0xFFFFFFFF),
    secondaryContainer = Color(0xE8DEF8),
    onSecondaryContainer = Color(0xFF1D192B),
    tertiary = Color(0x7D5260),
    onTertiary = Color(0xFFFFFFFF),
    tertiaryContainer = Color(0xFFD8E4),
    onTertiaryContainer = Color(0xFF31111D),
    error = Color(0xB3261E),
    onError = Color(0xFFFFFFFF),
    errorContainer = Color(0xF9DEDC),
    onErrorContainer = Color(0xFF410E0B),
    background = Color(0xFFFBFE),
    onBackground = Color(0xFF1C1B1F),
    surface = Color(0xFFFBFE),
    onSurface = Color(0xFF1C1B1F),
    surfaceVariant = Color(0xFFE7E0EC),
    onSurfaceVariant = Color(0xFF49454F),
    outline = Color(0xFF79747E),
    outlineVariant = Color(0xFFCAC4D0),
)
```

### Android (XML / Views)

```xml
<!-- themes.xml -->
<resources>
    <style name="Theme.MyApp" parent="Theme.Material3.DayNight.NoActionBar">
        <!-- Primary colors -->
        <item name="colorPrimary">@color/m3_sys_color_primary</item>
        <item name="colorOnPrimary">@color/m3_sys_color_on_primary</item>
        <item name="colorPrimaryContainer">@color/m3_sys_color_primary_container</item>
        <item name="colorOnPrimaryContainer">@color/m3_sys_color_on_primary_container</item>
        
        <!-- Secondary colors -->
        <item name="colorSecondary">@color/m3_sys_color_secondary</item>
        <item name="colorOnSecondary">@color/m3_sys_color_on_secondary</item>
        
        <!-- Background / Surface -->
        <item name="android:colorBackground">@color/m3_sys_color_background</item>
        <item name="colorOnBackground">@color/m3_sys_color_on_background</item>
        <item name="colorSurface">@color/m3_sys_color_surface</item>
        <item name="colorOnSurface">@color/m3_sys_color_on_surface</item>
    </style>
</resources>

<!-- colors.xml (baseline values) -->
<resources>
    <color name="m3_sys_color_primary">#6750A4</color>
    <color name="m3_sys_color_on_primary">#FFFFFF</color>
    <color name="m3_sys_color_primary_container">#EADDFF</color>
    <color name="m3_sys_color_on_primary_container">#21005D</color>
</resources>
```

### CSS / Web

```css
/* CSS Custom Properties for M3 Color System */
:root {
  /* Primary */
  --md-sys-color-primary: #6750A4;
  --md-sys-color-on-primary: #FFFFFF;
  --md-sys-color-primary-container: #EADDFF;
  --md-sys-color-on-primary-container: #21005D;
  
  /* Secondary */
  --md-sys-color-secondary: #625B71;
  --md-sys-color-on-secondary: #FFFFFF;
  --md-sys-color-secondary-container: #E8DEF8;
  --md-sys-color-on-secondary-container: #1D192B;
  
  /* Tertiary */
  --md-sys-color-tertiary: #7D5260;
  --md-sys-color-on-tertiary: #FFFFFF;
  --md-sys-color-tertiary-container: #FFD8E4;
  --md-sys-color-on-tertiary-container: #31111D;
  
  /* Error */
  --md-sys-color-error: #B3261E;
  --md-sys-color-on-error: #FFFFFF;
  --md-sys-color-error-container: #F9DEDC;
  --md-sys-color-on-error-container: #410E0B;
  
  /* Background & Surface */
  --md-sys-color-background: #FFFBFE;
  --md-sys-color-on-background: #1C1B1F;
  --md-sys-color-surface: #FFFBFE;
  --md-sys-color-on-surface: #1C1B1F;
  --md-sys-color-surface-variant: #E7E0EC;
  --md-sys-color-on-surface-variant: #49454F;
  
  /* Outline */
  --md-sys-color-outline: #79747E;
  --md-sys-color-outline-variant: #CAC4D0;
}

/* Dark theme */
@media (prefers-color-scheme: dark) {
  :root {
    --md-sys-color-primary: #D0BCFF;
    --md-sys-color-on-primary: #381E72;
    --md-sys-color-primary-container: #4F378B;
    --md-sys-color-on-primary-container: #EADDFF;
    
    /* ... dark theme values */
  }
}
```

---

## Advanced Customizations

### Applying Colors

1. **Combine multiple color schemes**
   - Baseline + Dynamic content-based
   - Multiple schemes in same app experience

2. **Remap colors to components**
   - Override component's default color mapping
   - Apply colors to custom components

### Defining New Colors

1. **Static colors in dynamic schemes**
   - Useful for semantic colors (brand colors that shouldn't change)
   - Mark specific colors as non-dynamic

2. **Custom color roles**
   - Define new roles beyond the 26+ standard roles
   - Extend the color scheme

### Adjusting Colors

1. **Custom baseline scheme**
   - Input your own colors to define baseline

2. **Custom dynamic scheme**
   - Define algorithm rules for custom dynamic output

3. **Apply dynamic color to imagery**
   - Tint imagery based on dynamic color scheme

---

## Accessibility Requirements

### Contrast Ratios

| Element Type | Minimum Ratio (AA) | Recommended (AAA) |
|--------------|--------------------|--------------------|
| Normal text (< 18pt / < 14pt bold) | 4.5:1 | 7:1 |
| Large text (≥ 18pt / ≥ 14pt bold) | 3:1 | 4.5:1 |
| UI components / graphics | 3:1 | N/A |
| Decorative elements | No requirement | N/A |

### Key Accessibility Features in M3

- **Built-in accessible color relationships**: Color pairs are designed to meet contrast requirements
- **Three contrast levels**: Users can choose contrast preference in system settings
- **Surface tones**: Proper tonal values ensure text readability on all surfaces
- **Error color accessibility**: Error colors meet minimum contrast ratios

---

## Key Color Tokens Reference

### Tone Values (Light Theme Example)

| Token | Hex | Usage |
|-------|-----|-------|
| Primary-0 | #FFFFFF | On Primary Container text |
| Primary-10 | #EADDFF | Primary Container |
| Primary-20 | #C9A7EB | - |
| Primary-30 | #B185DB | - |
| Primary-40 | #9A82DB | - |
| Primary-50 | #8661C9 | - |
| Primary-60 | #6750A4 | Primary |
| Primary-70 | #563EA6 | - |
| Primary-80 | #4B2C9A | - |
| Primary-90 | #3A1D87 | - |
| Primary-100 | #21005D | On Primary Container |

### Semantic Naming Convention

```
[Role]           = Base color (e.g., primary, secondary, tertiary, error)
On[Role]         = Text/icon on that color (e.g., onPrimary)
[Role]Container   = Surface variant of that color (e.g., primaryContainer)
On[Role]Container = Text on the container color
```

---

## Resources

| Resource | Link | Status |
|----------|------|--------|
| Design Kit (Figma) | Material Design Kit | Available |
| MDC-Android | GitHub | Available |
| Jetpack Compose | Compose Material 3 | Available |
| Flutter | flutter/material.dart | Available |
| Material Theme Builder | materialthemebuilder.com | Available |

---

## Related Documentation

- [Color Overview](https://m3.material.io/styles/color/overview)
- [Choosing a Color Scheme](https://m3.material.io/styles/color/choosing-a-scheme)
- [Dynamic Color](https://m3.material.io/styles/color/dynamic/overview)
- [Advanced Customizations](https://m3.material.io/styles/color/advanced/overview)
