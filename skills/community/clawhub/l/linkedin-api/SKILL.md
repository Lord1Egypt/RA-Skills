---
name: linkedin
description: |
  LinkedIn API integration with managed OAuth. Share posts, manage profile, and access LinkedIn features.
  Use this skill when users want to share content on LinkedIn, get profile/organization information, or interact with LinkedIn's platform.
  Advertising features (campaigns, ad accounts) require additional OAuth scopes — verify granted scopes before use.
  For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
  Requires network access and valid Maton API key.
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    requires:
      env:
        - MATON_API_KEY
---

# LinkedIn

Access the LinkedIn API with managed OAuth authentication. Share posts, manage advertising campaigns, retrieve profile and organization information, upload media, and access the Ad Library.

## Quick Start

```bash
# Get current user profile
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/linkedin/rest/me')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('LinkedIn-Version', '202506')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## Base URL

```
https://api.maton.ai/linkedin/rest/{resource}
```

Maton proxies requests to `api.linkedin.com` and automatically injects your OAuth token.

## Authentication

All requests require the Maton API key in the Authorization header:

```
Authorization: Bearer $MATON_API_KEY
```

**Environment Variable:** Set your API key as `MATON_API_KEY`:

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### Getting Your API Key

1. Sign in or create an account at [maton.ai](https://maton.ai)
2. Go to [maton.ai/settings](https://maton.ai/settings)
3. Copy your API key

### Required Headers

LinkedIn REST API requires the version header:

```
LinkedIn-Version: 202506
```

## Connection Management

Manage your LinkedIn OAuth connections at `https://api.maton.ai`.

