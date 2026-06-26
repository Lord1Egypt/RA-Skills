# ColorScheme 颜色体系详解

> 来源：Flutter 中文网 / GitHub cfug/flutter.cn
> URL: https://github.com/cfug/flutter.cn/blob/main/src/content/release/breaking-changes/new-color-scheme-roles.md
> 版本：Flutter 3.22+ (ColorScheme 角色更新)
> 抓取时间：2026-04-24

---

## 概述

Material Design 3 的 ColorScheme 经历了多次演进：
- **Flutter 3.16+：** `ColorScheme.fromSeed` 引入，动态配色基础建立
- **Flutter 3.22+：** 新增 tone-based surface 颜色角色，12 个新增 accent 颜色

---

## ColorScheme.fromSeed（核心 API）

### 基本用法

```dart
// 从种子色生成完整配色方案
ColorScheme.fromSeed(seedColor: Colors.blue)

// 指定 brightness
ColorScheme.fromSeed(
  seedColor: Colors.blue,
  brightness: Brightness.dark,
)
```

### DynamicSchemeVariant（3.22+ 新增）

当种子色过亮时，`ColorScheme.fromSeed` 会生成偏暗的结果。指定 `fidelity` 变体可强制保持亮度：

```dart
// ❌ 默认：亮色种子可能生成暗的 ColorScheme
ColorScheme.fromSeed(seedColor: Color(0xFF0000FF)) // 亮蓝

// ✅ fidelity：保持原始亮度
ColorScheme.fromSeed(
  seedColor: Color(0xFF0000FF),
  dynamicSchemeVariant: DynamicSchemeVariant.fidelity,
)

// ✅ comfortable：生成舒适的配色
ColorScheme.fromSeed(
  seedColor: Color(0xFF0000FF),
  dynamicSchemeVariant: DynamicSchemeVariant.comfortable,
)

// ✅ vibrant：生成鲜艳配色
ColorScheme.fromSeed(
  seedColor: Color(0xFF0000FF),
  dynamicSchemeVariant: DynamicSchemeVariant.vibrant,
)
```

---

## MD3 颜色角色完整列表

### Primary（主要色）

| 角色 | 说明 | 默认值 |
|------|------|--------|
| `primary` | 主要品牌色 | 从 seed 生成 |
| `onPrimary` | primary 上的文字色 | 白色/深色 |
| `primaryContainer` | 主要容器色 | 浅 primary |
| `onPrimaryContainer` | primaryContainer 上的文字 | 深 primary |

### Secondary（次要色）

| 角色 | 说明 |
|------|------|
| `secondary` | 次要品牌色 |
| `onSecondary` | secondary 上的文字色 |
| `secondaryContainer` | 次要容器色 |
| `onSecondaryContainer` | secondaryContainer 上文字色 |

### Tertiary（第三色）

| 角色 | 说明 |
|------|------|
| `tertiary` | 第三强调色 |
| `onTertiary` | tertiary 上文字色 |
| `tertiaryContainer` | 第三容器色 |
| `onTertiaryContainer` | tertiaryContainer 上文字色 |

### Error（错误色）

| 角色 | 说明 |
|------|------|
| `error` | 错误色 |
| `onError` | error 上文字色 |
| `errorContainer` | 错误容器色 |
| `onErrorContainer` | errorContainer 上文字色 |

### Surface（表面色）

| 角色 | 说明 | 引入版本 |
|------|------|---------|
| `surface` | 主表面色 | M2 |
| `onSurface` | surface 上文字色 | M2 |
| `surfaceVariant` | 表面变体 | M2 → 3.22+ 重新定义 |
| `onSurfaceVariant` | surfaceVariant 上文字色 | M2 |
| `surfaceBright` | 最亮表面 | 3.22+ |
| `surfaceDim` | 最暗表面 | 3.22+ |
| `surfaceContainer` | 标准容器色 | 3.22+ |
| `surfaceContainerLow` | 低 elevation 容器 | 3.22+ |
| `surfaceContainerLowest` | 最低容器色 | 3.22+ |
| `surfaceContainerHigh` | 高 elevation 容器 | 3.22+ |
| `surfaceContainerHighest` | 最高容器色 | 3.22+ |
| `surfaceTint` | 表面色调（elevation 指示） | M2 |

### Outline（边框色）

| 角色 | 说明 |
|------|------|
| `outline` | 边框色 |
| `outlineVariant` | 边框变体 |
| `inverseSurface` | 反转表面色 |
| `onInverseSurface` | inverseSurface 上文字色 |
| `inversePrimary` | 反转主要色 |

### Shadow / Scrim

| 角色 | 说明 |
|------|------|
| `shadow` | 阴影色 |
| `scrim` | 幕布色（对话框背景等） |

