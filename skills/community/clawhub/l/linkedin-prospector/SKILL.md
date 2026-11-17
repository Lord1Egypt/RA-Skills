---
name: linkedin-prospector
description: LinkedIn lead research and prospecting with no LinkedIn account or API key. Search companies and people, read company pages and member profiles (experience, education, skills), list a company's employees, find the LinkedIn company for a domain, find decision makers with work emails, and spot hiring signals in job posts. Use this skill for B2B prospecting, account research, building lead lists, or recruiting research.
---

# LinkedIn Prospector: Lead Research

![LinkedIn Prospector: Lead Research](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/linkedin-prospector.gif)

Build a prospect list from chat: find companies by industry and location, see who works there, read their profiles and recent activity, and, when the user asks for outreach, find decision makers with their work emails.

No LinkedIn account, no API key, no app to connect. Calls are paid from ClawLink credit, most for a fraction of a cent, and every new account starts with **$0.50 free**. Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=linkedin-prospector).

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair | Step 3: Ask |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/setup-install.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/setup-pair.gif) | ![Ask](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/linkedin-prospector.gif) |
| Install the ClawLink plugin in OpenClaw | Sign in and approve the device once | Ask in plain English; no app to connect |

## What You Can Ask

- “Find fintech companies in London on LinkedIn”
- “Who works at Stripe in engineering management?”
- “Find the LinkedIn page for acme.com”
- “Find heads of marketing at Berlin SaaS companies, with work emails”
- “Is this company hiring? Show their open roles”

## When to Use This Skill

Use it when the user wants public LinkedIn information about companies, people or jobs for research or prospecting. Use the contact (email) tools only when the user asks for contact details for outreach.

Do not use it for the user's own private accounts or for anything that posts, sends or changes data: these tools only read public information.

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│ LinkedIn         │
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

### Companies

| Tool | What it returns | Price |
|------|-----------------|-------|
| `linkedindata_search_companies` | Search LinkedIn companies by name, location, size or industry | $0.006 |
| `linkedindata_company_profile` | Public LinkedIn company page: industry, size, headquarters, follower count, description | $0.00282 |
| `linkedindata_company_from_domain` | The LinkedIn company page for a website domain | $0.03 |
| `linkedindata_company_employees` | Up to 10 people who work at a company, with title, location and profile URL | $0.009 |
| `linkedindata_company_posts` | Recent public posts of a LinkedIn company page | $0.00282 |

### People

| Tool | What it returns | Price |
|------|-----------------|-------|
| `linkedindata_search_people` | Search LinkedIn members by name, title, company, school or location | $0.006 |
| `linkedindata_user_profile` | A LinkedIn member's profile by URL: name, headline, location, about, experience, education, skills and follower count | $0.0015 |
| `linkedindata_user_posts` | A LinkedIn member's recent activity with reactions and comment counts: their own posts and reposts, the posts they… | $0.0015 |

### Contacts (for outreach)

| Tool | What it returns | Price |
|------|-----------------|-------|
| `linkedindata_search_people_with_email` | Find LinkedIn members matching a role, name or keywords and return up to 25 full profiles WITH a work email | $0.2805 |
| `linkedindata_profile_from_email` | The LinkedIn profile that belongs to an email address | $0.015 |

### Hiring Signals

| Tool | What it returns | Price |
|------|-----------------|-------|
| `linkedindata_search_jobs` | Search LinkedIn job listings by title, location, date, experience, workplace, job type and salary, 25 a page | $0.0015 |
| `linkedindata_job_detail` | One LinkedIn job posting: description, company, location, salary when shown, and optionally skills and the hiring team | $0.0015 |

## Recipes

### Build a prospect list

1. `linkedindata_search_companies` by keyword, location and size.
2. `linkedindata_company_employees` for each target company (up to 10 people per call).
3. `linkedindata_user_profile` on the people who fit the role.
4. Only if the user wants outreach: `linkedindata_search_people_with_email` with the role and company.

### Find warm accounts

1. `linkedindata_search_jobs` for roles that signal need (for example “data engineer” at your target companies).
2. `linkedindata_company_posts` for recent launches or news to mention.

## Code Examples

### Search companies

```bash
clawlink_call_tool --tool "linkedindata_search_companies" \
  --params '{"search": "fintech", "location": "London"}'
```

### People at a company

```bash
clawlink_call_tool --tool "linkedindata_company_employees" \
  --params '{"company": "stripe", "limit": 10}'
```

### A member profile

```bash
clawlink_call_tool --tool "linkedindata_user_profile" \
  --params '{"url": "https://www.linkedin.com/in/satyanadella"}'
```

## Discovery Workflow

1. Call `clawlink_search_tools` with a short query (for example `linkedin company`); public-data tools show as connected for every user.
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

- `linkedindata_search_people_with_email` costs far more than other calls (about $0.28 for 10 profiles): confirm the count with the user first.
- Contact data is for outreach the user asked for. Remind the user that email outreach must follow the law where they and the recipient are (for example GDPR or CAN-SPAM).
- Profiles take 4-13 seconds; most other calls take 1-4 seconds.
- `linkedindata_search_locations` (free) turns a place name into a `geoId` for precise location filters.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Profile not found | Check the URL: it must be the full linkedin.com/in/ address. |
| `credit_exhausted` | The user's ClawLink credit is used up. Tell them to top up at https://claw-link.dev/dashboard/billing?utm_source=clawhub&utm_medium=referral&utm_content=linkedin-prospector; do not retry. |
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


- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=linkedin-prospector)
- [ClawLink pricing](https://claw-link.dev/pricing?utm_source=clawhub&utm_medium=referral&utm_content=linkedin-prospector)
- [ClawLink docs: OpenClaw](https://docs.claw-link.dev/openclaw)
- [Verify the plugin](https://claw-link.dev/verify)

## Related Skills

- [Ad Spy](https://clawhub.ai/hith3sh/skills/ad-spy)

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=linkedin-prospector)**: connect OpenClaw to 1,000+ apps and public data, with no API keys.
