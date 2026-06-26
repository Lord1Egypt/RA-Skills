# Meta Ads API Skill (Full)

## Overview

This skill enables an agent to read, create, and manage Meta (Facebook/Instagram) ad campaigns via the Marketing API.

---

## Base Configuration

### API Base URL

```
https://graph.facebook.com/v19.0/
```

### Required Inputs

* `access_token`
* `ad_account_id` (format: `act_<ID>`)

---

## Authentication

### Method

Use access token in query or header:

```
Authorization: Bearer <ACCESS_TOKEN>
```

or

```
?access_token=<ACCESS_TOKEN>
```

---

## Permissions Required

| Permission     | Purpose                       |
| -------------- | ----------------------------- |
| ads_read       | Read campaigns, ads, insights |
| ads_management | Create & update campaigns     |

---

## Core Entities

* Campaign → Top-level objective
* Ad Set → Budget + targeting
* Ad → Creative (image/video + copy)

---

# READ OPERATIONS (Primary)

## 1. Get Campaigns

### Endpoint

```
GET /act_<AD_ACCOUNT_ID>/campaigns
```

### Example

```
GET /act_<ID>/campaigns?fields=id,name,status,objective
```

---

## 2. Get Ad Sets

```
GET /act_<ID>/adsets?fields=id,name,campaign_id,status,daily_budget
```

---

## 3. Get Ads

```
GET /act_<ID>/ads?fields=id,name,adset_id,status
```

---

## 4. Campaign Insights

```
GET /<CAMPAIGN_ID>/insights?fields=impressions,clicks,spend,ctr,cpc
```

---

## 5. Account Insights

```
GET /act_<ID>/insights?fields=impressions,clicks,spend&date_preset=last_7d
```

---

## 6. Time Range Filtering

```
time_range={'since':'2024-01-01','until':'2024-01-31'}
```

---

## 7. Status Filtering

```
effective_status=['ACTIVE']
```

---

## 8. Levels

```
level=campaign | adset | ad
```

---

## Pagination

Responses include:

```
paging.next
```

### Agent Rule

* Follow `paging.next` until exhausted
* Stop at safe limit (e.g., 10 pages)

---

# WRITE OPERATIONS

## 9. Create Campaign

```
POST /act_<ID>/campaigns
```

Payload:

```
name=My Campaign
objective=CONVERSIONS
status=PAUSED
special_ad_categories=[]
```

---

## 10. Create Ad Set

```
POST /act_<ID>/adsets
```

Payload:

```
name=Ad Set 1
daily_budget=1000
billing_event=IMPRESSIONS
optimization_goal=REACH
campaign_id=<CAMPAIGN_ID>
targeting={"geo_locations":{"countries":["MA"]}}
status=PAUSED
```

---

## 11. Create Ad Creative

```
POST /act_<ID>/adcreatives
```

Payload:

```
name=Creative 1
object_story_spec={"page_id":"<PAGE_ID>","link_data":{"message":"Hello","link":"https://example.com"}}
```

---

## 12. Create Ad

```
POST /act_<ID>/ads
```

Payload:

```
name=Ad 1
adset_id=<ADSET_ID>
creative={"creative_id":"<CREATIVE_ID>"}
status=PAUSED
```

---

## 13. Update Campaign Status

```
POST /<CAMPAIGN_ID>?status=PAUSED
```

---

# INSIGHTS METRICS

Common fields:

* impressions
* clicks
* spend
* ctr
* cpc
* conversions (if configured)

---

# ERROR HANDLING

| Code | Meaning               |
| ---- | --------------------- |
| 190  | Invalid/expired token |
| 200  | Permission denied     |
| 100  | Invalid parameter     |

---

# RATE LIMITS

* Respect HTTP 429
* Retry with exponential backoff
* Batch requests when possible

---

# AGENT RULES (IMPORTANT)

## Safety

* Always create campaigns as `PAUSED`
* Never expose access tokens
* Validate all IDs before use

## Efficiency

* Cache campaign lists
* Avoid duplicate API calls
* Use insights endpoints instead of raw data when possible

## Reliability

* Retry failed requests (max 3)
* Log all API responses
* Detect empty responses

---

# ANALYTICS LOGIC (Agent Intelligence)

## Detect Poor Performance

* High spend + low CTR → flag
* High CPC → recommend pause

## Detect Winners

* High CTR + low CPC → scale budget

## Example Rule

```
IF spend > 50 AND ctr < 0.5%
THEN mark campaign as underperforming
```

---

# SAMPLE REQUEST FLOW

1. Fetch campaigns
2. Fetch insights
3. Analyze metrics
4. Decide action
5. Update campaign (pause/scale)

---

# BEST PRACTICES

* Use long-lived tokens
* Prefer system users (Business Manager)
* Monitor token expiration
* Use versioned API (v19.0+)

---

# NOTES

* Insights are delayed (not real-time)
* Conversion tracking requires Pixel or CAPI
* Some features require app review

---
