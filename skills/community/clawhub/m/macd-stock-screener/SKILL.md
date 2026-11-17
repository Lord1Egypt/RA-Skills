---
name: macd-stock-screener
version: 1.0.0
description: "A股左右侧MACD选股筛选器，含东方财富股吧舆情采集与情感分析报告。当用户需要扫描全市场MACD金叉信号、MACD选股、左右侧策略选股、MACD即将金叉筛选时使用此skill。支持右侧MACD金叉选股（DIF上穿DEA）和左侧MACD即将金叉选股（DIF在DEA下方但差距收敛）。不含回测。"
agent_created: true
---

# A股左右侧MACD选股 + 股吧舆情

## 概述

本 skill 封装了 A 股全市场 MACD 选股 + 东方财富股吧舆情采集的完整流程：

1. **选股** — 扫描沪深两市全部正常交易股票，分别筛选：
   - **右侧MACD金叉**: DIF 上穿 DEA，明确的多头信号
   - **左侧MACD即将金叉**: DIF 仍在 DEA 下方，但差距在连续缩小且 MACD 柱状图负值收窄，预判拐点
2. **舆情采集** — 对候选股票采集东方财富股吧最新动态与评论数（内置随机延时，验证码检测自动中止）
3. **报告生成** — 产出 CSV 候选列表、情感分析报告、每日汇总

## 触发场景

- 用户说「跑一下MACD选股」「选股」「MACD金叉」「左侧选股」「右侧选股」
- 用户需要每日例行 MACD 选股
- 自动化任务触发选股流程

## 使用方式

### 直接运行独立脚本

脚本路径为 skill 目录下的 `scripts/macd_screener.py`。

```bash
# 完整流程：选股 + 舆情采集 + 报告生成（右侧+左侧，各10只）
python <skill-dir>/scripts/macd_screener.py

# 自定义数量
python <skill-dir>/scripts/macd_screener.py -n 15

# 仅运行右侧金叉
python <skill-dir>/scripts/macd_screener.py --right-only

# 仅运行左侧即将金叉
python <skill-dir>/scripts/macd_screener.py --left-only

# 仅选股不采集舆情
python <skill-dir>/scripts/macd_screener.py --scan-only

# 跳过舆情采集
python <skill-dir>/scripts/macd_screener.py --skip-sentiment

# 指定输出目录
python <skill-dir>/scripts/macd_screener.py -o ./my_output/
```

### 在 WorkBuddy 中触发

当用户表示需要 MACD 选股时，找到 `scripts/macd_screener.py` 的绝对路径并运行它。

### 产出文件

在 `outputs/YYYY-MM-DD/` 目录下生成：
- `right_macd_candidates.csv` — 右侧金叉候选列表（含收盘价、评论数）
- `left_macd_candidates.csv` — 左侧即将金叉候选列表（含收盘价、DIF-DEA差距、评论数）
- `sentiment_report.md` — 股吧舆情情感分析报告
- `summary.md` — 每日选股汇总

## 舆情采集说明

- 数据来源：东方财富股吧（`ak.stock_comment_em`）
- 每条采集之间随机延时 2-5 秒，避免触发反爬
- 检测到验证码自动中止全部采集并留痕
- 采集内容：最新动态、相关资讯、评论数

## 策略参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| 快线周期 (fast) | 12 | EMA 快线 |
| 慢线周期 (slow) | 26 | EMA 慢线 |
| 信号线周期 (signal) | 9 | DEA 平滑 |
| 最低历史数据 | 30 日 | 数据不足则跳过 |
| 左侧回看窗口 (lookback) | 3 日 | 连续收敛判断窗口 |
| 前复权 | qfq | 价格校准方式 |
| 排除范围 | ST/\*ST/退市/北交所 | 仅保留沪深创主板 |

## 依赖

```bash
pip install akshare pandas numpy
```

## 注意事项

- 全市场扫描约 5000+ 只股票，选股阶段需要数分钟（内置随机延时 0.1-0.3 秒）
- 舆情采集阶段每只股票额外 2-5 秒延时，20 只候选约需 1-2 分钟
- 仅在交易日运行有效，非交易日返回无结果
- MACD 金叉为滞后信号，右侧策略确认性强但进场偏晚；左侧策略预判拐点但假信号较多
