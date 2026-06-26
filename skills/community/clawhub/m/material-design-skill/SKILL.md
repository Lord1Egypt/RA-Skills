---
name: material-design
description: >
  Google Material Design 3 (M3) 跨平台设计系统技能。覆盖色彩系统、Typography、Shape、
  Elevation、Icons、Animation、组件规范（Buttons、Cards、Navigation 等）及
  Flutter/Compose/Android/Web 四平台实现。当用户提到 Material Design、MD3、M3、
  Material You、动态配色、Material Icon、设计系统、Android UI、Flutter Material
  时触发。
trigger: Material Design|Material Design 3|MD3|M3|material you|Android UI|Android 设计|Compose|Flutter Material|Material 3|色板|配色方案|Typography|组件规范|Elevation|阴影|Material Icon|设计系统|Google 设计|移动端设计|跨平台 UI|卡片设计|按钮样式|输入框|导航栏|Bottom Navigation|FAB|AppBar|动态配色|Material You
tags:
  - material-design
  - android
  - flutter
  - web
  - ui-design
  - design-system
hermes:
  platform: hermes
  version: "2.0"
  last_updated: "2026-04-24"
  source: |
    https://m3.material.io/
    https://m3.material.io/styles/color/overview
    https://m3.material.io/styles/typography/overview
    https://m3.material.io/styles/shape/overview
    https://m3.material.io/styles/motion/overview/how-it-works
    https://m3.material.io/foundations
    https://m3.material.io/components
    https://m3.material.io/develop
---

# 色彩系统

## 色彩角色

M3 定义了 26+ 色彩角色，分为五大类：

| 类别 | 角色 | 说明 |
|------|------|------|
| Primary | Primary, Primary Container, On Primary, On Primary Container | 主品牌色 |
| Secondary | Secondary, Secondary Container, On Secondary, On Secondary Container | 辅助色 |
| Tertiary | Tertiary, Tertiary Container, On Tertiary, On Tertiary Container | 强调色 |
| Error | Error, Error Container, On Error, On Error Container | 错误/警告 |
| Neutral | Surface, On Surface, Surface Variant, Outline, Outline Variant | 中性色 |
| Neutral Special | Inverse Surface, Inverse On Surface, Inverse Primary, Surface Tint | 特殊中性 |
| Scrim | Scrim | 遮罩层 |

### 动态配色（Material You）

用户可通过壁纸生成主题色（User-generated color scheme）：

- Android 12+：从壁纸提取主色，自动应用到整个系统
- Flutter：`ColorScheme.fromSeed(seedColor: color, brightness: Brightness.light)`
- Compose：`dynamicColor = DynamicColor.getOrCreate(context)`

### 主题构建

| 平台 | 代码 |
|------|------|
| Flutter | `ColorScheme.fromSeed(seedColor: Colors.blue, brightness: Brightness.light)` |
| Compose | `lightColorScheme(primary = ...)` |
| Android XML | `Theme.Material3.DayNight.NoActionBar` |
| CSS | `--md-sys-color-primary: #...;` |

详细参考：[color-system.md](references/color-system.md)

---

# Typography

## Type Scale（5 角色 × 3 尺寸 = 15 种样式）

| 角色 | 大（Large） | 中（Medium） | 小（Small） |
|------|-----------|------------|-----------|
| Display | Display Large (57sp) | Display Medium (45sp) | Display Small (36sp) |
| Headline | Headline Large (32sp) | Headline Medium (28sp) | Headline Small (24sp) |
| Title | Title Large (22sp) | Title Medium (16sp) | Title Small (14sp) |
| Body | Body Large (16sp) | Body Medium (14sp) | Body Small (12sp) |
| Label | Label Large (14sp) | Label Medium (12sp) | Label Small (11sp) |

## 字体

- **默认字体**：Roboto
- **等宽字体**：Roboto Mono
- **表达性字体**：Roboto Serif、Bagel Fat One、Anton（用于 Display 样式）

## 平台实现

