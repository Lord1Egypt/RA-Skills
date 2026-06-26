# Example Candidate Review Turn

This is P6. It must happen after P5 and before final image brief construction.

## 当前执行计划

- 当前位置：P6 - 候选图回看与方向锁定（TEXT_ONLY）
- 本轮目标：记录上一轮 IMAGE_ONLY 候选图 batch，比较候选图，并让用户选择/修改/重做

## Candidate Review

默认推荐：选择 Candidate 3 作为主方向。它最清楚地突出 proposed framework，模块层级可读，箭头路径不拥挤。风险是右侧 evidence cards 信息密度略高，需要在 P7 prompt 中压缩标签。

## 默认推荐

锁定 Candidate 3 的布局骨架，进入 P7 构建正式 image brief；如果用户不满意，则在 P4 重新设置候选图板。

## 当前状态与产物

- **当前模式：**TEXT_ONLY
- **当前步骤：**P6
- **全部步骤与当前位置：**S0 -> P1 -> P2 -> P3 -> P4 -> P5 -> P6 [当前位置] -> P7 -> P8 -> P9
- **visual_candidate_board_status：**reviewed
- **candidate_image_batch_id：**candidate-board-001
- **selected_visual_candidate：**Candidate 3 recommended
- **上一轮 IMAGE_ONLY 产物是否已登记：**recorded
- **本轮产物：**candidate review and default direction recommendation
- **待产物：**P7 final image brief

## 下一步你可以这样问

1. `请使用**paper-framework-figure-studio-pro**，执行，根据当前状态，下一步执行：锁定 Candidate 3，并构建正式 image brief。`
2. `请使用**paper-framework-figure-studio-pro**，根据当前状态，提供下一步提问建议。`
