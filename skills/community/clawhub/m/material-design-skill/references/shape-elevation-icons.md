---
name: material-design-shape-elevation
description: Google Material Design 3 形状、Elevation、图标系统完整参考。
source: https://m3.material.io/styles/shape/overview
---

# Material Design 3 — Shape, Elevation & Icons

## Shape System

### Overview

M3 形状系统包含 35 种预设形状、圆角半径刻度和形状渐变（Shape Morph）功能。

**核心原则：**
- 形状与文字和谐使用
- 通过形状渐变连接功能与情感
- 大胆运用张力
- 形状是表现性的，非语义性的
- 抽象形状仅用于强调时刻
- 形状可以是 2.5D

### 圆角半径刻度（Corner Radius Scale）

| 样式 | Token | 值 |
|------|-------|-----|
| None | `none` | 0dp |
| Extra Small | `extraSmall` | 4dp |
| Small | `small` | 8dp |
| Medium | `medium` | 12dp |
| Large | `large` | 16dp |
| Large Increased | `largeIncreased` | 20dp |
| Extra Large | `extraLarge` | 28dp |
| Extra Large Increased | `extraLargeIncreased` | 32dp |
| Extra Extra Large | `extraExtraLarge` | 48dp |
| Full | `full` | 完全圆角 |

**说明：** M3 Expressive 更新（2025年5月）新增了 Large Increased (20dp)、Extra Large Increased (32dp)、Extra Extra Large (48dp) 三个刻度，并将"完全圆角"从 50% 改为 `full` token。

### 形状 Tokens

| 形状 Token | 描述 |
|-----------|------|
| `fullyRounded` | 四角完全圆角 |
| `extraLargeTopRounding` | 顶部圆角加大 |
| `extraLargeRounding` | 整体加大圆角 |
| `largeTopRounding` | 顶部大圆角 |
| `largeEndRounding` | 末端大圆角 |
| `largeStartRounding` | 首端大圆角 |
| `largeRounding` | 整体大圆角 |
| `mediumRounding` | 中等圆角 |
| `smallRounding` | 小圆角 |
| `extraSmallTopRounding` | 顶部小圆角 |
| `extraSmallRounding` | 整体小圆角 |
| `noRounding` | 无圆角 |
| `largeIncreasedRounding` | 增大圆角 |
| `extraLargeIncreasedRounding` | 超大增大圆角 |
| `extraExtraLargeRounding` | 超超大圆角 |

### 资源

| 平台 | 资源 | 状态 |
|------|------|------|
| Design | Shape Library (Figma Design Kit) | Available |
| Implementation | Jetpack Compose (Shape Library) | Available |
| Android | MDC-Android | Available |

---

## Elevation 系统

### Overview

Elevation 表示两个表面在 z 轴上的距离，以 dps（密度无关像素）为单位。

**核心原则：**
- 所有表面和组件都有 Elevation 值
- Tokens 编码 z 轴距离，确保组件相对关系一致
- Tokens 本身不含阴影或颜色，由各平台实现
- Elevation 可通过色调表面颜色或阴影显示
- 避免修改 Material 3 组件的默认 Elevation
- 使用少量 Elevation 级别

### Elevation 级别

| Level | Token | 用途 |
|-------|-------|------|
| 0 | `level0` / `none` | 背景表面 |
| 1 | `level1` | 表面 |
| 2 | `level2` | 导航组件 |
| 3 | `level3` | 组件（如 FAB） |
| 4 | `level4` | 模态组件 |
| 5 | `level5` | 对话框 |

**注意：** M2 与 M3 的关键区别：
- **阴影**：M3 仅在需要创建额外保护或鼓励交互时才使用阴影
- **颜色**：新的颜色映射，支持动态配色

### 资源

| 平台 | 资源 | 状态 |
|------|------|------|
| Design | Design Kit (Figma) | Available |
| Implementation | Flutter | Available |
| Implementation | Jetpack Compose | Available |
| Implementation | MDC-Android | Available |
| Implementation | MWC-Web | Available |

---

## Icons 系统

### Overview

Material Icons 是用于识别操作和类别的微小符号。现已升级为 **Material Symbols** 可变字体。

### Material Symbols 样式

| 样式 | 描述 |
|------|------|
| Outlined | 描边风格 |
| Rounded | 圆角风格 |
| Sharp | 锐利风格 |

### 可调轴（Adjustable Axes）

Material Symbols 有四个可调属性：

| 轴 | 描述 |
|----|------|
| Weight | 字重（粗细） |
| Fill | 填充程度 |
| Optical Size | 光学尺寸 |
| Grade | 等级（灰度级别） |

### 图标尺寸

| 场景 | 推荐尺寸 |
|------|----------|
| 界面图标 (UI Icons) | 24dp |
| 触控目标 | 最小 48×48dp |
| 密集布局 | 20dp |
| 装饰性图标 | 16dp |

### 使用指南

- 通过 fonts.google.com/icons 获取 Material Symbols
- 使用 Material Symbols 可变字体实现动态样式
- 可在 Figma 中使用 Material Symbols 插件
- 支持复制粘贴自定义图标（调整大小、颜色后）

### 资源

| 类型 | 资源 | 状态 |
|------|------|------|
| Design | Icons Catalog | Available |
| Design | Material Symbols Figma Plugin | Available |
| Design | Icon Keyline Template (ZIP) | Available |

---

## 平台实现

### Jetpack Compose

```kotlin
// Shape
shape = RoundedCornerShape(16.dp)

// Elevation
Modifier.shadow(elevation = 8.dp)

// Icon
Icon(
    imageVector = Icons.Filled.Star,
    contentDescription = "Star"
)
```

### Android (MDC)

```xml
<!-- Shape -->
app:shapeAppearanceOverlay="@style/ShapeAppearance.Material3.LargeComponent"

<!-- Elevation -->
android:elevation="8dp"
```

### Flutter

```dart
// Shape
shape: RoundedRectangleBorder(
  borderRadius: BorderRadius.circular(16),
)

// Elevation
elevation: 8.0

// Icon
Icon(Icons.star)
```

### Web (MWC)

```html
<!-- Shape -->
<m3-elevated-button shape="large"></m3-elevated-button>

<!-- Elevation -->
<div style="elevation: 8dp"></div>
```
