# Data Flow Diagram

```mermaid
flowchart TD
    A[User / Agent] -->|"python3 scripts/list_ecs_export_sorted.py<br/>--region --format xlsx|csv|json|table<br/>--sort-by FIELD --order asc|desc<br/>--output --summary --status --name --page-size"| B[Write-Intent Guard]
    B -->|"create/delete/update/reboot/resize/start/stop/...<br/>or operation != ListServersDetails"| G[GuardError: 拦截写意图<br/>exit 1, 未执行任何命令]
    B -->|read-only (filter/sort/output values excluded)| C["build_command:<br/>hcloud ECS ListServersDetails<br/>--cli-region=R --limit=N --offset=O [--status --name]"]
    C --> D[subprocess.run hcloud]
    D -->|FileNotFoundError| F1{SDK fallback:<br/>huaweicloudsdkecs<br/>EcsClient.list_servers_details}
    F1 -->|"SDK / creds unavailable"| E1[ConfigError: 安装 KooCLI 或 ensure_env.py / 缺少 AK-SK]
    F1 -->|servers| F
    D -->|"exit != 0"| E2{classify failure}
    E2 -->|"cli-ak empty / no AK"| E3[ConfigError: 缺少 AK/SK]
    E2 -->|"401 / 403 / ApiGW.0301 / Unauthorized"| E4[AuthError: 无权限访问 ECS，请检查 IAM 权限]
    E2 -->|"other"| E5[ApiError]
    D -->|"[USE_ERROR] ..."| E6[ApiError: hcloud 参数错误<br/>指向 hcloud ECS ListServersDetails --help]
    D -->|"stdout JSON {servers, count}"| F2[extract_json / extract_servers<br/>offset paging until count]
    F2 -->|"servers empty"| H["当前区域（R）无 ECS 实例，未生成报表文件<br/>exit 0"]
    F2 -->|servers| N[normalize_server<br/>flavor/vcpus/ram/AZ/IPs/created]
    N --> S{"resolve_sort_field + sort_servers<br/>--sort-by FIELD --order asc|desc"}
    S -->|"unknown field"| SE[SortError: 未知的排序字段<br/>exit 1, 未执行查询]
    S -->|"--sort-by omitted"| SO[preserve query order]
    S -->|"sorted (invalid values last)"| F[normalized server records]
    F -->|--format json| K[结构化 JSON 数组]
    F -->|--format table| L[对齐表格<br/>name/id/status/flavor/vcpus/ram/AZ/privateIps/publicIps/created]
    F -->|"--format xlsx (默认)"| X1{export_xlsx via openpyxl}
    F -->|--format csv| C1{export_csv utf-8-sig}
    X1 -->|openpyxl missing| X2[ExportError: 提示运行 ensure_env.py<br/>exit 1, 无文件]
    X1 -->|bad output path| X3[ExportError: 写出失败<br/>清理临时文件 exit 1]
    X1 -->|ok| X4[.xlsx: 表头 + 数据行 + 可选汇总行<br/>本地文件, 绝不写回云端]
    C1 -->|ok| C2[.csv: UTF-8 BOM 表头 + 数据行 + 可选汇总行<br/>本地文件, 绝不写回云端]
```

## Sequence (CLI primary)

```mermaid
sequenceDiagram
    participant U as User
    participant P as list_ecs_export_sorted.py
    participant C as hcloud ECS
    participant O as ECS OpenAPI
    participant E as export_report (openpyxl / csv)
    U->>P: --region cn-north-4 --sort-by created --order desc --output /tmp/ecs.xlsx
    P->>P: guard_write_intent + guard_operation + resolve_sort_field
    P->>C: hcloud ECS ListServersDetails --cli-region=cn-north-4 --limit=100 --offset=0
    C->>O: GET /v1/{project_id}/cloudservers/detail
    O-->>C: {servers: [...], count: N}
    C-->>P: JSON payload (paged until count reached)
    P->>P: normalize + local sort (created, desc; invalid last)
    P->>E: export_xlsx(sorted, /tmp/ecs.xlsx, summary=True, region)
    E-->>P: written path
    P-->>U: 已生成 ECS 实例列表 XLSX 报表：/tmp/ecs.xlsx

    alt hcloud missing
        P->>O: EcsClient.list_servers_details (SDK)
        O-->>P: servers → normalize → local sort
        P-->>U: same output modes
    end
    alt empty list
        P-->>U: 无 ECS 实例，未生成报表文件 (exit 0, no file)
    end
```