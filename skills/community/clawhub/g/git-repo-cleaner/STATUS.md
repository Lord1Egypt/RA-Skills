# git-repo-cleaner — Status

**Price:** $49
**Status:** Ready
**Created:** 2026-04-01

## Description
Audit and clean up Git repositories. Find stale branches, merged branches, large files in history, repo bloat, and generate safe cleanup scripts.

## Features
- Branch audit: stale (configurable days), merged, active classification
- Large file detection: current tree + git history (pack analysis)
- Repo stats: .git size, commits, branches, tags, contributors, objects
- Maintenance checks: missing .gitignore patterns, tracked files that should be ignored, gc needs
- Cleanup script generation (--fix) with safe delete (git branch -d) or force (--force-delete)
- 3 output formats (text, JSON, markdown)
- CI-friendly exit codes (0 = clean, 1 = issues)
- Configurable thresholds (--stale-days, --min-size)
- Pure Python stdlib (requires git CLI)

## Tested Against
- nvm git repo (clean, basic stats)
- workspace git repo (empty repo handling)
- JSON + text output verified
- CLI args and flags verified