| 平台 | API |
|------|-----|
| Flutter | `TextTheme(displayLarge: TextStyle(...), ...)` |
| Compose | `Typography(displayLarge: TextStyle(...), ...)` |
| Android | `TextAppearance.Material3.DisplayLarge` |
| CSS | `font-size: 57px; font-weight: 400;` |

详细参考：[typography.md](references/typography.md)

---

# Shape、Elevation、Icons

## Shape 系统

35 种形状，corner radius 分为 10 级：

| 级别 | Small | Medium | Large |
|------|-------|--------|-------|
| 0 | 0dp | 0dp | 0dp |
| 1 | 2dp | 4dp | 0dp |
| 2 | 4dp | 8dp | 0dp |
| 3 | 6dp | 12dp | 0dp |
| 4 | 8dp | 16dp | 0dp |
| 5 | 12dp | 20dp | 0dp |

M3 Expressive 新增：Large Increased (20dp)、Extra Large Increased (32dp)、Extra Extra Large (48dp)

## Elevation

6 级（Level 0-5），通过 tonal surface color 或 shadow 显示高度：

| Level | 用途 | 叠加高度 |
|-------|------|---------|
| 0 | 平面 | 0dp |
| 1 | 表面 | 1dp |
| 2 | 导航 | 3dp |
| 3 | FAB | 6dp |
| 4 | 模态 | 8dp |
| 5 | 导航 + FAB | 12dp |

## Icons

Material Symbols variable font，支持 4 个可变轴：
- **Weight**：100-700
- **Fill**：0（Outlined）到 1（Filled）
- **Optical size**：20px-48px
- **Grade**：0（Regular）到 -25（more visible on small sizes）

样式：Outlined、Rounded、Sharp

详细参考：[shape-elevation-icons.md](references/shape-elevation-icons.md)

---

# Motion（动效系统）

## Motion Scheme

| 方案 | 特点 | 适用场景 |
|------|------|---------|
| **Expressive** | overshoot（弹性超出） | 英雄时刻、关键交互 |
| **Standard** | ease into（缓入到达） | 功能性产品 |

## Spring Physics

三个参数控制弹簧动画：

| 参数 | 说明 | 典型值 |
|------|------|-------|
| Stiffness | 刚度，越高越快 | 100-1000 |
| Damping | 阻尼，越高越少弹跳 | 10-30 |
| Mass | 质量，越低响应越快 | 0.5-2 |

## 过渡动画

| 模式 | 说明 | 平台可用性 |
|------|------|---------|
| Container Transform | 共享元素变换 | Flutter 需自定义实现（Hero + flightShuttleBuilder）|
| Fade Through | 淡入淡出 | 全平台 |
| Shared Axis | 共享轴位移 | 全平台 |

**注意**：Flutter 有物理弹簧动画（`SpringSimulation`）和 Hero/Staggered 动画，可实现类似 Expressive 效果，但官方 M3 Motion 库封装暂不可用。

详细参考：[motion.md](references/motion.md)

---

# Foundations（设计基础）

## 自适应布局

Window Size Classes：

| Class | 宽度 | 布局 |
|-------|------|------|
| Compact | < 600dp | 单列 |
| Medium | 600-840dp | 自适应列 |
| Expanded | > 840dp | 多列+侧边导航 |

详细参考：[foundations.md](references/foundations.md)

---

# 组件库

## 8 大组件类别

| 类别 | 组件 | 平台可用性 |
|------|------|---------|
| **Buttons** | Buttons, FABs, Icon buttons, Button groups | Flutter ✅ Compose ✅ Android ✅ Web ✅ |
| **Date & Time** | Date pickers, Time pickers | Flutter ✅ Compose ✅ Android ✅ Web ❌ |
| **Loading** | Loading indicators, Progress indicators | Flutter ✅ Compose ✅ Android ✅ Web ❌ |
| **Navigation** | Navigation bar, Navigation rail, Navigation drawer | Flutter ✅ Compose ✅ Android ✅ Web ❌ |
| **Sheets** | Bottom sheets, Side sheets | Flutter ✅ Compose ✅ Android ✅ Web ❌ |
| **Selection** | Checkboxes, Chips, Radio buttons, Switches | Flutter ✅ Compose ✅ Android ✅ Web ✅ |
| **Text Input** | Text fields | Flutter ✅ Compose ✅ Android ✅ Web ✅ |
| **Containment** | App bars, Cards, Dialogs, Lists | Flutter ✅ Compose ✅ Android ✅ Web ✅ |

