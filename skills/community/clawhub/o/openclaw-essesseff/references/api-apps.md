# Apps API

Source: https://www.essesseff.com/docs/api/apps

Manage essesseff apps, deployments, images, and retention policies.

---

## GET /accounts/{account_slug}/organizations/{organization_login}/apps

List essesseff apps

```
GET /api/v1/accounts/{account_slug}/organizations/{organization_login}/apps
```

### Path Parameters

#### account_slug (required)

The team account slug (name) associated with the API key. The API key must belong to this account.

#### organization_login (required)

GitHub organization login to list apps for (matched case-insensitively)

### Description

Lists essesseff apps for a team account. Supports filtering by organization and app name. Returns app details including repository URLs, template information, and creation timestamps.

### Query Parameters

#### app_name (optional)

Filter by app name (exact match). For single app operations, use the full path endpoint instead.

#### limit (optional)

Maximum number of results to return (default: 50)

#### offset (optional)

Number of results to skip for pagination (default: 0)

### Request Example

```
curl -X GET \
  "https://www.essesseff.com/api/v1/accounts/my-team/organizations/my-apps-org/apps" \
  -H "X-API-Key: ess_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

With optional app_name filter:

```
curl -X GET \
  "https://www.essesseff.com/api/v1/accounts/my-team/organizations/my-apps-org/apps?app_name=my-app" \
  -H "X-API-Key: ess_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

### Response Example

```json
{
  "success": true,
  "data": [
    {
      "app_name": "my-app",
      "organization_login": "my-apps-org",
      "description": "My essesseff app",
      "programming_language": "go",
      "repository_visibility": "private",
      "template": {
        "name": "essesseff-hello-world-go-template",
        "language": "go",
        "is_global_template": true
      },
      "created_at": "2025-01-01T00:00:00Z",
      "repository_urls": {
        "source_repo": "https://github.com/my-apps-org/my-app",
        "config_dev_repo": "https://github.com/my-apps-org/my-app-config-dev",
        "config_qa_repo": "https://github.com/my-apps-org/my-app-config-qa",
        "config_staging_repo": "https://github.com/my-apps-org/my-app-config-staging",
        "config_prod_repo": "https://github.com/my-apps-org/my-app-config-prod",
        "argocd_dev_repo": "https://github.com/my-apps-org/my-app-argocd-dev",
        "argocd_qa_repo": "https://github.com/my-apps-org/my-app-argocd-qa",
        "argocd_staging_repo": "https://github.com/my-apps-org/my-app-argocd-staging",
        "argocd_prod_repo": "https://github.com/my-apps-org/my-app-argocd-prod"
      }
    }
  ],
  "pagination": {
    "total": 1,
    "limit": 50,
    "offset": 0,
    "has_more": false
  }
}
```

---

## POST /accounts/{account_slug}/organizations/{organization_login}/apps

Create a new essesseff app

```
POST /api/v1/accounts/{account_slug}/organizations/{organization_login}/apps?app_name={app_name}
```

### Path Parameters

#### account_slug (required)

The team account slug (name) associated with the API key. The API key must belong to this account.

#### organization_login (required)

GitHub organization login where the app will be created (e.g., "my-apps-org")

### Query Parameters

#### app_name (required)

Name of the essesseff app to create (must be URL-compliant: lowercase letters, numbers, and hyphens only)

### Description

Creates a new essesseff app with the specified configuration. The app creation process includes creating 9 GitHub repositories (1 source + 4 config + 4 Argo CD), setting up webhooks, assigning teams, and configuring retention policies.

### Request Body

Note: `account_slug`, `organization_login`, and `app_name` are now provided in the path and query parameters, not in the request body.

#### template (required)

Template configuration object:

- `template_org_login` - Template organization login (e.g., "essesseff-hello-world-go-template")
- `source_template_repo` - Source template repository name (e.g., "hello-world")
- `is_global_template` - Boolean indicating if this is a global template
- `replacement_string` - String to replace in templates (always "hello-world" for global templates)

