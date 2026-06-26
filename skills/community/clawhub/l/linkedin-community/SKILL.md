---
name: linkedin-community-management
description: |
  LinkedIn Community Management API integration with managed OAuth. Manage organization pages, posts, comments, reactions, and analytics.
  Use this skill when users want to create or manage LinkedIn posts, comment on posts, react to content, look up organizations, or retrieve follower/page/share statistics.
  For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
  Requires network access and valid Maton API key.
metadata:
  author: maton
  version: "1.0"
  openclaw:
    emoji: 🧠
    homepage: "https://maton.ai"
    requires:
      env:
        - MATON_API_KEY
---

# LinkedIn Community Management

Access the LinkedIn Community Management API with managed OAuth authentication. Manage organization pages, create and manage posts, comments, reactions, and retrieve analytics.

## Quick Start

```bash
# Look up an organization by vanity name
curl -s -X GET "https://api.maton.ai/linkedin-community-management/rest/organizations?q=vanityName&vanityName=LinkedIn" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Linkedin-Version: 202605" \
  -H "X-Restli-Protocol-Version: 2.0.0"
```

## Base URL

```
https://api.maton.ai/linkedin-community-management/rest/{resource}
```

The gateway proxies requests to `api.linkedin.com/rest` and automatically injects your OAuth token.

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

All LinkedIn API requests require these additional headers:

| Header | Value | Description |
|--------|-------|-------------|
| `Linkedin-Version` | `YYYYMM` (e.g., `202605`) | API version |
| `X-Restli-Protocol-Version` | `2.0.0` | Protocol version |

## Connection Management

Manage your LinkedIn OAuth connections at `https://api.maton.ai`.

### List Connections

```bash
curl -s -X GET "https://api.maton.ai/connections?app=linkedin-community-management&status=ACTIVE" \
  -H "Authorization: Bearer $MATON_API_KEY"
```

### Create Connection

```bash
curl -s -X POST "https://api.maton.ai/connections" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -d '{"app": "linkedin-community-management"}'
```

### Get Connection

```bash
curl -s -X GET "https://api.maton.ai/connections/{connection_id}" \
  -H "Authorization: Bearer $MATON_API_KEY"
```

**Response:**
```json
{
  "connection": {
    "connection_id": "{connection_id}",
    "status": "ACTIVE",
    "creation_time": "2025-12-08T07:20:53.488460Z",
    "last_updated_time": "2026-01-31T20:03:32.593153Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "linkedin-community-management",
    "metadata": {}
  }
}
```

Open the returned `url` in a browser to complete OAuth authorization.

### Delete Connection

```bash
curl -s -X DELETE "https://api.maton.ai/connections/{connection_id}" \
  -H "Authorization: Bearer $MATON_API_KEY"
```

### Specifying Connection

Always specify which connection to use with the `Maton-Connection` header to ensure requests go to the intended LinkedIn account:

```bash
curl -s -X GET "https://api.maton.ai/linkedin-community-management/rest/..." \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Maton-Connection: {connection_id}"
```

If you have multiple connections, always list them first and confirm the correct one with the user before making requests.

## Security & Permissions

- **All write operations require explicit user confirmation.** Before creating, editing, or deleting a post, comment, or reaction, confirm the target resource, intended content, and the LinkedIn identity (person or organization) with the user.
- Always verify the intended Maton connection and LinkedIn organization before performing actions.
- Access is scoped to the organizations and permissions granted to the connected LinkedIn account.

## API Reference

### Current Member Profile

#### Get Current Member

```bash
curl -s -X GET "https://api.maton.ai/linkedin-community-management/rest/me" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Linkedin-Version: 202605" \
  -H "X-Restli-Protocol-Version: 2.0.0"
```

**Response:**
```json
{
  "localizedLastName": "Smith",
  "localizedFirstName": "John",
  "id": "abc123XYZ",
  "vanityName": "john-smith",
  "localizedHeadline": "Software Engineer at Acme Corp"
}
```

### People Lookup

#### Get Person by ID

Look up a LinkedIn member's profile by their person ID. The person ID can be obtained from `/rest/me`, `organizationAcls`, post authors, or comment actors.

