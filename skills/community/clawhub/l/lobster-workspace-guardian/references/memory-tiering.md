# Memory Tiering

## Three Temperature Layers

### 🔥 HOT (< 3 days)
- Retained in `memory/` root
- Recent context, active projects
- Priority reading for new sessions

### 🌡️ WARM (3–14 days)
- Retained in `memory/` root
- Recent enough for reference
- Marked `[WARM]` in notes

### ❄️ COLD (> 14 days)
- Moved to `memory/archive/` when MEMORY.md update is needed
- `memory/archive/YYYY-MM-DD_original-name.md`
- Accessible but not loaded by default

---

## Memory File Hierarchy

```
memory/                          ← L4 raw logs (HOT/WARM)
├── YYYY-MM-DD.md               ← daily record
├── YYYY-MM-DD-HHMM.md          ← milestone record
├── archive/                    ← L2 archived (COLD)
├── core/                       ← L0 identity/decisions/active_task (always HOT)
├── agents/                     ← L1 sub-agent memories (loaded on demand)
├── dreaming/                   ← session corpus (L0, not archived)
└── .dreams/                    ← dream corpus
```

### Exempt from Archival
- `memory/core/` — L0 core
- `memory/agents/` — L1 sub-agent
- `memory/dreaming/` — L0 dreams
- `memory/.dreams/` — session corpus

These subdirectories stay in `memory/` regardless of age.

---

## MEMORY.md (L3) Management

### Size Limit: 30KB

When approaching 30KB:
1. Identify oldest/least relevant entries
2. Move them to `memory/archive/` with timestamp
3. Preserve full context — archive is NOT deletion
4. L4 daily logs are NEVER deleted

### Entry Format (Decision Router Pattern)

```
Scenario → Insight → Action
```

Ask: "Did this entry ever change a decision?" If not, consider archiving.

---

## Dual-Write Rule (Learning Log + Memory)

When recording important lessons or corrections:
1. Write to `.learnings/LEARNINGS.md` (correction/insight/best_practice)
2. Write one line to `memory/YYYY-MM-DD.md` (raw record)

---

## Promotion Path

Proven practices may be promoted:
- Behavior patterns → `SOUL.md`
- Workflow improvements → `AGENTS.md`
- Tool pitfalls → `TOOLS.md`
- Project conventions → `projects/NNNN_name/SPEC.md`
