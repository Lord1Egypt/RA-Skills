# External CVE Data Sources

Working URLs marked with:
- `[CURL]` — works with curl/fetch directly
- `[API]` — REST API endpoint  
- `[BROWSER]` — blocks curl (Cloudflare bot protection). Use browser tool only.
- `[SKIP_IF_BLOCKED]` — if curl gets blocked, just skip. No crash.

---

## 1. CISA Known Exploited Vulnerabilities (KEV) Catalog

**Status:** ✅ Fully working with curl. No API key needed. No rate limits. Updated daily.

### URLs
| Type | URL | Works With |
|------|-----|-----------|
| JSON Feed | `https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json` | `[CURL]` ✅ |
| JSON Schema | `https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities_schema.json` | `[CURL]` ✅ |
| CSV Export | `https://www.cisa.gov/sites/default/files/csv/known_exploited_vulnerabilities.csv` | `[CURL]` ✅ |
| Web Portal | `https://www.cisa.gov/known-exploited-vulnerabilities-catalog` | `[BROWSER]` |

### Query params
```
?f[0]=vendor_project:Linux   → filter by vendor
?sort=date_added desc        → sort by date
```

### Fetch (always works with curl)
```bash
# Full catalog
curl -s "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"

# Filter Linux only
curl -s "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json" \
  | jq '[.vulnerabilities[] | select(.vendorProject == "Linux")]'

# Filter by date range (last 30 days)
curl -s "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json" \
  | jq '[.vulnerabilities[] | select(.dateAdded >= "2026-04-28")]'
```

### JSON Fields
| Field | Type | Description |
|-------|------|-------------|
| `cveID` | string | CVE identifier |
| `vendorProject` | string | Vendor name |
| `product` | string | Product name |
| `vulnerabilityName` | string | Short title |
| `dateAdded` | string | Date added to KEV (YYYY-MM-DD) |
| `shortDescription` | string | Description |
| `requiredAction` | string | Remediation instructions |
| `dueDate` | string | Remediation due date |
| `knownRansomwareCampaignUse` | string | "Known" or "Unknown" |
| `cwes` | array | CWE IDs |

---

## 2. NVD (National Vulnerability Database)

**IMPORTANT:** NVD has TWO surfaces:
- **API** (`services.nvd.nist.gov`) — works with curl, rate limited
- **Web Portal** (`nvd.nist.gov`) — **BLOCKED BY CLOUDFLARE** — curl gets `Attention Required!` page. Only use browser tool.

### NVD API [CURL] ✅ — Always works with curl

| Item | URL |
|------|-----|
| API Base | `https://services.nvd.nist.gov/rest/json/cves/2.0` |
| API Key Request | `https://nvd.nist.gov/developers/request-an-api-key` `[BROWSER]` |
| Docs | `https://nvd.nist.gov/developers/start-here` `[BROWSER]` |
| Terms | `https://nvd.nist.gov/developers/terms-of-use` |

**Rate limits:** Without key = 5 req/30s. With key = 50 req/30s.  
**API key = free. No key? Use OSV.dev instead — no rate limits.**

### Query Parameters (for services.nvd.nist.gov API)

| Param | Type | Example |
|-------|------|---------|
| `keywordSearch` | string | `linux`, `openssl` |
| `keywordExactMatch` | boolean | (use empty string for match) |
| `cveId` | string | `CVE-2024-1086` |
| `pubStartDate` | ISO 8601 | `2026-04-28T00:00:00.000` |
| `pubEndDate` | ISO 8601 | `2026-05-28T23:59:59.999` |
| `lastModStartDate` | ISO 8601 | ... |
| `lastModEndDate` | ISO 8601 | ... |
| `cvssV3Severity` | enum | `CRITICAL`, `HIGH`, `MEDIUM`, `LOW` |
| `resultsPerPage` | int | `25` (default), max `200` |
| `startIndex` | int | pagination cursor |

