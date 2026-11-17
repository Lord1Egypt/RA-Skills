# Infrastructure Engineer — 云基础设施工程师技能库

> 面向独立开发者和小团队的云基础设施技能集合。覆盖 Terraform 模块开发、基础设施变更分析、Kubernetes 可观测性和数据工程基础设施。

## 技能清单

| 技能 | 描述 | 安装量 | 来源 |
|------|------|--------|------|
| terraform-module-library | Terraform 模块开发：编写、测试、发布可复用的 IaC 模块 | 12.9K | [skills.sh](https://skills.sh/wshobson/agents/terraform-module-library) |
| terraform-diff-analyzer | 基础设施变更分析：Plan 审查、State 对比、风险识别 | 8.8K | [skills.sh](https://skills.sh/github/awesome-copilot/terraform-azurerm-set-diff-analyzer) |
| kubernetes-observability | K8s 可观测性：日志聚合、指标采集、分布式追踪、告警规则 | 1.4K | [skills.sh](https://skills.sh/dynatrace/dynatrace-for-ai/dt-obs-kubernetes) |
| terraform-data-infra | 数据工程基础设施：ETL 管道、数据仓库、批处理集群的 IaC 管理 | 1.6K | [skills.sh](https://skills.sh/aradotso/data-skills/terraform-data-engineering-infrastructure) |

## 工作流

```
模块开发 ──→ 变更分析 ──→ 可观测性
(terraform-module-library)  (terraform-diff-analyzer)  (kubernetes-observability)
        │
        └──→ 数据基础设施
             (terraform-data-infra)
```

## 安装

```bash
# 安装全部基础设施技能
npx skills add skills-repo/infrastructure-engineer -g -y

# 或按需安装单个技能
npx skills add skills-repo/infrastructure-engineer@terraform-module-library -g -y
npx skills add skills-repo/infrastructure-engineer@terraform-diff-analyzer -g -y
npx skills add skills-repo/infrastructure-engineer@kubernetes-observability -g -y
npx skills add skills-repo/infrastructure-engineer@terraform-data-infra -g -y
```

## 与本组织其他仓库的关系

- **devops-engineer** — CI/CD、容器化、监控，本仓库聚焦 IaC 和云基础设施代码化
- **backend-developer** — API 和后端架构，本仓库聚焦基础设施层
- **database-engineer** — 数据库内部管理，本仓库关注基础设施即代码