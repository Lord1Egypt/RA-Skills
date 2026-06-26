---
name: icecube-heartbeat
description: "🧊 IceCube Heartbeat — Proactive agent maintenance during idle periods. Self-check, memory governance, improvement detection, and evolution triggers. Keeps your agent alive and improving without manual intervention."
metadata:
  openclaw:
    requires: {}
---

# 🧊 IceCube Heartbeat

**The pulse that keeps your agent alive.**

When your agent receives periodic "heartbeat" polls, don't just reply "HEARTBEAT_OK". Use that time to maintain, improve, and evolve.

## Why IceCube Heartbeat?

**Problem:** Most agents sit idle between user requests. No learning. No improvement. No self-maintenance.

**Solution:** Heartbeat turns idle time into productive evolution cycles.

**Result:** An agent that gets better every day, without you doing anything.

## What Heartbeat Does

### 1. System Health Check
- Scan `unclosed_work.yaml` for pending tasks
- Check cron job status (recent failures?)
- Verify agent sessions are healthy
- Alert if anything needs attention

### 2. Memory Governance
- Scan `mistake_log.md` for new errors
- Scan `success_patterns.md` for new wins
- Evaluate if memory consolidation needed
- Promote important daily entries to MEMORY.md

### 3. Self-Improvement Detection
- Repeated fallback patterns → flag for optimization
- Repeated rollback patterns → flag for root cause analysis
- Task stagnation (>24h no progress) → alert
- User repeated corrections → update rules

### 4. Evolution Triggers
- Weekly: Check ClawHub for new relevant skills
- Weekly: Assess pending API configs can be activated
- Daily: Generate brief status report

### 5. Proactive Outreach (Optional)
- Important email arrived → notify
- Calendar event soon (<2h) → remind
- Weather relevant → mention if user might go out

## Setup

### 1. Create HEARTBEAT.md

```markdown
# HEARTBEAT.md

## 自检任务（每次 heartbeat 执行）

### 1. 系统健康检查
- [ ] 检查 unclosed_work.yaml 中的待办事项
- [ ] 检查 cron 任务状态
- [ ] 检查 agent sessions 是否有异常

### 2. 记忆治理
- [ ] 扫描 mistake_log 是否有新错误
- [ ] 扫描 success_patterns 是否有新模式
- [ ] 评估是否需要 memory consolidation

### 3. 自我改进触发条件检测
- [ ] 是否有 repeated fallback
- [ ] 是否有 repeated rollback
- [ ] 是否有 task stagnation
- [ ] 是否有用户重复纠正

### 4. 技能扩展检查（每周一次）
- [ ] ClawHub 是否有新技能适合当前需求
- [ ] pending API 配置技能是否可以激活
```

### 2. Configure Heartbeat Interval

In OpenClaw config:
```json
{
  "agents": {
    "heartbeat": {
      "intervalMs": 1800000,  // 30 minutes
      "prompt": "Read HEARTBEAT.md. Follow it strictly. Reply HEARTBEAT_OK if nothing needs attention."
    }
  }
}
```

### 3. Create Supporting Files

**mistake_log.md:**
```markdown
# Mistake Log

## Format
- Date: YYYY-MM-DD HH:MM
- Mistake: Description
- Impact: What went wrong
- Fix: How to prevent recurrence
```

**success_patterns.md:**
```markdown
# Success Patterns

## Format
- Date: YYYY-MM-DD HH:MM
- Pattern: Description
- Result: What worked well
- Applicability: When to use this pattern
```

## Heartbeat Response Rules

### When to Reply HEARTBEAT_OK
- Late night (23:00-08:00) unless urgent
- Nothing new since last check
- Checked <30 minutes ago
- User clearly busy

### When to Reach Out
- Important email arrived
- Calendar event in <2h
- Something interesting found
- >8h since last contact

### When to Stay Silent
- Routine checks with no findings
- User hasn't responded to previous proactive messages
- Late night quiet hours

## Example Heartbeat Cycle

**08:00 Morning heartbeat:**
```
1. Check unclosed_work.yaml → 3 pending items
2. Check mistake_log → 1 new entry (fallback loop)
3. Check calendar → meeting at 10:00
4. Action: Remind user about meeting, flag fallback issue for investigation
5. Reply: "Meeting at 10:00. Found a fallback pattern to fix later."
```

**14:00 Afternoon heartbeat:**
```
1. Check unclosed_work → same 3 items, no progress on TASK-A
2. Flag: task stagnation >24h
3. Check ClawHub → new skill matching current project
4. Reply: "TASK-A stalled >24h. New skill available for [project]."
```

**23:00 Evening heartbeat:**
```
1. All checks pass
2. Late night → stay quiet
3. Reply: HEARTBEAT_OK
```

## Anti-Patterns

❌ **Don't:**
- Reply HEARTBEAT_OK when there's unfinished work
- Ignore stale tasks
- Skip memory governance
- Never promote learnings to long-term memory

✅ **Do:**
- Check before you OK
- Act on findings immediately
- Keep heartbeat-state.json for tracking
- Batch checks to reduce API calls

## Proactive Work Without Asking

These are safe to do during heartbeat:

- Read and organize memory files
- Check on projects (git status)
- Update documentation
- Commit and push your own changes
- Review and update MEMORY.md
- Install new skills from ClawHub
- Run self-improvement routines

## Integration with Other IceCube Skills

**icecube-memory:** Heartbeat triggers memory distillation weekly
**icecube-ops:** Heartbeat checks system health status
**icecube-evolution:** Heartbeat drives continuous improvement loops

## Tracking State

**heartbeat-state.json:**
```json
{
  "lastChecks": {
    "email": 1703275200,
    "calendar": 1703260800,
    "weather": null,
    "clawhub": 1703260800
  },
  "lastPromotion": "2026-03-17",
  "heartbeatCount": 42
}
```

## License

MIT — Use freely.

---

*Idle time is evolution time.*