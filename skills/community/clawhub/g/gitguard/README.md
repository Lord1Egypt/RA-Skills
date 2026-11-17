# 🛡️ GitGuard

Advanced Git/GitHub repo intelligence for AI agents and developers juggling
many active projects.

**Local-first. No secrets ever leave your machine.**

## Features

- 🔑 **Secret scanning** via Shannon entropy + known credential patterns
  (AWS, GitHub, Stripe, Slack, private keys, generic assignments)
- 📊 **Composite health score** (0-100, graded A-F) across secrets,
  commits, branches, dependencies, and activity
- ✍️ **Commit quality analysis** — Conventional Commits scoring
- 🌿 **Stale branch detection** with keep/review/delete/merge recommendations
- 📦 **Dependency freshness** against live npm/PyPI registries
- 🐙 **GitHub PR/issue triage** for open backlog

## Install

```bash
pip install -r requirements.txt
```

`requests` is optional — secret scanning, commit analysis, and branch
detection all work fully offline without it.

## Quick Start

```python
from gitguard_skill import GitGuard

guard = GitGuard()

# Scan for exposed secrets
result = guard.scan_secrets(".")
print(f"{result['total_findings']} potential secrets found")

# Full health report
report = guard.health_report(".")
print(f"Health: {report['health_score']}/100 (grade {report['grade']})")

# Rank multiple repos
dashboard = guard.multi_repo_dashboard([
    "~/project-a", "~/project-b", "~/project-c",
])
```

## How the Health Score Works

```
health_score = 0.35 * secret_safety      (fewer/less severe secrets = higher)
             + 0.20 * commit_hygiene      (Conventional Commits quality)
             + 0.20 * branch_hygiene      (% of branches that aren't stale/dead)
             + 0.15 * dependency_health   (% of deps that are current)
             + 0.10 * activity            (recency of last commit)
```

Grade bands: A ≥ 90, B ≥ 75, C ≥ 60, D ≥ 40, F < 40.

## How Secret Detection Works

1. Extract candidate tokens from each line (quoted strings, bare
   high-entropy runs ≥ 20 chars).
2. Check against known patterns first (AWS keys, private key headers,
   GitHub/Slack/Stripe tokens, generic `key=`/`secret=` assignments) —
   these are high-confidence regardless of entropy.
3. Fall back to Shannon entropy scoring for anything else — random
   secrets cluster in a high-entropy band that ordinary source code and
   English text do not reach.
4. Findings are always redacted (first/last 4 chars only) before being
   returned or displayed.

## Requirements

- Python 3.9+
- `git` CLI on PATH
- `requests` (optional, for dependency/GitHub checks)
- `GITHUB_TOKEN` env var (optional, raises API rate limit)

## Support

GitGuard is free and open source. If it saved you time, voluntary support
is welcome:

- Website: https://btc-vision.org
- BTC: `bc1qtpuhwl0vnhrch5p7e5469q2ed66hlyyvh8rtsn`
- ETH: `0xf03b429d4d85896a46dd7a64b5a8ab9f0bbb4ced`
- SOL: `3G5UZHFYN8hbv3aTZt6Lr7qqx4FTTkAyLJq34HjQLraz`
- Lightning: `welove@blink.sv`

## License

MIT
