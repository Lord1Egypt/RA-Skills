# Material Design 3 动效与 Motion 设计

> 来源：Google Material Design 3 — Motion
> URL: https://m3.material.io/design/motion
> 版本：M3 2024-2025
> 抓取时间：2026-04-23

---
hermes:
  source: https://m3.material.io/
  version: "2024-2025"
  platform: android|flutter|web
  updated: 2026-04-23

## Motion 三大原则

| 原则 | 说明 | 示例 |
|------|------|------|
| **Expressive** | 动效表达品牌个性，体现产品情感 | FAB 展开动画、页面转场 |
| **Informative** | 动效传达状态变化和空间关系 | 选中态、加载状态、列表操作 |
| **Responsive** | 用户操作后立即响应，动画跟随 | 按钮点击反馈、拖拽跟随 |

---

## 动画时长规范

| 类型 | 时长 | 应用场景 |
|------|------|---------|
| **Micro（微交互）** | 100-200ms | 按钮状态变化、图标切换、选择反馈 |
| **Short（中短）** | 200-300ms | 展开/收起、Toast、Snackbar |
| **Medium（中）** | 300-400ms | 大型容器展开、页面过渡 |
| **Long（长）** | 400-500ms | 大型表单展开、复杂 FAB 展开菜单 |

**规则：用户参与程度越高，时长越短（越快越"响应"）**

---

## 缓动曲线（Easing）

### 四种核心曲线

| 曲线名称 | 特征 | 语义 | CSS | Flutter | Compose |
|---------|------|------|------|---------|---------|
| **Standard** | 减速进入，快速退出 | 主屏幕元素的标准过渡 | `cubic-bezier(0.4, 0.0, 0.2, 1)` | `Curves.easeInOut` | `FastOutSlowIn` |
| **Emphasized** | 快速进入，缓慢退出 | 强调元素（FABS、Selection） | `cubic-bezier(0.2, 0.0, 0.0, 1.0)` | `Curves.easeOut` | `FastOutLinearIn` |
| **Decelerated** | 快速进入，逐渐停止 | 进入动画（元素出现） | `cubic-bezier(0.0, 0.0, 0.2, 1)` | `Curves.easeOutCubic` | `SlowOutFastIn` |
| **Accelerated** | 逐渐加速，快速离开 | 退出动画（元素消失） | `cubic-bezier(0.4, 0.0, 1, 1)` | `Curves.easeInCubic` | `LinearOutSlowIn` |

### 曲线应用场景

| 场景 | 推荐曲线 |
|------|---------|
| 元素出现（Fade + Scale in） | Decelerated |
| 元素消失（Fade + Scale out） | Accelerated |
| 页面主内容过渡 | Standard |
| FAB 展开菜单 | Emphasized |
| Bottom Sheet 展开 | Standard |
| 选中状态变化 | Emphasized |
| 列表项增删 | Standard |

---

## Android Compose 动画

### 基础动画

```kotlin
import androidx.compose.animation.*

// Fade 动画
AnimatedVisibility(
    visible = visible,
    enter = fadeIn(animationSpec = tween(300, easing = FastOutSlowIn)),
    exit = fadeOut(animationSpec = tween(200, easing = LinearOutSlowIn))
) {
    Content()
}

// Scale + Fade 进入
AnimatedVisibility(
    visible = visible,
    enter = scaleIn(
        initialScale = 0.8f,
        animationSpec = tween(300, easing = SlowOutFastIn)
    ) + fadeIn(),
    exit = scaleOut(
        targetScale = 0.8f,
        animationSpec = tween(200, easing = LinearOutSlowIn)
    ) + fadeOut()
)

// Slide 动画
AnimatedVisibility(
    visible = visible,
    enter = slideInVertically(
        initialOffsetY = { fullHeight -> fullHeight },
        animationSpec = tween(300, easing = FastOutSlowIn)
    ),
    exit = slideOutVertically(
        targetOffsetY = { fullHeight -> fullHeight },
        animationSpec = tween(200, easing = LinearOutSlowIn)
    )
)
```

