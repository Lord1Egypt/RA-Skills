---
name: terraform-data-infra
description: 数据工程基础设施：ETL 管道、数据仓库、批处理集群的 IaC 管理
source:
  type: derived
  repo: skills-repo/infrastructure-engineer
  path: skills/terraform-data-infra/SKILL.md
  url: https://skills.sh/aradotso/data-skills/terraform-data-engineering-infrastructure
  version: 1.0.0
  updated: 2026-07-31
metadata:
  author: hope
  category: 云基础设施
  platform: 通用
  difficulty: 专家
  version: 1.0.0
  created: 2026-07-31
tags:
  - terraform
  - data-engineering
  - etl
  - data-warehouse
  - iac
---

# Terraform Data Infra — 数据工程基础设施

> 用 Terraform 管理数据工程基础设施，覆盖 ETL 管道、数据仓库、批处理集群和流处理平台的代码化部署。

## 能力

- **ETL 管道**：用 Terraform 部署 Airflow/Prefect 工作流编排，管理数据源连接和调度策略
- **数据仓库**：管理 BigQuery/Redshift/Snowflake 的数据库、Schema 和权限配置
- **批处理集群**：部署 EMR/Dataproc 集群，配置自动扩缩容和 Spot 实例策略
- **流处理**：管理 Kafka/PubSub 主题和 Kinesis 流的 IaC 配置
- **存储层**：S3/GCS 存储桶的创建、生命周期策略和访问控制

## 使用方式

在 Claude Code 中使用 `/terraform-data-infra` 调用。

```
/terraform-data-infra 用 Terraform 搭建一个数据湖基础设施
/terraform-data-infra 管理 BigQuery 的数据集和表权限
/terraform-data-infra 部署一个 Airflow 环境和 ETL 管道配置
```

## 工作流

1. **需求梳理** — 明确数据管道的输入、处理逻辑和输出目标
2. **架构设计** — 选择云服务组合（存储→计算→仓库），设计 IaC 模块
3. **编码实现** — 编写 Terraform 配置，管理资源依赖和变量
4. **部署验证** — 执行 plan 审查变更，apply 部署，验证数据管道运行
5. **运维管理** — 配置监控告警、备份策略和成本标签

## 适用场景

- 数据团队用 IaC 管理数据基础设施
- 独立开发者搭建个人数据管道和分析环境
- 多环境（开发/预发/生产）数据基础设施的标准化管理
- 数据基础设施的成本优化和资源生命周期管理

## 限制

- 仅管理基础设施层面，不涉及数据管道内部的业务逻辑
- 云服务商的 Terraform Provider 功能覆盖可能不完整
- 大数据集群的调优参数需要根据实际负载调整
- State 文件管理需要额外注意（建议使用远程 Backend）

## 相关参考（Playbook）

数据基础设施变更（RDS/桶/State）破坏面最高，上线前审查 → [references/terraform-change-safety.md](../../references/terraform-change-safety.md)；
模块设计准则与版本策略 → [references/iac-module-design.md](../../references/iac-module-design.md)。