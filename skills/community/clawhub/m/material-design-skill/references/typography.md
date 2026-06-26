---
name: material-design-typography
description: Google Material Design 3 字体系统完整参考，覆盖 Type Scale、Token、平台实现。
source: https://m3.material.io/styles/typography/overview
---

# Material Design 3 Typography Reference

## Overview

M3 type scale contains **30 type styles**: 15 baseline and 15 emphasized (May 2025 Expressive update). The type scale organizes styles into five roles: Display, Headline, Title, Label, and Body. Each role has three sizes: Large, Medium, and Small.

---

## M3 Type Scale

### Baseline Type Styles

| Role | Size | Token | Size (px) | Line Height (px) | Weight | Tracking |
|------|------|-------|-----------|------------------|--------|----------|
| **Display** | Large | `typescale-display-large` | 57 | 64 | 400 | -0.25 |
| **Display** | Medium | `typescale-display-medium` | 45 | 52 | 400 | 0 |
| **Display** | Small | `typescale-display-small` | 36 | 44 | 400 | 0 |
| **Headline** | Large | `typescale-headline-large` | 32 | 40 | 400 | 0 |
| **Headline** | Medium | `typescale-headline-medium` | 28 | 36 | 400 | 0 |
| **Headline** | Small | `typescale-headline-small` | 24 | 32 | 400 | 0 |
| **Title** | Large | `typescale-title-large` | 22 | 28 | 400 | 0 |
| **Title** | Medium | `typescale-title-medium` | 16 | 24 | 500 | 0.15 |
| **Title** | Small | `typescale-title-small` | 14 | 20 | 500 | 0.1 |
| **Body** | Large | `typescale-body-large` | 16 | 24 | 400 | 0.5 |
| **Body** | Medium | `typescale-body-medium` | 14 | 20 | 400 | 0.25 |
| **Body** | Small | `typescale-body-small` | 12 | 16 | 400 | 0.4 |
| **Label** | Large | `typescale-label-large` | 14 | 20 | 500 | 0.1 |
| **Label** | Medium | `typescale-label-medium` | 12 | 16 | 500 | 0.5 |
| **Label** | Small | `typescale-label-small` | 11 | 16 | 500 | 0.5 |

### Emphasized Type Styles (M3 Expressive)

Emphasized styles add more expression to highlighted moments with higher weight and minor adjustments. They complement baseline styles.

| Role | Size | Token | Size (px) | Line Height (px) | Weight | Tracking |
|------|------|-------|-----------|------------------|--------|----------|
| **Display** | Large | `typescale-display-large-emphasis` | 57 | 64 | 400 | -0.25 |
| **Display** | Medium | `typescale-display-medium-emphasis` | 45 | 52 | 400 | 0 |
| **Display** | Small | `typescale-display-small-emphasis` | 36 | 44 | 400 | 0 |
| **Headline** | Large | `typescale-headline-large-emphasis` | 32 | 40 | 400 | 0 |
| **Headline** | Medium | `typescale-headline-medium-emphasis` | 28 | 36 | 400 | 0 |
| **Headline** | Small | `typescale-headline-small-emphasis` | 24 | 32 | 400 | 0 |
| **Title** | Large | `typescale-title-large-emphasis` | 22 | 28 | 500 | 0 |
| **Title** | Medium | `typescale-title-medium-emphasis` | 16 | 24 | 500 | 0.15 |
| **Title** | Small | `typescale-title-small-emphasis` | 14 | 20 | 500 | 0.1 |
| **Body** | Large | `typescale-body-large-emphasis` | 16 | 24 | 500 | 0.5 |
| **Body** | Medium | `typescale-body-medium-emphasis` | 14 | 20 | 500 | 0.25 |
| **Body** | Small | `typescale-body-small-emphasis` | 12 | 16 | 500 | 0.4 |
| **Label** | Large | `typescale-label-large-emphasis` | 14 | 20 | 500 | 0.1 |
| **Label** | Medium | `typescale-label-medium-emphasis` | 12 | 16 | 500 | 0.5 |
| **Label** | Small | `typescale-label-small-emphasis` | 11 | 16 | 500 | 0.5 |

---

## Font Families

### Default Typeface: Roboto

Roboto is the default typeface for Android and M3. It includes over 3,300 glyphs supporting hundreds of languages worldwide.

### Variable Fonts (Available for Customization)

#### Roboto Flex
- Variable font with extended flexibility
- Additional customizable attributes including size-specific designs
- Over 900 glyphs with support for Latin, Greek, and Cyrillic
- Not yet part of the M3 typescale (May 2025)

#### Roboto Serif
- Variable font designed for comfortable reading
- Minimal and highly functional
- Extensive set of weights and widths across a broad range of sizes
- Suitable for app interfaces and editorial content

