---
name: md-to-share
version: 2.2.0
description: "将 Markdown 文件转换为原生长图的 skill，可被 OpenClaw、Claude Code 等 AI Agent 直接调用。A skill that converts Markdown to long images, callable by AI Agents like OpenClaw and Claude Code."
author: DTacheng
license: MIT
---

# MD to Share / MD 转长图

A skill that converts Markdown files to long images, directly callable by AI Agents like OpenClaw and Claude Code. Perfect for sharing on WeChat, Discord, and other platforms.

将 Markdown 文件转换为原生长图的 skill，可使用 OpenClaw、Claude Code 等 AI Agent 直接调用。方便分享到微信、Discord 等平台。

## Features / 特点

- **Environment Auto-Detection**: Automatically detects OpenClaw vs Claude Code and applies optimal settings
- **High Resolution**: Configurable width up to 1600px (2x scale factor) for crisp display
- **Auto Theme**: Light mode (6:00-18:00) / Dark mode (18:00-6:00) based on time
- **Discord Optimized**: JPEG format at 85% quality, auto-splits large files
- **Self-Contained**: Bundled Chromium via Playwright — no system browser needed
- **Smart Splitting**: Splits at semantic boundaries (headings, hr) not mid-paragraph
- **Robust Error Handling**: Clear exit codes for AI agents to understand failures

- **环境自动检测**：自动检测 OpenClaw 或 Claude Code 环境，应用最优设置
- **高分辨率**：可配置宽度最高 1600px（2x 缩放因子），在所有平台上清晰显示
- **自动主题**：根据时间自动切换浅色（6:00-18:00）/ 深色（18:00-6:00）模式
- **Discord 优化**：JPEG 格式 85% 质量，自动切分大文件
- **独立运行**：内置 Playwright Chromium，无需系统安装浏览器
- **智能切分**：在语义边界（标题、分隔线）处切分，不会在段落中间
- **健壮错误处理**：清晰的退出码，方便 AI Agent 理解错误

## Quick Start / 快速使用

Use this skill when user asks to "forward", "convert to image", "share", "generate long image".

当用户要求"转发"、"转成图片"、"方便分享"、"生成长图"时使用此 skill。

## ⚠️ Decision Flow for Agents / Agent 决策流程

**IMPORTANT: Before calling md2img, determine the target channel first.**

```
用户要求生成图片
  ├── 明确要发到 Discord → 使用 --channel=discord（自动切图，确保清晰）
  ├── 明确要发到 WeChat  → 使用 --channel=wechat（保留长图，微信原生支持）
  ├── 明确要发到 iMessage → 使用 --channel=imessage（保留长图）
  ├── 本地使用 / 保存文件  → 使用 --channel=local（保留长图）
  └── 不确定目标渠道      → ❗ 先反问用户确认渠道，再执行
```

**Why this matters**: Discord has strict image dimension limits (images taller than ~2000px get scaled down to unreadable sizes). WeChat and iMessage handle long images natively — splitting would break the reading experience.

**为什么这很重要**：Discord 对图片尺寸有严格限制（超过 ~2000px 高的图会被缩放到无法阅读）。微信和 iMessage 原生支持长图 — 切分反而会破坏阅读体验。

## Usage / 使用方法

### 1. Convert Command / 转换命令

```bash
md2img <input.md> [output] [options]
```

**Options / 选项:**

| Option | Description | Default |
|--------|-------------|---------|
| `--preset=<name>` | Configuration preset: `openclaw` \| `generic` | Auto-detect |
| `--channel=<name>` | Target channel: `discord` \| `wechat` \| `imessage` \| `local` | None |
| `--width=<px>` | CSS width in pixels | Preset value |
| `--scale=<factor>` | Device scale factor | 2 |
| `--max-size=<MB>` | Max file size before splitting | Preset value |
| `--max-height=<px>` | Max pixel height per image | Channel value |
| `--quality=<1-100>` | JPEG quality | 85 |
| `--theme=<light\|dark>` | Force theme | Auto by time |
| `--timeout=<ms>` | Browser operation timeout | 30000 |

**Channel behavior / 渠道行为:**

