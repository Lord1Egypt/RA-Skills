# Data Flow Diagram

```mermaid
flowchart TD
    A["User / Agent<br/>python3 scripts/list_er.py<br/>--resource er|attachment|route-table|detail<br/>--region --table --json --name --fuzzy<br/>--er-id --state --vpc-id ..."] --> B[Write-Intent Guard]
    B -->|"create/delete/update/associate/disassociate/enable/disable<br/>or operation not whitelisted for the resource"| G["GuardError: 拦截写意图<br/>exit 1, 未执行任何命令"]
    B -->|read-only| C{resource}
    C -->|er| C1["build_er_command:<br/>hcloud ER ListEnterpriseRouters<br/>--cli-region --limit --marker<br/>--state.1 --id.1 --owned_by_self<br/>--enterprise_project_id.1 --sort_key.1 --sort_dir.1"]
    C -->|attachment| C2["build_attachment_command:<br/>hcloud ER ListVpcAttachments<br/>--er_id --limit --marker<br/>--state.1 --vpc_id.1"]
    C -->|route-table| C3["build_route_table_command:<br/>hcloud ER ListRouteTables<br/>--er_id --limit --marker<br/>--state.1 --is_default_association_table<br/>--is_default_propagation_table"]
    C -->|detail| C4["build_detail_command:<br/>hcloud ER ShowEnterpriseRouter --er_id"]
    C1 --> D[subprocess.run hcloud]
    C2 --> D
    C3 --> D
    C4 --> D
    D -->|FileNotFoundError| F1{"SDK fallback:<br/>huaweicloudsdker v3<br/>ErClient"}
    F1 -->|SDK unavailable| E1["ConfigError: 安装 KooCLI 或 SDK"]
    F1 -->|records / instance| F
    D -->|"exit != 0"| E2{classify failure}
    D -->|"JSON error body with exit 0<br/>(common.01010013 / SYS.0404)"| E2
    E2 -->|"cli-ak / credential"| E3[ConfigError: 缺少 AK/SK]
    E2 -->|"401/403/not authorized"| E4["AuthError: 无权限访问企业路由器（ER）"]
    E2 -->|"404/not found"| E5["NotFoundError: 未找到企业路由器"]
    E2 -->|"other"| E6[ApiError]
    D -->|"[USE_ERROR] ... (exit 0)"| E7["ApiError: hcloud 参数错误<br/>指向 --help"]
    D -->|"JSON stdout"| F2["extract_json / extract_items<br/>page_info.next_marker"]
    F2 -->|"page_info.next_marker"| C
    F2 -->|"empty list"| H["无企业路由器（ER） / 无 VPC 连接 / 无路由表<br/>exit 0"]
    F2 --> F["apply_local_filters<br/>--name / --fuzzy"]
    F -->|"--json"| J["原始 JSON 数组 / 详情对象"]
    F -->|"--table"| K["固定列表格<br/>ER 8 列 / 连接 6 列 / 路由表 6 列"]
    F -->|default| L["简洁列表"])
    K -->|"state != available"| M["[!] 非 available 单独成段<br/>[异常] 醒目标注"]
    L -->|"state != available"| M
```