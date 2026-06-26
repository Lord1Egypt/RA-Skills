---
name: openclaw-relation
description: OpenClaw 完整文档知识库。涵盖安装、配置、Gateway 网关、渠道、节点、CLI 命令、自动化、安全等所有核心功能。
homepage: https://docs.openclaw.ai/zh-CN
---

# OpenClaw - 完整文档

## 概述

OpenClaw 是一个适用于任何操作系统的 AI 智能体 Gateway 网关，支持 WhatsApp、Telegram、Discord、iMessage 等多种聊天渠道。通过单个 Gateway 网关进程将聊天应用连接到编程智能体。

## 核心架构

```
Chat apps + plugins → Gateway → 智能体/CLI/Web UI/macOS/iOS/Android
```

**Gateway 网关**是会话、路由和渠道连接的唯一事实来源。

## 核心功能

### 多渠道 Gateway 网关
- 通过单个 Gateway 进程连接多个聊天应用
- 支持同时运行多个渠道

### 插件渠道
- 通过扩展包添加 Mattermost 等更多渠道
- 支持自定义渠道开发

### 多智能体路由
- 按智能体、工作区或发送者隔离会话
- 支持多智能体并行运行

### 媒体支持
- 发送和接收图片、音频、文档
- 支持 Canvas 和媒体理解

### Web 控制界面
- 浏览器仪表板管理聊天、配置和会话
- 实时监控和调试

### 移动节点
- 配对 iOS 和 Android 节点
- 支持 Canvas 远程显示

## 快速开始

### 1. 安装 OpenClaw

```bash
npm install -g openclaw@latest
```

### 2. 新手引导并安装服务

```bash
openclaw onboard --install-daemon
```

### 3. 配对渠道并启动 Gateway

```bash
openclaw channels login
openclaw gateway --port 18789
```

## 访问 Web 控制界面

- **本地**：http://127.0.0.1:18789/
- **远程**：通过 Tailscale 或 SSH 访问

## 配置文件

配置文件位于 `~/.openclaw/openclaw.json`。

### 基本配置示例

```json5
{
  channels: {
    whatsapp: {
      allowFrom: ["+15555550123"],
      groups: {
        "*": { requireMention: true }
      },
    },
  },
  messages: {
    groupChat: {
      mentionPatterns: ["@openclaw"]
    }
  },
}
```

### 配置说明

- 不做任何修改：使用内置 Pi 二进制文件，按发送者创建独立会话
- `allowFrom`：限制允许访问的电话号码
- `requireMention`：群聊中需要 @ 提及才会响应
- `mentionPatterns`：自定义提及模式

## 支持的渠道

### 官方内置渠道
- **WhatsApp** - 最常用的渠道
- **Telegram** - 功能强大的机器人平台
- **Discord** - 游戏和社区平台
- **iMessage** - Apple 设备
- **Signal** - 注重隐私的通讯
- **Slack** - 工作场所协作
- **Google Chat** - Google Workspace 集成
- **Matrix** - 去中心化通讯

### 插件扩展渠道
- **Mattermost** - 企业协作
- **Microsoft Teams** - 微软团队协作
- **IRC** - 互联网中继聊天
- **Feishu** - 飞书
- **LINE** - LINE 通讯
- **Twitch** - 直播平台

## CLI 命令参考

### 核心命令

```bash
# 状态检查
openclaw status

# Gateway 管理
openclaw gateway --port 18789
openclaw gateway start
openclaw gateway stop
openclaw gateway restart

# 渠道管理
openclaw channels login
openclaw channels list
openclaw channels connect

# 配置管理
openclaw config get <key>
openclaw config set <key> <value>
openclaw configure

# 日志查看
openclaw logs
openclaw logs --follow

# 技能管理
openclaw skills list
openclaw skills install <skill>
openclaw skills uninstall <skill>

# 会话管理
openclaw sessions list
openclaw sessions info <id>
openclaw sessions clear <id>

# 节点管理
openclaw nodes list
openclaw nodes pair
openclaw nodes status

# 更新
openclaw update
```

### 向导命令

```bash
# 新手引导
openclaw onboard --install-daemon

# 诊断
openclaw doctor

# 重置
openclaw reset
```

## 节点功能