| Channel | Splitting | Reason |
|---------|-----------|--------|
| `discord` | ✅ Auto-split at 1800px height | Discord scales tall images, making them unreadable |
| `wechat` | ❌ Keep long image | WeChat handles long images natively |
| `imessage` | ❌ Keep long image | iMessage handles long images well |
| `local` | ❌ Keep long image | No platform constraints |
| Not specified | ❌ No splitting | Default safe behavior |

**Output formats / 输出格式:**
- `.jpg` / `.jpeg` - JPEG format (default, recommended)
- `.png` - PNG format (lossless, larger files)

Example / 示例：
```bash
# For Discord (auto-split for readability)
md2img report.md report.jpg --preset=openclaw --channel=discord

# For WeChat (keep as long image)
md2img report.md report.jpg --preset=openclaw --channel=wechat

# For local use (no splitting)
md2img report.md report.jpg

# Force dark theme
md2img report.md report.jpg --theme=dark
```

### 2. Configuration Presets / 配置预设

| Preset | CSS Width | Scale | Actual Width | Max Size | Use Case |
|--------|-----------|-------|--------------|----------|----------|
| `openclaw` | 600px | 2x | 1200px | 5MB | OpenClaw → Discord (optimized for compression) |
| `generic` | 800px | 2x | 1600px | 8MB | Claude Code / local use (high resolution) |

| 预设 | CSS 宽度 | 缩放 | 实际宽度 | 最大文件 | 使用场景 |
|------|----------|------|----------|----------|----------|
| `openclaw` | 600px | 2x | 1200px | 5MB | OpenClaw → Discord（适配压缩层） |
| `generic` | 800px | 2x | 1600px | 8MB | Claude Code / 本地使用（高分辨率） |

**Auto-Detection Logic / 自动检测逻辑:**
- If `OPENCLAW_CHANNEL` or `OPENCLAW_SKILLS_DIR` env var exists → `openclaw` preset
- If current directory contains `.openclaw/skills` → `openclaw` preset
- Otherwise → `generic` preset

### 3. Send to Discord / 发送到 Discord

Use the message tool's media parameter:
```json
{
  "action": "send",
  "target": "channel_id",
  "message": "Brief description",
  "media": "/full/path/to/image.jpg"
}
```

**Note**: If the converted image exceeds the size limit, it will be automatically split into multiple files:
- `output-1.jpg`, `output-2.jpg`, `output-3.jpg`, ...

**注意**：如果转换后的图片超过大小限制，会自动切分为多个文件。

### 4. Send to WeChat / 发送到微信

- Image is generated at the specified path
- Open file manager to get the image
- Or copy to clipboard and paste

## Image Quality Optimization / 图片清晰度优化

### OpenClaw + Discord Flow / OpenClaw + Discord 流程

OpenClaw has two layers of image compression:
1. **Agent layer**: `imageMaxDimensionPx=1200`, `maxBytes=5MB`
2. **Media loading layer**: `MAX_IMAGE_BYTES=6MB`, scales down from 2048px

OpenClaw 有两层图片压缩：
1. **Agent 层**：`imageMaxDimensionPx=1200`，`maxBytes=5MB`
2. **媒体加载层**：`MAX_IMAGE_BYTES=6MB`，从 2048px 逐步缩小

**Recommended / 推荐**: Use `--preset=openclaw` to output 1200px images under 5MB. This bypasses both compression layers.

**推荐**：使用 `--preset=openclaw` 输出 1200px 且小于 5MB 的图片，这样可以绕过两层压缩。

```
With openclaw preset / 使用 openclaw 预设:
Skill outputs 1200px (< 5MB)
    ↓
Agent layer: 1200px ≤ 1200px → No compression ✓
    ↓
Media layer: 5MB < 6MB → No compression ✓
    ↓
User receives: 1200px (guaranteed) / 用户收到：1200px（确定）
```

### Final Resolution Reference / 最终分辨率参考

| Environment | Preset | Final Width | Notes |
|-------------|--------|-------------|-------|
| OpenClaw + Discord | `openclaw` | **1200px** | Bypasses compression |
| Claude Code | `generic` | **1600px** | Full resolution |
| Custom | User-defined | Variable | Full control |

