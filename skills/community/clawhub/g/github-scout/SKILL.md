---
name: github-scout
description: GitHub research without a GitHub token. Trending repositories and developers (daily, weekly, monthly, by language), any repository's details, and any developer's profile, repositories, pull requests, recent activity, contributions and followers. Use this skill for finding trending open source, vetting a developer or candidate, tracking a project, or tech scouting.
---

# GitHub Scout: Repos & Developers

![GitHub Scout: Repos & Developers](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/github-scout.gif)

Scout open source from chat: what is trending this week, any repo's details, and any developer's repos, pull requests and recent activity.

No GitHub account, no API key, no app to connect. Calls are paid from ClawLink credit, most for a fraction of a cent, and every new account starts with **$0.50 free**. Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=github-scout).

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair | Step 3: Ask |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/setup-install.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/setup-pair.gif) | ![Ask](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/github-scout.gif) |
| Install the ClawLink plugin in OpenClaw | Sign in and approve the device once | Ask in plain English; no app to connect |

## What You Can Ask

- “What's trending on GitHub this week?”
- “Show trending Rust repos today”
- “What has this developer been working on lately?”
- “Give me the details of this repo”

## When to Use This Skill

Use it when the user wants public GitHub repositories, trends or developer activity.

Do not use it for the user's own private accounts or for anything that posts, sends or changes data: these tools only read public information.

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│ GitHub           │
│   (User Chat)   │     │ (data tools) │     │ (public data)    │
└─────────────────┘     └──────────────┘     └──────────────────┘
         │                       │                       │
         │  1. Install plugin    │                       │
         │  2. Pair device once  │                       │
         │  3. Ask a question    │                       │
         │                       │  4. Fetch + trim      │
         │                       │  5. Charge credit     │
         ▼                       ▼                       ▼
   ┌──────────┐           ┌──────────┐           ┌──────────┐
   │  Answer  │           │  Credit  │           │ Results  │
   │ in chat  │           │ ($0.50)  │           │ as JSON  │
   └──────────┘           └──────────┘           └──────────┘
```

ClawLink holds the data-provider accounts. The user never pastes a key, and nothing is installed beyond the plugin.

## Install

Install the ClawLink plugin from ClawHub when the user asks for it:

```bash
openclaw plugins install clawhub:clawlink-plugin
```

The install applies to the running Gateway: do not restart it. The ClawLink tools appear on your next turn, so end this turn and tell the user: "ClawLink is installed. Reply ok and I will give you your pairing link." On the next turn call `clawlink_begin_pairing`, give the user the link, and after they approve call `clawlink_get_pairing_status`. Pairing happens once; after that every tool below works with no further setup.

## Tool Reference

Prices are what ClawLink charges per call, from the user's credit. The tool's own description (via `clawlink_describe_tool`) always shows the current price.

### Trending

| Tool | What it returns | Price |
|------|-----------------|-------|
| `githubdata_trending_repositories` | GitHub's trending repositories: rank, stars gained in the period, total stars, language, description | $0.00282 |
| `githubdata_trending_developers` | GitHub's trending developers: rank, name, and their popular repository | $0.00282 |

### Repos & Developers

| Tool | What it returns | Price |
|------|-----------------|-------|
| `githubdata_repository` | One public GitHub repository by URL: stars, forks, watchers, open issues, language, topics, license, homepage, last push | $0.00282 |
| `githubdata_user` | Public GitHub user or organization by handle: name, company, location, blog, bio, followers, following, public repo… | $0.00282 |
| `githubdata_user_repositories` | Public repositories of a GitHub user: stars, forks, language, topics, license, last push | $0.00282 |
| `githubdata_user_pull_requests` | Pull requests a GitHub user opened in any public repo: title, repo, state, date, link | $0.00282 |
| `githubdata_user_activity` | A GitHub user's public activity for one month, as on their profile: commits, repos created, PRs and issues opened,… | $0.00282 |
| `githubdata_user_contributions` | A GitHub user's contribution graph for one year: the total and the count for every day | $0.00282 |
| `githubdata_user_followers` | Accounts that follow a GitHub user, 30 per page | $0.00282 |

## Recipes

### Vet a developer

1. `githubdata_user` for the profile.
2. `githubdata_user_repositories` and `githubdata_user_contributions` for what and how often they ship.
3. `githubdata_user_pull_requests` for collaboration in other projects.

## Code Examples

### Trending this week

```bash
clawlink_call_tool --tool "githubdata_trending_repositories" \
  --params '{"since": "weekly"}'
```

### Trending in a language

```bash
clawlink_call_tool --tool "githubdata_trending_repositories" \
  --params '{"language": "rust", "since": "daily"}'
```

## Discovery Workflow

1. Call `clawlink_search_tools` with a short query (for example `github`); public-data tools show as connected for every user.
2. Call `clawlink_describe_tool` before the first call of a tool: it returns the parameters, defaults and price.
3. Treat the live catalog as the source of truth. If a tool named here is missing, say so; do not invent results.

## Execution Workflow

```
┌───────────────────────────────────────────────────────────┐
│  READ-ONLY, PAID PER CALL                                │
│  search → describe → call → summarise for the user       │
│                                                          │
│  Ask before: loops over many items, or a call that costs │
│  more than a few cents (the price is in the description) │
└───────────────────────────────────────────────────────────┘
```

1. Every tool here only reads public data; nothing is posted or changed.
2. Each call costs credit. Before looping over more than about ten items, or before a call priced above a few cents, tell the user what it will cost and ask.
3. A failed call is refunded automatically. Read the error's `hint`: it says what to change. Do not retry the same arguments unchanged.

## Notes

- `since` is daily, weekly or monthly.
- This reads public GitHub only; for the user's own repos connect the GitHub app.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| User not found | Check the username. |
| `credit_exhausted` | The user's ClawLink credit is used up. Tell them to top up at https://claw-link.dev/dashboard/billing?utm_source=clawhub&utm_medium=referral&utm_content=github-scout; do not retry. |
| `data_provider_unavailable` | ClawLink's data provider is down. Nothing was charged. Try again later. |
| `no_result` | The provider found nothing for these arguments. Nothing was charged. |
| `invalid_arguments` | A parameter is missing or malformed. Call `clawlink_describe_tool` and fix it. |

## Troubleshooting

### Tools not visible after install

1. The tools appear on the turn after the install, not in the same turn.
2. If they still do not appear, the OpenClaw tool profile may hide plugin tools. This is a config change for the OpenClaw owner; do not change the config yourself. Tell the user: "Your OpenClaw tool profile hides plugin tools. In the Control UI (or `~/.openclaw/openclaw.json`), add `clawlink-plugin` to `tools.alsoAllow`, then ask me again."
3. On OpenClaw versions before 2.0, the tool list can load only in a new chat: tell the user to send `/new` and ask again.

### A tool keeps failing with correct input

Report it with `clawlink_report_issue` (or `clawlink_call_tool --tool "CLAWLINK_REPORT_ISSUE"`) instead of retrying. Reports are free and reach the ClawLink team.

## Resources


- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=github-scout)
- [ClawLink pricing](https://claw-link.dev/pricing?utm_source=clawhub&utm_medium=referral&utm_content=github-scout)
- [ClawLink docs: OpenClaw](https://docs.claw-link.dev/openclaw)
- [Verify the plugin](https://claw-link.dev/verify)

## Related Skills

- [X Pulse](https://clawhub.ai/hith3sh/skills/x-pulse)

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=github-scout)**: connect OpenClaw to 1,000+ apps and public data, with no API keys.
