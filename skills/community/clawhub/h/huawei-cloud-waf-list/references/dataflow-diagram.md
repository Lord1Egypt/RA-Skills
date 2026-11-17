# Data Flow Diagram

```mermaid
flowchart TD
    A[User / Agent] --> B[list_waf_sites.py]
    B --> C{Parse args}
    C -->|--mode premium| D1[hcloud WAF ListCompositeHosts]
    C -->|--all-modes| D1
    C -->|default / --mode cloud| D2[hcloud WAF ListHost]
    D1 --> E1[GET /v1/{project_id}/composite-waf/host]
    D2 --> E2[GET /v1/{project_id}/waf/instance]
    E1 --> F[Parse JSON + normalize waf_type]
    E2 --> F
    F --> G{Output mode}
    G -->|--json| H[JSON response body]
    G -->|--names-only| I[Unique sorted domain list]
    G -->|default| J[Key-field table]
    F -.->|empty| K[当前区域无 WAF 防护网站]
    F -.->|WAF.00012006 / APIGW.0802| L[Explicit error hint]
    F -.->|write intent detected| M[Read-only guard error]
```

## Flow description

1. The agent (or user) invokes the entry script with an optional region, scope
   and filters.
2. The script validates there is no write intent, then builds the matching
   read-only KooCLI command:
   - cloud mode → `hcloud WAF ListHost`
   - all modes / premium → `hcloud WAF ListCompositeHosts`
3. The hcloud CLI resolves credentials from its profile/environment and calls
   the regional WAF endpoint.
4. The JSON response is parsed and normalized: `waf_type` (`cloud`/`premium`)
   marks the access mode, `protect_status`/`access_status` the protection
   state, `proxy` the keep-alive mode.
5. Output is rendered as a table (default), raw JSON (`--json`), or a unique
   sorted domain list (`--names-only`). Errors are mapped to explicit Chinese
   hints.