## Exit Codes / 退出码

When the skill fails, check the exit code to understand the error:

| Code | Name | Description |
|------|------|-------------|
| 0 | SUCCESS | Conversion completed successfully |
| 1 | INVALID_ARGS | Missing or invalid command line arguments |
| 2 | FILE_NOT_FOUND | Input markdown file does not exist |
| 3 | FILE_READ_ERROR | Cannot read the input file (permissions, encoding) |
| 4 | BROWSER_NOT_FOUND | Playwright Chromium not installed (run: npx playwright install chromium) |
| 5 | BROWSER_LAUNCH_ERROR | Failed to launch browser |
| 6 | RENDER_ERROR | Failed to render the HTML content |
| 7 | SCREENSHOT_ERROR | Failed to capture screenshot |
| 8 | OUTPUT_WRITE_ERROR | Cannot write to output location |

当 skill 失败时，检查退出码以理解错误：

| 代码 | 名称 | 描述 |
|------|------|-------------|
| 0 | 成功 | 转换成功完成 |
| 1 | 参数无效 | 缺少或无效的命令行参数 |
| 2 | 文件未找到 | 输入的 markdown 文件不存在 |
| 3 | 文件读取错误 | 无法读取输入文件（权限、编码） |
| 4 | 浏览器未安装 | Playwright Chromium 未安装（运行: npx playwright install chromium） |
| 5 | 浏览器启动错误 | 无法启动浏览器 |
| 6 | 渲染错误 | 无法渲染 HTML 内容 |
| 7 | 截图错误 | 无法捕获截图 |
| 8 | 输出写入错误 | 无法写入输出位置 |

## Configuration / 配置

### Environment Variables / 环境变量

| Variable | Description | Example |
|----------|-------------|---------|
| `CHROME_PATH` | Override Playwright's bundled Chromium | `/usr/bin/chromium` |
| `MD2IMG_TIMEOUT` | Override default 30s timeout (ms) | `60000` |
| `OPENCLAW_CHANNEL` | OpenClaw channel (auto-detection) | - |
| `OPENCLAW_SKILLS_DIR` | OpenClaw skills directory (auto-detection) | - |

### Default Settings by Preset / 各预设默认设置

**OpenClaw preset:**
- **Width**: 600px CSS (1200px actual with 2x scale)
- **Max file size**: 5MB (auto-splits if larger)

**Generic preset:**
- **Width**: 800px CSS (1600px actual with 2x scale)
- **Max file size**: 8MB (auto-splits if larger)

**Common:**
- **Format**: JPEG at 85% quality
- **Timeout**: 30 seconds
- **Theme**: Light mode 6:00-18:00, Dark mode 18:00-6:00

## Dependencies / 依赖

- Node.js 18+
- playwright (bundles its own Chromium — no system browser required)
- marked (markdown parser)

Install: `npm install` or `bun install` (postinstall automatically downloads Chromium)

## Styling / 样式说明

Generated image styles:
- H1: Large font with red bottom border
- H2: Blue left border accent
- H3: Gray color, smaller than H2
- Tables: Zebra stripes with hover highlight
- Code blocks: Dark background
- Inline code: Light gray background with red text
- Blockquotes: Blue border + light gray background
- Horizontal rules: Elegant dividers

## Example / 示例

When user says "share this to WeChat" or "make it easy to forward":
1. Read the MD file content
2. Run `md2img` to convert to long image
3. Tell user the image path, or send directly to the specified platform

## Troubleshooting / 故障排除

### Browser not found / 浏览器未安装

Playwright's bundled Chromium should be installed automatically during `npm install`. If not:
```bash
npx playwright install chromium
```

### Image too large / 图片太大

The tool automatically splits images at semantic boundaries (headings, horizontal rules). If you still have issues:
- Use JPEG format (default) instead of PNG
- Use `--max-size` to set a smaller split threshold
- Consider splitting your markdown into smaller files

### Image quality too low in OpenClaw / OpenClaw 图片清晰度低

Make sure you're using the `openclaw` preset (should auto-detect):
```bash
md2img input.md --preset=openclaw
```

This ensures 1200px output that bypasses OpenClaw's compression layers.
