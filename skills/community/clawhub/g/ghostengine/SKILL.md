---
name: ghostengine
description: Sign a business up for GhostEngine and run its paid ads on Google, Meta, TikTok, and Reddit through the GhostEngine MCP server, within limits the owner approves.
version: 1.0.0
metadata:
  openclaw:
    homepage: https://ghostengine.ai
    envVars:
      - name: GHOSTENGINE_MCP_KEY
        required: false
        description: GhostEngine MCP API key (gemcp_...). Not needed to sign up; the signup flow returns one.
    primaryEnv: GHOSTENGINE_MCP_KEY
---

# GhostEngine

GhostEngine runs a business's paid ads on Google, Meta, TikTok, and Reddit from one place: launch, budget pacing, attribution, and incrementality tests. You reach it over MCP (streamable HTTP).

| Endpoint | Auth | Use |
|---|---|---|
| `https://api.ghostengine.ai/api/v1/mcp/signup` | none | Start a signup when there is no account or key |
| `https://api.ghostengine.ai/api/v1/mcp` | `Authorization: Bearer gemcp_...` or OAuth | Everything else |

Every tool description says what it needs. Read it before calling.

## 1. Get access

If `GHOSTENGINE_MCP_KEY` is set, use it and skip to step 2. If the person can sign in through your client's OAuth flow, that works too.

Otherwise, on the signup endpoint:

1. `start_signup` with the person's `email`, the `website` to advertise, your `agentName`, and optionally `companyName`. Store `requestId` and `claimToken` privately; the claim token is the only way to collect the key.
2. Tell the person to open the email from GhostEngine. They create an account or sign in, accept the terms, and choose read or write access and a daily spend limit. You never see their password or card.
3. Poll `get_signup_status` with `requestId` and `claimToken`, no more than once every 30 seconds. On `approved`, the response contains the API key **once**. Save it. `declined` or `expired` means stop; do not retry without the person asking.
4. To start a subscription, `create_payment_link` with `plan` (`core` or `pro`) and optionally `billingCycle`, then give the person the Stripe link. Never ask for card numbers in chat.

## 2. Connect ad accounts

- `get_integration_status` shows what is connected.
- Meta, TikTok, and Reddit are owned and billed by the business. `create_connect_link` with `platform` returns a single-use link; the person opens it and signs in to the platform. Check progress with `get_connect_link_status`.
- Google Ads is provisioned by GhostEngine; no link is needed.

## 3. Set up and launch

1. `configure_campaign` with `channels`, `totalBudgetUsd` for the whole flight, optional `funnelStages`, and optional `startDate`/`endDate` (omit both for a rolling 30-day flight). Custom flights run at least 72 hours and start in the future; a start today needs `startTime`. It sets aside the Google share of the budget in the wallet and is refused if the wallet is short (`top_up_wallet` first). Needs `confirm: true` and an `idempotencyKey`. Nothing launches yet. It is refused (`BUDGET_BELOW_PLATFORM_MINIMUMS`) when the budget is below every channel's daily minimum times the flight days, counted like the dashboard: a custom flight's start-to-end span rounded up to whole days. Its `budgetCheck` gives that minimum and whether the key's daily spend limit covers the launch, which commits the whole flight budget; if not, ask the person to raise the limit.
2. Targeting: `get_targeting` shows countries, language and any US areas. Change countries with `set_target_market`; target states, DMAs, cities or ZIPs with `search_target_locations`, `preview_target_locations`, then `set_target_locations`.
3. `generate_audiences`, then poll `get_audience_generation_status` (every 30 seconds at most) and review with `get_audience_summary`.
4. `get_pixel_status`. If `verifiedForLaunch` is false, `get_pixel_install_snippet`, have it installed, then `verify_pixel_install`. A pass is recorded, so launch sees the pixel as verified. To require specific conversion events (for example `Purchase` or `Lead`) before the pixel counts as verified, save them with `set_conversion_plan`.
5. Creative: `get_asset_specs`, `get_creative_inventory`; add images and videos with `register_asset_from_url`. GhostEngine measures each file and assigns it only to channels it fits. `generate_ad_text` writes copy from the website; save it with `save_text_assets`, then `confirm_creative_assets`, which refuses assets with missing copy, links or covers and says why. Change channels, links, UTMs, promotional dates or the optimization exclusion with `update_creative_asset`; remove an asset with `archive_creative_asset`.
6. `plan_campaign`, `get_launch_readiness`. Fix every blocker it lists. For Google it also checks what the Google keywords cost: `GOOGLE_SEARCH_BUDGET_BELOW_KEYWORD_MINIMUM` gives the daily budget they need, and `GOOGLE_SEARCH_KEYWORDS_UNAFFORDABLE` means no budget buys enough of them. Both block when Google is the only channel; with other channels they are warnings and Google's share goes to the others. Raise the budget, shorten the flight, or save keywords people search for (`save_text_assets` `googleAdText.keywords`).
7. `launch_campaign` with `confirm: true` and a fresh `idempotencyKey`. This commits real spend.
8. `get_launch_status` with the returned `jobId` until it completes; it says per channel whether the campaign was created and why not. Then `get_campaign_status` reads each platform live: every ad, whether it is delivering, and its review state. A `rejected` ad needs new creative or copy.

