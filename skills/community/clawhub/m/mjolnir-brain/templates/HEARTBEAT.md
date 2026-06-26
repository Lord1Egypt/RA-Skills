# HEARTBEAT.md - Periodic Checks

> **⚠️ OPT-IN**: The checks in this file only execute automatically if the user has actively enabled cron jobs or heartbeat polling. Nothing here runs by default.

## 🔄 Periodic Checks (executed on each heartbeat poll)

### 1. System Health (Priority: Medium)
- **Frequency**: Every 2 hours
- **Checks**:
  - Service status (is everything running?)
  - Disk space (`df -h`)
  - Memory usage
  - Recent error logs

### 2. Self-check: Unrecorded Learnings (Priority: High)
- **Frequency**: Every heartbeat
- **Actions**: Review current session for:
  - ❌ Command failures not recorded?
  - 🔧 User corrections not documented?
  - 💡 Better approaches not written down?
- **If gaps found**: Record immediately

### 3. Idle Task Queue (Priority: Low)
- **Frequency**: Every heartbeat, only when nothing else needs attention
- **Current queue**:
  - *(add your pending tasks here)*
- **Execution**: Prefer spawning sub-tasks, don't block main session

## 🧠 Memory Maintenance

### Heartbeat Consolidation Flow
1. **Read `memory/memory-state.json`** — check `pendingConsolidation` list
2. **If files pending** — read each daily log
3. **AI summarization** — extract decisions/conclusions/lessons, write to MEMORY.md sections (not raw copy!)
4. **Mark processed** — append `# consolidated: YYYY-MM-DD` to log file
5. **Check MEMORY.md size** — trim old entries if over 20KB

### Consolidation Principles
- **Only conclusions**: "Chose A because X" ✅ | Full discussion ❌
- **Deduplicate**: Don't repeat what's already in MEMORY.md
- **Categorize**: Write to the right section, don't just append to bottom
- **Size-aware**: MEMORY.md ≤ 20KB, check every time

### Auto Maintenance (04:00 cron)
- 🗑️ Clean files < 200B (garbage session headers)
- 📦 Archive daily logs older than 30 days (gzip → memory/archive/)
- 📊 Check MEMORY.md size

## Check Interval
- ≥ 2 hours
