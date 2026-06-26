---
name: git-monitor
description: 通用 Git 项目监控工具。支持 GitHub、GitLab、Gitee 等所有 Git 平台。可以添加、删除、检查任意 Git 仓库的更新，自动拉取代码并生成变更摘要。当用户询问"监控项目"、"检查更新"、"添加仓库"、"代码有什么变化"、"拉取最新代码"、"仓库更新通知"、"自动同步代码"、"追踪项目变更"时使用此技能。即使用户没有明确说"监控"，只要涉及跟踪代码仓库的变化、获取更新通知、或需要定期检查项目状态，都应该使用此技能。
trigger:
  - 监控项目
  - 监控仓库
  - 检查更新
  - 添加仓库
  - 删除监控
  - 仓库列表
  - GitHub
  - GitLab
  - Gitee
  - 代码变化
  - 拉取代码
  - 同步代码
---

# Git 项目监控技能

自动监控 Git 项目更新（支持 GitHub、GitLab、Gitee 等所有 Git 平台），拉取最新代码并生成变更摘要。

## 🚀 快速开始（只需3步）

### 第1步：安装技能
```bash
clawhub install git-monitor
```

### 第2步：告诉我你要监控什么
直接在对话中说：
> "监控 GitHub 项目 anthropics/skills"

> "监控 https://gitee.com/mindspore/mindspore"

### 第3步：开启自动推送（可选）
说："设置定时检查，每6小时一次"

然后就完事了！有代码更新会自动推送到你的飞书/当前聊天窗口。

---

## 📖 完整使用指南

### 添加监控仓库
```
监控 GitHub 项目 anthropics/skills
监控 https://github.com/openai/openai-python
监控 GitLab 项目 gitlab-org/gitlab
监控 Gitee 项目 openharmony/docs
```

### 查看监控列表
```
查看监控列表
列出所有监控的仓库
```

### 手动检查更新
```
检查所有更新
检查 anthropics/skills 的更新
```

### 删除监控
```
删除监控 anthropics/skills
```

### 开启/修改定时检查
```
设置定时检查，每1小时一次
关闭定时检查
```

---

## ⚙️ 飞书通知配置（0配置，开箱即用）

### ✅ 推荐：OpenClaw 主配置（无需任何操作）
如果你的 OpenClaw 已经配置了飞书机器人，**自动读取，无需任何操作**。

技能会级联读取飞书凭证，优先级：
1. 环境变量 `FEISHU_APP_ID` / `FEISHU_APP_SECRET` / `FEISHU_CHAT_ID`
2. OpenClaw 主配置 `~/.openclaw/openclaw.json` 中的飞书配置
3. 以上都没有 → 跳过飞书推送（不影响 Git 监控功能）

### 可选：使用自己的飞书机器人
```bash
# 环境变量方式
export FEISHU_APP_ID="cli_xxx"
export FEISHU_APP_SECRET="xxx"
export FEISHU_CHAT_ID="ou_xxx"
```

或在 OpenClaw 配置中添加：
```json
"feishu": {
  "appId": "cli_xxx",
  "appSecret": "xxx",
  "chatId": "ou_xxx"
}
```

### 获取飞书配置
1. 访问 https://open.feishu.cn/ 创建企业自建应用
2. 获取 App ID 和 App Secret
3. 开启权限：`im:chat:read:chat_id` 和 `im:message:send_as_bot`
4. 将应用添加到群聊，获取群聊 ID

---

## 💻 命令行用法

```bash
cd ~/.openclaw/workspace/skills/git-monitor

# 添加仓库
node helper.js add https://github.com/owner/repo

# 查看列表
node helper.js list

# 检查更新
node helper.js check

# 删除仓库
node helper.js remove owner/repo
```
