---
name: marcus-investment-analyst
description: Marcus 投资分析技能 - 基于缠论+MACD+RSI 的 A 股投资策略。用于股票分析、回测、投资建议。触发词：分析股票、回测策略、投资建议、Marcus 策略。
license: MIT
---

# Marcus 投资分析技能

**版本**: v6.0  
**策略类型**: 缠论+MACD+RSI+ 追踪止损

---

## 🎯 何时使用

使用此技能当用户需要：
1. 分析 A 股股票（技术指标、缠论中枢、买卖点）
2. 执行策略回测（历史数据验证）
3. 获取投资建议（仓位配置、行业配置）
4. 下载/更新股票指标数据（MACD、RSI、KDJ）

---

## 📋 核心策略参数

```yaml
策略名称：优化版 5-存储芯片专用

缠论中枢:
  周期：60 日均线
  区间：±8%

MACD:
  快线：12
  慢线：26
  信号：9

RSI:
  周期：6
  超卖：20
  超买：80

止损止盈:
  止损：5%
  止盈：15%
  追踪：8%
```

---

## 📈 买入条件 (需同时满足)

1. ✅ 价格在缠论中枢内 (60 日均线×0.92 ~ 60 日均线×1.08)
2. ✅ MACD 金叉 (DIF 上穿 DEA)
3. ✅ RSI6 < 20 (超卖)

---

## 📉 卖出条件 (满足任一)

1. ❌ 盈利 ≥ 15% (止盈)
2. ❌ 亏损 ≥ 5% (止损)
3. ❌ 从最高点回撤 ≥ 8% (追踪止损)
4. ❌ MACD 死叉 (DIF 下穿 DEA)
5. ❌ 价格跌破中枢下沿

---

## 🎯 股票池 (20 支)

### 核心配置 (55-60%)
| 股票 | 代码 | 行业 | 仓位 |
|------|------|------|------|
| 江波龙 | 301308 | 存储芯片 | 25-30% |
| 兆易创新 | 603986 | 存储芯片 | 20-25% |

### 卫星配置 (25-30%)
| 股票 | 代码 | 行业 | 仓位 |
|------|------|------|------|
| 东山精密 | 002384 | 消费电子 | 10-15% |
| 金风科技 | 002202 | 风电 | 10% |
| 四方精创 | 300468 | 软件 | 10% |
| 云天化 | 600096 | 化工 | 8% |
| 宝丰能源 | 600989 | 化工 | 8% |
| 万向钱潮 | 000559 | 汽配 | 5% |
| 中国铝业 | 601600 | 有色 | 5% |

### 回避
- 广汇能源 (600256)
- 创新医疗板块

---

## 🚀 使用脚本

### 1. 运行策略回测

```bash
cd /root/.openclaw/workspace/skills/marcus-investment-analyst/scripts
python3 marcus_ultimate_optimized_strategy.py
```

**输出**: 20 支股票的回测结果，包含收益、夏普比率、胜率

### 2. 缠论分析单只股票

```bash
python3 marcus_chan_theory.py <股票代码>
# 示例：python3 marcus_chan_theory.py 301308
```

**输出**: 缠论中枢、背驰、买卖点分析

### 3. 缠论回测

```bash
python3 marcus_backtest_chan.py <股票代码>
# 示例：python3 marcus_backtest_chan.py 301308
```

**输出**: 缠论策略历史回测结果

### 4. 下载指标数据

```bash
python3 data_indicator_fetcher.py
```

**输出**: 更新 MACD/RSI/KDJ 指标到数据库

---

## 📊 回测表现 (2023-2026)

| 指标 | 数值 |
|------|------|
| 平均年化收益 | 21.96% |
| 夏普比率 | 0.56 |
| 胜率 | 75.0% |
| 用户股票平均 | 28.77% |

---

## 📁 文件结构

```
marcus-investment-analyst/
├── SKILL.md                    # 本文件
├── scripts/
│   ├── marcus_ultimate_optimized_strategy.py  # 主策略
│   ├── marcus_chan_theory.py                  # 缠论分析
│   ├── marcus_backtest_chan.py                # 缠论回测
│   └── data_indicator_fetcher.py              # 指标下载
├── references/
│   ├── strategy.md                            # 策略文档
│   └── optimization_report.md                 # 优化报告
└── assets/
    └── backtest_data.json                     # 回测数据
```

---

## 💡 使用示例

### 示例 1: 分析股票

**用户**: "分析一下江波龙"

**操作**:
1. 读取 `references/strategy.md` 获取股票池信息
2. 运行 `python3 marcus_chan_theory.py 301308`
3. 返回缠论分析结果

### 示例 2: 回测策略

**用户**: "回测一下 Marcus 策略"

**操作**:
1. 运行 `python3 marcus_ultimate_optimized_strategy.py`
2. 读取 `assets/backtest_data.json` 获取历史数据
3. 返回回测结果和投资建议

### 示例 3: 投资建议

**用户**: "有什么投资建议？"

**操作**:
1. 读取 `references/optimization_report.md`
2. 返回行业配置建议和个股推荐

---

## ⚠️ 风险提示

1. 历史业绩不代表未来
2. 存储芯片集中度高，建议分散配置
3. 市场系统性风险无法避免
4. 流动性风险：小盘股可能无法及时买卖

---

## 📞 数据位置

```
数据库：
/root/data/astock_history.db    # K 线数据 (154MB)
/root/data/astock_indicators.db # 指标数据 (283MB)

回测数据：
/root/.openclaw/workspace/memory/stock-analysis/终极优化策略回测_20260312_1629.json
```

---

**最后更新**: 2026-03-12  
**状态**: ✅ 实盘就绪
