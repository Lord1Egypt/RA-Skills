
---
name: lh-wechat-to-markdown
description: |
  抓取微信公众号文章并转换为 Markdown，同时保存 HTML 快照。
  需要在用户可访问页面的基础上操作，强调登录态、浏览器辅助和人工确认等现实边界。
  触发关键词："抓取微信文章"、"保存公众号文章"、"微信转 markdown"、"wechat article"。
version: 1.2.1
metadata:
  openclaw:
    homepage: https://github.com/liuhedev/lh-openclaw-kit
    requires:
      anyBins:
        - python3
---

# 微信公众号文章转 Markdown

在用户可访问微信文章页面的基础上，抓取公众号文章内容并转换为干净的 Markdown，同时保存 HTML 快照。

## 产品定位与边界说明

### 能力声明（重要！）

- ✅ **支持**：在用户已登录微信、可正常访问文章的前提下，抓取已加载的页面内容
- ✅ **支持**：保存 HTML 快照和转换后的 Markdown
- ✅ **支持**：提取文章标题、作者、发布时间、正文内容
- ❌ **不声称**："绕过微信拦截"、"破解反爬"、"无需登录"
- ❌ **不承诺**：对所有微信文章都能 100% 完美抓取
- ⚠️ **现实边界**：微信可能随时调整页面结构，本工具仅尽力而为

### 推荐使用场景

1. 个人收藏与归档：将自己喜欢的公众号文章保存到本地知识库
2. 内容二次加工：在获得授权的前提下，对文章进行 Markdown 格式转换
3. 离线阅读：将文章保存为本地文件便于离线查看

## 脚本目录

所有脚本位于本 skill 的 `scripts/` 子目录中。

**执行说明**：
1. 确定本 SKILL.md 文件的目录路径为 `{baseDir}`
2. 脚本路径 = `{baseDir}/scripts/<script-name>.py`
3. 使用 Python 3 运行脚本

## 功能特性

- Chrome CDP 浏览器自动化，支持 JavaScript 完整渲染
- 两种抓取模式：自动抓取 vs 等待用户确认后抓取
- 保存渲染后的 HTML 快照（`*-captured.html`）
- 干净的 Markdown 输出，包含元数据（标题、作者、发布时间等）
- 智能提取公众号文章特有结构（点赞、在看、评论等区域自动过滤）
- **微信图片专项处理**：优先使用微信正文图片中的 `data-src`，并兼容 `data-original`、`data-actualsrc`、`data-croporisrc`、`data-cover`
- **图片本地化下载**（`--download-images`）：下载到 `images/` 目录，Markdown 中自动替换为相对路径；下载时复用浏览器会话的 `Referer/Cookie`，单张失败不影响整体

## 使用方法

### 基础用法

```bash
# 自动模式 - 无头浏览器，页面加载完成后自动抓取（默认）
python3 {baseDir}/scripts/main.py <wechat-article-url>

# 使用可视浏览器（带 UI）
python3 {baseDir}/scripts/main.py <wechat-article-url> --headed

# 等待模式 - 可视浏览器，等待用户确认页面准备好后再抓取（推荐用于需要登录的情况）
python3 {baseDir}/scripts/main.py <wechat-article-url> --headed --wait

# 保存到指定文件
python3 {baseDir}/scripts/main.py <wechat-article-url> -o output.md

# 保存到自定义输出目录（自动生成文件名）
python3 {baseDir}/scripts/main.py <wechat-article-url> --output-dir ./wechat-articles/

# 下载图片到本地
python3 {baseDir}/scripts/main.py <wechat-article-url> --download-images
```

### 选项说明

| 选项 | 描述 |
|------|------|
| `<url>` | 微信公众号文章链接 |
| `-o &lt;path&gt;` | 输出文件路径（必须是文件路径，不是目录） |
| `--output-dir &lt;dir&gt;` | 基础输出目录，自动生成 `{dir}/{date}/{slug}.md` |
| `--headed` | 使用可视浏览器（默认无头模式） |
| `--wait` | 等待用户信号后再抓取（仅在 --headed 模式有效，适用于需要登录或复杂页面） |
| `--timeout &lt;ms&gt;` | 页面加载超时时间（默认：30000） |
| `--download-images` | 下载图片到本地 `images/` 目录并重写为相对路径；复用浏览器会话 `Referer/Cookie`，单张失败仅警告，保留原 URL |

