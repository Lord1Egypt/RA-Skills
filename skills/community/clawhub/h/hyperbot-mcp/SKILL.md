[中文](SKILL_zh.md) | [English](SKILL.md)

# MCP Server Skill Documentation

## 1. Overview
**Skill Name:** Hyperbot Trading Analytics  
**Description:** Provides trading data analytics capabilities for the Hyperbot platform, including smart money tracking, whale monitoring, market data queries, and trader statistics. Suitable for cryptocurrency traders conducting market analysis and decision-making.  
**Version:** 1.0.0  
**MCP Server URL / Endpoint:** https://mcp.hyperbot.network/mcp

**sessionId:** sessionId obtained via SSE at https://mcp.hyperbot.network/mcp/sse

---

## 2. Resources

### 2.1 Defined Resources
None

**Usage Notes:**
- Read-only resources that do not change system state
- Can be used as prompt input or for Agent decision-making reference
- Data sourced from Hyperbot platform and on-chain data
- Supports on-demand retrieval (pagination/filtering conditions)

---

## 3. Tools

### 3.1 Leaderboard & Smart Money Discovery

#### fetch_leader_board
**Function:** Get Hyperbot smart money leaderboard  
**Parameters:**
- `period`: Time period, options: 24h, 7d, 30d
- `sort`: Sort field, options: pnl (profit/loss), winRate (win rate)

**MCP Tool Call Example:**
```bash
curl 'https://mcp.hyperbot.network/mcp/message?sessionId=sessionId obtained via sse' \
  -H 'content-type: application/json' \
  --data-raw '{"method":"tools/call","params":{"name":"fetch_leader_board","arguments":{"period":"7d","sort":"pnl"}},"jsonrpc":"2.0","id":1}'
```

#### find_smart_money
**Function:** Discover smart money addresses with multiple sorting and filtering options  
**Parameters:**
- `period`: Period in days, e.g., 7 means last 7 days
- `sort`: Sorting method, options: win-rate, account-balance, ROI, pnl, position-count, profit-count, last-operation, avg-holding-period, current-position
- `pnlList`: Whether to include PnL curve data (true/false)

**MCP Tool Call Example:**
```bash
curl 'https://mcp.hyperbot.network/mcp/message?sessionId=sessionId obtained via sse' \
  -H 'content-type: application/json' \
  --data-raw '{"method":"tools/call","params":{"name":"find_smart_money","arguments":{"period":7,"sort":"win-rate","pnlList":true}},"jsonrpc":"2.0","id":2}'
```

---

### 3.2 Market Data

#### get_tickers
**Function:** Get latest trading prices for all markets  
**Parameters:** None

**MCP Tool Call Example:**
```bash
curl 'https://mcp.hyperbot.network/mcp/message?sessionId=sessionId obtained via sse' \
  -H 'content-type: application/json' \
  --data-raw '{"method":"tools/call","params":{"name":"get_tickers","arguments":{}},"jsonrpc":"2.0","id":3}'
```

#### get_ticker
**Function:** Get latest trading price for a specific coin  
**Parameters:**
- `address`: Coin code, e.g., btc, eth, sol

**MCP Tool Call Example:**
```bash
curl 'https://mcp.hyperbot.network/mcp/message?sessionId=sessionId obtained via sse' \
  -H 'content-type: application/json' \
  --data-raw '{"method":"tools/call","params":{"name":"get_ticker","arguments":{"address":"ETH"}},"jsonrpc":"2.0","id":4}'
```

#### get_klines
**Function:** Get K-line data (with trading volume), supports BTC, ETH, and other coins  
**Parameters:**
- `coin`: Coin code, e.g., btc, eth
- `interval`: K-line interval, options: 1m, 3m, 5m, 15m, 30m, 1h, 4h, 8h, 1d
- `limit`: Maximum number of records to return

**MCP Tool Call Example:**
```bash
curl 'https://mcp.hyperbot.network/mcp/message?sessionId=sessionId obtained via sse' \
  -H 'content-type: application/json' \
  --data-raw '{"method":"tools/call","params":{"name":"get_klines","arguments":{"coin":"BTC","interval":"15m","limit":100}},"jsonrpc":"2.0","id":5}'
```

#### get_market_stats
**Function:** Get active order statistics (long/short count, value, whale order ratio) and market mid price  
**Parameters:**
- `coin`: Coin code, e.g., btc, eth
- `whaleThreshold`: Whale threshold (in USDT)

**MCP Tool Call Example:**
```bash
curl 'https://mcp.hyperbot.network/mcp/message?sessionId=sessionId obtained via sse' \
  -H 'content-type: application/json' \
  --data-raw '{"method":"tools/call","params":{"name":"get_market_stats","arguments":{"coin":"BTC","whaleThreshold":100000}},"jsonrpc":"2.0","id":6}'
```

