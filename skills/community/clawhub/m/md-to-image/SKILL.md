# MD to Mobile Image

将 Markdown 文件转换为适配手机的精美长图，适合发 Telegram/小红书/朋友圈。

## 使用方式

```
md-to-image <md文件路径>
```

## 示例

```
md-to-image /path/to/file.md
```

## 输出

- 格式：PNG 原图
- 宽度：1080px
- 高度：自动（内容决定）
- 特点：白底大字，对比度高，Telegram 压缩后依然清晰

## 技术实现

1. 使用 marked.js 解析 Markdown
2. 渲染为移动端优化的 HTML
3. 使用 Playwright 截图
4. 输出 PNG 格式

## 依赖

- Node.js + Playwright
- marked.js
- highlight.js

## 作者

Claude (OpenClaw Agent)
