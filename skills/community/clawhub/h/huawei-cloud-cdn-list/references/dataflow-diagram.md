# Data Flow Diagram

```mermaid
flowchart TD
    A[User / Agent] -->|"python3 scripts/list_cdn.py<br/>--region --json --names-only<br/>--domain-name --domain-status --business-type"| B[Write-Intent Guard]
    B -->|"create/delete/update/enable/disable/refresh<br/>or operation != ListDomains"| G[GuardError: 拦截写意图<br/>exit 1, 未执行任何命令]
    B -->|read-only| C[build_command:<br/>hcloud CDN ListDomains<br/>--cli-region --page_size --page_number<br/>+ --domain_name/--domain_status/--business_type]
    C --> D[subprocess.run hcloud]
    D -->|FileNotFoundError| F1{SDK fallback:<br/>huaweicloudsdkcdn v1<br/>CdnClient.list_domains}
    F1 -->|SDK unavailable| E1[ConfigError: 安装 KooCLI 或 SDK]
    F1 -->|domains| F
    D -->|"exit != 0"| E2{classify failure}
    E2 -->|"cli-ak / credential"| E3[ConfigError: 缺少 AK/SK]
    E2 -->|"401 / 403 / Forbidden"| E4[AuthError: 无权限访问内容分发网络（CDN），请检查 IAM 权限]
    E2 -->|"other"| E5[ApiError]
    D -->|"[USE_ERROR] ... (exit 0)"| E6[ApiError: hcloud 参数错误<br/>指向 --help]
    D -->|JSON stdout| F2[extract_json / extract_domains]
    F2 -->|"domains empty"| H["当前区域（x）无 CDN 加速域名<br/>exit 0"]
    F2 -->|domains| F
    F -->|--names-only| J[加速域名清单]
    F -->|--json| K[原始 JSON 数组]
    F -->|default| L[完整字段表格<br/>域名/状态/CNAME/业务类型]
    F2 -->|"len < total"| C
```