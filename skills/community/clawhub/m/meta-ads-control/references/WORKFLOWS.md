# Workflow Playbook

These are repeatable agent workflows for common Meta ads tasks.

## 1) Initial account audit

Goal: understand structure, delivery state, and recent performance with minimal API spend.

### Steps

1. Read account metadata.
2. Read campaigns, ad sets, and ads with minimal lifecycle fields.
3. Pull a short Insights summary at campaign or ad set level.
4. Summarise:
   - active vs paused objects
   - biggest spenders
   - obvious delivery problems
   - next recommended actions

### Commands

```bash
python3 scripts/meta_ads.py account
python3 scripts/meta_ads.py list campaigns
python3 scripts/meta_ads.py list adsets
python3 scripts/meta_ads.py list ads
python3 scripts/meta_ads.py insights --level campaign --date-preset last_7d
```

## 2) Safe pause or resume

Goal: pause or resume an object without surprising the user.

### Steps

1. Read the object first.
2. Explain what will change.
3. Dry-run the status update.
4. Wait for explicit approval.
5. Apply with `--confirm`.
6. Read back the object.

### Commands

```bash
python3 scripts/meta_ads.py get 120000000000000 --fields id,name,status,effective_status,campaign_id,adset_id
python3 scripts/meta_ads.py set-status 120000000000000 PAUSED --dry-run
python3 scripts/meta_ads.py set-status 120000000000000 PAUSED --confirm
python3 scripts/meta_ads.py get 120000000000000 --fields id,name,status,effective_status,updated_time
```

## 3) Budget change

Goal: change spend without losing context.

### Steps

1. Read account currency and timezone.
2. Read the current ad set or campaign budgets.
3. Build an update payload in raw API units.
4. Dry-run it.
5. Confirm.
6. Apply and verify.

### Commands

```bash
python3 scripts/meta_ads.py account --fields id,currency,timezone_name
python3 scripts/meta_ads.py get 120000000000000 --fields id,name,daily_budget,lifetime_budget,status,effective_status
python3 scripts/meta_ads.py update 120000000000000 --params-file work/budget-change.json --dry-run
python3 scripts/meta_ads.py update 120000000000000 --params-file work/budget-change.json --confirm
python3 scripts/meta_ads.py get 120000000000000 --fields id,name,daily_budget,lifetime_budget,updated_time
```

## 4) Launch a new campaign structure

Goal: create campaign, ad set, creative, and ad with live-safety defaults.

### Steps

1. Confirm account, timezone, currency, page, pixel, and Instagram actor prerequisites.
2. Copy the templates in `assets/` into working files.
3. Fill in payloads.
4. Dry-run each step.
5. Create objects in order.
6. Read each created object.
7. Leave them paused unless the user explicitly wants immediate delivery.

### Commands

```bash
python3 scripts/meta_ads.py create campaign --params-file work/campaign.json --dry-run
python3 scripts/meta_ads.py create campaign --params-file work/campaign.json --confirm

python3 scripts/meta_ads.py create adset --params-file work/adset.json --dry-run
python3 scripts/meta_ads.py create adset --params-file work/adset.json --confirm

python3 scripts/meta_ads.py create adcreative --params-file work/adcreative.json --dry-run
python3 scripts/meta_ads.py create adcreative --params-file work/adcreative.json --confirm

python3 scripts/meta_ads.py create ad --params-file work/ad.json --dry-run
python3 scripts/meta_ads.py create ad --params-file work/ad.json --confirm
```

## 5) Creative rollout with local assets

Goal: upload local media and build creatives safely.

### Steps

1. Upload image or video.
2. Capture the returned `image_hash` or video ID.
3. Insert it into the creative payload.
4. Create the creative, then the ad.

### Commands

```bash
python3 scripts/meta_ads.py upload adimages --file work/creative.jpg --confirm
python3 scripts/meta_ads.py upload advideos --file work/creative.mp4 --confirm
python3 scripts/meta_ads.py create adcreative --params-file work/adcreative.json --confirm
python3 scripts/meta_ads.py create ad --params-file work/ad.json --confirm
```

## 6) Audience research and targeting build

Goal: create a valid targeting spec without made-up IDs.

### Steps

1. Resolve geo IDs or descriptors.
2. Resolve interests or behaviours.
3. Build the targeting JSON.
4. Dry-run ad set creation.

### Commands

```bash
python3 scripts/meta_ads.py targeting-search --type adgeolocation --q "Munich"
python3 scripts/meta_ads.py targeting-search --type adinterest --q "running"
python3 scripts/meta_ads.py create adset --params-file work/adset.json --dry-run
```

## 7) Performance triage

Goal: find what to scale down, pause, or investigate.

### Steps

1. Pull campaign-level Insights for the last 7 or 30 days.
2. If needed, drill into ad sets, then ads.
3. Sort by spend, CPA, or ROAS.
4. Separate decisions:
   - pause candidates
   - scale candidates
   - tracking investigations
   - creative tests needed

### Commands

```bash
python3 scripts/meta_ads.py insights --level campaign --date-preset last_7d --fields campaign_id,campaign_name,spend,actions,action_values,purchase_roas
python3 scripts/meta_ads.py insights --level adset --date-preset last_7d --fields adset_id,adset_name,spend,actions,action_values,purchase_roas
python3 scripts/meta_ads.py insights --level ad --date-preset last_7d --fields ad_id,ad_name,spend,clicks,ctr,cpc,actions,action_values,purchase_roas
```

## 8) Bulk account snapshot with batch

Goal: reduce latency and tool chatter for read-only snapshots.

### Steps

1. Build a batch file with several GET calls.
2. Run it.
3. Summarise the parsed bodies.

### Commands

```bash
python3 scripts/meta_ads.py batch --batch-file assets/batch-read-example.json
```

## 9) Large reporting job

Goal: get a big Insights extract without timing out.

### Steps

1. Keep fields tight.
2. Use `--async`.
3. Poll until complete.
4. Use `--fetch-all` if you truly need every row.
5. Write output to a file if the result will be large.

### Commands

```bash
python3 scripts/meta_ads.py insights act_123 --level ad --date-preset last_90d --fields ad_id,ad_name,spend,impressions,clicks,actions,action_values,purchase_roas --async --fetch-all --output work/insights.json
```

## 10) Unsupported endpoint escape hatch

Goal: avoid getting stuck when Meta changes or adds an endpoint.

### Steps

1. Identify the exact path and params.
2. Use `request`.
3. Dry-run if it is a write.
4. Confirm.
5. Wrap in a higher-level workflow only after the path is proven.

### Commands

```bash
python3 scripts/meta_ads.py request GET /120000000000000/previews --set ad_format=DESKTOP_FEED_STANDARD
python3 scripts/meta_ads.py request POST /120000000000000 --set status=ACTIVE --dry-run
python3 scripts/meta_ads.py request POST /120000000000000 --set status=ACTIVE --confirm
```