### List Connections

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections?app=linkedin&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Create Connection

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'linkedin'}).encode()
req = urllib.request.Request('https://api.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Get Connection

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections/{connection_id}')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**Response:**
```json
{
  "connection": {
    "connection_id": "{connection_id}",
    "status": "ACTIVE",
    "creation_time": "2026-02-07T08:00:24.372659Z",
    "last_updated_time": "2026-02-07T08:05:16.609085Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "linkedin",
    "metadata": {}
  }
}
```

Open the returned `url` in a browser to complete OAuth authorization.

### Delete Connection

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections/{connection_id}', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Specifying Connection

If you have multiple LinkedIn connections, specify which one to use with the `Maton-Connection` header:

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/linkedin/rest/me')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('LinkedIn-Version', '202506')
req.add_header('Maton-Connection', '{connection_id}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

If you have multiple connections, always include this header to ensure requests go to the intended account.

## Security & Permissions

- Access is scoped to posts, profiles, organizations, images, videos, and analytics within the connected LinkedIn account.
- **All write operations require explicit user approval.** Before executing any create, update, or delete call:
  1. State the exact operation (e.g., "Create a DRAFT campaign in ad account 123456789")
  2. Show the user the request body or key parameters
  3. Wait for explicit confirmation before sending the request
  4. For destructive operations (DELETE), additionally confirm the resource cannot be recovered
- Advertising operations (campaign creation, budget changes, account modifications) carry financial impact. Always confirm budget amounts and targeting criteria with the user before execution.

## API Reference

### Profile

#### Get Current User Profile

```bash
GET /linkedin/rest/me
LinkedIn-Version: 202506
```

**Example:**
```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/linkedin/rest/me')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('LinkedIn-Version', '202506')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**Response:**
```json
{
  "firstName": {
    "localized": {"en_US": "John"},
    "preferredLocale": {"country": "US", "language": "en"}
  },
  "localizedFirstName": "John",
  "lastName": {
    "localized": {"en_US": "Doe"},
    "preferredLocale": {"country": "US", "language": "en"}
  },
  "localizedLastName": "Doe",
  "id": "yrZCpj2Z12",
  "vanityName": "johndoe",
  "localizedHeadline": "Software Engineer at Example Corp",
  "profilePicture": {
    "displayImage": "urn:li:digitalmediaAsset:C4D00AAAAbBCDEFGhiJ"
  }
}
```

### Sharing Posts

#### Create a Text Post

```bash
POST /linkedin/rest/posts
Content-Type: application/json
LinkedIn-Version: 202506

{
  "author": "urn:li:person:{personId}",
  "lifecycleState": "PUBLISHED",
  "visibility": "PUBLIC",
  "commentary": "Hello LinkedIn! This is my first API post.",
  "distribution": {
    "feedDistribution": "MAIN_FEED"
  }
}
```

**Response:** `201 Created` with `x-restli-id` header containing the post URN.

#### Create an Article/URL Share

```bash
POST /linkedin/rest/posts
Content-Type: application/json
LinkedIn-Version: 202506

{
  "author": "urn:li:person:{personId}",
  "lifecycleState": "PUBLISHED",
  "visibility": "PUBLIC",
  "commentary": "Check out this great article!",
  "distribution": {
    "feedDistribution": "MAIN_FEED"
  },
  "content": {
    "article": {
      "source": "https://example.com/article",
      "title": "Article Title",
      "description": "Article description here"
    }
  }
}
```

#### Create an Image Post

First, initialize the image upload, then upload the image, then create the post.

**Step 1: Initialize Image Upload**
```bash
POST /linkedin/rest/images?action=initializeUpload
Content-Type: application/json
LinkedIn-Version: 202506

{
  "initializeUploadRequest": {
    "owner": "urn:li:person:{personId}"
  }
}
```

**Response:**
```json
{
  "value": {
    "uploadUrlExpiresAt": 1770541529250,
    "uploadUrl": "https://www.linkedin.com/dms-uploads/...",
    "image": "urn:li:image:D4D10AQH4GJAjaFCkHQ"
  }
}
```

**Step 2: Upload Image Binary**
```bash
PUT {uploadUrl from step 1}
Content-Type: image/png

{binary image data}
```

**Step 3: Create Image Post**
```bash
POST /linkedin/rest/posts
Content-Type: application/json
LinkedIn-Version: 202506

{
  "author": "urn:li:person:{personId}",
  "lifecycleState": "PUBLISHED",
  "visibility": "PUBLIC",
  "commentary": "Check out this image!",
  "distribution": {
    "feedDistribution": "MAIN_FEED"
  },
  "content": {
    "media": {
      "id": "urn:li:image:D4D10AQH4GJAjaFCkHQ",
      "title": "Image Title"
    }
  }
}
```

### Visibility Options

| Value | Description |
|-------|-------------|
| `PUBLIC` | Viewable by anyone on LinkedIn |
| `CONNECTIONS` | Viewable by 1st-degree connections only |

### Share Media Categories

| Value | Description |
|-------|-------------|
| `NONE` | Text-only post |
| `ARTICLE` | URL/article share |
| `IMAGE` | Image post |
| `VIDEO` | Video post |

### Ad Library (Public Data)

The Ad Library API provides access to public advertising data on LinkedIn. These endpoints use the REST API with version headers.

#### Required Headers for Ad Library

```
LinkedIn-Version: 202506
```

#### Search Ads

```bash
GET /linkedin/rest/adLibrary?q=criteria&keyword={keyword}
```

Query parameters:
- `keyword` (string): Search ad content (multiple keywords use AND logic)
- `advertiser` (string): Search by advertiser name
- `countries` (array): Filter by ISO 3166-1 alpha-2 country codes
- `dateRange` (object): Filter by served dates
- `start` (integer): Pagination offset
- `count` (integer): Results per page (max 25)

**Example - Search ads by keyword:**
```bash
GET /linkedin/rest/adLibrary?q=criteria&keyword=linkedin
```

**Example - Search ads by advertiser:**
```bash
GET /linkedin/rest/adLibrary?q=criteria&advertiser=microsoft
```

**Response:**
```json
{
  "paging": {
    "start": 0,
    "count": 10,
    "total": 11619543,
    "links": [...]
  },
  "elements": [
    {
      "adUrl": "https://www.linkedin.com/ad-library/detail/...",
      "details": {
        "advertiser": {...},
        "adType": "TEXT_AD",
        "targeting": {...},
        "statistics": {
          "firstImpressionDate": 1704067200000,
          "latestImpressionDate": 1706745600000,
          "impressionsFrom": 1000,
          "impressionsTo": 5000
        }
      },
      "isRestricted": false
    }
  ]
}
```

#### Search Job Postings

```bash
GET /linkedin/rest/jobLibrary?q=criteria&keyword={keyword}
```

**Note:** Job Library requires version `202506`.

Query parameters:
- `keyword` (string): Search job content
- `organization` (string): Filter by company name
- `countries` (array): Filter by country codes
- `dateRange` (object): Filter by posting dates
- `start` (integer): Pagination offset
- `count` (integer): Results per page (max 24)

**Example:**
```bash
GET /linkedin/rest/jobLibrary?q=criteria&keyword=software&organization=google
```

**Response includes:**
- `jobPostingUrl`: Link to job listing
- `jobDetails`: Title, location, description, salary, benefits
- `statistics`: Impression data

### Marketing API (Advertising)

The Marketing API provides access to LinkedIn's advertising platform. These endpoints use the versioned REST API.

#### Required Headers for Marketing API

```
LinkedIn-Version: 202506
```

#### List Ad Accounts

```bash
GET /linkedin/rest/adAccounts?q=search
```

Returns all ad accounts accessible by the authenticated user.

**Response:**
```json
{
  "paging": {
    "start": 0,
    "count": 10,
    "links": []
  },
  "elements": [
    {
      "id": 123456789,
      "name": "My Ad Account",
      "status": "ACTIVE",
      "type": "BUSINESS",
      "currency": "USD",
      "reference": "urn:li:organization:12345"
    }
  ]
}
```

#### Get Ad Account

```bash
GET /linkedin/rest/adAccounts/{adAccountId}
```

#### Create Ad Account

```bash
POST /linkedin/rest/adAccounts
Content-Type: application/json

{
  "name": "New Ad Account",
  "currency": "USD",
  "reference": "urn:li:organization:{orgId}",
  "type": "BUSINESS"
}
```

#### Update Ad Account

```bash
POST /linkedin/rest/adAccounts/{adAccountId}
Content-Type: application/json
X-RestLi-Method: PARTIAL_UPDATE

{
  "patch": {
    "$set": {
      "name": "Updated Account Name"
    }
  }
}
```

#### List Campaign Groups

Campaign groups are nested under ad accounts:

```bash
GET /linkedin/rest/adAccounts/{adAccountId}/adCampaignGroups
```

#### Create Campaign Group

```bash
POST /linkedin/rest/adAccounts/{adAccountId}/adCampaignGroups
Content-Type: application/json

{
  "name": "Q1 2026 Campaigns",
  "status": "DRAFT",
  "runSchedule": {
    "start": 1704067200000,
    "end": 1711929600000
  },
  "totalBudget": {
    "amount": "10000",
    "currencyCode": "USD"
  }
}
```

#### Get Campaign Group

```bash
GET /linkedin/rest/adAccounts/{adAccountId}/adCampaignGroups/{campaignGroupId}
```

#### Update Campaign Group

```bash
POST /linkedin/rest/adAccounts/{adAccountId}/adCampaignGroups/{campaignGroupId}
Content-Type: application/json
X-RestLi-Method: PARTIAL_UPDATE

{
  "patch": {
    "$set": {
      "status": "ACTIVE"
    }
  }
}
```

#### Delete Campaign Group

> **Destructive operation.** Deleting a campaign group may be irreversible and will remove all associated data. Confirm the campaign group ID and that no active campaigns depend on it before proceeding.

```bash
DELETE /linkedin/rest/adAccounts/{adAccountId}/adCampaignGroups/{campaignGroupId}
```

#### List Campaigns

Campaigns are also nested under ad accounts:

```bash
GET /linkedin/rest/adAccounts/{adAccountId}/adCampaigns
```

#### Create Campaign

```bash
POST /linkedin/rest/adAccounts/{adAccountId}/adCampaigns
Content-Type: application/json

{
  "campaignGroup": "urn:li:sponsoredCampaignGroup:123456",
  "name": "Brand Awareness Campaign",
  "status": "DRAFT",
  "type": "SPONSORED_UPDATES",
  "objectiveType": "BRAND_AWARENESS",
  "dailyBudget": {
    "amount": "100",
    "currencyCode": "USD"
  },
  "costType": "CPM",
  "unitCost": {
    "amount": "5",
    "currencyCode": "USD"
  },
  "locale": {
    "country": "US",
    "language": "en"
  }
}
```

#### Get Campaign

```bash
GET /linkedin/rest/adAccounts/{adAccountId}/adCampaigns/{campaignId}
```

#### Update Campaign

```bash
POST /linkedin/rest/adAccounts/{adAccountId}/adCampaigns/{campaignId}
Content-Type: application/json
X-RestLi-Method: PARTIAL_UPDATE

{
  "patch": {
    "$set": {
      "status": "ACTIVE"
    }
  }
}
```

#### Delete Campaign

> **Destructive operation.** Deleting a campaign is irreversible and will stop all ad delivery. Confirm the campaign ID and its current status with the user before proceeding.

```bash
DELETE /linkedin/rest/adAccounts/{adAccountId}/adCampaigns/{campaignId}
```

### Campaign Status Values

| Status | Description |
|--------|-------------|
| `DRAFT` | Campaign is in draft mode |
| `ACTIVE` | Campaign is running |
| `PAUSED` | Campaign is paused |
| `ARCHIVED` | Campaign is archived |
| `COMPLETED` | Campaign has ended |
| `CANCELED` | Campaign was canceled |

### Campaign Objective Types

| Objective | Description |
|-----------|-------------|
| `BRAND_AWARENESS` | Increase brand visibility |
| `WEBSITE_VISITS` | Drive traffic to website |
| `ENGAGEMENT` | Increase post engagement |
| `VIDEO_VIEWS` | Maximize video views |
| `LEAD_GENERATION` | Collect leads via Lead Gen Forms |
| `WEBSITE_CONVERSIONS` | Drive website conversions |
| `JOB_APPLICANTS` | Attract job applications |

### Organizations

#### List Organization ACLs

Get organizations the authenticated user has access to:

```bash
GET /linkedin/rest/organizationAcls?q=roleAssignee
LinkedIn-Version: 202506
```

**Response:**
```json
{
  "paging": {
    "start": 0,
    "count": 10,
    "total": 2
  },
  "elements": [
    {
      "role": "ADMINISTRATOR",
      "organization": "urn:li:organization:12345",
      "state": "APPROVED"
    }
  ]
}
```

#### Get Organization

```bash
GET /linkedin/rest/organizations/{organizationId}
LinkedIn-Version: 202506
```

#### Lookup Organization by Vanity Name

```bash
GET /linkedin/rest/organizations?q=vanityName&vanityName={vanityName}
```

**Example:**
```bash
GET /linkedin/rest/organizations?q=vanityName&vanityName=microsoft
```

**Response:**
```json
{
  "elements": [
    {
      "vanityName": "microsoft",
      "localizedName": "Microsoft",
      "website": {
        "localized": {"en_US": "https://news.microsoft.com/"}
      }
    }
  ]
}
```

#### Get Organization Share Statistics

```bash
GET /linkedin/rest/organizationalEntityShareStatistics?q=organizationalEntity&organizationalEntity={orgUrn}
```

**Example:**
```bash
GET /linkedin/rest/organizationalEntityShareStatistics?q=organizationalEntity&organizationalEntity=urn:li:organization:12345
```

#### Get Organization Posts

```bash
GET /linkedin/rest/posts?q=author&author={orgUrn}
```

**Example:**
```bash
GET /linkedin/rest/posts?q=author&author=urn:li:organization:12345
```

### Media Upload (REST API)

The REST API provides modern media upload endpoints. All require version header `LinkedIn-Version: 202506`.

#### Initialize Image Upload

```bash
POST /linkedin/rest/images?action=initializeUpload
Content-Type: application/json
LinkedIn-Version: 202506

{
  "initializeUploadRequest": {
    "owner": "urn:li:person:{personId}"
  }
}
```

**Response:**
```json
{
  "value": {
    "uploadUrlExpiresAt": 1770541529250,
    "uploadUrl": "https://www.linkedin.com/dms-uploads/...",
    "image": "urn:li:image:D4D10AQH4GJAjaFCkHQ"
  }
}
```

Use the `uploadUrl` to PUT your image binary, then use the `image` URN in your post.

#### Create a Video Post

Video uploads are a 4-step process: initialize, upload binary, finalize, then create the post.

> **CRITICAL — URL Encoding:** The upload URL returned by the initialize step contains URL-encoded characters (e.g., `%253D`) that get corrupted when passed through shell variables or `curl`. You **MUST** use Python `urllib` for the entire flow — parse the JSON response and use the URL directly in Python without passing it through the shell. This is the only reliable approach.

**Complete working example:**

```bash
python <<'EOF'
import urllib.request, os, json

GATEWAY = 'https://api.maton.ai'
HEADERS = {
    'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
    'Content-Type': 'application/json',
    'LinkedIn-Version': '202506',
    'X-Restli-Protocol-Version': '2.0.0',
}

# Step 0: Get person ID
req = urllib.request.Request(f'{GATEWAY}/linkedin/rest/me')
for k, v in HEADERS.items(): req.add_header(k, v)
person_id = json.load(urllib.request.urlopen(req))['id']
owner = f'urn:li:person:{person_id}'

# Step 1: Initialize upload (via gateway)
file_path = '/path/to/video.mp4'
file_size = os.path.getsize(file_path)

init_data = json.dumps({
    'initializeUploadRequest': {
        'owner': owner,
        'fileSizeBytes': file_size,
        'uploadCaptions': False,
        'uploadThumbnail': False,
    }
}).encode()

req = urllib.request.Request(f'{GATEWAY}/linkedin/rest/videos?action=initializeUpload', data=init_data, method='POST')
for k, v in HEADERS.items(): req.add_header(k, v)
init_resp = json.load(urllib.request.urlopen(req))
upload_url = init_resp['value']['uploadInstructions'][0]['uploadUrl']
video_urn = init_resp['value']['video']

# Step 2: Upload binary DIRECTLY to LinkedIn's pre-signed URL (NOT through the gateway)
# The upload URL points to www.linkedin.com — it is pre-signed and needs NO Authorization header.
# IMPORTANT: Use the URL exactly as returned by json.load() — do NOT pass it through shell variables.
with open(file_path, 'rb') as f:
    video_data = f.read()

upload_req = urllib.request.Request(upload_url, data=video_data, method='PUT')
upload_req.add_header('Content-Type', 'application/octet-stream')
upload_resp = urllib.request.urlopen(upload_req)
etag = upload_resp.headers['etag']

# Step 3: Finalize upload (via gateway)
finalize_data = json.dumps({
    'finalizeUploadRequest': {
        'video': video_urn,
        'uploadToken': '',
        'uploadedPartIds': [etag],
    }
}).encode()

req = urllib.request.Request(f'{GATEWAY}/linkedin/rest/videos?action=finalizeUpload', data=finalize_data, method='POST')
for k, v in HEADERS.items(): req.add_header(k, v)
urllib.request.urlopen(req)

# Step 4: Create post with video (via gateway)
post_data = json.dumps({
    'author': owner,
    'lifecycleState': 'PUBLISHED',
    'visibility': 'PUBLIC',
    'commentary': 'Check out this video!',
    'distribution': {'feedDistribution': 'MAIN_FEED'},
    'content': {'media': {'id': video_urn}},
}).encode()

req = urllib.request.Request(f'{GATEWAY}/linkedin/rest/posts', data=post_data, method='POST')
for k, v in HEADERS.items(): req.add_header(k, v)
resp = urllib.request.urlopen(req)
print(f'Video post created! {resp.headers.get("location")}')
EOF
```

**How it works:**
- Steps 1, 3, 4 go through the gateway (`api.maton.ai/linkedin/...`) — Maton injects your OAuth token automatically.
- Step 2 goes **directly** to LinkedIn's pre-signed upload URL (`www.linkedin.com/dms-uploads/...`) — no auth header needed, no gateway.
- The `etag` from the upload response is required for the finalize step.
- For large videos (>4MB), LinkedIn returns multiple `uploadInstructions` — upload each chunk to its respective URL and collect all etags.

**Video specifications:**
- Length: 3 seconds to 30 minutes
- File size: 75KB to 500MB
- Format: MP4

#### Initialize Document Upload

```bash
POST /linkedin/rest/documents?action=initializeUpload
Content-Type: application/json
LinkedIn-Version: 202506

{
  "initializeUploadRequest": {
    "owner": "urn:li:person:{personId}"
  }
}
```

**Response:**
```json
{
  "value": {
    "uploadUrlExpiresAt": 1770541530896,
    "uploadUrl": "https://www.linkedin.com/dms-uploads/...",
    "document": "urn:li:document:D4D10AQHr-e30QZCAjQ"
  }
}
```

### Ad Targeting

> **Compliance note:** Ad targeting involves sensitive audience attributes (age, gender, location, employers). Ensure all targeting criteria comply with LinkedIn's [Advertising Policies](https://www.linkedin.com/legal/ads-policy) and applicable anti-discrimination laws. Do not use protected characteristics for discriminatory exclusion in housing, employment, or credit advertising.

#### Get Available Targeting Facets

```bash
GET /linkedin/rest/adTargetingFacets
```

Returns all available targeting facets for ad campaigns (31 facets including employers, degrees, skills, locations, industries, etc.).

**Response:**
```json
{
  "elements": [
    {
      "facetName": "skills",
      "adTargetingFacetUrn": "urn:li:adTargetingFacet:skills",
      "entityTypes": ["SKILL"],
      "availableEntityFinders": ["AD_TARGETING_FACET", "TYPEAHEAD"]
    },
    {
      "facetName": "industries",
      "adTargetingFacetUrn": "urn:li:adTargetingFacet:industries"
    }
  ]
}
```

Available targeting facets include:
- `skills` - Member skills
- `industries` - Industry categories
- `titles` - Job titles
- `seniorities` - Seniority levels
- `degrees` - Educational degrees
- `schools` - Educational institutions
- `employers` / `employersPast` - Current/past employers
- `locations` / `geoLocations` - Geographic targeting
- `companySize` - Company size ranges
- `genders` - Gender targeting
- `ageRanges` - Age range targeting

## Getting Your Person ID

To create posts, you need your LinkedIn person ID. Get it from the `/rest/me` endpoint:

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/linkedin/rest/me')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('LinkedIn-Version', '202506')
result = json.load(urllib.request.urlopen(req))
print(f"Your person URN: urn:li:person:{result['id']}")
EOF
```

## Code Examples

### JavaScript - Create Text Post

```javascript
const personId = 'YOUR_PERSON_ID';

const response = await fetch(
  'https://api.maton.ai/linkedin/rest/posts',
  {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`,
      'Content-Type': 'application/json',
      'LinkedIn-Version': '202506'
    },
    body: JSON.stringify({
      author: `urn:li:person:${personId}`,
      lifecycleState: 'PUBLISHED',
      visibility: 'PUBLIC',
      commentary: 'Hello from the API!',
      distribution: {
        feedDistribution: 'MAIN_FEED'
      }
    })
  }
);
```

### Python - Create Text Post

```python
import os
import requests

