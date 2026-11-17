# Data Flow Diagram

```mermaid
flowchart TD
    A[User / Agent] -->|python3 scripts/list_dcs.py| B{Write-intent guard}
    B -->|mutating intent| X[GuardError → exit 1, no API call]
    B -->|read-only| C{operation == ListInstances?}
    C -->|no| X
    C -->|yes| D[hcloud DCS ListInstances --cli-region R --limit --offset + filters?]

    D -->|hcloud missing (FileNotFoundError)| E[SDK fallback]
    E --> F[huaweicloudsdkdcs v2 DcsClient.list_instances]
    E -->|SDK missing / no AK-SK / no project_id| Y[ConfigError → exit 1]

    D -->|rc != 0 or USE_ERROR| G[classify_hcloud_failure]
    G --> H[ConfigError / AuthError / ApiError → exit 1]

    D -->|success JSON| I[extract_instances]
    F --> I

    I --> J{instance_num reached?}
    J -->|no| D2[next page: offset += batch]
    J -->|yes| K{Output mode}
    K -->|--names-only / default| N[compact instance-name list]
    K -->|--json| M[raw instance array JSON]
    K -->|--table| O[full-field table: 名称/ID/引擎/容量/状态/连接地址/端口]
    K -->|--md / --format md| Q[Markdown table: fixed 10 columns, `-` for missing, pipe/newline escaped]
    Q -->|--md-output path| R[temp file + atomic rename → .md file, content == stdout]
    K -->|empty| P[当前区域无 DCS 实例 hint, exit 0, no header / no file]
```
