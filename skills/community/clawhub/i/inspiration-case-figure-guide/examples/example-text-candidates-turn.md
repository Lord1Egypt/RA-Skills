# Example Text Candidates Turn

```markdown
当前执行计划

- current_step: P3
- response_mode: TEXT_ONLY
- turn_goal: 定义 reader effect，并给出 6 个文字候选方案。

Reader effect: 读者在 5 秒内理解这篇论文为什么需要提出新方法。

候选方案:

1. C1 Single-Case Hook: 用一个输入样例展示现有方法的错误行为，再用一个短 callout 指向方法需求。
2. C2 Failure Chain: trigger -> baseline state -> observed failure -> consequence -> proposed need。
3. C3 Before/After Split: 左侧 current behavior，右侧 desired behavior，保持输入不变。
4. C4 Observation Ladder: observation -> recurring pattern -> design principle -> method implication。
5. C5 Evidence Tile Board: 中央 claim 周围放 3-4 个证据卡片。
6. C6 Taxonomy Hook: 用二维设计空间凸显未覆盖区域，再引出本文方向。

以上是默认的 4-6 个文字候选方案，通常 6 个。下一步不要只从文字方案里定稿；建议先生成 6 张候选图/示意图来比较方向。

默认推荐

推荐 C2 Failure Chain 作为默认候选图板方向，因为它最直接回答 "why is this paper needed?"，同时便于控制证据不越界。

当前状态与产物

- active_skill: inspiration-case-figure-guide v3.0.0
- response_mode: TEXT_ONLY
- current_step: P3
- text_candidate_count: 6
- candidate_scheme_ids: [C1, C2, C3, C4, C5, C6]
- visual_candidate_board_status: not_started
- current_turn_outputs: [reader_effect, six_text_candidates]
- pending_outputs: P4 visual candidate-board setup

全部步骤与当前位置: S0 done; P1 done; P2 done; P3 current; P4-P9 pending.

下一步你可以这样问

1. 请使用**inspiration-case-figure-guide**，执行，根据当前状态，下一步执行：生成 6 张候选图/示意图供我比较选择。
2. 请使用**inspiration-case-figure-guide**，执行，根据当前状态，下一步执行：先进入 P4，设置候选图板的固定元素和变化轴。
3. 请使用**inspiration-case-figure-guide**，根据当前状态，提供下一步提问建议。
```
