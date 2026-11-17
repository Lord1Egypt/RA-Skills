# Data Flow Diagram

```mermaid
flowchart TD
    A[User / Agent] -->|"python3 scripts/list_rds.py<br/>--region --json --names-only<br/>--status --name --datastore-type"| B[Write-Intent Guard]
    B -->|"create/delete/update/resize/restart/stop/restore<br/>or operation != ListInstances"| G[GuardError: 拦截写意图<br/>exit 1, 未执行任何命令]
    B -->|read-only| C[build_command:<br/>hcloud RDS ListInstances<br/>--cli-region --limit --offset<br/>+ --name/--datastore_type/--id<br/>（无 --status：API 无此参数）]
    C --> D[subprocess.run hcloud]
    D -->|FileNotFoundError| F1{SDK fallback:<br/>huaweicloudsdkrds<br/>list_instances}
    F1 -->|SDK unavailable| E1[ConfigError: 安装 KooCLI 或 SDK]
    F1 -->|instances| FS[filter_by_status<br/>客户端本地过滤]
    FS --> F
    D -->|"exit != 0"| E2{classify failure}
    E2 -->|"cli-ak / credential"| E3[ConfigError: 缺少 AK/SK]
    E2 -->|"401 / 403 / Forbidden"| E4[AuthError: 无权限访问 RDS，请检查 IAM 权限]
    E2 -->|"other"| E5[ApiError]
    D -->|"[USE_ERROR] ... (exit 0)"| E6[ApiError: hcloud 参数错误<br/>指向 --help]
    D -->|JSON stdout| F2[extract_json / extract_instances<br/>+ filter_by_status 客户端过滤]
    F2 -->|"instances" empty| H["当前区域（x）无 RDS 实例<br/>exit 0"]
    F2 -->|instances| F
    F -->|--names-only| J[实例名称列表]
    F -->|--json| K[原始 JSON 数组]
    F -->|default| L[完整字段表格<br/>名称/ID/状态/引擎/规格/私网IP/可用区]
    F2 -->|"len(batch) >= limit or collected < total_count"| C
```
