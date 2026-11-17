---
name: lazyads
description: Manage ad campaigns across Meta, Google, TikTok, LinkedIn, Reddit, Apple, Bing, ChatGPT, and Snapchat Ads via the hosted LazyAds MCP server.
  Bridge mode (BYOA) lets your agent create/edit/monitor campaigns without Lazy Ads AI.
  Full MCP (Starter+) also unlocks Lazy Ads AI builds, creatives, optimisation, and competitor intelligence.
tags: [advertising, ads, meta, google, tiktok, linkedin, reddit, apple, bing, chatgpt, snapchat, marketing, campaigns, mcp, byoa]
---

# LazyAds Skill

## What LazyAds Does
LazyAds is an ad management platform covering 9 platforms:
Meta (Facebook/Instagram), Google Ads, TikTok, LinkedIn, Reddit, Apple Ads, Bing Ads, ChatGPT Ads, and Snapchat Ads.
Instead of connecting each platform separately, LazyAds exposes everything
through a single MCP connection and API key.

Endpoint: `https://mcp.lazyads.ai/mcp` (Streamable HTTP, MCP 2026-07-28, stateless — no session
handshake). Send `Authorization: Bearer <api-key>` (or `X-API-Key`) on every request.
Per-key rate limits (1-minute window): BYOA 60, Starter 30, Growth 100, Scale 500, Enterprise 1000.
Exceeding returns 429 with `Retry-After`.

Two access modes:
- **Bridge (BYOA + every paid plan)** — 33 tools; your agent supplies strategy/copy; LazyAds is the connector to ad accounts and syncs stats to the dashboard. Never spends Lazy Ads AI credits.
- **Full MCP (Starter / Growth / Scale / Enterprise)** — 47 tools total; bridge plus 14 Lazy Ads AI tools (campaign build, chat, creative generation, optimisation, competitor AI, activity log).

The live catalog with descriptions is at https://lazyads.ai/mcp#tools.