详细参考：
- [components-overview.md](references/components-overview.md)
- [navigation-components.md](references/navigation-components.md)
- [input-components.md](references/input-components.md)
- [display-components.md](references/display-components.md)

---

# 跨平台实现

## Flutter

```dart
MaterialApp(
  theme: ThemeData(
    useMaterial3: true,
    colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
  ),
);
```

Flutter 有物理弹簧动画（`SpringSimulation`）和 Hero/Staggered 动画，可部分实现 Expressive 效果，但官方 M3 Motion 库封装暂不可用。

## Jetpack Compose

```kotlin
MaterialTheme(
    colorScheme = lightColorScheme(
        primary = Color(0xFF6750A4),
        // ...
    )
) { /* content */ }
```

Compose 支持完整的 M3 Expressive。

## Android View

```xml
<style name="Theme.MyApp" parent="Theme.Material3.DayNight.NoActionBar">
    <item name="colorPrimary">@color/...</item>
</style>
```

## Web

Material Web Components 处于**维护模式**，不再开发新功能。

详细参考：[platform-implementation.md](references/platform-implementation.md)

---

# Material Design 3 (M3) 跨平台设计系统

> 来源：Google Material Design 3 官方文档
> URL: https://m3.material.io/
> 版本：M3 Expressive（2025 年 5 月更新）
> 更新日期：2026-04-24

Material Design 3（MD3/M3）是 Google 发布的最新设计系统，通过 Material You（动态配色）实现跨平台一致的视觉体验。支持 Flutter、Jetpack Compose、Android View、Web 四平台。

---

## 设计原则

### 核心三原则

| 原则 | 说明 | 应用场景 |
|------|------|---------|
| **Material Expressive** | 表达品牌个性，通过颜色、形状、动画体现 | 自定义主题色、圆角半径 |
| **Responsive** | 适配不同屏幕尺寸和输入方式 | 断点布局、触摸/鼠标适配 |
| **Accessible** | 为所有用户设计，包含视觉/运动/认知障碍 | 对比度要求、最小触摸区域 |

### M3 Expressive 更新（2025 年 5 月）

| M3 Expressive 是 M3 的重大升级，引入了更丰富的动画系统、物理弹簧动效和组件变体。以下组件已在 M3 Expressive（May 2025）中被标记为**不再推荐**： |

- Navigation Drawer → 推荐使用 Expanded Navigation Rail
- Segmented Buttons → 推荐使用 Connected Button Group
- **Neutral text button** → 不再推荐，使用 Filled/Outlined/Text 变体之一
- Baseline Navigation Bar/Rail → 推荐使用 Flexible/Collapsed/Expanded 变体
- Baseline Extended FAB → 推荐使用 Surface FAB

---

