---
name: leadgenius-cli
description: Operate the LeadGenius Pro Automation API and lgp CLI — ICP management, FSD pipeline automation, lead generation/enrichment/scoring, user provisioning, territory analysis, webhooks, and email platform integration.
metadata: {"openclaw":{"emoji":"🎯","homepage":"https://github.com/thierryteisseire/leadgenius-cli","primaryEnv":"LGP_API_KEY","requires":{"env":["LGP_API_KEY"]}}}
---

# LeadGenius Pro — CLI & Automation API Skill

This skill teaches AI agents how to operate the **LeadGenius Pro Automation API** and the **`lgp` CLI tool**. It covers the full lifecycle of B2B lead management — from ICP (Ideal Customer Profile) definition and automated lead generation through enrichment, scoring, qualification, and email delivery via the FSD (Full-Stack Demand) pipeline.

> **Documentation-only package.** The `lgp` CLI script (`lgp.py`) is part of the LeadGenius Pro application repository and is not included in this skill package. Obtain the CLI from your LeadGenius Pro deployment.

## Base URL

```
https://api.leadgenius.app
```

All API endpoints live under `/api/automation/`.

## Authentication

Every request must include an API key in the `X-API-Key` header:

```
X-API-Key: lgp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

- Keys are prefixed with `lgp_` and tied to a specific company.
- The key determines `company_id`, `owner` identity, and rate limits.
- Keys are created via `POST /api/automation/users/provision` — the plain-text key is returned only once at creation time.
- Test your key with `GET /api/automation/auth/test`.

### Required Environment Variables

| Variable | Required | Description | Default |
|----------|----------|-------------|---------|
| `LGP_API_KEY` | **Yes** | API key with `lgp_` prefix. Required for all API and CLI operations. | — |
| `LGP_URL` | No | Base URL of the LeadGenius Pro API. | `http://localhost:3000` |
| `LGP_ADMIN_KEY` | No | Admin key to bypass rate limits. Sent as `X-Admin-Key` header alongside `X-API-Key`. Grants elevated access — use only for admin operations. | — |

### Rate Limits

| Window     | Default Limit    |
|------------|------------------|
| Per minute | 60 requests      |
| Per hour   | 1,000 requests   |
| Per day    | 10,000 requests  |

---

## Prerequisites Checklist

Before running enrichment, copyright, scoring, or FSD pipelines, the following configuration records must exist. Create them via the Tables API (`POST /api/automation/tables/{tableName}`).

### UrlSettings (required for enrichment)

| Field                | Description                              |
|----------------------|------------------------------------------|
| `companyUrl`         | Company URL lookup service endpoint      |
| `companyUrl_Apikey`  | API key for company URL service          |
| `emailFinder`        | Email finder service endpoint            |
| `emailFinder_Apikey` | API key for email finder service         |
| `enrichment1`–`enrichment10` | Enrichment service endpoints (up to 10) |
| `enrichment1_Apikey`–`enrichment10_Apikey` | Corresponding API keys |

### AgentSettings (required for copyright / AI content generation)

| Field                          | Description                                |
|--------------------------------|--------------------------------------------|
| `projectId`                    | EpsimoAI project ID                        |
| `enrichment1AgentId`–`enrichment10AgentId` | EpsimoAI agent IDs for each copyright process |

### SdrAiSettings (required for SDR AI scoring)

| Field                          | Description                                |
|--------------------------------|--------------------------------------------|
| `projectId`                    | EpsimoAI project ID                        |
| `aiLeadScoreAgentId`          | Agent for lead scoring                     |
| `aiQualificationAgentId`      | Agent for qualification assessment         |
| `aiNextActionAgentId`         | Agent for next-action recommendation       |
| `aiColdEmailAgentId`          | Agent for cold email generation            |
| `aiInterestAgentId`           | Agent for interest analysis                |
| `aiLinkedinConnectAgentId`    | Agent for LinkedIn connect messages        |
| `aiCompetitorAnalysisAgentId` | Agent for competitor analysis              |
| `aiEngagementLevelAgentId`    | Agent for engagement level assessment      |
| `aiPurchaseWindowAgentId`     | Agent for purchase window estimation       |
| `aiDecisionMakerRoleAgentId`  | Agent for decision-maker role detection    |
| `aiSentimentAgentId`          | Agent for sentiment analysis               |
| `aiSocialEngagementAgentId`   | Agent for social engagement scoring        |
| `aiNurturingStageAgentId`     | Agent for nurturing stage classification   |
| `aiBudgetEstimationAgentId`   | Agent for budget estimation                |
| `aiRiskScoreAgentId`          | Agent for risk scoring                     |
| `aiProductFitScoreAgentId`    | Agent for product-fit scoring              |

### ICP with Apify Config (required for lead generation)

