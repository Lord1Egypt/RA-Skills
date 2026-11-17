# Data Flow Diagram

```mermaid
flowchart TD
    A[User / Agent] -->|"python3 scripts/list_obs_buckets.py<br/>--region --output table|json|names<br/>--json --names-only --page-size --endpoint"| B[Write-Intent Guard]
    B -->|"create/delete/upload/download/copy/remove/restore/sync/...<br/>or operation != ls"| G[GuardError: 拦截写意图<br/>exit 1, 未执行任何命令]
    B -->|read-only| C["build_command:<br/>hcloud OBS ls<br/>-limit=N -e=obs.&lt;region&gt;.myhuaweicloud.com"]
    C --> D[subprocess.run hcloud]
    D -->|FileNotFoundError| F1{SDK fallback:<br/>huaweicloudsdkobs<br/>ObsClient.list_buckets}
    F1 -->|"SDK / creds unavailable"| E1[ConfigError: 安装 KooCLI 或 SDK / 缺少 AK-SK]
    F1 -->|buckets| F
    D -->|"exit != 0"| E2{classify failure}
    E2 -->|"please set ak, sk and endpoint"| E3[ConfigError: 缺少 AK/SK]
    E2 -->|"InvalidAccessKeyId / 401 / 403 / AccessDenied"| E4[AuthError: 无权限访问 OBS，请检查 IAM 权限]
    E2 -->|"other"| E5[ApiError]
    D -->|"[USE_ERROR] ..."| E6[ApiError: hcloud 参数错误<br/>指向 hcloud OBS ls --help]
    D -->|"stdout (obs:// names)"| F2[parse_cli_buckets<br/>obs://&lt;name&gt; + 可选 date/location]
    F2 -->|"buckets empty"| H["当前账号（Region x）无 OBS 桶<br/>exit 0"]
    F2 -->|buckets| F[normalized bucket records]
    F -->|--names-only| J[桶名称清单]
    F -->|--json| K[结构化 JSON 数组]
    F -->|default| L[对齐表格<br/>name/creation_date/location/storage_class]
```

## Sequence (CLI primary)

```mermaid
sequenceDiagram
    participant U as User
    participant P as list_obs_buckets.py
    participant C as hcloud OBS (obsutil)
    participant O as OBS Service
    U->>P: --region cn-north-4
    P->>P: guard_write_intent + guard_operation
    P->>C: hcloud OBS ls -limit=1000 -e=obs.cn-north-4...
    C->>O: GET / (ListBuckets)
    O-->>C: bucket list
    C-->>P: Bucket number is: N + obs://names
    P-->>U: table / json / names

    alt hcloud missing
        P->>O: ObsClient.list_buckets (SDK)
        O-->>P: buckets
        P-->>U: same output modes
    end
```