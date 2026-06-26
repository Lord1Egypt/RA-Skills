<div align="center">

<h1>pixelmsg</h1>

<p><strong>把 AI 回复变成精美图片卡片。</strong></p>

<p>
  <img src="https://img.shields.io/badge/node-%3E%3D18-brightgreen?style=flat-square" alt="Node.js" />
  <img src="https://img.shields.io/badge/playwright-1.58-blue?style=flat-square" alt="Playwright" />
  <img src="https://img.shields.io/badge/license-MIT-lightgrey?style=flat-square" alt="License" />
</p>

</div>

[English](README.md) | 中文

---

AI agent 被困在纯文本里。`pixelmsg` 打破这一限制 —— 给 agent 一个 HTML 模板，用 Playwright 渲染，把像素级精准的 PNG 图片发送给用户。天气卡片、日报、GitHub 统计、仪表盘。凡是能用 HTML 设计的，都能作为精美图片消息发出去。

## 为什么用 pixelmsg

| 不用 pixelmsg | 用 pixelmsg |
|---|---|
| "今日天气：18°C，多云，东南风 3 级..." | 带温度、预报和统计数据的精美天气卡片 |
| "热门仓库：1. openclaw/openclaw（今日 9k stars）..." | 排版精良的 GitHub 热榜，含 star 数和语言标签 |
| "你的任务：[x] Q1 报告，[ ] 产品评审..." | 带进度和优先级的可视化待办看板 |

纯文本能用。图片更能留下印象。

## 效果预览

<table>
<tr>
<td align="center"><img src="screenshots/zh/weather-default-mobile.png" width="200" /><br /><sub>天气卡片</sub></td>
<td align="center"><img src="screenshots/zh/github-trending-default-mobile.png" width="200" /><br /><sub>GitHub 热榜</sub></td>
<td align="center"><img src="screenshots/zh/todolist-default-mobile.png" width="200" /><br /><sub>待办清单</sub></td>
</tr>
</table>

<table>
<tr>
<td align="center"><img src="screenshots/zh/github-stats-default-desktop.png" width="640" /><br /><sub>GitHub 统计 — 桌面端</sub></td>
</tr>
</table>

## 特性

- **零构建** — 模板是纯 HTML，通过 CDN 引入 Alpine.js + Tailwind CSS
- **Playwright 渲染** — 无头 Chromium，默认 2x 视网膜屏质量
- **精准裁切** — 只截取 `#app` 元素，不截整页
- **多种视口** — 移动端（375px）、平板（768px）、桌面端（1440px），或自定义
- **Agent 就绪** — `render.sh` 输出绝对路径；兼容平台自动将其作为图片消息发送
- **5 个生产级模板** — 天气、GitHub 热榜、GitHub 统计、待办清单等
- **可组合** — 通过 URL 参数注入动态数据，无需修改 HTML

## 快速开始

```bash
# 1. 克隆并安装
git clone https://github.com/your-org/pixelmsg
cd pixelmsg
npm install
npx playwright install chromium

# 2. 渲染一个模板
./scripts/render.sh templates/weather.html

# 3. 使用输出路径
# → /absolute/path/to/screenshots/weather-default-mobile.png
```

## 模板列表

| 模板 | 描述 | 视口 |
|---|---|---|
| `templates/weather.html` | 通用天气卡片 — 城市、温度、3 日预报 | 移动端 |
| `templates/shanghai-weather.html` | 上海实时天气（Open-Meteo API） | 移动端 |
| `templates/github-trending.html` | GitHub 热榜 Top 10，含 star 数和语言 | 移动端 |
| `templates/github-stats.html` | GitHub 用户主页 — 贡献、连续天数、置顶仓库 | 桌面端 |
| `templates/todolist.html` | 分类待办清单，带进度概览 | 移动端 |

所有模板均使用真实演示数据，无需构建即可渲染。用浏览器打开任意 `.html` 文件即可预览。

## 使用方法

### 命令行

```bash
# 默认设置渲染（移动端视口，输出到 ./screenshots）
./scripts/render.sh templates/weather.html

# 自定义输出目录和视口
./scripts/render.sh templates/github-stats.html ./output desktop

# 通过 URL 参数注入数据
node screenshot.mjs templates/todolist.html --params category=工作 --viewport mobile
```

### 作为 Agent Skill 使用

pixelmsg 设计为 [OpenClaw](https://github.com/openclaw/openclaw) Agent Skill。Agent 读取 `SKILL.md` 来了解何时及如何使用。

```bash
# 通过 npx 安装（发布后可用）
npx skills add pixelmsg

# 或将 agent 运行时指向此目录
SKILL_PATH=/path/to/pixelmsg
```

Agent 调用 `render.sh` 后会得到一个绝对路径。OpenClaw 及兼容运行时会自动将其作为图片消息发送 —— 无需额外代码。

### 编写自己的模板

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <script src="https://cdn.tailwindcss.com"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
</head>
<body>
  <div id="app" x-data="{ message: 'Hello from pixelmsg' }">
    <div class="w-[390px] p-8 bg-white">
      <p class="text-2xl font-bold text-gray-900" x-text="message"></p>
    </div>
  </div>
</body>
</html>
```

规则：所有内容包裹在 `#app` 内，数据内联，渲染时避免外部 API 调用。

## `screenshot.mjs` 参数

| 参数 | 默认值 | 说明 |
|---|---|---|
| `--viewport` | `all` | `mobile` / `tablet` / `desktop` / `all` |
| `--width` | — | 自定义宽度（覆盖 `--viewport`） |
| `--height` | `900` | 视口高度 |
| `--selector` | `#app` | 要截取的 CSS 选择器 |
| `--out` | `./screenshots` | 输出目录 |
| `--name` | *（取自文件名）* | 输出文件名前缀 |
| `--params key=val` | — | 注入页面的 URL 查询参数 |
| `--full-page` | 关 | 截取完整页面而非元素 |
| `--device-scale` | `2` | 设备像素比（视网膜屏质量） |

## 贡献

欢迎贡献，尤其是新模板。一个好的模板应该：

- 自包含（无构建步骤，渲染时无外部 API 调用）
- 在 390px 或 800px 宽度下能干净地填充 `#app` 元素
- 使用真实演示数据，而非占位文本
- 遵循 `SKILL.md` 中的设计规范

请在 `templates/` 中添加模板，在 `screenshots/` 中添加截图，然后提交 PR。

## License

MIT
