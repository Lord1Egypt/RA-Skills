---
name: investment-decision-system
description: >-
  个人投资决策辅助系统。基于 INVEST 六维决策框架（意图/数字/价值/优势/安全/时机），
  将分散的市场信息、持仓数据、投资目标和风控纪律串成一个完整的决策闭环。
  提供持仓管理、决策评分、仓位计算、风控检查和交互式 HTML 可视化报告。
  触发词：投资决策, 买卖决策, 持仓分析, 投资复盘, 仓位计算, 风控检查,
  INVEST, 投资仪表盘, 添加持仓, 记录交易, 买入分析, 卖出决策, 投资目标。
metadata:
  openclaw:
    requires:
      bins:
        - python
      env: {}
---

# 个人投资决策系统 (INVEST Decision System)

## Overview

市面上不缺行情、研报、社区观点和 AI 解读。缺的是一套**把信息、资产、目标和纪律连起来的决策系统**。
这个 Skill 提供 INVEST 六维决策框架，帮你从"我知道很多"走到"我做出更好的决策"。

核心能力：持仓管理 → 决策评分 → 仓位计算 → 风控检查 → 复盘分析，输出交互式 HTML 可视化报告。

## 快速开始

首次使用时，运行以下命令初始化数据库：

```bash
python {baseDir}/scripts/db.py
```

或通过 Python 直接导入（首次自动创建数据库）：

```python
import sys; sys.path.insert(0, '{baseDir}/scripts')
import db
db.init_db()
```

## Core Capabilities

### 1. 投资画像管理

设置投资目标、风险偏好、资金规模等基础参数。
后续所有决策都将基于这些参数进行个性化评估。

**操作：**
- 查看当前画像：读取 `get_profile()` 结果
- 更新画像：使用 `update_profile()` 设置 `risk_tolerance`（conservative/moderate/aggressive）、
  `investment_goal`（growth/income/preservation/speculation）、
  `time_horizon`（short/medium/long）、`total_capital` 等

脚本：`{baseDir}/scripts/db.py` 中的 `get_profile()` 和 `update_profile()` 函数。

### 2. 持仓管理

记录和管理投资组合中的各类资产。

**操作：**
- 添加持仓：`add_holding(symbol, name, asset_class, market, quantity, avg_cost, current_price, sector=...)`
- 更新持仓：`update_holding(holding_id, current_price=..., quantity=...)`
- 删除持仓：`delete_holding(holding_id)`
- 查看持仓：`get_all_holdings()`
- 组合概览：`get_portfolio_summary()` 返回总市值、盈亏、资产配置、行业配置

支持的 `asset_class`：stock / fund / bond / cash / crypto / other
支持的 `market`：A-share / HK / US / other

脚本：`{baseDir}/scripts/db.py` 中的持仓相关函数。

### 3. INVEST 六维决策框架

这是系统的核心。对每笔交易决策，从六个维度打分（0-10）：

| 维度 | 权重 | 核心问题 |
|------|------|----------|
| I - Intent 意图 | 15% | 你为什么做这笔交易？与投资目标一致吗？ |
| N - Numbers 数字 | 20% | 财务数据和技术指标支持你的判断吗？ |
| V - Value 价值 | 20% | 当前价格低于内在价值吗？安全边际够吗？ |
| E - Edge 优势 | 10% | 你凭什么比别人判断得更准？ |
| S - Safety 安全 | 20% | 如果错了，你会损失多少？风控到位吗？ |
| T - Timing 时机 | 15% | 为什么是现在？周期位置对吗？ |

**使用方法：**

```python
from scripts.decision import evaluate_decision

scores = {
    'intent_score': 7,
    'numbers_score': 6,
    'value_score': 8,
    'edge_score': 5,
    'safety_score': 7,
    'timing_score': 6,
}
result = evaluate_decision(scores)
# result['total_score'] -> 6.4
# result['recommendation'] -> 'CAUTIOUS'
```

**决策阈值：**
- ≥ 7.0 → STRONG_CONFIDENCE：强烈推荐
- 5.0-6.9 → CAUTIOUS：谨慎推荐
- 3.0-4.9 → WAIT：建议等待
- < 3.0 → AVOID：应回避

**保存决策到数据库：**
```python
from scripts import db
did = db.create_decision('600519', '贵州茅台', 'buy',
    intent_score=7, numbers_score=6, value_score=8,
    edge_score=5, safety_score=7, timing_score=6,
    thesis='白酒龙头估值回调后具备配置价值',
    risks='消费降级、政策风险',
    position_size_pct=15, stop_loss_pct=8, take_profit_pct=20)
```

脚本：`{baseDir}/scripts/decision.py` 中的 `evaluate_decision()` 函数。
数据库操作：`{baseDir}/scripts/db.py` 中的 `create_decision()`, `update_decision()`, `get_decision()` 等。

### 4. 仓位计算器

基于固定比例法（Fixed Fractional）计算最优仓位：

```python
from scripts.decision import calculate_position_size

sizing = calculate_position_size(
    capital=100000,          # 可用资金
    risk_per_trade_pct=2,    # 单笔最大风险 2%
    entry_price=50,          # 计划入场价
    stop_loss_price=46,      # 止损价
    max_position_pct=20      # 单票最大仓位 20%
)
# Returns: shares, position_value, position_pct, risk_amount, suggested_take_profit
```

公式：可买股数 = (总资产 × 单笔风险%) ÷ |入场价 - 止损价|

