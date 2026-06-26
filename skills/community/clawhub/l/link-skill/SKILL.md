---
name: LinkSKILL
description: Universal API integration skill for enterprise platforms. Connect to any platform using Swagger/OpenAPI discovery.
metadata: {"clawdbot":{"emoji":"🔗","requires":{"bins":["python3"],"pip":["requests"]}}}
---

# LinkSKILL — Universal Platform API Integration

LinkSKILL is a config-driven API integration skill for enterprise platforms.  
Given a Swagger/OpenAPI endpoint and auth settings, it can discover APIs, authenticate, and execute requests with minimal manual setup.

## When to Use This Skill

Use LinkSKILL when you need to:

- Integrate with a new internal/external platform quickly.
- Explore unknown APIs from Swagger/OpenAPI docs.
- Standardize auth + request execution across multiple platforms.
- Run repeatable API calls from CLI without custom one-off scripts.

## Core Workflow (4-Step Closed Loop)

1. **Identify platform**  
   Read `scripts/platform_config.json` and select `active_platform` (or pass `--platform` explicitly).
2. **Discover APIs**  
   `python scripts/swagger_loader.py --config scripts/platform_config.json --mode list`
3. **Authenticate**  
   `python scripts/auth_manager.py --config scripts/platform_config.json`
4. **Execute request**  
   `python scripts/http_request_tool.py --config scripts/platform_config.json --method POST --endpoint "/api/xxx" --json-body '...'`

Tip: Use `search` and `detail` before execution to reduce trial-and-error:

- `--mode search --keyword "keyword"`
- `--mode detail --path "/api/xxx" --method POST`

## Tool Responsibilities

| Tool | Responsibility |
|---|---|
| `swagger_loader.py` | Fetch and parse Swagger 2.0 / OpenAPI 3.x; supports `list`, `search`, `detail`, `tags`, `cache` |
| `auth_manager.py` | Handle auth login/token retrieval and local token cache management |
| `http_request_tool.py` | Send HTTP requests, inject auth headers, and auto re-auth + retry on 401 |

## Configuration Model

All behavior is driven by `scripts/platform_config.json`.

### Required top-level fields

- `active_platform`: default platform ID.
- `platforms`: map of platform definitions.

### Typical platform definition

- `name`: human-readable platform name.
- `gateway`: base URL used by request executor.
- `swagger.url`: OpenAPI/Swagger endpoint URL.
- `swagger.auth_required`: whether Swagger endpoint needs auth header.
- `auth.type`: one of `bearer_token`, `api_key`, `basic`, `none`.
- `default_headers`: default request headers.

### Auth field reference (for token login)

- `auth.login_endpoint`: login path (joined with `gateway`).
- `auth.login_body`: login payload.
- `auth.token_field`: token extraction path (for example `data.token`).
- `auth.token_header`: header name (default `Authorization`).
- `auth.token_prefix`: header prefix (default `Bearer `).

## Authentication Strategies

LinkSKILL supports:

- `none`: no auth required.
- `api_key`: static key from config.
- `basic`: build Basic credential from username/password.
- `bearer_token`: login API + token extraction + local cache.

Token cache file: `scripts/.token_cache.json`

## Discovery Modes (`swagger_loader.py`)

- `list`: print all available endpoints.
- `search`: fuzzy-match endpoints by path/summary/description/tags.
- `detail`: show parameters, request body schema/example, and response schema.
- `tags`: show API groups.
- `cache`: print local swagger cache location.

Swagger cache directory: `scripts/.swagger_cache/`

## Request Execution (`http_request_tool.py`)

Supports:

- Methods: `GET`, `POST`, `PUT`, `DELETE`, `PATCH`
- URL styles: full `--url` or `--endpoint` + `gateway`
- Payload: `--json-body` or `--json-file`
- Query params: `--params`
- Extra headers: `--headers`

On `401`, the tool can trigger `auth_manager.py --force-login` and retry once automatically.

## Recommended Operating Pattern

For stable integrations, run in this order:

1. `list` or `search` to locate target endpoint.
2. `detail` to inspect params/schema.
3. Authenticate and verify token cache.
4. Execute with minimal body first, then iterate.
5. Use cached swagger/token for faster repeated calls.

## Troubleshooting

- **Platform not found**: check `active_platform` and `platforms` keys.
- **Swagger fetch failed**: verify `swagger.url`, network, and TLS/headers.
- **Token extraction failed**: correct `auth.token_field` based on real login response.
- **401 on request**: verify token TTL/login payload and header prefix.
- **Non-JSON response**: inspect raw response text and endpoint behavior.

## Onboarding a New Platform

1. Add a new platform under `platforms` in `scripts/platform_config.json`.
2. Fill `gateway`, `swagger`, `auth`, and optional `default_headers`.
3. Set `active_platform` (or use `--platform`).
4. Run the 4-step workflow end-to-end and validate one successful API call.

## Notes and Constraints

- Designed for CLI-driven API integration workflows.
- Assumes APIs are discoverable via Swagger/OpenAPI endpoint.
- Uses local JSON files for cache; suitable for local/dev automation.