> 📌 色彩系统完整内容见上方 [#色彩系统](#色彩系统) 章节。
> 
> 详细参考：[color-system.md](references/color-system.md)

---

## Typography

### Type Scale（5 角色 × 3 尺寸 = 15 种样式）

| 角色 | 大（Large） | 中（Medium） | 小（Small） |
|------|-----------|------------|-----------|
| Display | Display Large (57sp) | Display Medium (45sp) | Display Small (36sp) |
| Headline | Headline Large (32sp) | Headline Medium (28sp) | Headline Small (24sp) |
| Title | Title Large (22sp) | Title Medium (16sp) | Title Small (14sp) |
| Body | Body Large (16sp) | Body Medium (14sp) | Body Small (12sp) |
| Label | Label Large (14sp) | Label Medium (12sp) | Label Small (11sp) |

### 字体

- **默认字体**：Roboto
- **等宽字体**：Roboto Mono
- **表达性字体**：Roboto Serif、Bagel Fat One、Anton（用于 Display 样式）

### 平台实现

| 平台 | API |
|------|-----|
| Flutter | `TextTheme(displayLarge: TextStyle(...), ...)` |
| Compose | `Typography(displayLarge: TextStyle(...), ...)` |
| Android | `TextAppearance.Material3.DisplayLarge` |
| CSS | `font-size: 57px; font-weight: 400;` |

详细参考：[typography.md](references/typography.md)

---

## Shape、Elevation、Icons

### Shape 系统

35 种形状，corner radius 分为 10 级：

| 级别 | Small | Medium | Large |
|------|-------|--------|-------|
| 0 | 0dp | 0dp | 0dp |
| 1 | 2dp | 4dp | 0dp |
| 2 | 4dp | 8dp | 0dp |
| 3 | 6dp | 12dp | 0dp |
| 4 | 8dp | 16dp | 0dp |
| 5 | 12dp | 20dp | 0dp |

M3 Expressive 新增：Large Increased (20dp)、Extra Large Increased (32dp)、Extra Extra Large (48dp)

### Elevation

6 级（Level 0-5），通过 tonal surface color 或 shadow 显示高度：

| Level | 用途 | 叠加高度 |
|-------|------|---------|
| 0 | 平面 | 0dp |
| 1 | 表面 | 1dp |
| 2 | 导航 | 3dp |
| 3 | FAB | 6dp |
| 4 | 模态 | 8dp |
| 5 | 导航 + FAB | 12dp |

### Icons

Material Symbols variable font，支持 4 个可变轴：
- **Weight**：100-700
- **Fill**：0（Outlined）到 1（Filled）
- **Optical size**：20px-48px
- **Grade**：0（Regular）到 -25（more visible on small sizes）

样式：Outlined、Rounded、Sharp

详细参考：[shape-elevation-icons.md](references/shape-elevation-icons.md)

---

## Motion（动效系统）

### Motion Scheme

| 方案 | 特点 | 适用场景 |
|------|------|---------|
| **Expressive** | overshoot（弹性超出） | 英雄时刻、关键交互 |
| **Standard** | ease into（缓入到达） | 功能性产品 |

### Spring Physics

三个参数控制弹簧动画：

| 参数 | 说明 | 典型值 |
|------|------|-------|
| Stiffness | 刚度，越高越快 | 100-1000 |
| Damping | 阻尼，越高越少弹跳 | 10-30 |
| Mass | 质量，越低响应越快 | 0.5-2 |

### 过渡动画

| 模式 | 说明 | 平台可用性 |
|------|------|---------|
| Container Transform | 共享元素变换 | Flutter 需自定义实现（Hero + flightShuttleBuilder）|
| Fade Through | 淡入淡出 | 全平台 |
| Shared Axis | 共享轴位移 | 全平台 |

**注意**：Flutter 有物理弹簧动画（`SpringSimulation`）和 Hero/Staggered 动画，可实现类似 Expressive 效果，但官方 M3 Motion 库封装暂不可用。

详细参考：[motion.md](references/motion.md)

---

## Foundations（设计基础）

### 自适应布局

Window Size Classes：

| Class | 宽度 | 布局 |
|-------|------|------|
| Compact | < 600dp | 单列 |
| Medium | 600-840dp | 自适应列 |
| Expanded | > 840dp | 多列+侧边导航 |

详细参考：[foundations.md](references/foundations.md)

---

## 组件库

### 8 大组件类别

| 类别 | 组件 | 平台可用性 |
|------|------|---------|
| **Buttons** | Buttons, FABs, Icon buttons, Button groups | Flutter ✅ Compose ✅ Android ✅ Web ✅ |
| **Date & Time** | Date pickers, Time pickers | Flutter ✅ Compose ✅ Android ✅ Web ❌ |
| **Loading** | Loading indicators, Progress indicators | Flutter ✅ Compose ✅ Android ✅ Web ❌ |
| **Navigation** | Navigation bar, Navigation rail, Navigation drawer | Flutter ✅ Compose ✅ Android ✅ Web ❌ |
| **Sheets** | Bottom sheets, Side sheets | Flutter ✅ Compose ✅ Android ✅ Web ❌ |
| **Selection** | Checkboxes, Chips, Radio buttons, Switches | Flutter ✅ Compose ✅ Android ✅ Web ✅ |
| **Text Input** | Text fields | Flutter ✅ Compose ✅ Android ✅ Web ✅ |
| **Containment** | App bars, Cards, Dialogs, Lists | Flutter ✅ Compose ✅ Android ✅ Web ✅ |

详细参考：
- [components-overview.md](references/components-overview.md)
- [navigation-components.md](references/navigation-components.md)
- [input-components.md](references/input-components.md)
- [display-components.md](references/display-components.md)

---

## 跨平台实现

### Flutter

```dart
MaterialApp(
  theme: ThemeData(
    useMaterial3: true,
    colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
  ),
);
```

Flutter 有物理弹簧动画（`SpringSimulation`）和 Hero/Staggered 动画，可部分实现 Expressive 效果，但官方 M3 Motion 库封装暂不可用。

### Jetpack Compose

```kotlin
MaterialTheme(
    colorScheme = lightColorScheme(
        primary = Color(0xFF6750A4),
        // ...
    )
) { /* content */ }
```

Compose 支持完整的 M3 Expressive。

### Android View

```xml
<style name="Theme.MyApp" parent="Theme.Material3.DayNight.NoActionBar">
    <item name="colorPrimary">@color/...</item>
</style>
```

### Web

Material Web Components 处于**维护模式**，不再开发新功能。

详细参考：[platform-implementation.md](references/platform-implementation.md)

---

## 避坑指南

### M3 Expressive 兼容性

| 平台 | M3 Expressive 支持 |
|------|-------------------|
| Jetpack Compose | ✅ 完整支持 |
| Android View | ✅ 完整支持 |
| Flutter | ⚠️ 官方库不可用，可通过 Hero/Staggered/`SpringSimulation` 自定义实现 |
| Web | ❌ 不可用 |

### 动态配色

- Android 12+ 设备自动支持
- 旧版 Android 需回退到 baseline color scheme
- Web 端不支持动态配色

### 组件废弃

以下组件在 M3 Expressive（May 2025）中不再推荐：
- Navigation Drawer → 使用 Navigation Rail
- Segmented Buttons → 使用 Connected Button Group
- **Neutral text button** → 不再推荐，使用 Filled/Outlined/Text 变体之一

### Flutter Platform.adaptive

Flutter 3.22+ 引入了 `Platform.adaptive` 系列组件，自动在 iOS（Cupertino）和 Android（Material）间切换：

| 组件 | 说明 | 自动适配 |
|------|------|---------|
| `PlatformNavigationBar` | 底部导航栏 | iOS → CupertinoTabBar / Android → NavigationBar |
| `PlatformIconButton` | 图标按钮 | iOS → CupertinoButton / Android → IconButton |
| `PlatformTextButton` | 文字按钮 | iOS → CupertinoButton / Android → TextButton |
| `PlatformSwitch` | 开关 | iOS → CupertinoSwitch / Android → Switch |

```dart
// 最常用的 PlatformNavigationBar
PlatformNavigationBar(
  selectedIndex: currentIndex,
  onDestinationSelected: (i) => setState(() => currentIndex = i),
  destinations: const [
    NavigationDestination(
      icon: Icon(Icons.explore_outlined),
      selectedIcon: Icon(Icons.explore),
      label: 'Explore',
    ),
    NavigationDestination(
      icon: Icon(Icons.bookmark_border),
      selectedIcon: Icon(Icons.bookmark),
      label: 'Saved',
    ),
  ],
)

// PlatformIconButton 示例
PlatformIconButton(
  icon: Icon(Icons.settings),
  onPressed: () => openSettings(),
)
```

---

## 快速参考

### 色彩角色速查

| Token | 说明 |
|-------|------|
| `primary` | 主品牌色 |
| `onPrimary` | 主色上的文字色 |
| `primaryContainer` | 主色容器 |
| `surface` | 表面色 |
| `surfaceVariant` | 表面变体 |
| `outline` | 边框色 |
| `error` | 错误色 |

### Type Scale 速查

| 角色-尺寸 | 字重 | 大小 |
|---------|------|------|
| Display Large | 400 | 57sp |
| Headline Medium | 400 | 28sp |
| Title Medium | 500 | 16sp |
| Body Large | 400 | 16sp |
| Label Small | 500 | 11sp |

### Corner Radius 速查

| 级别 | 值 |
|------|-----|
| Small | 4-8dp |
| Medium | 8-16dp |
| Large | 12-20dp |
| Extra Large | 32dp+ |

### Elevation 速查

| Level | 叠加高度 | 典型用途 |
|-------|---------|---------|
| 0 | 0dp | 平面 |
| 1 | 1dp | 表面 |
| 3 | 6dp | FAB |
| 5 | 12dp | 模态 |

### 触摸目标

| 元素 | 最小尺寸 |
|------|---------|
| 触摸目标 | 48dp × 48dp |
| 按钮内图标 | 24dp |
| List item | 48dp 高 |

### 平台支持矩阵

| 功能 | Flutter | Compose | Android | Web |
|------|---------|---------|---------|-----|
| M3 基础 | ✅ | ✅ | ✅ | ✅ |
| M3 Expressive | ❌ | ✅ | ✅ | ❌ |
| 动态配色 | ✅ | ✅ | ✅ 12+ | ❌ |
| 物理弹簧动效 | ❌ | ✅ | ✅ | ❌ |
| Web Components | N/A | N/A | N/A | ✅ 维护中 |

---

## 输出格式规范

### 回复结构

1. **直接回答** — 一段简洁的话给出核心答案
2. **代码示例** — 提供完整的平台代码（如需）
3. **实现要点** — 关键步骤和注意事项
4. **避坑提醒** — 常见错误 + 正确做法

### 示例回复

> M3 的动态配色通过 `ColorScheme.fromSeed()` 实现。Flutter 中只需传入一个种子色，系统会自动生成完整的 26 色色板，支持亮色/暗色自动切换。
> M3 Expressive 更新后，Compose 已支持物理弹簧动效，但 Flutter 仍不原生支持。

```dart
// Flutter 动态配色
MaterialApp(
  theme: ThemeData(
    useMaterial3: true,
    colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
  ),
);
```

### 禁用格式

- ❌ 不要显式分层（避免"第一层/第二层/框架分析"等字眼）
- ❌ 不要长篇解释概念，要直接给出实现
- ❌ 不要只给代码片段，要给完整可运行的示例
- ✅ 输出应是一段干净的话 + 完整代码

---

## 来源

> 文档版本：Material Design 3 M3 Expressive（2025 年 5月更新）
> URL: https://m3.material.io/
> 抓取时间：2026-04-24
> 官方文档涵盖：Color, Typography, Shape, Elevation, Icons, Motion, Foundations, Components, Develop

---

## 参考文档

| 文件 | 行数 | 覆盖内容 |
|------|------|---------|
| color-system.md | 427 | 色彩系统完整参考 |
| typography.md | 316 | Typography 完整参考 |
| shape-elevation-icons.md | 213 | Shape、Elevation、Icons |
| motion.md | 507 | 动效系统完整参考 |
| foundations.md | 231 | 设计原则与自适应布局 |
| components-overview.md | 210 | 组件库总览 |
| navigation-components.md | 137 | 导航组件详解 |
| input-components.md | 252 | 输入组件详解 |
| display-components.md | 221 | 展示组件详解 |
| platform-implementation.md | 573 | 跨平台实现 |
| color-scheme-roles.md | 293 | 色彩角色详解 |
| components.md | 517 | 组件完整参考 |
| components-quickref.md | 462 | 组件速查 |
| m3-migration-guide.md | 520 | M2→M3 迁移指南 |
| md3-api-changes.md | 379 | API 变更 |
| motion-animation.md | 448 | 动效动画 |
| layout-constraints.md | 103 | 布局约束 |
