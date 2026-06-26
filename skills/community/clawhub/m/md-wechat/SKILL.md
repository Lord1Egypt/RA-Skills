---
name: md-wechat
description: 将 Markdown 文档转换为微信公众号格式的技能。当用户需要将 Markdown 文件排版为微信公众号文章格式时使用此技能。支持自定义主题、字体、颜色、代码高亮等配置。触发词：微信排版、公众号格式、md转微信、markdown转wechat、公众号文章。
---

# 微信 Markdown 排版 (md-wechat)

## Overview

将 Markdown 文档转换为适配微信公众号的 HTML 格式。支持三种预设主题（经典、优雅、简洁），可自定义字体、颜色、代码高亮等样式，生成的 HTML 可直接复制粘贴到微信公众号编辑器使用。

**版本 2.0.0** - 使用 Node.js 重写，完整支持所有功能！

## 核心功能

### 基础语法
- **标题**：h1-h6，带样式装饰
- **段落**：自动排版，支持缩进和两端对齐
- **列表**：有序/无序列表，支持嵌套
- **引用**：单层和多级嵌套引用
- **表格**：GFM 表格语法
- **分隔线**：水平分割线

### 扩展语法
- **删除线**：`~~删除线~~`
- **高亮**：`==高亮==`
- **下划线**：`++下划线++`
- **Ruby 注音**：`[文字]{注音}` 或 `[文字]^(注音)`

### 高级功能
- **代码高亮**：使用 highlight.js，支持 100+ 语言
- **Mac 风格代码块**：带红黄绿装饰按钮
- **数学公式**：KaTeX 渲染，支持行内和块级公式
- **Mermaid 图表**：流程图、时序图、饼图等
- **PlantUML 图表**：UML 类图、时序图等
- **Infographic 信息图**：数据可视化图表

## Workflow

### 1. 环境准备

**前提条件**：Node.js >= 18.0.0

**推荐安装方式（更安全）**：
```bash
# 手动安装依赖，可审查 package.json
npm install

# 然后运行转换
node scripts/convert.js article.md --no-auto-install
```

**自动安装方式**：
```bash
# 脚本会自动检测并安装缺失依赖
node scripts/convert.js article.md
```

> **安全提示**：建议在隔离环境（Docker/沙盒）中首次运行，或使用 `--no-auto-install` 参数手动控制依赖安装。

### 2. 转换流程

**输入**：
- Markdown 文件路径（必需）
- 配置选项（可选）

**处理流程**：

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ 读取 MD 文件 │ -> │ 解析 Markdown │ -> │ 渲染特殊元素 │ -> │ 生成 HTML   │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
                         │                   │
                         v                   v
                ┌─────────────┐    ┌─────────────────────┐
                │ marked 解析  │    │ KaTeX 渲染公式      │
                │ 扩展语法处理 │    │ Puppeteer 渲染图表  │
                └─────────────┘    └─────────────────────┘
```

**输出**：
- 文件名：`{原文件名}-wechat.html`
- 特点：样式内联，可直接复制到微信公众号

### 3. 输出格式

生成的 HTML 特点：
- 所有样式内联（微信公众号要求）
- 支持 GFM（GitHub Flavored Markdown）
- 代码块带 Mac 风格装饰
- 图片带图注
- 外链自动添加引用标记
- 数学公式已渲染为 HTML
- 图表已渲染为 SVG

## Configuration

### 配置文件 `md-config.json`

```json
{
  "version": "1.0.0",
  "theme": {
    "name": "default"
  },
  "style": {
    "fontFamily": "-apple-system-font, BlinkMacSystemFont, Helvetica Neue, PingFang SC, sans-serif",
    "fontSize": "16px",
    "primaryColor": "#0F4C81",
    "textColor": "#3f3f3f",
    "bgColor": "#ffffff",
    "lineHeight": 1.75
  },
  "codeBlock": {
    "themeUrl": "https://cdn.jsdelivr.net/npm/highlight.js@11.9.0/styles/atom-one-dark.min.css",
    "themeName": "atom-one-dark",
    "isMacStyle": true,
    "showLineNumber": false
  },
  "image": {
    "legend": "alt-title",
    "borderRadius": "4px"
  },
  "link": {
    "citeStatus": false,
    "color": "#0F4C81"
  },
  "content": {
    "countStatus": true,
    "useIndent": false,
    "useJustify": false,
    "padding": "20px"
  },
  "headingStyles": {
    "h1": "default",
    "h2": "default",
    "h3": "default",
    "h4": "default",
    "h5": "default",
    "h6": "default"
  },
  "customCSS": ""
}
```

### 配置提取功能

从已排版好的 HTML 文件中提取样式配置，实现样式复用：

```bash
# 从渲染后的 HTML 提取配置
node scripts/extract-config.js example-result.html -o my-style.json

