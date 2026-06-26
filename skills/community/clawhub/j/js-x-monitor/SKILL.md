---
name: js-x-monitor
description: "X.com (Twitter) 账号监控自动化 — 定时抓取指定账号最新推文，发现新内容即时推送通知到消息渠道"
version: 1.0.0
metadata:
  openclaw:
    emoji: "\U0001F4E1"
    os:
      - windows
      - macos
      - linux
    requires:
      bins:
        - node
---

# js-x-monitor-skill

X.com (Twitter) 账号监控自动化 Skill。

## 描述

定时监控指定 X.com 账号的最新推文，发现新内容即时推送通知到消息渠道（飞书/微信/Discord）。适合跟踪行业动态、竞品信息、技术趋势等场景。

## 适用场景

- 跟踪技术大牛的最新观点
- 监控竞品账号的产品动态
- 收集行业资讯和趋势
- 自动化信息收集工作流

## 前置依赖

- OpenClaw >= 2026.3.0
- js-eyes 插件 >= 1.4.0
- js-search-x 技能 >= 1.0.0
- 浏览器已登录 X.com

## 安装

```bash
openclaw skill install js-x-monitor
```

## 配置

初始化配置：

```bash
openclaw x-monitor init
```

编辑 `~/.openclaw/x-monitor/config.json`：

```json
{
  "accounts": [
    { "username": "karpathy", "enabled": true },
    { "username": "OpenAI", "enabled": true }
  ],
  "notification": {
    "channels": ["feishu"],
    "includeRetweets": false,
    "includeReplies": false,
    "summaryLength": 100
  },
  "deduplication": {
    "method": "id_and_hash",
    "historyDays": 30
  },
  "checkInterval": 3600
}
```

## 使用

### 添加监控账号

```bash
openclaw x-monitor add <username>
```

### 启动监控

```bash
openclaw x-monitor start
```

### 查看状态

```bash
openclaw x-monitor status
```

## AI 工具

本 Skill 注册以下 AI 工具：

| 工具名 | 描述 |
|--------|------|
| `x_monitor_add_account` | 添加监控账号 |
| `x_monitor_remove_account` | 移除监控账号 |
| `x_monitor_list_accounts` | 列出监控账号 |
| `x_monitor_get_status` | 获取监控状态 |
| `x_monitor_test_account` | 测试单个账号 |

## 数据存储

- 状态文件：`~/.openclaw/x-monitor/state/`
- 配置文件：`~/.openclaw/x-monitor/config.json`

## 开源协议

MIT
