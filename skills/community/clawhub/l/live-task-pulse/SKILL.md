---
name: live-task-pulse
description: Real-time task progress tracking with live push notifications. MANDATORY for ALL multi-step tasks (>30s or >2 tool calls). Activate automatically — do not wait for user to request it. Unique dual-layer architecture — file persistence for crash recovery + message tool push for real-time updates. Features step-based progress, stall detection (3min), auto-cleanup, and a Python CLI. Also triggers when user asks "what's running" / "task status" / "任务进度".
---

# Live Task Pulse

Real-time task execution tracking with **live push notifications**.

## Why This Exists

Other trackers write to files — users can't see progress until they ask. Live Task Pulse pushes every step change to the user's chat instantly via OpenClaw's `message` tool, while persisting state to JSON for crash recovery.

## Architecture

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│ task_pulse.py│───>│ JSON on disk │    │ User's chat │
│  (CLI tool)  │    │ (persistence)│    │ (Telegram/  │
└──────┬───────┘    └──────────────┘    │  Discord/..)│
       │                                └──────▲──────┘
       │         ┌──────────────┐              │
       └────────>│ message tool │──────────────┘
                 │ (real-time)  │
                 └──────────────┘
```

**Dual-layer** = no other skill does both.

## Quick Reference

### Create task → push start notification
```bash
TASK_ID=$(python3 scripts/task_pulse.py create "任务名" "步骤1" "步骤2" "步骤3")
```
Then immediately call `message` tool:
```
message(action="send", message="🚀 开始【任务名】\n📋 步骤1 → 步骤2 → 步骤3\n🔄 当前: 步骤1")
```

### Advance to next step → push progress
```bash
python3 scripts/task_pulse.py next "$TASK_ID" "抓取了25条数据"
```
Then push: `message(action="send", message="✅ [1/3] 步骤1完成（抓取了25条数据）\n🔄 → 步骤2")`

### Heartbeat (long step, >1min)
```bash
python3 scripts/task_pulse.py heartbeat "$TASK_ID" "已处理60%"
```
Push only if meaningful progress (avoid spam).

### Complete
```bash
python3 scripts/task_pulse.py done "$TASK_ID" "发布成功 https://..."
```
Push: `message(action="send", message="🎉 【任务名】完成！\n结果: https://...")`

### Fail
```bash
python3 scripts/task_pulse.py error "$TASK_ID" "登录过期"
```
Push: `message(action="send", message="❌ 【任务名】失败\n错误: 登录过期")`

### Query status
```bash
python3 scripts/task_pulse.py status
```

### Cleanup (>7 days completed)
```bash
python3 scripts/task_pulse.py cleanup
```

## Mandatory Rules

1. **Always push after file update** — file update alone is invisible to users
2. **Push format**: emoji + `[done/total]` + current step + one-line info (≤3 lines)
3. **Push frequency**: every step transition; long steps max once per 30s
4. **Stall = running + no update for 3 minutes** — detected on `status` query
5. **On stall detection**: push `⚠️ 【任务名】可能卡住了（3分钟无更新）`
6. **Cleanup**: run in heartbeat, keep completed tasks 7 days

## Status Icons

| Status | Icon | Meaning |
|--------|------|---------|
| running | 🔄 | Executing |
| done | ✅/🎉 | Completed |
| error | ❌ | Failed |
| stalled | ⚠️ | No update >3min |
| pending | ⏳ | Step not started |

## Integration

- **Cron jobs**: Wrap cron task payload with create/next/done calls
- **Sub-agents**: Parent agent creates task, sub-agent updates via file, parent pushes
- **Heartbeat cleanup**: Add `python3 scripts/task_pulse.py cleanup` to HEARTBEAT.md
- **Multi-channel**: `message` tool auto-routes to the active channel

See [references/integration-guide.md](references/integration-guide.md) for cron and sub-agent patterns.
