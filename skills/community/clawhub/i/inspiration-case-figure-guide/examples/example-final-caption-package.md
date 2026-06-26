# Example Final Caption Package

```markdown
当前执行计划

- current_step: P9
- response_mode: TEXT_ONLY
- turn_goal: 审查最终图，给出 caption、legend 和正文插入文本。

Figure review:
- Inspiration clarity: passed. The figure answers why the paper is needed through a concrete failure-to-need chain.
- Evidence integrity: passed if all shown case facts match the supplied paper material.
- Visual legibility: revise label length if any panel has more than 6-8 words.

Caption draft:
Figure X: Motivation of <paper idea>. A concrete case exposes <problem>, where <existing/baseline behavior> leads to <failure or limitation>. The observation motivates <paper direction>, which targets <desired property> while preserving <key constraint>.

Legend:
- Red: problem or failure state.
- Blue: proposed insight or desired direction.
- Gray: context or unchanged input.

Body insertion text:
Figure X summarizes the motivating case behind our approach. The case highlights that <problem> is not merely an implementation detail, but a recurring mismatch between <condition> and <desired outcome>. This motivates our focus on <paper contribution>.

默认推荐

Use the caption only after verifying all placeholders against the paper text. Do not keep any invented metric or unverified example.

当前状态与产物

- active_skill: inspiration-case-figure-guide v3.0.0
- response_mode: TEXT_ONLY
- current_step: P9
- current_turn_outputs: [review, caption_draft, legend, body_insertion_text]
- cumulative_outputs: [startup_plan, intake, routing, text_candidates, candidate_board, candidate_review, final_prompt, final_image_batch, final_text_package]
- pending_outputs: optional revision
- previous_IMAGE_ONLY_batch_recorded: yes

全部步骤与当前位置: S0-P8 done; P9 current.

下一步你可以这样问

1. 请使用**inspiration-case-figure-guide**，执行，根据当前状态，下一步执行：根据最终图再做一轮 caption 精修。
2. 请使用**inspiration-case-figure-guide**，根据当前状态，提供下一步提问建议。
```
