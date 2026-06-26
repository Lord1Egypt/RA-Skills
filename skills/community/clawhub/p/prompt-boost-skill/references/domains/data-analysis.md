# 数据分析领域（data-analysis）

## 识别特征
问题涉及：数据分析、指标归因、报表设计、BI、SQL、Python（Pandas）、可视化、趋势分析等。

## 任务类型
- root-cause-analysis：归因分析
- dashboard-design：报表设计
- exploratory-analysis：探索性分析
- metric-design：指标设计

## 必要槽位
| 槽位 | 说明 |
|------|------|
| analysis_goal | 分析目标 |
| data_source | 数据来源 |
| time_range | 时间范围 |
| metrics | 核心指标 |

## 常见缺失项
- 数据范围（近一周/一月/一年）
- 分析的受众（管理层/运营执行层）
- 输出形式（分析框架/SQL/图表/汇报材料）
- 指标口径定义

## 追问模板
1. "你这次最想解释的波动指标是什么？"
2. "数据范围是近一周、近一月还是近一年？"
3. "最终是给管理层看结论，还是给运营执行层看明细？"

## Rewrite 模板
请以资深数据分析师视角，围绕【{analysis_goal}】，基于【{time_range}】内的【{metrics}】指标，结合【{data_source}】输出结构化分析方案。请给出分析思路、拆解维度、验证方法、图表建议与结论框架。
