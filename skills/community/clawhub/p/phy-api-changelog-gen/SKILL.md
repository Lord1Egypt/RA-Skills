---
name: API Changelog Gen
description: OpenAPI/Swagger spec differ that generates human-readable API changelogs. Diffs two OpenAPI 3.x or Swagger 2.0 spec files (YAML or JSON) with a semantic diff — not a line-level text diff — and produces a structured changelog classifying every change as BREAKING (removed endpoint, removed required field, changed response type, narrowed enum, tightened auth) or NON-BREAKING (added optional field, new endpoint, relaxed constraint, added enum value). Outputs Markdown changelog for docs/PRs, JSON for CI pipelines, and a "migration guide" section addressed to API consumers. Detects auth scheme changes and removed security scopes. Supports local files and multiple spec versions in a git repo. Zero external API — pure local file parsing. Triggers on "api diff", "openapi diff", "what changed in the API", "breaking changes", "api changelog", "spec diff", "/api-changelog".
license: Apache-2.0
homepage: https://canlah.ai
metadata:
  author: Canlah AI
  version: "1.0.3"
  tags:
    - openapi
    - swagger
    - api-design
    - changelog
    - breaking-changes
    - developer-tools
    - rest-api
    - versioning
---

# API Changelog Generator

You ship a new API version. Your frontend team asks: "what changed?" You send them a GitHub diff of two 3,000-line YAML files.

This skill diffs two OpenAPI specs semantically — not line by line — and produces a consumer-facing changelog that clearly separates breaking changes from additions, grouped by endpoint.

**Supports OpenAPI 3.x and Swagger 2.0. Zero external API.**

---

## Trigger Phrases

- "api diff", "openapi diff", "swagger diff"
- "what changed in the API", "breaking changes"
- "api changelog", "spec diff", "schema diff"
- "which endpoints changed", "removed fields"
- "was this a breaking change", "api migration guide"
- "/api-changelog"

---

## How to Provide Input

```bash
# Option 1: Diff two local spec files
/api-changelog openapi-v1.yaml openapi-v2.yaml

# Option 2: Diff against git history (current vs previous commit)
/api-changelog openapi.yaml --vs HEAD~1
/api-changelog openapi.yaml --vs main

# Option 3: Diff against a tagged version
/api-changelog openapi.yaml --vs v2.0.0:openapi.yaml

# Option 4: Output only breaking changes
/api-changelog v1.yaml v2.yaml --breaking-only

# Option 5: Generate consumer migration guide
/api-changelog v1.yaml v2.yaml --migration-guide

# Option 6: Output JSON for CI
/api-changelog v1.yaml v2.yaml --json

# Option 7: Fail CI if breaking changes detected
/api-changelog v1.yaml v2.yaml --fail-on-breaking
```

---

## Step 1: Load and Normalize Specs

```python
import json
import yaml
from pathlib import Path

def load_spec(path: str) -> dict:
    """Load OpenAPI 3.x or Swagger 2.0 spec from YAML or JSON."""
    content = Path(path).read_text(encoding='utf-8')

    if path.endswith('.json'):
        spec = json.loads(content)
    else:
        spec = yaml.safe_load(content)

    # Detect version
    version = spec.get('openapi', spec.get('swagger', 'unknown'))

    # Normalize Swagger 2.0 → OpenAPI 3.0 structure for comparison
    if str(version).startswith('2.'):
        spec = normalize_swagger2(spec)

    return spec


def normalize_swagger2(spec: dict) -> dict:
    """Normalize Swagger 2.0 paths to OpenAPI 3.0 structure for diffing."""
    # Convert basePath + paths → servers + paths
    base = spec.get('basePath', '')
    if base and 'servers' not in spec:
        spec['servers'] = [{'url': base}]

    # Convert definitions → components.schemas
    if 'definitions' in spec and 'components' not in spec:
        spec['components'] = {'schemas': spec.pop('definitions')}

    return spec


def extract_endpoints(spec: dict) -> dict:
    """Extract all endpoints as {(method, path): operation_object}."""
    endpoints = {}
    for path, path_item in spec.get('paths', {}).items():
        for method in ['get', 'post', 'put', 'patch', 'delete', 'head', 'options']:
            if method in path_item:
                endpoints[(method.upper(), path)] = path_item[method]
    return endpoints


def extract_schemas(spec: dict) -> dict:
    """Extract all component schemas."""
    return spec.get('components', {}).get('schemas', {})
```

