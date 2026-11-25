---
name: hookbird-autopilot
description: Run a brand's TikTok and Instagram week after week with Hookbird. Each week it reads what is trending in the niche, writes and scores hooks, makes the posts in Hookbird Studio, schedules them after one approval, then learns from what sold and what got views. Use when someone asks an agent to run, grow or automate their social content, TikTok, Reels or Shorts.
metadata: {"openclaw": {"primaryEnv": "HOOKBIRD_API_KEY", "requires": {"env": ["HOOKBIRD_API_KEY"]}}}
---

# Hookbird autopilot

You run the owner's short-form content as a weekly loop: **research → hooks → make → approve → schedule → learn**.
Hookbird does the work through its MCP tools. You decide what to try next and keep a log so every week is better
than the last. The owner approves once a week; you never spend credits or publish without that approval.

## Setup (once)

1. Connect the Hookbird MCP server: `https://app.hookbird.ai/mcp-oauth-dynamic` (OAuth), or
   `https://app.hookbird.ai/api/mcp` with header `Authorization: Bearer $HOOKBIRD_API_KEY`
   (key in Hookbird → Agents). Setup per agent: https://hookbird.ai/agents
2. `brand_profile`. If `found` is false, ask for the website and call `brand_read` with `url`, then again with
   `jobId` until `status` is `done`.
3. `integrationList`: note the TikTok and Instagram channel ids. If none is connected, ask the owner to connect
   them in Hookbird first.
4. Ask the owner, once: posts per week, channels, monthly credit budget, topics or claims to avoid, and when they
   want the weekly approval (for example Sunday evening). Write the answers at the top of `hookbird-log.md`.

## The weekly loop

### 1. Learn from last week
- Read `hookbird-log.md`: last week's posts, hooks, formats and results.
- `posts_stats` (last 14 days, or `postIds` from the log): views, likes, comments and shares of each published
  post, live from each network. If your tool list has no `posts_stats`, ask the owner for the numbers (or a
  screenshot of TikTok Studio) instead.
- `sales_overview` (when a store is connected): which posts, formats and hooks sold. Sales beat views.
- `benchmarks`: the account's last 30 days against its niche median and top 10%.
- Write 3 lines in the log: what worked, what flopped, what to try next.

### 2. Research
- `radar_trends` (period 7): hashtags, sounds, creators and top posts in the niche and market.
- `radar_ads` for 1-2 competitors: the ads that have run longest are the ones that make money.
- Never invent a trend or a number that a tool did not return.

### 3. Hooks
- `hooks_generate` for the week's topics (pass the audience from `brand_profile`). Keep the best.
- Last week's winning hook family gets 2-3 new variations. A flop family gets dropped.
- `hooks_score` on any hook the owner wrote. Quote scores as "x/100"; percentiles are estimates, say so.

### 4. Plan and quote
- `strategy_plan` with `action: "create"` (channels, cadence, 1 week) gives dated draft posts. Or build the week
  yourself from the hooks.
- `studio_formats` for the price of each format. `credits_balance` for what is left.
- Send the owner one message: the week's posts (date, channel, format, hook), the total credit price and the
  balance. Mix formats: cheap slideshows and walls of text to test hooks, one video for a proven hook.

### 5. Make (after the owner's yes)
- `studio_generate` per post (`formatId` + `hook`, or `recipeId` from `studio_recipes` for "the usual"), then
  `studio_status` until `done`.
- Show the finished media. Fix what the owner asks before scheduling.

### 6. Schedule
- `integrationSchema` for each channel's rules, then `integrationSchedulePostTool` with the Studio outputs as
  attachments, at the agreed times.
- When a store is connected and the post sells a product: `sales_bio_link` (tracked link) or `sales_code`
  (discount code, admins only) so its sales count.
- Log each post: id, date, channel, format, hook, credits.

## Rules

- Only Studio spends credits; hooks, brand, plans, Radar, benchmarks, post stats and sales are free.
- One approval per week covers the posts and the credit total it showed. Anything new needs a new yes.
- Never publish without approval, never exceed the monthly budget, never make health, money or result claims the
  brand cannot prove.
- Judge a hook on 2-3 posts, never one: the same post can get 100x different views by chance.
- If a tool says a source is off, tell the owner why instead of guessing.

## hookbird-log.md (keep it in your workspace)

```
# Settings: 5 posts/week · TikTok + Instagram · 600 credits/month · approval Sunday 20:00
## Week of 2026-11-23
| Post id | Date | Channel | Format | Hook | Credits | Views | Saves | Sales |
Worked: ... / Flopped: ... / Next: ...
```
