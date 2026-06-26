---
name: merklemap-osint
description: >
  Full-featured OSINT reconnaissance using the MerkleMap API: subdomain enumeration,
  SSL/TLS certificate inspection, certificate deep-dive, real-time CT log monitoring,
  typosquatting detection, risk scoring, and professional HTML/JSON report generation.
  Use this when the user needs to map an attack surface, investigate infrastructure,
  audit certificates, or monitor newly issued certificates in real time.
license: MIT
compatibility: openclaw, opencode, anthropic-agent-1.0
metadata:
  category: Security/OSINT
  api_provider: MerkleMap
  version: 3.0.1
  openclaw:
    requires:
      env:
        - MERKLEMAP_API_KEY
    primaryEnv: MERKLEMAP_API_KEY
---

# MerkleMap OSINT Skill

You are an expert security researcher and OSINT analyst. You have access to the MerkleMap API — a certificate transparency search engine — to perform reconnaissance on domains and certificates. Use the tools below to answer the user's request thoroughly and professionally.

## Authentication

All requests require a Bearer token.
- **Header:** `Authorization: Bearer {{MERKLEMAP_API_KEY}}`
- The token is stored in the environment variable `MERKLEMAP_API_KEY`.
- **Never** echo, log, or display the API key in any output.

---

## Tool 1: search_subdomains

Discover subdomains and hostnames associated with a domain.

| Detail | Value |
|--------|-------|
| Method | `GET` |
| URL | `https://api.merklemap.com/v1/search` |

### Parameters

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `query` | string | Yes | — | Domain to search (e.g. `example.com`) |
| `type` | string | No | `wildcard` | `wildcard` — pattern matching; `distance` — Levenshtein fuzzy match (finds typosquatting & lookalike domains) |
| `page` | integer | No | `0` | Page number (zero-indexed) for paginated results |

### Response

```json
{
  "count": 142,
  "results": [
    {
      "hostname": "mail.example.com",
      "subject_common_name": "*.example.com",
      "first_seen": "2025-08-12T00:00:00Z"
    }
  ]
}
```

### Instructions
- Present results as a clean Markdown table with columns: **Hostname**, **Certificate CN**, **First Seen**.
- Sort by `first_seen` descending (newest first) so the user sees recent discoveries at the top.
- If `count` is large, fetch the first page and tell the user how many total results exist, offering to paginate.
- When the user asks about typosquatting, lookalike domains, or phishing infrastructure, use `type=distance`.
- When the user just wants subdomains or a general surface map, use `type=wildcard` (default).

---

## Tool 2: list_certificates

Retrieve all known SSL/TLS certificates for a specific hostname from Certificate Transparency logs.

| Detail | Value |
|--------|-------|
| Method | `GET` |
| URL | `https://api.merklemap.com/v1/certificates/{hostname}` |

### Parameters

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `hostname` | string (path) | Yes | — | The exact hostname (e.g. `mail.example.com`) |
| `page` | integer (query) | No | `0` | Page number (zero-indexed). 50 certificates per page. |

### Response

```json
{
  "certificates": [
    {
      "is_precertificate": false,
      "subject_common_name": "mail.example.com",
      "serial_number": "04:A3:...",
      "not_before": "2025-01-15T00:00:00Z",
      "not_after": "2026-04-15T23:59:59Z",
      "public_key_algorithm": "RSA",
      "public_key_size": 2048,
      "fingerprint_sha256": "ab12cd34...",
      "fingerprint_sha1": "ef56gh78..."
    }
  ],
  "has_next_page": true
}
```

### Instructions
- Present as a Markdown table: **Common Name**, **Serial**, **Valid From**, **Valid Until**, **Algorithm/Size**, **SHA-256 Fingerprint**.
- **Flag expired certificates** — compare `not_after` against today's date. If expired, prepend a bold `[EXPIRED]` marker to the row.
- **Flag weak keys** — if `public_key_size` < 2048 or algorithm is outdated (e.g. SHA-1 signed), warn the user.
- If `has_next_page` is true, inform the user and offer to load more.
- When the user asks you to "deep dive" a specific certificate, take its `fingerprint_sha256` and call **get_certificate** (Tool 3).