---

## Step 2: Semantic Diff Engine

```python
from dataclasses import dataclass
from typing import Literal

@dataclass
class ApiChange:
    endpoint: str           # "POST /users" or "Schema: UserResponse"
    change_type: str        # e.g., "REMOVED_ENDPOINT", "ADDED_REQUIRED_FIELD"
    breaking: bool
    description: str
    old_value: str | None
    new_value: str | None
    migration_hint: str | None


def diff_endpoints(old_spec: dict, new_spec: dict) -> list[ApiChange]:
    """Find all endpoint-level changes."""
    changes = []
    old_eps = extract_endpoints(old_spec)
    new_eps = extract_endpoints(new_spec)

    old_keys = set(old_eps.keys())
    new_keys = set(new_eps.keys())

    # Removed endpoints (BREAKING)
    for key in old_keys - new_keys:
        method, path = key
        old_op = old_eps[key]
        changes.append(ApiChange(
            endpoint=f'{method} {path}',
            change_type='REMOVED_ENDPOINT',
            breaking=True,
            description=f'Endpoint `{method} {path}` was removed.',
            old_value=old_op.get('summary', '(no summary)'),
            new_value=None,
            migration_hint='Check for replacement endpoint. If deprecated, use the replacement.',
        ))

    # Added endpoints (NON-BREAKING)
    for key in new_keys - old_keys:
        method, path = key
        new_op = new_eps[key]
        changes.append(ApiChange(
            endpoint=f'{method} {path}',
            change_type='ADDED_ENDPOINT',
            breaking=False,
            description=f'New endpoint `{method} {path}` added.',
            old_value=None,
            new_value=new_op.get('summary', '(no summary)'),
            migration_hint=None,
        ))

    # Changed endpoints (analyze deeper)
    for key in old_keys & new_keys:
        method, path = key
        endpoint_str = f'{method} {path}'
        old_op = old_eps[key]
        new_op = new_eps[key]

        changes.extend(diff_operation(endpoint_str, old_op, new_op))

    return changes


def diff_operation(endpoint: str, old_op: dict, new_op: dict) -> list[ApiChange]:
    """Diff a single operation object."""
    changes = []

    # ── Parameters ──
    old_params = {p['name']: p for p in old_op.get('parameters', [])}
    new_params = {p['name']: p for p in new_op.get('parameters', [])}

    # Removed parameter
    for name in set(old_params) - set(new_params):
        param = old_params[name]
        changes.append(ApiChange(
            endpoint=endpoint,
            change_type='REMOVED_PARAMETER',
            breaking=True,
            description=f'Parameter `{name}` ({param.get("in", "?")}) removed.',
            old_value=f'required={param.get("required", False)}',
            new_value=None,
            migration_hint=f'Remove `{name}` from all requests to `{endpoint}`.',
        ))

    # Added required parameter (BREAKING), added optional (NON-BREAKING)
    for name in set(new_params) - set(old_params):
        param = new_params[name]
        is_required = param.get('required', False)
        changes.append(ApiChange(
            endpoint=endpoint,
            change_type='ADDED_REQUIRED_PARAMETER' if is_required else 'ADDED_OPTIONAL_PARAMETER',
            breaking=is_required,
            description=f'{"Required" if is_required else "Optional"} parameter `{name}` '
                        f'({param.get("in", "?")} — {param.get("schema", {}).get("type", "?")}) added.',
            old_value=None,
            new_value=str(param.get('schema', {})),
            migration_hint=f'Add `{name}` to requests to `{endpoint}`.' if is_required else None,
        ))

    # Changed parameter type (BREAKING)
    for name in set(old_params) & set(new_params):
        old_p = old_params[name]
        new_p = new_params[name]
        old_type = old_p.get('schema', {}).get('type')
        new_type = new_p.get('schema', {}).get('type')
        if old_type and new_type and old_type != new_type:
            changes.append(ApiChange(
                endpoint=endpoint,
                change_type='CHANGED_PARAMETER_TYPE',
                breaking=True,
                description=f'Parameter `{name}` type changed: `{old_type}` → `{new_type}`.',
                old_value=old_type,
                new_value=new_type,
                migration_hint=f'Update `{name}` values from {old_type} format to {new_type} format.',
            ))

    # ── Response Schemas ──
    old_responses = old_op.get('responses', {})
    new_responses = new_op.get('responses', {})

    for status_code in set(old_responses) & set(new_responses):
        changes.extend(diff_response_schema(
            endpoint, status_code, old_responses[status_code], new_responses[status_code]
        ))

    # Removed successful response (BREAKING)
    for code in set(old_responses) - set(new_responses):
        if str(code).startswith('2'):
            changes.append(ApiChange(
                endpoint=endpoint,
                change_type='REMOVED_RESPONSE_CODE',
                breaking=True,
                description=f'Response code `{code}` removed.',
                old_value=str(code),
                new_value=None,
                migration_hint=f'Update response handling — `{code}` no longer returned.',
            ))

    # ── Auth Changes ──
    old_security = old_op.get('security', [])
    new_security = new_op.get('security', [])
    if old_security != new_security:
        changes.append(ApiChange(
            endpoint=endpoint,
            change_type='CHANGED_SECURITY',
            breaking=True,
            description=f'Security requirements changed for `{endpoint}`.',
            old_value=str(old_security),
            new_value=str(new_security),
            migration_hint='Update authentication headers/tokens for this endpoint.',
        ))

    return changes


def diff_response_schema(endpoint: str, code: str, old_resp: dict, new_resp: dict) -> list[ApiChange]:
    """Diff response schema for a specific status code."""
    changes = []

    def get_schema(resp):
        content = resp.get('content', {})
        for media_type in ['application/json', '*/*']:
            if media_type in content:
                return content[media_type].get('schema', {})
        return resp.get('schema', {})  # Swagger 2.0

    old_schema = get_schema(old_resp)
    new_schema = get_schema(new_resp)

    if not old_schema or not new_schema:
        return []

    old_props = old_schema.get('properties', {})
    new_props = new_schema.get('properties', {})
    old_required = set(old_schema.get('required', []))
    new_required = set(new_schema.get('required', []))

    # Removed field from response (may be BREAKING if consumers rely on it)
    for field in set(old_props) - set(new_props):
        changes.append(ApiChange(
            endpoint=endpoint,
            change_type='REMOVED_RESPONSE_FIELD',
            breaking=True,
            description=f'Response field `{field}` removed from `{code}` response.',
            old_value=str(old_props[field].get('type', '?')),
            new_value=None,
            migration_hint=f'Remove references to `response.{field}` in client code.',
        ))

    # Added field to response (NON-BREAKING)
    for field in set(new_props) - set(old_props):
        changes.append(ApiChange(
            endpoint=endpoint,
            change_type='ADDED_RESPONSE_FIELD',
            breaking=False,
            description=f'New field `{field}` ({new_props[field].get("type", "?")}) '
                        f'added to `{code}` response.',
            old_value=None,
            new_value=str(new_props[field].get('type', '?')),
            migration_hint=None,
        ))

    # Changed field type (BREAKING)
    for field in set(old_props) & set(new_props):
        old_type = old_props[field].get('type')
        new_type = new_props[field].get('type')
        if old_type and new_type and old_type != new_type:
            changes.append(ApiChange(
                endpoint=endpoint,
                change_type='CHANGED_RESPONSE_FIELD_TYPE',
                breaking=True,
                description=f'Response field `{field}` type changed: `{old_type}` → `{new_type}`.',
                old_value=old_type,
                new_value=new_type,
                migration_hint=f'Update client code to handle `{field}` as `{new_type}`.',
            ))

    # New required field in request body (BREAKING)
    new_required_added = new_required - old_required
    for field in new_required_added:
        if field in new_props:
            changes.append(ApiChange(
                endpoint=endpoint,
                change_type='ADDED_REQUIRED_FIELD',
                breaking=True,
                description=f'Field `{field}` is now required in `{code}` response contract.',
                old_value='optional',
                new_value='required',
                migration_hint=f'Ensure `{field}` is always included in request payloads.',
            ))

    return changes
```

