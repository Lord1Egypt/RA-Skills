---
name: juicer-brand-mentions
description: Find and alert on new mentions of a brand across Reddit, X and TikTok, plus its hashtags on Instagram, Facebook, LinkedIn and YouTube, using Juicer. Filters out posts that only share the name, drops the brand's own posts and sends a short daily digest to WhatsApp, Slack, Telegram or any connected chat. Use for "tell me when someone mentions us", "brand monitoring", "mention alerts", "who is talking about my company".
version: 1.0.3
metadata:
  openclaw:
    emoji: "🔔"
    homepage: https://developers.juicer.io/mcp-server
    primaryEnv: JUICER_API_KEY
    envVars:
      - name: JUICER_API_KEY
        required: false
        description: Optional. Only needed when the Juicer MCP server is not connected. Get one at https://www.juicer.io/developer
---

# Brand mentions with Juicer

Goal: every morning (or on demand) the user gets a short message with the new posts that are really about their brand, with links.

## Before the first run

1. Make sure Juicer is connected (see the `juicer` skill: MCP server with sign-in is best for daily runs).
2. Ask the user, in one message:
   - Brand name and any spellings (e.g. "Juicer", "Juicer.io").
   - Their own handles per network (e.g. X `@juicerio`, TikTok `@juicersocial`).
   - Branded hashtags, if any.
   - What the brand does, in a few words (e.g. "social media feed widget for websites"). This is how you tell real mentions from noise.
   - Where to send the digest (this chat, WhatsApp, Slack, Telegram) and what time.
3. Confirm each handle with `get_data_profiles` before using it. Read the returned `display_name`, `description` and `url`: an exact handle match can belong to someone else (the X account `@juicer` is an architect, not the company). Only keep handles whose description or website matches the brand.
4. Check credits with `get_account` and tell the user what one run costs (see below). For a big brand, also give the maximum: up to 5 pages per network, each page costing the network's credits again.

## Searches per run

| Network | Call | Credits |
|---|---|---|
| Reddit | `get_data_posts` term = brand name, `term_type: mentions` | 1 |
| X | `get_data_posts` term = `@handle`, `term_type: mentions` | 1 |
| TikTok | `get_data_posts` term = brand name, `term_type: mentions` | 3 |
| Instagram, Facebook, LinkedIn, YouTube, Bluesky | `get_data_posts` term = `#brandhashtag` | 3, 6, 3, 1, 1 |

X mentions work with a handle only, not a free keyword. Instagram, Facebook and LinkedIn have no keyword search: say so once in the first digest so the user is not surprised.

If the brand name is also a common word (Juicer, Apple, Notion), a keyword search on TikTok mostly returns the common meaning. Search the brand's own hashtag on TikTok instead (`#brandname`, `term_type: hashtag`), or a phrase that pairs the name with what the brand does.

Fetch pages until you cover the whole period of the digest (since the last run, or the last 7 days on the first run):

1. Fetch the first page per network and sort it by `post_created_at`.
2. If the oldest post on the page is still newer than the start of the period and `has_more` is true, fetch the next page (`cursor` from `meta.platforms[].next_cursor`). Every page costs the network's credits again.
3. Stop when the oldest post is older than the start of the period, when `has_more` is false, or after 5 pages on that network.
4. If you stopped at 5 pages, say how far back you got ("X: covered Oct 28-29, not the whole week") and offer more pages with the cost. Never present a partial period as the full week.

A small brand usually needs one page. A big brand (Nike, Coca-Cola) can fill a whole page in a few hours, so one page is not "this week". If the first page covers less than a day, 5 pages will not reach the week either: still fetch them, show the period covered per network in a table at the top, and suggest a Juicer feed with these searches so posts are collected continuously and the next digest is complete.

X mentions can come back as older popular posts rather than the newest ones. If a page has nothing inside the period, stop paging that network and say "X returned only older posts, so this week's X mentions may be missing" instead of "no mentions on X".

## Filter before reporting (the important part)

Keyword search matches the word, not the company. A real test for "juicer.io" on Reddit returned 114 posts and comments; only about 1 in 5 were about the company. The rest were kitchen juicers, Amazon deal lists and vintage ads.

For every post:

1. **Drop** posts older than the previous run (compare `post_created_at`). On the first run keep the last 7 days.
2. **Drop** posts from the brand's own handles; list them separately as "Our posts" only if the user asks.
3. **Keep** a post only if it is about this brand: it names the company in a way that fits what the brand does, links to its website or tags its handle. When unsure, drop it.
4. **Drop** duplicates (the same text cross-posted to several subreddits counts once; mention the extra places).
5. Keep a count of what was dropped and why.

## Digest format

Short, scannable, plain text that works in WhatsApp:

Template (fill every [ ] from the run, never from this example):

```
[Brand] mentions, [date] (since [last run time])
[N] new · [Network] [n] · [Network] [n]

1. [where, e.g. r/subreddit or @poster] · "[first line of the post]" · [n] comments
   [link]
2. ...

Needs a reply: #[n] ([why: question, complaint])
Skipped [n] posts that were about [what the noise was].
Searched: [each network and term]. Used [n] credits, [n] left.
```

- Lead with posts that ask a question or complain: those need a human reply.
- Always end with what was searched and what it cost.
- If nothing new: one line, "No new mentions since [time]", plus the searched line. Do not stay silent.

## Scheduling

Offer to make it daily with an OpenClaw Automation (scheduled job) that runs this skill at the user's chosen time and delivers to their chosen chat. Remember the last run time so the next digest only shows new posts.

## Errors

- `402 insufficient_credits`: tell the user the run was skipped, show the checkout link from the error and how many credits a run needs.
- `invalid_term` on a handle: the account was not found; ask the user to check it, do not guess another one.
- A network timing out: report it in the searched line and carry on with the others.
- Reddit returning `fetch_timeout` ("Reddit request timed out"): Reddit is slow at times. Retry it once at the end of the run (1 credit). If it fails again, say "Reddit could not be reached, so Reddit is not covered" and never report it as "no mentions on Reddit".
