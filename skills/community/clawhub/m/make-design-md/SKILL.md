---
name: make-design-md
description: 网站设计风格分析器，从网站URL、HTML文件或截图提取设计规范，生成符合 Google design.md 规范的 DESIGN.md 文档。当用户要求"分析设计风格"、"提取设计规范"、"生成设计文档"、"从XX网站提取风格"、"分析这个页面的设计"等任务时触发此skill。也支持用户直接提供URL、HTML文件路径或截图文件作为输入。
---

# Make Design MD

从网站、HTML文件或截图分析设计风格，生成符合 [Google design.md 规范](https://github.com/google-labs-code/design.md) 的结构化 DESIGN.md 设计规范文档。

## 规范说明

本技能遵循 Google 开源的 design.md 规范，生成的文档包含：

1. **YAML Front Matter** - 机器可读的设计令牌（colors, typography, spacing, rounded, components）
2. **Markdown Body** - 人类可读的设计原理说明

生成的 DESIGN.md 可通过官方 CLI 工具验证和导出：
```bash
npx @google/design.md lint DESIGN.md        # 验证格式
npx @google/design.md export --format tailwind DESIGN.md  # 导出 Tailwind 配置
```

## 工作流程

### 输入类型判断

根据用户提供的输入类型选择相应的分析路径：

| 输入类型 | 识别方式 | 处理方法 |
|---------|---------|---------|
| 网站URL | 以 http:// 或 https:// 开头 | 使用 WebFetch 抓取页面内容 |
| HTML文件 | 以 .html 或 .htm 结尾的文件路径 | 使用 Read 工具读取文件 |
| 截图文件 | 以 .png、.jpg、.jpeg、.webp 结尾 | 使用 Read 工具查看图片 |

### 分析流程

1. **获取内容**
   - URL：使用 WebFetch 抓取页面 HTML
   - HTML文件：使用 Read 工具读取
   - 截图：使用 Read 工具查看并分析视觉元素

2. **提取设计令牌**

   从内容中提取以下设计令牌：

   **colors** - 颜色系统
   - `primary` - 主品牌色（必须）
   - `secondary` - 次级强调色
   - `background` - 背景色（可包含多个层级如 `background-subtle`）
   - `surface` - 表面色（卡片、面板）
   - `text` - 文字色（main, muted, subtle）
   - `border` - 边框色
   - `success`, `warning`, `error`, `info` - 状态色

   **typography** - 字体排版对象
   每个排版角色包含：`fontFamily`, `fontSize`, `fontWeight`, `lineHeight`, `letterSpacing`
   ```yaml
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
     body:
       fontFamily: "Inter, system-ui, sans-serif"
       fontSize: "16px"
       fontWeight: "400"
       lineHeight: "1.5"
   ```

   **spacing** - 间距刻度
   ```yaml
   spacing:
     0: "0"
     1: "4px"
     2: "8px"
     3: "12px"
     4: "16px"
     5: "24px"
     6: "32px"
     8: "48px"
     10: "64px"
   ```

   **rounded** - 圆角刻度
   ```yaml
   rounded:
     none: "0"
     sm: "4px"
     md: "8px"
     lg: "12px"
     xl: "16px"
     2xl: "24px"
     full: "9999px"
   ```

   **components** - 组件样式（使用令牌引用）
   ```yaml
   components:
     button-primary:
       backgroundColor: "{colors.primary}"
       textColor: "#ffffff"
       typography: "{typography.body}"
       rounded: "{rounded.md}"
       padding: "{spacing.2} {spacing.4}"
     card:
       backgroundColor: "{colors.surface}"
       borderColor: "{colors.border}"
       rounded: "{rounded.lg}"
   ```

3. **生成 DESIGN.md**

   按照以下结构生成文档：

   ```markdown
   ---
   version: "alpha"
   name: "设计系统名称"
   description: "简短描述"
   colors:
     primary: "#533afd"
     background: "#ffffff"
     text-main: "#1a1a1a"
     # ...
   typography:
     display:
       fontFamily: "Inter, sans-serif"
       fontSize: "64px"
       fontWeight: "700"
       lineHeight: "1.0"
     # ...
   spacing:
     1: "4px"
     2: "8px"
     # ...
   rounded:
     sm: "4px"
     md: "8px"
     # ...
   components:
     button-primary:
       backgroundColor: "{colors.primary}"
       textColor: "#ffffff"
   ---

   ## Overview

   设计系统概述和视觉哲学...

   ## Colors

   颜色系统详细说明...

   ## Typography

   字体排版说明...

   ## Layout

   布局与间距说明...

   ## Elevation & Depth

   阴影与层级说明...

   ## Shapes

   圆角与形状说明...

   ## Components

   组件样式说明...

   ## Do's and Don'ts

   设计宜忌...
   ```

4. **生成预览文件**

   同时生成 HTML 预览文件，从 YAML front matter 提取令牌值：

   **preview.html** - 浅色/默认模式预览
   **preview-dark.html** - 深色模式预览（如适用）

   **字体 CDN 替换规则（必须遵循）**

   生成网页/预览文件时，若引用 Google Fonts，必须使用国内镜像自动替换：
   - `fonts.googleapis.com` → `fonts.loli.net`
   - `fonts.gstatic.com` → `gstatic.loli.net`

   ```html
   <!-- 错误 -->
   <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
   <!-- 正确 -->
   <link href="https://fonts.loli.net/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
   ```

   ```css
   :root {
     --color-primary: #533afd;
     --color-background: #ffffff;
     --spacing-1: 4px;
     --spacing-2: 8px;
     --rounded-md: 8px;
   }
   ```

### 章节顺序（必须遵循）

按 Google design.md 规范，章节必须按以下顺序排列：

| 顺序 | 章节名 | 别名 |
|-----|--------|------|
| 1 | Overview | Brand & Style |
| 2 | Colors | - |
| 3 | Typography | - |
| 4 | Layout | Layout & Spacing |
| 5 | Elevation & Depth | Elevation |
| 6 | Shapes | - |
| 7 | Components | - |
| 8 | Do's and Don'ts | - |

### 令牌格式规范

**颜色 (Color)**
- 格式：`#` + 十六进制（sRGB）
- 示例：`#1A1C1E`, `#FF5722`
- RGBA 格式：`rgba(0, 0, 0, 0.8)`

**尺寸 (Dimension)**
- 格式：数字 + 单位（`px`, `em`, `rem`）
- 示例：`48px`, `1.5rem`, `-0.02em`

**令牌引用**
- 格式：`{path.to.token}`
- 示例：`{colors.primary}`, `{typography.body.fontSize}`, `{spacing.4}`

**排版对象 (Typography)**
```yaml
heading1:
  fontFamily: "Inter, system-ui, sans-serif"
  fontSize: "48px"
  fontWeight: "700"
  lineHeight: "1.1"
  letterSpacing: "-0.02em"        # 可选
  fontFeature: "\"calt\", \"kern\""  # 可选
  fontVariation: "\"wght\" 400"      # 可选
```

### 分析技巧

**从 CSS 提取**
- 查找 `<style>` 标签内的样式
- 分析 `style` 属性中的内联样式
- 识别 CSS 变量（`--color-primary` 等）
- 提取 Tailwind/CSS 框架的类名

**从视觉推断（截图）**
- 使用颜色提取识别主色调
- 观察字体风格推断字体族
- 测量间距规律
- 分析组件形态

**从 HTML 结构推断**
- 语义化标签暗示布局意图
- class 名称可能包含设计信息
- 嵌套层级反映视觉层级

### 验证与导出

生成的 DESIGN.md 可使用 Google 官方 CLI 工具：

```bash
# 验证文档格式
npx @google/design.md lint DESIGN.md

# 比较两个版本
npx @google/design.md diff DESIGN.md DESIGN-v2.md

# 导出为 Tailwind 配置
npx @google/design.md export --format tailwind DESIGN.md

# 导出为 DTCG 格式
npx @google/design.md export --format dtcg DESIGN.md

# 查看规范
npx @google/design.md spec
```

**Lint 规则说明**
- `broken-ref` - 令牌引用无法解析
- `missing-primary` - 未定义 primary 颜色
- `contrast-ratio` - WCAG AA 对比度检查
- `orphaned-tokens` - 未使用的颜色令牌
- `section-order` - 章节顺序不符合规范

## 使用示例

**分析网站 URL**
```
分析 https://linear.app 的设计风格，生成 DESIGN.md
```

**分析本地 HTML**
```
分析 ./dist/index.html 的设计风格
```

**分析截图**
```
分析 ./screenshots/homepage.png 的设计风格
```

**生成后验证**
```
生成 DESIGN.md 后用 Google CLI 验证格式是否正确
```

**导出为 Tailwind 配置**
```
将 DESIGN.md 导出为 tailwind.config.js
```

## 资源

- `references/design-template.md` - DESIGN.md 文档模板结构
- [Google design.md 规范](https://github.com/google-labs-code/design.md) - 官方规范仓库
