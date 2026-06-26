# Grok Scraper 🐾

[English](./README.md) | [中文](./README_zh.md)

> 🚀 **摆脱 API 计费枷锁，零成本释放 Grok AI 的真正潜力！**

市面上大多数的 X AI (Grok) 集成工具都需要你申请并绑定昂贵的 **X API KEY**。这不仅门槛极高，而且随着对话量的增加，成本也会飙升。

**Grok Scraper 带来了一个颠覆性的解决方案：**
本项目专为 **X (Twitter) Premium 用户** 打造！通过 Playwright 浏览器自动化技术，我们让你能够**绕过 API 限制，以零额外成本使用 Grok 的强大功能**。只要你是 Premium 会员，就可以享受**真正免费的调用**，完全没有任何 API 计费焦虑。开箱即用！

---

## 🎬 预览

[<video src="./assets/grok-2026-03-15T10-01-45.webm" controls width="100%"></video>](https://github.com/user-attachments/assets/d48c7948-11d5-4606-baf8-db0a0b0a095f)

---

## 🌟 核心优势

- 💰 **绝对零成本**：无需购买 X API KEY 或按 token 付费。X Premium 用户可以直接免费使用。
- 🚀 **开箱即用**：省去繁琐的开发者账号申请和 API 配置。只需在网页端登录即可开始自动化查询。
- 🌐 **原生体验**：基于真实的浏览器环境，完美模拟人类交互，获取最真实的 Grok 实时网络搜索和对话能力。

---

## ⚠️ 使用前提

- 主机上必须已安装 **OpenClaw**。
- 必须通过登录步骤在浏览器中**登录 x.com** 并保存会话。没有有效会话，所有查询都将失败。

| 设备 / 环境 | 是否支持 |
|---|---|
| 💻 本地 macOS / Windows / Linux 桌面 | ✅ 完全支持 |
| 🖥️ 远程桌面（如 VNC、RDP、带 GUI 的云虚拟机） | ✅ 支持 |
| ☁️ 无屏幕云服务器 / VPS | ❌ 不支持 — 登录步骤需要打开真实浏览器窗口 |
| 🤖 CI/CD 流水线（如 GitHub Actions 等） | ❌ 不支持 |

---

## 📦 安装

**作为 OpenClaw Skill 安装：**
```bash
git clone https://github.com/aquarius-wing/grok-scraper.git ~/.openclaw/skills/grok-scraper
```

---

## 📁 文件结构

```text
grok-scraper/
├── SKILL.md              # 核心 Agent 指令
├── README.md             # 面向人类的说明
├── scripts/              # 集中存放所有执行脚本
│   ├── package.json      # 依赖与命令配置
│   ├── login.js          # 首次登录：启动浏览器进行手动登录
│   ├── scrape.js         # 核心脚本：发送提示词并抓取回复
│   └── run.sh            # Cron 定时任务入口
├── session/              # 浏览器会话数据（登录后自动生成）
└── output/               # 抓取结果
    ├── latest.md         # 最新结果
    └── grok-*.md         # 历史结果（按时间戳命名）
```

---

## 🚀 使用指南

### 0. 安装依赖
```bash
cd scripts
npm install
npx playwright install chromium
```

### 1. 首次登录
```bash
cd scripts
npm run login
# 在打开的浏览器中登录 x.com
# 登录完成后返回终端并按回车键
```

### 2. 执行查询
```bash
scripts/run.sh "你的自定义问题"
# 结果写入 output/latest.md
```

`run.sh` 是正式入口，负责写入日志到 `output/run.log`、Grok 服务错误时自动重试，以及会话失效时创建 `output/notify-login-expired` 标志文件。

### 3. 定时执行（Cron）
```bash
crontab -e
```
添加一行，每 6 小时执行一次：
```
0 */6 * * * /path/to/grok-scraper/scripts/run.sh "你的定时提示词"
```

### 4. 调试
如需绕过日志和重试逻辑直接检查输出：
```bash
cd scripts
npm run scrape -- "你的自定义问题"
```