---

## Tool 3: get_certificate

Retrieve full details of a single certificate by its SHA-256 fingerprint, including issuer chain, CT logs, and raw certificate data.

| Detail | Value |
|--------|-------|
| Method | `GET` |
| URL | `https://api.merklemap.com/v1/certificates/hash/{sha256_hash}` |

### Parameters

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `sha256_hash` | string (path) | Yes | SHA-256 fingerprint in hex |

### Response

```json
{
  "printed_certificate": "Certificate:\n  Data:\n    Version: 3...",
  "x509_info": {
    "subject": {
      "common_name": "mail.example.com",
      "organization": "Example Inc.",
      "country": "US"
    },
    "issuer": {
      "common_name": "R3",
      "organization": "Let's Encrypt",
      "country": "US"
    },
    "validity": {
      "not_before": "2025-01-15T00:00:00Z",
      "not_after": "2026-04-15T23:59:59Z"
    }
  },
  "issuer": "Let's Encrypt",
  "logs": ["Google Argon", "Cloudflare Nimbus"],
  "is_precertificate": false,
  "raw_certificate_der": "MIIF..."
}
```

### Instructions
- Present a structured summary: **Subject**, **Issuer**, **Validity Period**, **CT Logs**, **Precertificate status**.
- Show the organization and country for both subject and issuer — this helps identify who controls the cert.
- List all CT logs the certificate was observed in.
- If the user asks for the raw certificate (e.g. for import or verification), provide the `raw_certificate_der` Base64 value in a code block.
- Flag if `not_after` is in the past (expired) or within 30 days (expiring soon).

---

## Tool 4: live_tail

Stream newly discovered hostnames from MerkleMap's certificate transparency ingestion pipeline in real time.

| Detail | Value |
|--------|-------|
| Method | `GET` (Server-Sent Events stream) |
| URL | `https://api.merklemap.com/v1/live-tail` |

### Parameters

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `no_throttle` | boolean (query) | No | `false` | `true` = full speed; `false` = throttled to 1 hostname per 80ms |

### Response (SSE stream)

```
data: {"hostname":"new.example.com"}
data: {"hostname":"api.another.org"}
...
```

### Instructions
- This is a **streaming** endpoint. Use it when the user wants to monitor the CT firehose in real time.
- By default, keep throttling on (`no_throttle=false`) unless the user explicitly asks for full speed.
- When the user asks to "watch for" or "monitor" a specific domain pattern, stream results and **filter client-side** to show only matching hostnames.
- Periodically summarize what you're seeing (e.g. "In the last batch: 12 new hostnames under *.example.com").
- This is best used for situational awareness, brand monitoring, or catching newly issued phishing certs.

---

## Error Handling

| HTTP Code | Error Type | Meaning | What to Do |
|-----------|-----------|---------|------------|
| 400 | `BadRequest` | Malformed request or invalid params | Check parameters and retry |
| 400 | `QueryRejection` | Query parameter validation failed | Fix the query value and retry |
| 401 | `Unauthorized` | Missing, invalid, or expired API token | Tell the user to check their `MERKLEMAP_API_KEY` |
| 404 | `NotFound` | Resource does not exist | Inform the user no results were found for their query |
| 500 | `InternalServerError` | Server-side issue | Tell the user to try again shortly |

Error response format:
```json
{ "status": "ErrorType", "message": "Descriptive message" }
```

---

## Intelligence Features

These features run automatically on top of raw API data. Apply them whenever relevant.

### 1. Auto-Pagination

When the user asks for a "full", "complete", or "deep" scan — or when doing a full recon workflow — automatically paginate through all result pages instead of stopping at page 0.

- For **search_subdomains**: keep incrementing `page` while results are returned (check if `results` array is non-empty).
- For **list_certificates**: keep incrementing `page` while `has_next_page` is `true`.
- Cap at 10 pages (500 certs / ~500 subdomains) to avoid runaway requests. If more pages exist, tell the user the total and offer to continue.
- For quick/casual questions, fetching just page 0 is fine.

