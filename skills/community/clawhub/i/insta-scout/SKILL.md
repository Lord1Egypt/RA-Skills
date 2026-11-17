---
name: insta-scout
description: Instagram research without logging in or an API key. Search accounts and reels, browse hashtags, read any public profile, its posts, reels, stories and highlights, followers and following, similar accounts, tagged posts, post comments and likers. Use this skill for competitor research, influencer vetting, content ideas, or tracking what performs on Instagram.
---

# Insta Scout: Instagram Research

![Insta Scout: Instagram Research](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/insta-scout.gif)

Look inside any public Instagram account: profile and follower count, posts and reels with engagement, stories and highlights, who follows them, and similar accounts.

No Instagram account, no API key, no app to connect. Calls are paid from ClawLink credit, most for a fraction of a cent, and every new account starts with **$0.50 free**. Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=insta-scout).

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair | Step 3: Ask |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/setup-install.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/setup-pair.gif) | ![Ask](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/insta-scout.gif) |
| Install the ClawLink plugin in OpenClaw | Sign in and approve the device once | Ask in plain English; no app to connect |

## What You Can Ask

- “Look up National Geographic on Instagram”
- “Which of this account's reels got the most views?”
- “Find accounts similar to @glossier”
- “What's posted under #veganrecipes?”

## When to Use This Skill

Use it when the user wants public Instagram profiles, posts, reels, stories, hashtags or followers.

Do not use it for the user's own private accounts or for anything that posts, sends or changes data: these tools only read public information.

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│ Instagram        │
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

### Search

| Tool | What it returns | Price |
|------|-----------------|-------|
| `instagramdata_search_users` | Search public Instagram accounts by a keyword in their bio or captions | $0.00282 |
| `instagramdata_search_reels` | Search public Instagram reels by keyword: caption, views, likes, duration, author | $0.00282 |
| `instagramdata_hashtag_posts` | Public posts under an Instagram hashtag | $0.00282 |

### Accounts

| Tool | What it returns | Price |
|------|-----------------|-------|
| `instagramdata_user_profile` | Public Instagram profile by username: follower, following and post counts, bio, category, verified flag | $0.00282 |
| `instagramdata_user_posts` | Recent public posts of an Instagram account with likes, comments and captions | $0.00282 |
| `instagramdata_user_reels` | Recent public reels of an Instagram account with play counts | $0.00282 |
| `instagramdata_user_stories` | Stories an Instagram account has live right now (the last 24 hours): media type, time, link stickers, mentions | $0.003 |
| `instagramdata_user_highlights` | Story highlights pinned on an Instagram profile: id and title of each | $0.00282 |
| `instagramdata_highlight_items` | The stories inside one Instagram highlight: media type, date, duration, caption, link stickers | $0.00282 |
| `instagramdata_similar_users` | Accounts Instagram suggests as similar to a given account | $0.003 |

### Audience & Posts

| Tool | What it returns | Price |
|------|-----------------|-------|
| `instagramdata_user_followers` | A page of an Instagram account's followers (about 50): username, name, verified and private flags | $0.003 |
| `instagramdata_user_following` | A page of the accounts an Instagram account follows (about 50): username, name, verified and private flags | $0.003 |
| `instagramdata_tagged_posts` | Public posts other accounts tagged an Instagram account in: caption, likes, comments, author, location | $0.003 |
| `instagramdata_post_info` | One Instagram post or reel by URL: caption, media, likes, comments, author | $0.00282 |
| `instagramdata_post_comments` | Comments on an Instagram post or reel | $0.003 |
| `instagramdata_post_likers` | Accounts that liked an Instagram post or reel: username, name, verified and private flags | $0.003 |

## Recipes

### Benchmark a competitor

1. `instagramdata_user_profile` for followers.
2. `instagramdata_user_reels` and `instagramdata_user_posts` for engagement per post.
3. List their top 5 by views or likes, with format and caption hook.

## Code Examples

### A profile

```bash
clawlink_call_tool --tool "instagramdata_user_profile" \
  --params '{"handle": "natgeo"}'
```

### Reels

```bash
clawlink_call_tool --tool "instagramdata_user_reels" \
  --params '{"handle": "natgeo"}'
```

## Discovery Workflow

1. Call `clawlink_search_tools` with a short query (for example `instagram`); public-data tools show as connected for every user.
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

- Handles go without the @.
- Private accounts return only basic profile info.
- Stories exist for 24 hours; highlights stay.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Account is private | Only public accounts can be read. |
| `credit_exhausted` | The user's ClawLink credit is used up. Tell them to top up at https://claw-link.dev/dashboard/billing?utm_source=clawhub&utm_medium=referral&utm_content=insta-scout; do not retry. |
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


- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=insta-scout)
- [ClawLink pricing](https://claw-link.dev/pricing?utm_source=clawhub&utm_medium=referral&utm_content=insta-scout)
- [ClawLink docs: OpenClaw](https://docs.claw-link.dev/openclaw)
- [Verify the plugin](https://claw-link.dev/verify)

## Related Skills

- [Creator Scout](https://clawhub.ai/hith3sh/skills/creator-scout)
- [Transcribe Any Video](https://clawhub.ai/hith3sh/skills/transcribe-any-video)

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=insta-scout)**: connect OpenClaw to 1,000+ apps and public data, with no API keys.
