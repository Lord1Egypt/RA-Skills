---
name: meta-ads-control
description: Use this skill when the user wants to inspect, report on, create, update, pause, resume, budget, target, upload assets for, or troubleshoot Meta, Facebook, or Instagram ads via the Marketing API. It covers ad accounts, campaigns, ad sets, ads, creatives, ad images and videos, targeting search, batch reads, and Insights reports. Helpful for requests about Meta Ads Manager, ROAS or CPA reporting, launch workflows, creative rollout, audience setup, delivery issues, budget changes, or bulk ad operations.
license: MIT. See LICENSE.txt
compatibility: Requires Python 3 and outbound HTTPS access to graph.facebook.com. Best with OpenClaw and other AgentSkills-compatible agents. Reads META_ACCESS_TOKEN, META_AD_ACCOUNT_ID, META_API_VERSION, and META_GRAPH_BASE from the environment.
metadata: {"author":"OpenAI","version":"1.0.0","openclaw":{"emoji":"📣","primaryEnv":"META_ACCESS_TOKEN","requires":{"anyBins":["python3","python"]}}}
---

# Meta Ads Control

Use this skill for Meta Marketing API work. Prefer the bundled script because it gives structured JSON output, dry-run protection, retries, pagination, batch support, async Insights jobs, targeting search, and asset upload.

## Before you touch spend or delivery

1. Discover scope.
   ```bash
   python3 scripts/meta_ads.py accounts
   python3 scripts/meta_ads.py account
   ```
2. Confirm the intended ad account, currency, timezone, and writable objects.
3. For any change that can spend money, change delivery, or alter tracking:
   - prepare a short plan,
   - run `--dry-run`,
   - show the exact objects and fields to be changed,
   - wait for explicit user approval,
   - then rerun with `--confirm`.
4. Default new campaigns, ad sets, and ads to `PAUSED` unless the user explicitly asks to go live immediately.
5. After any write, do a read-after-write verification with `get`, `list`, or `request GET`.

## Authentication and environment

The script reads:

- `META_ACCESS_TOKEN` — required for live API calls
- `META_AD_ACCOUNT_ID` — optional default account, with or without `act_`
- `META_API_VERSION` — defaults to `v25.0`
- `META_GRAPH_BASE` — defaults to `https://graph.facebook.com`

If `META_ACCESS_TOKEN` is missing, help the user set it up first instead of guessing or fabricating API responses.

OpenClaw users can inject these values through skill config. See [OpenClaw notes](references/OPENCLAW.md).

## Fast path by task

### 1) Audit or diagnose an account

Start with the smallest read that answers the question.

```bash
python3 scripts/meta_ads.py account --fields id,name,account_status,currency,timezone_name,amount_spent,spend_cap
python3 scripts/meta_ads.py list campaigns --fields id,name,objective,status,effective_status,daily_budget,lifetime_budget
python3 scripts/meta_ads.py list adsets --fields id,name,campaign_id,status,effective_status,daily_budget,lifetime_budget,optimization_goal,bid_strategy
python3 scripts/meta_ads.py list ads --fields id,name,adset_id,campaign_id,status,effective_status,creative
```

Use `batch` when you need several small reads at once. Use minimal field sets first.

### 2) Performance reporting

Use `insights`. Start with a narrow level and date window. For large windows, many fields, or breakdowns, use `--async`.

```bash
python3 scripts/meta_ads.py insights act_123 --level campaign --date-preset last_7d
python3 scripts/meta_ads.py insights act_123 --level ad --fields ad_id,ad_name,spend,impressions,clicks,ctr,cpc,actions,action_values,purchase_roas --date-preset last_30d --async --fetch-all
```

If the user asks for conversions or ROAS, include `actions` and `action_values`. If the user asks for demographic or placement splits, use `--breakdowns`. If they ask for action-level splits, include `actions` and use `--action-breakdowns`.

### 3) Pause, resume, or archive objects

Prefer `set-status` for single-object changes.

```bash
python3 scripts/meta_ads.py set-status 120000000000000 PAUSED --dry-run
python3 scripts/meta_ads.py set-status 120000000000000 PAUSED --confirm
```

For bulk operations, create a JSON batch file and use `batch` after approval.

### 4) Create or update campaign structure

Create in order:

1. campaign
2. ad set
3. creative
4. ad

Use JSON payload files for any nested params. Start from templates in `assets/`.