#### get_l2_order_book
**Function:** Get market information (L2 order book, etc.)  
**Parameters:**
- `coin`: Coin code, e.g., btc, eth

**MCP Tool Call Example:**
```bash
curl 'https://mcp.hyperbot.network/mcp/message?sessionId=sessionId obtained via sse' \
  -H 'content-type: application/json' \
  --data-raw '{"method":"tools/call","params":{"name":"get_l2_order_book","arguments":{"coin":"BTC"}},"jsonrpc":"2.0","id":7}'
```

---

### 3.3 Whale Monitoring

#### get_whale_positions
**Function:** Get whale position information  
**Parameters:**
- `coin`: Coin code, e.g., eth, btc
- `dir`: Direction, options: long, short
- `pnlSide`: PnL filter, options: profit, loss
- `frSide`: Funding fee PnL filter, options: profit, loss
- `topBy`: Sorting method, options: position-value, margin-balance, create-time, profit, loss
- `take`: Maximum number of records to return

**MCP Tool Call Example:**
```bash
curl 'https://mcp.hyperbot.network/mcp/message?sessionId=sessionId obtained via sse' \
  -H 'content-type: application/json' \
  --data-raw '{"method":"tools/call","params":{"name":"get_whale_positions","arguments":{"coin":"BTC","dir":"long","pnlSide":"profit","frSide":"profit","topBy":"position-value","take":10}},"jsonrpc":"2.0","id":8}'
```

#### get_whale_events
**Function:** Real-time monitoring of latest whale open/close positions  
**Parameters:**
- `limit`: Maximum number of records to return

**MCP Tool Call Example:**
```bash
curl 'https://mcp.hyperbot.network/mcp/message?sessionId=sessionId obtained via sse' \
  -H 'content-type: application/json' \
  --data-raw '{"method":"tools/call","params":{"name":"get_whale_events","arguments":{"limit":20}},"jsonrpc":"2.0","id":9}'
```

#### get_whale_directions
**Function:** Get whale position long/short count. Can filter by specific coin  
**Parameters:**
- `coin`: Coin code, e.g., eth, btc (optional)

**MCP Tool Call Example:**
```bash
curl 'https://mcp.hyperbot.network/mcp/message?sessionId=sessionId obtained via sse' \
  -H 'content-type: application/json' \
  --data-raw '{"method":"tools/call","params":{"name":"get_whale_directions","arguments":{"coin":"BTC"}},"jsonrpc":"2.0","id":10}'
```

#### get_whale_history_ratio
**Function:** Get historical whale position long/short ratio  
**Parameters:**
- `interval`: Time interval, options: 1h, 1d or hour, day
- `limit`: Maximum number of records to return

**MCP Tool Call Example:**
```bash
curl 'https://mcp.hyperbot.network/mcp/message?sessionId=sessionId obtained via sse' \
  -H 'content-type: application/json' \
  --data-raw '{"method":"tools/call","params":{"name":"get_whale_history_ratio","arguments":{"interval":"1d","limit":30}},"jsonrpc":"2.0","id":11}'
```

---

### 3.4 Trader Analysis

#### fetch_trade_history
**Function:** Query historical trade details for a specific wallet address  
**Parameters:**
- `address`: Wallet address starting with 0x

**MCP Tool Call Example:**
```bash
curl 'https://mcp.hyperbot.network/mcp/message?sessionId=sessionId obtained via sse' \
  -H 'content-type: application/json' \
  --data-raw '{"method":"tools/call","params":{"name":"fetch_trade_history","arguments":{"address":"0x1234567890abcdef1234567890abcdef12345678"}},"jsonrpc":"2.0","id":12}'
```

#### get_trader_stats
**Function:** Get trader statistics  
**Parameters:**
- `address`: User wallet address
- `period`: Period in days

**MCP Tool Call Example:**
```bash
curl 'https://mcp.hyperbot.network/mcp/message?sessionId=sessionId obtained via sse' \
  -H 'content-type: application/json' \
  --data-raw '{"method":"tools/call","params":{"name":"get_trader_stats","arguments":{"address":"0x1234567890abcdef1234567890abcdef12345678","period":7}},"jsonrpc":"2.0","id":13}'
```

#### get_max_drawdown
**Function:** Get maximum drawdown  
**Parameters:**
- `address`: User wallet address
- `days`: Statistics days, options: 1, 7, 30, 60, 90
- `scope`: Statistics scope, default: perp

