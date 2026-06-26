---
name: openclaw-essesseff
description: Interact with the essesseff DevOps platform — call the essesseff Public API (templates, organizations, apps, deployments, images, image lifecycle, environments, retention policies, packages) and automate app creation and Argo CD setup using the essesseff onboarding utility. Use when the user wants to create essesseff apps, manage deployments, promote images through the DEV→QA→STAGING→PROD lifecycle, configure Argo CD environments, manage retention policies, or run the essesseff-onboard.sh script.
version: 1.0.0
metadata:
  openclaw:
    emoji: "🦞"
    homepage: https://github.com/essesseff/essesseff-onboarding-utility
    primaryEnv: ESSESSEFF_API_KEY
    requires:
      bins:
        - curl
        - bash
        - git
        - jq
        - kubectl
      env:
        - ESSESSEFF_API_KEY
        - ESSESSEFF_ACCOUNT_SLUG
        - GITHUB_ORG
        - APP_NAME
        - GITHUB_TOKEN
        - ARGOCD_MACHINE_USER
        - ARGOCD_MACHINE_EMAIL
        - GITHUB_ORG_ADMIN_PAT
        - TEMPLATE_NAME
        - TEMPLATE_IS_GLOBAL
        - K8S_NAMESPACE
---

# essesseff Skill

This skill covers two complementary ways to work with the essesseff DevOps platform:

1. **essesseff Public API** — direct HTTP calls for managing templates, organizations, apps, images, deployments, environments, packages, and retention policies.
2. **essesseff Onboarding Utility** — shell scripts that automate app creation and Argo CD deployment setup.

## Quick Reference

**Base URL:** `https://www.essesseff.com/api/v1` (use `www` to avoid 307 redirects)

**Authentication:** All requests require `X-API-Key: ess_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` header.

**Rate limit:** 3 requests per 10 seconds. Headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`.

**Path structure:**
- Global (no account needed): `/api/v1/global/...`
- Account-specific: `/api/v1/accounts/{account_slug}/...` — API key must belong to the `account_slug` in the path or a `403` is returned.

## API Reference Files

For full endpoint details, request/response examples, and query parameters, see:

| Reference | Contents |
|---|---|
| `references/api-overview.md` | Auth, base URL, rate limiting, error codes |
| `references/api-templates.md` | Global templates, account-specific templates |
| `references/api-organizations.md` | List and detail GitHub orgs for an account |
| `references/api-apps.md` | Create, list, get, update apps; list deployments |
| `references/api-images.md` | List images, get image by tag |
| `references/api-images.md` | Image lifecycle: get state, transition state |
| `references/api-environments.md` | Get environment; set Argo CD URL; DEV→QA→STAGING→PROD lifecycle actions |
| `references/api-packages.md` | Get GitHub API payloads for expired package deletion |
| `references/api-retention-policies.md` | List and update retention policies |

## API Endpoint Map

### Global

| Method | Path | Purpose |
|---|---|---|
| GET | `/global/templates` | List global templates (optional `?language=go\|python\|node\|java\|rust\|php`) |
| GET | `/global/templates/{template_name}` | Get global template details |

### Account-Specific (all require matching API key)

| Method | Path | Purpose |
|---|---|---|
| GET | `/accounts/{account_slug}/templates` | List account templates |
| GET | `/accounts/{account_slug}/templates/{template_name}` | Get account template details |
| GET | `/accounts/{account_slug}/organizations` | List orgs for account |
| GET | `/accounts/{account_slug}/organizations/{org_login}` | Get org detail + app list |
| GET | `/accounts/{account_slug}/organizations/{org_login}/apps` | List apps |
| POST | `/accounts/{account_slug}/organizations/{org_login}/apps?app_name={name}` | Create app |
| GET | `/accounts/{account_slug}/organizations/{org_login}/apps/{app_name}` | Get app detail |
| PATCH | `/accounts/{account_slug}/organizations/{org_login}/apps/{app_name}` | Update app |
| GET | `.../apps/{app_name}/deployments` | List deployments |
| GET | `.../apps/{app_name}/images` | List images |
| GET | `.../apps/{app_name}/images/{image_tag}` | Get image by tag |
| GET | `.../apps/{app_name}/images/{image_tag}/lifecycle` | Get image lifecycle state |
| POST | `.../apps/{app_name}/images/{image_tag}/lifecycle` | Transition image lifecycle state |
| GET | `.../apps/{app_name}/environments/{env}` | Get current env deployment |
| POST | `.../apps/{app_name}/environments/{env}/set-argocd-application-url` | Set/clear Argo CD URL |
| POST | `.../apps/{app_name}/environments/DEV/declare-rc` | Mark DEV image as RC |
| POST | `.../apps/{app_name}/environments/QA/accept-rc` | Accept RC → deploy to QA |
| POST | `.../apps/{app_name}/environments/QA/reject-rc` | Reject RC |
| POST | `.../apps/{app_name}/environments/QA/declare-stable` | Mark QA image as STABLE |
| POST | `.../apps/{app_name}/environments/QA/declare-rejected` | Mark QA image as REJECTED |
| POST | `.../apps/{app_name}/environments/STAGING/deploy-stable` | Deploy STABLE to STAGING |
| POST | `.../apps/{app_name}/environments/PROD/deploy-stable` | Deploy STABLE to PROD (no OTP) |
| GET | `.../apps/{app_name}/notifications-secret` | Get notifications-secret.yaml for Argo CD |
| GET | `.../apps/{app_name}/packages/delete-packages` | Get expired package deletion payloads |
| GET | `.../apps/{app_name}/retention-policies` | List retention policies (filter by `?state=`) |
| PATCH | `.../apps/{app_name}/retention-policies?state={state}` | Create or update a retention policy for a lifecycle state |

## Image Lifecycle State Machine

Images progress through states in this order:

```
BUILD → DEV → RC → QA → STABLE → STAGING → PROD
              ↑  ↓  ↓
            REJECTED