```bash
curl -s -g -X GET "https://api.maton.ai/linkedin-community-management/rest/people/(id:{personId})" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Linkedin-Version: 202605" \
  -H "X-Restli-Protocol-Version: 2.0.0"
```

**Response:**
```json
{
  "localizedLastName": "Smith",
  "profilePicture": {
    "displayImage": "urn:li:digitalmediaAsset:C5603AQFWsrW4dwGzmg"
  },
  "vanityName": "john-smith",
  "lastName": {
    "localized": {"en_US": "Smith"},
    "preferredLocale": {"country": "US", "language": "en"}
  },
  "firstName": {
    "localized": {"en_US": "John"},
    "preferredLocale": {"country": "US", "language": "en"}
  },
  "localizedHeadline": "Software Engineer at Acme Corp",
  "id": "abc123XYZ",
  "headline": {
    "localized": {"en_US": "Software Engineer at Acme Corp"},
    "preferredLocale": {"country": "US", "language": "en"}
  },
  "localizedFirstName": "John"
}
```

**Available fields:** `id`, `firstName`, `lastName`, `vanityName`, `localizedFirstName`, `localizedLastName`, `localizedHeadline`, `headline`, `profilePicture`

You can request a single field with the `fields` query parameter:

```bash
curl -s -g -X GET "https://api.maton.ai/linkedin-community-management/rest/people/(id:{personId})?fields=localizedHeadline" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Linkedin-Version: 202605" \
  -H "X-Restli-Protocol-Version: 2.0.0"
```

**Notes:**
- The `(id:{personId})` syntax uses Rest.li composite key format — parentheses are required
- Use `curl -g` to prevent shell glob expansion of parentheses
- Non-connected members may return `{"id": "private"}` with limited data
- The person ID comes from URNs like `urn:li:person:{personId}` found in org ACLs, post authors, and comment actors

### Organization Operations

#### Find Organization by Vanity Name

```bash
curl -s -X GET "https://api.maton.ai/linkedin-community-management/rest/organizations?q=vanityName&vanityName={vanityName}" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Linkedin-Version: 202605" \
  -H "X-Restli-Protocol-Version: 2.0.0"
```

#### Get Organization by ID (Admin Required)

```bash
curl -s -X GET "https://api.maton.ai/linkedin-community-management/rest/organizations/{organizationId}" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Linkedin-Version: 202605" \
  -H "X-Restli-Protocol-Version: 2.0.0"
```

#### Get Organization Follower Count

```bash
curl -s -X GET "https://api.maton.ai/linkedin-community-management/rest/networkSizes/urn%3Ali%3Aorganization%3A{orgId}?edgeType=COMPANY_FOLLOWED_BY_MEMBER" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Linkedin-Version: 202605" \
  -H "X-Restli-Protocol-Version: 2.0.0"
```

**Response:**
```json
{
  "firstDegreeSize": 33634367
}
```

#### Find Administered Organizations

```bash
curl -s -X GET "https://api.maton.ai/linkedin-community-management/rest/organizationAcls?q=roleAssignee&role=ADMINISTRATOR&state=APPROVED" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Linkedin-Version: 202605" \
  -H "X-Restli-Protocol-Version: 2.0.0"
```

#### Find Child Organizations (Brands)

```bash
curl -s -X GET "https://api.maton.ai/linkedin-community-management/rest/organizations?q=parentOrganization&parent=urn%3Ali%3Aorganization%3A{orgId}" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Linkedin-Version: 202605" \
  -H "X-Restli-Protocol-Version: 2.0.0"
```

### Posts Operations

#### Create a Post

```bash
curl -s -X POST "https://api.maton.ai/linkedin-community-management/rest/posts" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Linkedin-Version: 202605" \
  -H "X-Restli-Protocol-Version: 2.0.0" \
  -H "Content-Type: application/json" \
  -d '{
    "author": "urn:li:organization:{orgId}",
    "commentary": "Your post text here",
    "visibility": "PUBLIC",
    "distribution": {
      "feedDistribution": "MAIN_FEED",
      "targetEntities": [],
      "thirdPartyDistributionChannels": []
    },
    "lifecycleState": "PUBLISHED",
    "isReshareDisabledByAuthor": false
  }'
```