**MCP Tool Call Example:**
```bash
curl 'https://mcp.hyperbot.network/mcp/message?sessionId=sessionId obtained via sse' \
  -H 'content-type: application/json' \
  --data-raw '{"method":"tools/call","params":{"name":"get_max_drawdown","arguments":{"address":"0x1234567890abcdef1234567890abcdef12345678","days":30,"scope":"perp"}},"jsonrpc":"2.0","id":14}'
```

#### get_best_trades
**Function:** Get the most profitable trades  
**Parameters:**
- `address`: User wallet address
- `period`: Days
- `limit`: Maximum number of records to return

**MCP Tool Call Example:**
```bash
curl 'https://mcp.hyperbot.network/mcp/message?sessionId=sessionId obtained via sse' \
  -H 'content-type: application/json' \
  --data-raw '{"method":"tools/call","params":{"name":"get_best_trades","arguments":{"address":"0x1234567890abcdef1234567890abcdef12345678","period":7,"limit":10}},"jsonrpc":"2.0","id":15}'
```

#### get_performance_by_coin
**Function:** Break down win rate and PnL performance by coin for an address  
**Parameters:**
- `address`: User wallet address
- `period`: Days
- `limit`: Maximum number of records to return

**MCP Tool Call Example:**
```bash
curl 'https://mcp.hyperbot.network/mcp/message?sessionId=sessionId obtained via sse' \
  -H 'content-type: application/json' \
  --data-raw '{"method":"tools/call","params":{"name":"get_performance_by_coin","arguments":{"address":"0x1234567890abcdef1234567890abcdef12345678","period":30,"limit":20}},"jsonrpc":"2.0","id":16}'
```

---

### 3.5 Position History

#### get_completed_position_history
**Function:** Get completed position history. Deep analysis of complete historical position data for a coin  
**Parameters:**
- `address`: User wallet address
- `coin`: Coin name, e.g., BTC, ETH

**MCP Tool Call Example:**
```bash
curl 'https://mcp.hyperbot.network/mcp/message?sessionId=sessionId obtained via sse' \
  -H 'content-type: application/json' \
  --data-raw '{"method":"tools/call","params":{"name":"get_completed_position_history","arguments":{"address":"0x1234567890abcdef1234567890abcdef12345678","coin":"BTC"}},"jsonrpc":"2.0","id":17}'
```

#### get_current_position_history
**Function:** Get current position history. Returns historical data for a specific coin's current position  
**Parameters:**
- `address`: User wallet address
- `coin`: Coin name, e.g., BTC, ETH

**MCP Tool Call Example:**
```bash
curl 'https://mcp.hyperbot.network/mcp/message?sessionId=sessionId obtained via sse' \
  -H 'content-type: application/json' \
  --data-raw '{"method":"tools/call","params":{"name":"get_current_position_history","arguments":{"address":"0x1234567890abcdef1234567890abcdef12345678","coin":"BTC"}},"jsonrpc":"2.0","id":18}'
```

#### get_completed_position_executions
**Function:** Get completed position execution trajectory  
**Parameters:**
- `address`: User wallet address
- `coin`: Coin name, e.g., BTC, ETH
- `interval`: Time interval, e.g., 4h, 1d
- `startTime`: Start timestamp (milliseconds)
- `endTime`: End timestamp (milliseconds)
- `limit`: Maximum number of records to return

**MCP Tool Call Example:**
```bash
curl 'https://mcp.hyperbot.network/mcp/message?sessionId=sessionId obtained via sse' \
  -H 'content-type: application/json' \
  --data-raw '{"method":"tools/call","params":{"name":"get_completed_position_executions","arguments":{"address":"0x1234567890abcdef1234567890abcdef12345678","coin":"BTC","interval":"4h","limit":50}},"jsonrpc":"2.0","id":19}'
```

#### get_current_position_pnl
**Function:** Get current position PnL  
**Parameters:**
- `address`: User wallet address
- `coin`: Coin name, e.g., BTC, ETH
- `interval`: Time interval, e.g., 4h, 1d
- `limit`: Maximum number of records to return

**MCP Tool Call Example:**
```bash
curl 'https://mcp.hyperbot.network/mcp/message?sessionId=sessionId obtained via sse' \
  -H 'content-type: application/json' \
  --data-raw '{"method":"tools/call","params":{"name":"get_current_position_pnl","arguments":{"address":"0x1234567890abcdef1234567890abcdef12345678","coin":"BTC","interval":"4h","limit":20}},"jsonrpc":"2.0","id":20}'
```

---

### 3.6 Batch Queries

#### get_traders_accounts
**Function:** Batch query account information, supports up to 50 addresses  
**Parameters:**
- `addresses`: List of addresses, max 50 addresses

