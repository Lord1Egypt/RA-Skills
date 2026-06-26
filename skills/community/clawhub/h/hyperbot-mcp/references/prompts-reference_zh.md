[中文](prompts-reference_zh.md) | [English](prompts-reference.md)

# Hyperbot MCP 提示词参考

Hyperbot MCP 服务器提供用于加密货币交易分析、聪明钱追踪、鲸鱼行为监控和市场情绪分析的 **prompts** 和 **tools**。在调用 MCP 功能时（例如从 Cursor 或 Claude）使用这些提示词。

## 📊 分析提示词

| 提示词名称 | 使用场景 | 所需输入 |
|-------------|-------------|----------------|
| **smart-money-analysis** | 用户想要分析聪明钱地址的交易行为和特征，生成跟单策略建议 | 聪明钱地址数据（来自 `fetch_leader_board` 或 `find_smart_money`） |
| **whale-tracking** | 用户需要分析鲸鱼行为及其对市场的影响，预测短期趋势 | 鲸鱼持仓和动向数据（来自 `get_whale_positions`、`get_whale_events`） |
| **market-sentiment** | 用户想要基于订单簿、鲸鱼多空比和市场数据分析当前市场情绪和趋势 | 市场数据，包括订单簿、挂单统计、鲸鱼多空比（来自 `get_l2_order_book`、`get_market_stats`、`get_whale_history_ratio`） |
| **trader-evaluation** | 用户想要全面评估交易者的能力和表现，并进行评分 | 交易者统计、历史表现、币种偏好（来自 `get_trader_stats`、`get_performance_by_coin`、`get_best_trades`） |

## 🛠️ 核心工具

### 聪明钱分析工具

| 工具名称 | 描述 | 参数 |
|-----------|-------------|------------|
| **fetch_leader_board** | 获取 Hyperbot 聪明钱排行榜。可用周期：24h、7d、30d；排序选项：pnl、winRate | `period`: 时间周期（24h/7d/30d），`sort`: 排序字段（pnl/winRate） |
| **find_smart_money** | 发现聪明钱地址，支持多种过滤和排序选项 | `period`: 天数（例如 7 表示最近 7 天），`sort`: 排序方式（win-rate/account-balance/ROI/pnl/position-count/profit-count/last-operation/avg-holding-period/current-position），`pnlList`: 是否包含 PnL 曲线数据 |
| **fetch_trade_history** | 查询指定钱包地址的历史交易详情 | `address`: 以 0x 开头的钱包地址 |
| **get_trader_stats** | 获取指定地址的交易者统计 | `address`: 用户钱包地址，`period`: 天数 |
| **get_max_drawdown** | 获取交易者的最大回撤 | `address`: 用户钱包地址，`days`: 统计天数（1/7/30/60/90），`scope`: 范围（默认：perp） |
| **get_best_trades** | 获取地址收益最高的交易 | `address`: 用户钱包地址，`period`: 天数，`limit`: 返回记录数量 |
| **get_performance_by_coin** | 按币种拆解地址的胜率和 PnL 表现 | `address`: 用户钱包地址，`period`: 天数，`limit`: 返回记录数量 |

### 鲸鱼监控工具

| 工具名称 | 描述 | 参数 |
|-----------|-------------|------------|
| **get_whale_positions** | 获取鲸鱼持仓信息，支持高级过滤 | `coin`: 币种代码（ETH、BTC），`dir`: 方向（long/short），`pnlSide`: PnL 过滤（profit/loss），`frSide`: 资金费 PnL 过滤（profit/loss），`topBy`: 排序方式（position-value/margin-balance/create-time/profit/loss），`take`: 限制数量 |
| **get_whale_events** | 实时监控鲸鱼最新的开仓/平仓动态 | `limit`: 返回记录数量 |
| **get_whale_directions** | 获取鲸鱼仓位多空数量统计。可按币种过滤 | `coin`: 币种代码（可选） |
| **get_whale_history_ratio** | 获取历史鲸鱼仓位多空比 | `interval`: 时间间隔（1h/1d 或 hour/day），`limit`: 返回记录数量 |

### 市场数据工具

| 工具名称 | 描述 | 参数 |
|-----------|-------------|------------|
| **get_tickers** | 获取全市场最新交易价格 | 无 |
| **get_ticker** | 获取指定币种的最新交易价格 | `coin`: 币种代码（BTC、ETH、SOL 等） |
| **get_klines** | 获取 K 线数据，包含交易量。支持多种时间周期 | `coin`: 币种代码（BTC、ETH），`interval`: 时间周期（1m/3m/5m/15m/30m/1h/4h/8h/1d），`limit`: 记录数量 |
| **get_market_stats** | 获取挂单统计（多空数量、价值、鲸鱼挂单占比）及全网中间价 | `coin`: 币种代码（BTC、ETH），`whaleThreshold`: 鲸鱼阈值（单位：USDT） |
| **get_l2_order_book** | 获取市场信息（L2 订单簿等） | `coin`: 币种代码（BTC、ETH） |

