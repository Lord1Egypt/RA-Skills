---
name: money-never-sleep
version: 0.5.10
description: |
  MNS (Money Never Sleep, Market Neutral Strategist) CLI skill for autonomous agents. Provides investment
  portfolio tracking, market sentiment analysis using CNN Fear & Greed Index, and strategy
  suggestion report generation. Use when managing a contrarian investment portfolio,
  generating buy/sell suggestions based on market sentiment thresholds, or producing
  daily strategy reports.

  NOTE: This tool provides strategy suggestions only - it does NOT connect to any broker APIs
  or execute actual trades. All trades must be manually executed by users on their brokerage platforms
  and then recorded via CLI commands.

  Triggers include: "管理投资组合", "生成策略建议", "获取市场报告", "查看持仓收益",
  "更新现金余额", "记录买入卖出", "查看恐贪指数", "投资组合再平衡", "MNS 报告", "回测策略"
license: MIT
compatibility: Requires Node.js 18+ or Bun.
metadata:
  {
    "openclaw":
      {
        "requires": { "anyBins": ["npx", "bunx", "npm", "bun"] },
        "source": "https://github.com/sopaco/money-never-sleep",
        "homepage": "https://github.com/sopaco/money-never-sleep",
        "author": "Sopaco",
        "os": ["darwin", "linux", "win32"]
      }
  }
  
---

# MNS CLI 投资管理 Skill

## 概述

本 skill 提供 MNS 逆向投资策略的 CLI 操作能力。MNS 是基于 CNN Fear & Greed Index 情绪指标的量化投资工具，通过 contrarian 策略在情绪极度恐慌时买入，极度贪婪时卖出，实现市场中性风格的长期投资。

### 安全声明

