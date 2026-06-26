# Retention Policies API

Source: https://www.essesseff.com/docs/api/apps#retention-policies

---

## GET /accounts/{account_slug}/organizations/{organization_login}/apps/{app_name}/retention-policies

List retention policies for an app

```
GET /api/v1/accounts/{account_slug}/organizations/{organization_login}/apps/{app_name}/retention-policies
```

### Description

Lists lifecycle-state retention policies for a specific essesseff app. Retention policies are defined per image lifecycle state (BUILD, DEV, RC, QA, STABLE, STAGING, PROD, REJECTED, EXPIRED, etc.). For each state, the endpoint flattens account-wide defaults and app-specific overrides into a single app-scoped policy (app-level overrides take precedence over account-level defaults).

### Path Parameters

#### account_slug (required)

The team account slug (name) associated with the API key

#### organization_login (required)

GitHub organization login where the app exists

#### app_name (required)

Name of the essesseff app

### Query Parameters

#### state (optional)

Filter by lifecycle state (or comma-separated list of states). Valid values include: BUILD, DEV, RC, QA, STABLE, STAGING, PROD, REJECTED, EXPIRED, etc. If omitted, all lifecycle states for the app are returned.

### Request Example

```
curl -X GET \
  "https://www.essesseff.com/api/v1/accounts/my-team/organizations/my-apps-org/apps/my-app/retention-policies?state=PROD" \
  -H "X-API-Key: ess_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

### Response Example

```json
{
  "success": true,
  "data": [
    {
      "app_name": "my-app",
      "state": "PROD",
      "retention_days": 30,
      "scope": "app",
      "created_at": "2025-01-01T00:00:00Z",
      "updated_at": "2025-01-01T00:00:00Z"
    },
    {
      "app_name": "my-app",
      "state": "BUILD",
      "retention_days": 3,
      "scope": "account",
      "created_at": "2025-01-01T00:00:00Z",
      "updated_at": "2025-01-01T00:00:00Z"
    }
  ]
}
```

---

## PATCH /accounts/{account_slug}/organizations/{organization_login}/apps/{app_name}/retention-policies

Update a retention policy

```
PATCH /api/v1/accounts/{account_slug}/organizations/{organization_login}/apps/{app_name}/retention-policies?state={state}
```

### Description

Creates or updates a lifecycle-state retention policy for a specific app. Allows modifying retention_days for a single lifecycle state (e.g. PROD, QA, BUILD, etc.). Retention policies updated via this endpoint are app-specific and override any account-wide defaults for the same state.

### Path Parameters

#### account_slug (required)

The team account slug (name) associated with the API key

#### organization_login (required)

GitHub organization login where the app exists

#### app_name (required)

Name of the essesseff app

### Query Parameters

#### state (required)

Lifecycle state to update (e.g. BUILD, DEV, RC, QA, STABLE, STAGING, PROD, REJECTED, EXPIRED).

### Request Body

#### retention_days (required)

Number of days to retain images in this lifecycle state (non-negative integer)

### Request Example

```
curl -X PATCH \
  "https://www.essesseff.com/api/v1/accounts/my-team/organizations/my-apps-org/apps/my-app/retention-policies?state=PROD" \
  -H "X-API-Key: ess_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" \
  -H "Content-Type: application/json" \
  -d '{
    "retention_days": 60
  }'
```

### Response Example

```json
{
  "success": true,
  "data": {
    "app_name": "my-app",
    "state": "PROD",
    "retention_days": 60,
    "updated_at": "2025-01-02T00:00:00Z"
  }
}
```
