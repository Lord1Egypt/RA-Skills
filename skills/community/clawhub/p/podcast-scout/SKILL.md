---
name: podcast-scout
description: Podcast research on Spotify without an account or API key. Search podcasts and episodes, read a show's details, and list its episodes with release dates and lengths. Use this skill for guest research, finding podcasts to pitch, tracking a show's release schedule, or summarising what a podcast covers.
---

# Podcast Scout: Podcast Research

![Podcast Scout: Podcast Research](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/podcast-scout.gif)

Research podcasts from chat: find shows on any topic, read a show's details, and list its latest episodes with dates and lengths.

No Spotify account, no API key, no app to connect. Calls are paid from ClawLink credit, most for a fraction of a cent, and every new account starts with **$0.50 free**. Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=podcast-scout).

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair | Step 3: Ask |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/setup-install.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/setup-pair.gif) | ![Ask](https://raw.githubusercontent.com/ClawLink-HQ/clawhub-assets/main/podcast-scout.gif) |
| Install the ClawLink plugin in OpenClaw | Sign in and approve the device once | Ask in plain English; no app to connect |

## What You Can Ask

- “What are the latest Lex Fridman Podcast episodes?”
- “Find podcasts about bootstrapped SaaS”
- “How often does this show release episodes?”
- “Which shows has this guest appeared on?”

## When to Use This Skill

Use it when the user wants podcast shows or episodes.

Do not use it for the user's own private accounts or for anything that posts, sends or changes data: these tools only read public information.

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│ Spotify podcasts │
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

### Podcasts

| Tool | What it returns | Price |
|------|-----------------|-------|
| `spotifydata_search` | Search Spotify for tracks, artists, albums, playlists and podcasts | $0.00282 |
| `spotifydata_podcast` | A Spotify podcast (show) by URL | $0.00282 |
| `spotifydata_podcast_episodes` | Episodes of a Spotify podcast by URL | $0.00282 |

## Recipes

### Find shows to pitch

1. `spotifydata_search` for the topic.
2. `spotifydata_podcast_episodes` on each show to check it is active (recent release dates).
3. List active shows with their cadence.

## Code Examples

### Episodes

```bash
clawlink_call_tool --tool "spotifydata_podcast_episodes" \
  --params '{"url": "https://open.spotify.com/show/2MAi0BvDc6GTFvKFPXnkCL"}'
```

### Search

```bash
clawlink_call_tool --tool "spotifydata_search" \
  --params '{"query": "bootstrapped saas podcast"}'
```

## Discovery Workflow

1. Call `clawlink_search_tools` with a short query (for example `podcast`); public-data tools show as connected for every user.
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

- Episode lengths come in milliseconds; convert them for the user.
- Use the open.spotify.com/show URL.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Show not found | Search first and use the URL from the result. |
| `credit_exhausted` | The user's ClawLink credit is used up. Tell them to top up at https://claw-link.dev/dashboard/billing?utm_source=clawhub&utm_medium=referral&utm_content=podcast-scout; do not retry. |
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


- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=podcast-scout)
- [ClawLink pricing](https://claw-link.dev/pricing?utm_source=clawhub&utm_medium=referral&utm_content=podcast-scout)
- [ClawLink docs: OpenClaw](https://docs.claw-link.dev/openclaw)
- [Verify the plugin](https://claw-link.dev/verify)

## Related Skills

- [Music Intel](https://clawhub.ai/hith3sh/skills/music-intel)
- [Transcribe Any Video](https://clawhub.ai/hith3sh/skills/transcribe-any-video)

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=podcast-scout)**: connect OpenClaw to 1,000+ apps and public data, with no API keys.