#### Roboto Mono
- Monospaced version of Roboto
- Each letter has equal space with adjusted letterforms

---

## Type Scale Tokens

Each type style has a **single composite token** that captures all default properties. Individual axis tokens enable granular customization:

| Token Type | Description | Example |
|------------|-------------|---------|
| **Composite token** | All properties in one | `typescale-display-large` |
| **Font token** | Font family only | `typography-font-family` |
| **Size token** | Font size only | `typography-size` |
| **Line height token** | Line height only | `typography-line-height` |
| **Tracking token** | Letter spacing only | `typography-tracking` |
| **Weight token** | Font weight only | `typography-weight` |

### Token Naming Convention

```
// Composite token
material.typography.typescale.[role].[size]

// Individual axis token
material.typography.[role].[size].[property]
```

---

## Applying Type

### Role Guidelines

#### Display
- **Use for**: Short, important text or numerals; largest text on screen
- **Best on**: Large screens
- **Consider**: Expressive fonts (handwritten, script) for visual impact
- **Tip**: Set appropriate optical size when available

#### Headline
- **Use for**: Short, high-emphasis text on smaller screens; marking primary passages
- **Suitable for**: Section headers, important content regions
- **Expressive option**: Can use expressive typefaces with adjusted line height and letter spacing

#### Title
- **Use for**: Titles of content sections, card headers
- **Medium/Small sizes**: Use weight 500 (Medium) for increased emphasis

#### Body
- **Use for**: Longer paragraphs of text, content that requires reading
- **Large**: Primary body text
- **Medium/Small**: Secondary text, captions

#### Label
- **Use for**: Buttons, tabs, chips, small UI text
- **Tracking**: Medium and Small labels have higher tracking for legibility at small sizes

### Typesetting Best Practices

1. **Optical sizing**: Set appropriate optical size for display and headline styles
2. **Line height**: Ensure adequate line height for readability (typically 1.2-1.5× font size)
3. **Line length**: Target 50-75 characters per line for body text
4. **Contrast**: Maintain sufficient contrast between text and background
5. **Tracking adjustment**: Increase tracking for small text labels

### Ensuring Readability

- Body text minimum: 12px for legible text
- Label text minimum: 11px
- Line height ratios: 1.2× for headlines, 1.4-1.5× for body text
- Letter spacing: Adjust for size - smaller text may need more tracking

---

## Platform Implementation

### Flutter

```dart
// Using TextTheme
TextTheme(
  displayLarge: TextStyle(fontSize: 57, height: 64/57),
  displayMedium: TextStyle(fontSize: 45, height: 52/45),
  displaySmall: TextStyle(fontSize: 36, height: 44/36),
  headlineLarge: TextStyle(fontSize: 32, height: 40/32),
  headlineMedium: TextStyle(fontSize: 28, height: 36/28),
  headlineSmall: TextStyle(fontSize: 24, height: 32/24),
  titleLarge: TextStyle(fontSize: 22, height: 28/22),
  titleMedium: TextStyle(fontSize: 16, height: 24/16, fontWeight: FontWeight.w500),
  titleSmall: TextStyle(fontSize: 14, height: 20/14, fontWeight: FontWeight.w500),
  bodyLarge: TextStyle(fontSize: 16, height: 24/16),
  bodyMedium: TextStyle(fontSize: 14, height: 20/14),
  bodySmall: TextStyle(fontSize: 12, height: 16/12),
  labelLarge: TextStyle(fontSize: 14, height: 20/14, fontWeight: FontWeight.w500),
  labelMedium: TextStyle(fontSize: 12, height: 16/12, fontWeight: FontWeight.w500),
  labelSmall: TextStyle(fontSize: 11, height: 16/11, fontWeight: FontWeight.w500),
)
```

**Status**: M3 Expressive is NOT available on Flutter.

### Jetpack Compose

```kotlin
// Using Typography
Typography(
  displayLarge = TextStyle(fontSize = 57.sp, lineHeight = 64.sp),
  displayMedium = TextStyle(fontSize = 45.sp, lineHeight = 52.sp),
  displaySmall = TextStyle(fontSize = 36.sp, lineHeight = 44.sp),
  headlineLarge = TextStyle(fontSize = 32.sp, lineHeight = 40.sp),
  headlineMedium = TextStyle(fontSize = 28.sp, lineHeight = 36.sp),
  headlineSmall = TextStyle(fontSize = 24.sp, lineHeight = 32.sp),
  titleLarge = TextStyle(fontSize = 22.sp, lineHeight = 28.sp),
  titleMedium = TextStyle(fontSize = 16.sp, lineHeight = 24.sp, fontWeight = FontWeight.Medium),
  titleSmall = TextStyle(fontSize = 14.sp, lineHeight = 20.sp, fontWeight = FontWeight.Medium),
  bodyLarge = TextStyle(fontSize = 16.sp, lineHeight = 24.sp),
  bodyMedium = TextStyle(fontSize = 14.sp, lineHeight = 20.sp),
  bodySmall = TextStyle(fontSize = 12.sp, lineHeight = 16.sp),
  labelLarge = TextStyle(fontSize = 14.sp, lineHeight = 20.sp, fontWeight = FontWeight.Medium),
  labelMedium = TextStyle(fontSize = 12.sp, lineHeight = 16.sp, fontWeight = FontWeight.Medium),
  labelSmall = TextStyle(fontSize = 11.sp, lineHeight = 16.sp, fontWeight = FontWeight.Medium)
)
```