#### description (optional)

Description of the app

#### programming_language (optional)

Programming language (e.g., "go", "java", "node", "python")

#### repository_visibility (optional)

Repository visibility: "private" or "public" (default: "private")

#### k8s_namespace (optional)

Kubernetes namespace used to replace "{{K8S_NAMESPACE}}" in templates. If omitted, the target GitHub organization (`organization_login`) is used as the namespace. When provided (or when using the org as fallback), the value must be a valid Kubernetes namespace: at most 63 characters, lowercase letters, numbers, and hyphens only, and must start and end with a letter or number. Invalid values return 400 with a descriptive error.

### Request Examples

Below are examples for each available global template:

#### Java Spring Boot Template

```
curl -X POST \
  "https://www.essesseff.com/api/v1/accounts/my-team/organizations/my-apps-org/apps?app_name=my-java-app" \
  -H "X-API-Key: ess_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "My Java Spring Boot application",
    "programming_language": "java",
    "template": {
      "template_org_login": "essesseff-helloworld-springboot-templat",
      "source_template_repo": "helloworld",
      "is_global_template": true,
      "replacement_string": "helloworld"
    },
    "repository_visibility": "private"
  }'
```

#### Go Template

```
curl -X POST \
  "https://www.essesseff.com/api/v1/accounts/my-team/organizations/my-apps-org/apps?app_name=my-go-app" \
  -H "X-API-Key: ess_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "My Go application",
    "programming_language": "go",
    "template": {
      "template_org_login": "essesseff-hello-world-go-template",
      "source_template_repo": "hello-world",
      "is_global_template": true,
      "replacement_string": "hello-world"
    },
    "repository_visibility": "private"
  }'
```

#### Node.js Template

```
curl -X POST \
  "https://www.essesseff.com/api/v1/accounts/my-team/organizations/my-apps-org/apps?app_name=my-nodejs-app" \
  -H "X-API-Key: ess_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "My Node.js application",
    "programming_language": "node",
    "template": {
      "template_org_login": "essesseff-hello-world-nodejs-template",
      "source_template_repo": "hello-world",
      "is_global_template": true,
      "replacement_string": "hello-world"
    },
    "repository_visibility": "private"
  }'
```

#### Python Flask Template

```
curl -X POST \
  "https://www.essesseff.com/api/v1/accounts/my-team/organizations/my-apps-org/apps?app_name=my-python-app" \
  -H "X-API-Key: ess_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "My Python Flask application",
    "programming_language": "python",
    "template": {
      "template_org_login": "essesseff-hello-world-flask-template",
      "source_template_repo": "hello-world",
      "is_global_template": true,
      "replacement_string": "hello-world"
    },
    "repository_visibility": "private"
  }'
```

### Response Example

```json
{
  "success": true,
  "data": {
    "account_slug": "my-team",
    "app_name": "my-app",
    "organization_login": "my-apps-org",
    "description": "My essesseff app",
    "programming_language": "go",
    "resultant_repos": {
      "source_repo": "my-app",
      "config_dev_repo": "my-app-config-dev",
      "config_qa_repo": "my-app-config-qa",
      "config_staging_repo": "my-app-config-staging",
      "config_prod_repo": "my-app-config-prod",
      "argocd_dev_repo": "my-app-argocd-dev",
      "argocd_qa_repo": "my-app-argocd-qa",
      "argocd_staging_repo": "my-app-argocd-staging",
      "argocd_prod_repo": "my-app-argocd-prod",
      "template_org_login": "essesseff-hello-world-go-template",
      "is_global_template": true,
      "replacement_string": "hello-world"
    },
    "repository_visibility": "private"
  }
}
```

### Template Notes

