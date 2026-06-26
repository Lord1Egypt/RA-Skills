# linsoai-track

定时任务管理 OpenClaw Skill。用自然语言创建和管理定时任务，AI 自动执行并通知结果。

## 安装

```bash
openclaw skills install linsoai-track
```

## 快速开始

安装后，直接用自然语言描述你的需求：

```
"帮我创建一个每天早上9点的任务，查看BTC价格变化，如果波动超过5%就通知我"
```

Skill 会自动解析你的描述并创建定时任务，包含频率、时区、通知条件等配置。

### 更多示例

**每3小时检查一次服务器状态：**
```
"每3小时检查一下我的服务器 api.example.com 是否正常，异常就通知我"
```

**每周一生成周报：**
```
"每周一上午10点帮我汇总上周AI领域新闻，生成周报发到我的飞书"
```

**一次性提醒：**
```
"3月15号下午2点提醒我域名要到期了"
```

## 管理任务

```
"看看我有哪些定时任务"
"暂停BTC价格监控"
"删除服务器状态检查任务"
"手动跑一次每周报告"
```

## 通知配置

### IM 通知（推荐）

开箱即用，支持 Telegram、飞书、Discord、Slack 等 18 个渠道：

```bash
# 先配置渠道
openclaw channels add telegram --token <BotToken> --chat <ChatID>
```

### 邮件通知

需要安装 send-email skill 并配置 SMTP：

```bash
openclaw skills install send-email
```

详见 [通知配置指南](references/NOTIFICATIONS.md)。

## 从 Linso Track 迁移

如果你是 Linso Track 用户，可以快速将现有任务迁移过来：

1. 登录 Linso Track → 点击「迁移到龙虾」按钮
2. 生成迁移内容后，复制导出的自然语言描述
3. 粘贴到 OpenClaw 聊天窗口发送，AI 会自动批量创建所有任务
4. 检查导入结果：
```
"看看我的定时任务列表"
```

## 依赖

- **send-email skill**（可选）— 邮件通知功能需要

## 参考文档

- [任务模板库](references/TEMPLATES.md) — 常用任务模板
- [调度频率速查](references/SCHEDULING.md) — cron 表达式和时区
- [通知配置指南](references/NOTIFICATIONS.md) — 邮件、IM、Webhook 配置
