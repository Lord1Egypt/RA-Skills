---
name: Mixpanel
slug: mixpanel
version: 1.0.1
homepage: https://clawic.com/skills/mixpanel
description: Query Mixpanel analytics with funnels, retention, segmentation, and event tracking via REST API.
changelog: Improved security docs and env var declarations.
metadata: {"clawdbot":{"emoji":"📊","requires":{"bins":["curl","jq"],"env":["MP_SERVICE_ACCOUNT","MP_SERVICE_SECRET","MP_PROJECT_ID"],"config":["~/mixpanel/"]},"primaryEnv":"MP_SERVICE_SECRET","os":["linux","darwin"]}}
---

## Setup

On first use, read `setup.md` for integration guidelines.

## When to Use

User needs product analytics from Mixpanel. Agent handles event queries, funnel analysis, retention cohorts, user segmentation, and profile lookups.

## Architecture

Memory lives in `~/mixpanel/`. See `memory-template.md` for structure.

```
~/mixpanel/
├── memory.md        # Projects, saved queries, insights
└── queries/         # Saved JQL queries
```

## Quick Reference

| Topic | File |
|-------|------|
| Setup process | `setup.md` |
| Memory template | `memory-template.md` |

## Core Rules

### 1. Authentication
Requires a Mixpanel Service Account:

```bash
export MP_SERVICE_ACCOUNT="your-service-account"
export MP_SERVICE_SECRET="your-service-secret"
export MP_PROJECT_ID="123456"
```

Create a service account in Mixpanel → Organization Settings → Service Accounts.

### 2. Query API for Analysis
Use the Query API for insights, funnels, retention:

```bash
BASE="https://mixpanel.com/api/query"
AUTH=$(echo -n "$MP_SERVICE_ACCOUNT:$MP_SERVICE_SECRET" | base64)

# Insights query (event counts)
curl -s "$BASE/insights?project_id=$MP_PROJECT_ID" \
  -H "Authorization: Basic $AUTH" \
  -H "Content-Type: application/json" \
  -d '{
    "params": {
      "event": ["Sign Up", "Purchase"],
      "type": "general",
      "unit": "day",
      "from_date": "2024-01-01",
      "to_date": "2024-01-31"
    }
  }' | jq
```

### 3. Funnel Analysis
```bash
curl -s "$BASE/funnels?project_id=$MP_PROJECT_ID" \
  -H "Authorization: Basic $AUTH" \
  -H "Content-Type: application/json" \
  -d '{
    "params": {
      "events": [
        {"event": "Sign Up"},
        {"event": "Complete Onboarding"},
        {"event": "First Purchase"}
      ],
      "from_date": "2024-01-01",
      "to_date": "2024-01-31",
      "unit": "day"
    }
  }' | jq '.data.meta.overall'
```

### 4. Retention Cohorts
```bash
curl -s "$BASE/retention?project_id=$MP_PROJECT_ID" \
  -H "Authorization: Basic $AUTH" \
  -H "Content-Type: application/json" \
  -d '{
    "params": {
      "born_event": "Sign Up",
      "event": "App Open",
      "from_date": "2024-01-01",
      "to_date": "2024-01-31",
      "unit": "week",
      "retention_type": "birth"
    }
  }' | jq
```

### 5. User Profiles
```bash
curl -s "https://mixpanel.com/api/query/engage?project_id=$MP_PROJECT_ID" \
  -H "Authorization: Basic $AUTH" \
  -H "Content-Type: application/json" \
  -d '{
    "filter_by_cohort": {"id": 12345},
    "output_properties": ["$email", "$name", "plan"]
  }' | jq
```

### 6. Export Raw Events
```bash
curl -s "https://data.mixpanel.com/api/2.0/export?project_id=$MP_PROJECT_ID" \
  -H "Authorization: Basic $AUTH" \
  -d "from_date=2024-01-01" \
  -d "to_date=2024-01-07" \
  -d "event=[\"Purchase\"]"
```

### 7. JQL for Complex Queries
```javascript
// Mixpanel JQL (JavaScript Query Language)
function main() {
  return Events({
    from_date: "2024-01-01",
    to_date: "2024-01-31",
    event_selectors: [{event: "Purchase"}]
  })
  .groupByUser(["properties.$city"], mixpanel.reducer.sum("properties.amount"))
  .groupBy(["key.$city"], mixpanel.reducer.avg("value"))
  .sortDesc("value")
  .take(10);
}
```

## Common Queries

| Goal | Endpoint | Key Params |
|------|----------|------------|
| Event counts | `/insights` | event, type, unit, dates |
| Conversion funnel | `/funnels` | events array, dates |
| User retention | `/retention` | born_event, event, unit |
| User segments | `/engage` | filter_by_cohort, properties |
| Raw event export | `/export` | dates, event filter |

## Mixpanel Traps

- **Wrong date format** → use `YYYY-MM-DD`, not timestamps
- **Missing project_id** → every Query API call needs it
- **Rate limits** → 60 requests/hour for free tier, batch queries when possible
- **JQL timeouts** → queries over 60s fail, add `.take(N)` to limit results

## External Endpoints

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| mixpanel.com/api/query/* | Credentials, project ID, query params | Analytics queries |
| data.mixpanel.com/api/2.0/* | Credentials, project ID, date range | Raw data export |

No other data is sent externally.

## Security & Privacy

**Data sent to Mixpanel (over HTTPS):**
- Service account credentials for authentication
- Query parameters (event names, date ranges, filters)
- Project ID

**Data that stays local:**
- Credentials stored ONLY in environment variables
- Query results cached in ~/mixpanel/

**This skill does NOT:**
- Store credentials in memory.md or any file
- Send data to services other than mixpanel.com
- Modify your Mixpanel tracking code or SDK

## Trust

By using this skill, analytics data is queried from Mixpanel.
Only install if you trust Mixpanel with your product data.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `analytics` — multi-platform analytics
- `data-analysis` — data processing patterns
- `api` — REST API best practices

## Feedback

- If useful: `clawhub star mixpanel`
- Stay updated: `clawhub sync`
