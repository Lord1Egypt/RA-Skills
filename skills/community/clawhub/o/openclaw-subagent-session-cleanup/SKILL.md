---
name: openclaw-session-cleanup
description: >
  Clean up accumulated subagent and cron:run child sessions in OpenClaw to fix slow subagent startup.
  Use when: subagents are slow to start, sessions.json is too large, too many child sessions have accumulated,
  session cleanup is needed, or the user mentions "session cleanup", "session compact", "clean sessions", 
  "subagent slow", "sessions.json too large", "child session accumulation", "session too many", 
  "subagent startup slow", "gateway slow".
  
  清理 OpenClaw 积累的 subagent 和 cron:run child sessions，解决 subagent 启动慢的问题。
  当用户提到 subagent 启动慢、session 太多、想清理 sessions、sessions.json 太大、child session 积累时，务必使用此 skill。
---

keywords:
  - session cleanup
  - subagent slow
  - sessions.json too large
  - child session accumulation
  - session compact
  - clean sessions
  - subagent startup slow
  - gateway slow
  - session too many
  - 清理 session
  - subagent 启动慢
  - sessions.json 太大
---

# OpenClaw Session Cleanup

## Background / 背景

Every subagent call and cron job execution leaves an entry in `sessions.json`. After a few days of use, hundreds of entries accumulate, causing the gateway to slow down when starting new subagents.

**Symptom:** Subagent startup goes from a few seconds to 10+ seconds.
**Root cause:** Completed child session entries piling up in `sessions.json`.
**Fix:** Remove subagent and cron:run child session records, keep main and channel sessions.

每次 subagent 调用和 cron job 执行都会在 sessions.json 中留下记录。积累几百条后，gateway 启动 subagent 时明显变慢。

**症状：** subagent 启动时间从几秒变成十几秒甚至更长。
**根因：** sessions.json 中积累了大量已完成的 child session 索引。
**解法：** 删除 subagent 和 cron:run 类型的 child session 记录，保留主 session 和 channel session。

---

## Steps / 操作步骤

### Step 1: Stop Gateway
```powershell
openclaw gateway stop
```

### Step 2: Run cleanup script
```powershell
.\cleanup.ps1             # 清理 sessions.json 索引（默认保留 .jsonl 文件）
.\cleanup.ps1 -DryRun     # 预览模式，不实际修改
.\cleanup.ps1 -KeepJsonl  # 保留 .jsonl history 文件（明确指定，不删）
.\cleanup.ps1 -CleanJsonl # 危险！同时删除 .jsonl 文件（对话历史会丢失）
```

### Step 3: Restart Gateway
```powershell
openclaw gateway
```

---

## What is kept / 保留规则

| Session type | Example key | Action |
|---|---|---|
| Main session | `agent:main:main` | ✅ Keep |
| WhatsApp | `agent:main:whatsapp:direct:+1xxx` | ✅ Keep |
| Telegram | `agent:main:telegram:direct:xxx` | ✅ Keep |
| Signal | `agent:main:signal:direct:+1xxx` | ✅ Keep |
| Google Chat | `agent:main:google chat:direct:xxx` | ✅ Keep |
| Line | `agent:main:line:direct:xxx` | ✅ Keep |
| WeChat | `agent:main:wechat:direct:xxx` | ✅ Keep |
| iMessage / SMS | `agent:main:imessage:direct:xxx` | ✅ Keep |
| BlueBubbles (iOS) | `agent:main:bluebubbles:direct:xxx` | ✅ Keep |
| 其他 channel session | `agent:main:<channel>:...` | ✅ Keep |
| Cron definition | `agent:main:cron:uuid` | ✅ Keep |
| Cron run record | `agent:main:cron:uuid:run:uuid` | ❌ Delete |
| Subagent session | `agent:main:subagent:uuid` | ❌ Delete |
| 其他 child session | `agent:main:<type>:...` | ❌ Delete |

### ⚠️ 关于 .jsonl 文件（对话历史）

**默认不删除 .jsonl 文件。** .jsonl 包含完整的对话历史，删除后无法恢复。
如需清理 .jsonl，必须加 `-CleanJsonl` 参数：
```powershell
.\cleanup.ps1 -CleanJsonl    # 清理 sessions.json 索引 + 删除 .jsonl 文件
```