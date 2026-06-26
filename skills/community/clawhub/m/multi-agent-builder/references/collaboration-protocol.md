# Collaboration Protocol

## 1) Delegation envelope
Every delegation must include:
- Objective
- Context / inputs
- Expected deliverable format
- Deadline or SLA
- Escalation contact

## 2) Status machine
Allowed statuses:
- `accepted`: task received and understood
- `blocked`: cannot proceed (missing dependency/risk)
- `done`: deliverable completed

## 3) Return-path rule
When a subtask is complete, the assignee must return result to delegator explicitly (not only group broadcast).

## 4) Long task behavior
- If ETA > short response window, publish progress heartbeat at agreed cadence.
- Keep updates concise: progress, risks, next ETA.

## 5) Timeout and escalation
- If no status within SLA, delegator retries once with context snapshot.
- If still no response, escalate to owner/lead.

## 6) User-visible reporting
Report key milestones only:
- task accepted
- stage started (who is doing what)
- meaningful blocker
- stage completed (deliverable path)
- final completion
Avoid noisy micro-updates.

### Progress display format (recommended)
- `[阶段] 负责人: <角色名>`
- `正在处理: <任务简述>`
- `交付位置: <shared路径>`
- `状态: accepted/blocked/done`

## 7) No raw bulk output in chat
- No role may dump large raw artifacts (full source code, long JSON, full logs) into chat.
- Chat should contain concise summary + delivery path/filename only.
- Deliverables must be written to shared workspace and referenced by path.

## 8) Team leader execution boundary
- `team-leader` must not perform specialist implementation work.
- `team-leader` only orchestrates, tracks, and communicates with user.
