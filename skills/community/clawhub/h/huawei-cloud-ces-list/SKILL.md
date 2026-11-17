---
name: huawei-cloud-ces-list
description: |
  查询华为云 CES（云监控服务）监控指标列表与指标数据。支持指标列表查询（ListMetrics）
  按命名空间/指标名/维度/排序过滤，以及指标数据查询（ShowMetricData）按时间范围、
  聚合粒度、聚合方式获取监控数据点。只读操作，JSON 输出全部字段，AK/SK 环境变量认证。
version: 1.0.0
triggers:
  - 查询华为云CES
  - 列出监控指标
  - CES监控查询
  - 华为云云监控
  - 查看指标数据
tags:
  - huawei-cloud
  - ces
  - monitoring
  - query
  - metrics
tools:
  - hcloud
---

# Huawei Cloud CES 查询 Skill

## 安全硬约束

1. **AK/SK 不写日志/不硬编码**：凭据通过动态扫描环境变量获取（`HUAWEICLOUD_SDK_AK`/`HUAWEICLOUD_SDK_SK` 等任意 `HUAWEI*`/`HW*`/`HWC*` 前缀变量），不写死任何固定变量名，不输出到日志/评论。
2. **超时控制**：所有 hcloud CLI 调用设 30s 超时（`HCLOUD_TIMEOUT=30`），超时判定失败不 hang。
3. **403/401 处理**：鉴权失败时返回明确错误提示（exit 3），不尝试其他 token 或绕行手段。
4. **只读操作**：仅支持 ListMetrics / ShowMetricData（GET），无创建/删除/变更操作，无不可逆风险。
5. **参数校验**：维度格式使用 `key,value` 校验，filter/period/order 使用枚举校验，时间戳范围验证，防注入。

## Overview / 概述

本 skill 用于查询华为云 CES（云监控服务，Cloud Eye Service）监控指标信息，提供两个核心功能：

- **指标列表查询（list）**：查询当前账号下的监控指标列表，支持按命名空间、指标名称、维度、排序方式、分页过滤。
- **指标数据查询（show）**：按指定时间范围、聚合粒度、聚合方式查询单个指标的数据点。

**架构**：用户 → Python 脚本 → hcloud CLI → 华为云 CES API（ListMetrics / ShowMetricData）→ 返回 JSON。

**适用场景**：资源监控巡检、性能数据分析、告警阈值排查、容量规划辅助。

**技术模式**：CLI（hcloud KooCLI 优先）。通过 `--cli-access-key`/`--cli-secret-key` 运行时注入 AK/SK，无需预配置 profile。

## Prerequisites / 前置条件

1. **hcloud CLI**：已安装 KooCLI（版本 ≥ 4.0），安装方法见 `references/cli-installation-guide.md`。
2. **认证配置**：AK/SK 通过环境变量注入（如 `HUAWEICLOUD_SDK_AK` / `HUAWEICLOUD_SDK_SK`），脚本动态扫描 `HUAWEI*`/`HW*`/`HWC*` 前缀的变量。
3. **IAM 权限**：`CES:ces:metrics:list`、`CES:ces:metrics:get`（只读），详见 `references/iam-policies.md`。
4. **Python 3.8+**：运行入口脚本。

## Workflow / 工作流

1. 脚本启动，动态扫描环境变量获取 AK/SK。
2. 校验 AK/SK 非空（缺失 → exit 3，输出 JSON 错误到 stderr）。
3. 解析子命令与参数（list / show / capability-list）。
4. 组装 hcloud CLI 命令，注入 `--cli-access-key`/`--cli-secret-key`。
5. 执行 hcloud 调用（30s 超时）。
6. 解析 JSON 响应，输出到 stdout（全部字段保留）。
7. 错误处理：空指标返回空列表；无效参数返回明确错误；API 失败返回 JSON 错误。

## Core Commands / 核心命令

### 指标列表查询

```bash
# 列出所有监控指标（默认区域 cn-north-4）
python3 scripts/huawei-cloud-ces-list.py list

# 指定区域
python3 scripts/huawei-cloud-ces-list.py list --region cn-east-3

# 按命名空间过滤
python3 scripts/huawei-cloud-ces-list.py list --namespace SYS.ECS

# 按指标名称过滤
python3 scripts/huawei-cloud-ces-list.py list --metric-name cpu_util

# 按维度过滤（key,value 格式）
python3 scripts/huawei-cloud-ces-list.py list --dim.0 instance_id,6f3c6f91-4b24-4e1b-b7d1-a94ac1cb011d

# 按命名空间 + 指标名 + 维度组合过滤
python3 scripts/huawei-cloud-ces-list.py list --namespace SYS.ECS --metric-name cpu_util --dim.0 instance_id,6f3c6f91-4b24-4e1b-b7d1-a94ac1cb011d

# 分页查询（limit + start）
python3 scripts/huawei-cloud-ces-list.py list --limit 100 --start SYS.ECS.cpu_util.instance_id:xxx

# 降序排序
python3 scripts/huawei-cloud-ces-list.py list --order desc --limit 10
```

### 指标数据查询

