# Example Startup Turn

## 当前执行计划

- 当前位置：S0 - 启动确认（STARTUP_PLAN_ONLY / TEXT_ONLY）
- 本轮目标：只展示流程，不做实质论文分析，不生成图像
- 默认推荐动作：确认开始并进入 P1 材料收集

即使用户第一句话要求“直接出图”或“生成 6 张候选图”，首次回复也只能展示启动计划。出图请求应记录为 pending image request；本轮不能调用 Create image、`$imagegen` 或任何图像 API。

| 步骤 | 回复类型 | 做什么 | 本步产物 |
|---|---|---|---|
| S0 | STARTUP_PLAN_ONLY (TEXT_ONLY) | 启动确认 | 流程预览 |
| P1 | TEXT_ONLY | 材料收集 | material status |
| P2 | TEXT_ONLY | 图需求诊断与 routing | subtype candidates |
| P3 | TEXT_ONLY | 读者效果与 4-6 个文字候选 | text candidate schemes |
| P4 | TEXT_ONLY | 设置视觉候选图板 | candidate-board brief |
| P5 | IMAGE_ONLY | 生成多张候选图/示意图 | image candidates only |
| P6 | TEXT_ONLY | 回看候选图并锁定/修正方向 | selected direction |
| P7 | TEXT_ONLY | 构建正式 image brief | final image brief |
| P8 | IMAGE_ONLY | 生成正式候选图/修订图 | formal images only |
| P9 | TEXT_ONLY | 诊断、caption、legend、正文衔接 | final text package |

## 默认推荐

确认开始，先提供论文摘要/方法说明。后续一旦出现多个文字方案，默认下一步会进入 P4/P5/P6 候选图桥接流程，而不是只从文字方案里定稿。

## 当前状态与产物

- **当前模式：**STARTUP_PLAN_ONLY (TEXT_ONLY)
- **当前步骤：**S0
- **全部步骤与当前位置：**S0 [当前位置] -> P1 -> P2 -> P3 -> P4 -> P5 -> P6 -> P7 -> P8 -> P9
- **材料状态：**not_provided
- **visual_candidate_board_status：**not_started
- **本轮产物：**startup plan
- **待产物：**材料收集、routing、文字候选、候选图板
- **上一轮 IMAGE_ONLY 产物是否已登记：**not_applicable
- **session 状态延续提醒：**默认根据当前 session/history 自动延续状态。

## 下一步你可以这样问

1. `请使用**paper-framework-figure-studio-pro**，执行，根据当前状态，下一步执行：确认开始，我会提供论文摘要和方法说明。`
2. `请使用**paper-framework-figure-studio-pro**，根据当前状态，提供下一步提问建议。`
