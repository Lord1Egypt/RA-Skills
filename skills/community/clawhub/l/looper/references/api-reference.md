# Looper API Reference

Base URL: `https://api.looper.bot`

All authenticated endpoints require `Authorization: Bearer <admin-key>`.

## Public Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | /health | Health check |
| POST | /api/signup | Create account |
| POST | /api/login | Login (returns tenant info) |

## Loop Management

| Method | Path | Description |
|--------|------|-------------|
| GET | /api/loops | List all loops for tenant |
| POST | /api/loops | Create a new loop |
| GET | /api/loops/:id | Get loop details |
| PATCH | /api/loops/:id | Update loop settings |
| DELETE | /api/loops/:id | Delete a loop |
| POST | /api/loops/:id/run | Trigger manual run |
| GET | /api/loops/:id/runs | Get run history |
| GET | /api/loops/:id/runs/:runId | Get run details |
| GET | /api/loops/:id/runs/:runId/improvements | Get improvements from a run |

## Templates

| Method | Path | Description |
|--------|------|-------------|
| GET | /api/templates | List available templates |
| GET | /api/templates/:id | Get template details |

## Built-in Template IDs

| Template | ID | Engine |
|----------|-----|--------|
| Blog Kit | `68b7e661-46e1-45cd-b25a-584b8cd392b1` | create |
| Social Kit | `7431b897-396f-4542-8e32-d8d1c5e445a2` | social |

## API Keys

| Method | Path | Description |
|--------|------|-------------|
| GET | /api/keys | List API keys (metadata only) |
| POST | /api/keys | Generate new API key |

## GitHub

| Method | Path | Description |
|--------|------|-------------|
| GET | /api/github/connect | Get GitHub OAuth URL |
| GET | /api/github/callback | OAuth callback (browser) |
| GET | /api/github/status | Check GitHub connection |

## Stripe Billing

| Method | Path | Description |
|--------|------|-------------|
| POST | /api/stripe/checkout | Create checkout session |
| POST | /api/stripe/portal | Create billing portal session |

## Tenant

| Method | Path | Description |
|--------|------|-------------|
| GET | /api/tenant | Get current tenant info |
| PATCH | /api/tenant | Update tenant settings |

## Loop Create/Update Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| name | string | yes | - | Loop display name |
| target_type | string | yes | - | `github`, `file`, `url`, or `text` |
| target_config | object | yes | - | Target-specific config |
| template_id | string | no | - | Template to use |
| questions | string[] | yes | - | Prompts that drive the loop |
| schedule | string | yes | - | Cron expression |
| schedule_tz | string | no | UTC | Timezone for schedule |
| mode | string | no | auto | `auto`, `propose`, or `notify` |
| model | string | no | gemini-2.0-flash | AI model to use |
| enabled | boolean | no | true | Whether loop is active |
| max_runs_per_day | number | no | 0 | Daily run limit (0 = unlimited) |

## GitHub Target Config

```json
{
  "owner": "github-username-or-org",
  "repo": "repository-name",
  "branch": "main",
  "path": "optional/subdirectory"
}
```
