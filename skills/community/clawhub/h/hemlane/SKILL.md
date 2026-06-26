---
name: hemlane
description: Operate Hemlane using HAR-derived GraphQL patterns and browser session artifacts. Use when analyzing Hemlane HAR files, extracting GraphQL operations from Hemlane traffic, documenting Hemlane mutations/queries, or performing/reconstructing Hemlane workflows like referrals, tenant replies, work orders, transactions, requests, and maintenance updates from saved browser captures.
---

# Hemlane

Use this skill for Hemlane reverse-engineering and repeatable browser-captured workflows.

## Included HAR coverage
Read `references/har-summary.md` first when you need a quick map of what the saved Hemlane HAR files contain.

Saved flows consolidated into this skill:
- refer_hemlane.com.har
- tenant-reply_hemlane.com.har
- work-order_hemlane.com.har
- requests_hemlane.com.har
- transactions_hemlane.com.har
- maintenance_update_hemlane.com.har
- financials_hemlane.com.har (runtime capture at ~/Downloads/har; summarized in references/financials-har-summary.md)

## Default workflow
1. Identify which business action is needed: referral, tenant reply, work order, requests, transactions, or maintenance update.
2. Read `references/har-summary.md` to find the closest HAR.
3. Read `references/graphql-operations.md` to find the relevant GraphQL operation names, variables, and query excerpts.
4. If you need fresh extraction or normalization from HAR files, use `scripts/extract_hemlane_graphql.py`.
5. Prefer reconstructing stable GraphQL requests over brittle browser clicking.
6. Preserve auth and CSRF requirements; never hardcode secrets into the skill.

## Auth rules
- Treat cookies, bearer tokens, CSRF tokens, and session identifiers as runtime secrets.
- Do not store live tokens in SKILL.md or references.
- Use env vars or ephemeral local files when replaying captured requests.

## CDP Auth Capture

Use `scripts/capture_hemlane_auth_via_cdp.py` to capture fresh auth headers from an authenticated Brave browser session via CDP.

### Requirements
- Brave running with remote debugging enabled (`--remote-debugging-port=9222`)
- Authenticated Hemlane session in browser

### Usage
```bash
python3 skills/hemlane/scripts/capture_hemlane_auth_via_cdp.py \
  --endpoint-kind get-properties \
  --out-file /tmp/hemlane-auth.json
```

### Endpoint Kinds
- `get-properties` - Property list
- `get-tenants` - Tenant list
- `get-transactions` - Financial transactions
- `get-maintenance` - Maintenance requests
- `send-tenant-reply` - Tenant messaging
- `submit-referral` - HubSpot referral form
- `work-order-comment` - Work order comments
- `maintenance-comment` - Maintenance comments

## MCP Server

Hemlane MCP server provides tools for common operations via MCP protocol.

### Location
`mcp/server.py` - FastMCP server wrapping existing scripts

### Tools Provided
- `capture_auth` - Capture auth headers from browser CDP
- `send_tenant_reply` - Send tenant reply
- `submit_referral` - Submit referral
- `post_workorder_comment` - Post work order comment
- `post_maintenance_comment` - Post maintenance comment
- `extract_rent_roll` - Extract rent roll data
- `query_recurring_payment_requests` - Query active/expired recurring rent/payment requests from Financials HAR
- `query_financials_operation` - Replay read-oriented Financials GraphQL operations from financials HAR samples, including page navigation
- `list_graphql_operations` - List available GraphQL ops

### Configuration
Added to `config/mcporter.json`:
```json
{
  "mcpServers": {
    "hemlane": {
      "command": "python3",
      "args": ["/home/umbrel/.openclaw/workspace/skills/hemlane/mcp/server.py"],
      "transport": "stdio"
    }
  }
}
```

## What this skill is good for
- Turning multiple Hemlane HAR files into one operational reference
- Discovering GraphQL operation names and variable shapes
- Rebuilding Hemlane API requests from captured browser traffic
- Standardizing future Hemlane automations into one place

