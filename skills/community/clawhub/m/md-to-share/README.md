# MD to Share

[中文](#中文) | [English](#english)

---

## 中文

将 Markdown 文件转换为原生长图的 skill，可使用 OpenClaw、Claude Code 等 AI Agent 直接调用。方便分享到微信、Discord 等平台。

### 安装

```bash
git clone https://github.com/DTacheng/md-to-share.git
cd md-to-share
npm install
```

### 使用方法

```bash
# 基本用法（默认输出 JPEG 格式）
node md2img.mjs <输入文件.md> [输出文件]

# 示例
node md2img.mjs "~/Downloads/文档.md"
node md2img.mjs "~/Downloads/文档.md" "~/Downloads/输出.jpg"
node md2img.mjs "~/Downloads/文档.md" "~/Downloads/输出.png"
```

也可以添加全局命令：
```bash
npm link
md2img <输入文件.md> [输出文件]
```

### 特点

- **高分辨率输出**：1600px 宽度（2x 缩放因子），在所有平台上清晰显示
- **自动主题切换**：根据时间自动切换浅色（6:00-18:00）/ 深���（18:00-6:00）模式
- **Discord 优化**：JPEG 格式 85% 质量，自动切分 >8MB 的文件
- **跨平台支持**：自动检测 macOS、Linux、Windows 上的 Chrome
- **智能切分**：在语义边界（标题、分隔线）处切分，不在段落中间
- **健壮错误处理**：清晰的退出码，方便 AI Agent 理解错误
- **原生长图**：真正的文档流排版，不是 PPT 分页拼接
- **美观排版**：使用系统字体，支持表���、代码块、引用、列表等

### 输出格式

- `.jpg` / `.jpeg` - JPEG 格式（默认，文件更小，推荐用于 Discord）
- `.png` - PNG 格式（无损，文件更大）

### 退出码

| 代码 | 描述 |
|------|------|
| 0 | 成功 |
| 1 | 参数无效 |
| 2 | 文件未找到 |
| 3 | 文件读取错误 |
| 4 | Chrome 未找到 |
| 5 | 浏览器启动错误 |
| 6 | 渲染错误 |
| 7 | 截图错误 |
| 8 | 输出写入错误 |

### 环境变量

| 变量 | 描述 |
|------|------|
| `CHROME_PATH` | 覆盖 Chrome 可执行文件路径 |

### 样式说明

生成的长图样式：
- 标题：大字号，红色底部边框
- 二级标题：蓝色左侧边框
- 表格：斑马纹，悬停高亮
- 代码块：深色背景
- 行内代码：浅灰背景，红色文字
- 引用：蓝色边框 + 浅灰背景
- 分隔线：优雅分割

### 依赖

- Node.js 18+
- puppeteer-core
- marked
- Google Chrome 或 Chromium（使用系统已安装的浏览器）

---

## English

A skill that converts Markdown files to long images, directly callable by AI Agents like OpenClaw and Claude Code. Perfect for sharing on WeChat, Discord, and other platforms.

### Installation

```bash
git clone https://github.com/DTacheng/md-to-share.git
cd md-to-share
npm install
```

### Usage

```bash
# Basic usage (defaults to JPEG format)
node md2img.mjs <input.md> [output]

# Examples
node md2img.mjs "~/Downloads/document.md"
node md2img.mjs "~/Downloads/document.md" "~/Downloads/output.jpg"
node md2img.mjs "~/Downloads/document.md" "~/Downloads/output.png"
```

You can also add it as a global command:
```bash
npm link
md2img <input.md> [output]
```

### Features

- **High Resolution Output**: 1600px width (2x scale factor) for crisp display on all platforms
- **Auto Theme Switching**: Light mode (6:00-18:00) / Dark mode (18:00-6:00) based on time
- **Discord Optimized**: JPEG format at 85% quality, auto-splits files >8MB
- **Cross-Platform Support**: Auto-detects Chrome on macOS, Linux, and Windows
- **Smart Splitting**: Splits at semantic boundaries (headings, hr) not mid-paragraph
- **Robust Error Handling**: Clear exit codes for AI agents to understand failures
- **Native Long Image**: True document flow layout, not PPT page stitching
- **Beautiful Typography**: System fonts with support for tables, code blocks, blockquotes, lists

### Output Formats

- `.jpg` / `.jpeg` - JPEG format (default, smaller files, recommended for Discord)
- `.png` - PNG format (lossless, larger files)

### Exit Codes

| Code | Description |
|------|-------------|
| 0 | Success |
| 1 | Invalid arguments |
| 2 | File not found |
| 3 | File read error |
| 4 | Chrome not found |
| 5 | Browser launch error |
| 6 | Render error |
| 7 | Screenshot error |
| 8 | Output write error |

### Environment Variables

| Variable | Description |
|----------|-------------|
| `CHROME_PATH` | Override Chrome executable path |

### Styling

Generated image styles:
- H1: Large font with red bottom border
- H2: Blue left border accent
- H3: Gray color, smaller than H2
- Tables: Zebra stripes with hover highlight
- Code blocks: Dark background
- Inline code: Light gray background with red text
- Blockquotes: Blue border + light gray background
- Horizontal rules: Elegant dividers

### Dependencies

- Node.js 18+
- puppeteer-core
- marked
- Google Chrome or Chromium (uses system-installed browser)

---

## License

MIT
