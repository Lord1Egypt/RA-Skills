---
name: openclaw-twitter-post-engage
description: 'Search X/Twitter profiles, tweets, trends, and approved engagement actions through the AISA relay. Use when: the user asks for Twitter/X research, posting, likes, follows, or related workflows without sharing passwords. Supports read APIs, OAuth-gated posting, and follow or like operations.'
author: AIsa
version: 2.0.4
license: Apache-2.0
homepage: https://aisa.one
source: https://github.com/baofeng-tech/agent-skills-io/tree/main/targetSkills/openclaw-twitter-post-engage
user-invocable: true
primaryEnv: AISA_API_KEY
requires:
  bins:
  - python3
  env:
  - AISA_API_KEY
metadata:
  aisa:
    emoji: 🐦
    requires:
      bins:
      - python3
      env:
      - AISA_API_KEY
    primaryEnv: AISA_API_KEY
    compatibility:
    - openclaw
    - claude-code
    - hermes
  openclaw:
    emoji: 🐦
    requires:
      bins:
      - python3
      env:
      - AISA_API_KEY
    primaryEnv: AISA_API_KEY
---

# Twitter Post Engage

Runtime-focused skill package for Twitter/X search, posting, and engagement through the AISA relay.

## When to use

- The user wants Twitter/X research plus posting, liking, unliking, following, or unfollowing workflows.
- The task can use a Python client with `AISA_API_KEY` and explicit OAuth approval.
- The workflow needs a single package that covers read, post, and engagement actions.

## When NOT to use

- The user needs cookie extraction, password login, or a fully local Twitter client.
- The workflow must avoid relay-based network calls or media upload through `api.aisa.one`.
- The task needs undocumented secrets or browser-derived auth values.

## Quick Reference

- Required env: `AISA_API_KEY`
- Read client: `./scripts/twitter_client.py`
- Post client: `./scripts/twitter_oauth_client.py`
- Engage client: `./scripts/twitter_engagement_client.py`
- References: `./references/post_twitter.md`, `./references/engage_twitter.md`

## Setup

```bash
export AISA_API_KEY="your-key"
```

All network calls go to `https://api.aisa.one/apis/v1/...`.

## Capabilities

- Read user, tweet, trend, list, community, and Spaces data.
- Publish text, image, and video posts after explicit OAuth approval.
- Like, unlike, follow, and unfollow through the engagement client once authorization exists and `--confirm-engagement` is present.
- Reuse the current conversation context instead of local file-based conversation persistence.

## Common Commands

```bash
python3 scripts/twitter_client.py search --query "AI agents" --type Latest
python3 scripts/twitter_oauth_client.py authorize
python3 scripts/twitter_oauth_client.py post --text "Hello from AIsa" --confirm-public-write
python3 scripts/twitter_engagement_client.py like-latest --user "@elonmusk" --confirm-engagement
python3 scripts/twitter_engagement_client.py follow-user --user "@elonmusk" --confirm-engagement
```

## Posting and Engagement Workflow

- Use `./references/post_twitter.md` for post, reply, quote, and media-upload actions.
- Use `./references/engage_twitter.md` for likes, unlikes, follows, and unfollows.
- Obtain OAuth authorization before any write action.
- Treat plain posts, reply threads, and quote posts as separate modes: quote mode requires an explicit `--quote-tweet-url`, while multi-part text continues as a reply thread.

## Runtime Boundary

- The package is relay-based: read calls, OAuth requests, engagement actions, and approved media uploads go to `api.aisa.one`.
- The package is API-key-first: it requires `AISA_API_KEY` and does not ask for passwords, cookies, `CT0`, or other legacy secrets.
- CLI status and publish results report whether `AISA_API_KEY` is present, but do not print the key value.
- The package does not include cache sync, self-install logic, home-directory persistence, browser-cookie extraction, or external agent CLI wrappers.
- Browser opening is optional and not the default workflow; returning the authorization link is the preferred path for this release.
