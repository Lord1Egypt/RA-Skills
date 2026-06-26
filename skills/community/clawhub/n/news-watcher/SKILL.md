# News Watcher - 实时加密新闻监听 Skill

使用 Playwright 实时监听虚拟货币新闻网站，检测新文章发布并自动抓取全文、AI 总结、推送 Telegram。

**完全开源透明** · 源码 + 运行截图：https://github.com/vvxer/openclaw-news-watcher

## 功能

- 🎯 实时监听 CoinDesk、PANews 等新闻网站
- 🔍 通过 URL 哈希变化检测新文章（不依赖 RSS / API）
- 📰 自动抓取新文章全文
- 🤖 调用 OpenClaw AI Agent 生成中文摘要
- 📢 推送摘要到 Telegram
- ⏱️ 可配置检查间隔（默认 60 秒）

## 环境变量（必须设置）

| 变量 | 必填 | 说明 |
|------|------|------|
| `OPENCLAW_MJS` | ✅ 必填 | openclaw.mjs 的完整路径，用于调用 AI Agent 和发送消息 |
| `TELEGRAM_USER_ID` | ✅ 必填 | Telegram 收件人 Chat ID |
| `CHROME_PATH` | 可选 | 本地 Chrome 路径；未设置时按平台自动检测 |
| `PLAYWRIGHT_HEADLESS` | 可选 | 设为 `false` 显示浏览器窗口（调试用），默认 `true` |

```bash
# Windows PowerShell
$env:OPENCLAW_MJS = "D:\openclaw\node_modules\openclaw\openclaw.mjs"
$env:TELEGRAM_USER_ID = "你的ChatID"

# Linux / macOS
export OPENCLAW_MJS="/path/to/openclaw.mjs"
export TELEGRAM_USER_ID="你的ChatID"
```

## 基础用法

### 监听 CoinDesk（默认）

```bash
node {baseDir}/scripts/watch-news.js
```

### 监听其他网站

```bash
node {baseDir}/scripts/watch-news.js --site panews
node {baseDir}/scripts/watch-news.js --site coindesk --interval 120
```

## 参数

- `--site <name>` - 网站名称（支持: `coindesk`, `panews`）
- `--interval <seconds>` - 检查间隔（秒），默认 60

## 工作原理

1. **打开浏览器** - 使用 Playwright 加载新闻网站主页
2. **提取最新文章** - 获取置顶文章链接
3. **计算哈希** - 对文章 URL 做 MD5 哈希
4. **对比检测** - 与上次保存的哈希对比
5. **发现新文章** - URL 变化说明有新文章置顶
6. **抓取全文** - 打开文章页面抓取正文
7. **AI 总结** - 调用 `openclaw agent` 生成中文摘要
8. **推送通知** - 调用 `openclaw message send` 发送到 Telegram

## 缓存位置

新闻哈希缓存存储在：`~/.openclaw/cache/news-hash.json`

## 与 OpenClaw Cron 集成

### 方案 1：高频后台监听（推荐）

```bash
node ~/.openclaw/workspace/skills/news-watcher/scripts/watch-news.js --site coindesk --interval 60
```

### 方案 2：通过 OpenClaw Agent 调用

```bash
openclaw agent --message "监听 CoinDesk 新闻，有更新就通知我" --timeout 600
```

### 方案 3：每日新闻摘要 Cron

```bash
openclaw cron add \
  --name "Morning News Digest" \
  --cron "0 7 * * *" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --message "总结过去一晚上的加密新闻，列出前 3 个重点" \
  --announce \
  --channel telegram \
  --to "$TELEGRAM_USER_ID"
```

## 已支持的网站

| 网站 | site 参数 | 说明 |
|------|---------|------|
| CoinDesk | `coindesk` | 全球权威加密新闻 |
| PANews | `panews` | 中文区块链新闻 |

## 添加新网站

编辑 `watch-news.js`，在 `sites` 对象中添加：

```javascript
const sites = {
  coindesk: { /* ... */ },
  mynews: {
    url: 'https://example.com/news',
    selector: '.article-item',
    getContent: () => { /* 可选自定义提取逻辑 */ }
  }
};
```

## 故障排除

### 启动报错：OPENCLAW_MJS 未设置

```bash
export OPENCLAW_MJS="/path/to/openclaw.mjs"
```

### 启动报错：TELEGRAM_USER_ID 未设置

```bash
export TELEGRAM_USER_ID="你的Telegram Chat ID"
```

### 页面加载超时

```bash
node {baseDir}/scripts/watch-news.js --interval 180
```

### 显示浏览器窗口（调试）

```bash
PLAYWRIGHT_HEADLESS=false node {baseDir}/scripts/watch-news.js
```

### Chrome 路径未找到

```bash
export CHROME_PATH="/usr/bin/google-chrome"   # Linux
export CHROME_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"  # macOS
```

## 开源透明

- 完整源码：https://github.com/vvxer/openclaw-news-watcher
- 运行截图示例见 GitHub，可验证实际运行效果
- 所有操作通过本地 OpenClaw 完成，不依赖任何第三方 API
- 代码逻辑完全可审查，无隐藏行为
