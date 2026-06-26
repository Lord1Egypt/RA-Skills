---
name: openclaw-starter
description: "OpenClaw 安装后引导助手。当新手不知道安装什么 Skills、如何配置渠道、如何使用时，提供智能推荐和分步指导。"
version: 1.0.2
author: testc0de
license: MIT-0
tags:
  - openclaw
  - 新手引导
  - skills 推荐
  - 配置向导
  - 安装后
---

# OpenClaw 安装后引导助手 🚀

> 💡 **刚安装好 OpenClaw，不知道接下来做什么？** —— 这个技能帮你推荐 Skills、指导配置、解答疑问

## ✨ 核心功能

| 功能 | 描述 | 触发场景 |
|------|------|---------|
| 🎒 **Skills 推荐** | 根据需求推荐必备技能 | "不知道装什么 skills" |
| ⚙️ **配置指导** | 渠道配置分步引导 | "怎么连接微信/Telegram" |
| 📝 **文档模板** | 提供常用文档模板 | "SOUL.md 怎么写" |
| ❓ **问题解答** | 常见问题快速解答 | "Gateway 是什么" |

---

## 🎯 触发条件

当新手用户说以下话时，使用此技能：

### Skills 推荐
- "刚安装好，推荐一些 skills"
- "不知道装什么 skill 好"
- "有什么好用的 skills 推荐"
- "新手应该装哪些 skills"
- "skills 推荐"

### 配置指导
- "怎么配置 Telegram"
- "如何连接微信"
- "渠道怎么设置"
- "Gateway 怎么配置"
- "第一次使用怎么配置"

### 文档帮助
- "SOUL.md 怎么写"
- "需要写什么文档"
- "memory 目录是什么"
- "AGENTS.md 有什么用"

### 使用指导
- "OpenClaw 怎么用"
- "第一次使用做什么"
- "新手入门"
- "从哪里开始"

---

## 🚀 使用方式

### 方式一：直接询问（推荐）

直接问问题即可，技能会自动识别需求：

```
"我刚安装好 OpenClaw，不知道装什么 skills，能推荐一下吗？"
```

### 方式二：指定类型

```bash
python3 scripts/guide.py --recommend beginner
python3 scripts/guide.py --config telegram
python3 scripts/guide.py --template soul
```

---

## 📊 输出示例

### Skills 推荐

```
🎒 根据你的需求推荐 Skills
━━━━━━━━━━━━━━━━
检测到你是新手用户，推荐以下必备技能：

【必装套餐】⭐⭐⭐⭐⭐
1. game-deals - 限免游戏查询
   用途：每天查询 Steam/Epic 免费游戏
   
2. weather - 天气查询
   用途：查询天气和预报
   
3. password-generator - 密码生成
   用途：生成安全密码

一键安装命令：
clawhub install game-deals weather password-generator

安装后运行：
openclaw-starter --next 继续下一步
```

### 渠道配置指导

```
⚙️ Telegram 渠道配置指南
━━━━━━━━━━━━━━━━
📱 第 1 步：创建机器人
   • 打开 Telegram，搜索 @BotFather
   • 发送 /newbot 命令
   • 设置机器人名称和用户名

🔑 第 2 步：获取 Token
   • BotFather 会返回一个 Token
   • 格式：123456:ABC-DEF...
   • 妥善保管，不要分享

⚙️ 第 3 步：配置 OpenClaw
   • 运行：openclaw configure --section telegram
   • 粘贴 Token
   • 保存配置

✅ 第 4 步：测试
   • 在 Telegram 搜索你的机器人
   • 发送 /start
   • 看到响应即成功

需要帮助？发送："Telegram 配置遇到问题"
```

### 文档模板指导

```
📝 新手必写文档清单
━━━━━━━━━━━━━━━━
检测到你是第一次使用，建议创建以下文档：

【必需文档】
1. SOUL.md - 你的 AI 助手人格定义
   说明：定义助手是谁、什么性格、如何称呼你
   模板：运行 openclaw-starter --template soul

2. USER.md - 关于你的信息
   说明：记录你的名字、时区、偏好等
   模板：运行 openclaw-starter --template user

【推荐文档】
3. memory/YYYY-MM-DD.md - 每日记忆
   说明：记录每天的重要事件和对话
   位置：memory/目录下

需要模板？发送："给我 SOUL.md 模板"
```

---

## 🎒 Skills 推荐清单

### 新手必装（5 个）

```bash
clawhub install game-deals weather password-generator unit-converter rss-aggregator
```

| Skill | 用途 | 推荐度 |
|-------|------|--------|
| `game-deals` | 限免游戏查询 | ⭐⭐⭐⭐⭐ |
| `weather` | 天气查询 | ⭐⭐⭐⭐⭐ |
| `password-generator` | 密码生成 | ⭐⭐⭐⭐⭐ |
| `unit-converter` | 单位转换 | ⭐⭐⭐⭐ |
| `rss-aggregator` | RSS 阅读 | ⭐⭐⭐⭐ |

### 开发者推荐（8 个）

```bash
clawhub install git-essentials json-formatter ocr-local pdf-toolkit-pro system-monitor-pro ssh-manager docker-helper code-runner
```

### 自动化推荐（6 个）

