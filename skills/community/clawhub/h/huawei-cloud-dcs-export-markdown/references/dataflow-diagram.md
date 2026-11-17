# Data Flow Diagram

```mermaid
flowchart TD
    A[User / Agent] -->|python3 scripts/list_dcs_export_markdown.py| B{Write-intent guard}
    B -->|mutating intent| X[GuardError → exit 1, no API call]
    B -->|read-only| C{operation == ListInstances?}
    C -->|no| X
    C -->|yes| D[skill-quality-cli run ─▶ hcloud DCS ListInstances --cli-region R --limit --offset + filters]

    D -->|hcloud missing (FileNotFoundError)| E[SDK fallback]
    E --> F[huaweicloudsdkdcs v2 DcsClient.list_instances]
    E -->|SDK missing / no AK-SK / no project_id| Y[ConfigError → exit 1]

    D -->|rc != 0 or USE_ERROR| G[classify_hcloud_failure]
    G --> H[ConfigError / AuthError / ApiError → exit 1]

    D -->|success JSON| I[extract_instances]
    F --> I

    I --> J{instance_num reached?}
    J -->|no| D2[next page: offset += batch]
    J -->|yes| K{--format}

    K -->|md / default| L[normalize_instance → render_markdown]
    L --> M[temp file + atomic rename → .md report, exit 0]
    K -->|table| N[aligned full-field table on stdout]
    K -->|json| O[raw instance array JSON on stdout]
    K -->|empty| P[当前区域无 DCS 实例，未生成 Markdown 文件 hint, exit 0]
```