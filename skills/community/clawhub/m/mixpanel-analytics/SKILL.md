---
name: mixpanel-analytics
description: "Query Mixpanel product analytics — events, funnels, retention, user profiles, and cohorts via the Mixpanel Data Export API. Use when you need to: (1) Query event counts or unique users over time, (2) Analyze funnel conversion rates, (3) Check retention metrics, (4) Look up or update user profiles, (5) Export raw event data, (6) Get top events or properties, (7) List cohorts. Requires MIXPANEL_SERVICE_ACCOUNT_USERNAME + MIXPANEL_SERVICE_ACCOUNT_SECRET (or MIXPANEL_API_SECRET for legacy projects)."
---

# Mixpanel Analytics Skill

Query product analytics data from Mixpanel using the Data Export API.

## Setup

### Option A — Service Account (recommended, new projects)

```bash
export MIXPANEL_SERVICE_ACCOUNT_USERNAME="your-sa-username"
export MIXPANEL_SERVICE_ACCOUNT_SECRET="your-sa-secret"
export MIXPANEL_PROJECT_ID="12345678"
```

Get these: Mixpanel → Organization Settings → Service Accounts → Create Service Account

### Option B — API Secret (legacy / project-level)

```bash
export MIXPANEL_API_SECRET="your-api-secret"
```

Get it: Mixpanel → Project Settings → Access Keys → API Secret

### Data Residency (optional)

```bash
export MIXPANEL_DATA_REGION="eu"  # for EU data residency (default: us)
```

## Core Workflows

### Top Events (Last 30 Days)

```bash
python3 ~/.openclaw/workspace/skills/mixpanel-analytics/scripts/mx.py events --days 30
```

### Event Count Over Time

```bash
python3 ~/.openclaw/workspace/skills/mixpanel-analytics/scripts/mx.py segmentation \
  --event "Sign Up" --from-date 2026-01-01 --to-date 2026-03-21 --unit day
```

### Unique Users for an Event

```bash
python3 ~/.openclaw/workspace/skills/mixpanel-analytics/scripts/mx.py segmentation \
  --event "Purchase" --type unique --days 7
```

### Funnel Analysis

```bash
python3 ~/.openclaw/workspace/skills/mixpanel-analytics/scripts/mx.py funnel \
  --funnel-id 12345 --from-date 2026-03-01 --to-date 2026-03-21
```

### List All Funnels

```bash
python3 ~/.openclaw/workspace/skills/mixpanel-analytics/scripts/mx.py funnels
```

### Retention Cohort (Daily)

```bash
python3 ~/.openclaw/workspace/skills/mixpanel-analytics/scripts/mx.py retention \
  --from-date 2026-03-01 --to-date 2026-03-21 --retention-type birth --unit day
```

### User Profile Lookup

```bash
python3 ~/.openclaw/workspace/skills/mixpanel-analytics/scripts/mx.py profile --distinct-id "user@example.com"
```

### Export Raw Events

```bash
python3 ~/.openclaw/workspace/skills/mixpanel-analytics/scripts/mx.py export \
  --from-date 2026-03-20 --to-date 2026-03-21 \
  --event "Purchase" --limit 100
```

### List All Events

```bash
python3 ~/.openclaw/workspace/skills/mixpanel-analytics/scripts/mx.py list-events
```

## Direct API Calls (Advanced)

For EU data residency, replace `data.mixpanel.com` with `data-eu.mixpanel.com`.

```bash
# Segment by event with breakdown
curl -s "https://data.mixpanel.com/api/2.0/segmentation?project_id=$MIXPANEL_PROJECT_ID&event=Sign%20Up&from_date=2026-03-01&to_date=2026-03-21&unit=day" \
  -u "$MIXPANEL_SERVICE_ACCOUNT_USERNAME:$MIXPANEL_SERVICE_ACCOUNT_SECRET"
```

## Key Concepts

- **Events**: User actions tracked in your product (clicks, purchases, sign-ups)
- **Distinct ID**: Unique identifier per user in Mixpanel
- **Funnels**: Conversion paths (e.g. View → Add to Cart → Purchase)
- **Retention**: How often users return after a trigger event
- **Cohorts**: Groups of users with common behaviors for analysis

## Agent Use Cases

- Daily growth briefing: `events` for yesterday's top events + unique users
- Conversion monitoring: `segmentation` on key events (sign-up → activation)
- Funnel regression alerts: `funnel` comparison week-over-week
- User debugging: `profile` lookup when investigating support issues
- Weekly retention report: `retention` on 7-day and 30-day windows

## Notes

- Data Export API has a rate limit of 60 requests/hour
- Raw event export can return large datasets — use `--limit` to cap
- Funnel IDs are found in Mixpanel UI URL: `/report/funnels/XXXX`
- All dates should be in `YYYY-MM-DD` format
