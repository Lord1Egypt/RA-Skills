---
name: health-check
version: 1.0.0
description: 每日安全检查。检查 OpenClaw Gateway、磁盘空间、内存使用等系统健康状态。触发时机：cron 定时任务或手动调用。
---

# Health Check

每日系统安全检查，确保 OpenClaw 和环境正常运行。

## 核心流程

1. 读取 references/spec.md 获取详细规范
2. 检查 Gateway 运行状态
3. 检查磁盘空间
4. 检查内存使用
5. 检查最近日志有无错误
6. 生成报告并发送

## 触发时机

- cron 定时任务（建议每日）
- 用户明确要求时

## 投递规则（必须）

完成报告后，通过消息工具发送。
- 渠道：feishu
- 目标：<飞书群ID或用户ID>
如果报告超过 3800 字符，分成多条消息发送。
每条消息必须语义完整（不断开 URL 或格式）。
如果发送失败，重试一次。如果仍然失败，输出错误——永远不要静默退出。

## 输出

- 报告位置：`data/exec-logs/health-check/YYYY-MM-DD.md`
- 消息推送到飞书群