person_id = 'YOUR_PERSON_ID'

response = requests.post(
    'https://api.maton.ai/linkedin/rest/posts',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'Content-Type': 'application/json',
        'LinkedIn-Version': '202506'
    },
    json={
        'author': f'urn:li:person:{person_id}',
        'lifecycleState': 'PUBLISHED',
        'visibility': 'PUBLIC',
        'commentary': 'Hello from the API!',
        'distribution': {
            'feedDistribution': 'MAIN_FEED'
        }
    }
)
```

## Rate Limits

| Throttle Type | Daily Limit (UTC) |
|---------------|-------------------|
| Member | 150 requests/day |
| Application | 100,000 requests/day |

## Little Text Format (Commentary Field)

The `commentary` field in posts uses LinkedIn's "Little Text Format". **Reserved characters must be escaped with a backslash or the post content will be truncated.**

### Reserved Characters (Must Escape)

| Character | Escape As |
|-----------|-----------|
| `\` | `\\` |
| `\|` | `\\|` |
| `{` | `\{` |
| `}` | `\}` |
| `@` | `\@` |
| `[` | `\[` |
| `]` | `\]` |
| `(` | `\(` |
| `)` | `\)` |
| `<` | `\<` |
| `>` | `\>` |
| `#` | `\#` |
| `*` | `\*` |
| `_` | `\_` |
| `~` | `\~` |