## 抓取模式

| 模式 | 行为 | 适用场景 |
|------|------|----------|
| 自动（默认） | 网络空闲时抓取 | 公开可访问的文章、静态内容 |
| 等待（`--wait`） | 用户确认后抓取 | 需要登录、懒加载、可能有访问限制的页面 |

**等待模式工作流**：
1. 使用 `--wait` 运行脚本 → 脚本输出"请在浏览器中确认页面加载完成，然后按 Enter 继续"
2. 提示用户在浏览器中完成必要操作（登录、滚动等）
3. 用户确认页面准备好后，按 Enter 触发抓取

## 输出格式

每次运行会保存两个文件：

- **Markdown 文件**：包含 YAML front matter（`url`、`title`、`author`、`published_at`、`captured_at`），以及转换后的 Markdown 内容
- **HTML 快照**：`*-captured.html`，包含从 Chrome 捕获的渲染后页面 HTML

HTML 快照在任何 Markdown 处理之前保存，因此它始终是用于转换的页面 DOM 的忠实捕获。

## 输出目录结构

默认：`wechat-articles/YYYY-MM-DD/{slug}.md`
使用 `--output-dir ./posts/`：`./posts/YYYY-MM-DD/{slug}.md`

HTML 快照使用相同的 basename：

- `wechat-articles/YYYY-MM-DD/{slug}-captured.html`
- `./posts/YYYY-MM-DD/{slug}-captured.html`

- `{slug}`：从文章标题生成（kebab-case，2-6 个词）
- 冲突处理：追加时间戳 `{slug}-YYYYMMDD-HHMMSS.md`

当启用 `--download-images` 时：
- 图片保存到 Markdown 文件同级的 `images/` 目录
- Markdown 中的图片链接重写为本地相对路径
- 下载时复用当前浏览器会话里的 `Referer` 和 Cookie
- 兼容 markdownify 生成的 `![图片](url "null")` 图片语法

## 环境变量

| 变量 | 描述 |
|------|------|
| `WECHAT_CHROME_PATH` | 自定义 Chrome 可执行文件路径 |
| `WECHAT_DATA_DIR` | 自定义数据目录 |
| `WECHAT_CHROME_PROFILE_DIR` | 自定义 Chrome 用户配置目录（推荐用于保存登录态） |

## 故障排查

| 问题 | 建议解决方案 |
|------|--------------|
| Chrome 未找到 | 设置 `WECHAT_CHROME_PATH` 环境变量 |
| 页面超时 | 增加 `--timeout` 值 |
| 需要登录 | 使用 `--wait` 模式，配合 `WECHAT_CHROME_PROFILE_DIR` 使用已登录的 Chrome 配置 |
| 抓取不完整 | 检查保存的 `-captured.html`，尝试 `--wait` 模式让用户手动滚动页面 |
| Markdown 质量差 | 检查 HTML 快照，微信可能已更新页面结构，欢迎提交 Issue |

## 测试建议

### 基础测试
```bash
# 测试一篇公开的微信文章
python3 {baseDir}/scripts/main.py https://mp.weixin.qq.com/s/xxx -o test-output.md

# 测试等待模式
python3 {baseDir}/scripts/main.py https://mp.weixin.qq.com/s/xxx --wait
```

### 建议测试 Prompt
1. "帮我抓取这篇微信公众号文章：<链接>"
2. "保存这篇公众号文章到本地，带图片"
3. "把这篇微信文章转成 Markdown，我需要先登录一下"

## 法律与道德提示

- 请仅抓取您有权访问和使用的内容
- 尊重原创作者的版权
- 不要用于批量抓取或商业用途
- 遵守微信的服务条款
