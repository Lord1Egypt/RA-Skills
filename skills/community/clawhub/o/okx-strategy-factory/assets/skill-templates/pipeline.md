---
name: <skill-name>
description: "<描述：严格顺序的多步工作流，每步有门控条件。包含触发关键词。>"
license: Apache-2.0
metadata:
  author: <作者>
  version: "<major.minor.patch>"
  pattern: "pipeline"
  steps: "<N>"
---

# <Skill 名称> (Pipeline)

<!--
Pipeline 模式：严格顺序多步工作流 + 硬检查点。
显式菱形门控条件，需要满足条件才能进入下一步。

核心思路：
- 每步加载不同的 reference 文件
- 步骤间有门控条件（不能跳过）
- 门控可以是自动检查或用户确认
- 适合部署、交易执行、数据处理等多步流程

与 Inversion 的区别：
- Inversion 是"收集信息后一次性生成"
- Pipeline 是"每步都执行操作，步步推进"
-->

一句话概述：按严格顺序执行 N 步工作流，每步有门控检查。

## Architecture

```
Step 1: <步骤名>
    ↓ [Gate: <条件>]
Step 2: <步骤名>
    ↓ [Gate: <条件>]
Step N: <步骤名>
    ↓
Output / Completion
```

## Instructions

**CRITICAL RULE**: Steps MUST execute in order. Do NOT skip steps or proceed past a gate
that has not been satisfied. If a gate fails, STOP and report.

### Step 1: <步骤名称>

**Load**: `references/<step1-context>.md`

**Actions**:
1. <操作1>
2. <操作2>
3. <操作3>

**Output**: <本步骤的输出>

**Gate** (ALL must pass):
- [ ] <条件1> — 自动检查: `<检查命令或逻辑>`
- [ ] <条件2> — 用户确认: "Proceed to Step 2?"

### Step 2: <步骤名称>

**Load**: `references/<step2-context>.md`

**Input**: Step 1 output

**Actions**:
1. <操作1>
2. <操作2>

**Output**: <本步骤的输出>

**Gate**:
- [ ] <条件> — 自动检查: `<检查命令或逻辑>`

<!-- 按需添加更多步骤 -->

### Step N: <最终步骤>

**Load**: `references/<stepN-context>.md` (if needed)

**Input**: Step N-1 output

**Actions**:
1. <操作1>
2. <操作2>

**Output**: <最终输出>

**Completion criteria**:
- [ ] <最终验证条件>

## Gate Types

<!-- 门控类型参考 -->

| Type | Description | Example |
|---|---|---|
| `auto-check` | 自动验证，无需用户介入 | 文件存在、API 返回 200、测试通过 |
| `user-confirm` | 需要用户确认才能继续 | "Review the output. Proceed?" |
| `threshold` | 数值满足条件 | `success_rate > 95%` |
| `composite` | 多个条件 AND/OR 组合 | `auto-check AND user-confirm` |

## Failure & Rollback

<!-- 定义步骤失败时的处理策略 -->

```
IF Step N fails:
  1. Log failure reason
  2. [If rollback defined] Execute rollback for Step N
  3. Report to user: which step failed, why, how to fix
  4. DO NOT proceed to Step N+1

Rollback actions (optional, per step):
  Step 1 rollback: <撤销操作>
  Step 2 rollback: <撤销操作>
```

## State Tracking

<!-- Pipeline 可以用状态追踪执行进度 -->

```json
{
  "pipeline": "<skill-name>",
  "current_step": 2,
  "steps": {
    "1": {"status": "completed", "output": "...", "completed_at": "ISO"},
    "2": {"status": "in_progress"},
    "3": {"status": "pending"}
  }
}
```

## Directory Structure

```
<skill-name>/
├── SKILL.md                        # 主文件：步骤定义 + 门控规则
└── references/                     # 每步的上下文文档
    ├── step1-<context>.md          # Step 1 需要的参考资料
    ├── step2-<context>.md          # Step 2 需要的参考资料
    └── step3-<context>.md          # Step 3 需要的参考资料
```

## Combining with Other Patterns

<!-- Pipeline 经常与其他模式组合 -->

### Pipeline + Tool Wrapper
每步加载不同的 API reference，适合跨多个 API 的工作流：
```
Step 1: LOAD references/api-market-data.md → 获取价格
Step 2: LOAD references/api-swap.md → 执行交易
Step 3: LOAD references/api-portfolio.md → 验证结果
```

### Pipeline + Reviewer
某个步骤是审查步骤，加载 review-checklist：
```
Step 1: 生成代码
Step 2: LOAD references/review-checklist.md → 审查代码 [Gate: 0 errors]
Step 3: 部署
```

### Pipeline + Inversion
第一步是采访阶段，收集参数后执行后续步骤：
```
Step 1: Inversion phases → 收集需求 [Gate: user confirms]
Step 2: 生成 → 执行
Step 3: 验证
```

## Anti-Patterns

| Pattern | Problem |
|---|---|
| 跳过门控条件 | 后续步骤基于错误的前提执行 |
| 步骤间隐式依赖 | 应该显式声明每步的输入/输出 |
| 所有步骤加载相同 reference | 没必要用 Pipeline，用 Tool Wrapper 即可 |
| 无失败处理 | 步骤失败后状态不一致 |
| 步骤太多（>7） | 考虑合并相关步骤或拆分为子 Pipeline |
| 门控全是 user-confirm | 考虑哪些可以自动化 |