### Fetch (curl — always works)
```bash
# By keyword (no API key)
curl -s "https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch=linux&resultsPerPage=5"

# By keyword (with API key — recommended)
curl -s -H "apiKey:YOUR_KEY" \
  "https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch=linux&resultsPerPage=5"

# Specific CVE
curl -s "https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2024-1086"

# Critical + Linux
curl -s -H "apiKey:YOUR_KEY" \
  "https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch=linux&cvssV3Severity=CRITICAL&resultsPerPage=10"
```

### NVD Web Portal [BROWSER] ❌ — Cloudflare blocks curl

**Do NOT use curl on these URLs — they return Cloudflare block page.**  
Only works when agent opens with browser tool.

```
# Linux CVEs
https://nvd.nist.gov/vuln/search/results?query=linux&search_type=all&queryType=phrase

# Linux critical CVEs
https://nvd.nist.gov/vuln/search/results?query=linux&cvssSeverity=CRITICAL&queryType=phrase

# Last 90 days Linux
https://nvd.nist.gov/vuln/search/results?query=linux&pub_date_range=90&search_type=all

# Specific CVE detail
https://nvd.nist.gov/vuln/detail/CVE-2024-1086
```

### Fallback rule for NVD
```
IF curl to services.nvd.nist.gov returns 403 / Cloudflare / timeout:
  → SKIP NVD entirely. Do not retry.
  → OSV.dev and CISA KEV already provide sufficient coverage.
  → Log: "[SKIP] 07-cve: nvd_api blocked by Cloudflare — skipped"

IF curl succeeds but rate limited (HTTP 429):
  → Sleep 6s, retry once
  → Still fails? Skip. Move on.
```

---

## 3. OSV.dev (Open Source Vulnerabilities) [CURL] ✅

**Status:** ✅ Fully working with curl. No API key. No rate limits.  
**Best for:** matching installed packages by name + ecosystem + version (batch query up to 1000).

### URLs
| Type | URL |
|------|-----|
| Query (POST) | `https://api.osv.dev/v1/query` |
| Batch Query (POST) | `https://api.osv.dev/v1/querybatch` |
| Get Vuln (GET) | `https://api.osv.dev/v1/vulns/{id}` |
| Web Portal | `https://osv.dev/list` |
| Docs | `https://google.github.io/osv.dev/` |
| Schema | `https://ossf.github.io/osv-schema/` |

### Query by Package + Version (curl — always works)
```bash
# Single package
curl -s -X POST "https://api.osv.dev/v1/query" \
  -H "Content-Type: application/json" \
  -d '{"package":{"name":"openssl","ecosystem":"Debian"},"version":"3.0.2"}'

# By PURL
curl -s -X POST "https://api.osv.dev/v1/query" \
  -H "Content-Type: application/json" \
  -d '{"package":{"purl":"pkg:deb/debian/openssl@3.0.2"}}'

# Linux kernel
curl -s -X POST "https://api.osv.dev/v1/query" \
  -H "Content-Type: application/json" \
  -d '{"package":{"name":"linux","ecosystem":"Linux"},"version":"6.1.0"}'

# By git commit hash
curl -s -X POST "https://api.osv.dev/v1/query" \
  -H "Content-Type: application/json" \
  -d '{"commit":"6879efc2c1596d11a6a6ad296f80063b558d5e0f"}'

# Get specific vuln detail
curl -s "https://api.osv.dev/v1/vulns/CVE-2024-1086"
```

### Batch Query (up to 1000 packages — use this for full audit)
```bash
curl -s -X POST "https://api.osv.dev/v1/querybatch" \
  -H "Content-Type: application/json" \
  -d '{"queries":[
    {"package":{"name":"openssl","ecosystem":"Debian"},"version":"3.0.2"},
    {"package":{"name":"openssh","ecosystem":"Debian"},"version":"9.0p1"},
    {"package":{"name":"nginx","ecosystem":"Debian"},"version":"1.22.0"}
  ]}'
```

