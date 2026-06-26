# Konektor Agent API

> Version: 2.2.0
> Last updated: 2026-03-11

Machine-readable API documentation for AI agents, LLMs, and automation tools.

Base URL: `https://konektor.id`

Documentation: [https://konektor.id/docs/api/agent-api](https://konektor.id/docs/api/agent-api)

## Requirements

| Key | Value |
|-----|-------|
| Authentication | Bearer token (API key) |
| Environment Variable | `KONEKTOR_API_KEY` |
| Minimum Scopes | Depends on endpoint (see Scopes Reference) |
| Base URL | `https://konektor.id` |
| Transport | HTTPS only |
| Content-Type | `application/json` |

To use this API, set the `KONEKTOR_API_KEY` environment variable with a valid API key. Keys are created in the Konektor dashboard under Workspace Settings → API Keys. Each key must be assigned the minimum scopes required for the intended operations.

## Authentication

All endpoints (except SKILL.md) require a Bearer token:

```
Authorization: Bearer <api_key>
```

API keys are scoped. Available scopes: `agent.leads.read, agent.leads.write, agent.analytics.read, agent.conversions.read, agent.workspace.read, agent.support.write`

Each endpoint requires a specific scope — requests without the required scope receive HTTP 403.

## Endpoints

### SKILL.md (this document)

| | |
|---|---|
| Method | GET |
| Path | `/api/v2/agent/SKILL.md` |
| Auth | None (public) |
| Scope | — |

---

### List Leads

| | |
|---|---|
| Method | GET |
| Path | `/api/v2/agent/leads` |
| Scope | `agent.leads.read` |

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| page | integer | No | Page number (min: 1) |
| limit | integer | No | Items per page (1–100, default: 50) |
| cursor | string | No | Cursor for cursor-based pagination |
| status | string | No | Filter by status: pageview, new, contacted, responded, qualified, hot, proposal, negotiation, invoice, won, lost |
| priority | string | No | Filter by priority: low, medium, high, urgent |
| source | string | No | Filter by source: website, whatsapp, phone, email, referral, social, ads, event, other |
| adPlatform | string | No | Filter by ad platform: meta, google, tiktok, linkedin, posthog, other |
| assignedTo | string (UUID) | No | Filter by assigned team member |
| createdFrom | string (ISO 8601) | No | Filter leads created after this date |
| createdTo | string (ISO 8601) | No | Filter leads created before this date |
| search | string | No | Search by name, email, phone, uniqueCode, or externalRef (max 200 chars) |
| sortBy | string | No | Sort field: createdAt, updatedAt (default: createdAt) |
| sortOrder | string | No | Sort order: asc, desc (default: desc) |

**Example:**

```bash
curl -H "Authorization: Bearer YOUR_KEY" \
  "https://konektor.id/api/v2/agent/leads?status=new&limit=10"
```

```json
{
  "success": true,
  "data": [
    {
      "id": "lead_abc123",
      "uniqueCode": "KNK-001",
      "firstName": "Budi",
      "lastName": "Santoso",
      "email": "budi@example.com",
      "phone": "+6281234567890",
      "status": "new",
      "priority": "medium",
      "source": "ads",
      "adPlatform": "meta",
      "assignedTo": null,
      "estimatedValue": 5000000,
      "actualValue": null,
      "notes": null,
      "createdAt": "2025-01-15T10:30:00.000Z",
      "updatedAt": "2025-01-15T10:30:00.000Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 42,
    "totalPages": 5,
    "nextCursor": "eyJpZCI6ImxlYWRfYWJjMTIzIn0"
  }
}
```

---

### Get Lead

| | |
|---|---|
| Method | GET |
| Path | `/api/v2/agent/leads/:id` |
| Scope | `agent.leads.read` |

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| id | string | Lead ID |

**Example:**

```bash
curl -H "Authorization: Bearer YOUR_KEY" \
  "https://konektor.id/api/v2/agent/leads/lead_abc123"
```

```json
{
  "success": true,
  "data": {
    "id": "lead_abc123",
    "uniqueCode": "KNK-001",
    "firstName": "Budi",
    "lastName": "Santoso",
    "email": "budi@example.com",
    "phone": "+6281234567890",
    "status": "new",
    "priority": "medium",
    "source": "ads",
    "adPlatform": "meta",
    "assignedTo": null,
    "estimatedValue": 5000000,
    "actualValue": null,
    "notes": null,
    "createdAt": "2025-01-15T10:30:00.000Z",
    "updatedAt": "2025-01-15T10:30:00.000Z"
  }
}
```

---

### Create Lead

| | |
|---|---|
| Method | POST |
| Path | `/api/v2/agent/leads` |
| Scope | `agent.leads.write` |

**Request Body (JSON):**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| firstName | string | Yes | First name (1–100 chars) |
| lastName | string | No | Last name (max 100 chars) |
| email | string | No | Email address |
| phone | string | No | Phone number (max 20 chars) |
| status | string | No | Lead status (default: new) |
| priority | string | No | Priority: low, medium, high, urgent |
| source | string | No | Source: website, whatsapp, phone, email, referral, social, ads, event, other |
| adPlatform | string | No | Ad platform: meta, google, tiktok, linkedin, posthog, other |
| notes | string | No | Notes (max 5000 chars) |
| uniqueCode | string | No | Custom unique code (max 100 chars) |
| externalRef | string | No | External reference ID (max 150 chars) |
| assignedTo | string (UUID) | No | Assign to team member |
| estimatedValue | number | No | Estimated deal value |
| actualValue | number | No | Actual deal value |

**Example:**

```bash
curl -X POST -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"firstName":"Andi","email":"andi@example.com","status":"new","source":"ads","adPlatform":"meta"}' \
  "https://konektor.id/api/v2/agent/leads"
```

```json
{
  "success": true,
  "data": {
    "id": "lead_xyz789",
    "uniqueCode": "KNK-002",
    "firstName": "Andi",
    "email": "andi@example.com",
    "status": "new",
    "priority": "medium",
    "source": "ads",
    "adPlatform": "meta",
    "createdAt": "2025-01-16T08:00:00.000Z",
    "updatedAt": "2025-01-16T08:00:00.000Z"
  }
}
```

---

### Update Lead

| | |
|---|---|
| Method | PATCH |
| Path | `/api/v2/agent/leads/:id` |
| Scope | `agent.leads.write` |

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| id | string | Lead ID |

**Request Body (JSON):** Same fields as Create Lead, all optional.

**Example:**

```bash
curl -X PATCH -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"status":"contacted","notes":"Called via WhatsApp"}' \
  "https://konektor.id/api/v2/agent/leads/lead_xyz789"
```

```json
{
  "success": true,
  "data": {
    "id": "lead_xyz789",
    "uniqueCode": "KNK-002",
    "firstName": "Andi",
    "status": "contacted",
    "notes": "Called via WhatsApp",
    "updatedAt": "2025-01-16T09:15:00.000Z"
  }
}
```

---

### Analytics Summary

| | |
|---|---|
| Method | GET |
| Path | `/api/v2/agent/analytics/summary` |
| Scope | `agent.analytics.read` |

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| timeframe | string | No | Preset timeframe: today, last_7_days, last_30_days, current_week, current_month, all_time (default: last_30_days) |
| from | string (ISO 8601) | No | Custom start date (overrides timeframe) |
| to | string (ISO 8601) | No | Custom end date (overrides timeframe) |

**Example:**

```bash
curl -H "Authorization: Bearer YOUR_KEY" \
  "https://konektor.id/api/v2/agent/analytics/summary?timeframe=last_7_days"
```

```json
{
  "success": true,
  "data": {
    "totalLeads": 156,
    "newLeads": 42,
    "contactedLeads": 38,
    "totalConversions": 12,
    "totalConversionValue": 45000000,
    "timeframe": "last_7_days",
    "period": {
      "from": "2025-01-09T00:00:00.000Z",
      "to": "2025-01-16T00:00:00.000Z"
    }
  }
}
```

---

### Analytics Funnel

| | |
|---|---|
| Method | GET |
| Path | `/api/v2/agent/analytics/funnel` |
| Scope | `agent.analytics.read` |

**Query Parameters:** Same as Analytics Summary.

**Example:**

```bash
curl -H "Authorization: Bearer YOUR_KEY" \
  "https://konektor.id/api/v2/agent/analytics/funnel?timeframe=current_month"
```

```json
{
  "success": true,
  "data": [
    { "status": "new", "count": 42, "percentage": 26.92 },
    { "status": "contacted", "count": 38, "percentage": 24.36 },
    { "status": "qualified", "count": 25, "percentage": 16.03 },
    { "status": "proposal", "count": 20, "percentage": 12.82 },
    { "status": "won", "count": 12, "percentage": 7.69 },
    { "status": "lost", "count": 19, "percentage": 12.18 }
  ]
}
```

---

### Campaign Performance

| | |
|---|---|
| Method | GET |
| Path | `/api/v2/agent/analytics/campaigns` |
| Scope | `agent.analytics.read` |

**Query Parameters:** Same as Analytics Summary.

**Example:**

```bash
curl -H "Authorization: Bearer YOUR_KEY" \
  "https://konektor.id/api/v2/agent/analytics/campaigns?timeframe=last_30_days"
```

```json
{
  "success": true,
  "data": [
    {
      "campaignName": "Promo Januari",
      "adPlatform": "meta",
      "leads": 85,
      "conversions": 8,
      "conversionValue": 32000000
    },
    {
      "campaignName": "Brand Awareness",
      "adPlatform": "google",
      "leads": 45,
      "conversions": 3,
      "conversionValue": 12000000
    }
  ]
}
```

---

### Conversion Sync Status

| | |
|---|---|
| Method | GET |
| Path | `/api/v2/agent/conversions/status` |
| Scope | `agent.conversions.read` |

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| timeframe | string | No | Preset timeframe: today, last_7_days, last_30_days, current_week, current_month, all_time (default: last_30_days) |
| from | string (ISO 8601) | No | Custom start date |
| to | string (ISO 8601) | No | Custom end date |
| platform | string | No | Filter by ad platform: meta, google, tiktok, linkedin, posthog, other |

**Example:**

```bash
curl -H "Authorization: Bearer YOUR_KEY" \
  "https://konektor.id/api/v2/agent/conversions/status?timeframe=last_7_days"
```

```json
{
  "success": true,
  "data": {
    "pending": 5,
    "synced": 42,
    "partial": 2,
    "failed": 1,
    "none": 106
  }
}
```

---

### Pending Conversions

| | |
|---|---|
| Method | GET |
| Path | `/api/v2/agent/conversions/pending` |
| Scope | `agent.conversions.read` |

**Example:**

```bash
curl -H "Authorization: Bearer YOUR_KEY" \
  "https://konektor.id/api/v2/agent/conversions/pending"
```

```json
{
  "success": true,
  "data": [
    {
      "leadId": "lead_abc123",
      "uniqueCode": "KNK-001",
      "status": "won",
      "adPlatform": "meta",
      "conversionSyncStatus": "pending",
      "lastConversionSyncAt": null
    },
    {
      "leadId": "lead_def456",
      "uniqueCode": "KNK-005",
      "status": "won",
      "adPlatform": "google",
      "conversionSyncStatus": "failed",
      "lastConversionSyncAt": "2025-01-15T12:00:00.000Z"
    }
  ]
}
```

---

### Workspace Info

| | |
|---|---|
| Method | GET |
| Path | `/api/v2/agent/workspace` |
| Scope | `agent.workspace.read` |

**Example:**

```bash
curl -H "Authorization: Bearer YOUR_KEY" \
  "https://konektor.id/api/v2/agent/workspace"
```

```json
{
  "success": true,
  "data": {
    "displayName": "Toko Budi Online",
    "timezone": "Asia/Jakarta",
    "currency": "IDR",
    "language": "id",
    "dateFormat": "DD/MM/YYYY",
    "trackingCode": "KNK-abc123",
    "subscription": {
      "plan": "pro",
      "status": "active",
      "interval": "monthly",
      "currentPeriodEnd": "2025-02-15T00:00:00.000Z"
    },
    "usage": {
      "leadsPerDay": { "limit": 500, "current": 23 },
      "teamMembers": 5,
      "activeRotators": 2
    }
  }
}
```

---

### Create Support Ticket

| | |
|---|---|
| Method | POST |
| Path | `/api/v2/agent/support/tickets` |
| Scope | `agent.support.write` |

**Request Body (JSON):**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| subject | string | Yes | Ticket subject (3–180 chars) |
| message | string | Yes | Ticket body (1–10000 chars) |
| priority | string | No | Priority: ${ticketPriorities} (default: normal) |

**Example:**

```bash
curl -X POST -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"subject":"Tracking pixel not firing","message":"Our Meta pixel events stopped syncing since yesterday. Workspace ID: ws_abc123.","priority":"high"}' \
  "https://konektor.id/api/v2/agent/support/tickets"
```

```json
{
  "success": true,
  "data": {
    "ticketId": "t_abc123",
    "ticketRef": "A1B2C-3D4E",
    "subject": "Tracking pixel not firing",
    "status": "new",
    "priority": "high",
    "createdAt": "2026-03-10T08:00:00.000Z"
  }
}
```

**Ticket Statuses:** ${ticketStatuses}

**Ticket Priorities:** ${ticketPriorities}

## Rate Limits

Rate limits are per workspace (shared across all API keys) and vary by plan:

| Plan | Limit |
|------|-------|
| starter | 60 req/min |
| pro | 200 req/min |
| enterprise | 600 req/min |
| custom | 200 req/min |

Rate limit headers are included in every response:

- `X-RateLimit-Limit`: Maximum requests per minute
- `X-RateLimit-Remaining`: Remaining requests in current window
- `X-RateLimit-Reset`: Unix timestamp when the window resets

When rate limited, the response includes a `Retry-After` header (seconds).

## Error Handling

All errors follow a consistent JSON format:

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable description",
    "details": null
  }
}
```

### Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| UNAUTHORIZED | 401 | Missing, invalid, expired, or revoked API key |
| FORBIDDEN | 403 | Insufficient scope or plan does not support Agent API |
| VALIDATION_ERROR | 400 | Invalid request parameters (details contains field-level errors) |
| NOT_FOUND | 404 | Resource not found or soft-deleted |
| RATE_LIMITED | 429 | Rate limit exceeded |
| INTERNAL_ERROR | 500 | Unexpected server error |

### Validation Error Example

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request parameters",
    "details": {
      "firstName": "Required",
      "email": "Invalid email"
    }
  }
}
```

