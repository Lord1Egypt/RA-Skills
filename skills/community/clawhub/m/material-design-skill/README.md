# Material Design 3 设计系统技能

Google Material Design 3 (M3) 跨平台设计系统技能，覆盖色彩、Typography、Shape、Elevation、Icons、动效及四平台实现。当用户提到 Material Design、MD3、M3、Material You、设计系统时触发。

## 概述

本 skill 覆盖 Material Design 3 完整知识体系：

- **色彩系统** — 色彩角色、动态配色（Material You）、Token 映射
- **Typography** — Type Scale、品牌定制、三平台实现
- **Shape 与 Elevation** — 形状系统、阴影层级、光照模型
- **Icons** — Material Symbols、图标规格
- **Motion** — Motion Scheme、Spring 物理、过渡动画
- **Foundations** — 设计原则、自适应布局
- **组件库** — 按钮、卡片、导航、输入等 8 大组件类别
- **跨平台实现** — Flutter / Jetpack Compose / Android View / Web 四平台

## 核心章节

### 设计基础

| 章节 | 内容 |
|------|------|
| [色彩系统](SKILL.md#色彩系统) | 色彩角色、动态配色、ColorScheme.fromSeed |
| [Typography](SKILL.md#Typography) | Type Scale、品牌定制、三平台字体实现 |
| [Shape、Elevation、Icons](SKILL.md#Shape、Elevation、Icons) | 形状系统、阴影层级、图标规格 |

### 动效系统

| 章节 | 内容 |
|------|------|
| [Motion（动效系统）](SKILL.md#Motion动效系统) | Motion Scheme、Spring 物理、过渡动画 |
| [快速参考](SKILL.md#快速参考) | M3 Expressive 动效一览 |

### 设计基础与组件

| 章节 | 内容 |
|------|------|
| [Foundations（设计基础）](SKILL.md#Foundations设计基础) | 设计原则、自适应布局 |
| [组件库](SKILL.md#组件库) | 8 大组件类别、状态、废弃信息 |
| [跨平台实现](SKILL.md#跨平台实现) | Flutter/Jetpack Compose/Android/Web 四平台对照 |

### 参考文档

| 文件 | 行数 | 内容 |
|------|------|------|
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

## 快速参考

### 色彩角色

| 类别 | 角色 | 说明 |
|------|------|------|
| Primary | Primary, Primary Container, On Primary | 主品牌色 |
| Secondary | Secondary, Secondary Container | 辅助色 |
| Tertiary | Tertiary, Tertiary Container | 强调色 |
| Error | Error, Error Container | 错误/警告 |
| Neutral | Surface, On Surface, Surface Variant, Outline | 中性色 |

### 动态配色（Material You）

```kotlin
// Android Compose
val dynamicColor = DynamicColor(context = LocalContext.current)
val colorScheme = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
    dynamicColor.getColorSchemeByRole(userColor)
} else {
    ColorScheme.fromSeed(seed = userColor)
}
```

```dart
// Flutter
final colorScheme = ColorScheme.fromSeed(
  seedColor: userWallpaperColor,
  brightness: Brightness.light,
);
```

### Typography Type Scale

| 角色 | 用途 | 示例 |
|------|------|------|
| Display Large | Hero 标题 | 57sp / 64sp |
| Headline Large | 章节标题 | 32sp |
| Title Large | 卡片标题 | 22sp |
| Body Large | 正文 | 16sp |
| Label Small | 按钮文字 | 11sp |

### M3 按钮对照

| 类型 | Flutter | Android Compose | Web (H5) |
|------|---------|-----------------|-----------|
| Filled | `FilledButton()` | `Button()` | `.md-button--filled` |
| Filled Tonal | `FilledButton.tonal()` | `FilledTonalButton()` | `.md-button--tonal` |
| Outlined | `OutlinedButton()` | `OutlinedButton()` | `.md-button--outlined` |
| Text | `TextButton()` | `TextButton()` | `.md-button--text` |
| FAB | `FloatingActionButton()` | `FloatingActionButton()` | `.md-fab` |

### Motion Spring 配置

| 参数 | 说明 | 默认值 |
|------|------|--------|
| mass | 质量 | 1 |
| stiffness | 刚度 | 500 |
| damping | 阻尼 | 25 |
| duration | 持续时间（fallback） | 300ms |

### 组件状态

| 状态 | 说明 |
|------|------|
| **Available** | 正常可用 |
| **Expressive** | M3 Expressive 变体（2025年5月更新） |
| **No longer recommended** | 废弃，不建议使用 |

### 种子色配置

```kotlin
// Android
val colorScheme = ColorScheme.fromSeed(
  seedColor = Color(0xFF6750A4),
  brightness = Brightness.LIGHT,
)
```

```swift
// SwiftUI
ColorScheme.from(.init(red: 0.41, green: 0.33, blue: 0.65))
```

```dart
// Flutter
MaterialApp(
  theme: ThemeData(
    colorScheme: ColorScheme.fromSeed(seedColor: Color(0xFF6750A4)),
    useMaterial3: true,
  ),
)
```

## 避坑指南

### 色彩

| 错误做法 | 正确做法 |
|---------|---------|
| ❌ 硬编码 HEX 颜色值 | ✅ 使用 ColorScheme 色彩角色 |
| ❌ 浅色主题用深色 Primary | ✅ Primary 应同时适配浅/深色主题 |
| ❌ 动态配色降级处理不一致 | ✅ 降级时统一回退到种子色方案 |

### Typography

| 错误做法 | 正确做法 |
|---------|---------|
| ❌ 混用多个字体族 | ✅ 保持品牌字体一致性 |
| ❌ 标题正文字号相同 | ✅ 按 Type Scale 层级区分 |
| ❌ 在 Body 中使用 Display 字号 | ✅ 遵循 8dp 基准网格 |

### 动效

| 错误做法 | 正确做法 |
|---------|---------|
| ❌ 所有动画时长相同 | ✅ 按移动距离和复杂度调整（150~500ms） |
| ❌ 禁用减弱动画偏好 | ✅ 检测 `prefers-reduced-motion` 并提供替代方案 |
| ❌ 缺少入场/退场配对动画 | ✅ 遵循 M3 Motion 的进入/退出/禁用的语义 |

### 组件

| 错误做法 | 正确做法 |
|---------|---------|
| ❌ 使用已废弃组件（如 Neutral text button） | ✅ 使用对应 Expressive 变体或替代方案 |
| ❌ 混用 M2 和 M3 组件 | ✅ 统一使用 useMaterial3: true |
| ❌ 触摸目标小于 48dp | ✅ 最小触摸目标 48 × 48 dp |

## 来源

> Google Material Design 3（2026-04-24 访问）
> - 官方文档：https://m3.material.io/
> - 色彩系统：https://m3.material.io/styles/color/overview
> - Typography：https://m3.material.io/styles/typography/overview
> - Shape：https://m3.material.io/styles/shape/overview
> - Motion：https://m3.material.io/styles/motion/overview/how-it-works
> - 组件库：https://m3.material.io/components
>
> 版本：Material Design 3 M3 Expressive（2025 年 5 月更新）