For global templates, the `replacement_string` is always `"hello-world"` (or `"helloworld"` for Java Spring Boot template). The system will automatically replace `"hello-world"` and/or `"helloworld"` with the specified `app_name` when cloning repository content from the templates.

---

## GET /accounts/{account_slug}/organizations/{organization_login}/apps/{app_name}

Get app details

```
GET /api/v1/accounts/{account_slug}/organizations/{organization_login}/apps/{app_name}
```

### Description

Gets app details including all repository IDs and URLs. Returns 404 if app doesn't exist.

### Path Parameters

#### account_slug (required)

The team account slug (name) associated with the API key

#### organization_login (required)

GitHub organization login where the app exists

#### app_name (required)

Name of the essesseff app

### Request Example

```
curl -X GET \
  "https://www.essesseff.com/api/v1/accounts/my-team/organizations/my-apps-org/apps/my-app" \
  -H "X-API-Key: ess_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

### Response Example

```json
{
  "success": true,
  "data": {
    "app_name": "my-app",
    "organization_login": "my-apps-org",
    "description": "My essesseff app",
    "programming_language": "go",
    "repository_visibility": "private",
    "template": {
      "name": "essesseff-hello-world-go-template",
      "language": "go",
      "is_global_template": true
    },
    "created_at": "2025-01-01T00:00:00Z",
    "updated_at": "2025-01-01T00:00:00Z",
    "repository_urls": {
      "source_repo": "https://github.com/my-apps-org/my-app",
      "config_dev_repo": "https://github.com/my-apps-org/my-app-config-dev",
      "config_qa_repo": "https://github.com/my-apps-org/my-app-config-qa",
      "config_staging_repo": "https://github.com/my-apps-org/my-app-config-staging",
      "config_prod_repo": "https://github.com/my-apps-org/my-app-config-prod",
      "argocd_dev_repo": "https://github.com/my-apps-org/my-app-argocd-dev",
      "argocd_qa_repo": "https://github.com/my-apps-org/my-app-argocd-qa",
      "argocd_staging_repo": "https://github.com/my-apps-org/my-app-argocd-staging",
      "argocd_prod_repo": "https://github.com/my-apps-org/my-app-argocd-prod"
    },
    "repository_ids": {
      "source_repo": 12345678,
      "config_dev_repo": 12345679,
      "config_qa_repo": 12345680,
      "config_staging_repo": 12345681,
      "config_prod_repo": 12345682,
      "argocd_dev_repo": 12345683,
      "argocd_qa_repo": 12345684,
      "argocd_staging_repo": 12345685,
      "argocd_prod_repo": 12345686
    }
  }
}
```

---

## PATCH /accounts/{account_slug}/organizations/{organization_login}/apps/{app_name}

Update an existing essesseff app

```
PATCH /api/v1/accounts/{account_slug}/organizations/{organization_login}/apps/{app_name}
```

### Description

Updates an existing essesseff app. Currently supports updating description and repository visibility (private/public). When repository visibility is updated, all repositories associated with the app are updated in both the database and GitHub.

### Path Parameters

#### account_slug (required)

The team account slug (name) associated with the API key

#### organization_login (required)

GitHub organization login where the app exists

#### app_name (required)

Name of the essesseff app to update

### Request Body

#### description (optional)

Updated app description

#### repository_visibility (optional)

Repository visibility: "private" or "public"

At least one of description or repository_visibility must be provided.

### Request Example

```
curl -X PATCH \
  "https://www.essesseff.com/api/v1/accounts/my-team/organizations/my-apps-org/apps/my-app" \
  -H "X-API-Key: ess_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Updated description",
    "repository_visibility": "public"
  }'