### Crossfade（淡入淡出）

```kotlin
// 两状态之间的淡入淡出
Crossfade(
    targetState = currentTab,
    animationSpec = tween(300),
    label = "tab_crossfade"
) { tab ->
    when (tab) {
        Tab.HOME -> HomeContent()
        Tab.SEARCH -> SearchContent()
        Tab.PROFILE -> ProfileContent()
    }
}
```

### 共享元素过渡（Shared Element）

```kotlin
// 列表项到详情页的过渡
AnimatedContent(
    targetState = selectedItem,
    transitionSpec = {
        fadeIn(animationSpec = tween(300, easing = FastOutSlowIn)) togetherWith
        fadeOut(animationSpec = tween(200, easing = LinearOutSlowIn))
    },
    label = "item_transition"
) { item ->
    if (item != null) {
        ItemDetail(item = item)
    } else {
        ItemList()
    }
}
```

### Infinite Transition（循环动画）

```kotlin
val infiniteTransition = rememberInfiniteTransition(label = "loading")
val alpha by infiniteTransition.animateFloat(
    initialValue = 0.3f,
    targetValue = 1f,
    animationSpec = infiniteRepeatable(
        animation = tween(600, easing = FastOutSlowIn),
        repeatMode = RepeatMode.Reverse
    ),
    label = "alpha"
)

// Loading 动画
CircularProgressIndicator(
    modifier = Modifier.graphicsLayer { alpha = this.alpha }
)
```

---

## Flutter 动画

### 基础动画

```dart
import 'package:flutter/material.dart';

// AnimatedOpacity
AnimatedOpacity(
  opacity: visible ? 1.0 : 0.0,
  duration: const Duration(milliseconds: 300),
  curve: Curves.easeInOut,
  child: Content(),
)

// AnimatedContainer
AnimatedContainer(
  duration: const Duration(milliseconds: 300),
  curve: Curves.easeInOut,
  width: expanded ? 200 : 100,
  height: expanded ? 200 : 100,
  decoration: BoxDecoration(
    color: Theme.of(context).colorScheme.primaryContainer,
    borderRadius: BorderRadius.circular(expanded ? 28 : 8),
  ),
)

// AnimatedSwitcher + Fade
AnimatedSwitcher(
  duration: const Duration(milliseconds: 300),
  transitionBuilder: (child, animation) => FadeTransition(
    opacity: animation,
    child: child,
  ),
  child: KeyedSubtree(key: ValueKey(selected), child: Content()),
)
```

### Slide 动画

```dart
// SlideTransition + AnimationController
class _MyWidgetState extends State<MyWidget> with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<Offset> _slideAnimation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: const Duration(milliseconds: 300),
      vsync: this,
    );
    _slideAnimation = Tween<Offset>(
      begin: const Offset(0, 1),
      end: Offset.zero,
    ).animate(CurvedAnimation(
      parent: _controller,
      curve: Curves.easeOutCubic,
    ));
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return SlideTransition(
      position: _slideAnimation,
      child: Content(),
    );
  }
}
```

### Hero 动画（共享元素）

```dart
// 列表项 -> 详情页 Hero 动画
// 列表项
ListTile(
  leading: Hero(
    tag: 'avatar-${item.id}',
    child: CircleAvatar(backgroundImage: NetworkImage(item.avatarUrl)),
  ),
  title: Text(item.name),
  onTap: () => Navigator.push(
    context,
    MaterialPageRoute(builder: (_) => DetailPage(item: item)),
  ),
)

// 详情页
Hero(
  tag: 'avatar-${item.id}',
  child: CircleAvatar(
    radius: 60,
    backgroundImage: NetworkImage(item.avatarUrl),
  ),
)
```

### 循环动画

```dart
// 旋转 Loading
class LoadingSpinner extends StatefulWidget {
  @override
  _LoadingSpinnerState createState() => _LoadingSpinnerState();
}

class _LoadingSpinnerState extends State<LoadingSpinner>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: const Duration(milliseconds: 1000),
      vsync: this,
    )..repeat();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return RotationTransition(
      turns: _controller,
      child: const Icon(Icons.refresh, size: 32),
    );
  }
}
```

