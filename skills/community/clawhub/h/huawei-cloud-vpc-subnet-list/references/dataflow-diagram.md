# Data Flow Diagram

```mermaid
flowchart TD
    A[User / Agent] -->|"python3 scripts/list_subnet.py<br/>--region --json --names-only<br/>--vpc-id"| B[Write-Intent Guard]
    B -->|"create/delete/update/associate/release/change<br/>or operation != ListSubnets"| G[GuardError: 拦截写意图<br/>exit 1, 未执行任何命令]
    B -->|read-only| C[build_command:<br/>hcloud VPC ListSubnets<br/>--cli-region --limit --marker<br/>+ --vpc_id]
    C --> D[subprocess.run hcloud]
    D -->|FileNotFoundError| F1{SDK fallback:<br/>huaweicloudsdkvpc<br/>list_subnets}
    F1 -->|SDK unavailable| E1[ConfigError: 安装 KooCLI 或 SDK]
    F1 -->|subnets| F
    D -->|"exit != 0"| E2{classify failure}
    E2 -->|"cli-ak / credential"| E3[ConfigError: 缺少 AK/SK]
    E2 -->|"401 / 403 / Forbidden"| E4[AuthError: 无权限访问 VPC 子网（Subnet），请检查 IAM 权限]
    E2 -->|"other"| E5[ApiError]
    D -->|"[USE_ERROR] ... (exit 0)"| E6[ApiError: hcloud 参数错误<br/>指向 --help]
    D -->|JSON stdout| F2[extract_json / extract_subnets]
    F2 -->|"subnets empty"| H["当前区域（x）无 VPC 子网（Subnet）<br/>exit 0"]
    F2 -->|subnets| F
    F -->|--names-only| J[子网名称列表]
    F -->|--json| K[原始 JSON 数组]
    F -->|default| L[完整字段表格<br/>id/name/vpc_id/cidr/gateway_ip/status 及其余字段]
    F2 -->|"page_info.next_marker"| C
```