> - **源码公开**: 所有源码公开托管于 [GitHub](https://github.com/sopaco/money-never-sleep)
> - **无网络交易**: 不连接任何券商 API，所有数据存储在本地 SQLite 数据库
> - **无敏感权限**: 无需使用也不自动读取用户任何金融账户配置

## 核心能力

1. **投资组合管理**: 查看持仓、现金余额、资产配置、年化收益
2. **交易记录**: 记录买入/卖出操作，更新资产当前价格（手动输入或自动获取）
3. **策略建议**: 自动生成基于最新恐贪指数的买卖建议报告（仅建议，不执行交易）
4. **配置管理**: 查看和调整策略参数（阈值、买入/卖出比例、止盈线）
5. **历史查询**: 查看交易历史、价格更新记录
6. **策略回测**: 基于历史数据验证策略参数表现

> **重要说明**: 本工具仅提供策略建议和记录功能，不连接任何券商 API。
> 用户需自行在券商平台执行交易后，通过 CLI 记录交易结果。

## 快速开始

### 安装

```bash
# 通过 npm 安装（推荐）
npm install -g @never-sleeps/mns-cli

# 或通过 bun 安装
bun install -g @never-sleeps/mns-cli

# 或直接使用 npx（无需安装）
npx @never-sleeps/mns-cli --help
```

### 初始化

```bash
# 初始化配置文件和数据库
# 如果已有数据，会提示确认后再覆盖
mns init

# 使用 --force 跳过确认直接覆盖
mns init --force

# 设置初始现金
mns cash set 100000
```

### 添加资产到持仓池

```bash
mns add QQQ "纳指100" us_stocks
mns add SH600000 "浦发银行" cn_stocks
mns add GLD "黄金ETF" counter_cyclical
```

### 记录买入交易

```bash
mns buy QQQ 100 450.50
mns buy SH600000 500 12.30
```

### 查看持仓和策略建议

```bash
# 查看当前持仓（含年化收益）
mns portfolio

# 获取今日策略报告（基于最新恐贪指数）
mns report

# 查看当前恐贪指数
mns sentiment
```

### 更新价格和查看历史

```bash
# 手动更新单个资产价格
mns price QQQ 460.00

# 自动更新所有资产价格（需要网络）
mns update-prices

# 查看最近交易历史
mns history --limit 50

# 查看现金余额
mns cash
```

### 配置管理

```bash
# 查看所有配置
mns config

# 查看特定配置项（支持 dot-path 语法）
mns config thresholds.fear
mns config buy_ratio.extreme_fear

# 修改配置项（策略参数）
mns config thresholds.greed 75
mns config buy_ratio.fear 30.0
mns config sell_ratio.extreme_greed_target_high 60.0
```

### 策略回测

```bash
# 查看可调参数列表
mns backtest params

# 运行默认配置回测
mns backtest run

# 使用自定义配置回测
mns backtest run --config path/to/config.toml

# 对比多个配置
mns backtest run --compare config1.toml,config2.toml
```

## 数据存储

- **配置文件**: `~/.mns/config.toml`
- **数据库**: `~/.mns/mns.db`
- **报告输出**: `./reports/`（可通过 `settings.report_output_dir` 配置）

## 策略逻辑详解

### 情绪驱动的买入决策

买入比例基于恐贪指数区间：

| 恐贪区间 | 指数范围 | 买入比例 | 逻辑 |
|---------|---------|---------|------|
| 极度恐慌 | FGI < 30 | 60% (默认) | 极度恐慌，适度买入 |
| 恐慌 | 30 ≤ FGI < 45 | 35% (默认) | 恐慌，保守买入 |
| 中性 | 45 ≤ FGI < 55 | 0% (默认) | 中性，暂停买入 |
| 贪婪 | 55 ≤ FGI < 70 | 0% (默认) | 贪婪，不买入 |
| 极度贪婪 | FGI ≥ 70 | 0% (默认) | 极度贪婪，不买入 |

### 卖出决策（双准则）

卖出建议综合考虑：
1. **年化收益止盈**: 基于持有天数计算年化收益率，对照卖出矩阵
2. **绝对收益线**: 绝对收益 ≥ 30% 且持仓 ≥ 90 天时也可考虑卖出

卖出矩阵（按情绪区间和收益档位）：

| 情绪区间 | target_high | target_low | below_target |
|---------|-------------|------------|--------------|
| 极度贪婪 | 50% | 30% | 20% |
| 贪婪 | 40% | 25% | 0% |
| 中性 | 15% | 0% | 0% |
| 恐慌/极度恐慌 | 0% | 0% | 0% |

> 注：target_high = 年化收益 ≥ annualized_target_high（默认15%），target_low = 年化收益 ≥ annualized_target_low（默认10%）

### 买入资金分配：Contrarian 权重

可用现金按 contrarian 权重分配到各资产：

- **权重公式**: `weight = min(max_weight, max(1.0, cost_price / current_price))`
- **解释**: 浮亏资产（当前价格 < 成本价）获得更高权重，符合逆向抄底逻辑
- **上限控制**: `max_contrarian_weight`（默认 2.0）防止过度集中单一标的
- **浮盈资产**: 权重为 1.0（基线）

### 风险警告机制

当持仓浮亏 ≥ 20% 时触发风险警告，建议根据市场情绪差异化处理：

| 情绪环境 | 建议操作 |
|---------|---------|
| Extreme Fear/Fear | 可能是加仓机会 |
| Neutral | 审视基本面 |
| Greed/Extreme Greed | 紧急审视（别人赚钱你还在亏） |

## 常见工作流

### 日常报告（Agent 每日执行）

```bash
# 1. 自动更新所有资产价格
mns update-prices

# 2. 查看策略报告
mns report

# 3. 根据建议执行买入（如有）
mns buy QQQ 50 445.00

# 4. 记录卖出（如有）
mns sell QQQ 100 455.00

# 5. 查看最新持仓
mns portfolio
```

### 策略参数调优

```bash
# 查看当前买入比例
mns config buy_ratio

# 调整极端恐慌买入比例到 60%
mns config buy_ratio.extreme_fear 60.0

# 降低中性区间买入到 10%
mns config buy_ratio.neutral 10.0

# 调整卖出矩阵
mns config sell_ratio.extreme_greed_target_high 70.0

# 调整止盈线
mns config settings.annualized_target_low 12.0
mns config settings.annualized_target_high 18.0

# 调整逆向权重上限（防止单标的过度集中）
mns config settings.max_contrarian_weight 1.5
```

### 新资产添加流程

```bash
# 1. 添加资产到池子
mns add TSLA "特斯拉" us_stocks

# 2. 初始建仓买入
mns buy TSLA 50 250.00

# 3. 更新当前价格
mns price TSLA 255.00
```

## 高级分析指南

以下分析功能由 Agent 组合使用基础命令完成，非单一 CLI 命令。

### 行业分析 (Agent 执行)

组合使用基础命令分析行业表现：

```bash
# 1. 查询行业 ETF 表现
mns analyze XLK    # 科技
mns analyze XLF    # 金融
mns analyze XLE    # 能源
mns analyze XLV    # 医疗
mns analyze XLY    # 消费
mns analyze XLP    # 消费必需品
mns analyze XLB    # 材料
mns analyze XLU    # 公用事业
mns analyze XLI    # 工业
mns analyze XLRE   # 房地产

# 2. 分析各行业龙头股
mns analyze AAPL   # 科技龙头
mns analyze JPM    # 金融龙头
mns analyze XOM    # 能源龙头

# 3. 对比行业表现与大盘指数
mns market-indices  # 获取大盘指数参考
mns portfolio       # 查看当前持仓行业分布
```

Agent 分析要点：
- 比较各行业 ETF 涨跌幅，识别强势/弱势行业
- 对比行业与大盘（S&P 500）的相对表现
- 结合恐贪指数判断行业轮动机会

### 组合深度分析 (Agent 执行)

基于已有数据进行组合分析：

```bash
# 1. 查看当前持仓
mns portfolio

# 2. 获取市场情绪
mns sentiment

# 3. 获取策略报告
mns report

# 4. 查看历史表现
mns history --limit 100
```

Agent 分析要点：
- **配置合理性**: 持仓集中度是否过高（单一标的 > 30% 需警惕）
- **收益分布**: 各持仓年化收益率分布，识别拖累/贡献主力
- **情绪偏离**: 当前恐贪指数与持仓策略是否匹配（恐慌时应持有更多权益）
- **现金比例**: 现金占比是否符合理想配置（参考买入比例建议）

### 风险评估 (Agent 执行)

组合计算风险指标：

```bash
# 1. 获取持仓成本与当前价格
mns portfolio

# 2. 获取历史价格记录
mns history --limit 365

# 3. 结合市场波动率
mns market  # 包含 VIX 指数
```

Agent 风险指标计算：
- **最大回撤**: 基于历史快照计算峰值到谷值的最大跌幅
- **Sharpe 比率**: `(年化收益 - 无风险利率) / 波动率`（需历史数据支持）
- **持仓集中度**: 前三大持仓占比总和
- **浮亏暴露**: 当前浮亏 > 20% 的持仓数量及金额

风险等级判定：
| 风险等级 | 条件 |
|---------|------|
| 低风险 | 单一持仓 < 20%，无浮亏 > 20% 标的，现金 > 20% |
| 中风险 | 单一持仓 20-30%，或 1-2 个标的浮亏 10-20% |
| 高风险 | 单一持仓 > 30%，或 3+ 标的浮亏 > 20%，或 VIX > 30 |

## 配置参数

完整的配置参数说明请参考 `references/strategy.md`，其中包含：
- 所有配置项的默认值速查表
- 策略参数的详细解释
- 买入/卖出比例矩阵说明

命令使用方法请参考 `references/commands.md`。

## 注意事项

- **价格更新**: 买入/卖出后建议调用 `price` 或 `update-prices` 命令更新价格，确保持仓收益数据准确
- **时间敏感性**: `report` 和 `sentiment` 命令通过 HTTP 获取实时 CNN Fear & Greed Index，需要网络访问
- **异步要求**: 这两个命令是异步的，agent 调用时需确保环境支持 async execution
- **Windows 编码**: PowerShell 默认 GBK 编码可能导致中文乱码，建议使用 UTF-8 终端或重定向输出到文件
- **年化收益计算**: 使用 `annualized = (current / cost) ^ (365 / holding_days) - 1`，持仓天数 < min_holding_days 时不显示
- **绝对收益止盈**: 持仓绝对收益 ≥ 30% 且天数 ≥ min_absolute_profit_days 时，即使年化收益率未达阈值也可能触发卖出

## 错误处理

- **网络错误**: `sentiment` 和 `report` 可能因 API 不可用失败，建议重试或使用缓存数据
- **数据库锁定**: 多进程并发操作 SQLite 会导致锁定，agent 应确保串行访问

## 相关文件

- `references/commands.md` - 完整命令参考
- `references/strategy.md` - 策略参数详解