---

## Step 3: Output Report

```markdown
## API Changelog
Diff: `openapi-v1.yaml` → `openapi-v2.yaml`
Generated: 2026-03-19

---

### Summary

| Category | Count |
|----------|-------|
| 🔴 Breaking Changes | 4 |
| 🟢 Non-Breaking Additions | 7 |
| 🟡 Deprecations | 2 |

**This release contains BREAKING changes. Clients MUST update before upgrading.**

---

## 🔴 Breaking Changes

### `DELETE /users/{id}` — REMOVED
The endpoint for deleting users has been removed.

**Migration:** Use `PATCH /users/{id}` with `{ "status": "deactivated" }` instead.
Soft-delete replaces hard-delete as of this version.

---

### `GET /orders` — Removed response field `order_total`
The `order_total` field was removed from order list responses.

**Migration:** Use `items_subtotal + tax_amount` from the same response to calculate the total.

```json
// Before:
{ "id": "ord_123", "order_total": 49.99, "items": [...] }

// After:
{ "id": "ord_123", "items_subtotal": 42.00, "tax_amount": 7.99, "items": [...] }
```

---

### `POST /checkout` — Added required parameter `idempotency_key`
All checkout requests now require an `idempotency_key` header parameter.

**Migration:** Generate a UUID per request and include it as:
```
Idempotency-Key: <uuid-v4>
```
Without this header, the server returns `400 Bad Request`.

---

### `GET /products/{id}` — Changed `price` type: `number` → `string`
The `price` field changed from a floating-point number to a decimal string to avoid floating-point precision issues.

**Migration:**
```js
// Before: const price = product.price * 100
// After:  const price = parseFloat(product.price) * 100
```

---

## 🟢 Non-Breaking Additions

| Change | Description |
|--------|-------------|
| `GET /users/{id}/preferences` | New endpoint for user preferences |
| `POST /webhooks` | Webhook registration endpoint |
| `GET /orders` `+cursor` | Added cursor-based pagination parameter (optional) |
| `GET /products` `+category_ids[]` | New array filter parameter (optional) |
| `UserResponse` `+avatar_url` | New optional field on user objects |
| `OrderResponse` `+shipping_eta` | New optional field on order objects |
| `GET /search` `+facets` | New optional faceted search support |

---

## 🟡 Deprecations

| Endpoint | Deprecated Field | Replacement | Sunset Date |
|----------|-----------------|-------------|-------------|
| `GET /users` | `full_name` | `first_name` + `last_name` | 2026-09-01 |
| `POST /auth/login` | `remember_me` param | Cookie-based session now automatic | 2026-06-01 |

---

## Migration Guide for API Consumers

1. **Remove `DELETE /users/{id}` calls** — replace with soft-delete via `PATCH /users/{id}` with `status: "deactivated"`
2. **Update order total calculation** — `order_total` removed; compute from `items_subtotal + tax_amount`
3. **Add `Idempotency-Key` header** to all `POST /checkout` requests
4. **Update price parsing** — `price` is now a decimal string, not a float
5. **Optional:** Migrate to cursor pagination on `GET /orders` for better performance

---

## CI Integration

```bash
# Fail CI if breaking changes are introduced
/api-changelog openapi-current.yaml openapi-new.yaml --fail-on-breaking
# Exit code 1 if breaking changes found, 0 if only additions
```

Add to `.github/workflows/api-review.yml`:
```yaml
- name: Check for breaking API changes
  run: |
    if git show HEAD~1:openapi.yaml > /tmp/openapi-prev.yaml 2>/dev/null; then
      python3 scripts/api-changelog.py /tmp/openapi-prev.yaml openapi.yaml --fail-on-breaking
    fi
```
```

---

## Quick Mode Output

```
API Changelog: openapi-v1.yaml → openapi-v2.yaml

🔴 4 BREAKING CHANGES:
  - DELETE /users/{id} removed → use PATCH with status: deactivated
  - GET /orders response: removed field order_total
  - POST /checkout: new required param idempotency_key
  - GET /products/{id}: price type changed number → string

🟢 7 non-breaking additions (3 new endpoints, 4 new optional fields)
🟡 2 deprecations (full_name field, remember_me param)

Run /api-changelog --migration-guide for consumer-facing migration steps
```

---

## Author

**[Canlah AI](https://canlah.ai)** — Run performance marketing without breaking your brand.

- GitHub: [github.com/PHY041](https://github.com/PHY041)
- All Skills: [clawhub.ai/PHY041](https://clawhub.ai/PHY041)
