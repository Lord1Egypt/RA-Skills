# Module 07 — CVE Scan

## Detection Strategy (tries in order)

### EXECUTION NOTE
All commands run via `ssh_exec(op="run", sessionId, command="<command>")` on the remote server. Output retrieved via `ssh_exec(op="logs", commandId=cmdId)`. API calls (CISA KEV, OSV.dev, NVD) execute via `ssh_exec` on the remote server using `curl`. No local command execution.

### LOCAL METHODS (local tools, no network needed)

```bash
# Method 1: debsecan (Debian/Ubuntu — most accurate)
which debsecan >/dev/null 2>&1 && debsecan --suite $(lsb_release -cs) --only-fixed --format=detail

# Method 2: Ubuntu CVEScan
which cvescan >/dev/null 2>&1 && cvescan

# Method 3: apt security info (fallback)
apt-get --just-print upgrade 2>/dev/null | grep "^Inst" | grep -i "security\|CVE"

# Method 4: RHEL/CentOS yum security
which yum >/dev/null 2>&1 && yum updateinfo list security 2>/dev/null

# Method 5: Installed package list (for external source cross-ref)
dpkg-query -W -f='${Package}\t${Version}\n' 2>/dev/null
# Or: rpm -qa --queryformat '%{NAME}\t%{VERSION}\n' 2>/dev/null
```

### EXTERNAL METHODS (requires internet — enrich local findings)

```bash
# ═══════════════════════════════════════════════════════════════
# METHOD 6: CISA KEV Catalog [CURL] ✅
# ═══════════════════════════════════════════════════════════════
# URL: https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json
# No API key needed. No rate limits. Always works with curl.
# Cross-ref against installed packages. KEV match → auto-CRITICAL.
#
# curl -s "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json" \
#   | jq '[.vulnerabilities[] | select(.vendorProject == "Linux")]'

# ═══════════════════════════════════════════════════════════════
# METHOD 7: OSV.dev — open source vuln DB [CURL] ✅
# ═══════════════════════════════════════════════════════════════
# POST https://api.osv.dev/v1/query (single)
# POST https://api.osv.dev/v1/querybatch (batch — up to 1000)
# No API key. No rate limits. Always works with curl.
# Best method: matches by package + ecosystem + version.
#
# curl -s -X POST "https://api.osv.dev/v1/querybatch" \
#   -H "Content-Type: application/json" \
#   -d '{"queries":[
#     {"package":{"name":"openssl","ecosystem":"Debian"},"version":"3.0.2"},
#     {"package":{"name":"nginx","ecosystem":"Debian"},"version":"1.22.0"}
#   ]}'

# ═══════════════════════════════════════════════════════════════
# METHOD 8: NVD API 2.0 [CURL] ⚠️ rate limited
# ═══════════════════════════════════════════════════════════════
# URL: https://services.nvd.nist.gov/rest/json/cves/2.0
# Rate limit: 5 req/30s (no key), 50 req/30s (with key)
# API key (free): https://nvd.nist.gov/developers/request-an-api-key [BROWSER]
# ⚠️ API endpoint works with curl. Web portal (nvd.nist.gov) is CLOUDFLARE BLOCKED.
#
# Without key (sleep 6s between calls):
#   curl -s "https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch=linux&resultsPerPage=5"
# With key:
#   curl -s -H "apiKey:NVD_API_KEY" "https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2024-1086"
#
# ⚠️ Skip if blocked: if curl returns Cloudflare "Attention Required" → SKIP immediately
#    Do NOT retry. OSV.dev and CISA KEV already cover what NVD would tell you.

# ═══════════════════════════════════════════════════════════════
# METHOD 9: Web portal URLs [BROWSER] ❌ Cloudflare blocks curl
# ═══════════════════════════════════════════════════════════════
# Only use with browser tool. DO NOT use curl on these URLs.
#
# CISA KEV (Linux filter):
#   https://www.cisa.gov/known-exploited-vulnerabilities-catalog?f%5B0%5D=vendor_project%3ALinux
#
# NVD Search — Linux:
#   https://nvd.nist.gov/vuln/search/results?query=linux&search_type=all&queryType=phrase
#
# NVD Search — Critical Linux:
#   https://nvd.nist.gov/vuln/search/results?query=linux&cvssSeverity=CRITICAL&queryType=phrase
#
# OSV.dev — Linux kernel:
#   https://osv.dev/list?ecosystem=Linux
```

### Skip Logic (— every method runs independently)

```
EACH external method follows this rule:

1. curl --max-time 15 --connect-timeout 10 $URL
2. if curl exit code != 0:
     → Log "[SKIP] $SOURCE unavailable (network)"
     → Move to next source. Not fatal.
3. if response contains "Attention Required" OR "Cloudflare" OR "cf-wrapper":
     → Log "[SKIP] $SOURCE blocked by Cloudflare — use browser tool only"
     → Skip permanently this session. Don't retry. Ever.
4. if HTTP 429 (rate limit):
     → Sleep 6s, retry once
     → Still 429? Log "[SKIP] $SOURCE rate limited — too many requests"
     → Skip.
5. Success → parse results, write advisories, continue next method.

NEVER let one blocked/failed source fail the entire scan.
Each source is independent.
```

### URL Working Status Quick Reference

