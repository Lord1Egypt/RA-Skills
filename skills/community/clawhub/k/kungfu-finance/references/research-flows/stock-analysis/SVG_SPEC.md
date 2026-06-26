# Stock Research SVG Spec

这是当前 `kungfu_finance` 对 `stock-analysis-v2/SVG_SPEC.md` 的 repo-controlled 收口版本。

## Current Output Contract

当前 `stock-research` 结果面必须同时输出：

- `report_markdown`
- `report_svg`

`report_svg` 当前为 `markdown_svg_preview` 阶段，但已经进入可测试、可门禁的正式控制面。

## Required SVG Elements

以下元素属于当前仓库的硬性门禁：

1. 标题区
   - 公司名、代码、分析日期、综合评级
2. 阶段标签
   - 至少 4 个 `阶段X: 名称 (时间范围)` 标签
3. 主曲线
   - 基于价格窗口的真实主线
4. 副曲线
   - 当前版本优先使用财务/辅助趋势线
5. 推演线
   - 当前价格之后的单条主推演线
6. NOW 标记
   - 包含 `📍 NOW` 与日期
7. 估值区间
   - 高估 / 合理 / 低估
8. 历史极值标注
   - 至少一个高点和一个低点
9. 数据气泡
   - 至少 6 个
10. 综合评级框
11. 底部数据摘要

## Explicit Non-Goals

- 当前版本不承诺 source skill SVG 的全部像素级布局细节。
- 当前版本不输出具体仓位、建仓、加仓、目标价、买卖指令。
- 当前版本不把待补适配器伪装成已接入元素。

## Validation

当前仓库以自动化 quality gate 为准，见 `quality_gate/README.md`。