```bash
# 查询 OBS 桶容量指标数据（1小时聚合）
python3 scripts/huawei-cloud-ces-list.py show \
  --namespace SYS.OBS \
  --metric-name capacity_archive \
  --dim.0 bucket_name,demo-aac \
  --filter average \
  --period 3600 \
  --from 1607146998177 \
  --to 1607150598177

# 指定区域 + 实时数据查询
python3 scripts/huawei-cloud-ces-list.py show \
  --region cn-east-3 \
  --namespace SYS.ECS \
  --metric-name cpu_util \
  --dim.0 instance_id,6f3c6f91-4b24-4e1b-b7d1-a94ac1cb011d \
  --filter average \
  --period 60 \
  --from 1607146998177 \
  --to 1607150598177

# 查询最小值数据（5分钟聚合）
python3 scripts/huawei-cloud-ces-list.py show \
  --namespace SYS.ECS \
  --metric-name mem_usedPercent \
  --dim.0 instance_id,6f3c6f91-4b24-4e1b-b7d1-a94ac1cb011d \
  --filter min \
  --period 300 \
  --from 1607146998177 \
  --to 1607150598177
```

### 能力列表

```bash
# 查看支持的操作
python3 scripts/huawei-cloud-ces-list.py capability-list
```

### 帮助

```bash
python3 scripts/huawei-cloud-ces-list.py --help
python3 scripts/huawei-cloud-ces-list.py list --help
python3 scripts/huawei-cloud-ces-list.py show --help
```

## Parameter Confirmation / 参数确认

| 参数 | 子命令 | 必填 | 默认值 | 说明 |
|------|--------|------|--------|------|
| `--region` | list / show | 否 | cn-north-4 | 区域 ID（如 cn-north-4、cn-east-3） |
| `--namespace` | list | 否 | - | 服务命名空间（如 SYS.ECS、SYS.OBS） |
| `--metric-name` | list | 否 | - | 指标名称（如 cpu_util、capacity_archive） |
| `--dim.0` | list | 否 | - | 第一维度，格式 key,value（如 instance_id,xxx） |
| `--dim.1` ~ `--dim.3` | list | 否 | - | 第二至第四维度，格式 key,value |
| `--order` | list | 否 | asc | 排序方式：asc / desc |
| `--limit` | list | 否 | 1000 | 每页最大返回数（1-1000） |
| `--start` | list | 否 | - | 分页 marker（来自上次响应） |
| `--namespace` | show | 是 | - | 服务命名空间 |
| `--metric-name` | show | 是 | - | 指标名称 |
| `--dim.0` | show | 是 | - | 第一维度，格式 key,value |
| `--dim.1` ~ `--dim.3` | show | 否 | - | 第二至第四维度 |
| `--filter` | show | 是 | - | 聚合方式：average/variance/min/max/sum |
| `--period` | show | 是 | - | 聚合粒度（秒）：1/60/300/1200/3600/14400/86400 |
| `--from` | show | 是 | - | 开始时间（UNIX 毫秒时间戳） |
| `--to` | show | 是 | - | 结束时间（UNIX 毫秒时间戳） |

## KooCLI Command Format Standard

本 skill 通过 hcloud CLI 调用华为云 CES API，命令格式遵循 KooCLI 规范：

```
hcloud CES <Operation> --cli-region=<region> [--params] --cli-access-key=<AK> --cli-secret-key=<SK>
```

| 操作 | hcloud 命令 | HTTP 方法 | API 端点 |
|------|------------|-----------|----------|
| 指标列表 | `hcloud CES ListMetrics` | GET | `/v2/{project_id}/metrics` |
| 指标数据 | `hcloud CES ShowMetricData` | GET | `/v2/{project_id}/metric-data` |

**参数规范**：
- Service 名：`CES`（首字母大写）
- Operation 名：PascalCase（`ListMetrics` / `ShowMetricData`）
- `--cli-region`：必填，指定区域
- `--cli-access-key` / `--cli-secret-key`：运行时注入 AK/SK（不依赖固定 profile）
- `--project_id`：hcloud 自动从认证信息解析，无需手动指定
- `--dim.{i}`：维度参数，格式 `key,value`，最多 4 个（dim.0 ~ dim.3）

**时间戳说明**：
- `--from` / `--to` 均为 UNIX 毫秒时间戳（范围 [1111111111111, 9999999999999]）
- 建议 `--from` 至少比当前时间早一个聚合周期，避免聚合窗口内数据为空

## Reference Documents / 参考文档

- [IAM 权限策略](references/iam-policies.md)
- [hcloud CLI 安装指南](references/cli-installation-guide.md)
- [验证方法](references/verification-method.md)
- [数据流图](references/dataflow-diagram.md)
- [验收标准](references/acceptance-criteria.md)

## 输出格式

所有输出为 JSON：

- **list**：`{"count": N, "total": M, "marker": "...", "metrics": [...]}`（空列表时 count=0, metrics=[]）
- **show**：`{"metric_name": "...", "datapoints": [...]}`（无数据时 datapoints=[]）
- **错误**：`{"error": "消息", "details": "..."}`（输出到 stderr）

**指标字段**（list 返回，API 全部字段保留）：namespace、dimensions、metric_name、unit 等。

**数据点字段**（show 返回）：timestamp、unit、statistics（含 max/min/sum/average/variance）等。

## 退出码

| 退出码 | 含义 |
|--------|------|
| 0 | 成功 |
| 2 | 输入无效（参数错误/维度格式错误） |
| 3 | AK/SK 缺失或无效 |
| 4 | API 调用失败（超时/网络/服务端错误） |
