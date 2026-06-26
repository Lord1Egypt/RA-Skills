---
name: product-saas-productization
description: >
  触发词：产品化、SaaS改造、对外销售、多租户改造、现有系统改造、saas化
  场景：已有一个自用系统，要改造成可卖给其他公司的 SaaS 产品。
  与 0to1/SKILL.md 的区别：本 Skill 的起点是「已有系统」，核心工作是改造分析而非从零设计。
  由 ROUTER.md 路由进入，不直接触发。
---

# 产品化改造 Skill — SaaS Productization v2.1

将企业自用系统改造为可对外销售的 SaaS 产品。

**输入**：DDL 表结构 + 功能模块描述（P0推荐），可选补充截图/文档
**输出**：改造分析报告 + 用户故事 + 高保真交互原型 + 研发可落地 PRD

## 核心升级记录

- **v1.0**：产品化 Skill 初版，Step1 材料解析 + Step2 改造分析
- **v1.1**：原型交互自检强化（5步自检，禁止带缺陷交付）
- **v2.0**：Step1 新增 DDL 硬编码规则识别（1.6节，条件触发）；Step2 新增禁止超范围扩展（2.5节）+ 配置归属判断（2.6节）；Step6/saas-patches 新增全量展示/只读页面/决策型枚举三条页面设计规范；Step7 自检新增第15项（JS语法验证）+ 第16项（HTML结构完整性验证）
- **v2.1**：Step1 输入优先级重构为 DDL + 功能模块描述优先（P0最优输入）；触发提示优先引导提供DDL；新增 §1.0 输入优先级说明、§1.2.1 DDL解析策略、§1.2.2 功能模块文字解析策略；截图解析降为最低优先级 §1.2.3；草稿格式新增「核心对象与字段（来自DDL）」区块

## 文件引用结构

```
product-design/
├── ROUTER.md
├── productization/
│   ├── SKILL.md                       ← 本文件
│   └── references/
│       ├── step1-input.md             ← 输入收集
│       ├── step2-saas-analysis.md     ← 改造分析
│       └── saas-patches.md            ← SaaS差异补丁
└── shared/
    └── steps/
        ├── step3-validation.md        ← Step3（加载补丁后执行）
        ├── step4-user-stories.md      ← Step4（加载补丁后执行）
        ├── step5-flows.md
        ├── step5.3-business-objects.md
        ├── step5.5-field-decisions.md
        ├── step6-modules-er.md
        ├── step6.5-rbac-tracking.md
        └── step7-output.md            ← 含v3.6原型自检规则
```

## 流程步骤

| Step | 内容 | 卡点 | 参考文件 |
|------|------|------|---------|
| 1 | 输入收集（截图+文字混合解析 → 草稿输出 → 强制文字补充） | ✅ 草稿确认 | `references/step1-input.md` |
| 2 | SaaS改造分析（逐模块功能颗粒度） | ✅ **强制确认，未确认不得进入Step3** | `references/step2-saas-analysis.md` |
| 3 | 机械校验（7条标准 + 3条SaaS专项） | — 自动通过则继续 | `../shared/steps/step3-validation.md` + `references/saas-patches.md` |
| 4 | 用户故事（含US-T系列租户管理员故事） | ✅ 一次 | `../shared/steps/step4-user-stories.md` + `references/saas-patches.md` |
| 5 | 泳道图 + 状态机 | ✅ 一次 | `../shared/steps/step5-flows.md` |
| 5.3 | 业务对象 + ER（含TENANT/TENANT_CONFIG标准对象） | ❌ AI自主生成 | `../shared/steps/step5.3-business-objects.md` + `references/saas-patches.md` |
| 5.5 | 字段决策清单（含SaaS三项必决策） | ✅ 一次 | `../shared/steps/step5.5-field-decisions.md` + `references/saas-patches.md` |
| 6 | 功能模块7层详述（字段表含第8列「租户隔离」） | ✅ 一次 | `../shared/steps/step6-modules-er.md` + `references/saas-patches.md` |
| 6.5 | RBAC三层权限矩阵（平台超管/租户管理员/租户用户）+ 埋点 | ✅ 一次（仅RBAC） | `../shared/steps/step6.5-rbac-tracking.md` + `references/saas-patches.md` |
| 7 | 链路预检(R1-R7) + 高保真原型 + 13节PRD | ✅ 一次（断点确认） | `../shared/steps/step7-output.md` + `references/saas-patches.md` |
| — | 最终交付自检 | — | `../shared/appendices/selfcheck.md` |

## Cross-cutting Rules（全程生效）

1. **Step2 强制卡点**：改造分析完成后必须等用户逐模块确认，用户可增删改造项，**确认后才进入 Step3，禁止跳过**
2. **改造分析颗粒度标准**：每个模块必须分析到「功能操作级」，不能停留在模块级描述
3. **只列改造/新增内容**：已有且不需要改动的功能不出现在改造清单中，保持清单简洁
4. **SaaS差异层强制执行**：Step3-7 执行时必须同步加载 `references/saas-patches.md`，差异规则优先级高于 shared 文件
5. **置信度标注**：截图推断的内容标注（✅高/⚠️中/❓低），用户可随时纠正
6. **强制文字补充**：截图无法覆盖的后台逻辑（R1-R7相关）必须强制引导用户补充，**不允许带 [TODO] 继续往下走**
7. **回退即重生成**：任何步骤回退，下游产物全部重做
8. **原型自检强制执行**：原型生成后必须执行 step7-output.md 中的五步交互自检，全部通过后才能交付
9. **🆕 差异输出原则（全程强制）**：Step 3-7 所有环节的输出内容**仅包含相对于现有系统需要改造或新增的部分**。现有系统已有且无需变动的功能、字段、流程、角色，**一律不重复描述**。具体规则：
   - **用户故事（Step4）**：只写改造点和新增功能对应的故事，已有功能不出现
   - **泳道图/状态机（Step5）**：只画涉及改造的流程差异节点，未变动的流程段用「[沿用现有逻辑]」占位标注
   - **业务对象/ER（Step5.3）**：只列新增对象和改造字段，现有字段只在「改造字段」表中标注变动内容
   - **字段决策（Step5.5）**：只针对改造点和新增功能产生的字段决策项
   - **功能模块详述（Step6）**：只对改造/新增操作节点做7层详述，现有不变节点用「[沿用现有实现]」一行标注
   - **RBAC矩阵（Step6.5）**：在现有权限基础上只列新增角色和权限变化行，未变动的角色权限不重复列出
   - **PRD输出（Step7）**：第1节必须包含「改造范围说明」，明确哪些是改造内容、哪些沿用现有系统
10. **调整阶段 Skill 继续生效**：PRD 或原型首次交付后，用户提出任何调整请求（含：改、调整、修改、优化、增加、删除等词）时：
    - 修改原型 → 修改完成后强制执行 `../shared/appendices/selfcheck.md` 第六节（原型交互自检）+ `step7-output.md` 第15-16项，全部通过才能交付
    - 修改 PRD → 修改完成后执行 `selfcheck.md` 第二节（命名一致性）+ 第六节 6.5（原型与PRD一致性校验）
    - 同时修改两者 → 上述两套均执行
    - **调整阶段只加载 `step7-output.md` + `selfcheck.md`，禁止重新加载 step2-6 文件**

## End

"产品化改造完成（含改造分析 / PRD / 原型 / RBAC / 埋点）。下一步可调用 tech-design skill。"