Returns `201` with `x-restli-id` header containing the post URN (e.g., `urn:li:share:123456`).

Author can be `urn:li:person:{personId}` for member posts or `urn:li:organization:{orgId}` for organization posts.

#### Create a Post with Media

```bash
curl -s -X POST "https://api.maton.ai/linkedin-community-management/rest/posts" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Linkedin-Version: 202605" \
  -H "X-Restli-Protocol-Version: 2.0.0" \
  -H "Content-Type: application/json" \
  -d '{
    "author": "urn:li:organization:{orgId}",
    "commentary": "Check out this video!",
    "visibility": "PUBLIC",
    "distribution": {
      "feedDistribution": "MAIN_FEED",
      "targetEntities": [],
      "thirdPartyDistributionChannels": []
    },
    "content": {
      "media": {
        "title": "Video title",
        "id": "urn:li:video:{videoId}"
      }
    },
    "lifecycleState": "PUBLISHED",
    "isReshareDisabledByAuthor": false
  }'
```

#### Create an Article Post

```bash
curl -s -X POST "https://api.maton.ai/linkedin-community-management/rest/posts" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Linkedin-Version: 202605" \
  -H "X-Restli-Protocol-Version: 2.0.0" \
  -H "Content-Type: application/json" \
  -d '{
    "author": "urn:li:organization:{orgId}",
    "commentary": "Great article on AI",
    "visibility": "PUBLIC",
    "distribution": {
      "feedDistribution": "MAIN_FEED",
      "targetEntities": [],
      "thirdPartyDistributionChannels": []
    },
    "content": {
      "article": {
        "source": "https://example.com/article",
        "thumbnail": "urn:li:image:{imageId}",
        "title": "Article Title",
        "description": "Article description"
      }
    },
    "lifecycleState": "PUBLISHED",
    "isReshareDisabledByAuthor": false
  }'
```

#### Get Post by URN

```bash
curl -s -X GET "https://api.maton.ai/linkedin-community-management/rest/posts/{encoded_postUrn}" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Linkedin-Version: 202605" \
  -H "X-Restli-Protocol-Version: 2.0.0"
```

URNs must be URL-encoded: `urn:li:share:123` becomes `urn%3Ali%3Ashare%3A123`.

#### Find Posts by Author (Organization)

```bash
curl -s -X GET "https://api.maton.ai/linkedin-community-management/rest/posts?author=urn%3Ali%3Aorganization%3A{orgId}&q=author&count=10&sortBy=LAST_MODIFIED" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Linkedin-Version: 202605" \
  -H "X-Restli-Protocol-Version: 2.0.0" \
  -H "X-RestLi-Method: FINDER"
```

**Parameters:**

| Field | Description | Required |
|-------|-------------|----------|
| author | Organization or Person URN (URL-encoded) | Yes |
| q | Must be `author` | Yes |
| count | Number of results (max 100, default 10) | No |
| start | Offset for pagination (default 0) | No |
| sortBy | `LAST_MODIFIED` or `CREATED` | No |

#### Update a Post

```bash
curl -s -X POST "https://api.maton.ai/linkedin-community-management/rest/posts/{encoded_postUrn}" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Linkedin-Version: 202605" \
  -H "X-Restli-Protocol-Version: 2.0.0" \
  -H "X-RestLi-Method: PARTIAL_UPDATE" \
  -H "Content-Type: application/json" \
  -d '{
    "patch": {
      "$set": {
        "commentary": "Updated post text"
      }
    }
  }'
```

Returns `204` on success. Only `commentary`, `contentCallToActionLabel`, `contentLandingPage`, and `lifecycleState` can be updated.

#### Delete a Post

```bash
curl -s -X DELETE "https://api.maton.ai/linkedin-community-management/rest/posts/{encoded_postUrn}" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Linkedin-Version: 202605" \
  -H "X-Restli-Protocol-Version: 2.0.0" \
  -H "X-RestLi-Method: DELETE"
```

Returns `204` on success.

#### Reshare a Post

