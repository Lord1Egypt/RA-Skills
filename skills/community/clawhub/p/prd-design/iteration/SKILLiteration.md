---
name: product-design-iteration
description: >
  触发词：迭代、给现有产品加功能、改一下、删除某功能、在现有模块上修改
  场景：对已存在的内部流程管理系统进行功能迭代（新增/调整/删除模块）。
  不适用：完全新建系统（用 0to1）、SaaS产品化改造（用 productization）。
  由 ROUTER.md 路由进入，不直接触发。
---

# Product Design Iteration (Internal Process System) — v3.1

**精准迭代流程**：4步完成，以数据流为锚点，精确定位变更影响。

## 核心升级记录

- **v3.0**：精简为4步，截图为核心输入，按新增/调整/删除分类处理
- **v3.1**：Step 2 增加系统材料多入口解析（文档/流程图/纯文字/截图）+ 数据流简图；Step 4 增加命名一致性检查 + 完整16项原型自检

## Domain Assumption

Target is ALWAYS a company-internal process management system that **ALREADY EXISTS**.
- 有现有系统，在现有模块基础上迭代 → 本 Skill ✅
- 在现有项目中新增一条全新流程 → 用 `0to1/SKILL0to1.md` ✅
- 全新系统 → 用 `0to1/SKILL0to1.md` ✅
- SaaS 产品化改造 → 用 `productization/SKILLproductization.md` ✅

## Core Philosophy

**以数据流为锚点，精准变更。** 不梳理清楚模块间的数据依赖，就无法判断删除/调整的真实影响范围。

## 项目文件结构（执行时生成）

```
project/
├── 00-input/
│   └── baseline.md                    # Step 1 收集的基础信息
├── 01-adjustment-list.md              # Step 2 模块推断 + 数据流简图 + 调整清单
├── 02-add/                            # Step 3 新增界面材料
│   ├── {模块名}.md
│   └── screenshots/
├── 03-modify/                         # Step 3 调整界面材料
│   ├── {模块名}.md
│   └── screenshots/
├── 04-delete/                         # Step 3 删除影响分析
│   └── {模块名}-impact.md
├── 05-validation-passed.md            # Step 4 检查通过
└── 06-output/
    ├── delta-prd.md                   # 差量PRD
    └── prototype.html                 # 修改后原型（需通过16项自检）
```

## 流程步骤

| Step | 内容 | 卡点 | 参考文件 |
|------|------|------|---------| 
| 1 | 基础信息收集（角色/主流程/迭代需求） | ✅ 一次 | `references/steps/step1-baseline-collection.md` |
| 2 | 系统材料解析 + 数据流简图 + 调整清单 | ✅ 一次 | `references/steps/step2-adjustment-list.md` |
| 3 | 按类型收集材料（新增/调整/删除） | ✅ 一次（全部收集完后确认） | `references/steps/step3-material-collection.md` |
| 4 | 合理性检查（含命名一致性）+ 原型生成 + 16项自检 + 输出 | ✅ 一次（断点确认） | `references/steps/step4-validation-output.md` |
| — | 最终交付自检 | — | `references/appendices/selfcheck.md` |

## Cross-cutting Rules（全程生效）

1. **强制卡点**：每步产物必须用 `present_files` 呈现并等用户确认，未确认不得进入下一步
2. **数据流先行**：Step 2 的数据流简图是 Step 3 删除分析和 Step 4 检查的基础，必须在进入 Step 3 前完成并经用户确认
3. **截图优先**：Type B 调整界面，必须要求截图/原型，否则无法精准定位变更
4. **不编造**：信息不足时用 `[TODO: 需要用户补充XXX]` 占位，绝不自行编造业务逻辑
5. **命名一致性强制**：Step 4 必须执行命名一致性检查，以 Step 1-2 确认的命名为基准，差异项必须决策后才能进入输出
6. **16项原型自检强制**：原型生成后必须执行 `step4-validation-output.md` 中的全量16项自检，全部通过后才能写入 `06-output/prototype.html`
7. **before/after 必须对比**：调整类界面的原型必须有清晰的 Tab 切换对比展示，变更区域用高亮标注
8. **数据流影响必须追溯**：删除类模块必须基于 Step 2 数据流简图逐条分析下游影响，不允许仅凭感觉判断
9. **回退即重生成**：任何步骤回退，下游产物全部重做，禁止智能合并
10. **调整阶段 Skill 继续生效**：PRD 或原型首次交付后，用户提出任何调整请求（含：改、调整、修改、优化、增加、删除等词）时：
    - 修改原型 → 修改完成后强制重新执行 `step4-validation-output.md` 第10-16项自检，全部通过才能交付
    - 修改 PRD → 修改完成后执行命名一致性检查（检查项3）+ PRD与原型一致性检查（自检第9项）
    - 同时修改两者 → 上述两套均执行
    - **调整阶段只加载 `step4-validation-output.md`，禁止重新加载 step1-3 文件**

## End

"✅ 迭代设计完成（含差量PRD + 修改后原型）。请走灰度发布流程或交付工程实施。"
