# Data Flow Diagram

```mermaid
flowchart TD
    A[User / Agent] -->|python3 scripts/list_dws.py| B{Write-intent guard}
    B -->|mutating intent| X[GuardError → exit 1, no API call]
    B -->|read-only| C{operation == ListClusters?}
    C -->|no| X
    C -->|yes| D[hcloud DWS ListClusters --cli-region R + eps?]

    D -->|hcloud missing (FileNotFoundError)| E[SDK fallback]
    E --> F[huaweicloudsdkdws v2 DwsClient.list_clusters]
    E -->|SDK missing / no AK-SK| Y[ConfigError → exit 1]

    D -->|rc != 0 or USE_ERROR| G[classify_hcloud_failure]
    G --> H[ConfigError / AuthError / ApiError → exit 1]

    D -->|success JSON| I[extract_clusters]
    F --> I

    I --> J[filter_clusters: name / status / cluster_id]
    J --> K[paginate: offset / limit]
    K --> L{Output mode}
    L -->|--json| M[raw cluster array JSON]
    L -->|--names-only| N[compact name list]
    L -->|default| O[full-field table]
    L -->|empty| P[当前区域无 DWS 集群 hint]
```