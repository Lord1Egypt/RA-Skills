# Json To Api

[中文版](./README_zh.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0-blue)](SKILL.md)

> Designs REST API endpoints and OpenAPI specs from raw JSON data — endpoints, schemas, HTTP methods

## What Problem This Solves

User has JSON data and needs a proper API contract — not just a data dump, but endpoints, HTTP methods, status codes, and request/response schemas. This skill analyzes JSON structure and produces a production-ready OpenAPI 3.0 spec.

**When triggered:** JSON data + API design/create endpoint/write OpenAPI intent.

## Features

- **Automatic resource detection** — identifies single objects vs. arrays vs. nested objects and designs appropriate endpoints
- **Full OpenAPI 3.0 output** — generates complete spec with paths, schemas, examples, and response definitions
- **Plural noun conventions** — uses `/users` not `/user`, follows REST best practices
- **Extensibility planning** — `/expand` mode adds pagination, filtering, sorting, and embedded resources

## Quick Start

```bash
# Via ClawHub
clawhub install json-to-api

# Or manually
cp -r json-to-api ~/.openclaw/skills/
```

### Usage

```
/json-to-api
```

Paste JSON, ask to design an API around it.

```
/json-to-api/expand
```

Adds pagination, filtering, sorting — for production-grade API surface.

## Modes

| Mode | Description |
|------|-------------|
| `/json-to-api` | Designs REST API endpoints with OpenAPI 3.0 spec |
| `/json-to-api/expand` | Adds pagination, filtering, sorting to base design |

## Examples

| JSON Shape | API Design |
|------------|------------|
| Array of user objects | `GET /users` (list), `POST /users` (create) |
| Single object with ID | `GET /users/{id}`, `PUT /users/{id}`, `DELETE /users/{id}` |
| Nested address object | `GET /users/{id}/addresses` as sub-resource |
| Optional phone field | Marked `nullable: true` in schema, not required |

## Directory Structure

```
json-to-api/
├── SKILL.md
├── LICENSE
├── README.md
├── README_zh.md
├── CONTRIBUTING.md
├── .gitignore
├── references/       # OpenAPI schema templates, HTTP conventions
└── tests/
```

## License

MIT License — see [LICENSE](LICENSE).