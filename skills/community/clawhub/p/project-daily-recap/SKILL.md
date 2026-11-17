---
name: project-daily-recap
description: 项目进度定时复盘提醒 — 每晚8点自动推送复盘消息到微信，零LLM依赖，cron触发，适合工控/自动化/制造项目用
version: 1.0.0
slug: project-daily-recap
publisher: 
tags:
  - reminder
  - weixin
  - project-management
  - automation
  - daily-recap
---

# Project Daily Recap — 项目进度定时复盘

每晚 20:00 准时推送项目复盘提醒到微信。

> 💡 **定位：** 针对工厂/自动化/改造行业的项目复盘场景。**不依赖 LLM**，纯 Shell + OpenClaw 消息通道，哪怕 AI API 挂了照样推送。

---

## 特点

| 特性 | 说明 |
|------|------|
| 🔌 **零 LLM 依赖** | 不需要 DeepSeek/OpenAI 等任何 AI API |
| 📱 **微信推送** | 走 OpenClaw 消息通道，直达微信 |
| ⏰ **cron 触发** | 系统 cron 定时执行，不受 OpenClaw 心跳影响 |
| 🧩 **可配置** | 项目名称、推送时间、检查项、消息模板均可改 |
| 📝 **日志可追溯** | 每次推送记录到 `reminder.log` |
| 🛠️ **一键安装** | `bash setup.sh` 自动配置 |

---

## 安装

### 前置条件

- OpenClaw 已部署运行
- Node.js v22+（OpenClaw 要求）
- 微信通道（openclaw-weixin）已配置

### 安装步骤

```bash
# 克隆或下载技能到 skills 目录
cd ~/.openclaw/workspace/skills
git clone <repo-url> project-daily-recap

# 或者直接放在 skills 目录下
mkdir -p project-daily-recap
# 把文件复制进去

# 运行安装脚本
cd project-daily-recap
bash setup.sh
```

安装脚本会自动：
1. ✅ 检测 Node.js 版本
2. ✅ 检测当前 OpenClaw 登录状态
3. ✅ 读取当前会话信息自动配置微信接收人
4. ✅ 写入 cron 定时任务（默认每晚 20:00）
5. ✅ 测试发送一条消息验证

---

## 配置

编辑 `config` 文件：

```bash
# 项目名称
PROJECT_NAME="我的项目"

# 今日进度（每天手动更新）
TODAY_PROGRESS=""

# 明日计划
TOMORROW_PLAN=""

# 需要提醒的检查项（逗号分隔）
CHECKLIST="发了技术内容?,有客户沟通?,项目有推进?"

# 推送时间（24小时制）
PUSH_HOUR=20
PUSH_MINUTE=0

# 微信通道配置（setup.sh 会自动填写）
WEIXIN_CHANNEL="openclaw-weixin"
WEIXIN_TARGET="xxx@im.wechat"
WEIXIN_ACCOUNT="xxx-im-bot"
```

---

## 使用

### 每日使用

1. **白天工作** — 正常干活
2. **20:00 自动推送** — 微信收到复盘提醒
3. **回复进度** — 发到对话里，第二天手动更新 `config` 中的 `TODAY_PROGRESS` 和 `TOMORROW_PLAN`

### 手动触发测试

```bash
bash reminder.sh
```

### 查看日志

```bash
cat ~/.openclaw/workspace/skills/project-daily-recap/reminder.log
```

### 查看/编辑 cron 任务

```bash
crontab -e
```

默认条目：
```
0 20 * * * /bin/bash /home/ubuntu/.openclaw/workspace/skills/project-daily-recap/reminder.sh
```

---

## 自定义消息模板

编辑 `reminder.sh` 中的 `MESSAGE` 变量，可以自定义推送内容和格式。

默认模板包含：
- 📅 日期 + 星期
- 📋 今日复盘提示
- 📌 明日计划提示
- ⚠️ 阶段目标提醒
- 📊 已记录进度（如有）

---

## 文件结构

```
project-daily-recap/
├── SKILL.md        # 技能文档（本文件）
├── reminder.sh     # 执行脚本
├── config          # 配置文件
├── setup.sh        # 安装配置脚本
└── reminder.log    # 运行日志（自动生成）
```

---

## 与 LLM 类提醒的区别

| 对比项 | project-daily-recap | LLM 类提醒 |
|--------|---------------------|------------|
| AI API 依赖 | ❌ 无 | ✅ 需要 |
| API 宕机影响 | ❌ 不影响 | ✅ 推送失败 |
| 消息灵活性 | 固定模板，可手动改 | 动态生成 |
| 整机权重 | 极低 | 较高 |
| 可靠性 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |

---

## 故障排查

**推送失败：`Node.js v22+ is required`**

→ 脚本已内置自动检测，若仍出现：
```bash
# 确认 nvm 中的 Node 版本
nvm use 22
node --version
```

**推送失败：`Not logged in`**

→ OpenClaw 未登录，确认 `.openclaw/credentials` 存在。
```bash
openclaw status
```

**消息没收到**

→ 检查 `reminder.log` 看是否成功发送
→ 检查 cron 是否运行：`crontab -l`
→ 手动测试：`bash reminder.sh`

---

## License

MIT