```

### Response Example

```json
{
  "success": true,
  "data": {
    "app_name": "my-app",
    "description": "Updated description",
    "repository_visibility": "public",
    "updated_at": "2025-01-02T00:00:00Z"
  }
}
```

---

## GET /accounts/{account_slug}/organizations/{organization_login}/apps/{app_name}/deployments

List deployments for an app

```
GET /api/v1/accounts/{account_slug}/organizations/{organization_login}/apps/{app_name}/deployments
```

### Description

Lists deployments for a specific essesseff app. Supports filtering by environment (dev, qa, staging, prod) and status (pending, in_progress, succeeded, failed). Returns deployment details including image tags, GitHub commit information, and deployment timestamps.

### Path Parameters

#### app_name (required)

Name of the essesseff app

### Query Parameters

#### account_slug (required)

The team account slug (name) associated with the API key

#### organization_login (required)

GitHub organization login where the app exists

#### environment (optional)

Filter by environment: dev, qa, staging, prod

#### status (optional)

Filter by status: pending, in_progress, succeeded, failed

#### limit (optional)

Maximum number of results (default: 50, max: 1000)

#### offset (optional)

Number of results to skip for pagination (default: 0)

### Request Example

```
curl -X GET \
  "https://www.essesseff.com/api/v1/accounts/my-team/organizations/my-apps-org/apps/my-app/deployments?environment=prod&status=succeeded" \
  -H "X-API-Key: ess_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

### Response Example

```json
{
  "success": true,
  "data": [
    {
      "app_name": "my-app",
      "environment": "prod",
      "status": "succeeded",
      "image_tag": "v1.2.3",
      "github_sha": "abc123def456",
      "github_ref": "refs/heads/main",
      "deployed_at": "2025-01-01T12:00:00Z",
      "completed_at": "2025-01-01T12:05:00Z",
      "metadata": {
        "github_repository": "my-apps-org/my-app",
        "github_workflow_run_id": 12345678,
        "deployment_method": "manual_promote",
        "deployment_conclusion": "success",
        "health_status": "Healthy"
      }
    }
  ],
  "pagination": {
    "total": 10,
    "limit": 50,
    "offset": 0,
    "has_more": false
  }
}
```

---

## GET /accounts/{account_slug}/organizations/{organization_login}/apps/{app_name}/notifications-secret

Get notifications-secret.yaml for Argo CD setup

```
GET /api/v1/accounts/{account_slug}/organizations/{organization_login}/apps/{app_name}/notifications-secret
```

### Description

Retrieves the notifications-secret.yaml file content for Argo CD setup. Returns YAML content with `Content-Type: application/x-yaml`. This file contains Argo CD Notifications Event Processor API keys and environment-specific app secrets.

**Note:** Secrets are automatically issued from the database when this file is generated if they don't already exist.

### Path Parameters

#### account_slug (required)

The team account slug (name) associated with the API key

#### organization_login (required)

GitHub organization login where the app exists

#### app_name (required)

Name of the essesseff app

### Request Example

```
curl -X GET \
  "https://www.essesseff.com/api/v1/accounts/my-team/organizations/my-apps-org/apps/my-app/notifications-secret" \
  -H "X-API-Key: ess_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" \
  -o notifications-secret.yaml
```

### Response

Returns YAML content with `Content-Type: application/x-yaml`:

```yaml
# notifications-secret.yaml

# Store Argo CD Notifications Event Processor API key and environment-specific app secrets
# ***DELETE THIS FILE AFTER APPLYING - DO NOT COMMIT SECRETS TO GITHUB***

apiVersion: v1
kind: Secret
metadata:
  name: argocd-notifications-secret
  namespace: argocd
type: Opaque
stringData:
  argocd-webhook-url: "https://api.essesseff.com/api/v1/argocd/webhook"
  aws-api-gateway-key-my-apps-org: "ess_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
  app-secret-12345678: "abc123def456..."
  app-secret-12345679: "xyz789uvw012..."
  app-secret-12345680: "mno345pqr678..."
  app-secret-12345681: "ghi901jkl234..."
```

The response includes secrets for all environments (dev, qa, staging, prod) that have config repositories. Secret keys are environment-specific: `app-secret-{config-env-repository-id}`
