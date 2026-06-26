# Organizations API

Source: https://www.essesseff.com/docs/api/organizations

List and retrieve GitHub organizations for team accounts.

---

## GET /accounts/{account_slug}/organizations

List GitHub organizations for a team account

```
GET /api/v1/accounts/{account_slug}/organizations
```

### Description

Lists GitHub organizations associated with a team account. Returns organization details including GitHub organization IDs, creation timestamps, and app counts.

### Path Parameters

#### account_slug (required)

The team account slug (name) associated with the API key. The API key must belong to this account.

### Query Parameters

#### limit (optional)

Maximum number of results to return (default: 50, max: 1000)

#### offset (optional)

Number of results to skip for pagination (default: 0)

### Request Example

```
curl -X GET \
  "https://www.essesseff.com/api/v1/accounts/my-team/organizations" \
  -H "X-API-Key: ess_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

### Response Example

```json
{
  "success": true,
  "data": [
    {
      "organization_login": "my-apps-org",
      "github_organization_id": 12345678,
      "created_at": "2025-01-01T00:00:00Z",
      "app_count": 5
    }
  ],
  "pagination": {
    "total": 2,
    "limit": 50,
    "offset": 0,
    "has_more": false
  }
}
```

---

## GET /accounts/{account_slug}/organizations/{organization_login}

Retrieve detailed information about a GitHub organization

```
GET /api/v1/accounts/{account_slug}/organizations/{organization_login}
```

### Description

Retrieves detailed information about a specific GitHub organization. Returns organization details including GitHub organization ID, creation timestamp, app count, and a list of apps with names and creation timestamps.

### Path Parameters

#### account_slug (required)

The team account slug (name) associated with the API key. The API key must belong to this account.

#### organization_login (required)

GitHub organization login (e.g., "my-apps-org"; matched case-insensitively)

### Request Example

```
curl -X GET \
  "https://www.essesseff.com/api/v1/accounts/my-team/organizations/my-apps-org" \
  -H "X-API-Key: ess_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

### Response Example

```json
{
  "success": true,
  "data": {
    "organization_login": "my-apps-org",
    "github_organization_id": 12345678,
    "created_at": "2025-01-01T00:00:00Z",
    "app_count": 5,
    "apps": [
      {
        "app_name": "my-app",
        "created_at": "2025-01-01T00:00:00Z"
      }
    ]
  }
}
```