Setup and targeting changes are refused while campaigns are live. Pause first, or change the budget with `adjust_budget`. New creatives do not need a pause: `confirm_creative_assets` adds them to live campaigns. To change the thumbnail on live Reddit video ads, use `list_live_ads_for_video`, then `swap_live_ad_thumbnail` (undo with `undo_live_ad_swap`).

## 4. Run and measure

- Performance: `get_performance_report` returns every Performance tab KPI (spend, revenue, ROAS, conversions, CPA, AOV, conversion rate, visits, impressions, clicks, CTR, CPC, CPM, landing rate, visit rate, CPV) for all channels and per channel, with the change against the previous period and daily rows. Use it for any "how are we doing" question. Also `get_geo_performance`, `get_creative_performance`, `get_conversion_events`, `get_signal_health`; `get_campaign_performance` is raw platform-reported delivery by day.
- Attribution: `get_trueup_report` compares what each platform claims with what TrueUp verified against real purchases, with CPA on both bases and how matches were made. Also `get_attribution_summary`, `get_reconciliation_status`.
- Incrementality (Pro): `get_incrementality_results` for lift and iROAS; `get_incrementality_detail` for the ads running vs ads paused chart, markets, flight timeline, projected days to a confident read, test quality checks and lift history. Also `get_incrementality_status`, `get_geo_holdout_state`.
- What GhostEngine changed and why: `get_engine_decisions` (the dashboard's Engine Decisions feed), `get_optimization_ladder` (what each campaign optimizes for and what comes next), `get_optimization_log`, `get_policy_preview`.
- In apps that support MCP Apps (interactive views in the chat), `get_performance_report`, `get_trueup_report`, `get_incrementality_detail` and `get_campaign_status` also show as a report the person can read directly. Still summarize the numbers that answer the question in text.
- When reporting, say where numbers come from: conversions are TrueUp-verified, revenue is from the pixel, spend is platform-reported. Do not add platform-claimed conversions to verified ones. Do not claim a lift is real while its range crosses zero.
- `pause_flight` and `resume_flight` stop and restart the whole flight, the same as the dashboard Pause and Resume buttons. `resume_flight` is refused when the end date has passed or the budget is used up, and needs `confirm: true` and an `idempotencyKey`.
- `pause_campaign` and `resume_campaign` take a `campaignId` (from `get_campaign_status`) and optional `reason`. `resume_campaign` only works inside a live flight; use `resume_flight` for a paused one.
- `archive_campaign` permanently ends a paused campaign (`confirm: true`): archived on Meta and Reddit, removed on Google, deleted on TikTok. It cannot be undone, so only use it when the person asks to remove the campaign, not to stop it for now. Archiving the last campaign of a live flight also pauses the flight (`flightPaused: true`).

GhostEngine already shifts budget between channels and pauses weak creatives on its own. Do not fight it with repeated manual changes; read `get_optimization_log` first.

## 5. Budget and wallet

- `get_wallet_history` lists deposits, reservations, spend and refunds, how much is refundable now, and past refund requests. Refunds are requested in the dashboard (`billing`).
- `get_wallet_balance`. The wallet pays for Google Ads only; Meta, TikTok, and Reddit bill the business directly. `availableCents = 0` is normal for an active campaign; `reservedCents` is the money set aside for it.
- `adjust_budget` (`newTotalBudgetUsd`) and `top_up_wallet` (`amountUsd`) need the "add funds" permission, `confirm: true`, and an `idempotencyKey`. Both count against the key's daily spend limit. On a live flight a new budget is pushed to the platforms; on a paused flight it applies at `resume_flight`.
- `top_up_wallet` charges the saved card plus 2.9% + $0.30 processing. The person gets an emailed receipt. If the bank asks for verification, the person must add funds in GhostEngine themselves.

## 6. Things the person does in the dashboard

Some tasks are not tools on purpose: uploading customer lists, inviting teammates (Pro), changing the plan or card, account settings, and changing an agent's permissions or daily spend limit (`agent_access`). When the person asks for one of these, or for anything no tool covers, call `get_dashboard_link` with the matching `task` and show them `messageForUser`. It contains a direct link to the right screen.

## Rules

- Spend only within what the person approved. Ask before raising budgets or adding funds unless they told you to act on your own.
- Use a new `idempotencyKey` per intended action, and reuse it only to retry that same action.
- If a call is refused for scope, plan tier, or spend limit, tell the person what is needed (`get_dashboard_link` has the link: `agent_access` for permissions and the daily spend limit, `billing` for the card and wallet). Do not work around it.
- Never put API keys, claim tokens, or connect links anywhere public.
