---
name: material-design-foundations
description: Google Material Design 3 设计原则与自适应布局完整参考。
source: https://m3.material.io/foundations
---

# Material Design 3 Foundations

Material Design 3 (M3) 是一个适应性设计系统，包含指南、组件和工具，支持界面设计的最佳实践。

## M3 Design Principles

### Expressive
M3 通过颜色、排版、形状和动态效果实现品牌表达。
- **颜色系统**: 支持动态颜色和个性化配色方案，26+ 颜色角色映射到组件
- **排版**: 15 个基础类型样式 + 15 个强调类型样式，支持可变字体
- **形状系统**: 35 种预设形状，支持形状渐变（morphing）
- **动态效果**: 基于内容和用户偏好的自适应视觉体验

### Responsive
响应式设计使产品可在不同设备和使用场景下使用。
- 窗格（Pane）作为布局构建块
- 窗口尺寸类别（Window Size Classes）自适应布局
- 支持折叠屏、多屏幕、多窗口等复杂场景

### Accessible
无障碍设计让具有不同能力的用户都能导航、理解和使用界面。
- 内置可访问的颜色对比关系
- 支持三种对比度级别
- 动态颜色自动保持可访问的对比度

---

## Adaptive Design

### What Does Adaptive Mean?

自适应设计是一系列技术，允许界面响应以下上下文：

| Context Type | Examples |
|--------------|----------|
| **User** | 用户偏好和设置 |
| **Device** | 手表、手机、折叠屏、平板、桌面、XR 设备 |
| **Usage** | 窗口调整、方向改变、设备切换 |

### Conditions

条件是决定应用何时以及如何适配的信号。Material 自适应系统支持三类条件：

#### Device Conditions
- 全屏环境
- 窗口化环境
- 空间化环境
- 设备姿态（如折叠状态）

#### Window Size Conditions
- **窗口尺寸类别**（Window Size Classes）
- 屏幕方向（横屏/竖屏）

#### Input Modality Conditions
- 触摸
- 手写笔
- 外设
- 眼动追踪
- 手部追踪

### Window Size Classes

| Size Class | Breakpoint | Typical Devices |
|------------|------------|-----------------|
| **Compact** | < 600dp | 手机、折叠屏内屏 |
| **Medium** | 600dp - 840dp | 折叠屏外屏、小平板 |
| **Expanded** | > 840dp | 大平板、桌面显示器 |

### Layout Patterns

#### Pane-Based Layout
窗格是布局的构建块，每个窗格是产品中的单一目的地。

**示例 - 消息应用：**
- 窗格 1: 消息列表
- 窗格 2: 特定对话线程

#### Layout Behavior by Window Size

**Compact (< 600dp)**
```
┌─────────────────┐
│                 │
│    Single       │
│    Pane         │
│                 │
└─────────────────┘
```

**Medium (600dp - 840dp)**
```
┌─────────┬───────┐
│         │       │
│  List   │ Detail│
│  Pane   │ Pane  │
│         │       │
└─────────┴───────┘
```

**Expanded (> 840dp)**
```
┌─────┬─────────┬───────┐
│ Nav │  List   │ Detail│
│     │  Pane   │ Pane  │
│     │         │       │
└─────┴─────────┴───────┘
```

---

## Grid System & Layout Principles

### Layout Foundation

布局是元素在屏幕上的视觉排列。M3 布局系统基于以下原则：

1. **可见性**: 内容根据窗口尺寸和条件显示或隐藏
2. **空间**: 元素间距和对齐遵循 4dp/8dp 网格系统
3. **层次**: 通过海拔（Elevation）和色调区分内容层次

### Responsive Grid

| Window Size | Column Count | Gutter | Margin |
|-------------|--------------|--------|--------|
| Compact     | 4            | 16dp   | 16dp   |
| Medium      | 8            | 24dp   | 24dp   |
| Expanded    | 12           | 24dp   | 24dp   |

---

## Accessibility Guidelines

### Core Principles
- **可感知**: 信息和UI组件必须以用户可感知的方式呈现
- **可操作**: UI组件和导航必须可操作
- **可理解**: 信息和UI操作必须可理解
- **健壮**: 内容必须能被各种用户代理（包括辅助技术）解释

### Color Accessibility
- 所有颜色组合需满足 WCAG 2.1 对比度要求
- M3 提供三种对比度级别供用户选择
- 动态颜色自动保持可访问对比度

### Typography Accessibility
- 支持系统字体缩放
- 强调样式用于突出重要内容而非唯一信息载体
- 文本可调整大小（最大 200%）

### Interaction States
交互元素需明确传达状态：
- **Default**: 正常状态
- **Hover**: 悬停状态
- **Pressed**: 按下状态
- **Focused**: 焦点状态
- **Disabled**: 禁用状态
- **Drag**: 拖拽状态

---

## Platform-Specific Considerations

### Mobile (Phone)
- 触控优先交互
- 紧凑布局（单窗格）
- 底部导航或导航栏
- 手势导航支持

### Tablet
- 可使用触控或键盘交互
- 中等布局（双窗格列表/详情）
- 导航导轨（Navigation Rail）
- 支持分屏多任务

### Desktop
- 精确指针交互
- 展开布局（三窗格）
- 顶部应用栏或导航抽屉
- 窗口调整支持

### Large Screen / Foldable
- 最大化显示空间利用
- 动态布局调整
- 多任务分屏支持
- 铰链区域考虑

### Wear / XR
- 特定设备姿态支持
- 空间化环境适配
- 眼动/手部追踪输入
- 3D 深度和海拔表现

---

## Design Tokens

Tokens 存储样式值（颜色、字体等），确保相同值可用于跨设计、代码、工具和平台。

### Token Categories
| Category | Examples |
|----------|----------|
| **Color** | Primary, Secondary, Surface, Error |
| **Typography** | Font family, Size, Weight, Line height |
| **Shape** | Corner radius, Family |
| **Elevation** | Level 0-24, Tint/opacity values |
| **Spacing** | 4dp, 8dp, 16dp increments |

---

## Design System Overview

### Building for Everyone
Material Design 为具有不同能力的用户设计，包含内置无障碍功能。

### Customizing Material
M3 使品牌表达比以往更简单、更美观：
- 动态颜色生成
- 可配置的组件变体
- 主题化 API

### Material A-Z
关键术语和概念索引，帮助理解 Material Design 完整体系。

---

*Source: [Material Design 3 Foundations](https://m3.material.io/foundations)*