### Example

```json
{
  "commentary": "Hello\\! Check out these bullet points:\\n\\n\\* Point 1\\n\\* Point 2\\n\\* More info \\(details inside\\)"
}
```

### Mentions and Hashtags

Use Little Text Format syntax for mentions and hashtags:

- **Mention a person:** `@[Display Name](urn:li:person:123)`
- **Mention an organization:** `@[Company Name](urn:li:organization:456)`
- **Hashtag (template):** `{hashtag|\\#|MyTag}`
- **Hashtag (simple):** `#hashtag` (single words only)

### Python Helper Function

```python
def escape_linkedin_commentary(text):
    """Escape reserved characters for LinkedIn Little Text Format."""
    reserved = ['\\', '|', '{', '}', '@', '[', ']', '(', ')', '<', '>', '#', '*', '_', '~']
    for char in reserved:
        text = text.replace(char, '\\' + char)
    return text

# Usage
commentary = escape_linkedin_commentary("Check this out! Details (inside) #tech")
# Result: "Check this out\\! Details \\(inside\\) \\#tech"
```

## Notes

- Person IDs are unique per application and not transferable across apps
- **Commentary uses Little Text Format** — escape reserved characters (`\|{}@[]()<>#*_~`) with backslash or content will be truncated
- The `author` field must use URN format: `urn:li:person:{personId}`
- All posts require `lifecycleState: "PUBLISHED"`
- Image uploads are a 3-step process: initialize, upload binary, create post
- Video uploads are a 4-step process: initialize, upload binary, finalize, create post
- **Media upload URLs (images, videos, documents) point to `www.linkedin.com`, NOT `api.linkedin.com`.** These are pre-signed URLs that do NOT go through the gateway and do NOT require an Authorization header. You MUST use Python `urllib` to handle these URLs — do NOT pass them through shell variables or use `curl`, as the URL contains encoded characters (`%253D`) that get corrupted by shell expansion.
- Include `LinkedIn-Version: 202506` header for all REST API calls
- Profile picture URLs may expire; re-fetch if needed

