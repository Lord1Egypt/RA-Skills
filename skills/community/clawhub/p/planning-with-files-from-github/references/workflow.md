# Workflow Reference

## Why This Pattern Works

The Manus AI architecture (acquired by Meta for $2B) used filesystem-based planning as its core context engineering technique. The insight:

> "Context window = RAM (volatile, limited). Filesystem = Disk (persistent, unlimited). Anything important gets written to disk."

In long agentic tasks, the original goal drifts out of context as tool calls accumulate. Re-reading `task_plan.md` before major decisions is **attention manipulation** — it forces the goal back into the active context window.

## Full Workflow Diagram

```
USER REQUEST
    │
    ▼
┌───────────────────────────────┐
│  init-session.sh              │  Creates task_plan.md
│  (or manual file creation)    │         findings.md
└───────────┬───────────────────┘         progress.md
            │
            ▼
┌───────────────────────────────┐
│  Fill task_plan.md            │  Goal + Phases defined
└───────────┬───────────────────┘
            │
            ▼
    ╔═══════════════════╗
    ║   WORK LOOP       ║
    ║                   ║
    ║  Re-read plan     ║ ← before every major decision
    ║       ↓           ║
    ║  Do work          ║
    ║       ↓           ║
    ║  After 2 ops →    ║ ← update findings.md (2-Action Rule)
    ║  update findings  ║
    ║       ↓           ║
    ║  Phase done? →    ║ ← update task_plan.md + progress.md
    ║  update plan      ║
    ╚═══════╤═══════════╝
            │ all phases complete?
            ▼
┌───────────────────────────────┐
│  check-complete.sh            │  Verifies task_plan.md
└───────────┬───────────────────┘
            │ all [x]
            ▼
        DELIVER RESULT
```

## OpenClaw vs Claude Code: Key Differences

| Feature | Claude Code | OpenClaw |
|---------|-------------|----------|
| Hook system | PreToolUse / PostToolUse / Stop hooks | No native hooks — encoded in SKILL.md instructions |
| Script execution | Plugin hook scripts | `exec` tool calls |
| Session recovery | Built-in `/clear` recovery | Manual: re-read 3 files |
| Slash commands | `/planning-with-files:plan` | `/planning-with-files` (user-invocable) |
| File discovery | CLAUDE_PLUGIN_ROOT | `{baseDir}` in SKILL.md |

## The 2-Action Rule

After every **2** view / search / fetch / browser operations, immediately write key findings to `findings.md`. This prevents visual/multimodal context from being compressed away.

```
Op 1: web_search "X" → note results mentally
Op 2: web_fetch URL  → MUST update findings.md NOW
Op 3: read file      → note results mentally
Op 4: grep search    → MUST update findings.md NOW
```

## Context Engineering Principles (from Manus)

1. **Filesystem as memory** — Store in files, not context
2. **Attention manipulation** — Re-read plan before decisions; recent context gets more "attention"
3. **Error persistence** — Log failures in plan file; prevent repetition
4. **Goal tracking** — Checkboxes show progress at a glance
5. **Completion verification** — Check all phases before stopping
6. **KV-cache efficiency** — Stable file prefixes → better cache hit rates