### 配对移动设备

```bash
openclaw nodes pair
```

支持的设备：
- **iOS** - 需要 OpenClaw iOS App
- **Android** - 需要 OpenClaw Android App

### 节点功能

- **Camera Capture** - 远程拍照
- **Location** - 获取设备位置
- **Audio/Voice** - 录音和语音笔记
- **Canvas** - 远程显示和控制
- **Talk Mode** - 语音交互

## 自动化功能

### Cron Jobs

定期执行任务：

```bash
openclaw cron create "0 9 * * *" "早上好"
```

### Heartbeat

心跳检查，适合定期检查状态：

- 检查邮件
- 检查日历
- 检查通知
- 维护内存

### Webhooks

接收外部事件触发。

### Hooks

在特定事件时执行脚本。

## 安全

### 访问控制

```json
{
  channels: {
    whatsapp: {
      allowFrom: ["+15555550123"],
    },
  },
}
```

### 令牌管理

- 使用 secrets 管理敏感信息
- 支持环境变量
- 支持密钥引用

### 白名单

- 电话号码白名单
- 用户 ID 白名单
- 群组白名单

## 远程访问

### Tailscale

通过 Tailscale 访问远程 Gateway：

```bash
openclaw gateway --tailscale
```

### SSH

通过 SSH 隧道访问：

```bash
ssh -L 18789:localhost:18789 user@remote
```

## 技能 (Skills)

### 创建技能

在 `~/.openclaw/workspace/skills/` 目录下创建：

```
skills/
└── my-skill/
    ├── SKILL.md
    └── (可选的脚本和资源)
```

### SKILL.md 格式

```markdown
---
name: my-skill
description: 技能描述
---

# 技能文档

内容...
```

### 安装技能

```bash
openclaw skills install ./my-skill
```

## 内存管理

### MEMORY.md

长期记忆，存储重要决策、偏好、上下文。

### Daily Notes

`memory/YYYY-MM-DD.md` 存储每日日志。

### 内存维护

定期压缩和整理内存文件。

## 工作区

默认工作区：`~/.openclaw/workspace/`

### 重要文件

- `AGENTS.md` - 工作区配置
- `SOUL.md` - AI 人格定义
- `USER.md` - 用户信息
- `MEMORY.md` - 长期记忆
- `HEARTBEAT.md` - 心跳任务
- `TOOLS.md` - 工具配置

## 故障排除

### 诊断

```bash
openclaw doctor
```

### 常见问题

1. **Gateway 无法启动**
   - 检查端口是否被占用
   - 查看日志：`openclaw logs`

2. **渠道连接失败**
   - 检查网络连接
   - 验证凭证
   - 查看渠道文档

3. **会话丢失**
   - 检查会话配置
   - 查看日志中的错误

### 调试

- **日志**：`openclaw logs --follow`
- **状态**：`openclaw status`
- **Web UI**：访问 http://127.0.0.1:18789/

## 高级功能

### 多智能体

```json
{
  agents: {
    my-agent: {
      model: "anthropic/claude-3-opus",
    },
  },
}
```

### 本地模型

使用 Ollama 或 vLLM 等本地模型。

### 插件

开发自定义插件扩展功能。

## 文档资源

### 官方文档

- **主页**：https://docs.openclaw.ai/zh-CN
- **文档索引**：https://docs.openclaw.ai/llms.txt
- **社区**：https://discord.com/invite/clawd

### 重点文档

- 入门指南
- Gateway 配置
- 渠道设置
- 节点配对
- 自动化
- 安全
- 故障排除

## 最佳实践

### 安全性

1. 使用白名单限制访问
2. 定期更新 OpenClaw
3. 不要在配置中硬编码密钥
4. 使用 secrets 管理敏感信息

### 性能

1. 合理配置会话修剪
2. 使用内存压缩
3. 定期清理旧会话

### 可维护性

1. 使用版本控制管理工作区
2. 文档化自定义配置
3. 定期备份重要文件

## 更新

```bash
openclaw update
```

## 卸载

```bash
openclaw uninstall
```

---

**来源**：OpenClaw 官方文档
**文档链接**：https://docs.openclaw.ai/zh-CN
**文档索引**：https://docs.openclaw.ai/llms.txt
