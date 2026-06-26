# Sector Research Eval Baseline

这是当前 `kungfu_finance` 对 `sector-analysis/EVAL.md` 的 repo-controlled 最小可执行基线。

## Judge Dimensions

当前保留以下 5 个一级维度：

- structure
- logic
- facts
- risk
- svg

## Current Executable Baseline

当前可执行 eval baseline 由两部分组成：

1. `sector-research` integration tests
2. repo 内质量门禁校验器

## Scenario Baseline

沿用 source skill 的 6 类典型赛道场景作为设计基线，但当前仓库 first executable eval 不在同轮恢复完整 case runner 与 LLM judge。

## Pass Condition

- `report_markdown` 通过结构门禁
- `report_svg` 通过 SVG 门禁
- research flow 主路径测试通过

## Follow-up

若后续要恢复完整场景评测、Judge 评分器和辩论审计，需要新开 follow-up ExecPlan。
