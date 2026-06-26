---
name: prompt-slimmer
description: >
  Audit and slim down OpenClaw workspace files (SOUL.md, AGENTS.md, TOOLS.md, IDENTITY.md,
  USER.md, HEARTBEAT.md, MEMORY.md) to reduce system prompt token usage. Analyzes each file
  for redundancy, low-frequency content, and cross-file duplication, then produces an actionable
  slim-down plan with before/after metrics. Moves archived content to memory/archive/ while
  preserving searchability via memory_search. Use when: token costs are high, context window
  is filling up, system prompt feels bloated, or you want to optimize workspace files.
  Triggers on: "slim prompt", "reduce tokens", "optimize workspace", "瘦身", "精简 prompt",
  "audit system prompt", "trim workspace files", "token bloat".
---

# Prompt Slimmer

Audit and optimize OpenClaw workspace files to reduce system prompt token overhead without losing information.

## Why This Matters

Every workspace file (SOUL.md, MEMORY.md, etc.) is injected into the system prompt on **every API call**. A 50K-char workspace means ~12K tokens sent with every single message — even a simple "hi". At Opus pricing ($15/1M input tokens), that's $0.18 per message just for workspace overhead.

## Quick Start

Run the audit:
```
1. Measure all workspace files (chars + lines)
2. Analyze each section for frequency-of-use
3. Identify redundancies across files
4. Generate slim-down plan with before/after estimates
5. Execute (with user approval) and verify
```

## The Method: Frequency-Based Layering

### Layer 1: Always-On (workspace files)
Content needed in **every session**: core identity, active relationships, behavioral rules, critical safety constraints.

### Layer 2: Searchable (memory/archive/)
Content needed **sometimes**: completed projects, historical records, detailed technical specs, one-time learnings. Retrieved via `memory_search` when relevant.

### Layer 3: Skill-Embedded
Content needed **only for specific tasks**: workflow steps, code templates, platform-specific guides. Lives in SKILL.md files, loaded only when the skill triggers.

## Audit Procedure

### Step 0: Ghost File Scan (Often the Biggest Win!)

OpenClaw injects **all** `.md` files in the workspace root into the system prompt — not just the standard files. Scan for "ghost files": old reports, task materials, research notes, or temp files sitting in the workspace root.

```bash
cd <workspace_dir>
echo "=== All .md files in workspace root ==="
for f in *.md; do
  [ -f "$f" ] && echo "$f: $(wc -c < "$f") chars"
done
echo "=== Standard files ==="
echo "SOUL.md AGENTS.md TOOLS.md IDENTITY.md USER.md HEARTBEAT.md MEMORY.md BOOTSTRAP.md GARDEN.md"
```

Any `.md` file NOT in the standard list is a ghost file candidate. Move completed task files, old research, and temp notes to `memory/archive/` or a subdirectory (subdirectories are not injected).

**Real example**: One instance had 15K in standard files but 31K in two ghost files (an old promotion review + research report) — removing them saved 63% instantly.

### Step 1: Measure Standard Files

```bash
cd <workspace_dir>
for f in SOUL.md AGENTS.md TOOLS.md IDENTITY.md USER.md HEARTBEAT.md MEMORY.md; do
  [ -f "$f" ] && echo "$f: $(wc -c < "$f") chars, $(wc -l < "$f") lines"
done
```

### Step 2: Section-Level Analysis

For each file, extract `## ` headings and measure each section's size. Then classify:

| Category | Criteria | Action |
|----------|----------|--------|
| 🟢 Keep | Referenced every session, identity-critical | Keep as-is |
| 🟡 Slim | Useful but verbose, can be compressed | Rewrite concisely |
| 🔴 Archive | Completed/paused projects, historical records | Move to `memory/archive/` |
| ⚫ Deduplicate | Same info in multiple files | Keep in one place, remove others |

### Step 3: Cross-File Deduplication Check

Common duplication patterns:
- IDENTITY.md ↔ MEMORY.md (appearance, voice info)
- SOUL.md ↔ MEMORY.md (behavioral rules)
- HEARTBEAT.md ↔ AGENTS.md (task scheduling rules)
- MEMORY.md ↔ Skill files (project details duplicated in both)

**Rule**: Information lives in the **most specific** location. If a skill covers it, remove from MEMORY.md.

### Step 4: Execute Slim-Down

1. **Create archive file**: `memory/archive/projects.md` (or topic-specific files)
2. **Move archived sections**: Cut from workspace file → paste to archive
3. **Replace with pointer**: `Details: see memory/archive/projects.md` or just a 1-line summary
4. **Verify memory_search**: Confirm archived content is findable via search
5. **Measure result**: Compare before/after char counts

### Step 5: Verify Integrity

After slimming, verify:
- [ ] `memory_search` can find archived content
- [ ] No critical behavioral rules were accidentally removed
- [ ] Core identity (name, relationships, key rules) still present
- [ ] Safety constraints still in workspace files (not just archive)
- [ ] Pointers/references are correct paths

## File-Specific Heuristics

### MEMORY.md (Usually the biggest win)
Typical bloat sources:
- **Paused/completed project details** → archive, keep 1-line status
- **Detailed timelines/changelogs** → archive
- **Team roster tables** → archive
- **Cron job indexes** → `cron list` can fetch this live
- **Platform account details** → slim to name + ID only
- **Milestone lists** → archive (historical)
- **Cross-referenced content** → remove if covered by skill or other file

Target: MEMORY.md should be < 5,000 chars for a well-maintained instance.

### HEARTBEAT.md
Typical bloat sources:
- **Code templates** (osascript, shell snippets) → agent already knows these
- **Verbose priority descriptions** → compress to 1-2 lines per priority
- **Paused project references** → 1 line max
- **Repeated emphasis** ("核心！", "每次 HB 必做！") → once is enough

Target: HEARTBEAT.md should be < 3,000 chars.

### SOUL.md
**Be careful here.** SOUL.md is identity-critical. Don't optimize away personality.
- **Hierarchy diagrams** → can be compressed
- **Behavioral rules** → review for overlap with AGENTS.md
- Generally leave SOUL.md alone unless it's > 10,000 chars.

### TOOLS.md
Usually already lean. Check for:
- **Deprecated tool entries** → remove
- **Detailed port tables** for rarely-used services → slim or archive

### AGENTS.md
Usually already lean. Check for:
- **Redundancy with system prompt** (OpenClaw injects its own rules)
- **Over-detailed workflow descriptions** → reference skill instead

## Expected Results

| Workspace Size | Before | After | Typical Savings |
|---------------|--------|-------|-----------------|
| Light (<20K) | 20K | 15K | 25% |
| Medium (20-50K) | 35K | 18K | 50% |
| Heavy (50K+) | 60K | 22K | 63% |

## Cost Impact

At Opus pricing ($15/1M input, $1.50/1M cached):

| Savings | Chars Saved | Tokens Saved | $/message saved | $/day (100 msg) |
|---------|-------------|-------------|-----------------|-----------------|
| 25% | 5K | ~2K | $0.03 | $3 |
| 50% | 25K | ~10K | $0.15 | $15 |
| 63% | 38K | ~15K | $0.23 | $23 |

*With prompt caching, savings are ~90% less but still meaningful for cache-miss turns.*

## What NOT to Slim

- **Safety constraints** (never archive security rules)
- **Core identity** (name, key relationships, personality)
- **Active behavioral rules** that prevent known failure modes
- **Credentials management rules** (how to handle secrets)
- **Cross-instance coordination rules** (if running multiple agents)
