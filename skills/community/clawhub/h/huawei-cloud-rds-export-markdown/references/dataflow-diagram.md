# Data Flow Diagram

```mermaid
flowchart TD
    A[User / Agent] -->|"python3 scripts/list_rds_export_markdown.py<br/>--region --project_id --output<br/>--name --status"| B[Write-Intent Guard<br/>scrub read-only flag values]
    B -->|"create/delete/update/resize/restart/stop/restore<br/>or operation != ListInstances"| G[GuardError: 拦截写意图<br/>exit 1, 未执行任何命令, 不写文件]
    B -->|read-only| C[build_command:<br/>hcloud RDS ListInstances<br/>--cli-region --limit --offset<br/>+ --cli-project-id/--name/--datastore_type/--id<br/>（无 --status：API 无此参数）]
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
    F2 -->|"len(batch) >= limit or collected < total_count"| C
    F2 --> F[normalize_instance<br/>datastore/private_ips/nodes 展平]
    F --> R[render_markdown<br/>标题 + 表头 + 数据行]
    R -->|instances empty| H["表头 + 空表提示<br/>当前区域无 RDS 实例"]
    R --> W[write_markdown<br/>临时文件 + os.replace 原子落盘]
    H --> W
    W --> O["本地 .md 文件<br/>（默认当前目录 rds_instances.md）"]
```

No branch in this diagram writes to Huawei Cloud: the only cloud call is the
read-only `ListInstances` GET; the `.md` file is produced on the local
filesystem only.