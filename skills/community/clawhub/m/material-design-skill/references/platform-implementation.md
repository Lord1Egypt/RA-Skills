---
name: material-design-platform
description: Google Material Design 3 跨平台实现完整参考，覆盖 Flutter、Jetpack Compose、Android、Web。
source: https://m3.material.io/develop
---

# Material Design 3 跨平台实现参考

## 1. Cross-platform Overview

Material Design 3 (M3) provides official implementation libraries for four platforms:

| Platform | Library | M3 Status | M3 Expressive |
|----------|---------|-----------|---------------|
| **Android View** | MDC-Android | ✅ Available | ❌ Not available |
| **Jetpack Compose** | Compose Material 3 | ✅ Available | ✅ Available (May 2025) |
| **Flutter** | Material Widgets | ✅ Available | ❌ Not available |
| **Web** | Material Web Components | 🔒 Maintenance mode | ❌ Not available |

All platforms share:
- **26+ color roles** mapped to components
- **Unified color scheme system** (static baseline + dynamic color)
- **Typography scale** with M3 type levels
- **Elevation system** with tonal vs. overlay approaches
- **Shape tokens** for component corner radii

---

## 2. Flutter Implementation

### Enabling Material 3

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'M3 Demo',
      theme: ThemeData(
        useMaterial3: true,  // Opt-in to M3
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
      ),
      home: const MyHomePage(),
    );
  }
}
```

### ColorScheme in Flutter

```dart
// From seed color (recommended)
final colorScheme = ColorScheme.fromSeed(
  seedColor: Colors.blue,
  brightness: Brightness.light,  // or Brightness.dark
);

// From predefined scheme
final colorScheme = ColorScheme.fromScheme(
  scheme: ColorScheme.appleMedium(),  // iOS-style baseline
  brightness: Brightness.light,
);

// Manual color roles
final colorScheme = ColorScheme(
  brightness: Brightness.light,
  primary: Color(0xFF006590),
  onPrimary: Colors.white,
  primaryContainer: Color(0xFFC4E7FF),
  onPrimaryContainer: Color(0xFF001E2F),
  secondary: Color(0xFF4F600E),
  onSecondary: Colors.white,
  // ... all 12+ color roles
);
```

### Dynamic Color (Wallpaper-based)

```dart
ColorScheme.fromDynamic(
  dynamicScheme: DynamicScheme.fromImage(
    imageProvider: wallpaperImage,
    sourceColorHct: Hct.fromInt(Colors.blue.toARGB32()),
  ),
);
```

### Applying Theme to Components

```dart
// Wrap with MaterialApp using ThemeData
MaterialApp(
  theme: ThemeData(
    useMaterial3: true,
    colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
  ),
  home: const Scaffold(body: ...),
);

// Access in widgets
Widget build(BuildContext context) {
  final colorScheme = Theme.of(context).colorScheme;
  return Card(
    color: colorScheme.primaryContainer,
    child: Text('Hello', style: TextStyle(color: colorScheme.onPrimaryContainer)),
  );
}
```

### Key Flutter Theming Properties

```dart
ThemeData(
  useMaterial3: true,
  colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
  
  // Typography (M3 type scale)
  textTheme: Typography.material2021atypeScale,
  
  // Elevation overrides (optional)
  elevatedButtonTheme: ElevatedButtonThemeData(
    style: ElevatedButton.styleFrom(
      elevation: 2,  // M3 uses tonal elevation
    ),
  ),
)
```

---

## 3. Jetpack Compose Implementation

### Setup

```kotlin
// build.gradle.kts
dependencies {
    implementation("androidx.compose.material3:material3:1.3.0")
}
```

### Basic M3 Theme

```kotlin
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

@Composable
fun MyApp() {
    MaterialTheme(
        colorScheme = colorScheme,
        typography = Typography(),
        content = { /* app content */ }
    )
}

