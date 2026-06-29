---
name: hekouwang-stock-data-reader-skill
description: >
  会勇禾口王 · 个股公开数据速读 Skill。输入一个 A 股代码，自动用 akshare 拉取「资金流 /
  龙虎榜 / 估值band / 财务三表 / 主营构成 / 北向 / 日K」等公开数据，算出固定指标体系
  （价格轨迹·主力进出·席位结构·利润质量·利润结构·估值·风险线索），并产出「中立事后复盘」
  形态的财经贴图 / 公众号长文 / 头条三件套（V2 米白或 V3 财经风）。内置金融合规护栏：
  不荐股、不预测涨跌、不给买卖点，自动套风险提示条。
  触发词：个股数据速读 / 扒公司公开数据 / 资金面复盘 / 出个股报告 / 3天一只 /
  stock-data-reader / 给我一只股的数据体检 / 用 akshare 拉某股数据。
  ⚠️ 个股报告只走财经账号公众号/头条，绝不上小红书主账号。
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
---

# 个股公开数据速读 · Skill

把一个股票代码，变成一份「机构观感、但合规中立」的公开数据复盘。是工厂 B 财经栏目「3 天一只」的发动机，也是可对外售卖的工具。

**核心价值（差异化）**：借鉴 `daily_stock_analysis` 的多源数据层思路，但走第三条路——① 挖**资金博弈内核**（主力拉高出货 / 龙虎榜席位 / 北向 / 分部毛利），不是新闻级价格+财报摘要；② **合规护栏内置**（不荐股/不预测/风险条），是唯一能「公开发布且不踩金融红线」的个股分析产出器；③ **数据→可发布图文一条龙**（出版级贴图/长文/头条），不是丢一堆 JSON。详见 README「核心价值」。

## 0. 合规第一（必先读 `references/compliance.md`）
- **不荐股、不预测、不给买卖点**；每份报告文末固定风险提示条。
- 个股内容**只走公众号/头条**，**不上小红书**（小红书只发零金融词的纯方法科普）。
- 命中红线（买入/卖出/目标价/翻倍/上车…）→ 停下改写。

## 1. 三步工作流
```
python3 scripts/fetch.py <代码> [out目录]     # 取数 → out/<代码>/*.csv + _report.json
python3 scripts/analyze.py out/<代码>          # 算指标 → out/<代码>/analysis.json
python3 scripts/build_report.py out/<代码>     # 据 analysis.json 出贴图初稿（数字已对）
node templates/screenshot.js <贴图目录>        # 截图 output/，出图即删 HTML
```
`build_report.py` 出的是**数字正确的初稿**；中立复盘文案由人/LLM 按 `references/report-structure.md` 润色后再截图交付。

## 2. 指标体系（栏目固定，见 report-structure.md）
价格/市值/估值轨迹 · 主力资金进出（含"涨着出货"类反差日）· 龙虎榜席位结构（通道盘 vs 机构长线）· 利润质量（净利 vs 经营现金流）· 利润结构（分部收入 vs 毛利占比）· 资产负债 · 风险线索。

## 3. 数据源与踩坑
- akshare（乐咕估值 / 东方财富资金流·龙虎榜 / sina 财报·日K）。免费、无需 key。
- 日K走 sina 源（`stock_zh_a_daily`）避开 eastmoney `push2his`（受限网络常被挡）。
- `fetch.py` 已清代理环境变量兜底；筹码 `stock_cyq_em` 在受限网络可能拿不到（非核心）。
- 营销号数字常错，一律以 akshare 财报/乐咕口径为准。

## 4. 视觉与产出
- 默认 **V2 米白**（黏土主色），财经可选 V3 Google 财经风。字体统一黑体。
- 贴图复用「会勇禾口王内容工厂」流水线（`_build.py` + `screenshot.js`，出图即删）。
- 字体依赖 `hekouwang-content-factory/assets/fonts/`（Anthropic Sans/Mono + 思源黑体 CDN）。
  对外发布版需把字体路径改成相对内嵌（见 templates 注释）。

## 5. 加一只新股（3 天一期）
1. `python3 scripts/fetch.py <新代码>`
2. `python3 scripts/analyze.py out/<新代码>`
3. 复制 scripts/build_report.py 到选题目录，按 analysis.json 出初稿 → 润色 → 截图。
4. 套合规框架，发公众号 + 头条；建 `发布记录.md` 回填数据。

## 6. 文件
- `scripts/fetch.py` — 取数引擎（任意代码）
- `scripts/analyze.py` — 指标计算 → analysis.json
- `scripts/build_report.py` — 据指标出 8 贴图初稿（V2 米白）
- `templates/screenshot.js` — 1080×1350 @2x 截图，出图即删
- `references/compliance.md` — 金融合规护栏（先读）
- `references/report-structure.md` — 栏目固定报告结构
- `requirements.txt` — akshare + pandas

## 7. 案例
首版样例：利通电子 603629（`Pi.dev/利通电子/litong-0619/`，公众号长文+8贴图、头条三件套）。