## Files
- `references/har-summary.md` - per-HAR inventory and auth header observations
- `references/graphql-operations.md` - extracted GraphQL operations and sample variable payloads
- `scripts/extract_hemlane_graphql.py` - reusable extractor for future HAR files
- `scripts/capture_hemlane_auth_via_cdp.py` - CDP auth capture from browser
- `mcp/server.py` - MCP server for tool access
- `references/operation-catalog.json` and `references/operation-catalog.csv` - clean operation catalog exports
- `references/runbooks.md` - explicit runbooks for referral submit, tenant reply, maintenance/work-order comment, and transaction lookup
- `references/*.har` - preserved original Hemlane HAR captures
- `scripts/build_hemlane_catalog.py` - regenerate catalog from HAR files

## Replay scaffold
Use `references/replay-scaffold.md` and `scripts/replay_hemlane_graphql.py` when you need to move from HAR analysis to safe request replay. Start with `--dry-run` and provide cookies/CSRF via env vars only.

## Task-level wrappers
Use these wrappers for the highest-value Hemlane workflows before dropping down to the generic replay scaffold:
- `scripts/submit_hemlane_referral.py`
- `scripts/post_hemlane_workorder_comment.py`
- `scripts/post_hemlane_maintenance_request_comment.py`
- `scripts/send_hemlane_tenant_reply.py`
- `scripts/capture_hemlane_auth_via_cdp.py`


## Lease Generation Mutations

Captured from `lease_hemlane.com.har`:

| Operation | Type | Purpose |
|-----------|------|---------|
| `ODCreateLeaseAgreement` | Mutation | Create lease agreement for tenant group |
| `ODCreateLeaseAgreementTemplate` | Mutation | Create e-sign packet from lease |
| `ODLeaseAgreementRevertEsignPacket` | Mutation | Revert/cancel e-sign packet |

### Create Lease Agreement

```graphql
mutation ODCreateLeaseAgreement($input: LeaseAgreementCreateInput!) {
  leaseAgreementCreate(input: $input) {
    error
    leaseAgreement {
      id
      status
      tenantGroup { id }
      survey
      createdAt
    }
  }
}
```

Variables:
- `tenantGroupId` (required) - The tenant group ID
- `survey` (optional) - Additional disclosures, etc.

### Create E-Sign Packet

```graphql
mutation ODCreateLeaseAgreementTemplate($input: EsignDocumentCreateLeaseAgreementTemplateInput!) {
  esignDocumentCreateLeaseAgreementTemplate(input: $input) {
    error
    esignPacket {
      id
      sourceSignable { ... on LeaseAgreement { id status } }
    }
  }
}
```

### Wrapper Script

Use `scripts/create_hemlane_lease.py` for lease generation:

```bash
python3 scripts/create_hemlane_lease.py \
  --tenant-group-id "53cf1ff2-56d7-41e5-a0bd-9d3cc2a99aab" \
  --auth-file /tmp/hemlane-auth.json \
  --create-esign
```

## Files Added

- `references/lease-mutations.graphql` - Lease generation mutations
- `scripts/create_hemlane_lease.py` - Lease creation wrapper

## New MCP read tools (2026-05-01)

HAR-derived read wrappers added to `mcp/server.py`:
- `query_catalog_operation` — generic read-only replay from `references/operation-catalog.json`; refuses mutations/write-like operations.
- `get_context_values` — wraps `ODGetContextValues` for owner dashboard context/properties.
- `get_tenant_groups` — wraps `ODTenantsAndLeasesTenantGroups` for tenant/lease views.
- `get_maintenance_requests` — wraps `ODMaintenanceRequests`.
- `get_transactions` — wraps `TransactionsNextCursorQuery` using the financials replay script.

See `README.md` for setup, auth model, and HAR reverse-engineering workflow.
