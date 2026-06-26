---
name: midos-self-improver
description: Structured learning pipeline with quality-gated promotion. Captures corrections, errors, and patterns — promotes only what proves itself through recurrence.
version: 1.0.0
---

# midos-self-improver

An agent learning system that captures what goes wrong, what gets corrected, and what works — then promotes the best learnings into permanent project memory. With quality gates that prevent noise from polluting your knowledge base.

Most self-improving agents dump everything into a flat file. Over time, that file becomes a graveyard of one-off notes that never get cleaned up. midos-self-improver solves this with a **capture → quality gate → staging → scoring → promotion** pipeline where every learning must prove its value through recurrence before it becomes permanent.

## Architecture

```
Agent Session
    ↓
[Detectors] — 5 trigger types
    ↓
.learnings/entries/{category}/{timestamp}.json
    ↓
[Quality Gate] — dedup + decision check
    ↓
.patterns/{domain}_pattern.md (staging)
    ↓
[4-Axis Scorer] — recurrence, freshness, specificity, impact
    ↓
.knowledge/ (permanent) ← only if score >= 0.7
    ↓
CLAUDE.md / AGENTS.md (promoted rules)
```

## The 5 Detection Triggers

| Trigger | What It Captures | Example |
|---------|-----------------|---------|
| **Correction** | User corrects agent behavior | "Don't use git add ., use specific files" |
| **Error** | Tool call fails or returns unexpected result | ImportError, test failure, API timeout |
| **Knowledge Gap** | Agent didn't know something it should have | "The config file moved to /new/path" |
| **Best Practice** | Successful pattern worth repeating | "Running preflight before publish prevented 3 issues" |
| **Pattern** | Recurring code structure or workflow | "Every MCP tool needs tier guard + handler separation" |

### Detection hooks

```bash
# Correction detector — fires on UserPromptSubmit when correction language detected
# Patterns: "no, do X instead", "that's wrong", "actually", "I said", "don't do that"

# Error detector — fires on PostToolUse when tool returns error
# Captures: exit code != 0, exception traces, "Error:" in output

# Gap detector — fires when agent says "I don't know" or searches >3 times for same thing

# Pattern detector — fires on PostToolUse Write|Edit
# Analyzes: what decisions were made, what trade-offs considered
```

## Quality Gate (Deterministic)

Before any learning enters the staging area, it passes through a quality gate:

### Deduplication

```
1. SHA-256 hash of normalized content (lowercase, strip whitespace)
2. Compare against all entries in last 30 days
3. If hash exists → increment recurrence counter, skip creation
4. If similar (>85% trigram overlap) → merge into existing entry
```

### Decision Check

```
Rules (no LLM required):
  1. >= 2 decisions extracted from patterns → PASS
  2. >= 3 files across >= 2 domains → PASS (cross-cutting)
  3. Only docstrings, no decisions → FAIL (log, not pattern)
  4. All files in same trivial edit → FAIL (maintenance, not learning)
```

Only entries that pass both checks advance to the staging area.

## 4-Axis Scoring

Every staged learning gets scored on 4 axes:

| Axis | Weight | What It Measures |
|------|--------|-----------------|
| **Recurrence** | 0.35 | How many times this same issue/pattern appeared |
| **Freshness** | 0.25 | How recent (exponential decay, half-life 14 days) |
| **Specificity** | 0.20 | Concrete file paths/functions vs vague advice |
| **Impact** | 0.20 | Breadth of effect (multi-domain > single file) |

### Scoring formulas

```
recurrence_score = min(count / 5, 1.0)  # saturates at 5 occurrences
freshness_score = exp(-0.693 * days_since / 14)  # half-life 14 days
specificity_score = (has_path * 0.4) + (has_function * 0.3) + (has_example * 0.3)
impact_score = min(n_domains / 3, 1.0) * 0.6 + min(n_files / 5, 1.0) * 0.4

composite = (recurrence * 0.35) + (freshness * 0.25) +
            (specificity * 0.20) + (impact * 0.20)
```

### Promotion thresholds

```
composite >= 0.7  → PROMOTE to permanent knowledge base
composite < 0.3   → PRUNE (archive and stop tracking)
0.3 <= c < 0.7    → KEEP in staging (let it mature with more data)
```

## Quick Start

### Standalone Mode (zero dependencies)

Add to your CLAUDE.md or agent instructions:

```markdown
## Self-Improvement Protocol

### On Corrections
When the user corrects you:
1. Log the correction to `.learnings/corrections/{date}.md`
2. Include: what you did wrong, what the correct behavior is, which file/function
3. If this is the 3rd+ time for the same correction → promote to CLAUDE.md rules

### On Errors
When a tool call fails:
1. Log to `.learnings/errors/{date}.md`
2. Include: command, error message, root cause, fix applied
3. If same error type appears 3+ times → create a prevention rule

### On Patterns
When you notice a recurring approach that works:
1. Log to `.learnings/patterns/{domain}/{date}.md`
2. Include: what decision, why this over alternatives, evidence it works
3. Pattern must have >= 2 concrete decisions to be logged (not just descriptions)

### Promotion Rules
- Recurrence >= 3 AND composite score >= 0.6 → promote to permanent memory
- Never promote without evidence of repeated value
- Deduplicate: check SHA-256 before writing new entries
- Archive entries older than 30 days with score < 0.3
```

### With the capture hooks

