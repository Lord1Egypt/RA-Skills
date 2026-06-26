---
name: material-design-motion
description: Google Material Design 3 动效系统完整参考，覆盖物理弹簧、Motion Scheme、过渡动画。
source: https://m3.material.io/styles/motion/overview/how-it-works
---

# Material Design 3 Motion System Reference

> 官方文档: https://m3.material.io/styles/motion/overview/how-it-works

## Overview

Material 3 introduced a new **physics-based motion system** with M3 Expressive. This system makes interactions and transitions feel more alive, fluid, and natural. The physics system is replacing the previous system based on easing and duration.

### Platform Availability

| Platform | Status |
|----------|--------|
| **MDC-Android** | Available. Not yet added to components. See specs |
| **Flutter** | 部分可用：物理弹簧动画（`SpringSimulation`）✅，官方 M3 Motion 库封装 ❌ |
| **Jetpack Compose** | Available |
| **Web** | Compatible with Compose springs |

---

## Motion Philosophy: Physics-Based vs Easing-Based

### Physics-Based Motion

Physics-based animations use spring physics to determine movement:

- **Natural feel**: Motion responds to forces and continues based on physical properties
- **Interruptible**: Can be interrupted mid-animation and transitions smoothly to new target
- **Overshoot capability**: Can naturally exceed target values (bounce effect)
- **No fixed duration**: Animation time varies based on physics parameters

### Easing-Based Motion (Legacy)

The old system used predefined easing curves with fixed durations:

```javascript
// Legacy easing-based approach
transition: all 300ms ease-in-out;
```

### Comparison

| Aspect | Physics-Based | Easing-Based |
|--------|--------------|--------------|
| Feel | Natural, alive | Mechanical |
| Interruptibility | Smooth interruption | Jumps or restarts |
| Duration | Variable | Fixed |
| Overshoot | Natural | Not supported |
| Complexity | Higher | Lower |

---

## Motion Schemes

The physics system provides two preset motion schemes. The scheme defines how your product feels.

### Expressive Scheme

Material's **opinionated motion scheme** for most situations, particularly hero moments and key interactions.

**Characteristics:**
- Overshoots final values to add bounce
- More playful and dynamic
- Emphasizes important moments

```
Expressive → overshoots → settles
```

### Standard Scheme

More **functional with minimal bounce**. Best for utilitarian products.

**Characteristics:**
- Ease-in-out with minimal overshoot
- Efficient and focused
- Less visual emphasis

```
Standard → smooth ease → arrives
```

### Choosing a Scheme

| Use Case | Recommended Scheme |
|----------|-------------------|
| Hero moments | Expressive |
| Key interactions | Expressive |
| Important transitions | Expressive |
| Utility apps | Standard |
| Data-heavy interfaces | Standard |
| Form-filling tasks | Standard |

### Advanced Customization

Products can swap schemes to emphasize key moments while using a different scheme for the majority of motion.

---

## Spring Physics

### Spring Model Parameters

The spring physics system uses these core parameters:

| Parameter | Description | Effect |
|-----------|-------------|--------|
| **Stiffness** | Resistance to displacement | Higher = snappier |
| **Damping** | Resistance to oscillation | Higher = less bounce |
| **Mass** | Inertia of the object | Higher = slower |

### Spring Tokens

Material 3 defines spring tokens that map to common use cases:

```
// Expressive spring (bouncy)
spring: {
  damping: 0.6,
  stiffness: 200,
  mass: 1.0
}

// Standard spring (controlled)
spring: {
  damping: 0.8,
  stiffness: 300,
  mass: 1.0
}
```

### Overshoot Behavior

- **Expressive**: Springs overshoot the target value before settling
  - Creates bounce effect
  - Feels more responsive and playful
  
- **Standard**: Springs approach target with minimal overshoot
  - Controlled arrival
  - Feels more precise and efficient

### Damping Ratio

| Damping Ratio | Behavior |
|---------------|----------|
| < 1.0 | Underdamped (oscillates/bounces) |
| = 1.0 | Critically damped (no overshoot) |
| > 1.0 | Overdamped (slow settling) |

Material 3 Expressive uses underdamped springs (~0.6-0.7) for bounce.

---

## Transition Patterns

### Container Transform

Moving content between containers with smooth spatial transition.

**Use for:**
- List items expanding to detail views
- Cards transforming into full-screen content
- FAB expanding into screen

### Fade Through