| URL | curl | Browser | Notes |
|-----|------|---------|-------|
| `cisa.gov/.../known_exploited_vulnerabilities.json` | ✅ Works | ✅ Works | No key needed |
| `services.nvd.nist.gov/rest/json/cves/2.0` | ✅ Works | ❌ API only | Rate limited |
| `nvd.nist.gov/vuln/search` | ❌ **Cloudflare** | ✅ Works | Do NOT use curl |
| `nvd.nist.gov/vuln/detail/CVE-XXXX` | ❌ **Cloudflare** | ✅ Works | Do NOT use curl |
| `api.osv.dev/v1/querybatch` | ✅ Works | ❌ API only | No key needed |
| `osv.dev/list` | ✅ Works | ✅ Works | Web UI |

### Priority Chain

```
1. cve/cve-scan.sh (external: CISA KEV + OSV.dev batch + NVD API)
   → Run first if internet available via: cve/cve-scan.sh --client <name> --server <name>
   → Each source independent — if one fails, others still run
   → Writes to cve/<client>/<server>/scan-results/YYYY-MM-DD.md
   → Advisories to cve/<client>/<server>/advisories/<CVE-ID>.md
   → Matches against installed packages from dpkg-query

2. Local methods 1-5 (debsecan / cvescan / apt / yum)
   → Always run as baseline (no network dependency)
   → Catch what external methods miss

3. Web portal URLs [BROWSER]
   → Agent opens in browser for manual verification
   → Use when API calls are blocked or for deep investigation
   → NVD portal blocked by Cloudflare — only works in browser
```

## CVE Severity Classification (CVSS v3)

| CVSS Score | Severity | Action |
|---|---|---|
| 9.0 – 10.0 | CRITICAL | Immediate alert + confirm to patch |
| 7.0 – 8.9 | HIGH | Queue confirm to patch |
| 4.0 – 6.9 | MEDIUM | Report + advisory |
| 0.1 – 3.9 | LOW | Report only |

## External Source Override Flags

| Flag | Source | Impact |
|---|---|---|
| `KEV` | CISA Known Exploited Vulnerabilities | ⚡ Any CVE in KEV → treat as CRITICAL regardless of CVSS |
| `RANSOMWARE` | CISA KEV (knownRansomwareCampaignUse) | 🔥 Highest priority — immediate alert + confirm within due date |
| `OSV_MATCH` | OSV.dev (version match) | Confirmed vulnerable version installed — treat per CVSS |
| `NVD_CORROBORATED` | NVD API cross-check | Dual-source confirmed — increase severity by one level |

## Output to cve/<client>/<server>/scan-results/YYYY-MM-DD.md

```markdown
# CVE Scan — YYYY-MM-DD

## Summary
- Method used: debsecan / cvescan / apt-fallback
- Total CVEs found: N
- Critical: N | High: N | Medium: N | Low: N

## Critical CVEs
| CVE ID | Package | CVSS | Description | Patch Available |
|---|---|---|---|---|

## High CVEs
...

## Patch Commands
# For each patchable CVE:
# apt-get install --only-upgrade <package>
```

## Individual Advisory (for CVSS ≥ 7.0 OR KEV entry)
Write to cve/<client>/<server>/advisories/<CVE-ID>.md with full detail including source attribution.

### Advisory Format
```markdown
# CVE-2024-XXXXX — <package>

**Severity:** CRITICAL | HIGH
**CVSS:** 9.8
**Source:** CISA KEV | OSV.dev | NVD API
**Flags:** KEV | RANSOMWARE | OSV_MATCH | NVD_CORROBORATED
**Package:** openssh-server
**Installed Version:** 8.9p1
**Patch Available:** yes / no
**Due Date:** YYYY-MM-DD (if from KEV)
**Scan Date:** YYYY-MM-DD

## Description
...

## References
- https://nvd.nist.gov/vuln/detail/<CVE-ID>
- https://www.cve.org/CVERecord?id=<CVE-ID>
- https://osv.dev/vulnerability/<CVE-ID> (if OSV match)
```

## Output Format
```
[CRITICAL][KEV] 07-cve: CVE-2024-XXXXX | package: openssh-server | cvss: 9.8 | patch: available | action_id: ACT-XXX
[HIGH][OSV_MATCH] 07-cve: CVE-2024-YYYYY | package: sudo | cvss: 7.8 | patch: available | action_id: ACT-YYY
[CRITICAL][RANSOMWARE] 07-cve: CVE-2024-ZZZZZ | package: nginx | cvss: 7.5 | kev: ransomware_known | due: 2024-06-15 | action_id: ACT-ZZZ
[INFO] 07-cve: scan_complete | total: 23 | critical: 1 | high: 3 | medium: 12 | low: 7
[INFO] 07-cve: external_sources | cisa_kev: 2_matches | osv_dev: 5_matches | nvd_api: 10_findings
```

## External Script
CVE scan commands run via `ssh_exec(op="run", sessionId, command="...")` on the remote server:
- `dpkg-query -W -f='${Package}\t${Version}\n'` → installed packages
- `curl -s 'https://www.cisa.gov/...'` → CISA KEV fetch
- `curl -s -X POST 'https://api.osv.dev/v1/querybatch'` → OSV.dev query
- `curl -s 'https://services.nvd.nist.gov/rest/json/cves/2.0?...'` → NVD query
Results parsed locally, advisories written to `cve/<client>/<server>/advisories/<CVE-ID>.md`.
Scan report to `cve/<client>/<server>/scan-results/YYYY-MM-DD.md`.
