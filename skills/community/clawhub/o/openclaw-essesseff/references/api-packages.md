# Packages API

Source: https://www.essesseff.com/docs/api/packages/delete-packages

---

## GET /accounts/{account_slug}/organizations/{organization_login}/apps/{app_name}/packages/delete-packages

Retrieve GitHub API payloads for deleting expired package versions

```
GET /api/v1/accounts/{account_slug}/organizations/{organization_login}/apps/{app_name}/packages/delete-packages
```

### Description

Returns GitHub API payloads for deleting package versions that correspond to expired essesseff images. The function validates that all uniquely tagged images associated with a particular GitHub package version are expired before returning the package version for deletion.

**Important:** This endpoint only returns deletion payloads. You must execute the deletion using a GitHub Personal Access Token (PAT) with appropriate permissions, as GitHub Apps cannot reliably delete package versions via the API.

### Path Parameters

#### account_slug (required)

The team account slug (name) associated with the API key

#### organization_login (required)

GitHub organization login (e.g., "my-apps-org")

#### app_name (required)

essesseff app name. The repository name is automatically derived from the app's source repository.

### Query Parameters

#### assume_deleted (required)

Boolean (true/false). If true, marks all returned package version IDs as assume_to_be_deleted in the database, preventing duplicate payloads on subsequent requests. If false, does not mark them.

#### limit (optional)

Maximum number of results to return (default: 100)

#### offset (optional)

Number of results to skip for pagination (default: 0)

### Request Example

```
curl -X GET \
  "https://www.essesseff.com/api/v1/accounts/my-team/organizations/my-apps-org/apps/my-app/packages/delete-packages?assume_deleted=true" \
  -H "X-API-Key: ess_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

### Response Example

```json
{
  "success": true,
  "data": [
    {
      "package_version_id": 12345678,
      "organization_login": "my-apps-org",
      "repository_name": "my-app",
      "package_name": "my-app",
      "github_api_endpoint": "DELETE /repos/{owner}/{repo}/packages/{package_type}/{package_name}/versions/{package_version_id}",
      "github_api_params": {
        "owner": "my-apps-org",
        "repo": "my-app",
        "package_type": "container",
        "package_name": "my-app",
        "package_version_id": 12345678
      },
      "github_api_url": "https://api.github.com/repos/my-apps-org/my-app/packages/container/my-app/versions/12345678",
      "metadata": {
        "expired_tags": [
          {
            "image_tag": "v1.0.0",
            "expired_at": "2025-01-01T00:00:00Z"
          },
          {
            "image_tag": "v1.0.1",
            "expired_at": "2025-01-02T00:00:00Z"
          }
        ],
        "all_tags_expired": true
      }
    }
  ],
  "pagination": {
    "total": 1,
    "limit": 100,
    "offset": 0,
    "has_more": false
  }
}
```

### Best Practices

#### When to use assume_deleted=true

Use `assume_deleted=true` when you are confident that you will execute the deletion using the returned payloads. This prevents the same package versions from being returned on subsequent requests.

#### When to use assume_deleted=false

Use `assume_deleted=false` when you want to preview what would be deleted without committing to the deletion. The same package versions will be returned on subsequent requests until you use `assume_deleted=true`.

#### Executing Deletions

To delete a package version, make a DELETE request to the `github_api_url` using a GitHub Personal Access Token (PAT) with the `delete:packages` permission:

```
curl -X DELETE \
  "https://api.github.com/repos/my-apps-org/my-app/packages/container/my-app/versions/12345678" \
  -H "Authorization: token YOUR_GITHUB_PAT"
```
