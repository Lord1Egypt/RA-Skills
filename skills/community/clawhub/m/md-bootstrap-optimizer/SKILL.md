# SKILL.md — Bootstrap Optimizer

> Version: 2.0 | Updated: 2026-05-22
> Skill Name: md-bootstrap-optimizer
> Tags: bootstrap, memory-management, openclaw, file-architecture, lean-context
> Install: `npx clawhub@latest install md-bootstrap-optimizer`

---

## What This Is

A design guide and audit tool for keeping OpenClaw's bootstrap file system lean and maintainable as it grows. Prevents rules from scattering, keeps context usage low, and makes every file's purpose clear.

**Core problem it solves**: As OpenClaw agents accumulate rules, MEMORY.md and TOOLS.md bloat, critical rules get truncated, and context is wasted on rules that aren't relevant to the current session.

---

## The Three-Layer Architecture

Every file in the bootstrap layer belongs to exactly one of three layers:

| Layer | When Loaded | Rules |
|-------|-------------|-------|
| **Core (Permanent)** | Every session, full load | Atomic principles only — things that are always true |
| **Execution (On-demand)** | Triggered by scene or task type | Detailed procedures for specific situations |
| **Archive** | Never auto-loaded | Historical, reference-only — no rule participation |

---

### Layer 1: Core — Always in Context

Files here load on every session start. **Keep them small and permanent.**

```
MEMORY.md        — Atomic rules (Why), not facts (What)
AGENTS.md        — Core operating procedures
CLAUDE.md / SOUL.md / IDENTITY.md — Identity anchors
```

**Atomic rules only**: Store principles that never expire, not event logs or temporary facts.

**Good**: "When the user says 'confirm', check if decisions.md needs updating before acting"
**Bad**: "The user owns 1 million in assets" (fact, not rule)

---

### Layer 2: Execution — Loaded on Demand

Files here load only when their trigger fires. **Keep them comprehensive.**

```
SCHEDULING.md     — Loaded when scheduling tasks
INSTRUCTIONS.md   — Loaded when handling instructions
TOOLS.md          — Mother file (index only), children loaded on demand
PROJECT.md        — Loaded for specific projects
```

**Mother-Child split for TOOLS.md**: The mother file is an index (< 3KB). Child files contain the details. The child loads only when called.

```
TOOLS.md (mother, index only)
├── TOOLS_skills.md      — Detailed skill inventory
├── TOOLS_feishu.md      — Channel/protocol details
└── TOOLS_custom.md      — Your custom tool docs
```

---

### Layer 3: Archive — Reference Only

These files exist on disk but **never participate in bootstrap**. Use them for historical context, but don't count on them for current behavior.

```
AGENTS_full.md    — Full ruleset (verbose version)
DREAMS.md         — Past session insights
HEARTBEAT.md      — Maintenance logs
```

---

## The Lean Rules

### Rule 1: Atomic MEMORY.md

MEMORY.md stores only permanently true principles. When something in MEMORY.md becomes a fact rather than a principle, move it to a project file or daily log.

### Rule 2: Mother-Child Separation

When any bootstrap file exceeds ~3KB, split it:
- Mother: Index and summaries only
- Child: Full detail, loaded on demand

### Rule 3: One Owner Per Rule

Every rule lives in exactly one file. Cross-references between files are OK for navigation, but rule ownership is singular.

### Rule 4: Scene Loading Over Global Loading

Detailed procedures belong in scene-specific files, not in always-loaded core files. The session loads what's needed, not everything.

---

## Audit Checklist

Run this monthly or whenever bootstrap feels slow:

```bash
# Check bootstrap file sizes
ls -lh ~/.openclaw/workspace/*.md | awk '{print $5, $9}'

# Check total bootstrap size
cat ~/.openclaw/workspace/*.md | wc -c

# Flag files over 3KB
for f in ~/.openclaw/workspace/*.md; do
  size=$(wc -c < "$f")
  if [ "$size" -gt 3000 ]; then
    echo "OVER 3KB: $f ($size bytes)"
  fi
done
```

### Audit Thresholds

| Metric | Warning | Action |
|--------|---------|--------|
| Bootstrap total | > 15KB | Review for bloat |
| Any single file | > 3KB | Plan split |
| MEMORY.md growth | Any | Check if facts vs rules |

---

## Bootstrap File Size Budget

| File | Target Max | Reason |
|------|-----------|--------|
| MEMORY.md | < 3KB | Loaded every session |
| AGENTS.md | < 5KB | Core rules, always loaded |
| TOOLS.md (mother) | < 3KB | Index only |
| Execution layer files | No limit | Loaded on demand |

---

## Anti-Patterns to Avoid

**Don't pile everything into MEMORY.md**
> Symptoms: Version drift, critical rules truncated, facts mixed with principles

**Don't load detailed procedures in bootstrap**
> Symptoms: Context wasted, slow session start, rules irrelevant to current task

**Don't cross-reference without ownership**
> Symptoms: "Where does this rule actually live?" — nobody knows

**Don't keep facts in bootstrap files**
> Facts belong in project files or daily logs. Bootstrap is for rules, not state.

---

## Installation

```bash
# Install via ClawHub
npx clawhub@latest install md-bootstrap-optimizer

# Or manual: copy to your skills directory
cp -r md-bootstrap-optimizer ~/.openclaw/skills/
```

---

## Prerequisites

- OpenClaw workspace with bootstrap files
- Basic understanding of your agent's bootstrap structure
- No external dependencies beyond OpenClaw

---

## Customization

This skill describes a general architecture. Adapt the layer definitions and thresholds to your workflow:

- Change `3KB` thresholds based on your context budget
- Adjust layer assignments based on what actually triggers in your sessions
- Add or remove layer categories to match your file inventory
