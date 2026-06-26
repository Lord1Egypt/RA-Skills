# API Guide

This skill targets the Meta Marketing API, which sits on top of the Graph API. The API is broad, so the bundled script exposes both convenience subcommands and a low-level `request` escape hatch.

## Current assumptions

- Default API version: `v25.0`
- Default Graph base: `https://graph.facebook.com`
- Authentication: bearer token in `META_ACCESS_TOKEN`

Always pin a version. Do not assume unversioned behaviour will stay stable.

## Object model

The core hierarchy is:

1. **Ad account** — top-level container and billing boundary
2. **Campaign** — business objective and high-level budget strategy
3. **Ad set** — schedule, bid strategy, optimisation goal, audience, placements, and usually budget
4. **Ad** — the delivery unit inside an ad set
5. **Ad creative** — the rendering payload attached to an ad

Practical rule: if you are launching a new structure, create in this order:

1. campaign
2. ad set
3. creative
4. ad

## Auth and permissions

### Recommended token model

For interactive testing, a user token is fine. For long-running automation, prefer a **system user token** from Meta Business Manager.

### Permissions

Typical permissions:

- `ads_read` — read account, object, and reporting data
- `ads_management` — create and update ads objects
- `business_management` — often needed when you manage business assets such as ad accounts or audiences across a Business portfolio

### Standard vs Advanced access

- **Standard access** is enough if the app only manages ad accounts owned by the same business or assets you directly control.
- **Advanced access** is typically required if the app manages other people’s ad accounts, client accounts, or larger-scale production use cases.

### First calls to validate setup

Use these before doing anything else:

```bash
python3 scripts/meta_ads.py accounts
python3 scripts/meta_ads.py account
```

If these fail, the problem is usually one of:

- expired token
- wrong permissions
- missing ad account access for the token user or system user
- app still in development mode for a live use case

## Account IDs and object IDs

- Ad account IDs are often shown in URLs without `act_`; the API usually wants the `act_` prefix on account edges.
- The script normalises `META_AD_ACCOUNT_ID` automatically, so either `1234567890` or `act_1234567890` works.

## Common edges and when to use them

### Account discovery

```text
/me/adaccounts
/act_{account_id}
```

Use for account scope, currency, timezone, spend cap, business name, and health checks.

### Campaign structure

```text
/act_{account_id}/campaigns
/act_{account_id}/adsets
/act_{account_id}/ads
/act_{account_id}/adcreatives
/{node_id}
```

Use account edges to create or list. Use `/{node_id}` to read or update a specific object.

### Reporting

```text
/{node_id}/insights
/{report_run_id}
/{report_run_id}/insights
```

Use `GET` for small synchronous reads. Use `POST` to start an async report run for big jobs, then poll the report run ID and fetch the results.

### Targeting discovery

```text
/act_{account_id}/targetingsearch
/search
```

Use this to resolve targetable IDs and descriptors. Never guess interest IDs or geo IDs by name alone.

### Asset libraries

```text
/act_{account_id}/adimages
/act_{account_id}/advideos
```

Upload images or videos first, then refer to the returned hash or video ID in creatives.

### Batch

Use the Graph batch endpoint when you need several small reads at once. It is especially useful for account snapshots where you want campaigns, ad sets, and recent metadata in one round trip.

## Query design

### Field selection

Ask for the minimum fields that answer the task. Large field sets slow requests, create noisy output, and can interact badly with rate limits.

### Pagination

Collections paginate. Only use `--fetch-all` when the user truly needs every page.

### Filtering and sorting

Prefer server-side filtering and sorting for Insights and list queries when the API supports it. This reduces token usage and local processing.

### Async Insights

Use `--async` when:

- the time window is large
- the field list is long
- you use breakdowns
- you need many rows
- you query at `ad` level across a full account

### Batch reads

Prefer `batch` over several independent read calls when you need a compact account snapshot.

## Mutation strategy

### Default live-safety rules

- New campaigns, ad sets, and ads should usually start `PAUSED`.
- Dry-run first, then wait for explicit confirmation.
- Read back the changed object after any mutation.

### Budgets and money

Budgets and bids are typically represented in the **smallest denomination** of the account currency. Treat values as integer minor units unless the endpoint explicitly documents otherwise.

Example: on a USD account, a `daily_budget` of `5000` usually means 50.00 USD.

### Schedule and timezone

Always inspect account timezone before setting `start_time` or `end_time`. A valid timestamp can still be operationally wrong if you assume the wrong timezone.

### Status changes

Use `set-status` or `update` for:

- `ACTIVE`
- `PAUSED`
- `ARCHIVED`

Remember that child objects can remain effectively inactive because a parent campaign or ad set is paused.

## Reporting defaults

A safe default performance bundle is:

```text
account_id,account_name,campaign_id,campaign_name,adset_id,adset_name,ad_id,ad_name,impressions,reach,clicks,inline_link_clicks,spend,cpm,cpc,ctr,actions,action_values,purchase_roas
```

If the user only needs high-level health, remove the child IDs and keep the query at campaign level.

## Breakdowns and action arrays

- `breakdowns` splits rows by dimensions like age, country, platform, or placement.
- `action_breakdowns` splits the `actions` arrays themselves.
- Many conversion metrics arrive inside `actions` and `action_values` arrays rather than as flat columns.

Practical rule: if you use `action_breakdowns`, also request `actions`.

## Special ad category cautions

If the request touches areas such as housing, employment, credit, social issues, elections, or politics:

1. confirm whether a special category applies,
2. avoid assuming standard targeting is allowed,
3. review the account’s category settings and policy requirements before writing.

These categories often have extra approval and targeting restrictions that vary over time.

## Rate limits and retries

The Marketing API has per-app and ad-account limits, and Insights also has heavier cost controls. Build with this mindset:

- keep read field sets small,
- batch small reads,
- use async for heavy reporting,
- retry transient failures with backoff,
- slow down or reduce scope if you see error codes like `613` or `80004`.

The bundled script already retries common transient and throttling failures with exponential backoff.

## Error patterns

### Permission and auth errors

Symptoms:

- OAuth exceptions
- permission denied
- “object not found” on assets you can see in Ads Manager
- write calls fail but reads work

Check:

- token type and expiry
- `ads_read` vs `ads_management`
- system user or human user actually assigned to the ad account
- app mode and access level

### Invalid parameter errors

Usually caused by:

- wrong enum value
- wrong objective and optimisation pair
- missing required nested object
- legacy field names copied from old examples

### Object not found

Usually means the ID is wrong, belongs to a different account, or the token has no access.

## When to use the low-level request command

Use `request` when:

- you need an edge not covered by convenience commands,
- Meta changed a field or enum and the templates have not caught up,
- you need previews, reach estimates, delivery estimates, or other specialised endpoints,
- you need to test a new API behaviour before wrapping it in a workflow.

Examples:

```bash
python3 scripts/meta_ads.py request GET /act_123/reachestimate --set targeting_spec=@work/targeting.json
python3 scripts/meta_ads.py request GET /120000000000000/previews --set ad_format=DESKTOP_FEED_STANDARD
python3 scripts/meta_ads.py request POST /120000000000000 --set status=PAUSED --confirm
```

## See also

- [Field sets and reporting defaults](FIELDS.md)
- [Workflow playbook](WORKFLOWS.md)
- [Troubleshooting](TROUBLESHOOTING.md)
- [OpenClaw notes](OPENCLAW.md)
