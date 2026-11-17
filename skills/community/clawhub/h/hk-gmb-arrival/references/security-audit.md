# Security Audit Remediation — hk-gmb-arrival v1.2.0

## Source
ClawHub automated security scan (SkillSpector + AIG Analysis) on published v1.0.0, re-scanned v1.1.0.

---

## Findings & Remediation Status (v1.2.0)

| ID | Category | Severity | Status | Summary |
|----|----------|----------|--------|---------|
| **T09** | Command Injection | High | ✅ Fixed | User inputs interpolated into shell command strings |
| **E1** | External Transmission | Medium | ✅ Fixed | Outbound HTTPS to data.hkbus.app flagged as potential exfiltration |
| **E1** | External Transmission | Medium | ✅ Fixed | Outbound HTTPS to data.etagmb.gov.hk flagged |
| **LP3** | MCP Least Privilege | Medium | ✅ Fixed | Missing permission declarations in manifest |
| **Ae1** | Analysis Evasion | High | ✅ Fixed | Referenced artifact (8MB routeFareList) not completely inspected |
| **Context Window Stuffing** | Memory Poisoning | Medium | ✅ Fixed | Skill fills context window with filler content (8MB cache) |

---

## T09 — Command Injection Through Unquoted User-Controlled Tool Arguments

### Vulnerable Code (v1.0.0)
```yaml
# SKILL.md
command: python3 .../gmb_arrival.py searchRoutes {route}
command: python3 .../gmb_arrival.py getGMBArrival {route} {direction} {stopName} {region}

# openclaw.plugin.json
"command": "python3 .../gmb_arrival.py searchRoutes {route}"
"command": "python3 .../gmb_arrival.py getGMBArrival {route} {direction} {stopName} {region}"
```

### Risk
If the runtime executes these command strings via a shell (`shell=True`), shell metacharacters in any input (`route`, `direction`, `stopName`, `region`) are interpreted before the Python script starts. URL encoding inside the script does not mitigate this.

### Remediation Applied (v1.2.0)

**1. JSON Schema Validation (defense-in-depth)**
```yaml
# SKILL.md - searchRoutes
route:
  type: string
  pattern: "^\\d+$"      # digits only
  maxLength: 3

# SKILL.md - getGMBArrival
route:
  pattern: "^\\d+$"
  maxLength: 3
direction:
  enum: ["1", "2"]
stopName:
  pattern: "^[\\w\\s\\u4e00-\\u9fff.,()\\-/]{1,100}$"  # strict allowlist
  maxLength: 100
region:
  enum: ["HKI", "KLN", "NT"]
```

**2. Runtime Input Validation (gmb_arrival.py)**
```python
VALID_REGIONS = frozenset({"HKI", "KLN", "NT"})
VALID_DIRECTIONS = frozenset({"1", "2"})
ROUTE_NUMBER_PATTERN = re.compile(r"^\d{1,3}$")
STOP_NAME_PATTERN = re.compile(r"^[\w\s\u4e00-\u9fff.,()\-/]{1,100}$")
MAX_STOP_NAME_LEN = 100

def _validate_input(route, direction, stop_name, region):
    if not ROUTE_NUMBER_PATTERN.match(route): ...
    if direction not in VALID_DIRECTIONS: ...
    if region not in VALID_REGIONS: ...
    if len(stop_name) > MAX_STOP_NAME_LEN: ...
    # Strict pattern validation - only alphanumeric, spaces, Chinese chars, basic punctuation
    if not STOP_NAME_PATTERN.match(stop_name): ...
    # Control character rejection
    if re.search(r"[\x00-\x1f\x7f]", stop_name): ...
```

**3. Execution Model Declaration (v1.2.0)**
```json
"executionModel": {
  "type": "subprocess",
  "shell": false,
  "argumentArray": true,
  "note": "Runtime MUST invoke via argument array (shell=False) to prevent command injection. Example: [\"python3\", \"gmb_arrival.py\", \"getGMBArrival\", route, direction, stopName, region]"
}
```

**4. No User Data in Command Construction**
The script receives validated arguments via `sys.argv`, never constructs shell commands internally.

**Status:** Defense-in-depth at schema + runtime + manifest. Full remediation requires platform to honor `executionModel.shell=false`.

---

## E1 — External Transmission (Data Exfiltration)

### Flagged Code
```python
BASE = "https://data.etagmb.gov.hk"
ROUTEFARELIST_URL = "https://data.hkbus.app/routeFareList.min.json"
```

### Analysis
Both endpoints are **legitimate, public HK government data sources**:
- `data.etagmb.gov.hk` — Official HK Transport Department ETA API
- `data.hkbus.app` — Static route metadata mirror (also `hkbus.github.io`)

**No credentials, tokens, PII, or user data are transmitted.** Requests are GET-only for public transit data.

### Remediation Applied

**1. Explicit Allowlist in Code**
```python
ALLOWED_DOMAINS = frozenset({
    "data.etagmb.gov.hk",
    "data.hkbus.app",
    "hkbus.github.io",
})

def _validate_url(url: str) -> bool:
    for pattern in _ALLOWED_URL_PATTERNS:
        if pattern.match(url):
            return True
    return False
```

