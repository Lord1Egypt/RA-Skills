# Memory Management Skill

This is a complete and practical memory management framework for OpenClaw. It helps your agent consistently "remember key preferences/decisions/important facts" across multiple sessions, using importance scoring, time decay, and daily maintenance to continuously improve retrieval quality and usefulness.

---

## When to Use

- Long-term saving: user core preferences, key decisions, essential rules, recurring lessons
- Short-term retrievable: general tasks and normal conversation context (without infinite accumulation)
- Automatic down-ranking and cleanup over time to prevent memory from getting "dirty"
- Daily automated memory maintenance (for example `08:30`) instead of putting all logic into every conversation

---

## Target Workspace Layout (suggested)

Assume your workspace root is `~/.openclaw/workspace/`:

```text
workspace/
├── MEMORY.md
├── AGENTS.md        # optional agent behavior constraints snippet
├── TOOLS.md         # optional tools / skill index
├── HEARTBEAT.md     # optional heartbeat tasks
└── memory/
    ├── preferences.md
    ├── decisions.md
    ├── projects.md
    ├── contacts.md
    ├── patterns.md
    ├── feedback.md
    └── YYYY-MM-DD.md
```

---

## Importance Scoring (1-5) before writing

- `5`: write to `MEMORY.md` (core principles / key decisions / user's core preferences)
- `4`: write to `MEMORY.md` (important rules / lessons repeated multiple times)
- `3`: write to `memory/YYYY-MM-DD.md` (general tasks / normal conversation content worth retrieving)
- `2`: write to `memory/YYYY-MM-DD.md` (temporary info / optional record)
- `1`: do not record (small talk / meaningless content)

---

## Time Decay & Cleanup (30+ days)

- Today: retrieval weight 1.0
- 1-7 days: retrieval weight 0.8
- 8-30 days: retrieval weight 0.5
- 30+ days: expired (weight 0; recommended to delete or archive)

Daily maintenance recommended workflow (core idea):
1. Create/check today's `memory/YYYY-MM-DD.md`
2. Review yesterday's log; extract content worth long-termizing into `MEMORY.md` or topic files
3. Clean logs older than 30 days (migrate valuable content before deleting)
4. Generate a maintenance report (optional: output to chat / Lark)

---

## Manual Triggers (immediate write)

When the user says the following phrases, immediately start "write evaluation" and persist:

- `remember this` / `save this`: evaluate importance then write to the corresponding place
- `don't forget` / `permanently save`: write directly to `MEMORY.md`
- `this is an important point`: write directly to `MEMORY.md`
- `write to memory`: write to the corresponding topic file based on content type
  - preferences -> `memory/preferences.md`
  - decisions -> `memory/decisions.md`
  - projects -> `memory/projects.md`
  - contacts -> `memory/contacts.md`
  - patterns / best practices -> `memory/patterns.md`
  - feedback -> `memory/feedback.md`

---

## Auto Recall (retrieve then answer)

When the user asks about categories such as previous work/decisions/dates/people/preferences/tasks, run memory retrieval first and then answer:

- `memory_search`: hybrid retrieval (vector semantics + keywords)
- If retrieval is insufficient: do not fabricate; tell the user you checked but could not find enough relevant information

---

## Daily Maintenance (cron template)

In cron, schedule daily maintenance at `08:30` (example logic: create today's file -> review yesterday -> update `MEMORY`/topic files -> optional config backup -> clean old logs -> output report).
For the concrete cron payload, see the directory's `SKILL.md`.

---

## Related Skills

- `memory-setup`: configure persistent memorySearch (vector retrieval foundation)
- `self-improvement`: turn errors/corrections into learnable experiences
- `cron-mastery`: cron vs heartbeat time scheduling best practices

