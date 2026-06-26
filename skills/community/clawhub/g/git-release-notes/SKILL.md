---
name: git-release-notes
description: Generate polished release notes and changelogs from git history. Analyzes commits between tags/refs, categorizes changes (features, fixes, breaking changes, etc.), and produces formatted release notes in multiple styles. Use when asked to generate release notes, create a changelog, summarize changes between versions, write release documentation, or prepare a GitHub release. Triggers on "release notes", "changelog", "what changed since", "summarize commits", "version bump notes", "prepare release".
---

# Git Release Notes

Generate formatted release notes from git commit history. Analyzes commits between any two refs (tags, branches, SHAs) and produces categorized, human-readable release notes.

## Quick Usage

### Generate Notes Between Tags
```bash
scripts/gather_commits.sh v1.2.0 v1.3.0
```
Then format the JSON output into release notes using the formatting rules below.

### Generate Notes Since Last Tag
```bash
scripts/gather_commits.sh $(git describe --tags --abbrev=0) HEAD
```

### Generate Notes Between Branches
```bash
scripts/gather_commits.sh main release/2.0
```

## Workflow

### 1. Gather Commits

Run `scripts/gather_commits.sh <from_ref> <to_ref>` to get structured commit data (JSON array).

If no refs provided, ask user for:
- The starting point (tag, branch, or SHA)
- The ending point (default: HEAD)

### 2. Categorize Commits

Group commits by type using conventional commit prefixes and content analysis:

| Category | Prefixes / Signals | Emoji |
|----------|-------------------|-------|
| Breaking Changes | `BREAKING CHANGE:`, `!:` in subject | 💥 |
| Features | `feat:`, `feature:`, `add:` | ✨ |
| Bug Fixes | `fix:`, `bugfix:`, `hotfix:` | 🐛 |
| Performance | `perf:` | ⚡ |
| Documentation | `docs:`, `doc:` | 📚 |
| Refactoring | `refactor:` | ♻️ |
| Testing | `test:`, `tests:` | 🧪 |
| CI/Build | `ci:`, `build:`, `chore:` | 🔧 |
| Dependencies | `deps:`, `dep:`, "bump", "upgrade" in subject | 📦 |
| Other | Anything else | 📝 |

If commits don't follow conventional commits, analyze the commit message content to infer categories.

### 3. Format Release Notes

Default format (GitHub Release style):

```markdown
# v1.3.0

> Released on 2026-03-26 | 47 commits | 5 contributors

## 💥 Breaking Changes
- Remove deprecated `legacy_auth` endpoint (#234)

## ✨ Features
- Add dark mode support (#220)
- Implement batch export for CSV/JSON (#215)

## 🐛 Bug Fixes
- Fix race condition in queue processor (#228)
- Correct timezone handling for UTC offset (#225)

## ⚡ Performance
- Optimize database queries for dashboard load (#222)

## 📦 Dependencies
- Bump express from 4.18 to 4.21

## 🔧 Other
- Update CI pipeline for Node 22

**Full Changelog:** v1.2.0...v1.3.0
```

### 4. Alternative Formats

**Compact (for small releases):**
```
v1.3.0 — Dark mode, batch export, 5 bug fixes. Breaking: removed legacy_auth.
```

**Keep a Changelog (keepachangelog.com):**
```markdown
## [1.3.0] - 2026-03-26
### Added
- Dark mode support
### Changed
- Optimized dashboard queries
### Removed
- Deprecated legacy_auth endpoint
### Fixed
- Race condition in queue processor
```

**Slack/Discord announcement:**
```
🚀 **v1.3.0 is out!**

Highlights:
→ Dark mode support
→ Batch CSV/JSON export
→ 5 bug fixes

⚠️ Breaking: `legacy_auth` endpoint removed — migrate to `/v2/auth`
```

## Customization

Users can specify:
- **Format** — github (default), compact, keepachangelog, slack
- **Include/exclude categories** — "skip docs and chore commits"
- **Group by** — category (default), author, scope
- **PR links** — auto-detect GitHub PR numbers (#NNN)
- **Contributors** — list contributors at the bottom
- **Scope filter** — only include commits touching certain paths

## Scripts

- `scripts/gather_commits.sh <from> <to>` — Outputs JSON array of commits with hash, author, date, subject, body