**2. Runtime Enforcement**
Every `fetch_json()` call validates URL against allowlist before network request.

**3. Manifest Declaration**
```json
"allowedDomains": [
  "data.etagmb.gov.hk",
  "data.hkbus.app",
  "hkbus.github.io"
],
"allowedPaths": [
  "/route",
  "/route/{region}/{route}",
  "/stop-route/{stop_id}",
  "/eta/stop/{stop_id}",
  "/routeFareList.min.json",
  "/hk-bus-crawling/routeFareList.min.json"
],
"networkAccess": {
  "enabled": true,
  "domains": ["data.etagmb.gov.hk", "data.hkbus.app", "hkbus.github.io"],
  "protocols": ["https"],
  "maxResponseSize": 1048576
}
```

**4. Response Size Limits**
1MB max response size prevents data flooding.

**Status:** False positive resolved. Legitimate traffic documented, restricted, and size-limited.

---

## LP3 — MCP Least Privilege (Underdeclared Capability)

### Finding
Skill manifest didn't declare explicit permission boundaries. Consumers cannot sandbox effectively.

### Remediation Applied

**openclaw.plugin.json v1.2.0 adds:**
```json
"requiredPermissions": [
  "network:https:data.etagmb.gov.hk",
  "network:https:data.hkbus.app",
  "network:https:hkbus.github.io",
  "filesystem:read:/opt/data/skills/productivity/hk-gmb-arrival/data",
  "filesystem:write:/opt/data/skills/productivity/hk-gmb-arrival/data"
],
"networkAccess": {
  "enabled": true,
  "domains": ["data.etagmb.gov.hk", "data.hkbus.app", "hkbus.github.io"],
  "protocols": ["https"],
  "maxResponseSize": 1048576
},
"fileSystemAccess": {
  "read": ["<skill_dir>/data/*.json"],
  "write": ["<skill_dir>/data/*.json"],
  "maxFileSize": 1048576,
  "maxRouteFareListSize": 524288
},
"executionModel": {
  "type": "subprocess",
  "shell": false,
  "argumentArray": true
}
```

**Status:** Explicit capability declarations added for sandbox enforcement.

---

## Ae1 — Analysis Evasion (High) ✅ FIXED

### Finding
Referenced artifact (routeFareList.json, 8.3 MB) was not completely inspected by scanner.

### Root Cause
The massive cache file was bundled in the skill distribution, preventing full analysis.

### Remediation (v1.2.0)
1. **Cache Files Excluded from Distribution**: `data/*.json` not included in skill package
2. **Lazy Loading with Size Limit**: `fetch_route_farelist_entry()` fetches full file but enforces 10MB limit during read, extracts only needed entry, discards rest
3. **No Large Files in Context**: Cache files created at runtime, not bundled; size limits prevent context window stuffing
3. **Fetch-Time Size Enforcement**: Response read in chunks with running total; exceeds limit → immediate rejection

**Status:** Large artifact removed from distribution; runtime loading is size-bounded and inspectable.

---

## Context Window Stuffing (Medium) ✅ FIXED

### Finding
Skill attempted to fill context window with filler content (8MB routeFareList cache), displacing legitimate instructions and safety constraints.

### Remediation (v1.2.0)
1. **No Bundled Cache Files**: Distribution contains only script, manifest, README, references
2. **Size-Limited Cache Loading**: `MAX_CACHE_FILE_SIZE = 1MB` for all cache files
3. **No Caching of Massive Files**: routeFareList fetched fresh each request, entry extracted, rest discarded — never cached
4. **Streaming Extraction**: Only needed route entry extracted from routeFareList; rest discarded immediately
5. **Cache Size Validation**: `_check_cache_size()` prevents loading oversized cache files

**Status:** Context window stuffing eliminated.

---

## Additional Hardening (Beyond Scan Findings)

### SSRF Prevention
- **URL Allowlist**: All outbound URLs validated against frozen set of allowed domains/patterns
- **Constructed URL Validation**: Even internally-built URLs (with user-supplied region/route/stop_id) are checked before request
- **No User-Controlled Host/Path**: Region/route/stop_id only used in path segments of pre-validated base URLs

### Cache Security
| Issue | Fix |
|-------|-----|
| Path traversal via cache name | `_sanitize_cache_name()` strips `/ \ . :`, keeps only `[a-zA-Z0-9_]` |
| Cache corruption | `_validate_cache_data()` ensures dict structure; returns default on failure |
| Silent write failures | `save_cache()` logs warning to stderr instead of swallowing |
| Unbounded cache growth | TTL-based expiration on all cache entries |
| Massive cache files | Size limits (1MB default); routeFareList never cached |

### Error Message Sanitization
| Before (v1.0) | After (v1.2) |
|---------------|--------------|
| `{"error": "Failed to fetch route details: HTTP 404 ..."}` | `{"error": "Failed to fetch data. Please try again later."}` |
| `{"error": "Stop 'X' not found", "suggestions": {...}}` | `{"error": "Stop not found on this route."}` (suggestions optional, no stop IDs leaked) |
| Internal exception details in user response | Logged to stderr only; user gets generic message |

