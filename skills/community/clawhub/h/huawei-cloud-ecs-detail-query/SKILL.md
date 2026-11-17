---
name: huawei-cloud-ecs-detail-query
version: 1.0.0
description: 查询华为云ECS实例详情和列表的skill，支持通过实例ID查询单个ECS详情，以及列出所有ECS实例
triggers:
  - 查询华为云ECS
  - 列出ECS实例
  - ECS详情查询
  - 查看ECS信息
tags:
  - huawei-cloud
  - ecs
  - query
  - detail
---

# Huawei Cloud ECS Detail Query Skill

## 安全硬约束

1. **凭据安全**：AK/SK 从环境变量动态读取（支持 HUAWEI/HW/HWC 前缀），禁止硬编码在脚本中
2. **超时控制**：所有 API 调用设置 30s 超时
3. **错误处理**：API 返回 403/429 等错误码时给出明确提示，不静默崩溃
4. **最小权限**：仅使用只读查询 API（ShowServer / ListServersDetails），不做任何写操作
5. **输入校验**：对用户输入的 server_id 等参数做空值和格式校验

## Overview / 概述

该 Skill 基于**华为云 KooCLI**（hcloud CLI），提供华为云 ECS（弹性云服务器）实例的只读查询能力。

| 操作 | 功能 | 对应 API |
|------|------|---------|
| 实例详情查询 | 通过实例 ID 查询单个 ECS 的详细信息 | ShowServer |
| 实例列表查询 | 列出所有 ECS 实例及概要信息 | ListServersDetails |

### 适用场景

- 日常运维：查看 ECS 实例状态、规格、IP 地址等信息
- 故障排查：快速获取指定 ECS 实例的完整配置信息
- 资源盘点：列出账户下所有 ECS 实例并进行统计

### 架构

用户/Agent → 脚本 → hcloud CLI → 华为云 ECS API → 格式化输出

## Prerequisites / 前置条件

### 1. 安装 hcloud CLI

```bash
curl -O https://cn-huaweicloud.obs.cn-north-1.myhuaweicloud.com/cli/latest/hcloud_install.sh
bash hcloud_install.sh -y
hcloud version
```

### 2. 配置华为云认证

```bash
hcloud configure set --cli-region=cn-north-4 --access-key=YOUR_AK --secret-key=YOUR_SK
```

或通过环境变量配置：

```bash
export HUAWEICLOUD_SDK_AK=YOUR_ACCESS_KEY
export HUAWEICLOUD_SDK_SK=YOUR_SECRET_KEY
```

### 3. IAM 权限

| 权限 | 说明 |
|------|------|
| ecs:servers:get | 查询单个 ECS 实例详情 |
| ecs:servers:list | 查询 ECS 实例列表 |

详细 IAM 策略见 references/iam-policies.md。

## Workflow / 工作流

### 查询单个 ECS 实例详情

用户输入 server_id → 参数校验（非空、UUID 格式）→ hcloud ECS ShowServer → 解析 JSON → 格式化展示

### 列出 ECS 实例列表

用户输入可选筛选条件 → hcloud ECS ListServersDetails → 解析 JSON → 格式化表格展示

## Core Commands / 核心命令

### 查询 ECS 实例详情

```bash
hcloud ECS ShowServer --cli-region=cn-north-4 --server_id="d4c5865c-b3a5-4f36-9071-ec10e74eef59"
```

### 列出 ECS 实例列表

```bash
hcloud ECS ListServersDetails --cli-region=cn-north-4 --limit=20
```

### 按名称模糊查询

```bash
hcloud ECS ListServersDetails --cli-region=cn-north-4 --name="blog"
```

## Script Usage

```bash
# 查看帮助
python3 scripts/huawei_cloud_ecs_detail_query.py --help

# 列出 ECS 实例列表
python3 scripts/huawei_cloud_ecs_detail_query.py list --region=cn-north-4

# 查询单个 ECS 实例详情
python3 scripts/huawei_cloud_ecs_detail_query.py show --server-id=SERVER_ID --region=cn-north-4
```

## Parameter Confirmation / 参数确认

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| --region | 否 | string | 区域（默认 cn-north-4） |
| --server-id | 是(show) | string | ECS 实例 ID（UUID） |
| --limit | 否 | integer | 分页大小（1-1000，默认20） |
| --offset | 否 | integer | 分页偏移（从0开始） |
| --name | 否 | string | 名称模糊匹配 |
| --ip | 否 | string | IP 模糊匹配 |

## KooCLI Command Format Standard



KooCLI 命令格式遵循以下规范：



```

hcloud <Service> <Operation> --cli-region={region} [--param=value ...]

```



- Service 名称首字母大写（如 ECS）

- Operation 名称使用 PascalCase（如 ShowServer、ListServersDetails）

- --cli-region 为必填参数，指定 API 调用区域

- 参数名使用双横线前缀（如 --server_id、--limit）


## Error Handling / 错误处理

| 错误场景 | 退出码 | 说明 |
|---------|--------|------|
| AK/SK 未配置 | 3 | 提示配置环境变量 |
| 实例不存在 | 4 | 提示未找到实例 |
| limit 无效 | 5 | 提示超出范围 |
| CLI 执行失败 | 6 | 输出 CLI 错误详情 |
| 参数校验失败 | 7 | 输出具体原因 |
| 网络超时 | 8 | 提示检查网络 |

## Reference Documents

| 文档 | 说明 |
|------|------|
| references/iam-policies.md | IAM 权限策略 |
| references/cli-installation-guide.md | CLI 安装与认证 |
| references/verification-method.md | 验证方法 |
| references/dataflow-diagram.md | 数据流图 |
| references/acceptance-criteria.md | 验收标准 |
