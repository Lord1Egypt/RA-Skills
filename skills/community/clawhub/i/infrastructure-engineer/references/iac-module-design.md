# IaC 模块设计 Playbook

> 好的 Terraform 模块像好函数：接口清晰、职责单一、可组合、可测试。本 playbook 给出模块设计准则。

## 决策树：要不要抽模块

```
一段 IaC 代码
  ├─ 在 ≥2 处复用？（是）→ 抽模块，定义清晰输入/输出
  ├─ 跨团队共享？（是）→ 抽模块 + 版本化 + 文档
  └─ 仅一次性？（否）→ 保持内联，过度抽象反而难维护
```

## 接口设计

- **变量最小化**：只暴露必要的 `variable`，给 `type` 与 `description` 与 `default`。
- **输出稳定**：`output` 是契约，改名即破坏下游；用 `sensitive` 标记密钥类。
- **避免硬编码**：区域、账号、命名前缀走变量或 data source。

## 版本与发布

- **SemVer**：破坏性变更升 major；向后兼容升 minor；修复升 patch。
- **锁定约束**：`required_version` 与 `required_providers` 显式声明。
- **变更日志**：每个版本记录破坏点，下游据此升级。

## 测试与校验

- `terraform validate` / `fmt` 作为最低门槛。
- `terraform test`（或 check 块）覆盖核心路径：资源是否按预期创建、输出是否正确。
- 对破坏面大的模块加集成测试（临时 workspace 跑 plan/apply 后 destroy）。

## 组合与复用

- **扁平优于深层嵌套**：过度 `module{ module{ }}` 增加 debug 难度。
- **关注点分离**：网络 / 计算 / 数据分层模块，按生命周期拆分。
- **DRY 但不滥用**：复制两次以内可接受，第三次再抽。

## 常见坑（踩坑清单）

- **变量无类型约束**：`variable` 不写 `type`/`description`，下游靠猜传参，重构成本极高；必填项必须用 `type` 锁死。
- **`output` 改名破坏契约**：改 output 名即下游破坏却不升 major，是隐蔽的高危操作；改名必须 bump major 并在变更日志标注。
- **`count`/`for_each` 引发地址漂移**：加 `count` 后资源地址从 `x.0` 变为 `x["k"]`，state 需 `moved` 块迁移，否则全量 recreate。
- **版本约束过松**：`>= 1.0.0` 会在补丁级引入非预期破坏性变更；跨团队共享模块须锁 `~>` 或精确版本。
- **只测 happy path**：破坏性变更与 provider 升级常逃过 `terraform test`，应在 CI 加 plan-diff 断言覆盖破坏面。

## 输出

评审一个模块时产出：接口是否合理、版本策略是否清晰、测试是否覆盖破坏面。不替用户改写模块。

## 边界

- 不一刀切要求抽象；一次性代码内联更优。
- 不替用户决定模块粒度；给出权衡建议。

## 相关子技能与层次边界

- 落地到 [skills/terraform-module-library/SKILL.md](../skills/terraform-module-library/SKILL.md)：模块目录结构、变量设计、测试策略与版本发布（本 playbook 的设计准则即该子技能的工程化落地）。
- 兄弟 playbook [references/terraform-change-safety.md](terraform-change-safety.md)：模块上线前的 Plan 审查与安全门禁（设计质量 + 变更安全共同决定可维护性）。
- 相关资产 [assets/infra-review-checklist.md](../assets/infra-review-checklist.md)：模块与基础设施上线的统一检查清单。
- 边界：本 playbook 只给设计准则与权衡建议，不替用户决定模块粒度，也不做 apply。