```

Key transitions via API:
- `DEV/declare-rc` — promotes current DEV image to RC (no body)
- `QA/accept-rc` — body: `{"image_tag": "v1.2.3"}` → sets QA, deploys to QA
- `QA/reject-rc` — body: `{"image_tag": "v1.2.3"}` → sets REJECTED
- `QA/declare-stable` — no body → sets STABLE on current QA image
- `QA/declare-rejected` — no body → sets REJECTED on current QA image
- `STAGING/deploy-stable` — body: `{"image_tag": "v1.2.3"}` → deploys to STAGING
- `PROD/deploy-stable` — body: `{"image_tag": "v1.2.3", "deployment_note": "CR#123"}` → deploys to PROD (no OTP required via API)

Alternatively, use `POST .../images/{image_tag}/lifecycle` with body `{"state": "QA"}` for direct lifecycle transitions.

## Onboarding Utility Reference

For shell-script-based automation (no API calls required), see:

| Reference | Contents |
|---|---|
| `references/onboarding-utility.md` | Full guide: setup, commands, how it works |
| `references/prerequisites.md` | System binaries, PATs, K8s/Argo CD prereqs |
| `references/non-subscriber-mode.md` | Clone/replace/push workflow without a subscription |

The utility (`essesseff-onboard.sh`) accepts:
- `--list-templates` — list available templates
- `--create-app` — create all 9 repos (via API for subscribers, clone/replace/push for non-subscribers)
- `--setup-argocd dev,qa,staging,prod` — configure Argo CD for each environment
- `--non-essesseff-subscriber-mode` — no essesseff API required
- `--config-file .essesseff` — path to config file
- `--verbose` — debug output

## Common Errors

| Code | Meaning |
|---|---|
| 400 | Invalid request parameters |
| 401 | Invalid or missing API key |
| 403 | API key does not match the `account_slug` in the path |
| 404 | Resource not found |
| 429 | Rate limit exceeded — wait and retry |
| 500 | Server error |
