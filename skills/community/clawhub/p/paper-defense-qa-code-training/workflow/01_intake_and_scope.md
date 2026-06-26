# Step 1: Intake And Defense Scope

## Goal

确定答辩对象、听众、证据范围和风险边界。

## Actions

1. Read project state:
   - `metadata/project_directory_index.json`
   - `metadata/routing_status.json`
   - `metadata/delivery_bundle_manifest.json`
   - v10 detailed report if present.
2. Identify defense context:
   - thesis defense
   - lab meeting
   - paper reading group
   - conference rebuttal
   - advisor grilling
   - job talk / interview
3. Identify available artifacts:
   - paper PDF
   - supplement
   - OpenReview
   - code repo
   - configs
   - logs
   - checkpoints
   - slides
4. Identify missing artifacts.
5. Produce a `Defense Scope` block.

## Output skeleton

```markdown
## 答辩范围与证据状态

- 论文：...
- 场景：...
- 主要听众：...
- 已有证据：...
- 缺失证据：...
- 需要重点准备的攻击轴：...
- 本答辩包的保守边界：...
```
