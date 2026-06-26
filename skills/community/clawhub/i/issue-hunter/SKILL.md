---
name: issue-hunter
description: "Analyze, triage, and select the best issues to work on from GitHub repositories. Scores issues by reproducibility, scope, complexity, and community signal. Produces a structured analysis document with root cause hypotheses and fix approaches. Use when deciding which issues to tackle in open-source projects, prioritizing a backlog, or analyzing bug reports."
---

# Issue Hunter — Issue Analysis & Selection

## Overview

Systematically analyze open issues in target repositories, score them by fixability, and select the best candidates to work on. Produces a structured analysis document with root cause hypotheses and fix approaches.

**Use cases**: Open-source contribution targeting, sprint planning, backlog grooming, bug triage.

## Prerequisites

GitHub CLI must be authenticated — issue fetching relies on `gh` API calls:

```bash
gh auth status   # Must show "Logged in"
```

If not configured, ask the user to provide:
1. **GitHub username**
2. **GitHub token** — run `gh auth login` or set `export GH_TOKEN=<token>`

Without auth, API rate limits will block bulk issue fetching.

## Workflow

### Step 1: Fetch Issues

For each target repository, fetch open issues:

```bash
# Fetch bug-labeled issues
gh issue list --repo {owner}/{repo} --label bug --state open --limit 30 \
    --json number,title,body,labels,comments,createdAt,updatedAt

# Also check these labels
gh issue list --repo {owner}/{repo} --label "good first issue" --state open --limit 10 \
    --json number,title,body,labels,comments,createdAt

gh issue list --repo {owner}/{repo} --label "help wanted" --state open --limit 10 \
    --json number,title,body,labels,comments,createdAt
```

If no label filtering works, fetch recent open issues:
```bash
gh issue list --repo {owner}/{repo} --state open --limit 50 \
    --json number,title,body,labels,comments,createdAt
```

### Step 2: Score Each Issue

Rate each issue on these factors:

| Factor | 3 (High) | 2 (Medium) | 1 (Low) |
|--------|----------|-----------|---------|
| **Reproducibility** | Clear repro steps, stack trace | Partial description | Vague "doesn't work" |
| **Scope** | Single module/file | 2-3 files | Cross-cutting concern |
| **Complexity** | Logic bug, missing check | Algorithm issue | Architecture redesign |
| **Community signal** | Multiple reports, 👍 | Some engagement | Single report, no reaction |
| **Freshness** | Recent, no PR attempts | Moderate age | Old, multiple failed PRs |
| **Testability** | Can write automated test | Partially testable | Manual testing only |

**Total score** = sum of all factors (max 18).

### Step 3: Select Candidates

**Selection criteria** (in priority order):
1. Clearly a bug (not a feature request in disguise)
2. Self-contained (fixable without deep domain knowledge)
3. Testable (can write automated tests to verify)
4. No existing PR addressing it
5. Score ≥ 12/18

**Red flags** — skip issues if:
- Already has an open PR (check with `gh pr list --repo owner/repo --search "fixes #{number}"`)
- Requires access to proprietary services/APIs
- Involves native/platform-specific code you can't test
- Maintainer has said "won't fix" or "by design"

### Step 4: Deep-Dive Selected Issues

For each selected issue:

1. **Read the full thread** — comments often contain root cause hints or partial fixes
2. **Identify relevant source files** — search the codebase for keywords from the issue
3. **Draft a root cause hypothesis** — "I believe X happens because Y"
4. **Draft a fix approach** — "I'll modify Z to handle the W case"
5. **Estimate effort** — Low (< 1 hour), Medium (1-4 hours), High (4+ hours)

### Step 5: Produce Analysis Document

Write `{workspace}/issue-analysis.md`:

```markdown
# Issue Analysis — {Repository/Campaign Name}

> Generated: {date}

## Summary

| # | Repository | Issue | Title | Score | Effort | Status |
|---|-----------|-------|-------|-------|--------|--------|
| 1 | owner/repo | #123 | Bug title | 16/18 | Low | Selected |
| 2 | owner/repo | #456 | Bug title | 12/18 | Medium | Selected |
| 3 | owner/repo | #789 | Bug title | 8/18 | High | Skipped |

---

## Detailed Analysis

### owner/repo — Selected: #123 — Bug title

- **Score**: 16/18 (Repro: 3, Scope: 3, Complexity: 3, Signal: 2, Fresh: 3, Testable: 2)
- **Root cause**: {hypothesis}
- **Fix approach**: {description}
- **Files to modify**: `path/to/file.py`, `tests/test_file.py`
- **Effort estimate**: Low (< 1 hour)
- **Risk**: Low — straightforward null check
- **Dependencies**: None

### owner/repo — Skipped: #789 — Bug title
- **Reason**: Requires architecture redesign, score 8/18
```

## Output

- `{workspace}/issue-analysis.md` — Per-repo issue analysis with selections

## Tips

- Pairs naturally with **repo-scout** (upstream) and **repo-setup** / **dev-test** (downstream).
- For sprint planning: use the scoring system on your own project's issues to prioritize.
- For backlog grooming: run periodically to re-score issues as new information appears.
- When analyzing a single repo, skip the summary table and go straight to detailed analysis.
