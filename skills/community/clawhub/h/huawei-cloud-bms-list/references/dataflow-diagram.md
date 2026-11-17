# Data Flow Diagram

```mermaid
flowchart TD
    A[User / Agent] -->|"python3 scripts/list_bms.py<br/>--region --json --names-only<br/>--name --server-id --status"| B[Write-Intent Guard]
    B -->|"create/delete/update/reboot/rebuild/resize/reinstall/reset/attach/detach/change<br/>or operation != ListBareMetalServers"| G[GuardError: 拦截写意图<br/>exit 1, 未执行任何命令]
    B -->|read-only| C[build_command:<br/>hcloud BMS ListBareMetalServers<br/>--cli-region --limit --offset(page)<br/>+ --name/--status<br/>（无 server-id：API 无此参数）]
    C --> D[subprocess.run hcloud]
    D -->|FileNotFoundError| F1{SDK fallback:<br/>huaweicloudsdkbms<br/>list_bare_metal_servers}
    F1 -->|SDK unavailable| E1[ConfigError: 安装 KooCLI 或 SDK]
    F1 -->|servers| FS[filter_by_server_id<br/>客户端本地过滤]
    FS --> F
    D -->|"exit != 0"| E2{classify failure}
    E2 -->|"cli-ak / credential / profile"| E3[ConfigError: 缺少 AK/SK]
    E2 -->|"401 / 403 / Forbidden"| E4[AuthError: 无权限访问 BMS，请检查 IAM 权限]
    E2 -->|"other"| E5[ApiError]
    D -->|"[USE_ERROR] ... (exit 0)"| E6[ApiError: hcloud 参数错误<br/>指向 --help]
    D -->|JSON stdout| F2[extract_json / extract_servers<br/>+ filter_by_server_id 客户端过滤]
    F2 -->|"servers" empty| H["当前区域（x）无裸金属服务器<br/>exit 0"]
    F2 -->|servers| F
    F -->|--names-only| J[服务器名称列表]
    F -->|--json| K[原始 JSON 数组]
    F -->|default| L[完整字段表格<br/>名称/ID/状态/规格/可用区/IP]
    F2 -->|"len(batch) >= limit or collected < count"| C
```
