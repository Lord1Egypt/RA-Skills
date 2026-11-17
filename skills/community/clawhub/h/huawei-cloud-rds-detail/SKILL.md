---
name: huawei-cloud-rds-detail
version: 1.0.0
description: 查询华为云 RDS 实例列表、实例详情及监控指标（CPU/内存/磁盘）的只读 Skill，基于 Huawei Cloud SDK
tags:
  - huawei-cloud
  - rds
  - database
  - query
  - monitor
triggers:
  - 查询华为云RDS实例
  - 列出RDS实例
  - RDS实例详情
  - RDS监控指标
  - RDS查询
---

# huawei-cloud-rds-detail

华为云 RDS 详情查询 Skill，支持查询当前账号下所有 RDS 实例列表、按实例 ID 查询单实例详情，以及查询实例的 CPU/内存/磁盘监控指标。

## 安全硬约束

1. **凭据管理**：AK/SK 通过环境变量 `HUAWEICLOUD_SDK_AK` / `HUAWEICLOUD_SDK_SK` 获取，或通过项目知识配置动态加载，禁止硬编码在任何脚本或配置文件中。
2. **只读操作**：本 Skill 仅执行只读查询（List / Show / BatchListMetricData），不执行任何创建、修改、删除操作。
3. **超时控制**：所有 API 调用均设 30 秒超时。
4. **错误处理**：API 调用失败时需输出明确错误信息（含错误码和错误消息），不静默崩溃。
5. **日志安全**：凭据信息不得写入日志或输出。

## 概述

本 Skill 封装了华为云 RDS 和 CES（Cloud Eye）服务的只读 API，提供三组核心功能：

- **实例列表查询**：列出当前账号下所有 RDS 实例的基本信息
- **实例详情查询**：按实例 ID 查询单实例的完整规格、状态、连接信息
- **监控指标查询**：查询指定实例的 CPU 使用率、内存使用率、磁盘使用率等监控指标

### 架构

```
用户 → huawei-cloud-rds-detail (Python SDK) → Huawei Cloud RDS API / CES API → 返回 JSON 数据
```

### 适用场景

- 日常巡检：快速查看所有 RDS 实例运行状态
- 故障排查：查询特定实例的详细配置和监控指标
- 资源管理：了解当前账号下的 RDS 资源分布

## 前置条件

### 1. Python 环境

Python 3.8+，安装依赖：

```bash
pip install huaweicloudsdkrds huaweicloudsdkces huaweicloudsdkiam
```

### 2. 华为云凭证

需要有效的华为云 AK/SK 凭证，通过以下方式提供：

| 方式 | 说明 |
|------|------|
| 环境变量 | `HUAWEICLOUD_SDK_AK` / `HUAWEICLOUD_SDK_SK` |
| 项目知识配置 | `.project-info/` 目录下 JSON 配置文件的 `secrets.HUAWEI_AK` / `secrets.HUAWEI_SK` |

### 3. IAM 权限

需要以下 IAM 权限策略：

```json
{
  "Version": "1.1",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "rds:instance:list",
        "ces:metrics:list",
        "ces:metricData:list"
      ]
    }
  ]
}
```

详见 `references/iam-policies.md`。

## 工作流

```
1. 加载凭据 ──→ 从环境变量或项目知识获取 AK/SK
2. 初始化客户端 ──→ 创建 RdsClient / CesClient（区域：cn-north-4）
3. 执行操作 ──→ list / show / metrics 子命令
4. 格式化输出 ──→ 输出 JSON ���式结果
5. 错误处理 ──→ API 异常时输出错误信息并退出码 1
```

## 核心命令

### 列出所有 RDS 实例

```bash
python3 scripts/huawei_cloud_rds_detail.py list
```

### 查询单实例详情

```bash
python3 scripts/huawei_cloud_rds_detail.py show <instance-id>
```

### 查询监控指标（CPU/内存/磁盘）

```bash
python3 scripts/huawei_cloud_rds_detail.py metrics <instance-id>
```

### 查看能力列表

```bash
python3 scripts/huawei_cloud_rds_detail.py capability-list
```

## KooCLI Command Format Standard

本 Skill 使用 SDK 模式（非 CLI 模式），因此不使用 KooCLI 命令格式。通过 Python SDK 直接调用华为云 API。
所有操作均通过 `scripts/huawei_cloud_rds_detail.py` 脚本执行，支持的子命令见「核心命令」章节。

## 参数确认

| 参数 | 说明 | 默认值 | 是否可配置 |
|------|------|--------|-----------|
| `region` | 华为云区域 | `cn-north-4` | 是（可通过 `--region` 覆写） |
| `--timeout` | API 超时秒数 | `30` | 是 |
| `--project-id` | 项目 ID | 自动获取 | 否（自动获取） |

## 参考文档

- `references/iam-policies.md` — IAM 权限策略配置
- `references/verification-method.md` — 验证方法
- `references/acceptance-criteria.md` — 验收标准
- `references/dataflow-diagram.md` — 数据流图
- [华为云 RDS API 文档](https://console.huaweicloud.com/apiexplorer/#/openapi/RDS/doc)
- [华为云 CES API 文档](https://console.huaweicloud.com/apiexplorer/#/openapi/CES/doc)
- [华为云 SDK 中心](https://console.huaweicloud.com/apiexplorer/#/sdkcenter)