private val colorScheme = lightColorScheme(
    primary = Color(0xFF006590),
    onPrimary = Color.White,
    primaryContainer = Color(0xFFC4E7FF),
    onPrimaryContainer = Color(0xFF001E2F),
    secondary = Color(0xFF4F600E),
    onSecondary = Color.White,
    // ... all color roles
)
```

### Using rememberMaterial3Theme (Optional)

```kotlin
@Composable
fun rememberMaterial3Theme(
    seedColor: Color = Color(0xFF6750A4),
    lightTonalPalette: TonalPalette? = null,
    darkTonalPalette: TonalPalette? = null,
): MaterialTheme {
    val colorScheme = when {
        lightTonalPalette != null && darkTonalPalette != null -> {
            dynamicMultiBreakpointColorScheme(
                lightTonalPalette = lightTonalPalette,
                darkTonalPalette = darkTonalPalette,
            )
        }
        else -> {
            val scheme = ColorScheme.from(
                Color(seedColor),
                "en" // locale
            )
            if (darkTonalPalette != null) scheme.dark else scheme.light
        }
    }
    return MaterialTheme(colorScheme = colorScheme)
}
```

### Dynamic Color (Android 12+)

```kotlin
@Composable
fun DynamicColorMaterialTheme(
    content: @Composable () -> Unit
) {
    val colorScheme = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
        val context = LocalContext.current
        dynamicLightColorScheme(context)
        // or dynamicDarkColorScheme(context) for dark mode
    } else {
        lightColorScheme()  // fallback
    }
    MaterialTheme(colorScheme = colorScheme, content = content)
}
```

### Applying Colors in Components

```kotlin
@Composable
fun MyCard() {
    Card(
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.primaryContainer
        )
    ) {
        Text(
            "Hello",
            color = MaterialTheme.colorScheme.onPrimaryContainer
        )
    }
}
```

### M3 Expressive (Motion Physics) - Compose 1.3+

```kotlin
// Motion theming with spring physics
val springSpec = SpringSpec(
    dampingRatio = Spring.DampingRatioMediumBouncy,
    stiffness = Spring.StiffnessMedium
)

// Apply to component transitions
AnimatedVisibility(
    visibleState = expanded,
    enterMotionSpec = springSpec,
    exitMotionSpec = springSpec
)
```

---

## 4. Android View Implementation (MDC-Android)

### Setup

```gradle
// build.gradle
dependencies {
    implementation 'com.google.android.material:material:1.12.0'
}
```

### Applying M3 Theme

```xml
<!-- res/values/themes.xml -->
<resources>
    <style name="Theme.MyApp" parent="Theme.Material3.Light.NoActionBar">
        <!-- Primary colors -->
        <item name="colorPrimary">@color/md_theme_light_primary</item>
        <item name="colorOnPrimary">@color/md_theme_light_onPrimary</item>
        <item name="colorPrimaryContainer">@color/md_theme_light_primaryContainer</item>
        <item name="colorOnPrimaryContainer">@color/md_theme_light_onPrimaryContainer</item>
        
        <!-- Secondary, tertiary, error, etc. -->
        <item name="colorSecondary">@color/md_theme_light_secondary</item>
        <item name="colorSecondaryContainer">@color/md_theme_light_secondaryContainer</item>
        <!-- ... -->
    </style>
</resources>
```

### Programmatically with ColorScheme (M3 1.2+)

```kotlin
import com.google.android.material.color.DynamicColors
import com.google.android.material.color.ColorScheme

// Apply dynamic colors (wallpaper-based) to Activity
class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        DynamicColors.applyToActivityIfSupported(this)
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
    }
}

// Use ColorScheme programmatically
val colorScheme = ColorScheme.from(
    seedColor = Color(0xFF6750A4),
    brightness = Brightness.LIGHT
)

