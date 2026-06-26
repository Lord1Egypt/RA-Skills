---
name: product-design-0to1
description: >
  触发词：从零设计、0to1、新系统、设计一个、从头设计、内部系统、全新设计
  场景：没有现有系统，从头设计一个内部用的流程管理系统。
  适用：角色和工作流是核心关注点的企业内部流程系统。
  不适用：ToC 产品、已有系统改造（请用 productization/SKILL.md）。
  由 ROUTER.md 路由进入，不直接触发。
---

# Product Design 0→1 (Internal Process System) — v3.6

精简流水线：用户只需描述产品，AI 承担推断工作，确认点大幅缩减。

## 核心升级记录

- **v3.0**：极简输入，AI 自动推断主流程/角色/痛点，一次确认
- **v3.1**：PRD 第9节每个操作节点新增 Layer 2「完整交互流」
- **v3.2**：原型交互完整性 + 字段串联完整性强制要求
- **v3.4**：研发视角 R1-R7 七维度拆解，研发可直接写代码
- **v3.5**：字段流转索引表，分包生成 PRD 第9节
- **v3.6**：原型交互自检五步骤强化（见 shared/steps/step7-output.md）

## Domain Assumption

Target is ALWAYS a company-internal process management system.
Roles and workflows are core. NOT for ToC products.

## 项目文件结构（执行时生成）

```
project/
├── 00-input/
│   ├── overview.md
│   ├── roles.md
│   ├── main-process.md
│   ├── pain-points.md
│   └── expectations.md
├── 01-user-stories.md
├── 02-flows/
│   ├── swimlane.md
│   └── state-machine.md
├── 03-business-objects-er.md
├── 03.5-field-decisions.md
├── 03.6-field-flow-index.md
├── 04-modules.md
├── 05-rbac-matrix.md
├── 06-tracking-plan.md
└── 07-output/
    ├── prototype.html
    └── prd.md
```

## 流程步骤

| Step | 内容 | 卡点 | 参考文件 |
|------|------|------|---------|
| 1 | 入口确认 + 领域偏移检测 | — | inline |
| 2 | 输入收集（一句话描述 → AI推断三项 → 用户确认） | ✅ 一次 | `../shared/steps/step2-input-collection.md` |
| 3 | 7条机械校验 | — 自动通过则继续 | `../shared/steps/step3-validation.md` |
| 4 | 用户故事（三段式 + AC + 界面标题） | ✅ 一次 | `../shared/steps/step4-user-stories.md` |
| 5 | 泳道图 + 状态机 | ✅ 一次 | `../shared/steps/step5-flows.md` |
| 5.3 | 核心业务对象 + ER + 字段流转索引表（AI自主生成） | ❌ 无需确认 | `../shared/steps/step5.3-business-objects.md` |
| 5.5 | 字段决策清单 | ✅ 一次 | `../shared/steps/step5.5-field-decisions.md` |
| 6 | 功能模块7层详述（含 Layer 2 完整交互流） | ✅ 一次 | `../shared/steps/step6-modules-er.md` |
| 6.5 | RBAC权限矩阵（确认）+ 埋点规划（AI自主生成） | ✅ 一次（仅RBAC） | `../shared/steps/step6.5-rbac-tracking.md` |
| 7 | 链路预检(R1-R7) + 高保真原型 + 13节PRD | ✅ 一次（断点确认） | `../shared/steps/step7-output.md` |
| — | 最终交付自检 | — | `../shared/appendices/selfcheck.md` |

## Cross-cutting Rules（全程生效）

1. **强制卡点**：仅表格中标注 ✅ 的步骤需等用户确认，其余 AI 自主生成后直接流转
2. **AI推断显式化**：所有非用户明示内容（业务对象/字段/后台逻辑/埋点）由 AI 推断并标注「AI推断」，供用户事后参考
3. **回退即重生成**：任何步骤回退，下游产物全部重做，禁止智能合并
4. **[TODO:] 即时标注**：信息确实不足时用 `[TODO: 具体需要补什么]` 占位，绝不编造
5. **领域偏移检测**：Step 2 前必须扫描会话历史，发现领域切换主动暂停询问
6. **不发明**：角色/痛点/字段/权限必须能从用户输入或推断逻辑溯源
7. **来源必须标注**：Step 5.3 中每个要素必须有来源标签（🖊手动输入/📋固定选项/🔗从表获取/🤖系统自动/📥上游传入）
8. **原型自检强制执行**：Step 7 原型生成后必须执行 step7-output.md 中的五步自检，全部通过后才能交付
9. **调整阶段 Skill 继续生效**：PRD 或原型首次交付后，用户提出任何调整请求（含：改、调整、修改、优化、增加、删除等词）时：
   - 修改原型 → 修改完成后强制执行 `../shared/appendices/selfcheck.md` 第六节（原型交互自检）+ `step7-output.md` 第15-16项，全部通过才能交付
   - 修改 PRD → 修改完成后执行 `selfcheck.md` 第二节（命名一致性）+ 第六节 6.5（原型与PRD一致性校验）
   - 同时修改两者 → 上述两套均执行
   - **调整阶段只加载 `step7-output.md` + `selfcheck.md`，禁止重新加载 step2-6 文件**

## Step 1 — 入口确认（inline）

向用户发出唯一提问：
> "请简单描述你想做什么产品？一两句话即可。
> 例如：『做一个内容质检系统，让质检员在线完成质检，组长审核结果』"

收到描述后进入 Step 2，执行 `../shared/steps/step2-input-collection.md`。

## End

"Step 1-7 完成（含 PRD / 原型 / RBAC / 埋点）。下一步可调用 tech-design skill。"
