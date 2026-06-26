---
name: knowledge-health-checker
description: Audit and improve Markdown knowledge-base health across Obsidian, Logseq, Notion exports, docs folders, and wiki repositories. Detect empty placeholder notes, broken wiki links, weak content density, orphan notes, graph fragmentation, stale files, and repair opportunities. Generate health scores, actionable reports, and safe fix plans. Use for knowledge base audit, wiki lint, broken link detection, Obsidian vault cleanup, markdown graph health, content quality review, and documentation garden maintenance.
version: "1.1.0"
last_updated: "2026-04-25"
changelog: "ClawHub-ready Darwin optimization: public positioning, clearer workflow, safety boundaries, scoring rubric, output format, and test prompts."
---

# Knowledge Health Checker

Knowledge Health Checker audits a Markdown-based knowledge base as a living system, not a folder full of files.

It detects whether the knowledge garden is:

- connected or fragmented
- dense or hollow
- current or stale
- navigable or full of dead links
- safe to auto-fix or requiring human review

The goal is not only to find problems, but to produce a **prioritized, safe, actionable health report**.

---

## When to Use

Use this skill for:

- Obsidian vault cleanup
- Logseq / Notion Markdown export review
- documentation repository health checks
- wiki linting before migration or publishing
- broken link detection
- empty placeholder / TODO note detection
- orphan note and graph fragmentation analysis
- content density and structure quality review
- periodic knowledge-base maintenance

Do not use it for semantic fact-checking. This skill checks structure, links, density, freshness, and maintainability, not whether every claim is true.

---

## Core Principle

A healthy knowledge base has four properties:

1. **Substance** — notes contain enough content to be useful.
2. **Connectivity** — important notes are linked into the graph.
3. **Navigability** — links, headings, and structure help readers move through knowledge.
4. **Maintainability** — stale, broken, duplicate, or low-value content is visible and repairable.

A knowledge base can be large and still unhealthy. Size is not health.

---

## Default Workflow

### Step 1: Confirm scope and safety

Before scanning, identify:

```text
Target path:
Formats: markdown / wiki links / relative links
External URL check: yes/no
Generate fix script: yes/no
Auto-apply fixes: no by default
Exclude directories:
Estimated file count:
```

Safe default:

```text
scan only → report only → generate fix plan → user reviews → user applies
```

Never delete, rename, rewrite, or auto-apply fixes without explicit confirmation.

### Step 2: Build file and heading index

Index:

- `.md` files
- normalized filenames and aliases
- headings / anchors
- relative paths
- wiki links such as `[[note]]` and `[[note#heading]]`
- markdown links such as `[text](path.md)`

Exclude by default:

```text
.git/
node_modules/
__pycache__/
.obsidian/
.trash/
dist/
build/
```

### Step 3: Detect hollow or low-value notes

Flag likely hollow notes when they match one or more:

- fewer than 200 characters
- no heading
- only TODO / placeholder text
- image-heavy with very little explanation
- template content not filled in
- empty exported page from Notion/Logseq

Classify severity:

| Severity | Meaning | Typical action |
|---|---|---|
| P0 | Empty or pure placeholder | delete, archive, or fill immediately |
| P1 | Too thin to be useful | expand with definition, context, examples |
| P2 | Usable but weak | improve structure or add links |

### Step 4: Detect broken links

Check:

- wiki file links: `[[filename]]`
- wiki heading links: `[[filename#heading]]`
- local markdown links: `[text](../path/file.md)`
- image/embed paths
- optional external URLs, only with user confirmation because it can be slow/noisy

For each broken link, report:

```text
source file
link text
target
link type
probable fix if a similar file exists
```

### Step 5: Analyze content density and structure

Measure:

- word/character count
- heading depth and hierarchy
- list/table/code-block usage
- internal link count
- external link count
- last modified time
- very long files that may need splitting
- files with no inbound or outbound links

Suggested ranges:

| Signal | Healthy range | Warning |
|---|---|---|
| Short note | 300+ words or intentionally atomic | <200 characters |
| Long note | still navigable with headings | >3000 words without structure |
| Internal links | at least 1-3 for durable notes | zero links = possible orphan |
| Freshness | depends on domain | stale if >90 days and marked active |

### Step 6: Analyze knowledge graph health