# 同时提供 Markdown 源文件，增强分析
node scripts/extract-config.js example-result.html -m example.md -o my-style.json

# 指定配置名称
node scripts/extract-config.js output.html --name "my-brand" -o my-brand-config.json
```

**可提取的样式参数**：

| 参数 | 说明 | 提取方式 |
|-----|------|---------|
| 主色调 | 链接、标题等元素的颜色 | 分析 HTML 中的颜色值 |
| 字体 | 文章正文字体 | 从 CSS 中提取 |
| 字号 | 正文字号 | 从 CSS 中提取 |
| 代码块主题 | highlight.js 主题 | 从 CSS URL 中识别 |
| Mac 风格代码块 | 是否有红黄绿按钮 | 检测 SVG 元素 |
| 背景色 | 文章背景色 | 从 body 样式中提取 |
| 文本颜色 | 正文颜色 | 从段落样式中提取 |
| 行高 | 文本行高 | 从 CSS 中提取 |
| 图片圆角 | 图片边框圆角 | 从 img 样式中提取 |

### 使用提取的配置

```bash
# 使用提取的配置文件进行转换
node scripts/convert.js article.md -c my-style.json -o article-output.html

# 命令行参数覆盖配置文件
node scripts/convert.js article.md -c my-style.json --color "#FF6600"
```

### 命令行参数

```bash
md-wechat <input> [options]

选项：
  -o, --output <path>     输出 HTML 文件路径
  -c, --config <path>     配置文件路径 (默认: md-config.json)
  --theme <name>          主题名称 (default/grace/simple)
  --color <color>         主题颜色 (覆盖配置文件)
  --font <font>           字体系列 (覆盖配置文件)
  --font-size <size>      字体大小 (覆盖配置文件)
  --bg-color <color>      背景颜色 (覆盖配置文件)
  --text-color <color>    文本颜色 (覆盖配置文件)
  --no-auto-install       禁用自动安装依赖
```

## Usage Examples

### 基础用法

```bash
# 转换单个文件
node scripts/convert.js article.md

# 指定输出路径
node scripts/convert.js article.md -o output.html

# 使用自定义主题色
node scripts/convert.js article.md --color "#009874"
```

### npm scripts

```bash
# 安装依赖
npm install

# 测试转换
npm run test
```

### 编程方式使用

```javascript
import { MDToWechatConverter } from './scripts/convert.js';

const converter = new MDToWechatConverter({
  primaryColor: '#0F4C81',
  macStyleCode: true
});

