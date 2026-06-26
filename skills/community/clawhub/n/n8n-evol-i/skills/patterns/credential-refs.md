---
name: pattern-credential-refs
description: How workflow templates reference credentials — YAML shape and placeholder syntax.
user-invocable: false
---

# Pattern: credential refs (reference)

This is a **reference pattern** documenting the YAML shape and the `{{@env:credentials.<key>....}}` placeholder syntax. The actual creation/linking flow lives in [`skills/manage-credentials.md`](../manage-credentials.md).

## YAML shape

`<workspace>/n8n-config/<env>.yml` stores credentials under the `credentials` block:

```yaml
credentials:
  microsoft_oauth:
    id: "abcdef123456"
    name: "Microsoft 365 OAuth (Dev)"
    type: "microsoftOAuth2Api"
  redis_local:
    id: "ghijkl789012"
    name: "Redis Localhost"
    type: "redis"
```

The `id` and `name` fields are populated by `manage_credentials.py` (Path A or Path B). The `type` field is the n8n-side credential type string.

## Workflow template usage

Workflow templates reference credentials via the `credentials` block on each node:

```json
{
  "type": "n8n-nodes-base.microsoftExcel",
  "credentials": {
    "microsoftExcelOAuth2Api": {
      "id": "{{@env:credentials.microsoft_oauth.id}}",
      "name": "{{@env:credentials.microsoft_oauth.name}}"
    }
  }
}
```

## Why both `id` AND `name`

n8n verifies BOTH `id` and `name` match on activate. If a credential is renamed in the UI without resyncing, activation fails silently after deploy and only surfaces during activation — so a UI-side rename followed by deploy without resync is a common foot-gun.

**Mitigation:** if you suspect a name mismatch, run `resync` (which pulls the live credential names back into the YAML) or `doctor` to spot drift before deploying.

## Adding credentials

For the actual flow — writing secrets into `.env.<env>`, the helper POSTing to n8n or listing existing credentials, capturing `id`/`name` into `<env>.yml` — see [`skills/manage-credentials.md`](../manage-credentials.md).

## Per-service quirks

Per-service `type`-string and field-shape quirks live in `skills/integrations/<service>/...md`.
