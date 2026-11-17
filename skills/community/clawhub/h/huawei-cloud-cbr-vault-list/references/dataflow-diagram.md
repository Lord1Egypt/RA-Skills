# Data Flow Diagram

```mermaid
flowchart TD
    A[User / Agent] -->|"python3 scripts/list_cbr_vaults.py<br/>--region --json|--names-only<br/>--name --status --object-type --protect-type<br/>--enterprise-project-id --vault-id --page-size"| B[Write-Intent Guard]
    B -->|"create/delete/update/modify/restore/copy/import<br/>replicate/migrate/bind/associate/add/remove ...<br/>or operation != ListVault"| G[GuardError: 拦截写意图<br/>exit 1, 未执行任何命令]
    B -->|read-only| C["build_command:<br/>hcloud CBR ListVault<br/>--cli-region=&lt;region&gt; --limit=N --offset=M<br/>[--name --status --object_type ... --id.1=&lt;vault_id&gt;]"]
    C --> D[subprocess.run hcloud]
    D -->|FileNotFoundError| F1{SDK fallback:<br/>huaweicloudsdkcbr<br/>CbrClient.list_vault}
    F1 -->|"SDK / creds unavailable"| E1[ConfigError: 安装 KooCLI 或 SDK / 缺少 AK-SK]
    F1 -->|vaults + count| F
    D -->|"exit != 0"| E2{classify failure}
    E2 -->|"credential / configure"| E3[ConfigError: 缺少 AK/SK]
    E2 -->|"401 / 403 / Forbidden"| E4[AuthError: 无权限访问 CBR，请检查 IAM 权限]
    E2 -->|"other"| E5[ApiError]
    D -->|"[USE_ERROR] ..."| E6[ApiError: hcloud 参数错误<br/>指向 hcloud CBR ListVault --help]
    D -->|"stdout (error_code/error_msg, rc=0)"| E7[AuthError / ApiError]
    D -->|"stdout (JSON vaults[])"| F2[extract_vaults<br/>paging by count / full page<br/>duplicate-ID guard]
    F2 -->|"vaults empty"| H["当前区域（x）无 CBR 存储库<br/>exit 0"]
    F2 -->|vaults| F[normalized vault records]
    F -->|"client-side --name/--status/--object-type<br/>--protect-type/--enterprise-project-id/--vault-id"| F3[filter_vaults]
    F3 -->|--names-only| J[名称+ID+计费模式 清单]
    F3 -->|--json| K[原始结构化 JSON 数组]
    F3 -->|default| L[对齐表<br/>name/id/status/size/used/allocated/charging_mode/<br/>object_type/protect_type/...]
```

## Sequence (CLI primary)

```mermaid
sequenceDiagram
    participant U as User
    participant P as list_cbr_vaults.py
    participant C as hcloud CBR
    participant O as CBR Service
    U->>P: --region cn-north-4
    P->>P: guard_write_intent + guard_operation
    P->>C: hcloud CBR ListVault --cli-region=cn-north-4 --limit=100 --offset=0/…
    C->>O: GET /v3/{project_id}/vaults
    O-->>C: vaults[] + count
    C-->>P: JSON
    P->>P: filter_vaults (name/status/object_type/protect_type/eps/vault_id)
    P-->>U: table / json / names

    alt hcloud missing
        P->>O: CbrClient.list_vault (SDK)
        O-->>P: vaults + count
        P-->>U: same output modes
    end
```