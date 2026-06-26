---
name: product-design-0to1
description: Use this skill when the user wants to design a brand-new (0→1) PRD or prototype for a company-internal process management system, where roles and workflows are first-class concerns. Triggers when the user explicitly says "从0到1设计PRD/原型", "设计一个全新的流程系统", or has been routed here by product-design-router. Produces user stories, swimlane diagrams, ER models, state machines, function modules, high-fidelity interactive prototype, RBAC matrix, tracking plan, and detailed PRD through 7 confirmed steps.
---

# Product Design 0→1 (Internal Process System) — v2.1

7-step pipeline. Each step has a human checkpoint. Latest confirmed artifact flows to next step.

## Domain assumption
Target is ALWAYS a company-internal process management system. Roles and workflows are core. NOT for ToC products.

## File layout (under `project/`)
```
project/
├── 00-input/{overview, roles, pain-points, expectations}.md
├── 01-user-stories.md
├── 02-flows/{swimlane.md, state-machine.md}
├── 03-er-model.md            # 🆕 v2.1
├── 03.5-field-decisions.md
├── 04-modules.md
├── 05-rbac-matrix.md         # 🆕 v2.1
├── 06-tracking-plan.md       # 🆕 v2.1
└── 07-output/{prototype.html, prd.md}
```

## The 7 steps (each delegated to a reference file)

| Step | Topic | Reference |
|---|---|---|
| 1 | 入口确认 | inline (one sentence) |
| 2 | 输入收集（4 子步 + 领域偏移检测） | `references/steps/step2-input-collection.md` |
| 3 | 7 条机械校验 | `references/steps/step3-validation.md` |
| 4 | 用户故事（三段式 + AC） | `references/steps/step4-user-stories.md` |
| 5 | 泳道图 + 状态机 | `references/steps/step5-flows.md` |
| 5.5 | 字段决策清单 | `references/steps/step5.5-field-decisions.md` |
| 6 | 功能模块 + ER 模型 + 字段 | `references/steps/step6-modules-er.md` |
| 6.5 | RBAC 权限矩阵 + 埋点规划 | `references/steps/step6.5-rbac-tracking.md` |
| 7 | 高保真原型 + 12 节 PRD | `references/steps/step7-output.md` |

## Cross-cutting rules (always apply)

1. **强制卡点**：每步产物用 `present_files` 呈现后必须等用户确认（"确认"/"修改 X"），不允许越权进入下一步
2. **AI 推断必须显式化**：所有非用户明示的细节（字段、状态机、权限、埋点）必须通过 Step 5.5 + Step 6.5 让用户拍板
3. **回退即重生成**：任何回退后，下游产物全部重做，禁止智能合并
4. **`[TODO:]` 即时标注**：当某节信息确实不足时，PRD 中用 `[TODO: 具体需要补什么]` 占位，绝不编造（吸收自 create-prd）
5. **领域偏移检测**：Step 2.1 前必须扫描会话历史，发现领域切换主动暂停询问 a/b/c
6. **不发明**：角色/痛点/字段/权限/埋点必须能从用户输入或决策清单溯源

## Self-check
完成所有步骤后加载 `references/appendices/selfcheck.md` 跑自检清单，输出"通过/待补"清单。

## End
"0→1 设计完成（含 PRD / 原型 / RBAC / 埋点）。下一步可调用 tech-design skill 进行技术方案设计。"