---

## Tone-Based Surface 系统（3.22+）

### 概念

旧的 surface 模型使用 `surfaceTint` 叠加——在表面色上覆盖一层 tint 色来表示 elevation。MD3 改为 tone-based surface：每个 elevation 级别有独立的 surface 颜色，由 HCT 色彩系统自动计算。

### 新旧模型对比

| 模型 | 机制 | 问题 |
|------|------|------|
| M2 opacity 模型 | surface + surfaceTint 叠加 | 颜色计算不准确 |
| MD3 tone-based | 独立 surface 颜色 | 更精确的 elevation 感知 |

### Elevation 与 Surface 颜色映射

| Elevation | Light Mode surface | Dark Mode surface |
|-----------|-------------------|-------------------|
| 0dp | `surface` | `surface` |
| 1dp | `surfaceContainerLow` | — |
| 2dp | `surfaceContainer` | — |
| 3dp | `surfaceContainerHigh` | — |
| 4dp+ | `surfaceContainerHighest` | — |

### Flutter 中的使用

```dart
// MD3 中 Card 的 elevation 现在用 surfaceTint 实现
Card(
  elevation: 2,
  // 实际效果：背景色从 surface → surfaceContainerHigh
  // 同时 surfaceTint 层叠
)

// 如需恢复 M2 行为（透明 tint）
Card(
  color: Theme.of(context).colorScheme.surface,
  elevation: 2,
  surfaceTintColor: Colors.transparent,
)
```

---

## Extended Colors（扩展色板）

### 概念

Extended Colors 允许从品牌色生成多组协调的 accent 颜色。每个 seedColor 可以生成 4 组 accent 色调。

### API

```dart
ColorScheme.fromSeed(
  seedColor: Colors.blue,
  dynamicSchemeVariant: DynamicSchemeVariant.vibrant,
)

// 生成 extended 颜色
ColorScheme.fromSeed(
  seedColor: Colors.blue,
  brightness: Brightness.light,
).copyWith(
  // 手动扩展更多颜色
)
```

---

## 动态配色（Dynamic Color）

### Android 12+ 动态配色

Android 12+ 支持从壁纸提取颜色作为主题色。

```dart
// 自动检测是否支持动态配色
ColorScheme.fromImageProvider(
  provider: const NetworkImage('https://example.com/wallpaper.jpg'),
  brightness: Brightness.light,
)
```

### Flutter 中的动态配色

```dart
// 使用系统动态配色（Android 12+）
MaterialApp(
  theme: ThemeData(
    colorScheme: ColorScheme.fromSeed(
      seedColor: Theme.of(context).colorScheme.seed,
      dynamicSchemeVariant: DynamicSchemeVariant.system,
    ),
  ),
)
```

---

## 深色主题

### 深色模式颜色生成

```dart
// 自动从 seed 生成深色配色
ThemeData(
  colorScheme: ColorScheme.fromSeed(
    seedColor: Colors.indigo,
    brightness: Brightness.dark,
  ),
)

// 或使用 copyWith
ThemeData().copyWith(
  colorScheme: ColorScheme.fromSeed(
    seedColor: Colors.indigo,
    brightness: Brightness.dark,
  ),
)
```

### 手动深色模式

```dart
MaterialApp(
  theme: ThemeData(
    colorScheme: ColorScheme.fromSeed(seedColor: Colors.indigo),
  ),
  darkTheme: ThemeData(
    colorScheme: ColorScheme.fromSeed(
      seedColor: Colors.indigo,
      brightness: Brightness.dark,
    ),
  ),
  themeMode: ThemeMode.system,
)
```

---

## 迁移检查清单

| 检查项 | 操作 |
|--------|------|
| `ColorScheme.light()` 旧写法 | 改用 `ColorScheme.fromSeed()` |
| `ColorScheme.background` | 替换为 `ColorScheme.surface` |
| `ColorScheme.onBackground` | 替换为 `ColorScheme.onSurface` |
| `ColorScheme.surfaceVariant` | 替换为 `ColorScheme.surfaceContainerHighest` |
| 手动设置的 `surfaceTint` | 移除或设为 `Colors.transparent` |
| 亮色种子生成偏暗 | 添加 `dynamicSchemeVariant: .fidelity` |

---

## 相关链接

- [Material 3 迁移指南](https://flutter.cn/ui/design/material)
- [ColorScheme.fromSeed API](https://api.flutter.cn/flutter/material/ColorScheme/fromSeed.html)
- [Material Color Utilities 包](https://pub.dev/packages/material_color_utilities)
- [Flutter Material 3 Demo](https://github.com/flutter/samples/tree/main/material_3_demo)
