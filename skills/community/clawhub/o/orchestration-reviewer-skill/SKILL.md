---
name: orchestration-reviewer-skill
version: 1.0.2
description: 对现有工作流计划（Plan IR）进行结构化评审，输出评审结论、问题清单和修订建议。
  Use when user asks to 评审工作流计划、审查DAG、审核编排方案、review plan IR、
  检查计划合理性、对比多个编排版本、自动评审工作流.
  不适用于从零生成新计划/单步操作/纯文本任务。
---

# Orchestration Reviewer Skill v1.0

对已有工作流计划（Plan IR）进行结构化评审，判断其是否满足业务目标、
是否具备可执行性与治理合理性，输出明确评审结论和修订建议。

**核心定位**：不从零生成计划，而是面向已有编排结果进行审查、评分和修订。

## 功能范围

- 评审 Plan IR 与 business_goal 的对齐度
- 检查拓扑、节点职责、技能绑定、作用域声明
- 输出明确结论：pass / conditional_pass / reject / insufficient_information
- 输出评分卡（scorecard）和问题清单（issues）
- 可选修订：生成 revised_plan_ir + diff_report

**不覆盖**：从零生成计划、运行时调度/重试/补偿、执行结果担保。

## 使用

### 决策路由

| 用户说的 | 是否适用 | 说明 |
|---------|---------|------|
| "帮我审一下这个执行计划" | ✅ | 调用本 Skill |
| "这个DAG编排合理吗" | ✅ | 调用本 Skill |
| "对比两个版本的计划哪个更好" | ✅ | 调用本 Skill |
| "从零帮我规划一个流程" | ❌ | 用 workflow-orchestration-skill |
| "直接执行这个任务" | ❌ | 单步操作，不需要评审 |

### 调用输入

```json
{
  "business_goal": "需要编排的业务目标",
  "existing_plan_ir": { "nodes": [...], "edges": [...], ... },
  "available_skills_manifest": [...],
  "review_mode": "review_only",
  "constraints": { "max_nodes": 20, "max_depth": 5 }
}
```

可选字段：`review_preferences`（strictness_level / require_scorecard / prefer_minimal_change）。

### 五阶段流程

**阶段一：输入规范化**
- 解析 business_goal、existing_plan_ir、available_skills_manifest

**阶段二：静态结构校验**
```bash
python3 scripts/validate_schema.py --plan plan.json
python3 scripts/validate_topology.py --plan plan.json
python3 scripts/validate_scope.py --plan plan.json
```

**阶段三：语义评审（LLM 主导）**
从 7 个维度评审：目标一致性、拓扑合理性、技能绑定、作用域安全、
可执行性、效率与复杂度、风险与治理。

**阶段四：结论生成**
输出 overall_decision + scorecard + issues + suggested_actions。

**阶段五：可选修订**
当 `review_mode = "review_and_revise"` 时生成 revised_plan_ir + diff_report。

### 完整调用示例

```bash
# 1. 评审（仅 review）
python3 scripts/review_plan.py \
  --goal "新员工入职流程" \
  --plan plan.json \
  --manifest skills_manifest.json \
  --mode review_only \
  --output review_result.json

# 2. 评审 + 修订
python3 scripts/review_plan.py \
  --goal "新员工入职流程" \
  --plan plan.json \
  --manifest skills_manifest.json \
  --mode review_and_revise \
  --output review_result.json

# 3. 独立评分
python3 scripts/score_plan.py --plan plan.json --manifest skills.json --output score.json

# 4. 差异对比
python3 scripts/diff_plan.py --original v1.json --revised v2.json --output diff.json
```

## 补充说明

### 评审维度（7 维）

| 维度 | 检查内容 |
|------|---------|
| 目标一致性 | 计划是否覆盖 business_goal 所需关键步骤 |
| 拓扑合理性 | 依赖关系是否合理，有无冗余串行、错误前置、不可达节点 |
| 技能绑定 | target_skill 是否与节点职责匹配 |
| 作用域安全 | scoped_state_keys 是否遵循最小权限 |
| 可执行性 | 计划是否可被工作流引擎稳定消费 |
| 效率与复杂度 | 有无冗余节点、可并行未并行、复杂度过高 |
| 风险与治理 | 高风险技能、缺少人工确认点、敏感数据暴露 |

### 结论判定

| 结论 | 含义 |
|------|------|
| pass | 计划合理，可进入执行 |
| conditional_pass | 基本合理，需按建议修正后执行 |
| reject | 计划不合理，不建议执行 |
| insufficient_information | 信息不足，无法判断 |

### 问题严重级别

| 级别 | 含义 |
|------|------|
| critical | 阻断性问题，必须修复（如循环依赖、技能不在白名单） |
| major | 重要问题，强烈建议修复（如可并行未并行） |
| minor | 次要问题，建议优化（如命名不规范） |
| info | 信息提示（如全局状态引用） |

### 前置条件

- 已提供 `business_goal` 和 `existing_plan_ir`
- 已提供 `available_skills_manifest` 或等价技能元数据
- 不满足前置条件时返回结构化错误

### 安全规则

- 评审结果仅作为治理与决策依据，不自动触发执行
- 高风险修订建议要求人工复核
- 修订结果必须再次通过静态校验

### 依赖

```bash
pip install jsonschema networkx pydantic deepdiff
```

### 目录结构

```
orchestration-reviewer-skill/
├── SKILL.md
├── references/
│   ├── review-manual.md
│   ├── review-rules.md
│   ├── scoring-policy.md
│   └── security-guardrails.md
├── scripts/
│   ├── review_plan.py
│   ├── validate_schema.py
│   ├── validate_topology.py
│   ├── validate_scope.py
│   ├── score_plan.py
│   └── diff_plan.py
└── assets/
    ├── input_schema.json
    ├── output_schema.json
    ├── sample_review_input.json
    └── sample_review_output.json
```
