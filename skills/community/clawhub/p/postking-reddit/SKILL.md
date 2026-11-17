---
name: postking-reddit
description: Build a fit-scored subreddit pool, match content to the best communities with posting angles, and rewrite posts natively for Reddit.
license: MIT-0
compatibility: "Works with any MCP-compatible client connected to postking-mcp (local stdio or hosted at https://mcp.postking.app/mcp); the pking CLI is an optional fast path when a shell is available."
metadata:
  icon: https://raw.githubusercontent.com/bitsandtea/postking-skills/main/assets/icons/postking-reddit.svg
  category: marketing
---

# Reddit Growth

Grow a brand's presence on Reddit the way Reddit actually rewards: find the communities that fit, match a specific piece of content to the best ones with a tailored angle, and rewrite it in native Reddit voice — then hand it to the human to review and post.

## When to Use

Use this skill when a user wants to find subreddits that fit their brand, match an existing piece of content (blog post, post draft) to the best-fit communities with a posting angle, or get a Reddit-native rewrite of content before posting it themselves.

## When NOT to Use

Not for automatically publishing to Reddit — PostKing never posts on the brand's behalf; this skill only prepares review-ready drafts. Not for other-platform content generation or scheduling — that's `postking-social`/`postking`. Not for applying a saved voice profile in general — that's `postking-brand-voice` (this skill only consumes a `voiceId` from it).

## Minimal tool subset

This skill needs only these tools out of PostKing's 200+:

- `reddit_generate_pool` — crawl Reddit and build the brand's fit-scored subreddit pool from brand signals (async).
- `reddit_get_pool` — read the saved pool, sorted most-relevant first; each row includes `posting_style` and `no_promotion_reason`.
- `reddit_discover_subreddits` — search Reddit with explicit queries for candidates beyond the brand-signal pool (sync, 15 credits flat).
- `reddit_add_to_pool` — add chosen subreddits to the pool by name (sync, 0 credits).
- `reddit_remove_from_pool` — prune subreddits from the pool by name (sync, 0 credits).
- `reddit_suggest` — match a piece of content to up to 8 best-fit subreddits with posting angles (sync, 0 credits).
- `reddit_rewrite` — natively rewrite a post for a specific subreddit, optionally in a saved voice.
- `reddit_list_posts` — list previously rewritten Reddit posts.
- `list_voices` — get a `voiceId` to pass into `reddit_rewrite`.
- `get_job` — poll `reddit_generate_pool`.

Optional: `reddit_global_pool` — informational stats on the global known-subreddit dataset (not brand-specific). `get_post` — fallback poll if `reddit_rewrite` times out and returns a `postId` instead of a finished draft.

## Prerequisites

1. Authenticated with credits — see the `postking-getting-started` skill.
2. A brand already onboarded — see the `postking-getting-started` skill.

## Procedure

> "Find subreddits for us and turn this blog post into a Reddit post."

Async tools return `{ operationId, status }` — poll `get_job({ operationId })` until `state` is `completed`, `failed`, `partially_failed`, or `cancelled`.

1. **Build the pool.** `reddit_generate_pool({ brandId })` → async, poll `get_job`. Crawls Reddit and builds the brand's fit-scored subreddit pool from brand signals alone. Only needs to run once per brand (re-run occasionally to refresh). See "Manual subreddit curation" below for the alternative/companion path when the user wants to search in a specific direction instead of (or in addition to) this brand-signal crawl.
2. **Review the pool.** `reddit_get_pool({ brandId, top })` — the fit-scored subreddit pool, most relevant first. This is the brand-level match: no content needed yet. Each row's `posting_style` and `no_promotion_reason` fields are where you read a community's posting norms and promo tolerance — there is no separate "get subreddit rules" tool, it's surfaced here.
3. **Match content.** `reddit_suggest({ postId })` (an existing BlogArticle id) or `reddit_suggest({ title, content, detail: "medium" })` (pasted content) — returns up to 8 best-fit subreddits from the pool, each with 2–3 posting angles (angle type + tailored title + framing hook), `match_score`, `promotion_mode`, `buyer_intent`, `reason`, and `rule_to_watch`. Use `detail: "medium"` to get all angles plus `reason`/`rule_to_watch`. Requires the pool from step 1 to exist.
4. **(Optional) Pick a voice.** `list_voices({})` → get a `voiceId`, or use `"none"` for no voice. See the `postking-brand-voice` skill for details on managing voice profiles.
5. **Rewrite natively.** `reddit_rewrite({ subreddit, voiceId, sourcePostId, angle, length, variations })` (or `sourceContent` + optional `sourceTitle` instead of `sourcePostId`) — `subreddit` and `angle` should come from `reddit_suggest`'s results; `voiceId` is required. Usually returns the finished post inline; if it returns a `postId` instead, poll `get_post({ postId })` until `operationStatus` is `COMPLETED`.
6. **Review saved posts.** `reddit_list_posts({ brandId })` — cursor-paginated list of past rewrites, each with `outputData` (redditTitle, body, notes, wordCount, angle, length, subreddit).

