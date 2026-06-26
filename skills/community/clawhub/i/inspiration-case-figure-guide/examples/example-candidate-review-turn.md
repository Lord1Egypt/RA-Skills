# Example Candidate Review Turn

```markdown
当前执行计划

- current_step: P6
- response_mode: TEXT_ONLY
- turn_goal: 记录上一轮 IMAGE_ONLY 候选图批次，比较候选方向，并锁定或修订方向。

Recorded image batch:
- candidate_image_batch_id: ICFG-P5-001
- candidates: C1-C6

Comparison:

- C1 has the clearest single-case hook but underplays the failure consequence.
- C2 makes the failure-to-need logic most legible and preserves a stable reading order.
- C3 is fast to understand but may oversimplify the paper's contribution.
- C4 is good for observation-driven papers but less concrete for this target.
- C5 is strong for rebuttal or evidence-heavy framing, not ideal for a first intro figure.
- C6 is useful if the paper's inspiration is a missing design-space region.

默认推荐

Lock C2 as the direction, then move to P7 to build the final image brief. Keep C1's focal example as an inset if the user wants more concreteness.

当前状态与产物

- active_skill: inspiration-case-figure-guide v3.0.0
- response_mode: TEXT_ONLY
- current_step: P6
- visual_candidate_board_status: reviewed
- candidate_image_batch_id: ICFG-P5-001
- selected_visual_candidate: C2
- visual_candidate_history: [ICFG-P5-001]
- previous_IMAGE_ONLY_batch_recorded: yes
- current_turn_outputs: [candidate_batch_record, candidate_comparison, default_direction]
- pending_outputs: P7 final image brief

全部步骤与当前位置: S0-P5 done; P6 current; P7-P9 pending.

下一步你可以这样问

1. 请使用**inspiration-case-figure-guide**，执行，根据当前状态，下一步执行：基于 C2 构建正式图像 brief/prompt。
2. 请使用**inspiration-case-figure-guide**，执行，根据当前状态，下一步执行：把 C1 的单案例 inset 合并进 C2。
3. 请使用**inspiration-case-figure-guide**，根据当前状态，提供下一步提问建议。
```