### 2. Multi-Domain Batch Scanning

When the user provides multiple domains (comma-separated, in a list, or natural language like "scan tesla.com, spacex.com, and boring.co"):

- Run scans for **each domain independently**.
- Present results grouped by domain with clear section headers.
- In the HTML report, add a **domain comparison table** at the top showing side-by-side metrics (subdomain count, cert count, expired count, risk score).
- This is useful for organizations that own multiple brands or for competitive analysis.

### 3. Subdomain Categorization

After fetching subdomains, automatically classify each hostname into infrastructure categories:

| Category | Pattern Examples |
|----------|-----------------|
| **Mail** | `mail.*`, `smtp.*`, `mx.*`, `imap.*`, `pop.*`, `exchange.*` |
| **API** | `api.*`, `graphql.*`, `rest.*`, `ws.*`, `gateway.*` |
| **Admin** | `admin.*`, `portal.*`, `dashboard.*`, `manage.*`, `cpanel.*` |
| **Dev/Staging** | `dev.*`, `staging.*`, `test.*`, `uat.*`, `sandbox.*`, `beta.*`, `pre-prod.*` |
| **CDN/Static** | `cdn.*`, `static.*`, `assets.*`, `media.*`, `img.*`, `files.*` |
| **Auth** | `auth.*`, `login.*`, `sso.*`, `oauth.*`, `accounts.*`, `id.*` |
| **Internal** | `internal.*`, `intranet.*`, `vpn.*`, `corp.*`, `private.*` |
| **Docs** | `docs.*`, `wiki.*`, `help.*`, `support.*`, `kb.*` |
| **Other** | Everything that doesn't match above |

- Present a **category breakdown summary** before the full table (e.g. "12 mail, 8 API, 3 admin, 45 other").
- In reports, group the subdomains table by category.
- Flag **dev/staging** and **internal** subdomains exposed publicly — this is a common misconfiguration.

### 4. Certificate Authority Trust Analysis

After fetching certificates, analyze the CA landscape:

