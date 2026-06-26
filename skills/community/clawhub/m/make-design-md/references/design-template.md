# DESIGN.md 模板

此模板遵循 [Google design.md 规范](https://github.com/google-labs-code/design.md)，定义了设计规范文档的标准结构。

## YAML Front Matter 结构

每个 DESIGN.md 必须以 YAML front matter 开头，包含机器可读的设计令牌：

```yaml
---
version: "alpha"                    # 可选，当前版本为 "alpha"
name: "设计系统名称"
description: "简短描述"             # 可选
colors:
  primary: "#533afd"                # 必须：主品牌色
  secondary: "#00d4ff"
  background: "#ffffff"
  background-subtle: "#f5f5f7"
  surface: "#ffffff"
  surface-elevated: "#ffffff"
  text-main: "#1a1a1a"
  text-muted: "#6b6b6b"
  text-subtle: "#999999"
  border: "#e5e5e5"
  border-subtle: "#f0f0f0"
  success: "#22c55e"
  warning: "#f59e0b"
  error: "#ef4444"
  info: "#3b82f6"
typography:
  display:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: "64px"
    fontWeight: "700"
    lineHeight: "1.0"
    letterSpacing: "-0.04em"
  heading1:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: "48px"
    fontWeight: "700"
    lineHeight: "1.1"
    letterSpacing: "-0.02em"
  heading2:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: "36px"
    fontWeight: "600"
    lineHeight: "1.2"
    letterSpacing: "-0.01em"
  heading3:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: "24px"
    fontWeight: "600"
    lineHeight: "1.3"
  heading4:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: "18px"
    fontWeight: "600"
    lineHeight: "1.4"
  body:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: "16px"
    fontWeight: "400"
    lineHeight: "1.5"
  body-small:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: "14px"
    fontWeight: "400"
    lineHeight: "1.5"
  caption:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: "12px"
    fontWeight: "400"
    lineHeight: "1.4"
  code:
    fontFamily: "JetBrains Mono, Consolas, monospace"
    fontSize: "14px"
    fontWeight: "400"
    lineHeight: "1.6"
spacing:
  0: "0"
  0.5: "2px"
  1: "4px"
  1.5: "6px"
  2: "8px"
  3: "12px"
  4: "16px"
  5: "20px"
  6: "24px"
  8: "32px"
  10: "40px"
  12: "48px"
  16: "64px"
  20: "80px"
rounded:
  none: "0"
  sm: "4px"
  md: "8px"
  lg: "12px"
  xl: "16px"
  2xl: "24px"
  3xl: "32px"
  full: "9999px"
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "#ffffff"
    typography: "{typography.body}"
    rounded: "{rounded.md}"
    padding: "{spacing.2} {spacing.4}"
    height: "40px"
  button-secondary:
    backgroundColor: "transparent"
    textColor: "{colors.primary}"
    borderColor: "{colors.border}"
    rounded: "{rounded.md}"
    padding: "{spacing.2} {spacing.4}"
  card:
    backgroundColor: "{colors.surface}"
    borderColor: "{colors.border}"
    rounded: "{rounded.lg}"
    padding: "{spacing.4}"
  input:
    backgroundColor: "{colors.background}"
    textColor: "{colors.text-main}"
    borderColor: "{colors.border}"
    rounded: "{rounded.md}"
    padding: "{spacing.2} {spacing.3}"
    height: "40px"
---
```

## Markdown Body 章节顺序

章节必须按以下顺序排列（Google design.md 规范强制要求）：

### 1. Overview（别名：Brand & Style）

设计系统概述，描述整体设计哲学和视觉印象：

```markdown
## Overview

[设计系统名称] 是一个 [风格定位] 的设计系统。

**视觉哲学**
- 设计风格定位（极简、奢华、技术感、温暖等）
- 整体视觉印象（深色/浅色优先、色彩策略等）
- 关键视觉特征列表

**设计原则**
1. 原则一：说明
2. 原则二：说明
```

### 2. Colors

详细记录颜色系统：

```markdown
## Colors

### 品牌色

| 名称 | 值 | 用途 |
|------|-----|------|
| Primary | `#533afd` | 主要品牌色、CTA 按钮 |
| Secondary | `#00d4ff` | 次级强调、链接 |

### 背景与表面

| 名称 | 值 | 用途 |
|------|-----|------|
| Background | `#ffffff` | 页面主背景 |
| Background Subtle | `#f5f5f7` | 次级背景区域 |
| Surface | `#ffffff` | 卡片、面板背景 |

### 文字颜色

| 名称 | 值 | 用途 |
|------|-----|------|
| Text Main | `#1a1a1a` | 主要文字、标题 |
| Text Muted | `#6b6b6b` | 次要文字、描述 |
| Text Subtle | `#999999` | 占位符、禁用状态 |

### 状态色

| 名称 | 值 | 用途 |
|------|-----|------|
| Success | `#22c55e` | 成功状态 |
| Warning | `#f59e0b` | 警告状态 |
| Error | `#ef4444` | 错误状态 |
```

### 3. Typography

字体排版规则：

```markdown
## Typography

### 字体族

**主字体**：Inter（无衬线，现代几何风格）
**等宽字体**：JetBrains Mono（代码展示）

### 排版层级

| 角色 | 字号 | 字重 | 行高 | 字间距 | 用途 |
|------|------|------|------|--------|------|
| Display | 64px | 700 | 1.0 | -0.04em | 首屏大标题 |
| H1 | 48px | 700 | 1.1 | -0.02em | 页面主标题 |
| H2 | 36px | 600 | 1.2 | -0.01em | 章节标题 |
| H3 | 24px | 600 | 1.3 | - | 卡片标题 |
| H4 | 18px | 600 | 1.4 | - | 小节标题 |
| Body | 16px | 400 | 1.5 | - | 正文内容 |
| Small | 14px | 400 | 1.5 | - | 辅助信息 |
| Caption | 12px | 400 | 1.4 | - | 标签、时间戳 |

### 排版原则

- 标题使用紧密的字间距（负值）增强冲击力
- 正文保持舒适行高（1.5）提升可读性
- 字重仅使用 400、600、700 三个档位
```

### 4. Layout（别名：Layout & Spacing）

布局与间距系统：

```markdown
## Layout

### 间距刻度

基于 4px 基础单位的间距系统：

| 级别 | 值 | 用途 |
|------|-----|------|
| 1 | 4px | 紧凑元素间距 |
| 2 | 8px | 相关元素间距 |
| 3 | 12px | 组件内间距 |
| 4 | 16px | 标准内边距 |
| 6 | 24px | 区块间距 |
| 8 | 32px | 大区块间距 |

### 网格系统

- 最大内容宽度：1200px
- 列数：12 列
- 列间距：24px
- 边距：16px（移动端）/ 24px（桌面端）

### 断点

| 名称 | 宽度 | 用途 |
|------|------|------|
| Mobile | < 640px | 手机竖屏 |
| Tablet | 640-1024px | 平板/小屏笔记本 |
| Desktop | > 1024px | 桌面端 |
```

### 5. Elevation & Depth（别名：Elevation）

阴影与层级系统：

```markdown
## Elevation & Depth

### 阴影层级

| 级别 | 阴影值 | 用途 |
|------|--------|------|
| Subtle | `0 1px 2px rgba(0,0,0,0.05)` | 卡片默认状态 |
| Medium | `0 4px 12px rgba(0,0,0,0.1)` | 悬停状态、下拉菜单 |
| High | `0 8px 24px rgba(0,0,0,0.15)` | 模态框、弹窗 |

### 层级原则

- 扁平优先：尽量减少阴影使用
- 语义层级：通过背景色差异表达层级
- 交互反馈：悬停时增加阴影深度
```

### 6. Shapes

圆角与形状系统：

```markdown
## Shapes

### 圆角刻度

| 级别 | 值 | 用途 |
|------|-----|------|
| none | 0 | 无圆角 |
| sm | 4px | 小按钮、标签 |
| md | 8px | 输入框、按钮 |
| lg | 12px | 卡片 |
| xl | 16px | 大卡片、模态框 |
| 2xl | 24px | 特殊容器 |
| full | 9999px | 胶囊形状、头像 |

### 形状原则

- 按钮和输入框使用统一圆角（8px）
- 卡片使用较大圆角（12px）增强柔和感
- 头像和徽章使用完全圆形
```

### 7. Components

组件样式详细说明：

```markdown
## Components

### 按钮

**主要按钮**
- 背景：`{colors.primary}`
- 文字：`#ffffff`
- 圆角：`{rounded.md}`
- 高度：40px
- 内边距：8px 16px

**次要按钮**
- 背景：透明
- 文字：`{colors.primary}`
- 边框：`{colors.border}`
- 圆角：`{rounded.md}`

**幽灵按钮**
- 背景：透明
- 文字：`{colors.text-main}`
- 无边框
- 悬停时背景：`{colors.background-subtle}`

### 卡片

- 背景：`{colors.surface}`
- 边框：`{colors.border}`（可选）
- 圆角：`{rounded.lg}`
- 内边距：`{spacing.4}`
- 阴影：Subtle（默认）→ Medium（悬停）

### 输入框

- 背景：`{colors.background}`
- 边框：`{colors.border}`
- 圆角：`{rounded.md}`
- 高度：40px
- 聚焦边框：`{colors.primary}`

### 徽章

- 背景：`{colors.primary}`（透明度 10%）
- 文字：`{colors.primary}`
- 圆角：`{rounded.full}`
- 内边距：4px 12px
```

### 8. Do's and Don'ts

设计宜忌：

```markdown
## Do's and Don'ts

### ✅ Do

- 使用一致的间距刻度（4px 倍数）
- 标题使用负字间距增强可读性
- 保持按钮最小点击区域 44px
- 卡片悬停时提供视觉反馈
- 使用语义化的颜色名称

### ❌ Don't

- 不要混用多种主品牌色
- 不要在正文使用负字间距
- 不要使用纯黑（#000）作为文字颜色
- 不要过度使用阴影效果
- 不要忽略对比度要求（WCAG AA）
```

## 完整示例

```markdown
---
version: "alpha"
name: "Atmospheric Glass"
description: "A glassmorphism weather app with frosted crystalline UI"
colors:
  primary: "#60A5FA"
  secondary: "#818CF8"
  background: "#0F172A"
  background-glass: "rgba(255, 255, 255, 0.1)"
  text-main: "#F8FAFC"
  text-muted: "#94A3B8"
typography:
  display:
    fontFamily: "Inter, sans-serif"
    fontSize: "72px"
    fontWeight: "200"
    lineHeight: "1.0"
  body:
    fontFamily: "Inter, sans-serif"
    fontSize: "16px"
    fontWeight: "400"
    lineHeight: "1.5"
spacing:
  1: "4px"
  2: "8px"
  4: "16px"
  6: "24px"
rounded:
  md: "8px"
  lg: "16px"
  xl: "24px"
components:
  glass-card:
    backgroundColor: "rgba(255, 255, 255, 0.1)"
    backdropFilter: "blur(20px)"
    rounded: "{rounded.xl}"
    border: "1px solid rgba(255, 255, 255, 0.2)"
---

## Overview

Atmospheric Glass captures the ethereal beauty of weather through a glassmorphism aesthetic...

## Colors

[颜色说明...]

## Typography

[排版说明...]

[...其余章节...]
```

## 验证

使用 Google CLI 工具验证生成的 DESIGN.md：

```bash
npx @google/design.md lint DESIGN.md
```

常见 lint 错误：
- `broken-ref` - 令牌引用无法解析
- `missing-primary` - 缺少 primary 颜色定义
- `contrast-ratio` - 颜色对比度不符合 WCAG AA
- `orphaned-tokens` - 存在未使用的颜色令牌
- `section-order` - 章节顺序不符合规范
