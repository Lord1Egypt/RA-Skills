# Data Flow Diagram

```mermaid
flowchart TD
    A[User / Agent] -->|"python3 scripts/list_vpcep.py<br/>--view endpoint|service|public<br/>--region --name --fuzzy --id<br/>--vpc-id --service-name --status<br/>--table --json --format md"| B[Write-Intent Guard<br/>before argparse]
    B -->|"create/delete/update/batch/whitelist<br/>accept/reject/bind/unbind<br/>or non-list operation"| G[GuardError: 拦截写意图<br/>exit 1, 未执行任何命令]
    B -->|read-only| C{"resolve view → operation<br/>build_command with<br/>--cli-region --limit --offset<br/>+ endpoint_service_name/id/vpc_id/status/sort"}
    C --> D[subprocess.run hcloud]
    D -->|FileNotFoundError| F1{"SDK fallback:<br/>huaweicloudsdkvpcep<br/>list_endpoints / list_endpoint_service /<br/>list_service_public_details"}
    F1 -->|SDK unavailable| E1[ConfigError: 安装 KooCLI 或 SDK]
    F1 -->|items| F
    D -->|"exit != 0"| E2{classify failure}
    D -->|"JSON error_code (KooCLI exit 0)"| E7{classify API error body}
    E7 -->|"not authorized / no identity-based policy"| E4
    E7 -->|"invalid id / not found"| E8[InvalidRequestError: 参数或资源 ID 无效]
    E7 -->|other| E5[ApiError]
    E2 -->|"cli-ak / credential"| E3[ConfigError: 缺少 AK/SK]
    E2 -->|"401 / 403 / Forbidden"| E4[AuthError: 无权限访问终端节点服务（VPCEP）<br/>请检查 IAM 权限]
    E2 -->|other| E5
    D -->|"[USE_ERROR] ... (exit 0)"| E6[ApiError: hcloud 参数错误<br/>指向 --help]
    D -->|JSON stdout| F2[extract_json / extract_items]
    F2 -->|"len(batch) < limit or total_count reached"| F
    F2 -->|"full page"| F3["offset += limit"] --> C
    F2 -->|empty| H["当前区域（x）无 VPCEP <view><br/>exit 0"]
    F[client-side filters<br/>--name exact / --fuzzy substring<br/>--id --vpc-id --service-name --status] --> R{output mode}
    R -->|default| J[简洁列表<br/>AVAILABLE 与非 AVAILABLE 分区]
    R -->|--table| K[固定列表格<br/>[异常] 状态标注]
    R -->|--json| L[原始 JSON 数组]
    R -->|--format md| M[Markdown 报告<br/>原子写盘, 缺字段 '-']
```
