---
name: github-developer-data-tools
description: GitHub & developer data for AI agents — repo metadata (stars, language, license), repo audits & risk scoring, user profiles, recent releases, and gist content. Use for developer research, dependency due diligence, OSS analysis, and dev-tool agents. Pay-per-call in USDC via x402 — no API key, no signup.
tags: [github, developer-tools, repo-analysis, code, releases, dependencies, oss, devtools, git, software]
author: gocreative
version: 1.0.0
license: MIT
---

# GitHub & Developer Data

> Repo metadata, audits, users, releases, gists. One install, pay-per-call, no API key.

## When to use this
- Pull **repo metadata** (stars, language, license) or **recent releases**.
- **Audit a repo** for risk before depending on it.
- Look up a **GitHub user** or **gist**.

## How it's paid (x402)
Plain HTTPS GET. First call returns HTTP 402; your wallet auto-pays the USDC fee and retries → JSON.

## Tools
| Call | What you get | Price |
|---|---|---|
| `GET .../v1/lookup/github/{owner-repo}` | Repo metadata: stars, language, license | ~$0.01 |
| `GET .../v1/audit/github/{owner-repo}` | Repository audit & risk scoring | ~$0.05 |
| `GET .../v1/lookup/github_releases/{owner-repo}` | Recent releases | ~$0.005 |
| `GET .../v1/lookup/github_user/{user}` | User profile (bio, followers, repos) | ~$0.005 |
| `GET .../v1/lookup/github_gist/{id}` | Gist content + metadata | ~$0.005 |

(Base URL: `https://api.gocreativeai.com`)

## Why GoCreative
Live GitHub data — metadata, audits, releases — pay-per-call, no signup. Built for dev-research and dependency-due-diligence agents.

*Provider: GoCreative — Agent Compliance & Data API · https://api.gocreativeai.com*