**Important — Reddit is repurpose-to-review, not scheduled publishing.** PostKing does not post to Reddit on the brand's behalf. `reddit_rewrite` produces a review-ready native draft; the human copies it into Reddit and posts it themselves. Always surface the suggested `rule_to_watch` and `promotion_mode` to the user before they post, so they don't get a post removed for breaking a community's rules.

## Manual subreddit curation

`reddit_generate_pool` only finds subreddits from brand signals. Use this path instead (or alongside it) when the user wants to search in a specific direction — a competitor's niche, a product category, a named community they've heard of.

1. **Discover.** `reddit_discover_subreddits({ queries, context, minSubs })` — 1–8 explicit search queries, sync, 15 credits flat per call regardless of cache state. Pass `context` to disambiguate ambiguous terms (e.g. a brand name that also means something else). Returns candidates sorted by subscriber count, each flagged `already_in_pool` and `already_cached`. **This only returns candidates — it does not add anything to the pool.**
2. **Add.** `reddit_add_to_pool({ names })` — add the user's picks by name, 1–25 per call, free. Each name is resolved live against Reddit and merged into the pool. Partial success is normal, not an error: check the returned `failed` array — `retryable: true` means a transient lookup failure (retry the call), `retryable: false` means the subreddit itself can't be added (nonexistent/banned/private).
3. **Remove.** `reddit_remove_from_pool({ names })` — prune by name, 1–50 per call, free, case-insensitive. Brand-scoped unsubscribe only — it never touches the platform's global subreddit cache, so re-adding later is cheap. Names not currently in the pool come back in `notFound`, which is still success.

Note: `reddit_rewrite` auto-adds whatever subreddit(s) it targets to the pool at rewrite time, before the draft is even reviewed — so `reddit_add_to_pool` isn't a prerequisite for rewriting. Use it when curating the pool ahead of time, independent of any single rewrite, and use `reddit_remove_from_pool` afterward to prune anything a rewrite auto-added that the user doesn't want kept.

## CLI fast path

The `reddit_*` tools are MCP-only today — there is no `pking` CLI equivalent.

## Expected Output

A fit-scored subreddit pool for the brand, a shortlist of best-fit communities with tailored angles for a given piece of content, and a Reddit-native rewritten draft (with rule/promotion-mode guidance) ready for human review and posting.

## Pitfalls

- Empty pool / "no subreddit pool yet" on `reddit_suggest` or `reddit_rewrite` — run `reddit_generate_pool` and poll `get_job` to completion first.
- Expecting `reddit_discover_subreddits` to save results — it only returns candidates; call `reddit_add_to_pool` with the chosen names to actually add them.
- Subreddit not in pool on `reddit_rewrite` — pick a `subreddit` value from `reddit_get_pool` or a `reddit_suggest` result rather than typing one in.
- `INSUFFICIENT_CREDITS` — surface the `checkoutUrl` from the error envelope and stop, or hand off to the `postking-getting-started` skill's billing section (`billing_list_packs` → `billing_topup`).
- `RATE_LIMITED` — back off using the `retryAfter` value from the error envelope before retrying.
- `UNAUTHORIZED` — re-run the login flow described in the `postking-getting-started` skill.

## Verification

- `reddit_get_pool({ brandId })` should return a non-empty pool after `reddit_generate_pool` completes.
- `reddit_list_posts({ brandId })` should include the new draft after `reddit_rewrite` finishes.