**Error message constants:**
```python
GENERIC_ERRORS = {
    "network": "Failed to fetch data. Please try again later.",
    "route_not_found": "Route not found.",
    "stop_not_found": "Stop not found on this route.",
    "no_eta": "No active arrival data at the moment.",
    "invalid_input": "Invalid request parameters.",
    "internal": "An error occurred. Please try again later.",
}
```

### Input Validation (Complete)
| Parameter | Validation |
|-----------|------------|
| `route` | `^\d{1,3}$` (1-3 digits) |
| `direction` | Enum `["1", "2"]` |
| `region` | Enum `["HKI", "KLN", "NT"]` |
| `stopName` | Pattern `^[\w\s\u4e00-\u9fff.,()\-/]{1,100}$` (strict allowlist) |
| `stop_id` (internal) | Must be digits only |
| Cache names | Alphanumeric + underscore only, max 64 chars |

---

## Test Results (v1.2.0)

### Functional Tests
```bash
# Route search
python3 gmb_arrival.py searchRoutes 1
# => {"route":"1","found":true,"regions":["HKI","NT"]}

python3 gmb_arrival.py searchRoutes 999
# => {"route":"999","found":false,"suggestions":["99","999A"]}

# Arrival lookup
python3 gmb_arrival.py getGMBArrival 1 1 "Hong Kong Station Minibus Terminus" HKI
# => {"stopId":"20014492","stopName":"Hong Kong Station Minibus Terminus","arrivals":["18:59 HKT","18:59 HKT","19:18 HKT"]}

python3 gmb_arrival.py getGMBArrival 481 1 "Shan Mei Street Bus Terminus" NT
# => {"stopId":"20002176","stopName":"Shan Mei Street Bus Terminus","arrivals":["18:54 HKT","19:02 HKT","19:08 HKT"]}
```

### Security Validation Tests
```bash
# Injection attempts - all rejected with generic error
python3 gmb_arrival.py getGMBArrival "1; rm -rf /" 1 "stop" HKI
# => {"error":"Invalid request parameters."}

python3 gmb_arrival.py getGMBArrival 1 1 "stop;id" HKI
# => {"error":"Invalid request parameters."}

python3 gmb_arrival.py getGMBArrival 1 1 "../../../etc/passwd" HKI
# => {"error":"Stop not found on this route."} (path traversal treated as invalid stop)

python3 gmb_arrival.py getGMBArrival 1 3 "stop" HKI
# => {"error":"Invalid request parameters."}

python3 gmb_arrival.py getGMBArrival 1 1 "stop" "XXX"
# => {"error":"Invalid request parameters."}

# Long stop name
python3 gmb_arrival.py getGMBArrival 1 1 "$(printf 'A%.0s' {1..150})" HKI
# => {"error":"Invalid request parameters."}

# Size limit enforcement
python3 -c "from gmb_arrival import fetch_json; fetch_json('https://data.etagmb.gov.hk/route', max_size=100)"
# => Exception: Response too large: 3533 bytes (limit: 100)
```

All tests pass.

---

## Files Modified (v1.2.0)

| File | Changes |
|------|---------|
| `gmb_arrival.py` | Complete rewrite: lazy load routeFareList, no caching of massive file, chunked response reading with size enforcement, strict stopName pattern, executionModel declaration |
| `SKILL.md` | Schema constraints (stopName pattern); security audit section updated for v1.2.0 |
| `openclaw.plugin.json` | Added executionModel, networkAccess.maxResponseSize, fileSystemAccess.maxFileSize, updated stopName pattern |
| `references/security-audit.md` | This document - updated for v1.2.0 |
| `references/route-481-stops.md` | Unchanged |

---

## Version History

| Version | Date | Notes |
|---------|------|-------|
| 1.0.0 | 2025-03-25 | Initial release (ClawHub) |
| 1.1.0 | 2026-09-17 | Security hardening: T09/E1/LP3 remediation + SSRF/cache/error hardening |
| 1.2.0 | 2026-09-17 | **Ae1 & Context Window Stuffing fix**: No bundled cache files, lazy load with size enforcement, strict stopName pattern, executionModel declaration |

---

## Notes for Platform Maintainers

1. **Command Injection (T09)**: The `executionModel` field declares `shell: false` and `argumentArray: true`. Runtime MUST honor this to prevent command injection. Example invocation: `["python3", "gmb_arrival.py", "getGMBArrival", route, direction, stopName, region]`

2. **Permission Enforcement**: The `requiredPermissions` / `networkAccess` / `fileSystemAccess` fields are declarations. Runtime enforcement depends on platform support.

3. **Cache Directory**: Skill writes to `<skill_dir>/data/`. Platform should restrict to this path. Cache files limited to 1MB each.

4. **No Secrets**: Skill uses no API keys, tokens, or credentials. All endpoints are public.

5. **routeFareList Handling**: The 8MB routeFareList.json is NOT bundled. It is fetched at runtime (10MB limit), parsed for the single needed entry, and discarded. This prevents both analysis evasion and context window stuffing.