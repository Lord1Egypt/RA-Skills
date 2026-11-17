---
name: lingxi-github-daily-digest
category: automation
description: "Monitor GitHub Trending daily, use AI to analyze and summarize the hottest projects — with topic tagging, star growth prediction, and formatted digest output. Ideal for developers, investors, and tech enthusiasts who want to stay ahead of open-source trends."
version: 1.0
---

# lingxi-github-daily-digest

Automatically monitor GitHub Trending, analyze projects with AI, and produce a structured daily digest report.

## What It Does

1. Fetches today's GitHub Trending (all languages or specific language)
2. Uses AI to analyze each project: topic classification, innovation score, risk factors
3. Generates a structured markdown digest with rankings, insights, and recommendations
4. Supports scheduled daily runs via cron

## Usage

### Basic — Today's Trending Summary

```
Trigger: "Show me today's GitHub trending" or "GitHub 今日热点"
```

### Advanced — Filter by Language

```
Trigger: "Show me Python GitHub trending today"
```

### Full Digest — AI Analysis

```
Trigger: "Give me a full GitHub trending digest with AI analysis"
```

## Output Format

```markdown
# GitHub Trending Digest — YYYY-MM-DD

## 🏆 Top Projects Today

| # | Project | Stars | Language | Topics | Innovation Score |
|---|---------|-------|----------|--------|-----------------|
| 1 | owner/repo | +1.2k | Python | AI, ML, Open Source | ⭐⭐⭐⭐⭐ |

## 🔥 Hot Topics

- **AI/ML**: 12 projects trending
- **DevOps**: 8 projects trending

## 💡 Key Insights

- [AI analysis of the most significant trend]

## 🎯 Recommended Watch

- [Top 3 projects worth watching with reasoning]
```

## Installation

### Prerequisites

- `curl` or `wget` — for fetching GitHub Trending page
- `gh` CLI (optional) — for GitHub API calls
- OpenClaw with `browser-web-search` skill

### Install

```bash
clawhub install lingxi-github-daily-digest
```

### Configure

Set optional environment variables:
```bash
GITHUB_TRENDING_LANGUAGE=python      # filter by language (python, go, rust, etc.)
GITHUB_TRENDING_TIME_RANGE=daily     # daily, weekly, monthly
GITHUB_TOKEN=ghp_xxx                 # optional: higher API rate limit
```

## Cron Setup

To run daily at 9:00 AM:
```
Schedule: "0 9 * * *"
Command: Fetch trending → AI analysis → Save digest to ~/github-digest/YYYY-MM-DD.md
```

## AI Analysis Criteria

Each project is evaluated on:
- **Innovation Score** (1-5): Is this genuinely novel or just another wrapper?
- **Community Activity**: Recent commits, issues, PR velocity
- **Use Case Clarity**: Is the problem it solves immediately clear?
- **Risk Factors**: License issues, unmaintained, security concerns
- **Trend Potential**: Likelihood of continued growth

## Notes

- GitHub Trending is cached; avoid calling more than once per hour
- Use `--time-range weekly` for broader analysis on weekends
- For investment/competitive analysis, use `full` mode with GitHub API enrichment