val primaryPaint = Paint().apply {
    color = colorScheme.primary
}
```

### Material3 color roles (26+ roles)

```kotlin
// Light scheme
val colorScheme = ColorScheme.light(
    primary = Color(0xFF6750A4),
    onPrimary = Color.White,
    primaryContainer = Color(0xFFEADDFF),
    onPrimaryContainer = Color(0xFF21005D),
    secondary = Color(0xFF625B71),
    onSecondary = Color.White,
    secondaryContainer = Color(0xFFE8DEF8),
    onSecondaryContainer = Color(0xFF1D192B),
    tertiary = Color(0xFF7D5260),
    onTertiary = Color.White,
    tertiaryContainer = Color(0xFFFFD8E4),
    onTertiaryContainer = Color(0xFF31111D),
    error = Color(0xFFB3261E),
    onError = Color.White,
    errorContainer = Color(0xFFF9DEDC),
    onErrorContainer = Color(0xFF410E0B),
    background = Color(0xFFFFFBFE),
    onBackground = Color(0xFF1C1B1F),
    surface = Color(0xFFFFFBFE),
    onSurface = Color(0xFF1C1B1F),
    surfaceVariant = Color(0xFFE7E0EC),
    onSurfaceVariant = Color(0xFF49454F),
    outline = Color(0xFF79747E),
    outlineVariant = Color(0xFFCAC4D0),
    // ... more roles
)
```

### Using M3 Components

```xml
<com.google.android.material.card.MaterialCardView
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    app:cardElevation="0dp"
    app:cardBackgroundColor="?attr/colorSurfaceContainer">

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Card content"
        android:textColor="?attr/colorOnSurface"/>

</com.google.android.material.card.MaterialCardView>
```

---

## 5. Web Implementation

### Status

> ⚠️ **Note**: Material Web Components are currently in **maintenance mode**. No new features are being added. M3 Expressive is **not implemented** on Web.

### Installation

```bash
npm install @material/web
```

### Basic Setup with CSS Custom Properties

```html
<!DOCTYPE html>
<html>
<head>
  <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">
  <script type="importmap">
    {
      "imports": {
        "@material/web": "https://esm.sh/@material/web@2.0.0"
      }
    }
  </script>
</head>
<body>
  <script type="module">
    import '@material/web/button/filled-button.js';
    import '@material/web/button/outlined-button.js';
  </script>
  
  <md-filled-button>Hello</md-filled-button>
  <md-outlined-button>World</md-outlined-button>
</body>
</html>
```

### CSS Theming with M3 Tokens

```css
:root {
  /* M3 Color Tokens - Light */
  --md-sys-color-primary: #6750A4;
  --md-sys-color-on-primary: #FFFFFF;
  --md-sys-color-primary-container: #EADDFF;
  --md-sys-color-on-primary-container: #21005D;
  
  --md-sys-color-secondary: #625B71;
  --md-sys-color-on-secondary: #FFFFFF;
  --md-sys-color-secondary-container: #E8DEF8;
  --md-sys-color-on-secondary-container: #1D192B;
  
  --md-sys-color-surface: #FFFBFE;
  --md-sys-color-on-surface: #1C1B1F;
  --md-sys-color-surface-variant: #E7E0EC;
  --md-sys-color-on-surface-variant: #49454F;
  
  --md-sys-color-outline: #79747E;
  --md-sys-color-outline-variant: #CAC4D0;
  
  /* Typography */
  --md-sys-typescale-display-large: Roboto, sans-serif;
  --md-sys-typescale-headline-large: Roboto, sans-serif;
  --md-sys-typescale-body-large: Roboto, sans-serif;
  
  /* Shape */
  --md-sys-shape-corner-extra-large: 28px;
  --md-sys-shape-corner-large: 16px;
  --md-sys-shape-corner-medium: 12px;
  --md-sys-shape-corner-small: 8px;
}
```

### Using Web Components

```html
<!-- Button -->
<md-filled-button @click="${handleClick}">
  Confirm
</md-filled-button>

<!-- Text Field -->
<md-outlined-text-field 
  label="Email" 
  type="email"
  supporting-text="Enter your email">
</md-outlined-text-field>

<!-- Card -->
<md-card>
  <md-card-header>
    <h2 slot="headline">Card Title</h2>
    <h3 slot="subheadline">Subtitle</h3>
  </md-card-header>
  <md-card-content>
    Card content here
  </md-card-content>
</md-card>
```

### JavaScript Integration

```javascript
import { MdButton } from '@material/web/button/md-button.js';

