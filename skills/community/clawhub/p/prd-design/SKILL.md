---
name: product-design-router
description: >
  产品设计 Skill 统一入口路由。
  所有产品设计相关请求先经过本文件判断，再路由到对应 Skill。
  触发词：PRD、原型、产品设计、从零设计、0to1、产品化、SaaS改造、现有系统改造、迭代、加功能、改功能
---

# Product Design Router — 统一入口 v2.0

## 路由判断规则

收到用户请求后，按以下步骤判断，加载对应 Skill：

### 第一步：关键词扫描

| 关键词匹配 | 路由目标 |
|-----------|---------|
| 改造、产品化、SaaS化、SaaS改造、对外销售、多租户改造、现有系统改造、saas化 | → `productization/SKILLproductization.md` |
| 从零、0to1、全新设计、从头设计 | → `0to1/SKILL0to1.md`（进入后需二次判断，见下） |
| 迭代、给现有产品加功能、改一下、删除某功能、在现有模块上修改 | → `iteration/SKILLiteration.md` |

### 第二步：无法判断时向用户提问

若扫描后无法明确判断，向用户展示以下选项：

---

> **你想做哪种事情？**
>
> **A) 在现有系统的模块上迭代**
> 系统已存在，需要在某个或某些现有模块上增加/修改/删除功能
> 例如：「给回访系统的任务管理模块加个自动生成功能」
>
> **B) 在现有项目中新增一条全新流程**
> 系统已存在，但要新建一套之前完全没有的业务流程
> 例如：「我们的系统有质检流程，现在要再加一套培训管理流程」
>
> **C) 设计一个全新的系统**
> 没有现有系统，从头规划角色、流程、功能、PRD 和原型
> 例如：「我们要做一个全新的报销审批系统」
>
> **D) 将已有系统改造成 SaaS 产品**
> 已有一个自用系统，要改造成可以卖给其他公司的 SaaS 产品
>
> 请回复 A、B、C 或 D。

---

- 用户选 **A** → 加载 `iteration/SKILL.md`
- 用户选 **B** → 加载 `0to1/SKILL0to1.md`，并在 Step 1 提示：「这是在现有项目中新增流程，请先描述现有项目背景，再描述新流程需求」
- 用户选 **C** → 加载 `0to1/SKILL0to1.md`
- 用户选 **D** → 加载 `productization/SKILLproductization.md`

### 第三步：0to1 内部二次判断

进入 `0to1/SKILL0to1.md` 后，Step 1 入口收集信息时若发现用户描述的是「在现有项目中新增流程」，在 Step 2 开始前追问：

> "您提到的是在现有系统基础上新增流程，还是设计一个全新的独立系统？
>
> - **新增流程**：我会额外收集现有系统背景，确保新流程与原系统无缝衔接
> - **全新系统**：直接从零开始规划"

若是「新增流程」，Step 2 输入收集时增加一项：「请简要描述现有系统已有哪些模块/流程，新流程将与哪些现有模块交互」。

### 第四步：路由锁定

一旦确定路由，本次会话固定走该 Skill，不再重新判断。

### 第五步：调整阶段处理

路由锁定后，用户发出的任何调整请求（含「改、调整、修改、优化、增加、删除」等词），均视为当前 Skill 流程的延续，由对应 Skill 的 Cross-cutting Rules 最后一条「调整阶段 Skill 继续生效」处理，**不得作为普通对话直接修改输出**。

---

## 三个 Skill 的核心差异

| 维度 | 迭代 | 0to1（新增流程） | 0to1（全新系统） | 产品化 |
|------|------|---------------|---------------|--------|
| 起点 | 已有系统，改局部模块 | 已有系统，加全新流程 | 无现有系统 | 已有系统，全局改造为SaaS |
| 核心工作 | 精准定位变更 + 影响分析 | 新流程设计 + 与现有系统衔接 | 从零设计全套 | 改造分析 + SaaS化方案 |
| 数据流梳理 | Step 2 必做（推断现有+变更影响） | Step 2 可选（现有系统背景） | 不需要 | Step 2 SaaS改造分析 |
| 输出类型 | 差量PRD + 修改后原型（Before/After对比） | 标准PRD + 原型（含与现有系统衔接说明） | 标准PRD + 原型 | 改造清单 + 多租户PRD + 原型 |
| 原型风格 | Before/After 对比 + 变更高亮 | 新流程完整原型 | 完整系统原型 | 含改造对比的完整原型 |

---

## 文件结构总览

```
product-design/
├── SKILL.md                          ← 本文件，统一入口
│
├── shared/                            ← 0to1 和产品化共用，禁止直接修改
│   ├── steps/
│   │   ├── step2-input-collection.md
│   │   ├── step3-validation.md
│   │   ├── step4-user-stories.md
│   │   ├── step5-flows.md
│   │   ├── step5.3-business-objects.md
│   │   ├── step5.5-field-decisions.md
│   │   ├── step6-modules-er.md
│   │   ├── step6.5-rbac-tracking.md
│   │   └── step7-output.md
│   └── appendices/
│       └── selfcheck.md
│
├── 0to1/
│   └── SKILL0to1.md                  ← 从零设计 / 新增流程，引用 ../shared/steps/*.md
│
├── productization/
│   ├── SKILLproductization.md        ← 产品化改造，引用 ../shared/steps/*.md + references/saas-patches.md
│   └── references/
│       ├── step1-input.md
│       ├── step2-saas-analysis.md
│       └── saas-patches.md
│
└── iteration/                         ← 迭代，独立流程，不复用 shared
    ├── SKILL.md                       ← 迭代主控文件
    └── references/
        ├── steps/
        │   ├── step1-baseline-collection.md
        │   ├── step2-adjustment-list.md   ← 含系统材料多入口解析 + 数据流简图
        │   ├── step3-material-collection.md
        │   └── step4-validation-output.md ← 含命名一致性检查 + 16项原型自检
        ├── appendices/
        │   └── selfcheck.md
        └── templates/
            └── prototype-template.html
```