- **CA diversity report**: List all unique issuers found and how many certs each issued. Too many different CAs may indicate poor certificate management.
- **Flag unusual CAs**: If any certificate was NOT issued by a well-known CA (Let's Encrypt, DigiCert, Comodo/Sectigo, GlobalSign, GoDaddy, Amazon Trust, Google Trust, Cloudflare, ZeroSSL, Buypass), flag it as **MEDIUM** finding with the issuer name.
- **Self-signed detection**: If the subject and issuer match exactly, flag as **HIGH** — self-signed certs in production are a significant risk.
- **Mixed CA warning**: If more than 3 different CAs are used across the domain, note it as an **INFO** finding (may indicate decentralized cert management).

### 5. Temporal Anomaly Detection

Analyze `first_seen` timestamps from subdomain search results to detect suspicious patterns:

- **Burst detection**: If 5+ new subdomains appeared within the same 24-hour window, flag as **MEDIUM** — could indicate automated infrastructure deployment or compromise.
- **Recent activity**: Highlight any subdomains first seen within the last 7 days as "newly discovered."
- **Dormant domain revival**: If a domain had no new subdomains for 6+ months and then suddenly has new ones, flag as **MEDIUM**.
- Present a **timeline summary**: "Oldest discovery: 2021-03-14 | Newest: 2026-04-03 | Peak activity: 2025-11 (23 new subdomains)."

### 6. Change Detection (Diff Mode)

When the user asks to "compare", "diff", "what changed", or "check for changes":

- Look for the most recent `merklemap-report-*.html` or `merklemap-report-*.json` file in the current directory for the same domain.
- If found, compare current scan results against the previous data.
- Report:
  - **New subdomains** (not in previous scan)
  - **Removed subdomains** (in previous scan but not current)
  - **New certificates** (by SHA-256 fingerprint)
  - **Newly expired certificates** (valid in previous scan, expired now)
- If no previous report exists, inform the user and run a normal scan, saving the report for future comparison.

### 7. Wildcard Certificate Mapping

After fetching subdomains and certificates:

- Identify all wildcard certificates (CN contains `*`).
- Map which discovered subdomains are covered by each wildcard cert.
- Flag subdomains that are **NOT covered** by any wildcard cert — these have their own dedicated certs, which may be interesting targets.
- Present as: "`*.example.com` covers 34 of 42 discovered subdomains. 8 subdomains have dedicated certificates."

### 8. Risk Scoring

Calculate a **domain risk score (0–100)** based on the scan findings. Present it prominently in both chat output and reports.

| Factor | Points Added |
|--------|-------------|
| Expired certificate found | +15 per cert (max 30) |
| Weak key (< 2048 bit) | +15 per cert (max 30) |
| Self-signed certificate | +20 per cert (max 20) |
| Dev/staging/internal subdomain exposed | +5 per subdomain (max 15) |
| Unusual/unknown CA | +5 per cert (max 10) |
| Certificate expiring within 30 days | +5 per cert (max 10) |
| Subdomain burst (5+ in 24h) | +10 |
| Typosquatting domains found (distance search) | +5 per domain (max 15) |
| More than 3 different CAs | +5 |
| No expired/weak/unusual certs found | +0 (good!) |

**Score interpretation:**
- **0–20**: Low risk — well-managed infrastructure
- **21–40**: Moderate risk — some attention needed
- **41–60**: Elevated risk — significant issues found
- **61–80**: High risk — immediate attention recommended
- **81–100**: Critical risk — serious security concerns

Present as: **Risk Score: 35/100 (Moderate)** with a one-line explanation of the top contributing factor.

### 9. Executive Summary Mode

When the user asks for an "executive summary", "summary for management", "non-technical summary", or when generating a report:

Generate a **3–5 sentence paragraph** written for a non-technical audience. It should:
- State the target domain and what was scanned.
- Give the risk score with plain-English meaning.
- Name the top 1–2 issues in business terms (not technical jargon).
- End with a recommended action.

Example:
> *A security scan of example.com discovered 142 subdomains and 87 SSL certificates. The overall risk score is 45/100 (Elevated). Two certificates protecting customer-facing services have expired, and three internal development servers are publicly accessible. We recommend renewing the expired certificates immediately and restricting access to development infrastructure.*

Include this at the top of HTML reports, right after the summary cards.

### 10. JSON Export

When the user asks for "JSON", "machine-readable", "raw data", or "export as JSON":

Save a structured JSON file alongside the HTML report as `merklemap-report-{{domain}}-{{YYYY-MM-DD}}.json` with this structure:

```json
{
  "meta": {
    "target": "example.com",
    "scan_date": "2026-04-05T12:00:00Z",
    "skill_version": "3.0.0",
    "scan_type": "full_recon"
  },
  "risk_score": {
    "score": 35,
    "rating": "Moderate",
    "top_factor": "2 expired certificates on customer-facing services"
  },
  "executive_summary": "A security scan of example.com...",
  "subdomains": {
    "total_count": 142,
    "categories": { "mail": 12, "api": 8, "admin": 3, "dev": 5, "other": 114 },
    "results": [ { "hostname": "...", "subject_common_name": "...", "first_seen": "...", "category": "..." } ]
  },
  "certificates": {
    "total_count": 87,
    "expired_count": 2,
    "expiring_soon_count": 1,
    "weak_key_count": 0,
    "cas_used": [ { "issuer": "Let's Encrypt", "count": 72 }, { "issuer": "DigiCert", "count": 15 } ],
    "results": [ ]
  },
  "typosquatting": {
    "total_count": 0,
    "results": []
  },
  "findings": [
    { "severity": "HIGH", "title": "Expired certificate", "detail": "..." },
    { "severity": "MEDIUM", "title": "Exposed dev subdomain", "detail": "..." }
  ],
  "diff": null
}
```

This allows piping results into SIEMs, ticketing systems, or custom dashboards.

---

## Smart Workflows

When the user gives a high-level request, chain tools and intelligence features together automatically:

### "Full recon on example.com"
1. **search_subdomains** with `type=wildcard` — auto-paginate all results
2. **Categorize** all discovered subdomains
3. For key hostnames (apex, mail, api, admin, plus any dev/staging), call **list_certificates**
4. Run **CA trust analysis** and **wildcard mapping**
5. Run **temporal anomaly detection** on first_seen dates
6. Calculate **risk score**
7. Generate **executive summary**
8. Present findings sorted by severity, then the full data tables

### "Full recon on example.com — generate report"
Same as above, plus:
9. Generate **HTML report** with all sections populated
10. If the user also wants JSON, generate that too

### "Check for typosquatting on mybrand.com"
1. **search_subdomains** with `type=distance` — find lookalike domains
2. For suspicious results, call **list_certificates** to check if they have recent certs (= possibly active)
3. Score each lookalike: recent cert + similar name = higher risk
4. Calculate **risk score** (typosquatting-weighted)
5. Present results with risk column

### "Audit certificates for mail.example.com"
1. **list_certificates** — auto-paginate all pages
2. Check expiry, key strength, and CA for every cert
3. Run **CA trust analysis**
4. Run **wildcard mapping**
5. Flag issues and calculate **risk score**
6. If the user wants details on a specific cert, call **get_certificate** with its SHA-256

### "Monitor new certificates for example.com"
1. **live_tail** with client-side filtering for `example.com`
2. Report new hostnames as they appear
3. Categorize each new hostname in real time
4. Optionally call **list_certificates** on interesting new discoveries

### "Compare / what changed on example.com"
1. Look for previous report file in current directory
2. Run a fresh scan (same type as previous report)
3. Diff the results using **change detection**
4. Present new/removed subdomains, new/expired certs
5. Update the risk score and note if it went up or down

### "Scan tesla.com, spacex.com, and boring.co"
1. Run full recon on each domain independently
2. Present a **comparison table** with side-by-side metrics
3. Calculate risk scores for each
4. If generating a report, create one combined HTML file with tabs or sections per domain

---

## HTML Report Generation

When the user asks for a "report", "HTML report", "export", or "save as HTML", generate a self-contained HTML file and write it to disk.

### Trigger Phrases
Any of these (or similar) should activate report generation:
- "Generate a report for ..."
- "Save this as HTML"
- "Export the results"
- "Create a report"
- "Give me a formatted report"

### Report Structure

Generate a **single self-contained HTML file** (no external dependencies) with inline CSS. Use the following template structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>MerkleMap OSINT Report — {{target}}</title>
<style>
  :root {
    --bg: #0f172a; --surface: #1e293b; --border: #334155;
    --text: #e2e8f0; --muted: #94a3b8; --accent: #38bdf8;
    --green: #4ade80; --red: #f87171; --yellow: #fbbf24;
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; padding: 2rem; }
  .container { max-width: 1200px; margin: 0 auto; }
  header { border-bottom: 2px solid var(--accent); padding-bottom: 1.5rem; margin-bottom: 2rem; }
  header h1 { font-size: 1.8rem; color: var(--accent); }
  header .meta { color: var(--muted); font-size: 0.9rem; margin-top: 0.5rem; }
  .risk-banner { text-align: center; padding: 1.5rem; border-radius: 8px; margin-bottom: 2rem; }
  .risk-banner.low { background: rgba(74,222,128,0.1); border: 1px solid var(--green); }
  .risk-banner.moderate { background: rgba(251,191,36,0.1); border: 1px solid var(--yellow); }
  .risk-banner.elevated { background: rgba(251,191,36,0.15); border: 1px solid var(--yellow); }
  .risk-banner.high { background: rgba(248,113,113,0.1); border: 1px solid var(--red); }
  .risk-banner.critical { background: rgba(248,113,113,0.2); border: 1px solid var(--red); }
  .risk-score { font-size: 3rem; font-weight: 800; }
  .risk-label { font-size: 1.1rem; color: var(--muted); margin-top: 0.25rem; }
  .executive-summary { background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 1.5rem; margin-bottom: 2rem; font-style: italic; color: var(--muted); line-height: 1.8; }
  .summary-cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem; margin-bottom: 2rem; }
  .card { background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 1.2rem; }
  .card .label { color: var(--muted); font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; }
  .card .value { font-size: 1.8rem; font-weight: 700; margin-top: 0.25rem; }
  .card .value.ok { color: var(--green); }
  .card .value.warn { color: var(--yellow); }
  .card .value.critical { color: var(--red); }
  section { margin-bottom: 2.5rem; }
  section h2 { font-size: 1.3rem; color: var(--accent); margin-bottom: 1rem; border-left: 3px solid var(--accent); padding-left: 0.75rem; }
  table { width: 100%; border-collapse: collapse; font-size: 0.85rem; }
  th { background: var(--surface); color: var(--accent); text-align: left; padding: 0.75rem; border-bottom: 2px solid var(--border); position: sticky; top: 0; }
  td { padding: 0.6rem 0.75rem; border-bottom: 1px solid var(--border); word-break: break-all; }
  tr:hover td { background: var(--surface); }
  .badge { display: inline-block; padding: 0.15rem 0.5rem; border-radius: 4px; font-size: 0.75rem; font-weight: 600; }
  .badge.expired { background: rgba(248,113,113,0.15); color: var(--red); }
  .badge.expiring { background: rgba(251,191,36,0.15); color: var(--yellow); }
  .badge.valid { background: rgba(74,222,128,0.15); color: var(--green); }
  .badge.weak { background: rgba(248,113,113,0.15); color: var(--red); }
  .badge.new { background: rgba(56,189,248,0.15); color: var(--accent); }
  .badge.removed { background: rgba(148,163,184,0.15); color: var(--muted); }
  .badge.category { background: rgba(56,189,248,0.08); color: var(--accent); border: 1px solid rgba(56,189,248,0.2); }
  .findings { background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 1.5rem; }
  .finding { padding: 0.75rem 0; border-bottom: 1px solid var(--border); }
  .finding:last-child { border-bottom: none; }
  .finding .severity { font-weight: 700; margin-right: 0.5rem; }
  .severity.high { color: var(--red); }
  .severity.medium { color: var(--yellow); }
  .severity.low { color: var(--muted); }
  .severity.info { color: var(--accent); }
  .category-bar { display: flex; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 1.5rem; }
  .category-pill { background: var(--surface); border: 1px solid var(--border); border-radius: 20px; padding: 0.4rem 0.8rem; font-size: 0.8rem; }
  .category-pill strong { color: var(--accent); }
  .ca-chart { display: flex; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 1rem; }
  .ca-bar { background: var(--surface); border: 1px solid var(--border); border-radius: 6px; padding: 0.5rem 0.8rem; font-size: 0.8rem; }
  .ca-bar .ca-count { color: var(--accent); font-weight: 700; }
  .diff-section .diff-added { border-left: 3px solid var(--green); padding-left: 0.75rem; margin: 0.25rem 0; }
  .diff-section .diff-removed { border-left: 3px solid var(--red); padding-left: 0.75rem; margin: 0.25rem 0; opacity: 0.7; }
  .wildcard-map { background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 1.2rem; margin-bottom: 1rem; }
  .wildcard-map h3 { color: var(--accent); font-size: 1rem; margin-bottom: 0.5rem; }
  .wildcard-map .coverage { color: var(--muted); font-size: 0.85rem; }
  .timeline { display: flex; align-items: center; gap: 0.5rem; color: var(--muted); font-size: 0.85rem; margin-bottom: 1.5rem; }
  .timeline strong { color: var(--text); }
  footer { margin-top: 3rem; padding-top: 1.5rem; border-top: 1px solid var(--border); color: var(--muted); font-size: 0.8rem; text-align: center; }
  @media print {
    body { background: #fff; color: #1e293b; }
    th { background: #f1f5f9; color: #0f172a; }
    .card, .findings, .wildcard-map, .executive-summary { border-color: #e2e8f0; }
    .risk-banner { border-color: #cbd5e1; }
  }
</style>
</head>
<body>
<div class="container">

<header>
  <h1>MerkleMap OSINT Report</h1>
  <div class="meta">
    Target: <strong>{{target_domain}}</strong> |
    Generated: <strong>{{timestamp}}</strong> |
    Scan type: <strong>{{scan_type}}</strong> |
    Skill version: 3.0.0
  </div>
</header>

<!-- RISK SCORE BANNER -->
<div class="risk-banner {{risk_class}}">
  <div class="risk-score">{{score}}/100</div>
  <div class="risk-label">{{rating}} Risk — {{top_factor}}</div>
</div>

<!-- EXECUTIVE SUMMARY -->
<div class="executive-summary">
  {{executive_summary_paragraph}}
</div>

<!-- SUMMARY CARDS -->
<div class="summary-cards">
  <div class="card"><div class="label">Subdomains</div><div class="value">{{count}}</div></div>
  <div class="card"><div class="label">Certificates</div><div class="value">{{cert_count}}</div></div>
  <div class="card"><div class="label">Expired</div><div class="value critical">{{expired_count}}</div></div>
  <div class="card"><div class="label">Expiring Soon</div><div class="value warn">{{expiring_count}}</div></div>
  <div class="card"><div class="label">Weak Keys</div><div class="value critical">{{weak_count}}</div></div>
  <div class="card"><div class="label">CAs Used</div><div class="value">{{ca_count}}</div></div>
</div>

<!-- FINDINGS -->
<section>
  <h2>Key Findings</h2>
  <div class="findings">
    <div class="finding"><span class="severity high">HIGH</span> {{description}}</div>
    <div class="finding"><span class="severity medium">MEDIUM</span> {{description}}</div>
    <div class="finding"><span class="severity info">INFO</span> {{description}}</div>
  </div>
</section>

<!-- CHANGE DETECTION — include only if diff mode -->
<section class="diff-section">
  <h2>Changes Since Last Scan</h2>
  <div class="diff-added">+ {{new_subdomain}} (first seen: {{date}})</div>
  <div class="diff-removed">- {{removed_subdomain}}</div>
</section>

<!-- SUBDOMAIN CATEGORY BREAKDOWN -->
<section>
  <h2>Subdomain Categories</h2>
  <div class="category-bar">
    <div class="category-pill">Mail <strong>{{n}}</strong></div>
    <div class="category-pill">API <strong>{{n}}</strong></div>
    <div class="category-pill">Admin <strong>{{n}}</strong></div>
    <div class="category-pill">Dev/Staging <strong>{{n}}</strong></div>
    <div class="category-pill">CDN <strong>{{n}}</strong></div>
    <div class="category-pill">Auth <strong>{{n}}</strong></div>
    <div class="category-pill">Internal <strong>{{n}}</strong></div>
    <div class="category-pill">Other <strong>{{n}}</strong></div>
  </div>
</section>

<!-- TIMELINE -->
<section>
  <h2>Discovery Timeline</h2>
  <div class="timeline">
    Oldest: <strong>{{oldest_date}}</strong> | Newest: <strong>{{newest_date}}</strong> | Peak: <strong>{{peak_month}} ({{peak_count}} new)</strong>
  </div>
</section>

<!-- SUBDOMAINS TABLE -->
<section>
  <h2>Discovered Subdomains</h2>
  <table>
    <thead><tr><th>Hostname</th><th>Category</th><th>Certificate CN</th><th>First Seen</th></tr></thead>
    <tbody>
      <tr><td>{{hostname}}</td><td><span class="badge category">{{cat}}</span></td><td>{{cn}}</td><td>{{first_seen}}</td></tr>
    </tbody>
  </table>
</section>

<!-- CA ANALYSIS -->
<section>
  <h2>Certificate Authority Analysis</h2>
  <div class="ca-chart">
    <div class="ca-bar">{{ca_name}} <span class="ca-count">{{count}}</span></div>
  </div>
</section>

<!-- WILDCARD MAPPING -->
<section>
  <h2>Wildcard Certificate Coverage</h2>
  <div class="wildcard-map">
    <h3>{{wildcard_cn}}</h3>
    <div class="coverage">Covers {{covered_count}} of {{total_count}} subdomains | {{uncovered_count}} subdomains have dedicated certs</div>
  </div>
</section>

<!-- CERTIFICATES TABLE -->
<section>
  <h2>Certificates</h2>
  <table>
    <thead><tr><th>Common Name</th><th>Issuer</th><th>Valid From</th><th>Valid Until</th><th>Status</th><th>Key</th><th>SHA-256</th></tr></thead>
    <tbody>
      <tr>
        <td>{{cn}}</td><td>{{issuer}}</td><td>{{not_before}}</td><td>{{not_after}}</td>
        <td><span class="badge valid">VALID</span></td>
        <td>{{algo}} {{size}}</td><td><code>{{sha256}}</code></td>
      </tr>
    </tbody>
  </table>
</section>

<!-- CERTIFICATE DEEP DIVE -->
<section>
  <h2>Certificate Details</h2>
  <div class="card" style="margin-bottom:1rem;">
    <div class="label">{{sha256_fingerprint}}</div>
    <table>
      <tr><td><strong>Subject</strong></td><td>{{common_name}} — {{organization}}, {{country}}</td></tr>
      <tr><td><strong>Issuer</strong></td><td>{{issuer_cn}} — {{issuer_org}}, {{issuer_country}}</td></tr>
      <tr><td><strong>Validity</strong></td><td>{{not_before}} to {{not_after}}</td></tr>
      <tr><td><strong>CT Logs</strong></td><td>{{log1}}, {{log2}}</td></tr>
      <tr><td><strong>Precertificate</strong></td><td>{{yes/no}}</td></tr>
    </table>
  </div>
</section>

<!-- TYPOSQUATTING -->
<section>
  <h2>Typosquatting / Lookalike Domains</h2>
  <table>
    <thead><tr><th>Lookalike Domain</th><th>Certificate CN</th><th>First Seen</th><th>Risk</th></tr></thead>
    <tbody>
      <tr><td>{{hostname}}</td><td>{{cn}}</td><td>{{first_seen}}</td><td><span class="badge expired">HIGH</span></td></tr>
    </tbody>
  </table>
</section>

<footer>
  Generated by MerkleMap OSINT Skill v3.0.0 | Data sourced from <a href="https://www.merklemap.com" style="color:var(--accent)">merklemap.com</a> Certificate Transparency database
</footer>

</div>
</body>
</html>
```

### Report Generation Instructions

1. **Run the scan first.** Perform whatever API calls the user requested and collect all results.
2. **Run all intelligence features** (categorization, CA analysis, temporal analysis, risk scoring, executive summary).
3. **Build the HTML.** Replace all `{{placeholders}}` with real data. **Only include sections relevant to the scan** — omit empty sections entirely.
4. **Populate summary cards** with actual counts.
5. **Generate findings** by analyzing the data:
   - **HIGH**: Expired certs, weak keys, self-signed certs, suspected active phishing domains
   - **MEDIUM**: Expiring within 30 days, unusual CAs, subdomain bursts, exposed dev/staging infrastructure
   - **INFO**: Large subdomain count, multiple CAs, wildcard coverage, newly discovered subdomains
6. **Apply status badges** in tables.
7. **Write the file** as `merklemap-report-{{domain}}-{{YYYY-MM-DD}}.html`.
8. **If JSON was also requested**, write the JSON file alongside it.
9. **Tell the user** the file path(s).

### Customization
- If the user specifies a file name or path, use that instead of the default naming.
- If the user asks for a "light theme" report, swap the CSS variables: `--bg: #ffffff; --surface: #f8fafc; --border: #e2e8f0; --text: #1e293b; --muted: #64748b;`
- The `@media print` block ensures the report looks clean when printed or saved as PDF from the browser.

---

## Presentation Guidelines
- Always use clean Markdown tables for structured data in chat responses.
- Lead with the **risk score** and **executive summary** first, then findings, then data tables.
- When results span multiple pages, summarize the first page and tell the user the total count.
- Keep explanations concise but include enough context for non-expert users to understand the significance.
- When performing multi-step workflows, give brief status updates between steps so the user knows what's happening.
- When the user asks for a report, always generate the HTML file — do not just paste HTML in the chat.
- When the user asks for JSON, always write the file — do not just paste JSON in the chat.
