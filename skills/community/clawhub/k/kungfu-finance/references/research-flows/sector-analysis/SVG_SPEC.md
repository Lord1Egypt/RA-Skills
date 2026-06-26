# Sector Research SVG Spec

这是当前 `kungfu_finance` 对 `sector-analysis/SVG_SPEC.md` 的 repo-controlled 收口版本。

## Current Output Contract

当前 `sector-research` 结果面必须同时输出：

- `report_markdown`
- `report_svg`

当前 `report_svg` 属于 `markdown_svg_preview` 阶段，但已经纳入当前仓库的质量门禁。

## Required SVG Elements

1. 标题区
2. 至少 4 个阶段标签，且带时间范围
3. 主曲线
   - 必须以板块/概念指数窗口为基准
4. 副曲线
   - 当前版本优先使用流动性/辅助趋势线
5. 推演线
6. NOW 标记
7. 一体化情绪条
8. 方向判断框
9. 数据气泡
   - 至少 4 个
10. 底部摘要

## Explicit Non-Goals

- 当前版本不承诺 source skill 的全部像素级布局和全部数据气泡品类。
- 当前版本不输出仓位、买卖点、追高建议等交易指令。
- 当前版本不把相似板块、资金流、外部搜索缺口伪装成“已完成”。

## Validation

当前仓库以自动化 quality gate 为准，见 `quality_gate/README.md`。
