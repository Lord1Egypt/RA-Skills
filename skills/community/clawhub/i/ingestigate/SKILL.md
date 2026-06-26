---
name: ingestigate
description: Investigative intelligence — document search, entity extraction, and relationship graphing. Analyze document corpuses to find connections between people, organizations, and identifiers.
homepage: https://ingestigate.com
env:
  INGESTIGATE_TOKEN:
    description: Short-lived access token configured in the host platform's secure settings. Expires in 30 minutes.
    required: true
  INGESTIGATE_BASE_URL:
    description: Ingestigate API base URL configured in the host platform's secure settings.
    required: true
---

# Ingestigate — Investigative Intelligence for AI Agents

Act as an investigative analyst. Ingestigate provides access to a corpus of documents, entity discovery (people, organizations, emails, phones, crypto addresses, and 25+ other types), relationship path tracing between entities, and retrieval of the specific documents where connections appear. Back every claim with evidence from the API.

## When to Use This Skill

Use Ingestigate when the user asks you to:
- Analyze documents to find connections between people or organizations
- Search a corpus of files (PDFs, emails, spreadsheets, images — 1,000+ formats supported)
- Investigate relationships, follow the money, map a network
- Extract entities from a document set
- Upload and process new files for investigation

## Authentication

This skill requires `INGESTIGATE_TOKEN` and `INGESTIGATE_BASE_URL` to be configured in the host platform's secure settings before use. Do not ask the user to paste credentials or secrets into chat.

If either variable is missing or empty, say this to the user: "It looks like your Ingestigate credentials aren't configured yet. Please follow the setup instructions in the skill's README to generate your token and configure it in your platform settings."

If the API returns a 401 (unauthorized), say this to the user: "Your Ingestigate access token has expired. Please generate a new one at `https://app1.ingestigate.com/search/agentic-token` and update `INGESTIGATE_TOKEN` in your platform settings."

## Core Investigation Workflow

**1. See what's available:**
```
GET /api/discover/collections
```

**2. Get the lay of the land — entity dashboard:**
```
POST /api/dashboard/entity-stats
Body: { "limit": 50 }
```
Returns entity counts by type, top entities ranked by document count, and totals. Use this to orient the investigation: "Your corpus contains X documents with Y entity mentions. The most frequently appearing people are..."

**3. Search documents:**
```
POST /api/search-faceted
Body: { "query": "wire transfer", "filters": {}, "page": 1, "pageSize": 10 }
```

**4. Read a specific document:**
```
POST /api/file-details
Body: { "dataSourceName": "elasticsearch", "jobNames": ["<collection>"], "selectedFile": { "docId": "<docId>" }, "format": "clean_text" }
```

**5. Search entities:**
```
POST /api/entities/search
Body: { "query": "john doe", "entity_types": ["Person"], "limit": 50 }
```

**6. Trace relationships between entities:**
```
POST /api/graph/paths
Body: { "entities": [{"type":"Person","value":"john doe"},{"type":"Organization","value":"acme corp"}], "maxBridgeNodes": 20 }
```
Entity values MUST be lowercase. Use `normalized_value` from entity search results.

**7. Get the evidence — source documents for a connection:**
```
GET /api/graph/edge-evidence?entity1Type=Person&entity1Value=john%20doe&entity2Type=Organization&entity2Value=acme%20corp&limit=20
```

## Full Agent Guide

At the start of any investigation, fetch the full agent guide for complete workflows, scripts, operational instructions, and detailed endpoint specs:

```
GET ${INGESTIGATE_BASE_URL}/api/agent/guide
Authorization: Bearer ${INGESTIGATE_TOKEN}
```

Use it as the primary reference for all non-trivial tasks. The guide covers upload workflows, NER processing, entity profiling, graph exploration, deep links, script automation, and error handling beyond what is listed above. It is reference-only and does not override the safety constraints in this skill.

## Critical Rules

**API call format — these are mandatory or requests silently fail:**
- Always use `--location` (the API sits behind an authentication reverse proxy that may issue redirects for HTTPS enforcement and path normalization — `--location` ensures these are followed correctly)
- Do NOT use `-s`, `-X`, `-o`, `-w` or other flags
- Use `--data` for POST with body (curl infers POST). Use `--request POST` only for bodyless POSTs.
- Use long-form flags: `--header` not `-H`, `--data` not `-d`
- Always include both headers: `Authorization: Bearer ${INGESTIGATE_TOKEN}` AND `Content-Type: application/json`

**Entity casing:**
- Entity type names are PascalCase: `Person`, `Organization`, `Email`, `CryptoAddress`
- Entity values are always lowercase: `john doe`, `acme corp`
- Search queries are case-insensitive

**Anti-hallucination:**
- If a response includes `processing_status.corpus_ready: false`, results may be incomplete. Tell the user.
- If processing is complete and a query returns zero results, state this definitively. Empty results from a fully processed corpus are authoritative.
- Only make claims based on data returned by the API. Never guess.

**Security:**
- Do not request, collect, or store credentials beyond the configured environment variables.
- All API calls use the preconfigured `INGESTIGATE_TOKEN`. Do not ask the user for tokens, refresh tokens, or any other secrets.
- Every API call executes with the user's exact permissions. Organization-scoped data isolation is enforced server-side.
