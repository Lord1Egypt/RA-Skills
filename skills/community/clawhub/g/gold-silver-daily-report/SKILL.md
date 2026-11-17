---
name: gold-silver-daily-report
description: 生成「黄金 + 白银每日行情日报」交互式 HTML 研报。This skill should be used when the user asks for a daily gold/silver market report, 贵金属每日行情日报, 黄金白银行情速览, or wants an HTML deliverable covering spot gold/silver prices, domestic T+D & futures, macro indicators (DXY / TIPS / FedWatch / oil), gold-silver ratio (GSR), institutional targets, and a bull/bear conflict summary. 方法论固化自两周迭代验证的增强模板（结论前置 + 三图仪表盘）。不含飞书上传流程。
agent_created: true
---

# Gold Silver Daily Report（黄金白银行情日报）

## Overview

本 Skill 把"每日黄金白银行情日报"的完整生产流程固化成一个可复用、可分享的工作流：联网检索当日真实行情 → 按固定增强模板渲染成一份交互式 HTML 研报（含 ECharts 三图仪表盘）。输出一份统一、自包含的 HTML 文件，便于本地查看或二次分发。

**设计取舍**：本 Skill 刻意**不含**飞书/云盘上传步骤——研发报只负责"生成"，分发交给你自己的工具链。若需备份，可在生成后自行处理。

## When To Use

- 用户说"生成今天的黄金白银行情日报""来一份贵金属每日速览""做个黄金白银 HTML 研报"。
- 用户要一份含现货价、国内 T+D/期货、宏观指标、金银比、机构目标价、多空矛盾的结构化日报。
- 注意：若用户只要"趋势分析"而非"每日固定模板日报"，可改用 `precious-metal-trend-analysis`；本 Skill 专注"固定十节 + 结论前置 + 三图仪表盘"的日报形态。

## Workflow

### Step 1 — 联网检索当日真实数据（必须，不得捏造）

并行检索以下维度，优先选用可交叉验证的实时源（金投网、金十数据、财联社、同花顺、Wind、tradingeconomics、SGE 延时行情、cngold、T-GolDream、IndexMundi、FRED）：

1. **国际现货**：XAU / XAG 最新价（USD/oz）、涨跌幅、昨收、日内高/低、所在盘面（亚盘盘中 / COMEX 收盘）。
2. **国内盘面**：Au T+D、Ag T+D、沪金主力、沪银主力（最新价/涨跌/最高/最低/昨收）。
3. **宏观**：DXY、USD/CNY、10Y 美债、10Y TIPS 实际收益率（**金价核心压制变量，必查必列**）、WTI / Brent、CME FedWatch 加息概率。
4. **央行购金**：中国央行连续增持月数、最新环比、WGC 央行调研。
5. **机构目标价**：高盛 / 小摩 / 花旗 / 瑞银 / 大摩 / 德银（**必须标注是否已下调及幅度**）。
6. **金银比**：当日 GSR = 现货金 ÷ 现货银。

**数据铁律**：
- 人民币折算价 ≠ 国内 T+D，两者并列、不强行统一。公式：`美元价 × 汇率(USD/CNY) ÷ 31.1035`。
- 遇自相矛盾或时间戳在未来/异常的数据，剔除并保留多源一致的读数，正文注明口径。
- 「地缘冲突 → 油价 → 通胀 → 加息预期 → 实际利率↑ → 金银跌」的反向传导链优先解释行情。
- 白银分析必讲「光伏去银化」工业逻辑：银包铜/电镀铜使单瓦耗银 −30%~50%，2026 光伏用银预计 −10%~19%。
- 风险提示固定 5 条：政策超预期 / 地缘反复 / 白银高波动 / 国内流动性 / 数据噪声。

### Step 2 — 构建金银比半年序列

调用 `scripts/build_gsr_series.py` 生成近半年（约 1/21–当日）真实序列，输出一段 `<script>` 片段（含 `dates`、`values`、均值 `mean`）。

- 早期（1 月–6 月中）基于真实月度均值（T-GolDream / IndexMundi）与关键极值周度重建：1/29 低点 ≈45（格林大华期货半年报）、5 月低点 ≈54、6/21 低点 64.05、7/17 高点 72.05。
- 6/18 起尽量用真实日度值；末尾接当日 GSR。
- 半年均值随序列重算，均值线与该值一致；半年最低/最高取真实极值。
- 详见 `references/data_sources.md`。

### Step 3 — 渲染 HTML 研报

基于 `assets/report_template.html`（已含 CSS 配色、ECharts CDN、三图仪表盘结构、十节占位、图表脚本骨架）填充当日数据：

- **最简做法**：直接读取模板，把各 `{{占位符}}` 替换为当日真实数据，并把 Step 2 的 GSR 片段与近 90 天黄金双向价格 JSON 注入脚本区，写出 `黄金白银日报-YYYY-MM-DD.html`。
- **脚本化做法**：调用 `scripts/generate_report.py`，传入当日数据 JSON（检索结果 + GSR 片段 + 90 天价格序列），由脚本完成占位替换与写出。

**报告结构（固定，统一一份，禁止出现"原日报/模板新增/增强版"等来源标注）**：
1. 标题 + 日期 + 数据截止时间
2. **简明结论与风险提示（速览）置于最前**（金边高亮）：结论段 + 固定 5 条风险 + 免责声明
3. **核心图表仪表盘**（紧跟结论）：① 黄金人民币单价（沪金主力连续，元/克）② 黄金美元单价（COMEX，USD/oz）③ 金银比近半年（含均值线与当前线）；黄金两图为近 90 交易日、含 dataZoom 与最高/最低标记
4. 一、核心数据一览（国际现货）
5. 二、国内 T+D 与期货
6. 三、关键比率与宏观指标
7. 四、金银比（大数字 + 半年低/均/高；图表已并入仪表盘③，正文仅留指路说明）
8. 五、黄金走势关键驱动因素（TIPS / 美元 / 央行购金 / 地缘反向链）
9. 六、白银走势特征（金银比视角 / 光伏去银化 / 结论）
10. 七、近期核心矛盾（利多 vs 利空）
11. 八、主流机构最新目标价
12. 九、后续关键指标与价位（事件日历 + 支撑阻力）

完整模板规范见 `references/template_spec.md`。

### Step 4 — 校验与交付

- 校验：涨红跌绿（中国习惯，红 `#c0392b` / 绿 `#27ae60`）；金 `#e8c547`、深蓝 `#1a1a2e`；响应式。
- 在浏览器/预览中确认三图渲染正常、GSR 半年线均值/当前线标注正确。
- 写出文件：`黄金白银日报-YYYY-MM-DD.html`（默认工作区根目录）。本 Skill 不自动上传任何云盘。

## Resources

- `assets/report_template.html` — HTML 骨架（CSS + 仪表盘 + 十节占位 + ECharts 脚本模板），主渲染基底。
- `scripts/build_gsr_series.py` — 生成金银比近半年序列的 `<script>` 片段。
- `scripts/generate_report.py` — 传入当日数据 JSON，渲染并写出最终 HTML。
- `references/template_spec.md` — 十节模板逐节要素与措辞规范。
- `references/data_sources.md` — 各数据维度的推荐数据源与口径说明（含 GSR 半年重建法）。