```bash
curl -s -X POST "https://api.maton.ai/linkedin-community-management/rest/posts" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Linkedin-Version: 202605" \
  -H "X-Restli-Protocol-Version: 2.0.0" \
  -H "Content-Type: application/json" \
  -d '{
    "author": "urn:li:organization:{orgId}",
    "commentary": "Great insights!",
    "visibility": "PUBLIC",
    "distribution": {
      "feedDistribution": "MAIN_FEED",
      "targetEntities": [],
      "thirdPartyDistributionChannels": []
    },
    "lifecycleState": "PUBLISHED",
    "isReshareDisabledByAuthor": false,
    "reshareContext": {
      "parent": "urn:li:share:{originalPostId}"
    }
  }'
```

### Comments Operations

#### Get Comments on a Post

```bash
curl -s -X GET "https://api.maton.ai/linkedin-community-management/rest/socialActions/{encoded_postUrn}/comments" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Linkedin-Version: 202605" \
  -H "X-Restli-Protocol-Version: 2.0.0"
```

#### Get a Specific Comment

```bash
curl -s -X GET "https://api.maton.ai/linkedin-community-management/rest/socialActions/{encoded_postUrn}/comments/{commentId}" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Linkedin-Version: 202605" \
  -H "X-Restli-Protocol-Version: 2.0.0"
```

#### Create a Comment

```bash
curl -s -X POST "https://api.maton.ai/linkedin-community-management/rest/socialActions/{encoded_postUrn}/comments" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Linkedin-Version: 202605" \
  -H "X-Restli-Protocol-Version: 2.0.0" \
  -H "Content-Type: application/json" \
  -d '{
    "actor": "urn:li:organization:{orgId}",
    "object": "urn:li:activity:{activityId}",
    "message": {
      "text": "Your comment text"
    }
  }'
```

Returns `201` with `x-restli-id` header containing the comment ID.

#### Create a Nested Comment (Reply)

```bash
curl -s -X POST "https://api.maton.ai/linkedin-community-management/rest/socialActions/{encoded_commentUrn}/comments" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Linkedin-Version: 202605" \
  -H "X-Restli-Protocol-Version: 2.0.0" \
  -H "Content-Type: application/json" \
  -d '{
    "actor": "urn:li:organization:{orgId}",
    "object": "urn:li:share:{shareId}",
    "message": {
      "text": "Reply to comment"
    },
    "parentComment": "urn:li:comment:(urn:li:activity:{activityId},{commentId})"
  }'
```

#### Edit a Comment

```bash
curl -s -X POST "https://api.maton.ai/linkedin-community-management/rest/socialActions/{encoded_postUrn}/comments/{commentId}?actor=urn%3Ali%3Aorganization%3A{orgId}" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Linkedin-Version: 202605" \
  -H "X-Restli-Protocol-Version: 2.0.0" \
  -H "X-RestLi-Method: PARTIAL_UPDATE" \
  -H "Content-Type: application/json" \
  -d '{
    "patch": {
      "message": {
        "$set": {
          "text": "Updated comment text"
        }
      }
    }
  }'
```

#### Delete a Comment

```bash
curl -s -X DELETE "https://api.maton.ai/linkedin-community-management/rest/socialActions/{encoded_postUrn}/comments/{commentId}?actor=urn%3Ali%3Aorganization%3A{orgId}" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Linkedin-Version: 202605" \
  -H "X-Restli-Protocol-Version: 2.0.0"
```

### Reactions Operations

#### Create a Reaction

```bash
curl -s -X POST "https://api.maton.ai/linkedin-community-management/rest/reactions?actor=urn%3Ali%3Aorganization%3A{orgId}" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Linkedin-Version: 202605" \
  -H "X-Restli-Protocol-Version: 2.0.0" \
  -H "Content-Type: application/json" \
  -d '{
    "root": "urn:li:activity:{activityId}",
    "reactionType": "LIKE"
  }'
```

**Reaction types:** `LIKE`, `PRAISE` (Celebrate), `EMPATHY` (Love), `INTEREST` (Insightful), `APPRECIATION` (Support), `ENTERTAINMENT` (Funny).

#### Get Reactions on a Post

```bash
curl -s -X GET "https://api.maton.ai/linkedin-community-management/rest/reactions/(entity:{encoded_entityUrn})?q=entity" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Linkedin-Version: 202605" \
  -H "X-Restli-Protocol-Version: 2.0.0"
```