Build a graph:

```text
node = markdown file
edge = internal link
```

Report:

- total nodes
- total edges
- orphan nodes
- central nodes
- weakly connected components
- one-way links
- fragmented topic clusters

A perfect graph is not required. The goal is to identify the highest-value repair points.

### Step 7: Score health

Default scoring:

| Dimension | Weight | Good state |
|---|---:|---|
| Hollow note rate | 25% | few or no empty placeholders |
| Broken link rate | 30% | no broken internal links |
| Content density | 25% | most notes have useful substance and structure |
| Network connectivity | 20% | important notes are connected; few accidental orphans |

Health score:

```text
health = weighted score from 0 to 100
```

Use labels:

| Score | Label |
|---:|---|
| 90-100 | Excellent |
| 75-89 | Healthy |
| 60-74 | Needs maintenance |
| 40-59 | Fragile |
| 0-39 | Critical |

### Step 8: Generate report and fix plan

Return a concise summary first. For large scans, provide a full report path.

Fix plans must be safe:

- generate proposed changes
- group by risk
- include reason for each fix
- require user review before applying destructive changes

Never silently delete or rewrite knowledge files.

---

## Output Format

Use this format:

```markdown
## Knowledge Health Summary
- Target:
- Files scanned:
- Health score:
- Label:
- Top risks:

## Findings
| Category | Count | Severity | Notes |
|---|---:|---|---|
| Hollow notes |  |  |  |
| Broken links |  |  |  |
| Orphan notes |  |  |  |
| Overlong notes |  |  |  |
| Stale active notes |  |  |  |

## Highest-Impact Fixes
1. P0:
2. P1:
3. P2:

## Safe Fix Plan
- Auto-safe fixes:
- Needs human review:
- Do not auto-apply:

## Artifacts
- Report:
- Fix script:
- Raw JSON:
```

For small knowledge bases, include concrete file examples. For large ones, include top 10 examples per category and write full details to a report file.

---

## Safe Fix Policy

Classify fixes by risk:

| Risk | Examples | Permission |
|---|---|---|
| Low | generate report, list broken links, suggest links | no extra confirmation |
| Medium | create fix script, add missing backlinks in draft output | ask before writing files |
| High | delete notes, rename files, rewrite links globally, split files | explicit confirmation required |

Default behavior: **report and propose, do not mutate**.

---

## Bundled Scripts

Use these when available:

- `scripts/health_check.py` — core scanner for hollow files, broken links, density, and graph stats.
- `scripts/report_generator.py` — HTML report generation.
- `scripts/auto_fix.py` — fix-plan or repair-script generation.

Run scripts from the skill directory or pass absolute paths. If a script lacks CLI ergonomics, inspect it and adapt safely rather than guessing destructive behavior.

---

## Example Commands

Basic scan:

```bash
python3 scripts/health_check.py /path/to/knowledge-base
```

Generate a report from scan results if supported:

```bash
python3 scripts/report_generator.py results.json --output health-report.html
```

Generate a fix plan, not auto-apply:

```bash
python3 scripts/auto_fix.py results.json --dry-run
```

If the bundled script does not support these exact flags, read the script first and use its actual interface.

---

## Test Prompts

Use `test-prompts.json` for Darwin-style regression evaluation. Good test coverage should include:

- small Markdown folder with broken links
- Obsidian-style wiki links and missing headings
- placeholder-heavy exported notes
- a large graph with orphan clusters
- request for safe fix plan without auto-apply

---

## Anti-Patterns

Avoid:

- equating more notes with better knowledge
- deleting or rewriting files without confirmation
- checking external URLs by default on large vaults
- treating all orphan notes as bad; some are intentionally private/draft
- creating huge reports with no prioritized next action
- producing a repair script without explaining risk
- ignoring non-English filenames and encodings

---

## Quality Bar

A good knowledge health check must be:

- **safe**: no destructive changes without confirmation
- **specific**: names files and link targets
- **prioritized**: P0/P1/P2, not a flat dump
- **actionable**: includes exact repair suggestions
- **scalable**: summarizes large vaults without flooding context
- **portable**: works for Obsidian, Logseq, Notion exports, and plain Markdown

If the output only says “you have broken links” without showing where, why it matters, and what to do next, it failed.
