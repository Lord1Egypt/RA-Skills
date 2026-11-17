---
name: terraform-diff-analyzer
description: 基础设施变更分析：Plan 审查、State 对比、风险识别
source:
  type: derived
  repo: skills-repo/infrastructure-engineer
  path: skills/terraform-diff-analyzer/SKILL.md
  url: https://skills.sh/github/awesome-copilot/terraform-azurerm-set-diff-analyzer
  version: 1.0.0
  updated: 2026-07-31
metadata:
  author: hope
  category: 云基础设施
  platform: 通用
  difficulty: 进阶
  version: 1.0.0
  created: 2026-07-31
tags:
  - terraform
  - plan
  - state
  - diff
  - risk-analysis
---

# Terraform Diff Analyzer — 变更分析

> 深度分析 Terraform Plan 输出，识别基础设施变更的类型、影响范围和潜在风险，输出结构化的变更审查报告。

## 能力

- **Plan 解析**：解析 terraform plan 输出，提取资源创建、更新、删除的变更清单
- **风险识别**：标记高风险变更（如数据库删除、安全组修改、网络拓扑变更）
- **State 对比**：对比当前 State 和远程 State，发现漂移（drift）和手动变更
- **影响分析**：基于资源依赖图，评估变更的波及范围
- **审查报告**：生成结构化的变更审查报告，包含风险等级和审批建议

## 使用方式

在 Claude Code 中使用 `/terraform-diff-analyzer` 调用。

```
/terraform-diff-analyzer 分析这个 terraform plan 输出
/terraform-diff-analyzer 检查 State 文件是否有漂移
/terraform-diff-analyzer 评估这次变更的风险等级
```

## 工作流

1. **获取 Plan** — 读取 terraform plan 的 JSON 输出或文本输出
2. **分类变更** — 按资源类型（计算、网络、存储、数据库）分类变更
3. **风险评级** — 为每个变更标记风险等级（低/中/高/关键）
4. **影响分析** — 基于依赖关系分析变更的波及范围
5. **输出报告** — 生成变更审查报告，包含建议和审批要点

## 适用场景

- 生产环境变更前的安全审查
- CI/CD 流水线中的自动化变更风险评估
- 审计和合规要求下的变更记录
- 多人协作时的变更沟通和审批

## 限制

- 依赖 terraform plan 的完整输出，增量分析需要历史 State 文件
- 风险判断基于规则引擎，需要根据组织规范调整风险阈值
- 不支持跨 Provider 的依赖分析
- 复杂模块的内部变更需要手动展开

## 相关参考（Playbook）

Plan 审查工作流、风险目录与上线前检查清单 → [references/terraform-change-safety.md](../../references/terraform-change-safety.md)；
自动化标红 delete/replace 与安全资源 → [scripts/tf_plan_risk.py](../../scripts/tf_plan_risk.py)；
统一检查清单 → [assets/infra-review-checklist.md](../../assets/infra-review-checklist.md)。