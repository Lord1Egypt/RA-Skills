# CLI Reference

---

## Installation

```bash
chmod +x scripts/hawk
ln -s scripts/hawk /usr/local/bin/hawk
```

---

## Command Overview

```
hawk <command> [options]

Task management:
  hawk task ["description"]    Create/view task
  hawk task --start            Start/resume task
  hawk task --step N done     Mark step N complete
  hawk task --next "action"   Add next action
  hawk task --output "file"   Record output
  hawk task --block "reason"  Record blocker
  hawk task --done             Complete task
  hawk task --list            List all tasks
  hawk resume                 Resume last task ← CORE!

Memory management:
  hawk init                   Initialize (LanceDB optional)
  hawk status [--json]        View context usage
  hawk compress [target] [strategy]  Compress memory
  hawk strategy [A|B|C|D|E]   Switch injection strategy
  hawk introspect [--deep]    Self-introspection report
  hawk search <query>         Hybrid search
  hawk inject                 Manual context injection

Auto-trigger:
  hawk check                  Run auto-check now (every 10 rounds)
  hawk check --rounds 5       Check after 5 rounds

LanceDB management:
  hawk extract [--force]       Trigger memory extraction
  hawk recall <query>         Test recall
  hawk backup                 Backup LanceDB
  hawk export [--json]        Export memories

Alerts:
  hawk alert on|off|set <n>   Toggle/configure alerts
```

---

## hawk task

```bash
hawk task "Complete the API documentation"  # Create task
hawk task                               # View current task
hawk task --start                      # Start/resume task
hawk task --step 1 done             # Mark step 1 done
hawk task --next "Write README"       # Add next action
hawk task --output "SKILL.md"         # Record output
hawk task --block "Missing token"     # Record blocker
hawk task --done                      # Complete task
hawk task --abort                      # Abandon task
hawk task --list                      # List all tasks
```

### Task Output

```
[Context-Hawk] Current task

  ID:       task_20260329_001
  Desc:     Complete the API documentation
  Progress: 65% (3/5 steps)
  Status:   🔄 in_progress
  Created:   2026-03-29 00:00

  Completed:
    ✅ 1. SKILL.md completed
    ✅ 2. constitution.md completed
    ✅ 3. architect.md completed

  Current:
    🔄 4. Review architecture template

  Pending:
    ⬜ 5. Report to user

  Constraints:
    - Coverage must reach 98%
    - APIs must be versioned

  Outputs:
    - SKILL.md
    - constitution.md
    - architect.md
```

---

## hawk resume

```
$ hawk resume

[Context-Hawk] Task Resume

  Task:    Complete the API documentation
  Progress: 65% (3/5 steps complete)
  Status:   🔄 in_progress

  Completed:
    ✅ 1. SKILL.md completed
    ✅ 2. constitution.md completed

  Current:
    🔄 3. Review architecture template

  Next:
    ⬜ 4. Report to user

  [Press Enter to continue step 3]
```

---

## hawk status

```
[Context-Hawk] Context Status

  Today:    today.md    12 lines
  Week:     week.md     34 lines
  Month:    month.md    8 lines
  Total:    54 lines (estimated ~12% context)

  LanceDB Memory Layers:
  ┌────────────────────────────────────┐
  │ Working Memory   23 memories  ~8%     │
  │ Short-term     156 memories ~21%     │
  │ Long-term       89 memories ~12%     │
  │ Archive        412 memories —      │
  └────────────────────────────────────┘

  Current task: ✅ task_20260329_001 (65% done)
  Active strategy: B (task-related)
  Status: ✅ Normal
  Alert: 🔔 Enabled (threshold: 60%)
  Auto-check: every 10 rounds (3 rounds since last check)
```

---

## hawk compress

```bash
hawk compress today summarize           # Summarize today.md
hawk compress week extract             # Extract week.md
hawk compress all promote --dry-run   # Preview promote all
hawk compress month archive           # Archive month.md
hawk compress today delete "debug"    # Delete debug lines
```

---

## hawk strategy

```bash
hawk strategy          # View current strategy
hawk strategy A        # High-importance (importance ≥ 0.7)
hawk strategy B        # Task-related (default)
hawk strategy C        # Recent conversation (last 10 turns)
hawk strategy D        # Top5 recall (access_count top 5)
hawk strategy E        # Full recall (no filter)
```

---

## hawk introspect

```
[Context-Hawk] Introspection

  1. Task Clarity: ✅ Clear
     Current: task_20260329_001 (65% done)

  2. Info Completeness: ✅ Complete
     Requirements: ✅ clear
     Tech spec: ✅ available

  3. Context Usage: ✅ Healthy
     Current: 41% / Threshold: 80%

  4. Loop Detection: ✅ No loops

  5. Memory Recall: 💡 2 relevant available
     - User communication preferences (importance: 0.9)
     - Four Agent responsibilities (importance: 0.85)
```

---

## hawk backup

```
[hawk] Backup complete
  Path: ~/.openclaw/memory-lancedb-backup-20260329.tar.gz
  Size: 2.3MB
  Contents: working.lance + shortterm.lance + longterm.lance + archive.lance
  Task state: ✅ included (task_state.jsonl)
```
