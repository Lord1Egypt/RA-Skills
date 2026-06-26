# Example Visual Board Setup Turn

This is P4. It follows P3 text candidates and must stop before image generation.

## 当前执行计划

- 当前位置：P4 - 视觉候选图板设置（TEXT_ONLY）
- 上一步 P3 已给出 6 个文字候选方案
- 本轮目标：设置 6 张候选图/示意图的生成规则

## Candidate-Board Brief

- board type: scheme / layout
- candidate count: 6
- varied axis: layout skeleton
- fixed elements: figure thesis, required modules, exact labels, palette semantics
- rendering route: ChatGPT web Create image / ChatGPT Images 2.0; Codex `$imagegen` first; fallback ChatGPT Images 2.0 API or approved image API
- compare: reading clarity, contribution prominence, label readability, paper-slot fit

## 默认推荐

生成 6 张候选图。固定论文 thesis、核心模块和标签，只变化布局骨架，这样用户可以看图选方向，而不是只靠文字定稿。

## 当前状态与产物

- **当前模式：**TEXT_ONLY
- **当前步骤：**P4
- **全部步骤与当前位置：**S0 -> P1 -> P2 -> P3 -> P4 [当前位置] -> P5(IMAGE_ONLY candidate-board generation) -> P6 -> P7 -> P8 -> P9
- **text_candidate_count：**6
- **image_candidate_count：**6
- **visual_candidate_board_status：**setup_ready
- **visual_board_type：**scheme/layout
- **visual_board_axis_varied：**layout skeleton
- **candidate_image_batch_id：**not_created
- **本轮产物：**candidate-board brief
- **待产物：**P5 IMAGE_ONLY candidate image board

## 下一步你可以这样问

1. `请使用**paper-framework-figure-studio-pro**，执行，根据当前状态，下一步执行：生成 6 张候选图/示意图供我比较选择。`
2. `请使用**paper-framework-figure-studio-pro**，根据当前状态，提供下一步提问建议。`