---

## H5 动画

### CSS Transitions

```css
/* 基本 Transition */
.md-button {
  transition: background-color 200ms ease-in-out,
              box-shadow 200ms ease-in-out;
}

.md-button:hover {
  background-color: var(--md-sys-color-primary);
  box-shadow: 0 2px 4px rgba(0,0,0,.2);
}

/* Scale 变换 */
.md-card:hover {
  transform: scale(1.02);
  transition: transform 200ms cubic-bezier(0.4, 0.0, 0.2, 1);
}

/* FAB 展开动画 */
.md-fab-menu {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.md-fab-menu-item {
  opacity: 0;
  transform: scale(0.8) translateY(20px);
  transition: opacity 300ms ease-out,
              transform 300ms cubic-bezier(0.2, 0.0, 0.0, 1);
}

.md-fab-menu.expanded .md-fab-menu-item {
  opacity: 1;
  transform: scale(1) translateY(0);
}
```

### H5 + JS 动画

```html
<script>
// AnimatedVisibility (H5 实现)
function animateIn(element, duration = 300) {
  element.style.opacity = '0';
  element.style.transform = 'translateY(16px)';
  element.style.display = 'block';
  
  requestAnimationFrame(() => {
    element.style.transition = `opacity ${duration}ms ease-out, transform ${duration}ms cubic-bezier(0.4, 0.0, 0.2, 1)`;
    element.style.opacity = '1';
    element.style.transform = 'translateY(0)';
  });
}

function animateOut(element, duration = 200) {
  element.style.transition = `opacity ${duration}ms ease-in, transform ${duration}ms cubic-bezier(0.4, 0.0, 1, 1)`;
  element.style.opacity = '0';
  element.style.transform = 'translateY(-8px)';
  
  setTimeout(() => {
    element.style.display = 'none';
  }, duration);
}

// FAB 菜单展开
function toggleFabMenu() {
  const menu = document.querySelector('.md-fab-menu');
  const isExpanded = menu.classList.toggle('expanded');
  
  const items = menu.querySelectorAll('.md-fab-menu-item');
  items.forEach((item, index) => {
    if (isExpanded) {
      item.style.transitionDelay = `${index * 50}ms`;
      item.style.opacity = '1';
      item.style.transform = 'scale(1) translateY(0)';
    } else {
      item.style.transitionDelay = `${(items.length - 1 - index) * 50}ms`;
      item.style.opacity = '0';
      item.style.transform = 'scale(0.8) translateY(20px)';
    }
  });
}
</script>
```

---

## 响应式动效

### 减少动画（无障碍）

| 用户设置 | 动作 |
|---------|------|
| `prefers-reduced-motion: reduce` | 所有动画时长设为 0 或极短 |
| 运动障碍 | 禁用所有位移动画，只保留 Fade |

```css
/* H5 — 尊重减少动画偏好 */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

```kotlin
// Android — 尊重减少动画
@Composable
fun Content() {
    val reducedMotion = androidx.compose.animation.core.rememberInfiniteTransition(label = "")
    // 使用 Animatable 或以编程方式检测系统设置
}
```

---

## 平台差异速查

| 特性 | Android | Flutter | Web |
|------|---------|---------|-----|
| 声明式动画 | `AnimatedVisibility` | `AnimatedSwitcher` | CSS `transition` |
| 程序化动画 | `Animatable.animateTo()` | `AnimationController` | `requestAnimationFrame` |
| 共享元素 | `SharedTransitionLayout` | `Hero` | `View Transitions API` |
| 循环动画 | `rememberInfiniteTransition` | `AnimationController.repeat()` | CSS `@keyframes` |
| 缓动曲线 | `FastOutSlowIn` 等 | `Curves.*` | `cubic-bezier()` |
| 减少动画 | `MediaQuery.disableAnimations()` | `MediaQuery.platformDataOf(context)` | `@media (prefers-reduced-motion)` |

---

## 来源
