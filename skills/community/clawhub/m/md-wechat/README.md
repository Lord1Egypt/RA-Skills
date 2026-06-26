# md-wechat

将 Markdown 文档转换为微信公众号格式的排版工具。支持自定义主题、字体、颜色、代码高亮等配置，生成的 HTML 可直接复制粘贴到微信公众号编辑器使用。

## 功能特性

- 完整支持 Markdown 基础语法和 GFM 扩展
- 支持数学公式渲染（KaTeX）
- 支持 Mermaid 流程图渲染
- Mac 风格代码块（红黄绿装饰按钮）
- 代码语法高亮（highlight.js）
- 扩展语法支持：删除线、高亮、下划线、Ruby 注音
- 从排版文件提取配置，实现样式复用
- 自动检测并安装缺失依赖

## 快速开始

### 环境要求

- Node.js >= 18.0.0

### 安装

```bash
git clone https://github.com/italks/md-wechat.git
cd md-wechat
npm install
```

> **安全建议**：首次使用建议检查 `package.json` 中的依赖，或在隔离环境中运行。

### 基础用法

```bash
# 转换 Markdown 文件
node scripts/convert.js your-article.md
```

转换完成后，会在同目录生成 `your-article-wechat.html` 文件。

## 主要流程

### 1. Markdown 直接生成排版

**首次使用时**，如果没有配置文件，会自动生成默认配置文件 `md-config.json`：

```bash
node scripts/convert.js article.md
```

输出：
- `article-wechat.html` - 排版后的 HTML 文件
- `md-config.json` - 默认配置文件（如果不存在）

### 2. 提取自定义配置

从已排版好的 HTML 文件中提取样式配置：

```bash
node scripts/extract-config.js article-wechat.html -o my-style.json
```

可提取的样式参数：

| 参数 | 说明 |
|-----|------|
| 主色调 | 链接、标题等元素的颜色 |
| 字体 | 文章正文字体 |
| 字号 | 正文字号 |
| 代码块主题 | highlight.js 主题名称 |
| Mac 风格代码块 | 是否启用红黄绿按钮装饰 |
| 背景色/文本颜色 | 文章背景和文字颜色 |
| 行高 | 文本行高 |

### 3. 使用自定义配置排版

使用提取的配置文件进行排版：

```bash
# 使用配置文件
node scripts/convert.js new-article.md -c my-style.json

# 命令行参数覆盖配置
node scripts/convert.js new-article.md -c my-style.json --color "#009874"
```

## 配置文件说明

配置文件 `md-config.json` 结构：

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
    "themeName": "atom-one-dark",
    "isMacStyle": true
  },
  "content": {
    "countStatus": true,
    "useIndent": false,
    "useJustify": false,
    "padding": "20px"
  }
}
```

## 命令行参数

### convert.js - Markdown 转换

```bash
node scripts/convert.js <input> [options]

参数：
  input                  输入 Markdown 文件路径

选项：
  -o, --output <path>    输出 HTML 文件路径
  -c, --config <path>    配置文件路径 (默认: md-config.json)
  --color <color>        主题颜色 (覆盖配置文件)
  --font <font>          字体系列 (覆盖配置文件)
  --font-size <size>     字体大小 (覆盖配置文件)
  --bg-color <color>     背景颜色 (覆盖配置文件)
  --text-color <color>   文本颜色 (覆盖配置文件)
  --no-auto-install      禁用自动安装依赖
```

### extract-config.js - 配置提取

```bash
node scripts/extract-config.js <input> [options]

参数：
  input                  渲染后的 HTML 文件路径

选项：
  -o, --output <path>    输出配置文件路径
  -m, --markdown <path>  对应的 Markdown 文件 (增强分析)
  --name <name>          配置名称 (默认: extracted)
```

## 功能支持

| 功能 | 支持 |
|-----|:----:|
| 基础 Markdown | ✅ |
| GFM 扩展（表格、任务列表等） | ✅ |
| 代码语法高亮 | ✅ |
| Mac 风格代码块 | ✅ |
| 数学公式 (KaTeX) | ✅ |
| Mermaid 流程图 | ✅ |
| 删除线/高亮/下划线 | ✅ |
| Ruby 注音 | ✅ |
| 样式内联 | ✅ |
| 配置提取与复用 | ✅ |

## 与 doocs/md 功能对比

本项目受 [doocs/md](https://github.com/doocs/md) 启发开发，以下是功能对比：

| 功能 | doocs/md | md-wechat |
|-----|:--------:|:---------:|
| **运行环境** | 浏览器/在线 | Node.js 命令行 |
| **使用方式** | 在线编辑器 | CLI 批量处理 |
| 基础 Markdown | ✅ | ✅ |
| GFM 扩展 | ✅ | ✅ |
| 代码语法高亮 | ✅ | ✅ |
| Mac 风格代码块 | ✅ | ✅ |
| 数学公式 (LaTeX) | ✅ | ✅ KaTeX |
| Mermaid 图表 | ✅ | ✅ |
| PlantUML 图表 | ✅ | ⚠️ 部分 |
| Infographic 信息图 | ✅ | ⚠️ 部分 |
| 删除线/高亮/下划线 | ✅ | ✅ |
| Ruby 注音 | ✅ | ✅ |
| **配置提取** | ❌ | ✅ |
| **配置复用** | ❌ | ✅ |
| **批量处理** | ❌ | ✅ |
| **CLI 自动化** | ❌ | ✅ |
| **依赖自动安装** | ❌ | ✅ |

### 适用场景

**doocs/md 更适合：**
- 在线实时编辑预览
- 单篇文章快速排版
- 可视化操作

**md-wechat 更适合：**
- 批量文章处理
- 自动化工作流
- CI/CD 集成
- 样式配置复用
- 团队协作排版

## 项目结构

```
md-wechat/
├── README.md                    # 项目说明
├── README_EN.md                 # 英文说明
├── skill.md                     # 技能详细文档
├── package.json                 # Node.js 依赖配置
├── md-config.json               # 默认配置文件
├── scripts/
│   ├── convert.js               # 核心转换脚本
│   └── extract-config.js        # 配置提取脚本
└── example.md                   # 示例 Markdown 文件
```

## 使用到微信公众号

1. 使用本工具转换 Markdown 文件生成 HTML
2. 用浏览器打开生成的 HTML 文件
3. 全选复制（Ctrl+A / Cmd+A）
4. 粘贴到微信公众号编辑器

## 致谢

本项目灵感来源于 [doocs/md](https://github.com/doocs/md)，感谢该项目提供的优秀思路和实现参考。

同时也感谢以下开源项目：

- [marked](https://marked.js.org/) - Markdown 解析器
- [KaTeX](https://katex.org/) - 数学公式渲染
- [highlight.js](https://highlightjs.org/) - 代码语法高亮
- [Mermaid](https://mermaid.js.org/) - 图表渲染

## License

MIT License
