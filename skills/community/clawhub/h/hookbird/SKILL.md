---
name: hookbird
description: Make scroll-stopping social posts with Hookbird — read the brand, write and score hooks, generate wall-of-text, slideshow and UGC videos in Studio, plan weeks of content, check competitor ads and trends, and schedule to TikTok, Instagram, LinkedIn, X and 30+ channels. Use for any social content, hook or posting request.
metadata: {"openclaw": {"primaryEnv": "HOOKBIRD_API_KEY", "requires": {"env": ["HOOKBIRD_API_KEY"]}}}
---

# Hookbird

Hookbird is hook-first social content: it reads a brand, writes and scores the first line that
stops the scroll, makes the content (Studio) and schedules it to 30+ channels. Its tools come from
the `hookbird` MCP server.

## When to use
The user wants social posts, hooks, TikTok/Reels/Shorts content, a content plan, competitor ads,
trends in their niche, benchmarks, or to schedule a post.

## Workflow (skip what the user already did)
1. **Brand** — `brand_profile`. If `found` is false, ask for the website and call `brand_read`
   with `url`, then call it again with `jobId` until `status` is `done` (each call waits ~20 s).
2. **Hooks** — `hooks_generate` (topic, audienceId from the profile, platform, count) returns
   scored hooks, best first. `hooks_score` scores the user's own hook with fixes and a rewrite.
   Quote scores as "x/100"; percentiles are *estimated*, say so.
3. **Make** — `studio_formats` (formats + credit prices) → tell the user the price and get a yes →
   `studio_generate` (formatId + hook) → `studio_status` until `done` (it waits up to 25 s per call).
   Outputs are media-library files with URLs. `credits_balance` shows what is left.
   "The usual" or a named recipe: `studio_recipes` lists the saved ones, pass its id as `recipeId`
   to `studio_generate` (its format and settings are used; anything you pass yourself wins).
4. **Schedule** — `integrationList` → `integrationSchema` (rules for that channel) →
   `integrationSchedulePostTool` with the Studio outputs as attachments, after the user confirms
   text, media, channel and time.

Weeks at once: `strategy_plan` with `action: "create"` (audience, channels, cadence, weeks) builds
a calendar of hooks + formats and draft posts; `action: "get"` reads plans back.
Research: `radar_ads` (a competitor's running ads and for how long), `radar_trends` (hashtags,
sounds, creators), `benchmarks` (the account vs its niche). Results: `posts_stats` (views, likes,
comments and shares of published posts), `sales_overview` (what posts sold, when a store is connected).
For a weekly routine, use the `hookbird-autopilot` skill.

## Rules
- Only Studio generations cost credits; hooks, brand, plans, Radar and benchmarks are free.
- Never generate without confirming the credit price, never publish without confirmation.
- Never invent ads, trends or numbers that a tool did not return; when a source is off the tool
  says why — pass that on.

## Setup
Add the `hookbird` MCP server: `https://app.hookbird.ai/mcp-oauth-dynamic` (OAuth), or
`https://app.hookbird.ai/api/mcp` with header `Authorization: Bearer $HOOKBIRD_API_KEY` (key in Hookbird → Agents).
Setup per agent: https://hookbird.ai/agents