## Setup
1. Sign up at https://lazyads.ai/pricing (BYOA for bridge-only, or Starter+ for full MCP)
2. Connect your ad platform accounts in the Lazy Ads dashboard (ChatGPT Ads can also be connected with `connect_chatgpt_ads` using an Ads Manager API key; every other platform uses dashboard OAuth or BYO-key cards)
3. Generate an API key at Settings → API (https://lazyads.ai/dashboard/settings?tab=api) and store it:
   ```
   # ~/.hermes/.env
   LAZY_ADS_API_KEY=la_your_api_key
   ```
4. Add the server to `~/.hermes/config.yaml` (see https://lazyads.ai/hermes):
   ```yaml
   mcp_servers:
     lazyads:
       url: "https://mcp.lazyads.ai/mcp"
       headers:
         Authorization: "Bearer ${LAZY_ADS_API_KEY}"
   ```
   Local development against a Lazy Ads checkout: `http://127.0.0.1:3100/mcp`.
5. Restart Hermes. Confirm with "Which ad platforms am I connected to?" (`list_platform_connections`).

## When to Use This Skill
Load when the user asks about:
- Their ad campaigns (performance, status, spend, ROAS, breakdowns)
- Creating, importing, pausing, scaling, or building campaigns
- Syncing live platform metrics into the Lazy Ads dashboard
- Ad-set level controls: budgets, bids, targeting, keywords
- Ad creative (browse/attach on any paid plan; generate/score on full MCP)
- Competitor ad activity (full MCP for Ad Library search and AI analysis)
- Whether an ad account can spend (`check_platform_billing`)

## Bridge MCP Tools (BYOA-safe, 33)
### Create and publish
- `create_manual_campaign` — create on Meta/Google/TikTok/LinkedIn/Reddit/Apple/Bing/ChatGPT/Snapchat + Lazy Ads (`aiManaged=false`; LinkedIn = campaign group)
- `create_manual_ad_set` — ad set / ad group with geo, age, gender, interests, keywords, custom audiences
- `create_manual_ad` — ads with copy/creative (Meta needs `create_meta_ad_creative` first; others take `imageUrl`)
- `create_meta_ad_creative` — Meta creative from a public image URL + copy
- `list_platform_audiences` — Meta/TikTok custom audiences to attach via `targeting.customAudienceIds`
- `update_manual_campaign` — name/objective/daily budget/end date on Lazy Ads + platform
- `duplicate_campaign` — clone a campaign into a new draft

### Import and sync
- `list_live_platform_campaigns` — list campaigns directly from a connected ad account
- `import_platform_campaign` — link an existing live campaign into Lazy Ads
- `sync_campaign_performance` / `sync_all_campaign_performance` — pull live metrics into the **unified Lazy Ads dashboard** (1–90 days)

### Manage live campaigns
- `list_campaigns` — Lazy Ads campaigns with status + latest synced metrics
- `get_ad_details` — full ad set + ad copy + creative details
- `pause_resume_campaign` / `pause_resume_ad_set` / `pause_resume_ad` — propagates to the live platform
- `set_campaign_budget` / `set_ad_set_budget` — daily budgets (ad-set budgets on Meta ABO, TikTok, LinkedIn, Reddit)
- `update_ad_set_targeting` — live audience targeting when the platform API allows it
- `update_ad_set_bid` — manual bid on LinkedIn, TikTok, ChatGPT, or Snapchat (null = LinkedIn auto bid)
- `add_ad_set_keywords` — Google / Bing / Apple search keywords with match types

### Analytics
- `get_campaign_performance` / `get_ad_spend_summary` / `get_breakdown_data` / `get_best_performing_creative` / `compare_campaigns`

### Creatives, audiences, and account
- `list_creatives` (lifetime ROAS/spend + predicted scores) / `attach_creative_to_ad`
- `list_audiences` — audiences currently used across ad sets
- `list_platform_connections` / `connect_chatgpt_ads` / `check_platform_billing`
- `get_recent_notifications`

### BYOA hierarchy workflow
1. `create_manual_campaign` (platform + objective + budget)
2. `create_manual_ad_set` (targeting / audiences)
3. Meta: `create_meta_ad_creative` → `create_manual_ad`; others: `create_manual_ad` with `imageUrl`
4. `sync_campaign_performance` so the Lazy Ads dashboard shows spend/ROAS without logging into each ads manager

## Full MCP Tools (Starter+, adds 14)
### Campaign build and automation
- `build_ai_campaign` — trigger a full Lazy Ads AI campaign build. Same options as the dashboard and REST `POST /api/v1/campaigns/build`: `platforms`, `dailyBudgetUsd`, `objectiveOverride`, `creativeMix` (`ai_decide` | `images_only` | `videos_only` | `images_and_videos` | `existing`), `preferredCreativeIds`, `preferredPagePostId`, `socialContentIds`, `referenceCreativeIds`, `customInstructions`, `skipCompetitorAnalysis`, `confirmNotPolitical`.
- `get_campaign_build_status` — poll build progress (2–5 minutes)
- `set_campaign_automation` — toggle Tracking (dashboard + analysis) and Management (optimizer may edit) on a campaign

### AI and optimisation
- `get_optimization_suggestions` — AI analysis with action recommendations
- `chat_with_lazy_ads` — ask the Lazy Ads assistant anything about the account (it can act)
- `get_creative_score` — predicted performance before launch
- `generate_creative` — AI image/video generation (credits + quota enforced)
- `get_audience_suggestions` — AI targeting from a description

### Competitor intelligence
- `list_competitors` / `search_competitor_ads` / `get_competitor_analysis` / `scan_competitor_ads`

### Activity
- `get_ai_activity` — recent Lazy Ads AI tasks
- `list_activity` — searchable user-facing log: credit charges and campaign/ad-set/ad changes

## Example Workflows

### BYOA: Manual Campaign Launch
"Create a Meta campaign named Summer Sale with OUTCOME_SALES objective and $40/day, then sync performance after it has data."
→ `create_manual_campaign` → `create_manual_ad_set` → `create_meta_ad_creative` → `create_manual_ad` → later `sync_campaign_performance`

### Import what is already running
"Bring my live Google campaigns into Lazy Ads."
→ `list_live_platform_campaigns` (platform=google) → `import_platform_campaign` per id → `sync_all_campaign_performance`

### Morning Campaign Review
"Check my campaigns — anything I should be worried about today?"
→ `list_campaigns` + `get_campaign_performance` (+ `get_breakdown_data` for the outlier)

### Pause Underperformers
"Pause any campaigns where CPA is more than 2× my target for 3+ days"
→ identify via performance tools, then `pause_resume_campaign` / `pause_resume_ad_set` / `pause_resume_ad`

### Full MCP: AI Campaign Build
"Build me a Meta campaign for my best-selling product with $50/day budget"
→ `build_ai_campaign` + `get_campaign_build_status` (Starter+ only)

## Pitfalls
- BYOA cannot call Lazy Ads AI tools (`build_ai_campaign`, `chat_with_lazy_ads`, `generate_creative`, `scan_competitor_ads`, etc.); the server answers with a plan error, not an OpenRouter error
- Bridge create/update requires a connected platform account in the dashboard; run `check_platform_billing` before launching spend
- Campaign builds (full MCP) take 2–5 minutes — poll with `get_campaign_build_status`
- Creative generation and AI builds consume monthly AI credits on AI plans
- LinkedIn and Reddit do not report revenue via API; ROAS can show 0 there
- Prefer `sync_all_campaign_performance` over one sync per campaign to stay under the per-minute rate limit
- Do not expect a sticky MCP session — the API key (and any protocol headers your client manages) goes on every call
- The REST API and outbound webhooks are Growth+; BYOA/Starter keys are MCP-only