Content is replaced with a new element.

**Use for:**
- Navigation between major sections
- Tab content changes
- Mode switches

### Shared Axis

Elements maintain relationship through 3D space.

**Use for:**
- Onboarding flows
- Step-by-step processes
- Sequential content

### Elevation Transition

Elements moving up/down in z-axis.

**Use for:**
- FAB morphing
- Bottom sheets
- Dialogs

### Staggered Animation

Sequential or overlapping animations of multiple elements.

**Use for:**
- List item animations
- Grid reveals
- Dashboard loading states

---

## Platform Implementation

### Flutter

Flutter uses implicit animations with physics-based support.

```dart
import 'package:flutter/material.dart';

// Implicit animation with AnimatedContainer
AnimatedContainer(
  duration: Duration(milliseconds: 300),
  curve: Curves.easeInOut,
  width: isExpanded ? 200 : 100,
  height: isExpanded ? 200 : 100,
  child: Container(color: Colors.blue),
)

// Custom spring animation with AnimationController
class SpringAnimation extends StatefulWidget {
  @override
  _SpringAnimationState createState() => _SpringAnimationState();
}

class _SpringAnimationState extends State<SpringAnimation>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _animation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      // No fixed duration - driven by physics
    );
    
    _animation = Tween<double>(begin: 0, end: 1).animate(
      CurvedAnimation(
        parent: _controller,
        curve: Curves.elasticOut, // Simulates spring overshoot
      ),
    );
  }
}
```

**Note:** M3 Expressive motion is not yet available for Flutter.

### Jetpack Compose

Compose provides comprehensive spring animation support.

```kotlin
import androidx.compose.animation.core.*
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Box
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp

@Composable
fun SpringAnimationExample() {
    var expanded by remember { mutableStateOf(false) }
    
    // Spring-based animation state
    val animatedSize by animateDpAsState(
        targetValue = if (expanded) 200.dp else 100.dp,
        animationSpec = spring(
            dampingRatio = SpringDampingRatio.R_mediumBouncy,
            stiffness = SpringStiffness.medium,
        ),
        label = "size"
    )
    
    Box(
        modifier = Modifier
            .size(animatedSize)
            .background(Color.Blue)
            .clickable { expanded = !expanded }
    )
}

// Explicit spring specification
val springSpec = spring<Float>(
    dampingRatio = 0.6f,    // Bouncy overshoot
    stiffness = 200f,       // Snappiness
    mass = 1f               // Heaviness
)

// Using with animateFloatAsState
@Composable
fun FloatAnimation() {
    var target by remember { mutableStateOf(0f) }
    
    val animatedValue by animateFloatAsState(
        targetValue = target,
        animationSpec = spring(
            dampingRatio = SpringDampingRatio.NoBouncy,
            stiffness = SpringStiffness.high,
        ),
        label = "float"
    )
}
```

### Android (Views / XML)

Android uses the Transition framework with spring physics.

```xml
<!-- res/anim/fragment_fade_through.xml -->
<transitionSet xmlns:android="http://schemas.android.com/apk/res/android"
    android:transitionOrdering="together">
    <fade android:fadingMode="fade_out" />
    <fade android:fadingMode="fade_in" />
</transitionSet>

<!-- Kotlin with SpringAnimation -->
import android.animation.SpringAnimation
import android.animation.SpringForce

// Spring animation for a view property
val scaleXAnimation = SpringAnimation(view, SpringAnimation.SCALE_X, targetScale).apply {
    spring = SpringForce(targetScale).apply {
        dampingRatio = SpringForce.DAMPING_RATIO_MEDIUM_BOUNCY
        stiffness = SpringForce.STIFFNESS_MEDIUM
    }
}

// Start the animation
scaleXAnimation.start()

// Cancel on interruption
scaleXAnimation.cancel()
```

```kotlin
// Container transform transition (AndroidX)
import androidx.transition.TransitionSet
import androidx.transition.Slide
import androidx.transition.Fade

val customTransition = TransitionSet().apply {
    ordering = TransitionSet.ORDERING_TOGETHER
    addTransition(Slide(Gravity.END))
    addTransition(Fade(Fade.OUT))
}

// Apply to fragment
val exitTransition = customTransition
val reenterTransition = Fade(Fade.IN)
```

### Web / CSS

Web supports spring-like animations through CSS and JavaScript.

