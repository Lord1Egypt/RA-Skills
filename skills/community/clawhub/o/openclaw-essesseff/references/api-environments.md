# Environments API

Source: https://www.essesseff.com/docs/api/apps

Get environment status and drive the image promotion pipeline through DEV → QA → STAGING → PROD.

All paths begin with: `/api/v1/accounts/{account_slug}/organizations/{organization_login}/apps/{app_name}/environments`

Valid `{env}` values (case-sensitive in path): `DEV`, `QA`, `STAGING`, `PROD`

---

## GET .../environments/{env}

Get current deployment for an environment

```
GET /api/v1/accounts/{account_slug}/organizations/{organization_login}/apps/{app_name}/environments/{env}
```

### Path Parameters

`env` must be one of: DEV, QA, STAGING, PROD.

### Description

Returns the image currently deployed to the given environment. Response includes account_slug, organization, app, environment, image_name, image_tag, state_timestamp, and argocd_application_url (optional URL to the Argo CD application for this environment, if set in app settings). If no deployment exists, image_name, image_tag, and state_timestamp are null.

### Request Example

```
curl -X GET \
  "https://www.essesseff.com/api/v1/accounts/my-team/organizations/my-apps-org/apps/my-app/environments/QA" \
  -H "X-API-Key: ess_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

### Response Example (200, with deployment)

```json
{
  "account_slug": "my-team",
  "organization": "my-apps-org",
  "app": "my-app",
  "environment": "QA",
  "image_name": "my-app",
  "image_tag": "v1.2.3",
  "state_timestamp": "2025-09-30T11:00:00Z",
  "argocd_application_url": "https://argocd.example.com/applications/argocd/my-app-qa"
}
```

### Response Example (200, no deployment)

When no image is deployed to the environment:

```json
{
  "account_slug": "my-team",
  "organization": "my-apps-org",
  "app": "my-app",
  "environment": "QA",
  "image_name": null,
  "image_tag": null,
  "state_timestamp": null,
  "argocd_application_url": null
}
```

---

## POST .../environments/{env}/set-argocd-application-url

Set Argo CD application URL for an environment

```
POST /api/v1/accounts/{account_slug}/organizations/{organization_login}/apps/{app_name}/environments/{env}/set-argocd-application-url
```

### Path Parameters

`env` must be one of: DEV, QA, STAGING, PROD.

### Description

Sets the optional Argo CD application URL for the given environment. The URL is stored in app settings and shown in the essesseff UI (deployment cards, app settings). The URL is validated and normalized (trailing slash removed). Send `null` or empty to clear. Returns 204 on success.

### Request Body

`url` (optional): string or null. Full URL to the Argo CD application for this environment (e.g. `https://argocd.example.com/applications/argocd/my-app-qa`). Max 1000 characters. Omit or set to null to clear.

### Request Example

```
curl -X POST \
  "https://www.essesseff.com/api/v1/accounts/my-team/organizations/my-apps-org/apps/my-app/environments/QA/set-argocd-application-url" \
  -H "X-API-Key: ess_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://argocd.example.com/applications/argocd/my-app-qa"}'
```

### Response

Returns 204 No Content on success. Returns 400 for invalid env or invalid URL format.

---

## POST .../environments/DEV/declare-rc

Set current DEV deployment image lifecycle to RC

```
POST /api/v1/accounts/{account_slug}/organizations/{organization_login}/apps/{app_name}/environments/DEV/declare-rc
```

No body. Sets the current DEV deployment image's lifecycle state to RC.

### Request Example

```
curl -X POST \
  "https://www.essesseff.com/api/v1/accounts/my-team/organizations/my-apps-org/apps/my-app/environments/DEV/declare-rc" \
  -H "X-API-Key: ess_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" \
  -H "Content-Type: application/json" \
  -d '{}'
```

### Response Example (200)

```json
{
  "account_slug": "my-team",
  "organization": "my-apps-org",
  "app": "my-app",
  "environment": "DEV",
  "image_name": "my-app",
  "image_tag": "v1.2.3",
  "state": "RC",
  "state_timestamp": "2025-09-30T12:00:00Z"
}
```

---

## POST .../environments/QA/accept-rc

Accept release candidate and deploy to QA

```
POST /api/v1/accounts/{account_slug}/organizations/{organization_login}/apps/{app_name}/environments/QA/accept-rc
```

Body: `{"image_tag": "v1.2.3"}`. Sets image lifecycle to QA, promotes config_qa, and creates a deployment record.

### Request Example

```
curl -X POST \
  "https://www.essesseff.com/api/v1/accounts/my-team/organizations/my-apps-org/apps/my-app/environments/QA/accept-rc" \
  -H "X-API-Key: ess_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" \
  -H "Content-Type: application/json" \
  -d '{"image_tag": "v1.2.3"}'
```

### Response Example (200)

```json
{
  "account_slug": "my-team",
  "organization": "my-apps-org",
  "app": "my-app",
  "environment": "QA",
  "image_name": "my-app",
  "image_tag": "v1.2.3",
  "state": "QA",
  "state_timestamp": "2025-09-30T12:00:00Z"
}
```