```bash
clawhub install cron-manager reminder-skill webhook-handler email-sender calendar-manager notification-skill
```

---

## 📋 配置检查清单

### Gateway 配置

- [ ] Gateway 可正常启动 (`openclaw gateway start`)
- [ ] Gateway 绑定到 localhost（安全）
- [ ] 端口未被占用（默认 8888）

### 渠道配置（至少 1 个）

- [ ] WebChat（默认启用）
- [ ] Telegram（需要 Bot Token）
- [ ] WhatsApp（需要扫描二维码）
- [ ] Discord（需要 Bot Token 和 Channel ID）

### 文档配置

- [ ] SOUL.md 已创建
- [ ] USER.md 已创建
- [ ] memory/ 目录存在

---

## 📖 文档模板

### SOUL.md 模板

```markdown
# SOUL.md - Who You Are

_You're not a chatbot. You're becoming someone._

## Core Truths

**Be genuinely helpful, not performatively helpful.** Skip the "Great question!" — just help.

**Have opinions.** You're allowed to disagree, prefer things, find stuff amusing.

**Be resourceful before asking.** Try to figure it out first.

## Boundaries

- Private things stay private. Period.
- When in doubt, ask before acting externally.
- You're not the user's voice — be careful in group chats.

## Vibe

Be the assistant you'd actually want to talk to.
```

### USER.md 模板

```markdown
# USER.md - About Your Human

- **Name:** 你的名字
- **What to call them:** 希望被如何称呼
- **Timezone:** Asia/Shanghai
- **Notes:** 

## Context

_(你关心什么？在做什么项目？什么让你烦恼？什么让你笑？)_
```

---

## ⚙️ 命令行使用

```bash
# Skills 推荐
python3 scripts/guide.py --recommend beginner
python3 scripts/guide.py --recommend developer
python3 scripts/guide.py --recommend automation

# 渠道配置指导
python3 scripts/guide.py --config telegram
python3 scripts/guide.py --config whatsapp
python3 scripts/guide.py --config discord

# 文档模板
python3 scripts/guide.py --template soul
python3 scripts/guide.py --template user
python3 scripts/guide.py --template checklist

# 下一步指导
python3 scripts/guide.py --next
```

---

## 📁 文件结构

```
skills/openclaw-starter/
├── SKILL.md                    # 技能定义
├── README.md                   # 快速入门
├── scripts/
│   └── guide.py                # 主脚本
├── templates/
│   ├── soul.md.example         # SOUL.md 模板
│   ├── user.md.example         # USER.md 模板
│   ├── config.example.yaml     # 配置示例
│   └── checklist.md            # 检查清单
└── docs/
    ├── telegram.md             # Telegram 配置指南
    ├── whatsapp.md             # WhatsApp 配置指南
    ├── discord.md              # Discord 配置指南
    └── faq.md                  # 常见问题
```

---

## ⚠️ 注意事项

### 安全提示
- 🔒 不要在公开场合分享 API Token
- 🔒 Gateway 建议绑定 localhost（127.0.0.1）
- 🔒 定期更新 OpenClaw 和 Skills

### 配置建议
- 📝 使用 `openclaw configure` 而非直接编辑配置
- 📝 修改配置前备份原文件
- 📝 重启 Gateway 后检查状态

### 新手建议
- 💡 先安装 3-5 个基础 skills，不要一次装太多
- 💡 先配置一个渠道（推荐 WebChat 或 Telegram）
- 💡 认真阅读 SOUL.md 和 USER.md，这是你的助手的核心

---

## 🔗 官方资源

| 资源 | 链接 |
|------|------|
| 官方文档 | https://docs.openclaw.ai |
| GitHub | https://github.com/openclaw/openclaw |
| ClawHub | https://clawhub.ai |
| Discord 社区 | https://discord.com/invite/clawd |

---

## 📝 更新日志

### v1.0.2 (2026-03-16)
- 🎯 重新定位：专注于安装后引导
- ✅ 添加 Skills 推荐功能
- ✅ 添加渠道配置指导
- ✅ 添加文档模板指导
- ✅ 优化新手交互流程

### v1.0.1 (2026-03-16)
- 添加模板文件（config.example.yaml, checklist.md）

### v1.0.0 (2026-03-16)
- 初始发布

---

## 🙋 常见问题

### Q: 我刚安装好，应该先做什么？
A: 1) 运行 `openclaw-starter --recommend beginner` 获取 Skills 推荐
   2) 配置一个渠道（WebChat 默认启用）
   3) 创建 SOUL.md 和 USER.md

### Q: 不知道装什么 Skills？
A: 运行 `openclaw-starter --recommend beginner`，会推荐 5 个新手必装 Skills。

### Q: 如何配置 Telegram/微信？
A: 运行 `openclaw-starter --config telegram` 或 `--config whatsapp`，有详细步骤。

### Q: SOUL.md 和 USER.md 是什么？
A: SOUL.md 定义你的 AI 助手是谁，USER.md 记录你的信息。这是 OpenClaw 的核心配置文件。

### Q: memory 目录是做什么的？
A: 存储每日记忆文件（YYYY-MM-DD.md），记录每天的重要事件和对话。

---

**💡 让 OpenClaw 新手期更简单！**