#### Delete a Reaction

```bash
curl -s -X DELETE "https://api.maton.ai/linkedin-community-management/rest/reactions/(actor:urn%3Ali%3Aperson%3A{personId},entity:{encoded_entityUrn})" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Linkedin-Version: 202605" \
  -H "X-Restli-Protocol-Version: 2.0.0"
```

Returns `204` on success.

### Statistics (Admin Required)

These endpoints require the authenticated member to be an `ADMINISTRATOR` of the organization.

#### Organization Follower Statistics (Lifetime)

```bash
curl -s -X GET "https://api.maton.ai/linkedin-community-management/rest/organizationalEntityFollowerStatistics?q=organizationalEntity&organizationalEntity=urn%3Ali%3Aorganization%3A{orgId}" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Linkedin-Version: 202605" \
  -H "X-Restli-Protocol-Version: 2.0.0"
```

Returns follower counts segmented by geo, function, industry, seniority, and staff count range.

#### Organization Follower Statistics (Time-Bound)

```bash
curl -s -X GET "https://api.maton.ai/linkedin-community-management/rest/organizationalEntityFollowerStatistics?q=organizationalEntity&organizationalEntity=urn%3Ali%3Aorganization%3A{orgId}&timeIntervals.timeGranularityType=DAY&timeIntervals.timeRange.start={startMs}&timeIntervals.timeRange.end={endMs}" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Linkedin-Version: 202605" \
  -H "X-Restli-Protocol-Version: 2.0.0"
```

`timeGranularityType` can be `DAY`, `WEEK`, or `MONTH`. Timestamps are milliseconds since epoch.

#### Organization Page Statistics (Lifetime)

```bash
curl -s -X GET "https://api.maton.ai/linkedin-community-management/rest/organizationPageStatistics?q=organization&organization=urn%3Ali%3Aorganization%3A{orgId}" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Linkedin-Version: 202605" \
  -H "X-Restli-Protocol-Version: 2.0.0"
```

#### Organization Page Statistics (Time-Bound)

```bash
curl -s -X GET "https://api.maton.ai/linkedin-community-management/rest/organizationPageStatistics?q=organization&organization=urn%3Ali%3Aorganization%3A{orgId}&timeIntervals.timeGranularityType=DAY&timeIntervals.timeRange.start={startMs}&timeIntervals.timeRange.end={endMs}" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Linkedin-Version: 202605" \
  -H "X-Restli-Protocol-Version: 2.0.0"
```

#### Organization Share Statistics (Lifetime)

```bash
curl -s -X GET "https://api.maton.ai/linkedin-community-management/rest/organizationalEntityShareStatistics?q=organizationalEntity&organizationalEntity=urn%3Ali%3Aorganization%3A{orgId}" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Linkedin-Version: 202605" \
  -H "X-Restli-Protocol-Version: 2.0.0"
```

**Response:**
```json
{
  "elements": [{
    "totalShareStatistics": {
      "uniqueImpressionsCount": 36430528,
      "shareCount": 0,
      "engagement": 0.029,
      "clickCount": 1999920,
      "likeCount": 0,
      "impressionCount": 67703905,
      "commentCount": 0
    },
    "organizationalEntity": "urn:li:organization:1337"
  }]
}
```

#### Organization Share Statistics (Time-Bound)

```bash
curl -s -X GET "https://api.maton.ai/linkedin-community-management/rest/organizationalEntityShareStatistics?q=organizationalEntity&organizationalEntity=urn%3Ali%3Aorganization%3A{orgId}&timeIntervals.timeGranularityType=DAY&timeIntervals.timeRange.start={startMs}&timeIntervals.timeRange.end={endMs}" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Linkedin-Version: 202605" \
  -H "X-Restli-Protocol-Version: 2.0.0"
```

#### Share Statistics for Specific Posts

```bash
curl -g -s -X GET "https://api.maton.ai/linkedin-community-management/rest/organizationalEntityShareStatistics?q=organizationalEntity&organizationalEntity=urn%3Ali%3Aorganization%3A{orgId}&shares=List(urn%3Ali%3Ashare%3A{shareId1},urn%3Ali%3Ashare%3A{shareId2})" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Linkedin-Version: 202605" \
  -H "X-Restli-Protocol-Version: 2.0.0"
```

