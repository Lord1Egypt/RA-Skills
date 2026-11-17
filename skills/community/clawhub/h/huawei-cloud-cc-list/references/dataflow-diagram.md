# Data Flow Diagram

```mermaid
flowchart TD
    A[User / Agent] -->|"python3 scripts/list_cc.py<br/>--region --json --names-only<br/>--name --status --id"| B[Write-Intent Guard]
    B -->|"create/delete/update/associate/detach/restart<br/>or operation != ListCloudConnections"| G[GuardError: 拦截写意图<br/>exit 1, 未执行任何命令]
    B -->|read-only| C[build_command:<br/>hcloud CC ListCloudConnections<br/>--cli-region --limit --marker<br/>+ --name/--status/--id]
    C --> D[subprocess.run hcloud]
    D -->|FileNotFoundError| F1{SDK fallback:<br/>huaweicloudsdkcc<br/>list_cloud_connections}
    F1 -->|SDK unavailable| E1[ConfigError: 安装 KooCLI 或 SDK]
    F1 -->|cloud_connections| F
    D -->|"exit != 0"| E2{classify failure}
    E2 -->|"cli-ak / credential"| E3[ConfigError: 缺少 AK/SK]
    E2 -->|"401 / 403 / Forbidden"| E4[AuthError: 无权限访问云连接（CC），请检查 IAM 权限]
    E2 -->|"other"| E5[ApiError]
    D -->|"[USE_ERROR] ... (exit 0)"| E6[ApiError: hcloud 参数错误<br/>指向 --help]
    D -->|JSON stdout| F2[extract_json / extract_connections]
    F2 -->|"cloud_connections empty"| H["当前区域（x）无云连接（CC）实例<br/>exit 0"]
    F2 -->|cloud_connections| F
    F -->|--names-only| J[实例名称列表]
    F -->|--json| K[原始 JSON 数组]
    F -->|default| L[完整字段表格<br/>名称/ID/状态/带宽/网络实例数/企业项目]
    F2 -->|"page_info.next_marker"| C
```
