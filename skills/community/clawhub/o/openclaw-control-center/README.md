# 🦞 openclaw-control-center

> **OpenClaw 可视化控制中心** — 让你对 AI 的运行状态一目了然

一个专为 OpenClaw 用户设计的双模式可视化仪表盘，内置**简洁模式**（普通人也能看懂）和**专业模式**（完整技术数据），无需安装额外软件，浏览器直接打开。

---

## ✨ 功能特色

| 特性 | 说明 |
|------|------|
| 🌿 简洁模式 | 大数字 + 通俗语言 + 说明提示，非技术人员也能快速看懂 |
| 📊 专业模式 | 完整表格 + 架构图 + API 端点，适合技术人员深度排查 |
| 🔄 一键切换 | 页面顶部按钮，实时切换两个模式 |
| 📐 原创设计 | 来自 github.com/TianyiDataScience/openclaw-control-center 理念，但独立实现的静态版 |

---

## 📸 界面预览

### 简洁模式（日常查看）
- 🟢 **系统是否正常** — 一句话回答
- 🧠 **AI 用了多少** — Token 消耗 + 上下文压力
- 👥 **谁在干活** — 工作中/待命/空闲 三态
- 🧩 插件状态 · 🔐 安全设置 · 🧠 记忆系统 · ⏰ 定时任务
- 每个模块附带通俗语言说明

### 专业模式（技术详情）
- 🚀 系统核心指标（Agent / Node.js / Shell / Build）
- 🧠 模型与 Token 详细数据（7天趋势柱状图）
- 💻 会话管理（全部活跃会话 Key / 通道 / 消息数）
- ⏰ Cron Jobs 表格（含 Job ID / Payload / Timeout）
- 🧩 插件表格（含类型 / 状态 / 说明）
- 🔗 OpenClaw 三层架构图（Tools → Skills → Plugins）
- 🔐 安全配置表格（含当前值 + 说明）
- 🔌 Gateway API 端点一览
- ⚡ Lobster 工作流引擎图

---

## 🚀 快速使用

### 方式一：AI 自动生成（推荐）

告诉你的 OpenClaw：
```
打开控制中心
```

AI 会自动采集实时数据，生成 HTML 仪表盘并打开浏览器。

### 方式二：手动打开

直接在浏览器地址栏输入：
```
file:///C:/Users/你的用户名/.qclaw/workspace/control-center.html
```

### 方式三：部署全功能版（推荐进阶用户）

真实 Control Center（React + WebSocket 实时推送）：
```bash
git clone https://github.com/TianyiDataScience/openclaw-control-center.git
cd openclaw-control-center
npm install
cp .env.example .env
npm run build
npm run dev:ui
# 访问 http://127.0.0.1:4310/?section=overview&lang=zh
```

---

## 🛠️ 技能触发方式

| 触发词 | 行为 |
|--------|------|
| `打开控制中心` | 生成简洁模式仪表盘 |
| `控制中心 --pro` | 生成专业模式仪表盘 |
| `控制中心 --html` | 生成 HTML 并打开浏览器 |
| `系统状态` | 简洁模式系统状态 |
| `dashboard` | 同"打开控制中心" |

---

## 📁 文件结构

```
~/.qclaw/workspace/
├── skills/
│   └── openclaw-control-center/
│       ├── SKILL.md        ← 技能定义文件
│       └── README.md       ← 本说明文件
└── control-center.html     ← 生成的仪表盘
```

---

## 🔧 依赖

- OpenClaw 2026.3+（内置 browser / session_status / cron / gateway 等工具）
- 浏览器（Chrome / Edge / Firefox 均支持）
- 无需额外 npm / Node.js（静态版）

---

## 🌟 与真实 Control Center 的关系

本技能灵感来源：
- **GitHub**: https://github.com/TianyiDataScience/openclaw-control-center
- **Stars**: ~1.1k ⭐
- **技术栈**: TypeScript + React + WebSocket

本技能为**静态实现版**，优势：
- ✅ 无需安装，打开即用
- ✅ 无需 npm / Node.js / git
- ✅ 数据实时采集（每次打开都是最新状态）
- ✅ 简洁/专业双模式按需切换

---

## 📝 发布说明

- **版本**: v1.0
- **日期**: 2026-03-22
- **适用**: OpenClaw 用户，尤其是需要可视化监控的非技术用户
- **协议**: OpenClaw AgentSkills 规范
- **作者**: QClaw 自主创建（基于开源社区灵感）
