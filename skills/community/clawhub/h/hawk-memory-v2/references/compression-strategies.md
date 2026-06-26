# Compression Strategies

---

## 5 Strategies

| Strategy | Command | Best For | Effect |
|-----------|---------|----------|--------|
| `summarize` | `/hawk compress summarize` | Long process, clear conclusion | 500 lines → 30 |
| `extract` | `/hawk compress extract` | Facts/decisions/lists | Keep core facts |
| `delete` | `/hawk compress delete` | Temp/debug/outdated | Full delete |
| `promote` | `/hawk compress promote` | learnings | Aggregate to topic file |
| `archive` | `/hawk compress archive` | >30 days | Move to archive layer |

---

## Pre-Compression Confirmation

All compress operations require confirmation:

```
[Context-Hawk] Confirm compression
  Target: today.md (186 lines)
  Strategy: summarize (summarize)

  [1] Compress all
  [2] Compress part only (enter line range or keyword)
  [3] Cancel
```

### Partial Compression

```
[Context-Hawk] Partial compression

  today.md — 186 lines total. Preview:

  [1-30]   User question about Skill architecture
  [31-80]   Multi-turn discussion (verbose)
  [81-120]  Final decision
  [121-186] Additional details

  Enter line range to compress (e.g., 5-50)
  Or enter keyword to locate specific content:
```

---

## Smart Strategy Recommendation

Before compression, AI analyzes and recommends:

```markdown
[Context-Hawk] Strategy recommendation

  File: today.md (186 lines)

  Content analysis:
  ┌────────────────────────────────────────────────────────┐
  │ 30% discussion process   → summarize (save ~50 lines)  │
  │ 25% specific code      → extract (keep core snippets)  │
  │ 20% decision records   → promote (aggregate to week)  │
  │ 15% debug logs        → delete (fully remove)        │
  │ 10% important facts    → keep                          │
  └────────────────────────────────────────────────────────┘

  Recommended combination: summarize + delete + promote

  Estimated: 186 lines → 45 lines (76% reduction)

  [1] Execute recommended
  [2] Manual selection
  [3] Cancel
```

---

## Strategy 1: Summarize

Keep conclusions, remove process.

```markdown
## 2026-03-28 Skill Architecture Discussion

### Process (before — 60 lines)
Discussed whether to split the skill...
First conclusion: no split, because...
User said...
Discussed again...
Final decision: no split

### Conclusion (after — 8 lines)
- Decision: do not split skill; e-commerce as biz/examples/
- Reason: generic framework + business examples is the right direction
```

---

## Strategy 2: Extract

Extract key facts from large content.

```markdown
## Team Rules (extracted)

### Core Facts
| Agent | Role | Core Responsibility |
|-------|------|---------------------|
| Architect | Architect | Technical specs, rule enforcement |
| Backend | Backend | Logic/Dao/Model |
| Frontend | Frontend | Filament/Blade |
| Tester | Tester | Test cases, coverage ≥98% |

### Key Rules (4 total)
1. Four-layer architecture — no cross-layer calls
2. DTO+Enum mandatory
3. Coverage ≥98%
4. APIs must be versioned
```

---

## Strategy 3: Delete

Dangerous — requires double confirmation:

```
[Context-Hawk] ⚠️ Destructive operation
  Will delete:
  - today.md lines 15-28 (debug logs)

  This is irreversible.

  [1] Confirm delete
  [2] Only delete lines where N is odd
  [3] Cancel
```

---

## Strategy 4: Promote

Aggregate scattered learnings to topic files:

```markdown
[Context-Hawk] Promote suggestion

  Found these scattered learnings:

  today.md:42   → "user prefers concise replies" → user-preferences.md
  today.md:78   → "coverage must be 98%" → team-rules.md
  week.md:15   → "skill must be reusable" → tech-patterns.md

  [1] Promote all
  [2] Selective promotion
  [3] Cancel
```

---

## Strategy 5: Archive

Move content older than 30 days to archive (not deleted):

```markdown
[Context-Hawk] Archive suggestion

  The following is >30 days old — archive:

  - memory/month.md content from 2026-02
  - memory/week.md weeks 1-2

  Will move to: memory/archive/2026-02/

  [1] Archive all
  [2] Selective archive
  [3] Cancel
```

---

## Batch Compression

```bash
hawk compress all summarize      # Summarize all layers
hawk compress --dry-run          # Preview without executing
hawk compress today delete "debug"  # Delete lines containing "debug"
```

---

## Compression ↔ Memory Tier Interaction

After compression, LanceDB decay scores update:

| Strategy | Effect on decay_score |
|----------|----------------------|
| summarize (keep core) | × 1.0 |
| extract (keep facts) | × 1.0 |
| promote | Recalculate importance |
| delete | decay_score → 0, trigger cleanup |
| archive | Move to archive table |
