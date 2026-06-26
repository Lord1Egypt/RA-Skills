# 🖥️ OpenClaw Dashboard

Real-time monitoring dashboard for [OpenClaw](https://openclaw.ai) AI agent systems.

[中文版](#-openclaw-dashboard-中文)

## Features

- 🤖 **Agent Cards** — Status, model, context window usage (up to 1M tokens), session count
- ⚡ **Live Activity Feed** — Real-time view of what every agent is doing right now
- 📊 **Project Board** — Kanban-style project tracker with priorities and next actions
- ⏱ **Cron Jobs** — Schedule overview + execution heatmap
- 🔄 **Sub-agents** — Active + recent sub-agent runs with task summaries
- 💰 **Cost Panel** — Daily/weekly/monthly spend breakdown by model
- 📈 **Activity Pulse** — Message volume chart over time
- 🔥 **Burn Rate** — Token consumption trends
- 🧠 **Memory Browser** — Browse agent memory files in-browser
- 🎬 **Session Replay** — Step through conversation history message by message
- 📝 **Live Logs** — Tail agent logs in real-time

## Quick Start

```bash
git clone https://github.com/Mrpixelraf/openclaw-dashboard.git
cd openclaw-dashboard
npm install
npm run dev
```

Open `http://localhost:5173` in your browser.

## Requirements

- [OpenClaw](https://openclaw.ai) running locally
- Node.js 18+

## Stack

React · Vite · Tailwind CSS · Express · Chart.js

## How It Works

The dashboard reads directly from your local `~/.openclaw/` directory — agent configs, session files, cron logs, cost data. **Zero API calls to any AI provider.** No extra tokens consumed.

The Express server (`port 3721`) serves the API, Vite (`port 5173`) handles the frontend with hot reload.

## Demo

Try the [live demo](https://openclaw-dashboard-demo.vercel.app) with mock data — no OpenClaw installation needed.

## Install via ClawHub

```bash
npx clawhub install openclaw-dashboard
```

## License

MIT

---

# 🖥️ OpenClaw Dashboard 中文

[OpenClaw](https://openclaw.ai) AI Agent 系统的实时监控面板。

## 功能特性

- 🤖 **Agent 状态卡** — 模型、上下文窗口用量（支持 1M token）、会话数
- ⚡ **实时活动流** — 实时查看每个 Agent 正在做什么
- 📊 **项目看板** — 看板式项目追踪，支持优先级和下一步行动
- ⏱ **定时任务** — Cron 任务概览 + 执行热力图
- 🔄 **子 Agent** — 正在运行和最近完成的子任务
- 💰 **费用面板** — 按日/周/月/模型拆分的费用统计
- 📈 **活动脉冲** — 消息量时间轴图表
- 🔥 **消耗趋势** — Token 消耗走势
- 🧠 **记忆浏览器** — 在浏览器中查看 Agent 记忆文件
- 🎬 **会话回放** — 逐条回放对话历史
- 📝 **实时日志** — 实时查看 Agent 日志输出

## 快速开始

```bash
git clone https://github.com/Mrpixelraf/openclaw-dashboard.git
cd openclaw-dashboard
npm install
npm run dev
```

打开浏览器访问 `http://localhost:5173`。

## 环境要求

- 本地运行的 [OpenClaw](https://openclaw.ai)
- Node.js 18+

## 技术栈

React · Vite · Tailwind CSS · Express · Chart.js

## 工作原理

Dashboard 直接读取本地 `~/.openclaw/` 目录中的数据 — Agent 配置、会话文件、Cron 日志、费用记录。**不会调用任何 AI API，零额外 Token 消耗。**

Express 服务器（端口 3721）提供 API，Vite（端口 5173）负责前端热更新。

## 在线演示

体验 [在线 Demo](https://openclaw-dashboard-demo.vercel.app)（模拟数据，无需安装 OpenClaw）。

## 通过 ClawHub 安装

```bash
npx clawhub install openclaw-dashboard
```

## 开源协议

MIT