---

## POST .../environments/QA/reject-rc

Reject a release candidate

```
POST /api/v1/accounts/{account_slug}/organizations/{organization_login}/apps/{app_name}/environments/QA/reject-rc
```

Body: `image_tag`. Sets image lifecycle to REJECTED.

### Request Example

```
curl -X POST \
  "https://www.essesseff.com/api/v1/accounts/my-team/organizations/my-apps-org/apps/my-app/environments/QA/reject-rc" \
  -H "X-API-Key: ess_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" \
  -H "Content-Type: application/json" \
  -d '{"image_tag": "v1.2.3"}'
```

### Response Example (200)

```json
{
  "account_slug": "my-team",
  "organization": "my-apps-org",
  "app": "my-app",
  "environment": "QA",
  "image_name": "my-app",
  "image_tag": "v1.2.3",
  "state": "REJECTED",
  "state_timestamp": "2025-09-30T12:00:00Z"
}
```

---

## POST .../environments/QA/declare-stable

Set current QA deployment image to STABLE

```
POST /api/v1/accounts/{account_slug}/organizations/{organization_login}/apps/{app_name}/environments/QA/declare-stable
```

No body. Sets the current QA deployment image's lifecycle state to STABLE.

### Request Example

```
curl -X POST \
  "https://www.essesseff.com/api/v1/accounts/my-team/organizations/my-apps-org/apps/my-app/environments/QA/declare-stable" \
  -H "X-API-Key: ess_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" \
  -H "Content-Type: application/json" \
  -d '{}'
```

### Response Example (200)

```json
{
  "account_slug": "my-team",
  "organization": "my-apps-org",
  "app": "my-app",
  "environment": "QA",
  "image_name": "my-app",
  "image_tag": "v1.2.3",
  "state": "STABLE",
  "state_timestamp": "2025-09-30T12:00:00Z"
}
```

---

## POST .../environments/QA/declare-rejected

Set current QA deployment image to REJECTED

```
POST /api/v1/accounts/{account_slug}/organizations/{organization_login}/apps/{app_name}/environments/QA/declare-rejected
```

No body. Sets the current QA deployment image's lifecycle state to REJECTED.

### Request Example

```
curl -X POST \
  "https://www.essesseff.com/api/v1/accounts/my-team/organizations/my-apps-org/apps/my-app/environments/QA/declare-rejected" \
  -H "X-API-Key: ess_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" \
  -H "Content-Type: application/json" \
  -d '{}'
```

### Response Example (200)

```json
{
  "account_slug": "my-team",
  "organization": "my-apps-org",
  "app": "my-app",
  "environment": "QA",
  "image_name": "my-app",
  "image_tag": "v1.2.3",
  "state": "REJECTED",
  "state_timestamp": "2025-09-30T12:00:00Z"
}
```

---

## POST .../environments/STAGING/deploy-stable

Deploy STABLE image to STAGING

```
POST /api/v1/accounts/{account_slug}/organizations/{organization_login}/apps/{app_name}/environments/STAGING/deploy-stable
```

Body: `image_tag`. Deploys the given STABLE image to STAGING (lifecycle STAGING, config_staging promotion, deployment record).

### Request Example

```
curl -X POST \
  "https://www.essesseff.com/api/v1/accounts/my-team/organizations/my-apps-org/apps/my-app/environments/STAGING/deploy-stable" \
  -H "X-API-Key: ess_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" \
  -H "Content-Type: application/json" \
  -d '{"image_tag": "v1.2.3"}'
```

### Response Example (200)

```json
{
  "account_slug": "my-team",
  "organization": "my-apps-org",
  "app": "my-app",
  "environment": "STAGING",
  "image_name": "my-app",
  "image_tag": "v1.2.3",
  "state": "STAGING",
  "state_timestamp": "2025-09-30T12:00:00Z"
}
```

---

## POST .../environments/PROD/deploy-stable

Deploy STABLE image to PROD (no OTP required via API)

```
POST /api/v1/accounts/{account_slug}/organizations/{organization_login}/apps/{app_name}/environments/PROD/deploy-stable
```

Body: `image_tag`, optional `deployment_note`. Same as STAGING but for PROD. No OTP required when using the API.

### Request Example

```
curl -X POST \
  "https://www.essesseff.com/api/v1/accounts/my-team/organizations/my-apps-org/apps/my-app/environments/PROD/deploy-stable" \
  -H "X-API-Key: ess_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" \
  -H "Content-Type: application/json" \
  -d '{"image_tag": "v1.2.3", "deployment_note": "CR#12345"}'
```

### Response Example (200)

```json
{
  "account_slug": "my-team",
  "organization": "my-apps-org",
  "app": "my-app",
  "environment": "PROD",
  "image_name": "my-app",
  "image_tag": "v1.2.3",
  "state": "PROD",
  "state_timestamp": "2025-09-30T12:00:00Z",
  "deployment_note": "CR#12345"
}
```

Response includes `deployment_note` (the value sent in the request body, or `null` if omitted).