## Error Handling

| Status | Meaning |
|--------|---------|
| 400 | Missing LinkedIn connection or invalid request |
| 401 | Invalid or missing Maton API key |
| 403 | Insufficient permissions (check OAuth scopes) |
| 404 | Resource not found |
| 422 | Invalid request body or URN format |
| 429 | Rate limited |
| 4xx/5xx | Passthrough error from LinkedIn API |

### Error Response Format

```json
{
  "status": 403,
  "serviceErrorCode": 100,
  "code": "ACCESS_DENIED",
  "message": "Not enough permissions to access resource"
}
```

### Troubleshooting: API Key Issues

1. Check that the `MATON_API_KEY` environment variable is set:

```bash
echo $MATON_API_KEY
```

2. Verify the API key is valid by listing connections:

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Troubleshooting: Invalid App Name

1. Ensure your URL path starts with `linkedin`. For example:

- Correct: `https://api.maton.ai/linkedin/rest/me`
- Incorrect: `https://api.maton.ai/rest/me`

## OAuth Scopes

| Scope | Description |
|-------|-------------|
| `openid` | OpenID Connect authentication |
| `profile` | Read basic profile |
| `email` | Read email address |
| `w_member_social` | Create, modify, and delete posts |
| `r_organization_social` | Read organization posts and statistics |
| `w_organization_social` | Create and manage organization posts |
| `r_ads` | Read advertising account data |
| `rw_ads` | Create and manage ad campaigns, campaign groups, and accounts |

Note: Available scopes depend on your LinkedIn OAuth connection. Verify granted scopes at your [Maton connection settings](https://maton.ai/settings) before attempting advertising operations.

## Resources

- [LinkedIn API Overview](https://learn.microsoft.com/en-us/linkedin/)
- [Share on LinkedIn Guide](https://learn.microsoft.com/en-us/linkedin/consumer/integrations/self-serve/share-on-linkedin)
- [Profile API](https://learn.microsoft.com/en-us/linkedin/shared/integrations/people/profile-api)
- [Sign In with LinkedIn](https://learn.microsoft.com/en-us/linkedin/consumer/integrations/self-serve/sign-in-with-linkedin-v2)
- [Authentication Guide](https://learn.microsoft.com/en-us/linkedin/shared/authentication/authentication)
- [Marketing API](https://learn.microsoft.com/en-us/linkedin/marketing/)
- [Ad Accounts](https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads/account-structure/create-and-manage-accounts)
- [Campaign Management](https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads/account-structure/create-and-manage-campaigns)
- [Ad Library API](https://www.linkedin.com/ad-library/api/)
- [Maton Community](https://discord.com/invite/dBfFAcefs2)
- [Maton Support](mailto:support@maton.ai)