脚本：`{baseDir}/scripts/decision.py` 中的 `calculate_position_size()` 函数。

### 5. 风控合规检查

检查当前持仓是否违反预设的风控规则：

```python
from scripts import db
violations = db.check_risk_compliance()
```

默认风控规则：
- 单票最大仓位 ≤ 20%
- 单行业最大仓位 ≤ 40%
- 单笔硬止损 8%
- 最低现金 10%
- 单月交易 ≤ 10 次
- 最少持有 5 个交易日

可自定义：通过 `risk_rules` 表管理。

脚本：`{baseDir}/scripts/db.py` 中的 `check_risk_compliance()` 和 `get_risk_rules()` 函数。

### 6. 交易记录

记录买卖交易，自动更新持仓：

```python
from scripts import db
db.record_trade('600519', 'buy', quantity=100, price=1650, fee=5)
db.record_trade('600519', 'sell', quantity=50, price=1700, fee=5, decision_id=1)
```

脚本：`{baseDir}/scripts/db.py` 中的 `record_trade()` 函数。

### 7. 决策复盘

对已执行的决策进行复盘：

```python
from scripts import db
db.update_decision(decision_id, outcome='win', outcome_pnl=5000,
                   outcome_notes='按计划执行，盈利符合预期')
```

查看决策统计：
```python
stats = db.get_decision_stats()
# win_rate, profit_factor, avg_score_win, avg_score_loss, total_pnl
```

### 8. 关注列表

维护潜在投资标的的观察列表：

```python
from scripts import db
db.add_to_watchlist('300750', '宁德时代', reason='新能源龙头，关注回调机会', target_price=180)
```

### 9. 可视化报告

生成交互式 HTML 报告：

```python
from scripts.report import generate_dashboard_html, generate_decision_html, generate_review_html, save_report

# 投资仪表盘（综合概览）
html = generate_dashboard_html()
path = save_report(html, 'dashboard.html')

# 单笔决策报告
html = generate_decision_html(decision_id)
path = save_report(html, 'decision_report.html')

# 决策复盘报告
html = generate_review_html()
path = save_report(html, 'review_report.html')
```

报告保存到 `outputs/` 目录。报告包含：
- 投资仪表盘：资产配置饼图、盈亏统计、风控合规、持仓列表、近期决策
- 决策报告：INVEST 六维雷达图、详细评分、投资论点和风险分析、仓位参数
- 复盘报告：决策历史、胜率统计、评分-结果关联分析

脚本：`{baseDir}/scripts/report.py`

## 典型用户交互流程

### 场景 1：用户想评估是否买入某股票

1. 引导用户提供标的代码和基本信息
2. 逐维度（或一次性）询问 INVEST 六维度评分
3. 对于 Numbers 维度，主动联网搜索当前 PE/PB/ROE 等数据
4. 调用 `evaluate_decision()` 计算总分和建议
5. 调用 `calculate_position_size()` 计算仓位
6. 如果用户确认，调用 `create_decision()` 保存，并 `generate_decision_html()` 生成报告
7. 展示决策报告 HTML 文件给用户

**重要：** 当用户只需要快速评估而不保存时，直接使用 `{baseDir}/scripts/decision.py` 的纯计算方法，
无需初始化数据库。只有用户确认要保存决策、持仓或交易时才操作数据库。

### 场景 2：用户想查看投资仪表盘

1. 调用 `generate_dashboard_html()`
2. 使用 `save_report()` 保存到 outputs 目录
3. 展示给用户

### 场景 3：用户想复盘

1. 调用 `generate_review_html()` 生成复盘报告
2. 展示给用户，引导关注评分-结果的关联模式
3. 针对低分但盈利的决策，讨论运气 vs 能力
4. 针对高分但亏损的决策，分析出错原因

### 场景 4：用户想记录交易

1. 询问交易详情（标的、方向、数量、价格）
2. 调用 `record_trade()` 自动更新持仓
3. 检查风控合规 `check_risk_compliance()`
4. 如有违规，提醒用户

## 数据架构

数据库文件位置：`{baseDir}/data/investment.db`，包含以下表：

- `profile` — 投资者画像
- `holdings` — 持仓
- `trades` — 交易记录
- `decisions` — INVEST 决策记录
- `decision_log` — 决策变更日志
- `watchlist` — 关注列表
- `risk_rules` — 风控规则

详见 `scripts/db.py` 中的 `init_db()` 函数。

## 参考文档

- `references/framework.md` — INVEST 决策框架完整文档，包含每个维度的详细评分标准、常见陷阱、仓位管理规则
- `references/indicators.md` — 投资关键指标速查：A股估值参考、财务健康指标、技术分析速查、行业估值差异、行为金融学偏差

当需要深入了解某个维度的评分标准或投资指标参考时，读取对应的 `{baseDir}/references/` 文件。

## 重要原则

1. **本系统不提供投资建议**，只提供决策框架。所有投资决策由用户自行负责。
2. **不替代专业金融工具**。行情数据需要用户提供或通过联网搜索获取。
3. **评分是主观的**。INVEST 框架的价值在于强制结构化思考，而非绝对准确的评分。
4. **决策质量 ≠ 结果质量**。好决策可能亏损，坏决策可能盈利。复盘时区分两者。
5. **纪律 > 预测**。系统的核心价值是帮助用户建立和执行纪律，而非做出准确预测。
