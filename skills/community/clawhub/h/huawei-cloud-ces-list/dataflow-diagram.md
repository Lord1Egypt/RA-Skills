# 数据流图

## Skill 请求/响应流程

```mermaid
flowchart TD
    A[用户执行命令] --> B[Python 脚本启动]
    B --> C[动态扫描环境变量获取 AK/SK]
    C --> D{AK/SK 非空?}
    D -->|否| E[输出 JSON 错误到 stderr\n退出码 3]
    D -->|是| F[解析子命令与参数]
    F --> G{子命令类型}
    G -->|list| H[组装 ListMetrics 命令]
    G -->|show| I[组装 ShowMetricData 命令]
    G -->|capability-list| J[输出能力列表 JSON]
    H --> K[执行 hcloud CLI\n注入 --cli-access-key/--cli-secret-key\n30s 超时]
    I --> K
    K --> L{调用成功?}
    L -->|是| M[解析 JSON 响应]
    L -->|超时| N[输出超时错误\n退出码 4]
    L -->|404| O[输出指标不存在错误\n退出码 2]
    L -->|401/403| P[输出认证失败错误\n退出码 3]
    L -->|其他错误| Q[输出 API 错误\n退出码 4]
    M --> R[输出 JSON 到 stdout\n保留全部字段]
    R --> S[退出码 0]
```

## 数据结构

### list 请求 → 响应

```
请求: hcloud CES ListMetrics --cli-region=cn-north-4 [--namespace] [--metric_name] [--dim.0] [--order] [--limit] [--start]
响应: {"count": N, "total": M, "marker": "...", "metrics": [{指标全部字段}, ...]}
```

### show 请求 → 响应

```
请求: hcloud CES ShowMetricData --cli-region=cn-north-4 --namespace=SYS.ECS --metric_name=cpu_util --dim.0=instance_id,xxx --filter=average --period=3600 --from=时间戳 --to=时间戳
响应: {"metric_name": "...", "datapoints": [{数据点全部字段}, ...]}
```

### 指标字段（list 返回，API 全部字段）

- `namespace`：服务命名空间（如 SYS.ECS、SYS.OBS）
- `dimensions`：维度数组（含 name 和 value）
- `metric_name`：指标名称（如 cpu_util）
- `unit`：指标单位（如 Byte、%）

### 数据点字段（show 返回，API 全部字段）

- `timestamp`：数据点时间戳
- `unit`：指标单位
- `statistics`：统计数据（含 max/min/sum/average/variance）
- 其他 API 返回字段
