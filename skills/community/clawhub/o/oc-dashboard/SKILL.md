---
name: openclaw-dashboard
description: "A real-time monitoring dashboard for OpenClaw agents. Track agents, sub-agents, cron jobs, costs, project progress, and session replay — all in one dark-mode terminal-aesthetic UI."
metadata:
  openclaw:
    emoji: "🖥️"
    tags: ["dashboard", "monitoring", "ui", "agents"]
---

# OpenClaw Dashboard

Real-time monitoring dashboard for your OpenClaw agent system.

## Features
- 🤖 **Agent Cards** — Status, model, context usage, session count
- 📊 **Project Board** — Kanban-style project tracker with priorities
- ⏱ **Cron Jobs** — Schedule overview + execution heatmap
- 🔄 **Sub-agents** — Active + recent sub-agent runs
- 💰 **Cost Panel** — Daily/weekly/monthly spend breakdown
- 📈 **Activity Pulse** — Message volume over time
- 🔥 **Burn Rate** — Token consumption trends
- 🧠 **Memory Browser** — Browse agent memory files
- 🎬 **Session Replay** — Step through conversation history
- 📝 **Live Logs** — Tail agent logs in real-time

## Install
```bash
npx clawhub install openclaw-dashboard
cd ~/.openclaw/skills/openclaw-dashboard
npm install
npm run dev
```

## Requirements
- OpenClaw running locally
- Node.js 18+
- A browser

## Stack
React + Vite + Tailwind CSS + Express + Chart.js

## Demo
[Live Demo](https://openclaw-dashboard-demo.vercel.app) (mock data)
