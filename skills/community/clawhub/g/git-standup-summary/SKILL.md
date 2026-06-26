---
name: git-standup
description: "Generate concise daily/weekly standup summaries from git commit history. Analyzes recent commits, groups them by type (features, fixes, refactors, chores), and produces a standup-ready status report. Use when the user wants to: (1) Generate a daily standup summary for yourself or your team, (2) See what everyone worked on yesterday, (3) Prepare for daily scrum meetings, (4) Get a weekly activity digest, (5) Track progress on a specific branch or feature, (6) Generate a status report for your manager. Best for developers, engineering teams, remote workers, scrum masters, and anyone who needs quick git-based status reports."
version: 1.0.0
homepage: https://clawhub.ai
metadata:
  openclaw:
    emoji: "🗓️"
    requires:
      bins:
        - git
---

# Git Standup

Turn your git log into **actionable standup summaries** — see what you (or your team) worked on in seconds.

## When to Use

✅ **USE this skill when:**

- "What did I do yesterday?"
- "Generate my daily standup"
- "What did the team work on this week?"
- "Show me progress on the feature/xyz branch"
- "Summarize commits since last Monday"
- "Prepare my scrum update"
- "Generate a weekly activity report"

❌ **DON'T use this skill when:**

- Need a full changelog between releases → use a release tool
- Need code review on the changes → use a code review skill
- Need deployment summaries → use a CI/CD skill

## How It Works

1. Queries `git log` with the requested time window
2. Parses commit messages, authors, dates, and file paths
3. Groups commits by:
   - **Type** (features, fixes, refactors, docs, chores, tests)
   - **Scope/area** (API, frontend, CLI, database, etc.) — extracted from Conventional Commits scopes
   - **Author** (for team reports)
4. Generates a clean, scrum-ready summary

## Available Actions

### `standup:daily`
Commits from yesterday / last 24 hours.

```
What did I do yesterday?
```

### `standup:weekly`
Last 7 days of activity.

```
Generate my weekly standup for this week
```

### `standup:range`
Custom date range or commit range.

```
Summarize commits from May 1 to May 5
What did we do between v1.0 and v1.1?
```

### `standup:team`
Show what all authors in the repo contributed.

```
What did the team work on this week?
```

### `standup:branch`
Compare a feature branch against base.

```
What changed in the feature/new-auth branch?
```

### `standup:author`
Filter by a specific author.

```
What did @alice work on this week?
```

## Output Format

### Single Author Daily Standup

```
🗓️  Standup for Tuesday, May 5

✅ Done (4 commits):
  • feat(api): add rate limiting middleware        — 30m ago
  • fix(auth): handle null token in verify flow     — 2h ago
  • refactor(db): extract connection pool logic     — 3h ago
  • chore(deps): upgrade express to v5              — yesterday

📊 Breakdown:
  • 1 feature   ·  1 fix   ·  1 refactor   ·  1 chore
  • 6 files changed · +142 / -38

📁 Areas: API → 2 · Auth → 1 · Database → 1
```

### Team Weekly Standup

```
🗓️  Team Standup — Apr 29 – May 5

👤 alice (8 commits)
  • feat(ui): dark mode toggle
  • fix(css): mobile nav overflow
  • refactor(store): migrate to Zustand
  • 5 more commits...

👤 bob (5 commits)
  • feat(api): add user export endpoint
  • fix(api): wrong status code on delete
  • 3 more commits...

👤 charlie (12 commits)
  • feat(cli): add --json output flag
  • fix(cli): --help formatting
  • chore: update CI cache strategy
  • 9 more commits...

───
Total: 25 commits · +1084 / -312 across 47 files
```

## Tips

- **Best with Conventional Commits** — works best when commit messages follow `type(scope): description` format, but also works with any commit style
- **Use daily** — run at the end of your day or first thing in the morning for your standup
- **Team repos** — run on the shared repo for a quick team-wide view
- **Multiple repos** — run in each repo and combine results for a multi-project standup

## Notes

- Works with any git repo — no special configuration needed
- Respects `.git` boundaries; won't traverse outside the repo
- For `team` mode, lists up to 10 most active authors
- Large history (>200 commits) is summarized rather than listed individually
