---
name: pr-description-generator
description: >
  Auto-generate pull request descriptions from git diffs and commit history.
  Parses conventional commits, categorizes changes (features, fixes, refactoring),
  analyzes file impact, generates reviewer hints, and produces structured descriptions.
  Supports minimal, standard, and detailed templates with markdown or JSON output.
  Use when asked to generate PR descriptions, create pull request summaries,
  describe git changes, summarize a branch, or prepare a PR body.
  Triggers on "PR description", "pull request description", "generate PR",
  "describe changes", "PR summary", "what changed", "PR body", "PR template".
---

# PR Description Generator

Auto-generate structured PR descriptions from git diffs and commit history. Pure Python + git CLI.

## Quick Start

```bash
# Standard description (current branch vs main)
python3 scripts/generate_pr_description.py

# Compare against specific base branch
python3 scripts/generate_pr_description.py --base develop

# Minimal template (just bullet points)
python3 scripts/generate_pr_description.py --template minimal

# Detailed template (file breakdown + reviewer hints)
python3 scripts/generate_pr_description.py --template detailed

# JSON output (for automation)
python3 scripts/generate_pr_description.py --format json

# Different repo path
python3 scripts/generate_pr_description.py --repo /path/to/repo

# Save to file
python3 scripts/generate_pr_description.py --output pr-body.md

# Copy to clipboard
python3 scripts/generate_pr_description.py --copy
```

## Features

- **Conventional commit parsing** — groups commits by type (feat, fix, refactor, etc.)
- **Impact analysis** — rates changes as high/medium/low based on files, size, and risk
- **File categorization** — groups by code, tests, docs, infra, deps, config, database, styles
- **Reviewer hints** — warns about missing tests, DB migrations, infra changes, deletions
- **Auto test plan** — generates relevant test checklist based on changed file types
- **Auto base detection** — detects main vs master branch

## Templates

| Template | Use Case |
|----------|----------|
| `minimal` | Quick summary, internal PRs |
| `standard` | Default, most PRs |
| `detailed` | Large PRs, cross-team reviews |

## Conventional Commits

Best results when commits follow conventional format:

```
feat(auth): add OAuth2 login
fix(api): handle null response from payment gateway
refactor: extract validation into shared utility
docs: update API reference for v2 endpoints
```

Non-conventional commits are grouped under "Other Changes".
