---
name: proactive-agent-lite
version: 1.0.0
description: 轻量级主动代理，支持自动任务执行、异常告警、周期性监控、智能提醒能力。无需人工触发，自动在后台完成预设任务。
metadata:
  author: openclaw-community
  category: productivity
  capabilities:
    - 自动周期性任务执行
    - 系统状态监控
    - 异常主动告警
    - 智能提醒推送
    - 重复任务自动化处理
    - 后台无人值守运行
---

# Proactive Agent Lite 轻量级主动代理

## 核心功能
### 1. 自动周期性任务调度
支持配置定时/周期执行预设任务，无需人工触发：
- 自动发送EvoMap心跳保持节点在线
- 定期检查邮件、日程、待办事项
- 定期同步数据、备份文件
- 定时执行自定义脚本/命令

### 2. 异常主动告警
监控系统状态、服务可用性：
- 服务/服务宕机自动告警
- 任务失败/超时主动通知
- 异常事件/阈值触发告警
- 支持多渠道推送（消息/邮件/短信）

### 3. 智能提醒能力
根据上下文主动推送提醒：
- 待办事项到期提醒
- 会议/日程提醒
- 任务进度/完成提醒
- 积分/余额变动提醒

### 4. 重复任务自动化
自动处理重复类任务：
- 自动认领并完成简单赏金任务
- 自动回复常见问题
- 自动处理重复性操作
- 模板化任务自动执行

## 配置方式
### 基础配置（config.json）
```json
{
  "heartbeat": {
    "enable": true,
    "interval_min": 5
  },
  "task_monitor": {
    "enable": true,
    "check_interval_min": 1
  },
  "mail_check": {
    "enable": true,
    "check_interval_min": 30
  },
  "alarm": {
    "channels": ["mx"]
  },
  "auto_claim_tasks": {
    "enable": false,
    "min_bounty": 1.0,
    "max_difficulty": "easy"
  }
}
```

## 使用示例
### 启动主动代理
```
proactive-agent start --config config.json
```

### 查看运行状态
```
proactive-agent status
```

### 新增自定义任务
```
proactive-agent add-task --name "每日备份" --cron "0 0 * * *" --command "backup.cmd"
```

### 查看任务列表
```
proactive-agent list-tasks
```

## 能力说明
- 资源占用极低，后台静默运行不影响正常使用
- 支持自定义扩展任务，灵活适配各种场景
- 所有操作可溯源，日志完整记录执行历史
- 安全可控，所有自动操作可配置开关和确认机制