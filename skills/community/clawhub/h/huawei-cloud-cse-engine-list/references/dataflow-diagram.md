# Data Flow Diagram

```mermaid
flowchart TD
    A[User / Agent] -->|"python3 scripts/list_cse_engines.py<br/>--region --type --name/--fuzzy<br/>--table | --json"| B[Write-Intent Guard<br/>scan flag names + operation<br/>selector values excluded]
    B -->|"create/delete/update/upgrade/<br/>modify/start/stop/resize ..."| G[GuardError: 拦截写意图<br/>exit 1, 未执行任何命令]
    B -->|read-only| C[build_command:<br/>hcloud CSE ListEngines<br/>--cli-region --limit --offset --type]
    C --> D[subprocess.run hcloud]
    D -->|FileNotFoundError| F1{SDK fallback:<br/>huaweicloudsdkcse.v1<br/>CseClient.list_engines}
    F1 -->|SDK unavailable| E1[ConfigError: 安装 KooCLI 或 SDK]
    F1 -->|items| F
    D -->|"exit != 0"| E2{classify failure}
    E2 -->|"cli-ak / credential / profile"| E3[ConfigError: 缺少 AK/SK]
    E2 -->|"401 / 403 / not authorized /<br/>cse:engine:list"| E4[AuthError: 无权限访问 CSE，请检查 IAM 权限]
    E2 -->|"timeout / connection"| E5[ApiError: 网络异常]
    E2 -->|"other"| E6[ApiError]
    D -->|"[USE_ERROR] ... (exit 0)"| E7[ApiError: hcloud 参数错误<br/>指向 CSE ListEngines --help]
    D -->|"JSON stdout"| J1[extract_json]
    J1 -->|"error_code / error_message"| E8{error body with rc=0}
    E8 -->|"auth / credential"| E4
    E8 -->|other| E6
    J1 -->|"{\"total\",\"data\"} or bare array"| F2[extract_engines<br/>normalize camelCase/snake_case<br/>fill region, missing -> '-']
    F2 -->|"has_more (total / full page)"| C
    F2 -->|"client-side --name exact / --fuzzy"| F
    F -->|"items empty"| H["未找到微服务引擎<br/>exit 0"]
    F -->|items| F3{output mode}
    F3 -->|--json| K[归一化 JSON 数组]
    F3 -->|--table| L[完整字段表格<br/>名称/ID/类型/版本/状态/规格/实例数/创建时间/region]
    F3 -->|default| M[简洁清单]
```