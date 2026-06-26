# Integration Guide

## Cron Job Integration

Wrap cron task logic with task pulse calls:

```
# In cron task message:
1. python3 task_pulse.py create "日报发布" "抓取" "筛选" "写稿" "封面" "发布" "通知"
2. After each step: task_pulse.py next + message push
3. On success: task_pulse.py done + message push  
4. On failure: task_pulse.py error + message push
```

## Sub-Agent Integration

When spawning sub-agents for long tasks:

1. **Parent creates task** before spawning sub-agent
2. **Sub-agent updates file** via `task_pulse.py next/heartbeat`
3. **Parent pushes to user** via `message` tool when sub-agent reports back
4. Or: sub-agent writes file, parent polls status on heartbeat

## Heartbeat Cleanup

Add to HEARTBEAT.md:
```
- Run task cleanup: python3 ~/.openclaw/workspace/skills/live-task-pulse/scripts/task_pulse.py cleanup
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| TASK_PULSE_DIR | ~/.openclaw/workspace/tasks | Task JSON storage |
| TASK_PULSE_TZ | 8 | UTC offset hours |
| TASK_PULSE_STALL | 180 | Stall threshold (seconds) |

## Multi-Agent Setup

For teams with multiple agents sharing a workspace:
- Each agent uses a unique task name prefix (e.g., `agent1-daily-news`)
- Tasks dir is shared, allowing cross-agent visibility
- Status query shows all agents' tasks

## Push Message Templates

### Start
```
🚀 开始【{taskName}】
📋 共{N}步: {step1} → {step2} → ...
🔄 当前: {step1}
```

### Progress  
```
✅ [{done}/{total}] {stepName}完成（{message}）
🔄 → {nextStep}
```

### Complete
```
🎉 【{taskName}】完成！({duration})
结果: {result}
```

### Error
```
❌ 【{taskName}】失败
错误: {error}
当前步骤: {currentStep} [{done}/{total}]
```

### Stall Alert
```
⚠️ 【{taskName}】可能卡住了
最后更新: {updatedAt}（{elapsed}前）
当前步骤: {currentStep} [{done}/{total}]
```