**Status**: M3 Expressive IS available on Jetpack Compose (May 2025).

### Android (XML)

```xml
<!-- Using TextAppearance -->
<TextAppearance
    android:textAppearance="?attr/textAppearanceDisplayLarge"
    />

<!-- Common TextAppearances -->
<!-- ?attr/textAppearanceDisplayLarge -->
<!-- ?attr/textAppearanceDisplayMedium -->
<!-- ?attr/textAppearanceDisplaySmall -->
<!-- ?attr/textAppearanceHeadlineLarge -->
<!-- ?attr/textAppearanceHeadlineMedium -->
<!-- ?attr/textAppearanceHeadlineSmall -->
<!-- ?attr/textAppearanceTitleLarge -->
<!-- ?attr/textAppearanceTitleMedium -->
<!-- ?attr/textAppearanceTitleSmall -->
<!-- ?attr/textAppearanceBodyLarge -->
<!-- ?attr/textAppearanceBodyMedium -->
<!-- ?attr/textAppearanceBodySmall -->
<!-- ?attr/textAppearanceLabelLarge -->
<!-- ?attr/textAppearanceLabelMedium -->
<!-- ?attr/textAppearanceLabelSmall -->
```

### CSS

```css
/* M3 Type Scale CSS */
:root {
  --md-sys-typescale-display-large: clamp(3.56rem, 3.54rem + 0.11vw, 3.57rem);
  --md-sys-typescale-display-medium: clamp(2.81rem, 2.8rem + 0.05vw, 2.81rem);
  --md-sys-typescale-display-small: clamp(2.25rem, 2.25rem + 0vw, 2.25rem);
  /* ... additional type scale values ... */
}

/* Example usage */
.text-display-large {
  font-family: Roboto;
  font-size: 57px;
  line-height: 64px;
  letter-spacing: -0.25px;
  font-weight: 400;
}
```

**Status**: M3 Expressive IS NOT available on Web.

---

## Accessibility

### Minimum Readable Sizes

| Context | Minimum Size |
|---------|--------------|
| Body text | 12px |
| Labels (buttons, chips) | 11px |
| Captions | 12px |

### Line Height Guidelines

- **Headlines**: 1.2× font size (e.g., 32px text → 40px line height)
- **Body text**: 1.4-1.5× font size (e.g., 14px text → 20px line height)
- **Small labels**: 1.3-1.5× font size for legibility

### Contrast Requirements

- Normal text: 4.5:1 contrast ratio minimum
- Large text (18px+ or 14px bold): 3:1 contrast ratio minimum
- Ensure sufficient contrast in both light and dark themes

### Additional Considerations

1. **Touch targets**: Label text should be at least 11px but ensure clickable areas are at least 48×48dp
2. **Scaling**: Support dynamic text scaling while maintaining layout integrity
3. **Language support**: Roboto supports 3,300+ glyphs for internationalization
4. **Line length**: Limit body text to 50-75 characters per line for optimal readability

---

## M3 Expressive Update (May 2025)

The M3 Expressive update introduced emphasized type styles:

- **15 new emphasized styles** complement the 15 baseline styles
- Emphasized styles have **higher weight** and minor adjustments
- Best used for **bold, selection, and other areas of emphasis**
- Baseline and emphasized styles are **meant to be used together**
- **Roboto Flex** enables expressive typography but is not yet part of the M3 typescale

### Where Emphasized Styles Are Available

| Platform | Status |
|----------|--------|
| Flutter | Not available |
| Jetpack Compose | Available |
| MDC-Android | Available |
| Web | Not available |

---

## Resources

- **Google Fonts**: [Roboto](https://fonts.google.com/specimen/Roboto), [Roboto Flex](https://fonts.google.com/specimen/Roboto+Flex), [Roboto Serif](https://fonts.google.com/specimen/Roboto+Serif), [Roboto Mono](https://fonts.google.com/specimen/Roboto+Mono)
- **Design Kit**: Available (Figma)
- **Official Documentation**: https://m3.material.io/styles/typography/overview