**MCP Tool Call Example:**
```bash
curl 'https://mcp.hyperbot.network/mcp/message?sessionId=sessionId obtained via sse' \
  -H 'content-type: application/json' \
  --data-raw '{"method":"tools/call","params":{"name":"get_traders_accounts","arguments":{"addresses":["0x1234567890abcdef1234567890abcdef12345678","0xabcdef1234567890abcdef1234567890abcdef12"]}},"jsonrpc":"2.0","id":21}'
```

#### get_traders_statistics
**Function:** Batch query trader statistics, supports up to 50 addresses  
**Parameters:**
- `period`: Period in days, e.g., 7 means last 7 days
- `pnlList`: Whether to include PnL curve data
- `addresses`: List of addresses, max 50 addresses

**MCP Tool Call Example:**
```bash
curl 'https://mcp.hyperbot.network/mcp/message?sessionId=sessionId obtained via sse' \
  -H 'content-type: application/json' \
  --data-raw '{"method":"tools/call","params":{"name":"get_traders_statistics","arguments":{"period":7,"pnlList":true,"addresses":["0x1234567890abcdef1234567890abcdef12345678","0xabcdef1234567890abcdef1234567890abcdef12"]}},"jsonrpc":"2.0","id":22}'
```

---

## 4. Prompts

| Prompt Name | Purpose | Template / Example |
|-------------|--------|------------------|
| smart-money-analysis | Smart money address analysis and trading recommendations | ```You are a quantitative trading expert. Analyze the input smart money address data: 1. Identify characteristics of high win-rate addresses 2. Analyze their position preferences and trading style 3. Provide copy-trading strategy suggestions Output in JSON format``` |
| whale-tracking | Whale behavior analysis and market impact assessment | ```Analyze whale position data and latest movements: 1. Judge main force intentions 2. Assess market impact 3. Predict short-term trends 4. Provide trading recommendations Output in JSON format``` |
| market-sentiment | Market sentiment analysis | ```Based on market data (order book, active orders, whale long/short ratio): 1. Analyze current market sentiment 2. Identify support/resistance levels 3. Judge short-term trends Output in JSON format``` |
| trader-evaluation | Trader capability evaluation | ```Comprehensively evaluate a trader's ability: 1. Analyze win rate and profit/loss ratio 2. Assess risk management capability 3. Analyze coin preferences 4. Provide comprehensive score and improvement suggestions Output in JSON format``` |

**Usage Notes:**
- Prompts can be dynamically populated with resources content
- Multiple prompts can be combined to form reasoning chains
- JSON output format is recommended for easy Agent parsing

---

## 5. Usage Examples

### Example 1: Discover and Analyze Smart Money Addresses

1. Call Tool: `find_smart_money(7, "win-rate", true)`
2. Get list of high win-rate smart money addresses
3. Use Prompt: `smart-money-analysis` to analyze characteristics of these addresses
4. Generate analysis report and copy-trading recommendations

### Example 2: Whale Behavior Monitoring

1. Call Tool: `get_whale_events(20)` to get latest whale movements
2. Call Tool: `get_whale_directions("BTC")` to view BTC whale long/short ratio
3. Use Prompt: `whale-tracking` to analyze whale behavior
4. Generate market impact assessment report

### Example 3: In-depth Trader Analysis

1. Call Tool: `get_trader_stats(address, 30)` to get basic statistics
2. Call Tool: `get_performance_by_coin(address, 30, 20)` to view coin-specific performance
3. Call Tool: `get_completed_position_history(address, "BTC")` to view historical positions
4. Use Prompt: `trader-evaluation` to generate comprehensive evaluation report

### Example 4: Comprehensive Market Sentiment Analysis

1. Call Tool: `get_all_mids()` to get market mid prices
2. Call Tool: `get_l2_order_book("BTC")` to get order book data
3. Call Tool: `get_market_stats("BTC", 100000)` to get active order statistics
4. Call Tool: `get_whale_history_ratio("1d", 30)` to get historical long/short ratio
5. Use Prompt: `market-sentiment` to generate market sentiment analysis report

---

## 6. Important Notes

### MCP Call Instructions
- **sessionId**: Need to obtain session ID via SSE connection first, GET access to https://mcp.hyperbot.network/mcp/sse
- **JSON-RPC 2.0**: Follows standard JSON-RPC 2.0 protocol
- **method**: Fixed as `tools/call`
- **params.name**: MCP tool name (corresponds to @McpTool annotation's name attribute)
- **params.arguments**: Tool parameters, passed as key-value pairs

### Rate Limiting
- Single IP request frequency limit: 100 requests/minute
- Batch interfaces support maximum 50 addresses

### Data Update Frequency
- Market data: Real-time updates
- Smart money leaderboard: Updated hourly
- Whale positions: Real-time updates
- Trader statistics: Updated every 5 minutes
