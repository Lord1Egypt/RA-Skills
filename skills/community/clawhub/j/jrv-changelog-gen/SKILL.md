---
name: jrv-changelog-gen
description: Generate changelogs from git commit history with conventional commit parsing. Use when asked to generate a changelog, create release notes, summarize git history, list changes between tags or dates, or prepare release documentation. Supports conventional commits (feat, fix, docs, etc.), breaking change detection, grouped output, and markdown or JSON format. No external dependencies.
---

# Changelog Generator

Generate clean, professional changelogs from git commit history.

## Quick Start

```bash
python3 scripts/changelog_gen.py
python3 scripts/changelog_gen.py --since v1.0.0 --group
python3 scripts/changelog_gen.py --since v1.0.0 --until v2.0.0 --format json
python3 scripts/changelog_gen.py --repo /path/to/project --since "2026-01-01" -o CHANGELOG.md
```

## Features

- **Conventional commit parsing** — auto-detects feat, fix, docs, refactor, perf, test, build, ci, chore, revert
- **Breaking change detection** — from `!` suffix or `BREAKING CHANGE` in body
- **Grouped output** — organize by commit type with `--group`
- **Tag ranges** — generate changelogs between any two tags or refs
- **Dual format** — markdown (default) or JSON
- **File output** — write directly to CHANGELOG.md with `-o`
- **No dependencies** — Python stdlib + git

## Options

| Flag | Description |
|------|-------------|
| `--repo PATH` | Path to git repo (default: cwd) |
| `--since REF` | Start ref — tag, branch, or commit |
| `--until REF` | End ref (default: HEAD) |
| `--format md\|json` | Output format (default: md) |
| `--group` | Group commits by type |
| `-o FILE` | Write to file |

## Conventional Commit Types

feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert — all parsed automatically.
