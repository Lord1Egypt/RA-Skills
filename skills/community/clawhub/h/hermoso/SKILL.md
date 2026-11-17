---
name: hermoso
description: AI marketing agent and AI ad generator for your agent. Research winning ads, generate on-brand image and video ads, publish, schedule and run ad campaigns. No markup on models.
homepage: https://hermoso.ai/mcp/
---

# Hermoso: the marketing MCP

Hermoso is an AI marketing agent and AI ad generator an agent operates end to end: **research** the ads already winning in any market,
**create** on-brand image and video ads (including UGC-style talking-head spots with native speech),
**publish or schedule** to the user's own channels, and **build and read ad campaigns** on twelve ad platforms.
One MCP server, and every area works on its own: nothing requires another step first. No markup on models.

## Connect (once)
1. The user creates a free account at https://app.hermoso.ai and makes an agent key on the **MCP & CLI** tab, under **Terminal & API keys**
   (it starts with `hmk_`; direct link: https://app.hermoso.ai/?tab=api-keys, and Settings → API keys goes there too). Free accounts start with credits; renders are quoted before they run.
2. Add Hermoso as an MCP server in OpenClaw (**Settings → MCP → Add server**), either transport:
   - **Streamable HTTP**: URL `https://app.hermoso.ai/mcp`, header `Authorization: Bearer hmk_…`
   - **Stdio**: command `npx`, args `-y hermoso mcp`, environment `HERMOSO_TOKEN=hmk_…`
3. Verify it answers: `openclaw mcp doctor hermoso --probe`. Then call `hermoso_capabilities` (free) once; it returns the
   live model catalog with exact credit costs, which is what to quote before any render.

## The tools, by job
- **Research**: `find_competitors`, `pull_competitor_ads`, `research_ads`, `search_meta_ads`, `search_google_ads`,
  `search_linkedin_ads`, `search_tiktok`, `search_instagram`, `search_youtube`, `mine_angles`, `analyze_video`.
  Nearly free. Report the strongest hooks and angles and quote the real headlines.
- **Create**: `draft_brand` (onboard a brand from its website once) → `plan_ad` → `render_ad` (the Studio pipeline:
  brand, product photo, storyboard, native audio, read-back of the delivered file). `generate_image` / `generate_video`
  for raw model runs, `make_template_ad` for native formats, `make_explainer` for narrated explainers.
  Video renders take 2 to 6 minutes: `render_ad` returns a job id. Keep calling `get_job` until it reports done, and never
  describe a video before that.
- **Publish & schedule**: `post_to_meta` (Facebook + Instagram + Threads), `post_to_x`, `post_to_linkedin`, `post_to_tiktok`,
  `post_to_youtube`, `post_to_pinterest`, `post_to_reddit`, `post_to_bluesky`, `post_to_telegram`, `post_to_google_business`;
  `schedule_post`, `list_scheduled`, `reschedule_post`, `cancel_scheduled`. `upload_file` turns any local or external file
  into a URL these accept. Channels are connected by the user in the app (OAuth needs a browser); `list_connectors` says which are live.
- **Ads management**: `create_meta_campaign` / `_adset` / `_ad`, `create_google_ads_campaign` / `_ad_group` / `_ad`, and the
  TikTok, LinkedIn, Pinterest, Reddit, Microsoft, X and ChatGPT equivalents; `meta_insights`, `google_ads_report` and the
  per-platform reports. Everything is created **paused** and read back from the platform before it is described. Only the
  `set_*_ads_status` tools with `confirm:true` can make money move; never pass `confirm` unless the user asked to go live.

## Shell shortcuts (same account, via `exec`)
`npx -y hermoso auth login --token hmk_…`, then: `hermoso competitors <domain>`, `hermoso ads pull --company "<name>"`,
`hermoso research "<request>"`, `hermoso brand draft --domain <domain>`, `hermoso create --brand <name> --product "<product>" --format video`,
`hermoso generate image --prompt "…"`, `hermoso jobs get <id> --wait`, `hermoso credits`, `hermoso capabilities`. Add `--json` for machine output.

## Rules the agent should keep
- Quote credits (from `hermoso_capabilities`) before a render or a campaign build; the user pays per render, not per seat.
- A render is done when its URL comes back, not before.
- If a tool answers "not connected", ask the user to connect that channel in the app; the agent cannot complete OAuth.
- Nothing here spends ad budget without the explicit confirm flag.