```bash
python3 scripts/meta_ads.py create campaign --params-file assets/campaign-create.json --dry-run
python3 scripts/meta_ads.py create campaign --params-file work/campaign.json --confirm

python3 scripts/meta_ads.py create adset --params-file work/adset.json --dry-run
python3 scripts/meta_ads.py create adset --params-file work/adset.json --confirm

python3 scripts/meta_ads.py create adcreative --params-file work/adcreative.json --dry-run
python3 scripts/meta_ads.py create adcreative --params-file work/adcreative.json --confirm

python3 scripts/meta_ads.py create ad --params-file work/ad.json --dry-run
python3 scripts/meta_ads.py create ad --params-file work/ad.json --confirm
```

If assets are local files, upload them first with `upload`.

### 5) Targeting discovery

Never invent targeting IDs. Resolve them with targeting search first.

```bash
python3 scripts/meta_ads.py targeting-search --type adinterest --q "running"
python3 scripts/meta_ads.py targeting-search --type adgeolocation --q "Munich"
```

Then place the returned IDs and descriptors into the ad set `targeting` spec.

### 6) Unsupported or niche endpoints

Use the low-level `request` subcommand.

```bash
python3 scripts/meta_ads.py request GET /act_123/reachestimate --set targeting_spec=@work/targeting.json
python3 scripts/meta_ads.py request GET /120000000000000/previews --set ad_format=DESKTOP_FEED_STANDARD
```

For nested values, prefer `--params-file` or `@file.json` values over many inline `--set`s.

## Script reference

### Main entry point

```bash
python3 scripts/meta_ads.py --help
```

### Most useful subcommands

- `accounts` — list accessible ad accounts from the token
- `account` — read the default or provided account
- `list` — list campaigns, adsets, ads, creatives, audiences, assets, pixels, and more
- `get` — read a node or node edge
- `create` — create campaign, adset, adcreative, ad, customaudience, or any supported account edge
- `update` — update a node by ID
- `set-status` — convenience wrapper for `status`
- `insights` — sync or async reporting
- `targeting-search` — resolve targeting descriptors
- `upload` — upload to `adimages` or `advideos`
- `batch` — send Graph batch requests
- `request` — low-level escape hatch for any Graph path

## Rules for good agent behaviour

- Read before write.
- Use the smallest field set that answers the question.
- Prefer JSON payload files for nested data.
- Use `--fetch-all` only when the user actually needs all pages.
- Use `--async` for heavy Insights jobs.
- Pause on repeated 613 or 80004 rate-limit errors; reduce scope or add time between retries.
- Prefer `PAUSED` or `ARCHIVED` over destructive delete operations.
- Report money in both raw API units and human units when relevant. Budgets are usually in the smallest currency denomination.
- When writing budgets, verify account currency and timezone first.
- After any mutation, verify the live state with a follow-up read.
- If the request touches housing, employment, credit, social issues, elections, or politics, check [API guide](references/API-GUIDE.md) for special-category cautions before proceeding.

## Examples

### Quick 7-day account snapshot

```bash
python3 scripts/meta_ads.py batch --batch-file assets/batch-read-example.json
python3 scripts/meta_ads.py insights act_123 --level campaign --date-preset last_7d --fields campaign_id,campaign_name,spend,impressions,clicks,ctr,cpc,actions,action_values,purchase_roas
```

### Increase a budget safely

1. Inspect the current ad set.
2. Prepare an update payload with the new budget.
3. Dry-run it.
4. Ask for confirmation.
5. Apply and verify.

```bash
python3 scripts/meta_ads.py get 120000000000000 --fields id,name,status,effective_status,daily_budget,lifetime_budget
python3 scripts/meta_ads.py update 120000000000000 --params-file work/adset-budget.json --dry-run
python3 scripts/meta_ads.py update 120000000000000 --params-file work/adset-budget.json --confirm
python3 scripts/meta_ads.py get 120000000000000 --fields id,name,daily_budget,lifetime_budget,updated_time
```

### Upload an image and build a link ad

```bash
python3 scripts/meta_ads.py upload adimages --file creative.jpg --confirm
# Put the returned image_hash into work/adcreative.json
python3 scripts/meta_ads.py create adcreative --params-file work/adcreative.json --confirm
python3 scripts/meta_ads.py create ad --params-file work/ad.json --confirm
```

## References

- [API guide](references/API-GUIDE.md)
- [Field sets and reporting defaults](references/FIELDS.md)
- [Workflow playbook](references/WORKFLOWS.md)
- [Troubleshooting](references/TROUBLESHOOTING.md)
- [OpenClaw notes](references/OPENCLAW.md)
- Asset templates in `assets/`
- Example evals in `evals/evals.json`
