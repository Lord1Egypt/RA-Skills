# Stock Research Eval Baseline

这是当前 `kungfu_finance` 对 `stock-analysis-v2/EVAL.md` 的 repo-controlled 最小可执行基线。

## Judge Dimensions

当前仓库保留以下 5 个一级维度：

- structure
- logic
- facts
- risk
- svg

## Current Executable Baseline

当前不在仓库里直接落完整 LLM-as-Judge pipeline。
当前可执行 eval baseline 由两部分组成：

1. research flow integration tests
   - 生成真实 `report_markdown` / `report_svg`
2. quality gate validators
   - 对报告结构和 SVG 核心元素做自动化断言

## Scenario Baseline

当前沿用 source skill 的 6 类典型场景作为设计基线，但本仓库 first executable eval 不在同轮实现完整 case runner。

## Pass Condition

- `report_markdown` 通过结构门禁
- `report_svg` 通过 SVG 门禁
- research flow 主路径测试通过

## Follow-up

若后续要恢复完整 `LLM-as-Judge`、场景化评测集与辩论分布审计，应新开 follow-up ExecPlan，不在本文件中隐式承诺。
