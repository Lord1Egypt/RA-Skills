# Images API

Source: https://www.essesseff.com/docs/api/apps

List container images and manage image lifecycle state.

All paths begin with: `/api/v1/accounts/{account_slug}/organizations/{organization_login}/apps/{app_name}`

---

## GET .../images

List container images for an app

```
GET /api/v1/accounts/{account_slug}/organizations/{organization_login}/apps/{app_name}/images
```

### Description

Lists container images for a specific essesseff app. Supports filtering by repository name, image tag, and status (active, expired, all). Returns image metadata including GitHub package version IDs.

### Path Parameters

#### app_name (required)

Name of the essesseff app

### Query Parameters

#### account_slug (required)

The team account slug (name) associated with the API key

#### organization_login (required)

GitHub organization login where the app exists

#### repository_name (optional)

Filter by GitHub repository name

#### image_tag (optional)

Filter by image tag

#### status (optional)

Filter by status: active, expired, all (default: all)

#### limit (optional)

Maximum number of results (default: 100, max: 1000)

#### offset (optional)

Number of results to skip for pagination (default: 0)

### Request Example

```
curl -X GET \
  "https://www.essesseff.com/api/v1/accounts/my-team/organizations/my-apps-org/apps/my-app/images?status=active" \
  -H "X-API-Key: ess_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

### Response Example

```json
{
  "success": true,
  "data": [
    {
      "app_name": "my-app",
      "repository_name": "my-app",
      "image_name": "my-app",
      "image_tag": "v1.2.3",
      "status": "active",
      "github_package_version_id": 12345678,
      "created_at": "2025-01-01T00:00:00Z",
      "expired_at": null,
      "metadata": {
        "github_organization": "my-apps-org",
        "package_type": "container"
      }
    }
  ],
  "pagination": {
    "total": 50,
    "limit": 100,
    "offset": 0,
    "has_more": false
  }
}
```

---

## GET .../images/{image_tag}

Get image details by tag

```
GET /api/v1/accounts/{account_slug}/organizations/{organization_login}/apps/{app_name}/images/{image_tag}
```

### Description

Retrieves detailed information about a specific container image by tag. If multiple repositories have the same image tag, use the repository_name query parameter to disambiguate.

### Path Parameters

#### account_slug (required)

The team account slug (name) associated with the API key

#### organization_login (required)

GitHub organization login where the app exists

#### app_name (required)

Name of the essesseff app

#### image_tag (required)

Image tag (e.g., "v1.2.3")

### Query Parameters

#### repository_name (optional)

GitHub repository name (required if multiple repos have same tag)

### Request Example

```
curl -X GET \
  "https://www.essesseff.com/api/v1/accounts/my-team/organizations/my-apps-org/apps/my-app/images/v1.2.3" \
  -H "X-API-Key: ess_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

### Response Example

```json
{
  "success": true,
  "data": {
    "app_name": "my-app",
    "repository_name": "my-app",
    "image_name": "my-app",
    "image_tag": "v1.2.3",
    "status": "active",
    "github_package_version_id": 12345678,
    "created_at": "2025-01-01T00:00:00Z",
    "expired_at": null,
    "metadata": {
      "github_organization": "my-apps-org",
      "package_type": "container",
      "github_package_url": "https://github.com/my-apps-org/my-app/pkgs/container/my-app"
    }
  }
}
```

---

## GET .../images/{image_tag}/lifecycle

Get image lifecycle state; optional history

```
GET /api/v1/accounts/{account_slug}/organizations/{organization_login}/apps/{app_name}/images/{image_tag}/lifecycle
```

### Description

Returns current lifecycle state and timestamp for the image. Query `history=true` to include state history (no UUIDs). Response includes account_slug, organization, app, image_name, image_tag, current_state, state_timestamp.

### Query Parameters

#### history (optional)

Set to `true` or `1` to include state history in the response.

### Request Example

```
curl -X GET \
  "https://www.essesseff.com/api/v1/accounts/my-team/organizations/my-apps-org/apps/my-app/images/v1.2.3/lifecycle?history=true" \
  -H "X-API-Key: ess_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

### Response Example (200, no history)

```json
{
  "account_slug": "my-team",
  "organization": "my-apps-org",
  "app": "my-app",
  "image_name": "my-app",
  "image_tag": "v1.2.3",
  "current_state": "RC",
  "state_timestamp": "2025-09-30T12:00:00Z"
}
```

### Response Example (200, with history=true)

```json
{
  "account_slug": "my-team",
  "organization": "my-apps-org",
  "app": "my-app",
  "image_name": "my-app",
  "image_tag": "v1.2.3",
  "current_state": "RC",
  "state_timestamp": "2025-09-30T12:00:00Z",
  "history": [
    { "state": "BUILD", "state_timestamp": "2025-09-30T10:00:00Z", "is_active": false },
    { "state": "DEV",   "state_timestamp": "2025-09-30T11:00:00Z", "is_active": false },
    { "state": "RC",    "state_timestamp": "2025-09-30T12:00:00Z", "is_active": true }
  ]
}
```

---

## POST .../images/{image_tag}/lifecycle

Update image lifecycle state; can trigger environment deployment

```
POST /api/v1/accounts/{account_slug}/organizations/{organization_login}/apps/{app_name}/images/{image_tag}/lifecycle
```

### Description

Transition the image to a new lifecycle state. Body: `state` (required); optional `deployment_note` when state is PROD. Only allowed transitions (per lifecycle table) are accepted; same-state or backwards transitions return 400. When state is DEV, QA, STAGING, or PROD, the API also performs the corresponding environment deployment (config repo promotion and deployment record). PROD via API does not require OTP.

### Request Example

```
curl -X POST \
  "https://www.essesseff.com/api/v1/accounts/my-team/organizations/my-apps-org/apps/my-app/images/v1.2.3/lifecycle" \
  -H "X-API-Key: ess_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" \
  -H "Content-Type: application/json" \
  -d '{"state": "QA"}'
```

### Response Example (200)

```json
{
  "account_slug": "my-team",
  "organization": "my-apps-org",
  "app": "my-app",
  "image_name": "my-app",
  "image_tag": "v1.2.3",
  "state": "QA",
  "state_timestamp": "2025-09-30T12:00:00Z"
}
```
