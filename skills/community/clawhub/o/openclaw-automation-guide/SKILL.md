---
name: openclaw-automation-guide
version: 1.0.0
description: OpenClaw 自动化工作流 - 教你创建自动执行的任务。适合：效率提升、定时任务。
metadata:
  openclaw:
    emoji: "⚡"
    requires:
      bins: []
---

# OpenClaw 自动化工作流指南

让 AI 帮你自动执行任务。

## 定时任务

### 1. 每日简报

```yaml
# ~/.openclaw/config.yaml
cron:
  daily_briefing:
    enabled: true
    schedule: "0 8 * * *"  # 每天 8:00
    task: "generate_briefing"
```

### 2. 价格监控

```yaml
cron:
  price_monitor:
    enabled: true
    schedule: "*/10 * * * *"  # 每 10 分钟
    task: "check_prices"
    notify:
      channel: telegram
      threshold: 5%  # 波动超过 5% 通知
```

### 3. 内容发布

```yaml
cron:
  content_publish:
    enabled: true
    schedule: "0 9 * * *"  # 每天 9:00
    task: "publish_content"
    platforms:
      - juejin
      - zhihu
```

## 事件触发

### 1. 消息触发

```yaml
triggers:
  message:
    - keyword: "订单"
      action: "check_order"
    - keyword: "快递"
      action: "check_delivery"
```

### 2. Webhook 触发

```yaml
triggers:
  webhook:
    - path: /webhook/payment
      action: "process_payment"
    - path: /webhook/error
      action: "handle_error"
```

### 3. 文件触发

```yaml
triggers:
  file:
    - path: ~/Documents/inbox
      action: "process_file"
      pattern: "*.pdf"
```

## 自动化示例

### 1. 自动回复

```yaml
automation:
  auto_reply:
    enabled: true
    rules:
      - match: "你好"
        reply: "你好！有什么可以帮你的？"
      - match: "价格"
        reply: "当前价格：XXX"
```

### 2. 自动分类

```yaml
automation:
  classify:
    enabled: true
    rules:
      - keyword: ["bug", "错误"]
        tag: "问题反馈"
      - keyword: ["建议", "希望"]
        tag: "功能建议"
```

### 3. 自动转发

```yaml
automation:
  forward:
    enabled: true
    rules:
      - source: telegram
        target: discord
      - source: wechat
        target: slack
```

## Skills 自动化

### 创建自动化 Skill

```yaml
# ~/.openclaw/skills/auto_report.yaml
name: auto_report
trigger:
  schedule: "0 18 * * 5"  # 每周五 18:00
action:
  - generate_weekly_report
  - send_email
```

### 启用自动化

```bash
openclaw skill enable auto_report
```

## 监控

### 查看自动化日志

```bash
openclaw logs --filter automation
```

### 查看执行历史

```bash
openclaw automation history
```

## 常见问题

### Q: 定时任务不执行？

检查：
1. 时区设置
2. cron 表达式是否正确
3. OpenClaw 是否在运行

### Q: 如何调试自动化？

```bash
openclaw automation test <task_name>
```

### Q: 如何暂停自动化？

```bash
openclaw automation disable <task_name>
```

## 需要帮助？

- 自动化配置：¥99
- 工作流设计：¥299
- 企业定制：¥999

联系：微信 yang1002378395 或 Telegram @yangster151

---
创建：2026-03-14
