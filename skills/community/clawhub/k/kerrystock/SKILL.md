---
name: Kerrystock
description: >
  个股/ETF 的「日历效应（季节性）买卖点分析」端到端工作流。当用户要求分析某只股票或基金的
  月度/年度季节性规律、确定基于日历效应的买入卖出时间点与买卖策略、或做"季节性 + 技术指标"
  复合选股时使用本技能。本技能串联 westock-data（行情/技术指标/投资日历）、
  neodata-financial-search（历史区间涨跌幅交叉验证）、wb-finance-skill 的 seasonality.py
  （季节性信号引擎）与 trade-plan 框架（买卖点：位置判断→分仓→止盈止损→失效条件），
  最后用 westock-tool 按策略信号选股。This skill should be used when the user asks for
  calendar/seasonal effect analysis, buy/sell timing, or seasonal+technical stock screening.
agent_created: true
---

# Kerrystock — 日历效应买卖点分析工作流

对单只标的（A股/港股/美股个股、ETF、基金）执行「日历效应 → 买卖点」的全链路分析。
核心思想：**先用标的自身的历史数据算出真实的月度/年度季节性，再据此定买卖时间点，而不是套用通用经验月份**。

## 依赖技能（运行时经 Skill 工具加载）

| 步骤 | 技能 | 用途 |
|---|---|---|
| 1 | `westock-data` | 拉 K 线、技术指标（MACD/KDJ/RSI/BOLL）、投资日历/财报披露 |
| 2 | `neodata-financial-search` | 交叉验证历史区间涨跌幅、季节性强弱、研报观点 |
| 3 | `wb-finance-skill` | `scripts/quant/seasonality.py` 的 `SignalEngine` 生成日历信号 |
| 4 | `wb-finance-skill` | `references/trade-plan.md` 买卖点框架（位置→分仓→止盈止损→失效） |
| 5 | `westock-tool` | 按策略信号选股（如 `macd_golden` + 日历效应时段） |

## 五步工作流

### 步骤 1 — 拉行情与基础数据（westock-data）
- 日线导出（供步骤3）：用本技能 `scripts/export_kline.py`
  ```bash
  python3 <skill>/scripts/export_kline.py --code sh601138 --start 2018-01-01 --end 2026-07-18 --out 601138_day.csv
  ```
  > 脚本自动分段（每段约2年）规避 westock-data day K 上限（约2000条），解析 markdown 表（`last`=收盘价）并合并为 CSV。
  > 路径可通过环境变量覆盖：`WESTOCK_DATA_SCRIPT`（指向 westock-data 的 index.js）、`NEODATA_SCRIPT`（指向 neodata 的 query.py）、`WB_FINANCE_QUANT_DIR`（指向 wb-finance-skill 的 quant 目录）、`NODE_BIN`（默认 managed node）。未设置时由 `scripts/common.py` 自动探测常见安装位置。
- 技术指标截面（当前状态）：`westock-data technical sh601138 --group macd,kdj,rsi,boll` → 保存为 JSON 供步骤4报告。
- 财报披露日历：`westock-data disclosure sh601138`（确认中报/年报窗口，作为事件催化点）。

### 步骤 2 — 交叉验证季节性（neodata-financial-search）
用本技能 `scripts/neodata_verify.py`（已封装凭证坑，强制 `--token` 直传，不踩 `--save-token` 写入失败）：
```bash
# 1) 先经 connect_cloud_service 工具拿到临时 token（约24h有效）
# 2) 再跑验证（建议显式要"逐月/区间涨跌幅数值"）
python3 <skill>/scripts/neodata_verify.py \
  --query "601138 自上市以来每一年度 1-12 月涨跌幅 季节性统计 哪个月胜率高" \
  --token <tempToken> --out verify_601138.md
```
> 用于核对「真实月收益/胜率」与步骤3自算结果是否一致，并补充研报观点、业绩趋势。
> 凭证坑与参数细节见 `references/lessons.md` 第二节；neodata 路径可用 `NEODATA_SCRIPT` 覆盖。

### 步骤 3 — 跑季节性信号引擎（wb-finance-skill·seasonality.py）
用本技能 `scripts/seasonal_analysis.py`（内部 import `seasonality.SignalEngine`）：
```bash
python3 <skill>/scripts/seasonal_analysis.py --csv 601138_day.csv --out-json seasonal_stats.json --out-csv seasonal_stats.csv
```
- 脚本计算**月度 close-to-close 收益**，按月份统计 `n / 均值 / 中位数 / 胜率`；
- **判定规则**（可调）：胜率 ≥ `--win 0.55` 且均值 >0 → 做多月份；胜率 ≤ `--lose 0.45` 且均值 <0 → 回避月份；
- 同时输出**年度收益**、历史高低点、以及 `SignalEngine` 的日线信号统计（做多/做空/观望天数）。
- 输出 `seasonal_stats.json` 供步骤4生成报告。

