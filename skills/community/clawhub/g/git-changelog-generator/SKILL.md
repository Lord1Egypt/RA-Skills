# Git Changelog Generator

Generate structured changelogs from git history. Supports conventional commits, semantic versioning, and multiple output formats. Use when preparing releases, writing release notes, or documenting project history.

## Usage

```bash
# Generate changelog for latest unreleased changes
python3 scripts/generate_changelog.py

# Generate changelog between two tags
python3 scripts/generate_changelog.py --from v1.2.0 --to v1.3.0

# Generate for last N commits
python3 scripts/generate_changelog.py --last 20

# Generate since a date
python3 scripts/generate_changelog.py --since 2026-04-01
```

## Output Formats

```bash
# Markdown (default)
python3 scripts/generate_changelog.py --format markdown

# Keep a Changelog format (keepachangelog.com)
python3 scripts/generate_changelog.py --format keepachangelog

# GitHub Release format
python3 scripts/generate_changelog.py --format github-release

# JSON (for programmatic use)
python3 scripts/generate_changelog.py --format json
```

## How It Works

1. **Collect** — reads git log between specified ranges
2. **Parse** — extracts conventional commit types (feat, fix, refactor, docs, test, chore, perf, ci)
3. **Categorize** — groups changes by type with human-readable headers
4. **Enrich** — adds PR links, issue references, author attribution, breaking change warnings
5. **Format** — outputs in the requested format

## Conventional Commit Support

Parses standard prefixes:
- `feat:` → Features
- `fix:` → Bug Fixes
- `refactor:` → Code Refactoring
- `docs:` → Documentation
- `test:` → Tests
- `perf:` → Performance
- `ci:` → CI/CD
- `chore:` → Maintenance
- `BREAKING CHANGE:` → Breaking Changes (highlighted)

Non-conventional commits are categorized as "Other Changes" with AI-assisted categorization.

## Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--from` | Start tag/commit | Last tag |
| `--to` | End tag/commit | HEAD |
| `--last` | Last N commits | All since last tag |
| `--since` | Start date (YYYY-MM-DD) | None |
| `--format` | Output format | `markdown` |
| `--output` | Write to file | stdout |
| `--repo` | Repository path | Current directory |
| `--include-authors` | Show commit authors | false |
| `--include-hashes` | Show commit hashes | false |
| `--group-by` | Group by `type` or `scope` | `type` |

## AI Enhancement

When used as an agent skill, the AI can:
- Rewrite terse commit messages into human-readable descriptions
- Identify the most impactful changes and highlight them
- Generate a summary paragraph for release announcements
- Detect breaking changes even without conventional commit markers
- Cross-reference with issue trackers for richer context
