# Example Routing Turn

## 当前执行计划

- 当前位置：P2 - 图需求诊断与 routing（TEXT_ONLY）
- 本轮目标：识别所有适用 diagram labels，并选择 primary production subtype

## Routing

候选 labels：`method_framework`, `architecture`, `pipeline_process`, `agent_workflow`, `system_data_flow`, `mechanism_intuition`, `case_walkthrough`, `graph_network`, `evidence_board`, `taxonomy_design_space`, `data_benchmark_protocol`, `failure_limitation`, `theory_proof_intuition`。

默认推荐：primary production subtype = `method_framework`。理由：它最适合解释方法模块、输入输出、贡献边界和论文主张；`pipeline_process` 与 `architecture` 可作为次级标签影响布局和箭头语法。

## 默认推荐

确认 `method_framework` 后进入 P3，生成 4-6 个文字候选方案，通常 6 个。P3 之后默认进入 P4/P5/P6 候选图桥接流程。

## 当前状态与产物

- **当前模式：**TEXT_ONLY
- **当前步骤：**P2
- **全部步骤与当前位置：**S0 -> P1 -> P2 [当前位置] -> P3 -> P4 -> P5 -> P6 -> P7 -> P8 -> P9
- **diagram labels：**method_framework, pipeline_process, architecture
- **primary production subtype：**method_framework
- **材料状态：**partial
- **本轮产物：**multi-label routing and subtype recommendation
- **待产物：**P3 text candidates, P4 candidate-board setup
- **上一轮 IMAGE_ONLY 产物是否已登记：**not_applicable

## 下一步你可以这样问

1. `请使用**paper-framework-figure-studio-pro**，执行，根据当前状态，下一步执行：确认 method framework，并继续生成 6 个文字候选方案。`
2. `请使用**paper-framework-figure-studio-pro**，根据当前状态，提供下一步提问建议。`
