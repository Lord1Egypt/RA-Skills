---
name: github-growth-tracker
description: >
  Track GitHub repo growth (stars, forks, issues, commits) with periodic digests and trend
  analysis. Compare your repos against a watchlist. Use when checking repo stats, monitoring
  growth, setting up a github digest, comparing repos, or managing a repo watchlist.
  Requires GITHUB_TOKEN environment variable or GitHub PAT (see Credentials).
homepage: https://github.com/99rebels/github-growth-tracker
---

# GitHub Growth Tracker 📊

Track stars, forks, issues, and commit activity across GitHub repos. Generates text digests with trend arrows (↑↓→) and compares your repos against a watchlist you curate.

## Why

You ship code but have no idea if anyone's using it. This skill gives you a weekly pulse on your projects — what's growing, what's stagnant, and how you stack up against repos you admire.

## When to Use

- "Check my repo stats"
- "How's my project doing on GitHub?"
- "Give me a growth digest"
- "Compare my repo against X"

## Credentials

**Required:** GitHub Personal Access Token (fine-grained, public repo read-only).

```
Create at: github.com → Settings → Developer settings → Personal access tokens
Type:     Fine-grained
Access:   Public repos (read-only)
```

Pass via `setup --token <TOKEN>` (saved to `<DATA_DIR>/github.json`) or set `GITHUB_TOKEN` env var.

⚠ Token is stored plaintext on disk. For higher security, use the `GITHUB_TOKEN` environment variable instead.

## Setup

```
python3 scripts/github_tracker.py setup --token <TOKEN>   # list your repos
python3 scripts/github_tracker.py add owner/repo1 owner/repo2  # track repos
python3 scripts/github_tracker.py add other/repo --watch  # watchlist
python3 scripts/github_tracker.py fetch                     # record data
```

## Commands

```
setup [--token TOKEN]              List your repos, optionally save token
fetch                              Fetch metrics for all tracked + watched repos
digest                             Generate growth digest with trends
add repo1 [repo2 ...] [--watch]    Add repos to tracking or watchlist
remove owner/repo                  Stop tracking (history preserved)
list                               Show tracked repos and watchlist
```

## Output Example

```
📊 GitHub Growth Digest — Friday April 03, 2026
====================================================

📌 Your Repos

   99rebels/blog-translator
      Stars: 3 ↑ (+2)
      Forks: 1 →
      Issues: 2 ↓ (-1)
      Commits (4w): 5 ↑ (+5)
      Lang: TypeScript  Last push: 2026-04-03
      vs watchlist: ✅ above avg commit velocity

📌 Watchlist

   octocat/Hello-World
      Stars: 3,550 NEW  Forks: 5,963 NEW  Commits (4w): 0
```

Format output for the current channel. Read [references/formatting.md](references/formatting.md) for platform-specific examples.

## Scheduled Monitoring

```
python3 <skill_path>/scripts/github_tracker.py fetch && python3 <skill_path>/scripts/github_tracker.py digest
```

## Data Directory

Credentials and data resolve to:

```
1. $SKILL_DATA_DIR (set by agent platform)
2. ~/.config/github-growth-tracker/  (default fallback)
```

```
Credentials: <DATA_DIR>/github.json     (token)
Config:      <DATA_DIR>/config.json      (repo lists)
History:     <DATA_DIR>/repos/           (per-repo, 90 days)
```

Any platform can set `$SKILL_DATA_DIR`. If unset, `~/.config/github-growth-tracker/` is used. Works with OpenClaw, Claude Code, Codex, and any agent that can run Python scripts.

## Notes

- `fetch` skips repos already recorded today (safe to run multiple times)
- `add` accepts multiple repos: `add repo1 repo2 repo3`
- History auto-trims to 90 days on each save
- GitHub API rate limit: 5,000 req/hour authenticated
