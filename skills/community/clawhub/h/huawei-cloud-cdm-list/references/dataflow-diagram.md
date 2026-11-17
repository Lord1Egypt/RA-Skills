# Data Flow — huawei-cloud-cdm-list

```mermaid
flowchart TD
    A[Agent / user] -->|python3 scripts/list_cdm_clusters.py| B[Argument parse + write-intent guard]
    B -->|mutating intent| Z[GuardError, exit 1 — nothing executed]
    B -->|read-only| C{Operation}
    C -->|default / --name / --status| D[ListClusters]
    C -->|--cluster-id| E[ShowClusterDetail]

    D --> F{hcloud available?}
    E --> F

    F -->|yes| G[skill-quality-cli run -- hcloud CDM Op --cli-region=...]
    G --> H[Huawei Cloud CDM OpenAPI]
    F -->|no| I[huaweicloudsdkcdm v1 CdmClient — BasicCredentials, project_id auto-resolved via IAM]
    I --> H

    H --> J[JSON response / error envelope]
    J -->|error envelope on stdout rc=0| K[classify: ConfigError / AuthError / ApiError, exit 1]
    J -->|ok| L[client-side --name / --status filter]
    L --> M{Render}
    M -->|table| N[stdout aligned table — list view or detail field/value view]
    M -->|json / markdown / csv| O[local file via temp + atomic rename]
```

Read-only guarantee: no branch constructs a mutating CDM operation (the only
argv ever built are `ListClusters` and `ShowClusterDetail`, both GET), and the
export writes only to the local filesystem.
