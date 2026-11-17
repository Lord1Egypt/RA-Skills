# Infrastructure Engineer — Agent 入口

> 本仓库是 skills-repo 组织下的云基础设施工程师技能库。面向独立开发者和小团队，覆盖 Terraform 模块开发、基础设施变更分析、Kubernetes 可观测性和数据工程基础设施。

## 技能清单

| 环节 | 技能 | 文件 | 用途 |
|------|------|------|------|
| 模块 | terraform-module-library | [skills/terraform-module-library/SKILL.md](skills/terraform-module-library/SKILL.md) | Terraform 模块开发：编写、测试、发布可复用模块 |
| 变更 | terraform-diff-analyzer | [skills/terraform-diff-analyzer/SKILL.md](skills/terraform-diff-analyzer/SKILL.md) | 基础设施变更分析：Plan 审查、State 对比、风险识别 |
| 观测 | kubernetes-observability | [skills/kubernetes-observability/SKILL.md](skills/kubernetes-observability/SKILL.md) | K8s 可观测性：日志、指标、追踪、告警配置 |
| 数据 | terraform-data-infra | [skills/terraform-data-infra/SKILL.md](skills/terraform-data-infra/SKILL.md) | 数据工程基础设施：ETL 管道、数据仓库、批处理 |

## 使用场景

- 独立开发者用 Terraform 管理个人项目的云资源
- 小团队搭建和运维 Kubernetes 集群
- 基础设施即代码（IaC）的编写、审查和变更管理
- 数据工程师用 Terraform 管理数据基础设施

## 相关仓库

- `devops-engineer` — CI/CD、容器化、监控，本仓库聚焦 IaC 和云基础设施
- `backend-developer` — API 和后端架构，本仓库聚焦基础设施层
- `database-engineer` — 数据库管理，本仓库关注基础设施而非数据库内部

> 本仓库聚焦**云基础设施的代码化管理**，与 devops-engineer 的 CI/CD 和容器化互补。