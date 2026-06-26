# Example Final Caption Package

This is P9. It can happen only after the visual direction and formal figure candidates have been reviewed or the user explicitly requests text finalization.

## 当前执行计划

- 当前位置：P9 - 诊断与论文文字（TEXT_ONLY）
- 本轮目标：输出 caption、legend 和正文衔接文字

## Final Text Draft

Caption draft:

Figure X: Overview of the proposed framework. The diagram shows how the input is transformed through the core modules, how feedback updates the intermediate state, and where the proposed mechanism differs from prior baselines.

Body insertion:

Figure X summarizes the method pipeline and highlights the central mechanism used to connect the problem setting with the final prediction objective.

## 默认推荐

先锁定最佳候选图，再根据论文方法章节调整 caption 的粒度。

## 当前状态与产物

- **当前模式：**TEXT_ONLY
- **当前步骤：**P9
- **全部步骤与当前位置：**S0 -> P1 -> P2 -> P3 -> P4 -> P5 -> P6 -> P7 -> P8 -> P9 [当前位置]
- **selected_visual_candidate：**candidate selected or user-approved
- **上一轮 IMAGE_ONLY 产物是否已登记：**recorded
- **本轮产物：**caption draft, body insertion draft
- **累计产物：**selected image, critique, final text package
- **待产物：**user edits or final polish

## 下一步你可以这样问

1. `请使用**paper-framework-figure-studio-pro**，执行，根据当前状态，下一步执行：把 caption 改得更适合方法章节。`
2. `请使用**paper-framework-figure-studio-pro**，根据当前状态，提供下一步提问建议。`
