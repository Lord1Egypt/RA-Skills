---
name: lingxi-daily-ops
category: automation
description: "Complete daily operations automation for GitHub projects — automated GitHub interactions (star, comment, PR review), daily report generation, trending watch, and multi-platform social publishing. Reduces manual effort to near zero."
version: 1.0
---

# lingxi-daily-ops

Automate your daily GitHub and social media operations with a systematic, schedulable workflow.

## What It Automates

| Operation | Frequency | Description |
|-----------|-----------|-------------|
| GitHub Star | Daily | Star relevant trending projects |
| GitHub Comment | Daily | Meaningful comment on target repos |
| Daily Report | Daily | Generate operations summary |
| Trending Watch | Daily | Monitor specified topics for new projects |
| Health Check | Hourly | Verify services and endpoints |

## Usage

### Trigger Commands

```
"Run daily ops"        → Full daily workflow
"GitHub star run"      → Only GitHub starring
"Generate daily report"→ Only report generation
"Health check"         → Only service health check
"Trending watch"       → Only topic monitoring
```

## Daily Workflow Sequence

```
1. Health Check (08:30)
   → Check GitHub API status
   → Verify all webhook endpoints
   → Check ZeroGPU status

2. GitHub Trending Watch (08:35)
   → Fetch trending for watched languages
   → Compare with yesterday's snapshot
   → Flag new entries in watched topics

3. GitHub Interactions (08:40)
   → Star relevant new projects (auto filter by topics)
   → Post comments on configured repos
   → Update issue trackers

4. Report Generation (08:50)
   → Compile operations log
   → Generate markdown report
   → Upload via GitHub API fallback (if push blocked)

5. Social Publish (09:00)
   → Format digest for target platforms
   → Post to configured channels
```

## Configuration

Create `~/.openclaw/daily-ops-config.json`:

```json
{
  "github_token": "ghp_xxx",
  "watch_topics": ["ai", "open-source", "developer-tools"],
  "watch_languages": ["python", "typescript", "rust"],
  "target_repos": ["owner/repo1", "owner/repo2"],
  "star_threshold": 100,
  "comment_templates": {
    "default": "Great project! 🚀 Auto-starred by lingxi daily-ops."
  },
  "report_channel": "~/daily-ops/reports/",
  "health_check_targets": [
    "https://github.com",
    "https://api.github.com",
    "https://platform.zerogpu.ai"
  ]
}
```

## Comment Quality Rules

**DO:**
- Acknowledge specific features you genuinely find useful
- Ask a real question about the project
- Point to related resources that might help

**DON'T:**
- Generic "Great project!" spam
- Duplicate existing comments
- Comments on repos with explicitly anti-bot policies

## Report Template

```markdown
# Daily Ops Report — YYYY-MM-DD

## GitHub Activity
- Stars given: N
- Comments posted: N
- New projects discovered: N

## Health Status
- GitHub API: ✅
- ZeroGPU: ✅
- Webhooks: ✅

## Trending Watch
New entries in watched topics:
- [project-name](url) — [brief description]

## Tomorrow's Focus
- [ ] Priority task 1
- [ ] Priority task 2
```

## Cron Schedule

```
0 9 * * *  → Full daily workflow (9:00 AM)
*/30 * * * * → Health check (every 30 min)
```

## Installation

```bash
clawhub install lingxi-daily-ops
```

## Requirements

- `gh` CLI authenticated with appropriate scopes
- GitHub token with: `repo`, `read:user`, `public_repo`
- OpenClaw with `github` skill installed