// Customize via properties
const button = document.querySelector('md-filled-button');
button.disabled = false;
button.icon = 'check';

// Listen to events
button.addEventListener('click', (e) => {
  console.log('Button clicked:', e.target);
});
```

### Applying Theme in JavaScript

```javascript
import { Theme } from '@material/web/theme/theme.js';

// Apply M3 theme to elements
const theme = new Theme();
theme.applyTo(document.body);

// Or via CSS
document.documentElement.style.setProperty('--md-sys-color-primary', '#6750A4');
```

---

## 6. Theming Across Platforms

### Shared Token Structure

All platforms share the same 26+ M3 color roles:

| Token Category | Roles |
|----------------|-------|
| **Primary** | primary, onPrimary, primaryContainer, onPrimaryContainer |
| **Secondary** | secondary, onSecondary, secondaryContainer, onSecondaryContainer |
| **Tertiary** | tertiary, onTertiary, tertiaryContainer, onTertiaryContainer |
| **Error** | error, onError, errorContainer, onErrorContainer |
| **Surface** | surface, onSurface, surfaceVariant, onSurfaceVariant |
| **Outline** | outline, outlineVariant |
| **Background** | background, onBackground (non-surface roles) |
| **Inverse** | inverseSurface, inverseOnSurface, inversePrimary |
| **Shadow** | shadow, scrim |
| **Surface Tint** | surfaceTint |

### Unified Color Scheme Generation

```
Seed Color → Tonal Palette Generation → Color Role Mapping
     ↓
  Blue → 16 tonal steps → 26+ color roles per theme mode
```

### Platform Comparison

| Feature | Flutter | Compose | Android View | Web |
|---------|---------|---------|--------------|-----|
| **Enable M3** | `useMaterial3: true` | `MaterialTheme()` | `Theme.Material3.*` | CSS tokens |
| **From seed** | `ColorScheme.fromSeed()` | `ColorScheme.from()` | `ColorScheme.from()` | N/A |
| **Dynamic color** | ✅ | ✅ | ✅ | ❌ |
| **Dark mode** | `Brightness.dark` | `darkColorScheme()` | `Theme.Material3.Dark` | CSS media query |
| **Typography** | `textTheme` | `Typography()` | `textAppearance` | CSS `font-*` |
| **Elevation** | Tonal (default) | Tonal (default) | Tonal (default) | CSS `box-shadow` |
| **Components** | Material Widgets | `material3` library | `Material` library | Web Components |

### ColorScheme Generation Example (Unified Concept)

```
// All platforms can generate a ColorScheme from a seed color:

Flutter:   ColorScheme.fromSeed(seedColor: Colors.purple)
Compose:   ColorScheme.from(Color(0xFF6750A4))
Android:   ColorScheme.from(seedColor = Color(0xFF6750A4))
Web:       Use --md-sys-color-primary CSS token

// Result: Consistent color relationships across all platforms
```

### Typography Scale (M3)

| Level | Flutter | Compose | Android View | Web |
|-------|---------|---------|--------------|-----|
| Display Large | `displayLarge` | `DisplayLarge` | `DisplayLarge` | `--typescale-display-large` |
| Headline | `headlineMedium` | `HeadlineMedium` | `HeadlineMedium` | `--typescale-headline-medium` |
| Title | `titleLarge` | `TitleLarge` | `TitleLarge` | `--typescale-title-large` |
| Body | `bodyLarge` | `BodyLarge` | `BodyLarge` | `--typescale-body-large` |
| Label | `labelMedium` | `LabelMedium` | `LabelMedium` | `--typescale-label-medium` |

---

## Resources

| Platform | Documentation |
|----------|---------------|
| Flutter | https://m3.material.io/develop/flutter |
| Jetpack Compose | https://m3.material.io/develop/android/jetpack-compose |
| MDC-Android | https://m3.material.io/develop/android |
| Web | https://m3.material.io/develop/web |
| Material Theme Builder | https://material-foundation.github.io/material-theme-builder/ |
