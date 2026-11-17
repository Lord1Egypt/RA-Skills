# Data Flow Diagram

```mermaid
flowchart TD
    A[User / Agent] -->|python3 scripts/list_gaussdb.py| B{Write-intent guard}
    B -->|mutating intent| X[GuardError → exit 1, no API call]
    B -->|read-only| C{operation == ListGaussMySqlInstances?}
    C -->|no| X
    C -->|yes| D[hcloud GaussDB ListGaussMySqlInstances --cli-region R --limit --offset + filters?]

    D -->|hcloud missing (FileNotFoundError)| E[SDK fallback]
    E --> F[huaweicloudsdkgaussdb v3 GaussDBClient.list_gauss_my_sql_instances]
    E -->|SDK missing / no AK-SK / no project_id| Y[ConfigError → exit 1]

    D -->|rc != 0 or USE_ERROR| G[classify_hcloud_failure]
    G --> H[ConfigError / AuthError / ApiError → exit 1]

    D -->|success JSON| I[extract_instances]
    F --> I

    I --> J{total_count reached?}
    J -->|no| D2[next page: offset += batch]
    J -->|yes| S{Local --status filter}
    S --> K{Output mode}
    K -->|default / --table| O[aligned table: 名称/ID/状态/引擎版本/规格/存储/区域/创建时间 ...]
    K -->|--json| M[raw instance array JSON]
    K -->|empty| P[当前区域无 GaussDB 实例 hint, exit 0]
```