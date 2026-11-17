# 输出模板索引（output-templates-index）

> 各场景的完整输出模板在仓库对应 Skill 的 `references/` 下。命中场景后按需读取，产出对齐全仓库格式。

| 场景（Skill id） | 模板位置（仓库内路径） | 关键格式要求 |
|---|---|---|
| 五维深度分析 `stock_5d_deep_analysis` | `skills/subject_analysis/stock_5d_deep_analysis/references/output-template.md` | 核心摘要→五维逐维→可选同业对标→综合评价→来源→免责 |
| 对比分析 `stock_comparative_analysis` | `skills/subject_analysis/stock_comparative_analysis/SKILL.md`（含输出规范） | 公司/基本面/技术面/资金面/消息面；MD+HTML（可选 PDF） |
| 行业速报 `industry_brief` | `skills/macro_event/industry_brief/references/EXAMPLE_OUTPUT.md` | 六段式速报；信号规则带证据链 |
| 主题产业链 `concept_chain_analysis` | `skills/macro_event/concept_chain_analysis/references/output-template.md` | 上中下游分层作战图 + 核心/弹性/补涨 + 风险 |
| 市场热点 `market_hotspot` | `skills/macro_event/market_hotspot/references/output-template.md` | 七大模块；MD/HTML 双格式 |
| 政策解读 `policy_interpret` | `skills/macro_event/policy_interpret/references/EXAMPLE_OUTPUT.md` | 政策原文+结构化分析；可溯源角标 |
| 舆情风险 `sentiment_risk_warning` | `skills/macro_event/sentiment_risk_warning/SKILL.md`（输出节） | 大盘/个股双模式；风险分级+风险分 |
| 底部信号 `a_share_bottom_monitor` | `skills/macro_event/a_share_bottom_monitor/references/decision-rules.md` | 状态/路径/执行三层；结论前置+唯一动作 |
| 政策底 `policy_bottom_monitor` | `skills/macro_event/policy_bottom_monitor/references/methodology.md` | S/A/B/C/D 双轴分级 + 量价叠加 |
| 宏观分析 `macro_analysis` | `skills/macro_event/macro_analysis/assets/sample_report.md` | 一句话结论→景气定位→五维证据→行业超低配表 |
| 每日收评 `market_daily_review` | `skills/market_review/market_daily_review/references/output-template.md` | 十段式；全字段溯源+降级标记 |
| 隔夜复盘 `overnight_review` | `skills/market_review/overnight_review/references/report-template.md` + `.html` | Bloomberg 五件事+主线分歧+常驻决策时间线；MD+自包含 HTML |
| 量化选股 `racing_quant_pick` | `skills/quant_strategy/racing_quant_pick/SKILL.md`（输出节） | 选股池+策略画像；可衔接个股分析 |
| 激进成长 `aggressive_growth_strategy` | `skills/subjective_strategy/aggressive_growth_strategy/SKILL.md` | 道法术器；八步分析+A+~D 评级 |

## 通用输出骨架（模板缺失时兜底）
1. 核心结论（前置，明确标注事实/观点）
2. 分析主体（按方法论框架分节）
3. 数据附录（来源与时间、降级轨迹、缺失项）
4. 风险提示与失效条件
5. 完整免责声明（不可简化）

## 交付规范
- 同时产出 Markdown 与**自包含 HTML**（图表内嵌 data URI，无本地路径依赖，可离线打开）。
- 落盘 `files/report/{主题}_{YYYYMMDD}_投研分析.md/.html`。
- 每个数值带来源角标与时间戳；事实与观点分层。
