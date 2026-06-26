# Role Discovery Dialog Flow

Goal: collect enough information with minimal questions, then propose a complete role plan for confirmation.

## A. Minimal-question strategy (ask in this order)
1. Objective: "What outcome should this team deliver?"
2. Scope: "From strategy only, or strategy + execution?"
3. Constraints: "Any hard constraints (timeline, budget, compliance, tool stack)?"

If user already provided an item, do not ask it again.

> Channel confirmation is deferred to post-creation binding stage.

## B. Auto-completion rules
When user gives sparse input, infer defaults:
- 先按目标域选择团队原型（Product/Engineering、Growth/Marketing、Ops/Support 等），不得默认带研发角色。
- 只有当目标明确包含研发实施时，才建议工程角色（默认 fullstack；前后端拆分必须过 splitting-principles）。
- If objective includes "growth/marketing" → suggest Growth+Marketing core set.
- If objective includes "ops/support" → suggest Operations+Support core set.
- If timeline is tight, prioritize fewer roles with broader ownership.
- If compliance mentioned, add security/compliance role as core.

Always mark inferred items as "assumed" and ask for confirmation.

## C. Confirmation contract
Before creation steps, require explicit confirmation:
- final roles (must include `team-leader`)
- core vs optional
- lead role
- proceed now (yes/no)


## C.1 Role display rule during confirmation
- Use user's language.
- Show role display names + function/value only.
- Do NOT show agent IDs during this phase.
- Agent IDs appear only in final creation report.

### Localized display mapping example (Chinese)
| 角色 | 职责 |
|---|---|
| 团队负责人 | 团队协调、任务分配、进度汇总 |
| 产品经理 | 产品需求分析、PRD文档、里程碑规划 |
| 技术架构师 | 技术架构设计、服务边界、API契约 |
| 全栈工程师 | 端到端实现、接口联调、关键链路交付 |
| 测试工程师 | 测试计划、质量把控、发布就绪报告 |

## D. Anti-overdesign constraints
- Avoid >8 roles unless user explicitly requests larger team.
- Merge overlapping roles when outputs are not clearly distinct.
- Each role must own one primary output artifact.
- Apply `splitting-principles.md` before final role confirmation.

## E. Split/Merge rationale block (mandatory)
Before confirming roles, provide concise rationale per role:
- why_split_or_not
- unique_artifact
- authority_boundary
- dependency_count
- expected_parallel_gain
