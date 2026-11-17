# Terraform 变更安全 Playbook

> 基础设施即代码的铁律：不可见的变更 = 不可控的风险。本 playbook 给出 Plan 审查方法：先判破坏面，再决定能否 apply。

## 决策树：看到一份 plan 怎么审

```
读取 terraform show -json 计划
  ├─ 有 delete / replace？（是）→ 破坏级，必须人工确认影响范围
  │    ├─ 是状态资源（DB/存储/证书）？→ 阻断，走备份+演练
  │    └─ 是无状态（Pod/临时）？→ 仍需确认是否预期
  ├─ 有 IAM / 安全组 / 策略变更？（是）→ 安全级，核对最小权限
  └─ 仅 create / update？（是）→ 常规，核对命名与标签即可
```

## 风险目录

1. **destroy / replace**：数据丢失风险最高。replace = delete+create，旧资源先删。
   - 处置：对带持久数据的资源（RDS、桶、磁盘、证书）一律先快照/导出再动。
2. **IAM / 策略 / 安全组**：权限扩散风险。
   - 处置：核对是否最小权限；避免 `"Action": "*"`、`"Principal": "*"`。
3. **State 漂移**：实际资源与 state 不一致导致非预期 replace。
   - 处置：apply 前 `terraform plan` 确认无神秘变更；怀疑漂移先 `refresh`。
4. **Provider / 版本升级**：隐式行为变更。
   - 处置：锁定 provider 版本；升级单独提交、单独 review。

## 审查工作流（4 步）

1. **结构化扫描**：`python3 scripts/tf_plan_risk.py plan.json --strict` 自动标出 delete/replace 与安全资源。
2. **破坏面确认**：逐条 delete/replace 写明"为什么、影响谁、能否回滚"。
3. **State 锁**：apply 期间开启 state 锁（远程 backend），防并发改写。
4. **灰度与回滚**：重大变更分批、保留上一版 state、准备好回滚命令。

## 上线前检查清单（详见 [assets/infra-review-checklist.md](../assets/infra-review-checklist.md)）

- [ ] 所有 delete/replace 已说明影响与回滚路径
- [ ] 无权限扩张（最小权限原则）
- [ ] provider 版本已锁定
- [ ] state 后端开启锁与版本化
- [ ] 已对持久数据资源做备份

## 边界

- 脚本只做静态标红，不替代人工判断破坏面。
- 不替用户执行 apply；产出审查报告，拍板留给用户。

## 相关子技能与层次边界

- 落地到 [skills/terraform-diff-analyzer/SKILL.md](../skills/terraform-diff-analyzer/SKILL.md)：Plan 解析、风险识别与结构化审查报告（本 playbook 的审查工作流即该子技能的实操步骤）。
- 关联 [skills/terraform-data-infra/SKILL.md](../skills/terraform-data-infra/SKILL.md)：数据基础设施变更（RDS/桶/State）破坏面最高，是 change-safety 的重点对象。
- 关联 [skills/terraform-module-library/SKILL.md](../skills/terraform-module-library/SKILL.md)：模块设计质量直接影响变更安全（接口稳定 = 破坏性变更少）。
- 相关脚本 [scripts/tf_plan_risk.py](../scripts/tf_plan_risk.py)：静态标红 delete/replace 与安全资源（审查工作流第 1 步）。
- 相关资产 [assets/infra-review-checklist.md](../assets/infra-review-checklist.md)：上线前检查清单（本 playbook 已引用）。
- 兄弟 playbook [references/iac-module-design.md](iac-module-design.md)：设计阶段就降低变更风险。
- 边界：脚本只做静态标红，不替代人工判断破坏面；不替用户执行 apply。
