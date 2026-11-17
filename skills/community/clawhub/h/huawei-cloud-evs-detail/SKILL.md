---
name: huawei-cloud-evs-detail
version: 1.0.0
description: 查询华为云 EVS 磁盘列表及监控指标（IOPS/吞吐量/延迟）的只读 Skill，基于 Huawei Cloud KooCLI
tags:
  - huawei-cloud
  - evs
  - storage
  - query
  - monitor
triggers:
  - 查询华为云EVS磁盘
  - 列出EVS磁盘
  - EVS磁盘监控
  - EVS磁盘IOPS
  - EVS查询
---

# huawei-cloud-evs-detail

华为云 EVS（弹性卷服务）详情查询 Skill，支持查询当前账号 cn-north-4 下所有云硬盘列表及监控指标（IOPS/吞吐量/延迟）。

## 安全硬约束

1. **凭据管理**：AK/SK 通过 hcloud CLI 的 `configure` 命令管理，或通过环境变量动态加载，禁止硬编码在任何脚本或配置文件中。
2. **只读操作**：本 Skill 仅执行只读查询（ListVolumes / ShowMetricData），不执行任何创建、修改、删除操作。
3. **超时控制**：所有 CLI 调用均设 30 秒超时。
4. **错误处理**：CLI 调用失败时需输出明确错误信息（含错误码和错误消息），不静默崩溃。
5. **日志安全**：凭据信息不得写入日志或输出。

## 概述

本 Skill 封装了华为云 EVS 和 CES（Cloud Eye）服务的只读 CLI 命令，提供两组核心功能：

- **磁盘列表查询**：列出当前账号 cn-north-4 下所有 EVS 云硬盘，包含 ID、名称、状态、容量、挂载信息
- **监控指标查询**：查询指定 EVS 磁盘的 IOPS（读写）、吞吐量（读写）、延迟（I/O服务时间）等监控指标

## 前置条件

### 1. hcloud CLI 安装与配置

需要安装华为云 KooCLI（hcloud）并配置 AK/SK 凭证。详细安装指南见 references/cli-installation-guide.md。

### 2. Python 环境

Python 3.6+（用于包装脚本）

### 3. IAM 权限

需要以下 IAM 权限策略：
- evs:volumes:list
- ces:metrics:list
- ces:metricData:list

详见 references/iam-policies.md。

## 工作流

1. 解析用户输入 -> 识别意图（list 或 metrics）
2. 执行 CLI 命令
3. 格式化输出
4. 错误处理

## 核心命令

### 列出所有 EVS 磁盘
python3 scripts/huawei_cloud_evs_detail.py list

### 查询监控指标
python3 scripts/huawei_cloud_evs_detail.py metrics <disk-id>

### 查看能力列表
python3 scripts/huawei_cloud_evs_detail.py capability-list

## Koo CLI Command Format

| 操作 | 命令 |
|------|------|
| 列出 EVS 磁盘 | hcloud EVS ListVolumes --cli-region=cn-north-4 [--limit=N] |
| 查监控指标 | hcloud CES ShowMetricData --cli-region=cn-north-4 --namespace=SYS.EVS --metric_name=X --dim.0=instance_id,<id> --filter=average --period=3600 --from=T --to=T |

## EVS 监控指标映射

| 指标名 | 说明 | 单位 |
|--------|------|------|
| disk_device_read_requests_rate | 读 IOPS | count/s |
| disk_device_write_requests_rate | 写 IOPS | count/s |
| disk_device_read_bytes_rate | 读吞吐量 | bytes/s |
| disk_device_write_bytes_rate | 写吞吐量 | bytes/s |
| disk_device_service_time | I/O 服务时间（延迟） | ms |

## KooCLI Command Format Standard

本 Skill 使用 CLI 模式，通过 hcloud 命令直接调用华为云 API：

| 操作 | 命令 |
|------|------|
| 列出 EVS 磁盘 | `hcloud EVS ListVolumes --cli-region=cn-north-4 [--limit=N]` |
| 查监控指标 | `hcloud CES ShowMetricData --cli-region=cn-north-4 --namespace=SYS.EVS --metric_name=X --dim.0=instance_id,<id> --filter=average --period=3600 --from=T --to=T` |

## 参数确认

| 参数 | 说明 | 默认值 | 是否可配置 |
|------|------|--------|-----------|
| `region` | 华为云区域 | `cn-north-4` | 是（通过 `--region` 覆写） |
| `--timeout` | CLI 调用超时秒数 | `30` | 是 |
| `--period` | 监控数据粒度（秒） | `3600` | 是 |

## 参考文档

- references/iam-policies.md
- references/cli-installation-guide.md
- references/verification-method.md
- references/acceptance-criteria.md
- references/dataflow-diagram.md
