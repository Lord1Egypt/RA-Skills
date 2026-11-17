---
name: gitguard
version: 1.1.0
description: "Git Security Scanner & Repo Health Auditor — entropy-based secret detection, composite health scoring, commit quality analysis, stale branch cleanup, and dependency freshness checks across all your local repos. Local-first, no data leaves your machine except optional GitHub API reads."
author: welove111
homepage: https://btc-vision.org
license: MIT
tags: [git, github, devtools, security, code-quality, repo-management]
protocols: [mcp]
category: developer-tools
---

# GitGuard — Repo Intelligence for AI Agents

Give an agent the ability to audit, score, and triage your own Git
repositories: exposed secrets, branch hygiene, commit quality, stale
dependencies, and GitHub PR/issue backlog — all from local git data plus
optional public GitHub API reads.

**🔒 Scope and safety notice** — GitGuard only reads files and git metadata
already on your local disk in the repository you point it at. Secret scan
findings are always returned as redacted previews (first/last 4 characters
only); raw secret values are never stored, logged, or transmitted. The only
network calls this skill makes are read-only lookups against the public
npm/PyPI registries (dependency freshness) and the GitHub REST API
(PR/issue triage, optional token) — no data about your code or secrets is
ever sent anywhere.

## What This Skill Does

- **Secret scanning** — Shannon-entropy analysis plus known credential
  patterns (AWS keys, GitHub tokens, private key headers, Stripe/Slack
  keys, generic `key=`/`secret=` assignments) to catch exposed
  credentials before you push.
- **Composite health score** — a single 0-100 grade (A-F) blending secret
  safety, commit hygiene, branch hygiene, dependency freshness, and
  recent activity, so you know which of your repos needs attention first.
- **Commit quality analysis** — Conventional Commits compliance, subject
  length, imperative mood, and body presence, scored per commit.
- **Stale branch detection** — flags merged-but-not-deleted branches,
  long-abandoned branches, and branches badly diverged from main, with a
  keep/review/delete/merge recommendation for each.
- **Dependency freshness** — checks `package.json` and `requirements.txt`
  against live npm/PyPI registries.
- **GitHub PR/issue triage** — pulls open PRs and issues via the GitHub
  API and flags which have gone stale.

## When To Use This Skill

Use this when a user wants to audit one or more of their own Git
repositories: checking for accidentally committed secrets before a push,
getting an overview of repo health across many projects, cleaning up
stale branches, or triaging a GitHub backlog. This is a defensive,
local-first tool for maintaining your own code — it is not a scanning
or reconnaissance tool for third-party targets.

## Endpoint

MCP Server: `https://github.com/welove111/gitguard-skill/.netlify/functions/mcp`

POST a JSON body like `{"tool": "health_report", "repo_path": "."}`.

## Available Tools

| Tool | Description |
|------|-------------|
| `scan_secrets` | Entropy + pattern-based secret scan of a repo |
| `health_report` | Composite 0-100 health score for one repo |
| `multi_repo_dashboard` | Rank many local repos by health score |
| `commit_quality` | Conventional Commits compliance scoring |
| `stale_branches` | Branch staleness + keep/review/delete recommendation |
| `dependency_check` | npm/PyPI freshness check |
| `github_triage` | Open PR/issue staleness via GitHub API |

## Requirements

- Python 3.9+
- `git` CLI available on PATH
- `requests` (optional — only needed for dependency/GitHub checks; secret
  scanning and commit/branch analysis work fully offline without it)
- `GITHUB_TOKEN` environment variable (optional — raises GitHub API rate
  limits from 60/hour to 5,000/hour; not required for public repos)

## Support

GitGuard is free and open source. If it saved you time or caught something
useful, the project accepts voluntary support:

- Website: https://btc-vision.org
- BTC: `bc1qtpuhwl0vnhrch5p7e5469q2ed66hlyyvh8rtsn`
- ETH: `0xf03b429d4d85896a46dd7a64b5a8ab9f0bbb4ced`
- SOL: `3G5UZHFYN8hbv3aTZt6Lr7qqx4FTTkAyLJq34HjQLraz`
- Lightning: `welove@blink.sv`

## Links

- GitHub: https://github.com/welove111/gitguard-skill
- Website: https://btc-vision.org