```css
/* CSS with custom properties (limited spring support) */
.motion-expressive {
  --motion-spring-damping: 0.6;
  --motion-spring-stiffness: 200;
  
  transition: transform var(--motion-duration-medium) 
              cubic-bezier(0.34, 1.56, 0.64, 1); /* spring-like curve */
}

.motion-standard {
  transition: transform var(--motion-duration-medium) 
              cubic-bezier(0.4, 0.0, 0.2, 1); /* ease-in-out */
}

/* Web Animations API with physics */
@keyframes spring-bounce {
  0% { transform: scale(0.8); }
  50% { transform: scale(1.1); } /* overshoot */
  100% { transform: scale(1.0); }
}
```

```javascript
// Web Animations API with spring-like timing
element.animate([
  { transform: 'scale(0.8)', offset: 0 },
  { transform: 'scale(1.1)', offset: 0.6 },  // overshoot at 60%
  { transform: 'scale(1.0)', offset: 1 }
], {
  duration: 400,
  easing: 'cubic-bezier(0.34, 1.56, 0.64, 1)', // spring curve
  fill: 'forwards'
});
```

---

## When to Use Motion

### Use Motion When

| Scenario | Motion Type |
|----------|-------------|
| **Showing spatial relationships** | Container transform |
| **Indicating state changes** | Fade through |
| **Emphasizing importance** | Expressive spring |
| **Guiding user attention** | Staggered reveals |
| **Confirming actions** | Bounce/scale feedback |
| **Navigating between views** | Shared axis |
| **Expanding/collapsing content** | Spring-based implicit |

### Don't Overuse Motion

Avoid motion when:
- User prefers reduced motion (respect `prefers-reduced-motion`)
- Motion serves no communicative purpose
- Animation is purely decorative in a utilitarian context
- It slows down task completion
- It causes nausea or discomfort (flashing, rapid movement)

### Accessibility

```kotlin
// Compose: Respecting reduced motion preferences
@Composable
fun AccessibleAnimation() {
    val prefersReducedMotion = LocalLayoutDirection.current
    
    val animatedValue by animateFloatAsState(
        targetValue = target,
        animationSpec = if (prefersReducedMotion) {
            snap() // Instant or very short
        } else {
            spring(dampingRatio = 0.6f)
        }
    )
}
```

```dart
// Flutter: Checking accessibility preferences
MediaQuery.of(context).disableAnimations; // Returns true if user wants reduced motion

// Wrap animations to check preference
Widget build(BuildContext context) {
    final reduceMotion = MediaQuery.of(context).disableAnimations;
    
    return AnimatedContainer(
        duration: reduceMotion ? Duration.zero : Duration(milliseconds: 300),
        curve: reduceMotion ? Curves.linear : Curves.easeInOut,
        // ...
    );
}
```

---

## Key Token Reference

### Duration Tokens

| Token | Duration | Use Case |
|-------|----------|----------|
| `motion_duration_short1` | 50ms | Micro-interactions |
| `motion_duration_short2` | 100ms | Small state changes |
| `motion_duration_medium1` | 200ms | Standard transitions |
| `motion_duration_medium2` | 300ms | Larger movements |
| `motion_duration_long1` | 400ms | Full screen transitions |
| `motion_duration_long2` | 500ms | Complex animations |

### Easing Tokens (Legacy Reference)

| Token | Curve | Character |
|-------|-------|-----------|
| `easing-standard` | 0.4, 0.0, 0.2, 1 | Smooth entry/exit |
| `easing-emphasized` | 0.4, 0.0, 0.2, 1 | Slightly more pronounced |
| `easing-decelerated` | 0.0, 0.0, 0.2, 1 | Entering |
| `easing-accelerated` | 0.4, 0.0, 1.0, 1 | Exiting |

---

## Resources

| Resource | Link | Status |
|----------|------|--------|
| Motion Overview | https://m3.material.io/styles/motion/overview | Official docs |
| MDC-Android | GitHub | Available |
| Jetpack Compose | Compose Material 3 | Available |
| Flutter | flutter/material.dart | M3 Expressive unavailable |
| Design Kit (Figma) | Material Design Kit | Available |

---

## Related Documentation

- [Motion Overview](https://m3.material.io/styles/motion/overview)
- [Motion System - How it Works](https://m3.material.io/styles/motion/overview/how-it-works)
- [Flutter Animations](https://docs.flutter.dev/development/ui/animations)
- [Jetpack Compose Animation](https://developer.android.com/jetpack/compose/animation)
