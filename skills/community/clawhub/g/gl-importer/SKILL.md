---
name: gl-importer
description: Import CSV/XLSX accounting data into QuickBooks Online or Xero via the Synder Importer REST API. Use when asked to import invoices, bills, journal entries, customers, vendors, or any accounting data from spreadsheets/CSV files into QBO or Xero. Handles field mapping, file upload, import execution, status polling, and result retrieval. Supports smart auto-mapping for quick imports. NOT for reading/exporting data from QBO/Xero — this is import-only.
requirements:
  apiKeys:
    - name: IMPORTER_API_TOKEN
      description: Bearer token for the Synder Importer API. Generate at importer.synder.com → Account → API Keys.
      required: true
---

# Synder Importer API

Import CSV/XLSX files into QuickBooks Online or Xero.

## Setup

### Getting an API Token

If the user doesn't have a token yet, guide them through these steps:

1. **Create an account** at [importer.synder.com](https://importer.synder.com) and confirm your email
2. **Connect your accounting software** — in the web UI, link QuickBooks Online or Xero via OAuth
3. **Generate an API key** — go to **Account → API Keys**, click **Generate**. Copy the token immediately — it's shown only once

```bash
export IMPORTER_API_TOKEN="your_token_here"
export BASE="https://importer.synder.com/api/v1"
```

> **Trial users**: Imports are limited by row count without a paid subscription. No subscription is required to use the API itself.

## Data Privacy

- **Homepage**: [importer.synder.com](https://importer.synder.com) | **Docs**: [importer.synder.com/apidocs](https://importer.synder.com/apidocs)
- **Operator**: Synder Technologies Inc. — [synder.com](https://synder.com)
- **What's sent**: CSV/XLSX files containing accounting data (invoices, bills, journal entries, etc.) are uploaded to importer.synder.com and forwarded to your connected accounting provider (QuickBooks Online or Xero)
- **Retention**: Uploaded files are stored for import processing only and are not retained after import completion. Import logs (row counts, status, error messages) are retained for your account history.
- **Scope**: API tokens are scoped to a single user account and its connected companies. Tokens can be revoked at any time from the web UI.
- **Recommendation**: Always use `dryRun=true` first to preview before importing live data. Use non-production data for initial testing.

## Quick Reference

| Action | Method | Endpoint |
|--------|--------|----------|
| Account info | GET | /account |
| List companies | GET | /companies |
| Company settings | GET/POST | /companies/{id}/settings |
| List entities | GET | /companies/{id}/entities |
| Entity fields | GET | /companies/{id}/entities/{name}/fields |
| Create mapping | POST | /companies/{id}/mappings |
| List mappings | GET | /companies/{id}/mappings |
| Update mapping | PUT | /companies/{id}/mappings/{mid} |
| Delete mapping | DELETE | /companies/{id}/mappings/{mid} |
| Execute import | POST | /companies/{id}/imports |
| Auto-import | POST | /companies/{id}/imports/auto |
| List imports | GET | /companies/{id}/imports |
| Import status | GET | /companies/{id}/imports/{iid} |
| Cancel import | POST | /companies/{id}/imports/{iid}/cancel |
| Revert import | POST | /companies/{id}/imports/{iid}/revert |
| Import results | GET | /companies/{id}/imports/{iid}/results |

## Core Workflow

### 1. Find the company

```bash
curl "$BASE/companies" -H "Authorization: Bearer $IMPORTER_API_TOKEN"
```

Response is an array. Pick the company with `status: "ACTIVE"`. Save its `id`.

### 2. Choose entity and check fields

Common entities: `Invoice`, `Bill`, `JournalEntry`, `Customer`, `Vendor`, `Expense`, `SalesReceipt`, `Payment`, `CreditMemo`

```bash
curl "$BASE/companies/$CID/entities/$ENTITY/fields" -H "Authorization: Bearer $IMPORTER_API_TOKEN"
```

Fields with `isRequired: true` MUST be mapped. Fields with `isForGrouping: true` (e.g., DocNumber) combine multiple CSV rows into one entity (multi-line invoices).

> **Important**: Check `GET /companies/{id}/settings` for `dateFormat` (e.g., `MM/dd/yyyy`). CSV date columns must match this format or the import will fail. Update with `POST /companies/{id}/settings` if needed.

### 3. Option A: Smart Auto-Import (recommended)

Skip manual mapping — auto-match CSV headers to fields:

```bash
curl -X POST "$BASE/companies/$CID/imports/auto" \
  -H "Authorization: Bearer $IMPORTER_API_TOKEN" \
  -F "file=@data.csv" \
  -F "entityName=Invoice" \
  -F "dryRun=true"
```

- `dryRun=true` (default): Returns proposed mapping without importing. Check `missingRequired` array — if empty, safe to import. Response: `proposedFields`, `missingRequired`, `totalFieldsMapped`.
- `dryRun=false`: Maps AND imports in one call. Returns `{"id": "42", "status": "SCHEDULED", "mappingId": "33", ...}` — use the `id` to poll for completion (same as step 5).

**Confidence levels** in `proposedFields`: `high` = exact title match, `medium` = matched via alternative title. Review `medium` matches before importing with `dryRun=false`.

### 3. Option B: Manual Mapping

Create a mapping linking CSV columns to entity fields:

```bash
curl -X POST "$BASE/companies/$CID/mappings" \
  -H "Authorization: Bearer $IMPORTER_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Invoice Mapping",
    "entityName": "Invoice",
    "fields": [
      {"sourceFieldTitle": "Invoice #", "targetFieldId": "231"},
      {"sourceFieldTitle": "Customer",  "targetFieldId": "176"},
      {"sourceFieldTitle": null, "targetFieldId": "234", "fixedValue": "Imported via API"}
    ]
  }'
```

- `sourceFieldTitle`: CSV column header name
- `targetFieldId`: from the fields endpoint
- `fixedValue`: constant value for every row (set `sourceFieldTitle` to null)

### 4. Upload and Execute Import

```bash
curl -X POST "$BASE/companies/$CID/imports" \
  -H "Authorization: Bearer $IMPORTER_API_TOKEN" \
  -H "Idempotency-Key: $(uuidgen)" \
  -F "file=@data.csv" \
  -F "mappingId=$MAPPING_ID"
```

Returns `202` with `status: "SCHEDULED"`. **Always send Idempotency-Key** to prevent duplicate imports on retry.

### 5. Poll for Completion

```bash
curl "$BASE/companies/$CID/imports/$IMPORT_ID" -H "Authorization: Bearer $IMPORTER_API_TOKEN"
```

Terminal statuses: `FINISHED`, `FINISHED_WITH_WARNINGS`, `FAILED`, `CANCELED`.

Poll with exponential backoff: start 2s, multiply 1.5x, cap 30s.

### 6. Check Results

```bash
# All results
curl "$BASE/companies/$CID/imports/$IMPORT_ID/results" -H "Authorization: Bearer $IMPORTER_API_TOKEN"

# Errors only
curl "$BASE/companies/$CID/imports/$IMPORT_ID/results?type=ERROR" -H "Authorization: Bearer $IMPORTER_API_TOKEN"
```

Result types: `INFO` (success), `WARNING`, `ERROR`.

## File Requirements

- **CSV**: UTF-8, comma-delimited, header row required, max 50MB
- **XLSX**: First sheet by default (use `sheetName` param for others), header row required, max 50MB

## Error Handling

All errors return `{"error": {"code": "...", "message": "..."}}`.

| Code | HTTP | Action |
|------|------|--------|
| UNAUTHORIZED | 401 | Check/refresh API token |
| NOT_FOUND | 404 | Verify company/mapping/import/entity ID |
| BAD_REQUEST | 400 | Check request format, file validity, provider connection |
| VALIDATION_ERROR | 422 | Map all required fields — call GET .../fields to see which |
| DUPLICATE_REQUEST | 409 | Same Idempotency-Key reused within 24h — use new UUID |
| CONFLICT | 409 | Import not in valid state for cancel/revert |
| RATE_LIMITED | 429 | Wait `Retry-After` header seconds, then retry |

## Rate Limits

- **Standard**: 60 requests/minute per account
- **Imports**: 30 imports/hour per company

Check `X-RateLimit-Remaining` header. On 429, wait `Retry-After` seconds.

## Tips

- Use `dryRun=true` on auto-import before committing — all operations hit live accounting data
- Revert mistakes with `POST .../imports/{id}/revert` (deletes created entities from QBO/Xero)
- `alternativeTitles` on fields show what CSV headers auto-mapping recognizes
- For multi-line entities (invoices with line items), use a grouping field (DocNumber) — rows with same value become one entity
- Paginated endpoints accept `page` and `perPage` (max 100, default 20)

## Full API Details

For complete field schemas, response examples, and OpenAPI spec: see [references/api.md](references/api.md)