### 仓位分析工具

| 工具名称 | 描述 | 参数 |
|-----------|-------------|------------|
| **get_completed_position_history** | 获取已完成仓位历史。深度分析某个币种的完整历史仓位数据 | `address`: 用户钱包地址，`coin`: 币种名称（BTC、ETH） |
| **get_current_position_history** | 获取当前仓位历史。如果没有当前仓位则返回 400 错误 | `address`: 用户钱包地址，`coin`: 币种名称（BTC、ETH） |
| **get_completed_position_executions** | 获取已完成仓位操盘轨迹 | `address`: 用户钱包地址，`coin`: 币种名称（BTC、ETH），`interval`: 时间周期（4h/1d），`startTime`: 开始时间戳（毫秒），`endTime`: 结束时间戳（毫秒），`limit`: 返回记录数量 |
| **get_current_position_pnl** | 获取当前仓位 PnL | `address`: 用户钱包地址，`coin`: 币种名称（BTC、ETH），`interval`: 时间周期（4h/1d），`limit`: 返回记录数量 |

### 批量查询工具

| 工具名称 | 描述 | 参数 |
|-----------|-------------|------------|
| **get_traders_accounts** | 批量查询账户信息。最多支持 50 个地址 | `addresses`: 地址列表（最多 50 个） |
| **get_traders_statistics** | 批量查询交易者统计。最多支持 50 个地址 | `period`: 天数（例如 7 表示最近 7 天），`pnlList`: 是否包含 PnL 曲线数据，`addresses`: 地址列表（最多 50 个） |

## 📦 资源

| 资源名称 | 描述 | URI |
|---------------|-------------|-----|
| **smart_money_addresses** | 聪明钱地址列表，包含胜率、PnL 等关键指标的性能数据 | https://hyperbot.network/api/leaderboard/smart/hot |
| **whale_positions** | 鲸鱼持仓信息，包括币种、方向、仓位价值 | https://open.aicoin.com/api/upgrade/v2/hl/whales/open-positions |
| **market_data** | 实时市场数据，包括价格、订单簿深度 | https://open.aicoin.com/api/upgrade/v2/hl/tickers |
| **trader_statistics** | 交易者统计，包括交易次数、胜率、最大回撤 | https://open.aicoin.com/api/upgrade/v2/hl/traders/statistics |
| **whale_events** | 最新的鲸鱼开仓/平仓事件 | https://open.aicoin.com/api/upgrade/v2/hl/whales/latest-events |
| **whale_directions** | 鲸鱼仓位多空数量统计 | https://open.aicoin.com/api/upgrade/v2/hl/whales/directions |
| **all_mids** | 所有币种的市场中间价 | https://open.aicoin.com/api/upgrade/v2/hl/info |

## 💡 使用示例

### 示例 1：分析聪明钱策略
```
1. 使用 `fetch_leader_board`，参数 period="7d", sort="winRate" 获取顶级聪明钱地址
2. 使用 `smart-money-analysis` 提示词，传入地址数据获取策略建议
```

### 示例 2：追踪鲸鱼动向
```
1. 使用 `get_whale_events`，参数 limit=20 获取最新鲸鱼活动
2. 使用 `get_whale_positions` 查看当前大额持仓
3. 使用 `whale-tracking` 提示词分析鲸鱼行为并预测市场走势
```

### 示例 3：市场情绪分析
```
1. 使用 `get_l2_order_book` 获取订单簿深度
2. 使用 `get_market_stats` 获取挂单统计
3. 使用 `get_whale_history_ratio` 查看鲸鱼持仓趋势
4. 使用 `market-sentiment` 提示词获取综合市场分析
```

### 示例 4：评估交易者
```
1. 使用 `get_trader_stats` 获取基础统计
2. 使用 `get_performance_by_coin` 查看不同币种的表现
3. 使用 `get_best_trades` 查看其最佳交易
4. 使用 `trader-evaluation` 提示词获取带评分的详细评估
```

## 🎯 最佳实践

- **聪明钱分析**：始终使用近期数据（7d 或 30d 周期），并关注胜率而非单纯的 PnL
- **鲸鱼追踪**：结合持仓数据和事件数据以了解完整情况
- **市场分析**：使用多个数据源（订单簿 + 鲸鱼多空比 + 挂单统计）以提高准确性
- **交易者评估**：考虑多个维度，包括最大回撤、胜率以及在不同币种间的一致性

提示词通常接受来自工具响应的 JSON 格式输入数据。当用户要求"分析"、"策略"、"评估"或"建议"时，优先使用这些引导式提示词，而不是原始工具调用，以获得更复杂的分析结果。
