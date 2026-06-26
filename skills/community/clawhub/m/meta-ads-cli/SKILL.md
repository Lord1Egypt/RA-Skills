---
name: meta-ads-cli
version: 2.1.0
description: Control Meta/Facebook/Instagram ads through Meta's official `meta ads ...` CLI. Use for read-only audits, reporting, safe planning, and approved one-step mutations of campaigns, ad sets, ads, creatives, catalog/product assets, datasets/pixels, and insights. The skill is agent-agnostic and designed for shell-capable agents.
license: MIT. See LICENSE.txt
homepage: https://developers.facebook.com/documentation/ads-commerce/ads-ai-connectors/ads-cli/ads-cli-overview
compatibility: Shell-capable agents. Guard script requires Python 3.9+. Official Meta Ads CLI package requires Python 3.12+.
required_env_vars:
  - ACCESS_TOKEN
  - AD_ACCOUNT_ID
optional_env_vars:
  - BUSINESS_ID
  - META_ADS_AGENT_LOG
primary_credential: Meta Marketing API access token supplied through ACCESS_TOKEN
capability_signals:
  - requires-sensitive-meta-credentials
  - can-affect-ad-spend
  - can-modify-ad-assets
  - local-command-execution
install_spec: requirements-meta-ads-cli.txt
provenance: resources/provenance.json
metadata: {"author":"community-generated skill template; not an official Meta package","source":"user-provided meta-ads-cli skill revision","primary_cli":"meta ads","official_cli_package":"meta-ads==1.0.1","wrapped_cli":"scripts/meta_ads_agent.py","risk_model":"read-plan-approve-write-verify","approval_required_for":["create","update","delete/remove/unshare","budget-or-bid-change","status-active-or-activate","catalog-or-dataset-connection","creative-or-media-upload"],"logging_default":"disabled"}
---

# Meta Ads CLI skill

Use this skill when an AI agent needs to manage Meta ads from a terminal. The agent should use Meta's official CLI as the source of truth and should not reimplement the Marketing API unless the user explicitly asks for a lower-level workaround.

The command family is:

```bash
meta ads <resource> <action> [options]
```

Common resources include `adaccount`, `campaign`, `adset`, `ad`, `creative`, `catalog`, `page`, `product-set`, `product-item`, `product-feed`, `dataset`, and `insights`.

## Install and verify

Use the pinned install spec in this skill. Do not install an unpinned CLI package for production ad-account work.

```bash
python3.12 -m pip install -r requirements-meta-ads-cli.txt
meta --help
meta ads --help
meta auth status
```

Expected credentials:

```bash
export ACCESS_TOKEN=<meta-access-token>
export AD_ACCOUNT_ID=act_<ad-account-id>
# Optional when needed by catalog/dataset/page/business operations:
export BUSINESS_ID=<business-id>
```

Use a token limited to the intended ad accounts and tasks. Use read-only access for reporting where possible. Use a token with write authority only for approved mutation work.

## Default execution path

Use the guard script for all commands unless the user explicitly asks for raw CLI execution.

```bash
python3 scripts/meta_ads_agent.py doctor
python3 scripts/meta_ads_agent.py classify -- meta ads campaign list
python3 scripts/meta_ads_agent.py run -- meta ads campaign list --limit 25
```

The guard script:

- appends `--output json` for `meta ads` commands when no output format is provided;
- refuses non-`meta ads` commands;
- blocks token/secret arguments so credentials stay in the environment;
- blocks writes, unknown actions, budget changes, activation, and destructive actions without specific approval;
- keeps persistent logging disabled by default.

## Non-negotiable operating rules

1. Read before write. Inspect the relevant object, account, and recent performance before changing anything.
2. Never guess IDs. Resolve account, campaign, ad set, ad, creative, page, dataset/pixel, catalog, product set, and product item IDs through the CLI or from user-provided values.
3. Prefer JSON. Use machine-readable output for analysis and only present tables or summaries after parsing.
4. No spend-affecting change without explicit approval. A generic “yes” is not enough; approval must name the action, object/account, and key values.
5. Never activate by accident. New or modified objects should remain paused unless the user explicitly asks to activate and reviews the object.
6. One write step at a time. Run one mutation, verify it, then continue. Do not batch multiple creation/update steps unless the user has approved a controlled automation plan.
7. Keep secrets out of chat, commands, files, and logs. Do not print tokens, `.env` contents, cookies, app secrets, or debug output containing them.
8. Treat special or regulated categories conservatively. Housing, employment, credit, social issues, elections, politics, health, financial services, minors, and sensitive audiences require extra review.

## Risk gates

Read-only commands may run after auth/account checks:

```bash
python3 scripts/meta_ads_agent.py run -- meta ads insights get --date-preset last_7d --fields spend,impressions,clicks,ctr
```

Ordinary writes require specific approval:

```bash
python3 scripts/meta_ads_agent.py run \
  --approved "User approved pausing ad 120000000000000 in account act_123456" \
  -- meta ads ad update 120000000000000 --status PAUSED
```

Budget changes require the budget flag:

```bash
python3 scripts/meta_ads_agent.py run \
  --approved "User approved changing campaign 120000000000000 daily budget to 5000 minor units in account act_123456" \
  --allow-budget \
  -- meta ads campaign update 120000000000000 --daily-budget 5000
```

Activation requires the activation flag:

```bash
python3 scripts/meta_ads_agent.py run \
  --approved "User approved activating campaign 120000000000000 in account act_123456 after review" \
  --allow-active \
  -- meta ads campaign update 120000000000000 --status ACTIVE
```

Delete/remove/unshare requires the destructive flag:

```bash
python3 scripts/meta_ads_agent.py run \
  --approved "User approved deleting paused creative 120000000000000 in account act_123456" \
  --allow-destructive \
  -- meta ads creative delete 120000000000000
```

## Agent workflow

For read-only analysis:

```text
1. Run doctor/auth/account check if access is uncertain.
2. List or get the relevant objects.
3. Query insights with an explicit date range or date preset.
4. Summarise findings with date range, fields, caveats, and recommendations.
5. Separate recommendations from actual changes.
```

For any mutation:

```text
1. Read current object state and recent performance.
2. Present the exact command, account/object IDs, before value, after value, risk, and verification command.
3. Wait for specific approval.
4. Run one guarded command.
5. Verify the changed object.
6. Report object IDs touched, before/after, what remains paused/not live, and any follow-up needed in Ads Manager.
```

## Common tasks

### Account snapshot

```bash
python3 scripts/meta_ads_agent.py run -- meta ads adaccount current
python3 scripts/meta_ads_agent.py run -- meta ads campaign list --limit 50
python3 scripts/meta_ads_agent.py run -- meta ads insights get --date-preset last_7d --fields spend,impressions,clicks,ctr,cpc,cpm,conversions
```

### Performance triage

Fetch insights for the requested level and date range, then recommend actions. Do not pause or change budgets until the user approves a specific command.

```bash
python3 scripts/meta_ads_agent.py run -- meta ads insights get --date-preset last_7d --fields campaign_id,campaign_name,spend,impressions,clicks,ctr,cpc,cpm,conversions,cost_per_conversion
```

### Safe pause

Before pausing, get the object and recent insights. After pausing, verify status.

```bash
python3 scripts/meta_ads_agent.py run -- meta ads ad get <AD_ID>
python3 scripts/meta_ads_agent.py run -- meta ads insights get --ad_id <AD_ID> --date-preset last_7d --fields spend,impressions,clicks,conversions
python3 scripts/meta_ads_agent.py run --approved "User approved pausing ad <AD_ID> in account <AD_ACCOUNT_ID>" -- meta ads ad update <AD_ID> --status PAUSED
python3 scripts/meta_ads_agent.py run -- meta ads ad get <AD_ID>
```

### Paused launch

Create launch plans as reviewable commands, but execute one write at a time. Default every created object to `PAUSED` if the CLI supports a status flag. Do not activate the campaign, ad set, or ad unless the user approves activation separately.

Suggested sequence:

```text
1. Verify account, page, destination URL, catalog/dataset needs, objective, budget currency/minor units, schedule, and special ad categories.
2. Create campaign as paused; verify returned ID.
3. Create ad set as paused; verify returned ID.
4. Create creative; verify returned ID and preview where possible.
5. Create ad as paused; verify returned ID.
6. Summarise all IDs and tell the user what is still paused.
```

## Plans and templates

Plan files are JSON command lists for review. `run-plan` is read-only by default; for writes, lint the plan and then run one approved write command at a time.

```bash
python3 scripts/meta_ads_agent.py lint-plan templates/read-report-plan.json
python3 scripts/meta_ads_agent.py run-plan templates/read-report-plan.json
```

Use `--allow-write-plan` only in a controlled environment where the user has already reviewed the plan, the ad account is correct, and the plan contains at most one write step unless explicitly marked otherwise.

## Logging

The guard does not persist a run log by default. To keep a redacted local JSONL audit trail, set a controlled path:

```bash
export META_ADS_AGENT_LOG=.meta-ads-agent/runs.jsonl
# or per command:
python3 scripts/meta_ads_agent.py run --log-file .meta-ads-agent/runs.jsonl -- meta ads campaign list
```

Delete or protect logs when working with sensitive accounts. Logs may contain account IDs, object IDs, command names, and redacted result metadata.

## Failure handling

If a command fails:

1. Do not retry mutations blindly.
2. Read the object/account state before deciding whether anything changed.
3. Check `meta ads <resource> <action> --help` for the installed CLI syntax.
4. For auth errors, check `ACCESS_TOKEN`, `AD_ACCOUNT_ID`, token permissions, app/business asset assignment, and token expiry.
5. For rate limits or API errors, reduce scope, wait, or use smaller date ranges; do not parallelise writes.

## Output format for the user

For reporting, include:

```text
- what was queried
- ad account/object IDs when relevant
- date range and attribution assumptions
- top findings with numbers
- caveats about missing, zero, delayed, or odd metrics
- recommendations separated from changes actually made
```

For writes, include:

```text
- exact object IDs touched
- before/after values
- command run, with secrets redacted
- verification result
- whether anything is live or still paused
- unresolved issues or follow-up needed in Ads Manager
```