### 步骤 4 — 定买卖点（trade-plan 框架）
依据 `wb-finance-skill` 的 `references/trade-plan.md`，按以下顺序输出买卖点计划：
**位置判断 → 分仓（试错仓/确认加仓）→ 止盈止损 → 失效条件 → 事件窗口**。
详细框架模板与本技能的判定/配色约定见 `references/workflow.md`。
用本技能 `scripts/gen_report.py` 生成可视化 HTML 研报（月度/年度/日历三图 + 技术面板 + 策略表）：
```bash
python3 <skill>/scripts/gen_report.py --stats seasonal_stats.json --tech tech.json --name 工业富联 --code sh601138 --out 研报.html
```
> ETF/LOF 用 `--label 价`、场外基金用 `--label 净值`，使研报"最新价/净值"表述准确（股票默认"收盘"）。

### 步骤 5 — 按策略信号选股（westock-tool）
将日历效应时段与技术指标信号结合，做复合选股。典型命令：
```bash
# 策略信号（如 MACD 金叉）
westock-tool strategy macd_golden
# 在 MACD 金叉信号内，按估值二次排序（找到"金叉+低估值"的标的）
westock-tool ranking fin_valuation --within-strategy macd_golden
# 自定义条件（如 PE>0 且 PE<20 且 ROE>15）
westock-tool filter "intersect([PE_TTM>0, PE_TTM<20, ROETTM>15])"
```
> 选股命令需经 `westock-tool` 技能加载后执行；实时策略/标签/事件清单用 `strategy --list` / `label --list` / `event --list` 获取，勿凭记忆。

## ETF / 基金适配

场内 ETF 与 LOF（如 `sh510300` 沪深300ETF、`sz161725` 招商中证白酒LOF）的 K 线格式与股票**完全一致**（含 open/high/low/last/volume），脚本**无需特殊改动**即可直接分析。

- **代码格式**：ETF/LOF 需带市场前缀。脚本 `--code` 支持纯数字自动补前缀（沪 5/6/9→`sh`、深 0/1/2/3→`sz`）；歧义或指数/北交所用 `--market sh|sz` 显式指定。
  ```bash
  # 以下等价：自动补 sz 前缀
  python3 <skill>/scripts/export_kline.py --code 161725 --start 2015-06-01 --end 2026-07-18 --out 161725_day.csv
  python3 <skill>/scripts/export_kline.py --code sz161725 --start 2015-06-01 --end 2026-07-18 --out 161725_day.csv
  ```
- **场外基金（无场内交易，仅单位净值）**：westock-data 无 K 线，改用 neodata 拉净值序列存为 CSV（列 `Date,close`，缺失的 `open/high/low` 用 close 填充、`volume` 填 0），直接喂给步骤3/4。脚本已对缺失 OHLC 做"用 close 填充"的降级兼容。
  ```bash
  # 场外基金净值CSV（Date,close 两列即可）
  python3 <skill>/scripts/seasonal_analysis.py --csv fund_nav.csv --out-json stats.json --out-csv stats.csv
  python3 <skill>/scripts/gen_report.py --stats stats.json --daycsv fund_nav.csv --name 某基金 --code xxx --label 净值 --out 研报.html
  ```
- **报告标签**：ETF/LOF 用 `--label 价`、场外基金用 `--label 净值`，使研报"最新价/净值"表述准确（股票默认"收盘"）。
- **注意**：基金跟踪指数/板块，其日历效应往往体现为**所跟踪标的的季节性**（如白酒LOF≈白酒板块、沪深300ETF≈大盘季节性），分析时需结合跟踪标的的基本面。

## 关键约定与坑位

- **踩坑与经验教训汇总见 `references/lessons.md`**（数据源坑、neodata 凭证坑、BOLL 口径、默认月份禁用等），本技能迭代与排错优先阅读。
- **中国配色**：涨=红、跌=绿（与欧美相反）。图表与买卖信号一律遵守。
- **季节性是辅助，不是主信号**：对强趋势/强基本面标的（如 AI 龙头），须以"业绩+趋势+事件"为主、日历规律为辅。
- **不要用 seasonality.py 的默认 bullish/bearish 月份直接套单只**：默认值是 A股通用经验（[1,2,3,11,12]多 / [5,6,7,8,9]空），必须用步骤3用标的自身数据算出的真实月份。
- **样本偏差**：上市较晚或历史短的标的，某月样本数可能很少（如仅1~2次），结论置信度低，须在报告中标注 `n`。
- 所有数据为客观市场数据，**不构成投资建议**；输出须带风险提示。

## 引用文件
- `scripts/export_kline.py` — 步骤1 K线导出
- `scripts/neodata_verify.py` — 步骤2 季节性交叉验证（封装 neodata 凭证坑）
- `scripts/seasonal_analysis.py` — 步骤3 季节性统计 + 信号引擎
- `scripts/gen_report.py` — 步骤4 研报生成
- `references/workflow.md` — 判定规则、trade-plan 模板、配色与报告规范
- `references/lessons.md` — 经验教训与踩坑记录（数据源/凭证/BOLL口径/默认月份等）
