# Example Startup Turn

```markdown
当前执行计划

- current_step: S0
- layer: Figure Production startup gate
- turn_goal: 只展示工作流计划，不分析论文、不生成图像。
- plan_changed: no

我将按 `inspiration-case-figure-guide` v3.0.0 执行。这个 skill 用来制作论文 inspiration 图，包括 motivating case、problem teaser、failure case、before/after contrast、scenario storyboard、observation-to-hypothesis、taxonomy hook 和 reviewer concern case。

| Step | Mode | Purpose |
|---|---|---|
| S0 | STARTUP_PLAN_ONLY (TEXT_ONLY) | 启动确认 |
| P1 | TEXT_ONLY | 收集论文材料、目标位置、inspiration 来源和参考图 |
| P2 | TEXT_ONLY | 诊断图的读者问题和多标签 subtype |
| P3 | TEXT_ONLY | 生成 4-6 个文字候选方案，默认 6 个 |
| P4 | TEXT_ONLY | 设置视觉候选图板 |
| P5 | IMAGE_ONLY | 生成 4-6 张候选图，默认 6 张 |
| P6 | TEXT_ONLY | 记录并比较候选图，锁定或修订方向 |
| P7 | TEXT_ONLY | 写正式图像 brief/prompt |
| P8 | IMAGE_ONLY | 生成正式图候选 |
| P9 | TEXT_ONLY | 审稿、caption、legend、正文插入文本 |

默认推荐

下一步进入 P1，提供论文摘要/引言/方法片段，以及你想体现的 inspiration 来源。

当前状态与产物

- active_skill: inspiration-case-figure-guide v3.0.0
- response_mode: STARTUP_PLAN_ONLY (TEXT_ONLY)
- current_step: S0
- current_turn_outputs: startup_plan
- cumulative_outputs: startup_plan
- pending_outputs: P1 material intake
- previous_IMAGE_ONLY_batch_recorded: not_applicable

全部步骤与当前位置: S0 current; P1-P9 pending.

下一步你可以这样问

1. 请使用**inspiration-case-figure-guide**，执行，根据当前状态，下一步执行：进入 P1，我提供论文摘要和想体现的 inspiration case。
2. 请使用**inspiration-case-figure-guide**，根据当前状态，提供下一步提问建议。
```