const html = await converter.convert(markdownText);
console.log(html);
```

## Dependencies

### 核心依赖

| 依赖 | 版本 | 用途 |
|-----|------|------|
| `marked` | ^12.0.0 | Markdown 解析 |
| `highlight.js` | ^11.9.0 | 代码语法高亮 |
| `katex` | ^0.16.9 | 数学公式渲染 |
| `juice` | ^10.0.0 | CSS 内联化 |
| `puppeteer` | ^22.0.0 | 图表渲染（无头浏览器） |
| `commander` | ^12.0.0 | 命令行参数解析 |
| `chalk` | ^5.3.0 | 终端彩色输出 |

### 自动安装机制

脚本会自动检测缺失的依赖并安装：
1. 检查 `node_modules` 目录
2. 缺失时自动执行 `npm install`
3. 安装完成后继续执行

### 可选依赖

对于 PlantUML 支持，需要安装 Java 运行时环境。

## 功能支持矩阵

| 功能 | Python 版本 | Node.js 版本 |
|-----|------------|--------------|
| 基础 Markdown | ✅ | ✅ |
| GFM 扩展 | ✅ | ✅ |
| 删除线/高亮/下划线 | ✅ | ✅ |
| Ruby 注音 | ✅ | ✅ |
| 代码高亮 | ✅ | ✅ |
| 数学公式 | ❌ 原始代码 | ✅ KaTeX 渲染 |
| Mermaid 图表 | ❌ 原始代码 | ✅ SVG 渲染 |
| PlantUML | ❌ 原始代码 | ⚠️ 部分 |
| Infographic | ❌ 原始代码 | ⚠️ 部分 |
| 样式内联 | ❌ | ✅ juice |

## Implementation Notes

### 架构设计

```
convert.js
├── 扩展语法处理器
│   ├── strikethrough  删除线
│   ├── highlight      高亮
│   ├── underline      下划线
│   ├── rubyBrace      Ruby 注音 {}
│   └── rubyCaret      Ruby 注音 ^()
│
├── 数学公式渲染
│   ├── mathExtension  块级公式
│   └── inlineMath     行内公式
│
├── 图表渲染
│   └── mermaidExtension  Mermaid → SVG
│
├── 代码块处理
│   └── codeBlockExtension  代码高亮 + Mac 装饰
│
└── 核心转换器
    └── MDToWechatConverter
        ├── setupMarked()     配置解析器
        ├── convert()         主转换流程
        ├── renderMermaid()   渲染 Mermaid
        └── wrapHTML()        包装输出
```

### 关键技术点

1. **marked 扩展系统**：使用 marked 的 extension API 实现自定义语法
2. **KaTeX 服务端渲染**：在 Node.js 中直接渲染数学公式为 HTML
3. **Puppeteer 无头浏览器**：渲染 Mermaid 等 JavaScript 依赖的图表
4. **CSS 内联化**：使用 juice 库将 CSS 样式内联到 HTML 元素

### 微信公众号适配

关键适配点：
1. **样式内联**：所有 CSS 必须内联到 style 属性
2. **选择器限制**：不支持 class 选择器，使用标签和内联样式
3. **外部链接**：微信会屏蔽外链，建议添加引用标记
4. **图片处理**：需上传到微信服务器或使用支持的图床
5. **代码块**：使用 pre + code 标签，添加 Mac 装饰
6. **KaTeX 样式**：通过 CDN 引入，复制时需保留

## Troubleshooting

### 常见问题

**Q: Puppeteer 安装失败？**
A: Puppeteer 需要下载 Chromium，可能需要配置镜像：
```bash
npm config set puppeteer_download_host=https://cdn.npmmirror.com/mirrors
npm install puppeteer
```

**Q: 数学公式显示异常？**
A: 确保 KaTeX CSS 正确加载，检查网络连接。

**Q: Mermaid 图表渲染失败？**
A: 检查 Puppeteer 是否正确安装，可能需要额外的系统依赖。

**Q: 复制到公众号后样式丢失？**
A: 
1. 使用浏览器打开 HTML 文件
2. 全选复制（Ctrl+A）
3. 粘贴到公众号编辑器

**Q: 图片不显示？**
A: 微信公众号不支持外链图片，需要：
1. 上传图片到微信后台
2. 使用微信支持的图床（如腾讯云）

## File Structure

```
md-wechat/
├── skill.md                    # 本文档
├── package.json                # Node.js 依赖配置
├── md-config.json              # 默认配置文件
├── scripts/
│   ├── convert.js              # 核心转换脚本 (Node.js)
│   ├── extract-config.js       # 配置提取脚本
│   └── convert.py              # Python 备用脚本
├── references/
│   ├── config-reference.md     # 配置参考
│   └── theme-reference.md      # 主题参考
└── assets/
    └── themes/
        ├── base.css            # 基础样式
        ├── default.css         # 经典主题
        ├── grace.css           # 优雅主题
        └── simple.css          # 简洁主题
```

## Version History

- **2.0.0** (2024-03) - 使用 Node.js 重写，完整支持数学公式和图表渲染
- **1.0.0** (2024-03) - Python 版本，支持基础 Markdown 和扩展语法

## Based on

- [doocs/md](https://github.com/doocs/md) - 原始项目灵感来源
- [marked](https://marked.js.org/) - Markdown 解析器
- [KaTeX](https://katex.org/) - 数学公式渲染
- [Mermaid](https://mermaid.js.org/) - 图表渲染