## Response Headers

Every response (except SKILL.md) includes:

| Header | Description |
|--------|-------------|
| X-Request-Id | Unique request ID (UUID) for debugging |
| X-RateLimit-Limit | Max requests per minute |
| X-RateLimit-Remaining | Remaining requests |
| X-RateLimit-Reset | Window reset timestamp (Unix seconds) |

## Scopes Reference

| Scope | Description |
|-------|-------------|
| agent.leads.read | Read leads (list, get) |
| agent.leads.write | Create and update leads |
| agent.analytics.read | Read analytics (summary, funnel, campaigns) |
| agent.conversions.read | Read conversion sync status and pending conversions |
| agent.workspace.read | Read workspace info and subscription |
| agent.support.write | Create support tickets |

## Values Reference

**Lead Statuses:** pageview, new, contacted, responded, qualified, hot, proposal, negotiation, invoice, won, lost

**Lead Priorities:** low, medium, high, urgent

**Lead Sources:** website, whatsapp, phone, email, referral, social, ads, event, other

**Ad Platforms:** meta, google, tiktok, linkedin, posthog, other

**Timeframes:** today, last_7_days, last_30_days, current_week, current_month, all_time

**Error Codes:** UNAUTHORIZED, FORBIDDEN, VALIDATION_ERROR, NOT_FOUND, RATE_LIMITED, INTERNAL_ERROR
