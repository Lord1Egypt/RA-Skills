# lh-wechat-to-markdown

抓取微信公众号文章并转换为 Markdown，同时保存 HTML 快照。

## 快速开始

```bash
# 安装依赖
pip install playwright beautifulsoup4 python-frontmatter markdownify requests

# 安装 Playwright 浏览器
playwright install chromium

# 抓取微信文章（默认无头模式）
python3 scripts/main.py https://mp.weixin.qq.com/s/xxx
```

## 主要功能

- ✅ Chrome CDP 浏览器自动化，完整 JavaScript 渲染
- ✅ 两种抓取模式：自动抓取 vs 等待用户确认
- ✅ 保存 HTML 快照和转换后的 Markdown
- ✅ 智能提取公众号文章结构
- ✅ **微信图片定向修复**：优先使用样本中稳定出现的 `data-src`，并兼容 `data-original`、`data-actualsrc`、`data-croporisrc`、`data-cover`
- ✅ **图片本地化下载**（`--download-images`）：下载到 `images/` 目录，并复用浏览器会话的 `Referer/Cookie`，单张失败不影响整体

## 使用示例

```bash
# 自动模式（默认无头）
python3 scripts/main.py <wechat-url>

# 使用可视浏览器
python3 scripts/main.py <wechat-url> --headed

# 等待模式（推荐用于需要登录的情况，需要 --headed）
python3 scripts/main.py <wechat-url> --headed --wait

# 保存到指定文件
python3 scripts/main.py <wechat-url> -o my-article.md

# 下载图片到本地
python3 scripts/main.py <wechat-url> --download-images
```

## 图片处理说明

微信公众号文章在浏览器端常把 `<img src>` 渲染成 1×1 SVG 占位图。此次定向修复所依据的真实样本里，正文图片稳定出现在 `data-src`，并伴随 `data-type`、`data-w`、`data-ratio`、`data-imgfileid`；个别裁剪图还带 `data-croporisrc`。

本工具在 HTML → Markdown 转换之前，会自动扫描所有 `<img>` 标签，按以下优先级提取真实图片地址：

1. `data-src`（最常见）
2. `data-original`（部分历史模板）
3. `data-actualsrc`（极少数旧版编辑器）
4. `data-croporisrc`（样本中个别裁剪图存在）
5. `data-cover`（封面/头图场景兜底）
6. `src`（兜底，仅当不是 SVG 占位图时采用）

使用 `--download-images` 时：
- 图片保存到 Markdown 同级的 `images/` 目录
- Markdown 中图片链接自动替换为相对路径（如 `images/img_00_xxxx.jpg`）
- 下载时复用当前浏览器会话里的 `Referer` 和 Cookie，提高微信图片落盘成功率
- 自动兼容 markdownify 生成的 `![图片](url "null")` 形式，避免把标题字段误当成 URL
- 单张下载失败仅打印警告，保留原始 URL，不会导致整个流程中断

## 重要提示

⚠️ **本工具不声称"绕过微信拦截"或"破解反爬"**

- 需要在用户可访问页面的基础上操作
- 推荐使用已登录的 Chrome 配置文件
- 尊重原创版权，遵守微信服务条款

详细文档请见 [SKILL.md](./SKILL.md)
