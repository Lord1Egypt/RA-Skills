# Data Flow Diagram

```mermaid
flowchart TD
    A[User / Agent] -->|"python3 scripts/list_sfs.py<br/>--region --json|--names-only|--count-only<br/>--name --id --status --share-proto --az --page-size"| B[Write-Intent Guard]
    B -->|"create/delete/expand/shrink/resize/mount/unmount/attach/detach/restore/...<br/>or operation != ListShares"| G[GuardError: 拦截写意图<br/>exit 1, 未执行任何命令]
    B -->|read-only| C["build_command:<br/>hcloud SFSTurbo ListShares<br/>--cli-region=&lt;region&gt; --limit=N --offset=M"]
    C --> D[subprocess.run hcloud]
    D -->|FileNotFoundError| F1{SDK fallback:<br/>huaweicloudsdksfsturbo<br/>SFSTurboClient.list_shares}
    F1 -->|"SDK / creds unavailable"| E1[ConfigError: 安装 KooCLI 或 SDK / 缺少 AK-SK]
    F1 -->|shares + count| F
    D -->|"exit != 0"| E2{classify failure}
    E2 -->|"credential / configure"| E3[ConfigError: 缺少 AK/SK]
    E2 -->|"401 / 403 / Forbidden"| E4[AuthError: 无权限访问 SFS，请检查 IAM 权限]
    E2 -->|"other"| E5[ApiError]
    D -->|"[USE_ERROR] ..."| E6[ApiError: hcloud 参数错误<br/>指向 hcloud SFSTurbo ListShares --help]
    D -->|"stdout (JSON shares[])"| F2[extract_shares<br/>paging by count / full page]
    F2 -->|"shares empty"| H["当前区域（x）无 SFS 文件系统<br/>exit 0"]
    F2 -->|shares| F[normalized file-system records]
    F -->|"client-side --name/--id/--status/--share-proto/--az"| F3[filter_shares]
    F3 -->|--count-only| N[数量]
    F3 -->|--names-only| J[名称+ID 清单]
    F3 -->|--json| K[结构化 JSON 数组]
    F3 -->|default| L[对齐表<br/>name/id/status/share_proto/size/availability_zone/...]
```

## Sequence (CLI primary)

```mermaid
sequenceDiagram
    participant U as User
    participant P as list_sfs.py
    participant C as hcloud SFSTurbo
    participant O as SFS Service
    U->>P: --region cn-north-4
    P->>P: guard_write_intent + guard_operation
    P->>C: hcloud SFSTurbo ListShares --cli-region=cn-north-4 --limit=200 --offset=0/…
    C->>O: GET /v1/{project_id}/sfs-turbo/shares/detail
    O-->>C: shares[] + count
    C-->>P: JSON
    P->>P: filter_shares (name/id/status/proto/az)
    P-->>U: table / json / names / count

    alt hcloud missing
        P->>O: SFSTurboClient.list_shares (SDK)
        O-->>P: shares + count
        P-->>U: same output modes
    end
```