### Supported Ecosystems
```
Debian, Ubuntu, Alpine, Red Hat, SUSE, openSUSE, Rocky Linux,
AlmaLinux, Mageia, openEuler, Wolfi, Chainguard, Android,
Linux (kernel), npm, PyPI, Go, crates.io, RubyGems, NuGet,
Maven, Packagist, Pub, Hex, Julia, GIT, GitHub Actions,
OSS-Fuzz, CRAN, Hackage, opam, SwiftURL, Bitnami, GHC
```

### Response Fields
```json
{
  "vulns": [{
    "id": "CVE-2024-XXXX",
    "summary": "Short description",
    "details": "Long description",
    "aliases": ["CVE-2024-XXXX"],
    "modified": "2024-01-01T00:00:00Z",
    "published": "2024-01-01T00:00:00Z",
    "references": [{"type": "WEB", "url": "..."}],
    "affected": [{
      "package": {"name": "openssl", "ecosystem": "Debian"},
      "ranges": [{"type": "SEMVER", "events": [{"introduced": "0"}, {"fixed": "3.0.3"}]}],
      "versions": ["3.0.1", "3.0.2"]
    }],
    "database_specific": {"severity": "HIGH"}
  }]
}
```

### ⚠️ Known Issue: OSV.dev may return DEBIAN-CVE-* IDs instead of CVE-*
Some OSV.dev responses return IDs like `DEBIAN-CVE-2024-XXXX` instead of `CVE-2024-XXXX`. This is normal — it's the Debian tracker ID. Map it to the real CVE via the `aliases` field.

---

## 4. Quick Reference: What Works With What

| Source | curl/fetch | Browser Tool | API Key Needed | Rate Limited |
|--------|-----------|-------------|----------------|-------------|
| CISA KEV JSON Feed | ✅ Yes | ✅ Yes | No | No |
| CISA KEV Web Portal | ❌ Blocks? | ✅ Yes | No | No |
| NVD API (services.nvd.nist.gov) | ✅ Yes | N/A | Recommended | 5/30s no key, 50/30s with key |
| NVD Web Portal (nvd.nist.gov) | ❌ **Cloudflare blocks** | ✅ Yes | No | No |
| OSV.dev API | ✅ Yes | N/A | No | No |
| OSV.dev Web Portal | ✅ Yes | ✅ Yes | No | No |

## 5. Fallback Chain (what script uses)

```
TRY Method A: OSV.dev batch query [CURL]
  → Works? Great. Parse results. Write advisories.
  → Fails? → Skip. Log as unavailable.

TRY Method B: CISA KEV JSON Feed [CURL]
  → Works? Cross-ref against installed packages. Flag KEV matches as CRITICAL.
  → Fails? → Skip. Use cached version if available.

TRY Method C: NVD API [CURL]
  → Works? Cross-check critical packages.
  → HTTP 403/Cloudflare? → SKIP. Log: "blocked by Cloudflare".
  → HTTP 429 (rate limit)? → Sleep 6s, retry once. Still fail? Skip.

FALLBACK: Web portal URLs [BROWSER]
  → Agent opens URLs in browser tool for manual inspection.
  → Only when API methods fail or for deep investigation.
```

## 6. Skip Logic (for script)

```bash
# If any source fails, just skip it. Don't retry more than once.
# Don't let one blocked API break the whole scan.

LOGIC:
  curl --max-time 15 --connect-timeout 10 $URL > /dev/null 2>&1
  if $? != 0:
    log "[SKIP] $SOURCE unavailable — continuing with other sources"
    continue  # next source

  if response contains "Attention Required" || "Cloudflare":
    log "[SKIP] $SOURCE blocked by Cloudflare — use browser tool instead"
    continue  # skip, not fatal

  if HTTP 429 (rate limit):
    sleep 6s
    retry once
    if still 429:
      log "[SKIP] $SOURCE rate limited — skipping"
```
