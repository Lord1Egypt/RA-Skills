---
name: infrastructure-engineer
description: >-
  云基础设施工程师技能库：Terraform 模块开发、基础设施变更安全审查、Kubernetes 可观测性、
  数据工程基础设施（IaC）。覆盖模块设计、Plan 风险标红、黄金信号监控与变更评审。
  触发词："terraform-module-library、terraform-diff-analyzer、kubernetes-observability、terraform-data-infra、plan 审查、IaC、可观测性"。
agent_created: true
metadata:
  version: 1.0.0
  category: 云基础设施
  difficulty: 进阶
  architecture: superpower
---

# 云基础设施工程师

> 把 AI 助手变成一名 IaC 与云基础设施搭档：写得出好模块，审得清变更风险，看得见系统健康。

本技能采用 **superpower 架构**：`SKILL.md` 只做路由，深层 playbook 放在 `references/` 中
**按需加载**，细粒度能力放在 `skills/` 子技能，确定性任务交给 `scripts/`，可复用模板放在 `assets/`。

## 何时使用

- 编写或评审 Terraform 模块与基础设施代码
- 审查一份 `terraform plan`，判断 delete/replace 的破坏面
- 搭建或诊断 Kubernetes 日志/指标/追踪/告警
- 用 IaC 管理数据工程基础设施（ETL、数据仓库、批处理）

## 能力索引（超级技能路由）

本技能采用渐进式加载（progressive disclosure）。`SKILL.md` 仅作路由，**按需**读取下列
`references/` 中的完整 playbook，避免一次性占满上下文。

| 任务 | 读取 / 调用 | 关键词（grep 线索） |
|------|------------|---------------------|
| Terraform 变更安全（Plan 审查/破坏面/回滚） | [references/terraform-change-safety.md](references/terraform-change-safety.md) | terraform plan 审查 破坏面 blast radius 回滚 变更安全 |
| K8s 可观测性（黄金信号/日志指标追踪/告警） | [references/kubernetes-observability.md](references/kubernetes-observability.md) | k8s 可观测性 黄金信号 日志 指标 tracing 告警 slo |
| IaC 模块设计（接口/版本/测试/组合） | [references/iac-module-design.md](references/iac-module-design.md) | terraform 模块 设计 接口 版本 测试 组合 iac |
| K8s 可观测性：日志聚合、指标采集、分布式追踪、告警规则 | [skills/kubernetes-observability/SKILL.md](skills/kubernetes-observability/SKILL.md) | k8s 可观测性 日志 指标 追踪 告警 分布式 tracing prometheus |
| 数据工程基础设施：ETL、数据仓库、批处理集群的 IaC | [skills/terraform-data-infra/SKILL.md](skills/terraform-data-infra/SKILL.md) | 数据工程 基础设施 etl 数据仓库 批处理 terraform 数据湖 |
| 基础设施变更分析：Plan 审查、State 对比、风险识别 | [skills/terraform-diff-analyzer/SKILL.md](skills/terraform-diff-analyzer/SKILL.md) | terraform 变更 分析 plan 审查 state 对比 风险 |
| Terraform 模块开发：编写、测试、发布可复用 IaC 模块 | [skills/terraform-module-library/SKILL.md](skills/terraform-module-library/SKILL.md) | terraform 模块 开发 测试 发布 iac 复用 |

> 路由规则：方法论 / 审查类任务读 `references/`；要落地具体动作（搭监控、管数据、析变更、写模块）直接调 `skills/`。

## 内置脚本（确定性、可重复执行）

放在 `scripts/`，优先用脚本处理重复/确定性任务，而非每次重写代码：

- `scripts/tf_plan_risk.py <plan.json> [--json] [--strict]` — 解析 `terraform show -json` 计划，统计 create/update/delete/replace，标红破坏级变更与 IAM/安全资源。

运行示例：

```bash
terraform show -json plan.out > plan.json
python3 scripts/tf_plan_risk.py plan.json --strict
```

## 模板资源

`assets/` 提供可直接套用的配置与模板：

- [assets/infra-review-checklist.md](assets/infra-review-checklist.md) — apply 前评审清单（计划/数据/状态/版本/回滚）。

## 核心原则（始终遵循）

1. **不可见的变更不可控**：每份 plan 必须过风险审查。
2. **最小权限**：IAM/策略变更宁可偏严。
3. **渐进式加载**：先读路由表与对应 `references/`，再动手；不凭记忆猜命令。
4. **可观测优先**：先能看见，再谈优化。
5. **明确边界**：只出审查报告与建议，不替用户执行 apply。

## 与其他技能协作

- 需要 CI/CD 与容器化 → 调用 `skills-repo/devops-engineer`
- 需要数据库内部管理 → 调用 `skills-repo/database-engineer`
