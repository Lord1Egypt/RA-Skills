# Example Visual Board Setup Turn

```markdown
当前执行计划

- current_step: P4
- response_mode: TEXT_ONLY
- turn_goal: 设置候选图板，停止在生成前。

Board purpose:
Generate candidate images or schematic candidates for choosing an inspiration-figure direction, not a final figure.

Candidate count:
6.

Hold fixed:
- figure thesis: <why the paper is needed>
- target slot: introduction
- evidence anchors: <supplied case facts only>
- labels: <exact short labels>
- color semantics: red/problem, blue/proposed insight, gray/context

Vary only:
Layout skeleton across C1-C6: single-case hook, failure chain, before/after split, observation ladder, evidence tile board, taxonomy hook.

Compare:
Choose the candidate that makes the motivating case concrete without inventing evidence or overclaiming the method.

Rendering route:
ChatGPT web uses Create image through ChatGPT Images 2.0. Codex uses `$imagegen` first; if unavailable, use ChatGPT Images 2.0 API or another approved image-generation API.

默认推荐

下一步执行 P5，生成 6 张候选图。P5 必须是 IMAGE_ONLY，不附带解释或状态页脚。

当前状态与产物

- active_skill: inspiration-case-figure-guide v3.0.0
- response_mode: TEXT_ONLY
- current_step: P4
- visual_candidate_board_status: setup_ready
- visual_board_type: layout
- visual_board_candidate_count: 6
- visual_board_axis_varied: layout skeleton
- visual_board_fixed_elements: [figure thesis, target slot, evidence anchors, exact labels, color semantics]
- current_turn_outputs: [candidate_board_setup]
- pending_outputs: P5 IMAGE_ONLY candidate board

全部步骤与当前位置: S0-P3 done; P4 current; P5-P9 pending.

下一步你可以这样问

1. 请使用**inspiration-case-figure-guide**，执行，根据当前状态，下一步执行：生成 6 张候选图/示意图供我比较选择。
2. 请使用**inspiration-case-figure-guide**，根据当前状态，提供下一步提问建议。
```