| Field             | Description                                      |
|-------------------|--------------------------------------------------|
| `name`            | ICP display name                                 |
| `apifyActorId`    | Apify actor ID for lead scraping (required)      |
| `apifyInput`      | JSON string of actor input configuration         |
| `apifySettings`   | JSON string of additional Apify settings         |
| `maxLeads`        | Max leads per generation run (default 100)       |
| `industries`      | JSON array of target industries                  |
| `companySizes`    | JSON array of size ranges ("1-10", "51-200")     |
| `geographies`     | JSON array of countries/regions                  |
| `jobTitles`       | JSON array of target job titles                  |
| `seniority`       | JSON array of seniority levels                   |
| `client_id`       | Client partition for data isolation              |

### Client (required for data isolation)

| Field         | Description                          |
|---------------|--------------------------------------|
| `clientName`  | Display name for the client          |
| `companyURL`  | Company website URL                  |
| `description` | Client description                   |

### EmailPlatformSettings (required for email delivery)

| Field        | Description                              |
|--------------|------------------------------------------|
| `platform`   | Email platform name (e.g., "woodpecker") |
| `apiKey`     | Platform API key                         |
| `campaignId` | Default campaign ID on the platform      |

---

## Quick-Reference: Endpoint Map

| API Section         | Reference                                                        |
|---------------------|------------------------------------------------------------------|
| Auth                | [references/api_endpoints.md#authentication](references/api_endpoints.md#authentication) |
| Leads               | [references/api_endpoints.md#leads](references/api_endpoints.md#leads) |
| Tasks               | [references/api_endpoints.md#tasks](references/api_endpoints.md#tasks) |
| Lead Generation     | [references/api_endpoints.md#lead-generation](references/api_endpoints.md#lead-generation) |
| Territory           | [references/api_endpoints.md#territory-companies](references/api_endpoints.md#territory-companies) |
| Webhooks            | [references/api_endpoints.md#webhook-events](references/api_endpoints.md#webhook-events) |
| Users               | [references/api_endpoints.md#users](references/api_endpoints.md#users) |
| Organizations       | [references/api_endpoints.md#organizations](references/api_endpoints.md#organizations) |
| Tables / ICP        | [references/api_endpoints.md#tables-generic-crud-with-icp-focus](references/api_endpoints.md#tables-generic-crud-with-icp-focus) |
| Email Platforms     | [references/api_endpoints.md#email-platforms](references/api_endpoints.md#email-platforms) |
| FSD Pipeline        | [references/api_endpoints.md#fsd-pipeline](references/api_endpoints.md#fsd-pipeline) |
| Job Ad Lead Triggering | [references/api_endpoints.md#job-ad-lead-triggering](references/api_endpoints.md#job-ad-lead-triggering) |
| Lead Notifications (Unipile) | [references/api_endpoints.md#lead-notifications-unipile](references/api_endpoints.md#lead-notifications-unipile) |
| EpsimoAI            | [references/api_endpoints.md#epsimoai-user--credit-management](references/api_endpoints.md#epsimoai-user--credit-management) |
| Account-Based Lead Analysis | [references/api_endpoints.md#account-based-lead-analysis](references/api_endpoints.md#account-based-lead-analysis) |
| Error Codes         | [references/api_endpoints.md#error-codes](references/api_endpoints.md#error-codes) |

## Quick-Reference: CLI Map

| Command Group      | Reference                                                          |
|--------------------|--------------------------------------------------------------------|
| `auth`             | [references/cli_reference.md#auth](references/cli_reference.md#auth) |
| `leads`            | [references/cli_reference.md#leads](references/cli_reference.md#leads) |
| `tasks`            | [references/cli_reference.md#tasks](references/cli_reference.md#tasks) |
| `generate`         | [references/cli_reference.md#generate](references/cli_reference.md#generate) |
| `clients`          | [references/cli_reference.md#clients](references/cli_reference.md#clients) |
| `maintenance`      | [references/cli_reference.md#maintenance](references/cli_reference.md#maintenance) |
| `pipeline`         | [references/cli_reference.md#pipeline](references/cli_reference.md#pipeline) |
| `campaigns`        | [references/cli_reference.md#campaigns](references/cli_reference.md#campaigns) |
| `companies`        | [references/cli_reference.md#companies](references/cli_reference.md#companies) |
| `webhooks`         | [references/cli_reference.md#webhooks](references/cli_reference.md#webhooks) |
| `tables`           | [references/cli_reference.md#tables](references/cli_reference.md#tables) |
| `email-platforms`  | [references/cli_reference.md#email-platforms](references/cli_reference.md#email-platforms) |
| `users`            | [references/cli_reference.md#users](references/cli_reference.md#users) |
| `cognito`          | [references/cli_reference.md#cognito](references/cli_reference.md#cognito) |
| `org`              | [references/cli_reference.md#org](references/cli_reference.md#org) |
| `fsd`              | [references/cli_reference.md#fsd](references/cli_reference.md#fsd) |
| `epsimo`           | [references/cli_reference.md#epsimoai-commands](references/cli_reference.md#epsimoai-commands) |
| `admin`            | [references/cli_reference.md#admin](references/cli_reference.md#admin) |
| `account-analysis` | [references/cli_reference.md#account-analysis](references/cli_reference.md#account-analysis) |

---

## Maintenance CLI (Standalone Node.js Scripts)

Standalone scripts for managing maintenance items (bugs, enhancements). These use raw GraphQL over HTTPS with API key auth from `amplify_outputs.json` — they do NOT go through the Automation API or `lgp` CLI.

### Create a maintenance item

```bash
node scripts/create-maintenance-item.js --type=BUG --description="Login fails on mobile"
node scripts/create-maintenance-item.js --type=ENHANCEMENT --description="Add bulk export feature"
```

| Flag | Required | Values | Description |
|------|----------|--------|-------------|
| `--type` | Yes | `BUG`, `ENHANCEMENT` | Item type |
| `--description` | Yes | string | Description of the issue or request |

### List maintenance items

```bash
node scripts/list-maintenance-items.js
node scripts/list-maintenance-items.js --type=BUG
node scripts/list-maintenance-items.js --type=BUG --status=OPEN
node scripts/list-maintenance-items.js --company-id=company-xxx
```

| Flag | Required | Values | Description |
|------|----------|--------|-------------|
| `--type` | No | `BUG`, `ENHANCEMENT` | Filter by type |
| `--status` | No | `OPEN`, `IN_PROGRESS`, `RESOLVED`, `CLOSED` | Filter by status |
| `--company-id` | No | string | Filter by company ID |

### Update a maintenance item

```bash
node scripts/update-maintenance-item.js --id=<UUID> --status=RESOLVED
node scripts/update-maintenance-item.js --id=<UUID> --status=CLOSED --description="Fixed in v2.1"
```

| Flag | Required | Values | Description |
|------|----------|--------|-------------|
| `--id` | Yes | UUID | Full maintenance item ID |
| `--status` | No | `OPEN`, `IN_PROGRESS`, `RESOLVED`, `CLOSED` | New status |
| `--description` | No | string | Updated description |

### Maintenance REST API

There is also a REST API at `/api/maintenance` supporting full CRUD with JWT or API key auth. See the `leadgenius-api` skill for details.

---

## Documentation Site

Docsify-based docs are served at `/docs` (e.g., `https://api.leadgenius.app/docs`). Source files in `/docs/`, copied to `public/docs-content/` at build time.

---

## API Behavioral Notes (2026-03-27)

Important behavioral changes that affect CLI and API consumers:

### Leads List Pagination (GET /api/automation/leads)

- **Max page size capped at 50.** The `limit` parameter is clamped to 50 regardless of the value passed. Callers must paginate via `nextToken` to retrieve all leads.
- **Orphaned leads mode:** Pass `client_id=__orphaned__` to find leads with null/empty `client_id` within your company. These leads are invisible to normal GSI queries.
- **Cross-tenant validation:** The API now validates that the requested `client_id` belongs to your company before querying. Foreign `client_id` values return 403.

### Lead Import Upsert (POST /api/automation/leads/import)

- **Idempotent by email:** If a lead with the same `email` already exists in the **same** `client_id`, the import updates the existing record instead of creating a duplicate. This makes retries after ECONNRESET safe.
- **Explicit ID upsert:** If the payload includes an `id` field that matches an existing lead, it updates instead of crashing with a DynamoDB conditional error.
- **Empty strings → null:** Empty string values (`""`) are automatically converted to `null` before write to prevent DynamoDB GSI `ValidationException` errors.
- **Response always includes `errors` and `warnings` arrays** (even when empty) for consistent CLI parsing.

### Lead Transfer (POST /api/automation/leads/transfer)

- **`skipSourceValidation: true`** — Allows transferring from an orphaned/deleted source client that no longer has a Client record.
- **`fromClientId: "__orphaned__"`** — Transfers leads with null/empty `client_id` to a valid target client.

### Generic Tables (POST /api/automation/tables/{tableName})

- **Client table auto-generates `client_id`** if not provided in the body, matching the behavior of `POST /api/clients`.
- **Tables without `client_id`** (Maintenance, Company, CompanyUser, etc.) no longer crash — the field is automatically stripped before the GraphQL mutation.
- **Table-specific fields** are now included in list/create responses (e.g., `clientName` for Client, `name` for ICP, `type`/`description`/`status` for Maintenance).

### Cross-Tenant Safety

- **Single lead GET** (`GET /api/automation/leads/{id}`) flags cross-tenant `client_id` references with a `_clientWarning` field and prefixes the value with `__foreign:`.
- All lead PUT/DELETE operations cascade across EnrichLeads, B2BLeads, and SourceLeads tables transparently.