## Pagination

LinkedIn uses offset-based pagination with `start` and `count` parameters:

```bash
GET /linkedin-community-management/rest/posts?author=...&q=author&count=10&start=0
```

Response includes pagination info:

```json
{
  "paging": {
    "start": 0,
    "count": 10,
    "links": [
      {
        "rel": "next",
        "href": "/rest/posts?q=author&author=...&count=10&start=10"
      }
    ],
    "total": 500
  },
  "elements": [...]
}
```

Use the `links[].href` with `rel: "next"` for the next page, or increment `start` by `count`.

## Mentions and Hashtags

### Mentioning an Organization

Use `@[Display Name](urn:li:organization:{orgId})` syntax in `commentary`:

```json
{
  "commentary": "Congrats to @[LinkedIn](urn:li:organization:1337) on the milestone!"
}
```

### Hashtags

Use `#keyword` syntax in `commentary`:

```json
{
  "commentary": "Follow best practices #coding #engineering"
}
```

## Code Examples

### JavaScript

```javascript
const baseUrl = 'https://api.maton.ai/linkedin-community-management/rest';
const headers = {
  'Authorization': `Bearer ${process.env.MATON_API_KEY}`,
  'Linkedin-Version': '202605',
  'X-Restli-Protocol-Version': '2.0.0'
};

// Find organization by vanity name
const response = await fetch(
  `${baseUrl}/organizations?q=vanityName&vanityName=LinkedIn`,
  { headers }
);
const data = await response.json();
```

### Python

```python
import os
import requests

BASE_URL = "https://api.maton.ai/linkedin-community-management/rest"
HEADERS = {
    "Authorization": f"Bearer {os.environ['MATON_API_KEY']}",
    "Linkedin-Version": "202605",
    "X-Restli-Protocol-Version": "2.0.0"
}

# Create a post
response = requests.post(
    f"{BASE_URL}/posts",
    headers={**HEADERS, "Content-Type": "application/json"},
    json={
        "author": "urn:li:organization:12345",
        "commentary": "Hello from Python!",
        "visibility": "PUBLIC",
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": []
        },
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False
    }
)
post_urn = response.headers.get("x-restli-id")
```

## Notes

- All URNs in URL path segments and query parameters must be URL-encoded (`:` -> `%3A`)
- Organization posts require `w_organization_social` permission and an admin role on the org
- Member posts require `w_member_social` permission
- Reading member posts requires `r_member_social` (restricted permission)
- The `Linkedin-Version` header is required on all requests (format: `YYYYMM`, e.g., `202605`). LinkedIn keeps roughly the last ~12 monthly versions active and returns HTTP 426 `NONEXISTENT_VERSION` for retired or future-dated versions — pin to a recent month and bump periodically
- Post content types: text-only, image (`urn:li:image:{id}`), video (`urn:li:video:{id}`), document (`urn:li:document:{id}`), article
- Statistics endpoints return data only for administered organizations
- Share statistics only cover the past 12 months (rolling window)
- The `MAYBE` (Curious) reaction type is deprecated since version 202307
- IMPORTANT: When using curl commands, use `curl -g` when URLs contain parentheses or brackets to disable glob parsing
- IMPORTANT: When piping curl output to `jq` or other commands, environment variables like `$MATON_API_KEY` may not expand correctly in some shell environments

## Error Handling

| Status | Meaning |
|--------|---------|
| 400 | Missing LinkedIn connection or invalid request parameters |
| 401 | Invalid or missing Maton API key |
| 403 | Insufficient permissions (check org admin role or OAuth scopes) |
| 404 | Resource not found |
| 429 | Rate limited |
| 4xx/5xx | Passthrough error from LinkedIn API |

## Resources

- [LinkedIn Community Management Overview](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/community-management-overview)
- [Posts API](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/posts-api)
- [Comments API](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/comments-api)
- [Reactions API](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/reactions-api)
- [Organization Lookup API](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/organizations/organization-lookup-api)
- [Follower Statistics](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/organizations/follower-statistics)
- [Page Statistics](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/organizations/page-statistics)
- [Share Statistics](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/organizations/share-statistics)
