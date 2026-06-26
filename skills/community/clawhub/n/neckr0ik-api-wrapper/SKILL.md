---
name: neckr0ik-api-wrapper
version: 1.0.0
description: Convert any REST API into an OpenClaw skill automatically. Generates SKILL.md, scripts, and claw.json from OpenAPI spec or URL. Use when you want to quickly create a skill for any API.
---

# API Wrapper Generator

Automatically generate OpenClaw skills from REST APIs.

## What This Does

- **Parses OpenAPI specs** — Read API documentation
- **Generates skill files** — SKILL.md, scripts, claw.json
- **Handles authentication** — API keys, OAuth, Bearer tokens
- **Creates type-safe wrappers** — Validates requests/responses
- **Documents endpoints** — Usage examples for each operation

## Quick Start

```bash
# Generate skill from OpenAPI spec
neckr0ik-api-wrapper generate --spec https://api.example.com/openapi.json --name my-api

# Generate from URL (discovers OpenAPI)
neckr0ik-api-wrapper generate --url https://api.example.com --name my-api

# Generate from local file
neckr0ik-api-wrapper generate --spec ./openapi.yaml --name my-api
```

## Output Structure

```
my-api/
├── SKILL.md           # Skill documentation
├── claw.json          # Package metadata
└── scripts/
    └── api.py         # Generated API client
```

## Supported Auth Types

| Type | Support | Config |
|------|---------|--------|
| API Key (header) | ✅ | `--auth header:X-API-Key` |
| API Key (query) | ✅ | `--auth query:api_key` |
| Bearer Token | ✅ | `--auth bearer` |
| Basic Auth | ✅ | `--auth basic` |
| OAuth 2.0 | ✅ | `--auth oauth2` |

## Commands

### generate

Generate OpenClaw skill from API spec.

```bash
neckr0ik-api-wrapper generate [options]

Options:
  --spec <url>          OpenAPI spec URL or file
  --url <url>           API base URL (discovers spec)
  --name <name>         Skill name (default: api name)
  --output <dir>        Output directory
  --auth <type>         Authentication type
  --include <endpoints> Include specific endpoints (comma-sep)
  --exclude <endpoints>  Exclude specific endpoints (comma-sep)
```

### validate

Validate OpenAPI spec before generating.

```bash
neckr0ik-api-wrapper validate --spec <url>
```

### test

Test generated skill against live API.

```bash
neckr0ik-api-wrapper test --skill ./my-api --endpoint <operationId>
```

## Generated Skill Example

```markdown
# Generated from Stripe API

## Quick Start

```bash
stripe-api customers list --limit 10
stripe-api customers create --email "user@example.com"
stripe-api charges create --amount 1000 --currency usd
```

## Endpoints

### customers.list
List all customers.
- Method: GET
- Path: /v1/customers
- Auth: Bearer Token

### customers.create
Create a new customer.
- Method: POST
- Path: /v1/customers
- Auth: Bearer Token
- Body: email, name, metadata
```

## Benefits

1. **Speed** — Generate skills in minutes, not hours
2. **Consistency** — Standard format for all API skills
3. **Documentation** — Auto-generated from OpenAPI
4. **Type Safety** — Request/response validation
5. **Maintainability** — Regenerate when API updates

## Use Cases

- **API Providers** — Create skills for your APIs
- **Developers** — Quickly integrate new APIs
- **Monetization** — Sell skills for popular APIs

## Example APIs to Wrap

- Stripe Payments API
- OpenAI API
- Slack API
- Notion API
- GitHub API
- Any OpenAPI-compliant API

## See Also

- `references/openapi.md` — OpenAPI specification guide
- `references/templates/` — Skill templates
- `scripts/generator.py` — Main generator