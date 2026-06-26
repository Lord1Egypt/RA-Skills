---
name: integration-airtable
description: Airtable nodes — PAT credential, base / table IDs.
user-invocable: false
---

# Airtable

## Node type

`n8n-nodes-base.airtable`.

## Credential type

`airtableTokenApi` — Personal Access Token (PAT) from `airtable.com/create/tokens`.

For setup, see [`skills/manage-credentials.md`](../../manage-credentials.md). Scopes minimum: `data.records:read` and (if writing) `data.records:write`. Each token can be limited to specific bases — granular tokens are best practice.

## Base + table IDs

Airtable URLs: `https://airtable.com/<baseId>/<tableId>/<viewId>`. The n8n Airtable node takes `base` (= `baseId`) and `table` (= `tableId` or table name).

Store in env YAML:

```yaml
airtable:
  ordersBase: "appabc..."
  ordersTable: "tblxyz..."
```

## Field-name vs field-id

Records returned by the API use field NAMES by default. The Airtable node also supports `returnFieldsByFieldId: true` if your field names change frequently — this returns IDs instead and is more stable.
