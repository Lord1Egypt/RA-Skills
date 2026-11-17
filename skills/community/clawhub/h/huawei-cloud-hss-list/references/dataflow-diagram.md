# Data Flow Diagram

```mermaid
flowchart LR
    agent[AI Agent] -->|python3 scripts/list_hss.py --region &lt;region&gt;| script[list_hss.py]

    script --> cli{hcloud installed?}
    cli -- yes --> hcloud["hcloud HSS ListHostStatus<br/>GET /v5/{project_id}/host-management/hosts"]
    hcloud --> api[HSS OpenAPI<br/>hss.<region>.myhuaweicloud.com]
    cli -- no --> sdk["huaweicloudsdkhss v5<br/>HssClient.list_host_status"]

    api --> resp{response}
    resp -- success --> hosts[data_list: host list]
    resp -- 403 / error_code --> err[classify failure:<br/>AuthError / ApiError / ConfigError]

    sdk --> hosts

    hosts --> out{output mode}
    out -- default --> table[full-field table]
    out -- --json --> json_out[raw JSON]
    out -- --names-only --> names[host name list]
    err --> msg[explicit Chinese error hint]
```

## Execution modes

1. **Read-only**: the only API invoked is `ListHostStatus` (a GET). A
   write-intent guard scans all arguments and rejects create/delete/update/
   install/isolate intents before any command runs.
2. **CLI-first, SDK fallback**: KooCLI is the primary path; when the `hcloud`
   binary is missing the script switches to the official `huaweicloudsdkhss`
   v5 SDK (`HssClient.list_host_status`).
3. **Offset paging**: pages through all servers using `--limit` (10–200) and
   `--offset` (0–2,000,000), stopping at `total_num`.