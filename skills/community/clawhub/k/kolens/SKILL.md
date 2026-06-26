---
name: kolens
version: 1.0.0
slug: kolens
description: |
  Search and analyze TikTok KOL (Key Opinion Leaders) using the KOLens API.
  Use when: (1) User asks to search KOL/influencers for a specific keyword/niche. (2) User wants to find contact information (email, website, Instagram) of TikTok creators. (3) User wants to analyze KOL metrics (followers, avg views, engagement rate).
environment:
  KOLENS_API_KEY:
    description: "Your KOLens API key (e.g. kol_xxxxx). Get this from the KOLens service admin."
    required: true
  KOLENS_API_URL:
    description: "KOLens API base URL (e.g. https://kolens-api-production.up.railway.app). Get this from the KOLens service admin."
    required: true
executables:
  curl:
    description: "HTTP client for making API requests"
    required: true
  jq:
    description: "JSON processor for parsing API responses"
    required: false
---

# KOLens - TikTok KOL Intelligence API

## Overview

KOLens is a TikTok KOL data scraping API that provides:
- Search TikTok KOLs by keyword
- Get KOL metrics (followers, avg views, engagement rate)
- Get contact information (email, website, Instagram, YouTube)

## Setup

### 1. Get API Credentials

Contact the KOLens service administrator to obtain:
- **KOLENS_API_KEY** — Your personal API key
- **KOLENS_API_URL** — The KOLens API base URL

### 2. Set Environment Variables

```bash
export KOLENS_API_KEY="kol_your_key_here"
export KOLENS_API_URL="https://your-kolens-api-url.com"
```

## Usage

### Step 1: Submit a Scraping Job

```bash
curl -X POST "${KOLENS_API_URL}/api/scrape" \
  -H "Authorization: Bearer ${KOLENS_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"keyword":"[KEYWORD]","max_videos":30,"fetch_contacts":true}'
```

**Parameters:**
- `keyword` (required): TikTok search keyword
- `max_videos` (optional, default: 50): Max videos to scrape (1-200)
- `fetch_contacts` (optional, default: true): Whether to fetch contact info

**Response:**
```json
{
  "job_id": "abc123",
  "status": "queued",
  "keyword": "peptides",
  "estimated_seconds": 105
}
```

### Step 2: Poll Job Status

```bash
curl "${KOLENS_API_URL}/api/jobs/[JOB_ID]" \
  -H "Authorization: Bearer ${KOLENS_API_KEY}"
```

**Status values:** `queued` → `running` → `completed` | `failed`

**Completed response:**
```json
{
  "job_id": "abc123",
  "status": "completed",
  "stage": "Done — 12 videos, 8 KOLs, 0 Sellers",
  "progress": 100,
  "total_videos": 12,
  "kol_count": 8,
  "seller_count": 0
}
```

### Step 3: Query KOL List

```bash
# KOLs with email only
curl "${KOLENS_API_URL}/api/kols?keyword=[KEYWORD]&require_email=true&per_page=30" \
  -H "Authorization: Bearer ${KOLENS_API_KEY}"

# All KOLs
curl "${KOLENS_API_URL}/api/kols?keyword=[KEYWORD]&per_page=30" \
  -H "Authorization: Bearer ${KOLENS_API_KEY}"
```

**Response:**
```json
{
  "total": 6,
  "page": 1,
  "per_page": 30,
  "kols": [
    {
      "username": "somekol",
      "display_name": "Some KOL",
      "follower_count": 1000000,
      "avg_views": 500000,
      "avg_engagement_rate": 0.05,
      "has_email": true,
      "has_website": true,
      "first_seen_at": "2026-04-10T07:18:59.933946",
      "last_updated_at": "2026-04-10T07:18:59.933948"
    }
  ]
}
```

### Step 4: Get Single KOL Profile

```bash
curl "${KOLENS_API_URL}/api/kols/[USERNAME]" \
  -H "Authorization: Bearer ${KOLENS_API_KEY}"
```

**Response:**
```json
{
  "username": "somekol",
  "display_name": "Some KOL",
  "follower_count": 1000000,
  "avg_views": 500000,
  "avg_engagement_rate": 0.05,
  "bio": "This is my bio",
  "contact": {
    "email": "contact@example.com",
    "phone": null,
    "website": "https://example.com",
    "instagram": "@somekol",
    "youtube": "somekol",
    "linktree_url": "https://linktr.ee/somekol"
  }
}
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/scrape` | POST | Submit a scraping job |
| `/api/jobs/{job_id}` | GET | Get job status |
| `/api/kols` | GET | Query KOL database |
| `/api/kols/{username}` | GET | Get single KOL profile |

## Workflow Example

```bash
# 1. Submit job
curl -s -X POST "${KOLENS_API_URL}/api/scrape" \
  -H "Authorization: Bearer ${KOLENS_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"keyword":"camping","max_videos":30,"fetch_contacts":true}' > /tmp/job.json

JOB_ID=$(cat /tmp/job.json | jq -r '.job_id')
echo "Job ID: ${JOB_ID}"

# 2. Poll until completed (every 90s)
for i in 1 2 3 4 5 6 7 8 9 10; do
  STATUS=$(curl -s "${KOLENS_API_URL}/api/jobs/${JOB_ID}" \
    -H "Authorization: Bearer ${KOLENS_API_KEY}" | jq -r '.status')
  echo "Status: ${STATUS}"
  if [ "${STATUS}" = "completed" ]; then
    echo "Job completed!"
    break
  fi
  sleep 90
done

# 3. Get KOLs with email
curl -s "${KOLENS_API_URL}/api/kols?keyword=camping&require_email=true" \
  -H "Authorization: Bearer ${KOLENS_API_KEY}"
```

## Troubleshooting

- **Task stuck in "running"**: The scraping typically takes 2-3 minutes. Continue polling.
- **"Invalid or inactive API key"**: Your API key may have expired. Contact the KOLens admin for a new one.
- **Empty results**: Try different/ broader keywords, or check if TikTok has content for that keyword.
- **Rate limiting**: If you get rate limited, wait before making more requests.

## Legal Notice

When using this skill to collect KOL contact information:
- Only use scraped data for legitimate outreach and collaboration purposes
- Respect privacy regulations (GDPR, CCPA, etc.) applicable in your jurisdiction
- Do not use scraped data for spam or unsolicited marketing
- Always verify contact information before reaching out
