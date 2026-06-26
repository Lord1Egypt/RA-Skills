# essesseff Public API — Overview

Source: https://www.essesseff.com/docs/api

## Overview

The essesseff Public API provides programmatic access to essesseff platform features. All API requests require authentication via API keys and are subject to rate limiting.

## Base URL

```
https://www.essesseff.com/api/v1
```

Use the `www` host to avoid 307 redirects.

## Authentication

All API requests must include an API key in the `X-API-Key` header:

```
X-API-Key: ess_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

API keys can be generated and managed in your team account settings (`/home/[account]/settings`). API keys are only issuable to account owners and DevOps Engineers.

## API Structure

The essesseff API uses a hierarchical path structure to express context explicitly:

- **Global resources**: `/api/v1/global/...` (system-level resources, not account-specific)
- **Account-specific resources**: `/api/v1/accounts/{account_slug}/...` (requires account_slug in path)

For account-specific endpoints, the API key **must** belong to the account_slug specified in the path. If the API key does not match the account_slug, a `403 Forbidden` error is returned.

## Rate Limiting

API requests are rate-limited to 3 requests per 10 seconds.

Rate limit information is included in response headers:

```
X-RateLimit-Limit: 3
X-RateLimit-Remaining: 2
X-RateLimit-Reset: 1234567890
```

## Error Handling

Errors are returned in JSON format with appropriate HTTP status codes:

```json
{
  "error": "Error message describing what went wrong",
  "message": "Additional details about the error"
}
```

Common error codes:

- `400 Bad Request` - Invalid request parameters
- `401 Unauthorized` - Invalid or missing API key
- `403 Forbidden` - API key does not belong to the specified account_slug
- `404 Not Found` - Resource not found
- `429 Too Many Requests` - Rate limit exceeded
- `500 Internal Server Error` - Server error

## API Endpoints

Available essesseff public API endpoints organized by context hierarchy.

### Global Resources

System-level resources available to all authenticated users (no account_slug required).

#### GET /global/templates

List available global essesseff app templates. Supports optional filtering by programming language.

#### GET /global/templates/{template_name}

Get complete details for a specific global template (all fields needed for app creation).

### Account-Specific Resources

All account-specific endpoints require `account_slug` in the path. The API key must belong to the specified account_slug.

#### Templates

##### GET /accounts/{account_slug}/templates

List team-account-specific templates for the specified account.

##### GET /accounts/{account_slug}/templates/{template_name}

Get complete details for a team-account-specific template.

#### Organizations

##### GET /accounts/{account_slug}/organizations

List GitHub organizations associated with a team account.

##### GET /accounts/{account_slug}/organizations/{organization_login}

Retrieve detailed information about a specific GitHub organization with app list.

#### Apps

##### POST /accounts/{account_slug}/organizations/{organization_login}/apps

Create a new essesseff app. Requires `app_name` as a query parameter.

##### GET /accounts/{account_slug}/organizations/{organization_login}/apps

List essesseff apps for an organization. Supports optional filtering by app_name.

##### GET /accounts/{account_slug}/organizations/{organization_login}/apps/{app_name}

Get app details including all repository IDs and URLs.

##### PATCH /accounts/{account_slug}/organizations/{organization_login}/apps/{app_name}

Update an existing essesseff app (description, repository_visibility).

#### App Resources

##### GET .../apps/{app_name}/deployments

List deployments for a specific essesseff app. Supports filtering by environment and status.

##### GET .../apps/{app_name}/images

List container images for a specific essesseff app. Supports filtering by repository, tag, and status.

##### GET .../apps/{app_name}/images/{image_tag}

Get detailed information about a specific container image by tag.

##### GET .../apps/.../images/{image_tag}/lifecycle

Get image lifecycle state (optional history).

##### POST .../apps/.../images/{image_tag}/lifecycle

Update image lifecycle state; can trigger environment deployment.

##### GET .../apps/.../environments/{env}

Get current deployment for an environment (DEV, QA, STAGING, PROD). Response includes argocd_application_url when set.

##### POST .../environments/{env}/set-argocd-application-url

Set or clear Argo CD application URL for an environment (body: url or null). Returns 204.

##### POST .../environments/DEV/declare-rc

Set current DEV image lifecycle to RC (no body).

##### POST .../environments/QA/accept-rc

Accept RC and deploy to QA (body: image_tag).

##### POST .../environments/QA/reject-rc

Reject RC (body: image_tag).

##### POST .../environments/QA/declare-stable

Set current QA image to STABLE (no body).

##### POST .../environments/QA/declare-rejected

Set current QA image to REJECTED (no body).

##### POST .../environments/STAGING/deploy-stable

Deploy STABLE image to STAGING (body: image_tag).

##### POST .../environments/PROD/deploy-stable

Deploy STABLE image to PROD (body: image_tag, optional deployment_note; no OTP).

##### GET .../apps/{app_name}/retention-policies

List retention policies for a specific essesseff app.

##### PATCH .../apps/{app_name}/retention-policies

Update an existing retention policy for a specific app and lifecycle state.

##### GET .../apps/{app_name}/notifications-secret

Retrieve the notifications-secret.yaml file content for Argo CD setup. Returns YAML content.

#### Other Endpoints

##### GET .../apps/{app_name}/packages/delete-packages

Retrieve GitHub API payloads for deleting package versions that correspond to expired essesseff images.

## Getting Started

1. Generate an API key in your team account settings (`/home/[account]/settings`)
2. Include the API key in the `X-API-Key` header of all requests
3. Review the individual endpoint documentation for request/response formats
4. Implement proper error handling and rate limit management in your client code