```python
# Correction capture (wired to UserPromptSubmit)
from hooks.learning_capture import capture_correction
capture_correction(
    user_message="no, always use specific files in git add",
    agent_response="I'll use git add file1 file2 instead of git add .",
    context={"file": "CLAUDE.md", "function": "commit_protocol"}
)

# Error capture (wired to PostToolUse)
from hooks.learning_capture import capture_error
capture_error(
    tool="Bash",
    command="python -m pytest tests/",
    error="ImportError: cannot import name 'AuthMiddleware'",
    fix="Changed to absolute import: from modules.community_mcp.auth import AuthMiddleware"
)

# Assess all staged patterns
from hooks.pattern_harvester import assess_pattern_value
results = assess_pattern_value()
# Returns: [{"file": "...", "score": 0.82, "action": "PROMOTE"}, ...]
```

### Triggering promotion

```bash
# Run assessment on all staged patterns
python -c "from hooks.pattern_harvester import assess_pattern_value; assess_pattern_value()"

# Check what's in staging
ls docs/patterns/

# Check what was promoted
ls .knowledge/ | grep pattern

# Check what was discarded
cat knowledge/_discarded/LOG.md
```

## Usage Patterns

### Pattern 1: Correction Loop

```
User: "Don't read entire files, use grep first"
  ↓
Detector: correction language detected ("don't", imperative)
  ↓
Entry: .learnings/corrections/2026-03-04T10:23:45.json
  {
    "type": "correction",
    "wrong": "Read entire file with cat/Read",
    "right": "Grep for pattern first, then Read with offset",
    "context": {"domain": "efficiency"},
    "recurrence": 1
  }
  ↓
(Same correction appears 2 more times over 3 days)
  ↓
recurrence_score: 0.6 (3/5)
freshness_score: 0.95 (recent)
specificity_score: 0.7 (has concrete tool names)
impact_score: 0.8 (affects all file operations)
composite: 0.76 → PROMOTE
  ↓
.knowledge/efficiency_grep_before_read_pattern_20260307.md
  ↓
Added to CLAUDE.md: "Grep > Read — Never read full files, use offset/limit"
```

### Pattern 2: Error Prevention

```
Error: ImportError on absolute vs relative import (3rd occurrence)
  ↓
Entry already exists with recurrence=3
  ↓
Assessment: composite 0.72 → PROMOTE
  ↓
Generated rule: "Always use absolute imports in package directories"
  ↓
Promoted to project-level AGENTS.md
```

### Pattern 3: Noise Rejection

```
Agent writes docstrings to 2 files in same module
  ↓
Quality gate: "no decisions found — only docstrings (log, not pattern)"
  ↓
REJECTED — never enters staging
```

## How It Compares

| Feature | midos-self-improver | self-improving-agent (101K) | proactive-agent (54K) |
|---------|--------------------|-----------------------------|----------------------|
| Promotion tiers | 4 (entry → staging → chunks → rules) | 2 (.learnings → CLAUDE.md) | 1 (WAL → manual) |
| Quality gate | Deterministic (dedup + decision check) | None | None |
| Deduplication | SHA-256 + trigram similarity | None | None |
| Scoring | 4-axis composite (recurrence, freshness, specificity, impact) | Manual review | VFM scoring (manual) |
| Promotion trigger | Automatic at threshold | Manual (activator.sh) | Manual |
| Noise rejection | Yes (quality gate rejects non-decisions) | No (logs everything) | No |
| Categories | 5 types with domain tagging | 3 files (LEARNINGS, ERRORS, FEATURES) | 1 file (WAL) |
| Maturation | Staging area with aging | None | None |
| Archival | Auto-prune at score < 0.3 | None | None |
| Hook integration | PostToolUse + UserPromptSubmit | PostToolUse + UserPromptSubmit | Manual |
| Works without LLM | Yes (all deterministic) | Yes | Yes |

## Entry Format

```json
{
  "id": "sha256-first-8-chars",
  "type": "correction|error|knowledge_gap|best_practice|pattern",
  "timestamp": "2026-03-04T10:23:45Z",
  "content": "Always use absolute imports in packages",
  "context": {
    "domain": "imports",
    "files": ["src/auth/server.py"],
    "functions": ["import_auth"],
    "trigger": "ImportError in CI"
  },
  "recurrence": 3,
  "hash": "a1b2c3d4",
  "scores": {
    "recurrence": 0.6,
    "freshness": 0.95,
    "specificity": 0.7,
    "impact": 0.4,
    "composite": 0.66
  },
  "status": "staging|promoted|pruned",
  "promoted_to": null
}
```

## MidOS-Connected Mode

When running inside the MidOS ecosystem, the self-improver gains:

- **GEPA coherence scoring** validates promoted chunks against the knowledge base
- **L2R reranker** helps find truly similar existing patterns (prevents subtle duplicates)
- **Vector dedup** via LanceDB cosine similarity (catches semantic duplicates, not just textual)
- **Auto-promotion pipeline** with MC-2 deliverable gates (frontmatter, length, coherence)
- **Pattern harvester hook** wired to every Write|Edit operation
- **Scheduled assessment** via `your cron/scheduler system` (runs every 2 hours)
- **MCP tools**: `learning_log`, `learning_search`, `learning_stats` exposed via MCP server

The standalone mode handles 80% of learning scenarios. The ecosystem adds deeper dedup, quality scoring, and integration with the 6-layer knowledge pipeline.

---

Built with [MidOS](https://midos.dev) — MCP Community Library.
This is 1 of 200+ skills in the MidOS ecosystem.

Free MCP access: [midos.dev/dev](https://midos.dev/dev) (500 queries/mo)
Full ecosystem: [midos.dev/pro](https://midos.dev/pro) ($20/mo)
