---
name: make-design-md
description: 网站设计风格分析器，从网站URL、HTML文件或截图提取设计规范，生成符合 Google design.md 规范的 DESIGN.md 文档。当用户要求"分析设计风格"、"提取设计规范"、"生成设计文档"、"从XX网站提取风格"、"分析这个页面的设计"等任务时触发此skill。也支持用户直接提供URL、HTML文件路径或截图文件作为输入。
license: MIT
---

# Make Design MD

从网站、HTML文件或截图分析设计风格，生成符合 [Google design.md 规范](https://github.com/google-labs-code/design.md) 的结构化 DESIGN.md 设计规范文档。

## 规范说明

本技能遵循 Google 开源的 design.md 规范，生成的文档包含：

1. **YAML Front Matter** - 机器可读的设计令牌（colors, typography, spacing, rounded, components）
2. **Markdown Body** - 人类可读的设计原理说明

生成的 DESIGN.md 可通过官方 CLI 工具（当前版本 0.3.x）验证和导出：
```bash
npx @google/design.md lint DESIGN.md                     # 验证格式（JSON 输出）
npx @google/design.md export --format css-tailwind DESIGN.md  # 导出 Tailwind v4 主题
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
   - `primary-hover` - 主色悬停态（配合组件变体使用）
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
     none: "0px"
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
     button-primary-hover:
       backgroundColor: "{colors.primary-hover}"
     card:
       backgroundColor: "{colors.surface}"
       borderColor: "{colors.border}"
       rounded: "{rounded.lg}"
   ```

   组件属性的规范清单：`backgroundColor`, `textColor`, `typography`, `rounded`, `padding`, `size`, `height`, `width`。其他属性（如 `borderColor`, `backdropFilter`）会被接受但 lint 时给出警告，非必要时优先使用规范内属性。

   交互状态变体（hover、active、pressed）以独立的组件条目表示，命名与基础组件相关联（如 `button-primary-hover`）。

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
- 格式：任意 CSS 颜色（hex、`rgb()`、`rgba()`、`oklch()`、命名颜色等）
- 示例：`#1A1C1E`, `#FF5722`, `rgba(0, 0, 0, 0.8)`, `oklch(62% 0.18 250)`

**尺寸 (Dimension)**
- 格式：数字 + 单位（`px`, `em`, `rem`）；spacing 令牌也允许纯数字
- 示例：`48px`, `1.5rem`, `-0.02em`
- 注意：无单位的 `"0"` 不是合法 dimension（lint 报错），零值需写成 `"0px"`

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

生成的 DESIGN.md 可使用 Google 官方 CLI 工具（所有命令接受文件路径或 `-` 表示 stdin，输出默认为 JSON）：

```bash
# 验证文档格式（存在 error 时退出码为 1）
npx @google/design.md lint DESIGN.md

# 比较两个版本（after 文件 findings 变多时退出码为 1）
npx @google/design.md diff DESIGN.md DESIGN-v2.md

# 导出为 Tailwind v3 配置（theme.extend JSON）
npx @google/design.md export --format json-tailwind DESIGN.md

# 导出为 Tailwind v4 主题（CSS @theme 块）
npx @google/design.md export --format css-tailwind DESIGN.md

# 导出为 DTCG 格式（W3C Design Tokens Format）
npx @google/design.md export --format dtcg DESIGN.md

# 查看规范（可注入 agent prompt）
npx @google/design.md spec
```

**注意事项**
- `--format tailwind` 是 `json-tailwind` 的兼容别名。
- **Windows/PowerShell**：`design.md` 这个 bin 名的 `.md` 后缀会与 Windows 的 Markdown 文件关联冲突，导致 `npx @google/design.md` 无输出。改用无点的 `designmd` 别名：`npx -p @google/design.md designmd lint DESIGN.md`。
- **`npm error ENOVERSIONS`**：说明 npm 未查询公共 registry（`.npmrc` 自定义了 registry 或公司镜像未同步该包）。用 `npm config get registry` 检查，正常应为 `https://registry.npmjs.org/`。

**Lint 规则说明**（共 9 条规则）

| 规则 | 级别 | 检查内容 |
|------|------|---------|
| `broken-ref` | error | 令牌引用无法解析（如 `{colors.primary}` 未定义） |
| `missing-primary` | warning | 定义了 colors 但缺少 primary 颜色 |
| `contrast-ratio` | warning | 组件背景/文字对比度低于 WCAG AA（4.5:1） |
| `orphaned-tokens` | warning | 定义了但未被任何组件引用的颜色令牌 |
| `token-summary` | info | 各部分的令牌数量统计 |
| `missing-sections` | info | 存在其他令牌但缺少可选部分（spacing、rounded） |
| `missing-typography` | warning | 定义了 colors 但没有 typography 令牌 |
| `section-order` | warning | 章节顺序不符合规范 |
| `unknown-key` | warning | 顶层 YAML 键疑似已知 schema 键的拼写错误 |

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
