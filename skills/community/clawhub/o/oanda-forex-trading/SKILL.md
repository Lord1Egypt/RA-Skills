---
name: oanda-forex-trading
description: "Oanda Forex Trading: Trade forex via OANDA. Real-time prices, historical candles, order management, positions. Supports demo and live accounts. Use when an agent needs oanda forex trading, oanda forex trading 2, forex trading automation, currency trading bot, fx trading api, oanda api integration, cancel order, order id through AgentPMT-hosted remote tool calls. Discovery terms: oanda forex trading, oanda forex trading 2, forex trading automation, currency trading bot, fx trading api."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/oanda-forex-trading-2
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/oanda-forex-trading-2"}}
---
# Oanda Forex Trading

## Freshness
Last updated: `2026-06-23`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
OANDA Forex is a comprehensive foreign exchange trading interface that connects AI agents and automation workflows to OANDA's REST v20 API for real-time currency trading and market data access. It provides a simplified action-based abstraction over OANDA's trading platform, supporting both practice accounts for paper trading and live accounts for real money transactions. Market data capabilities include fetching real-time bid and ask prices with spread calculations for single or multiple currency pairs, as well as historical candlestick data across 21 granularities ranging from 5-second intervals to monthly bars with up to 5000 candles per request. Account management functions retrieve balance, margin, net asset value, unrealized and realized profit and loss, open trade counts, and pending order status. The trading engine supports market orders for immediate execution, limit orders for price-targeted entries, and stop orders for breakout or momentum strategies, all with optional take profit and stop loss levels attached at order creation. Position and order management includes viewing open positions and trades, modifying pending order parameters, canceling unfilled orders, and closing positions either by instrument or by individual trade ID.  It is highly recommended that you perform extensive testing with demo accounts before placing any live orders.

## Product Instructions
### Oanda Forex Trading - Tool Instructions

#### Overview

Trade forex currencies and access real-time market data through the OANDA platform. This tool supports live and practice trading environments, covering market data retrieval, account management, order placement, and position/trade management. Credentials are provided automatically when connected.

#### Instrument Format

Currency pairs use underscore-separated format: `EUR_USD`, `GBP_JPY`, `USD_CAD`, `AUD_NZD`, etc.

---

#### Actions

##### get_price

Get current bid/ask pricing for one or more currency pairs.

**Required fields (at least one):**
- `instrument` (string) - Single currency pair, e.g. `EUR_USD`
- `instruments` (array of strings) - Multiple currency pairs for batch pricing

Returns bid, ask, spread, timestamp, and whether the instrument is currently tradeable.

**Example:**
```json
{
  "action": "get_price",
  "instruments": ["EUR_USD", "GBP_USD", "USD_JPY"]
}
```

---

##### get_candles

Get historical candlestick (OHLCV) data for a single instrument.

**Required fields:**
- `instrument` (string) - Currency pair, e.g. `EUR_USD`
- `granularity` (string) - Time interval per candle. Options: `S5`, `S10`, `S15`, `S30` (seconds), `M1`, `M2`, `M4`, `M5`, `M10`, `M15`, `M30` (minutes), `H1`, `H2`, `H3`, `H4`, `H6`, `H8`, `H12` (hours), `D` (daily), `W` (weekly), `M` (monthly)

**Optional fields:**
- `count` (integer) - Number of candles to retrieve. Default: 100. Range: 1-5000.

Returns open, high, low, close, volume, and timestamp for each candle.

**Example:**
```json
{
  "action": "get_candles",
  "instrument": "EUR_USD",
  "granularity": "H1",
  "count": 50
}
```

---

##### get_account_summary

Get account overview including balance, margin, and profit/loss information.

**Required fields:** None (credentials are provided automatically).

Returns balance, NAV, unrealized P&L, realized P&L, margin used, margin available, open trade count, open position count, and pending order count.

**Example:**
```json
{
  "action": "get_account_summary"
}
```

---

##### get_positions

Get all currently open positions.

**Required fields:** None.

Returns a list of open positions with instrument, long/short units, average prices, and unrealized/realized P&L for each side.

**Example:**
```json
{
  "action": "get_positions"
}
```

---

##### get_trades

Get all currently open trades with details.

**Required fields:** None.

Returns trade ID, instrument, units, entry price, unrealized/realized P&L, margin used, open time, and any attached take-profit or stop-loss order IDs.

**Example:**
```json
{
  "action": "get_trades"
}
```

---

##### get_pending_orders

Get all pending (unfilled) orders.

**Required fields:** None.

Returns order ID, type, instrument, units, price, time-in-force, and any attached take-profit or stop-loss conditions.

**Example:**
```json
{
  "action": "get_pending_orders"
}
```

---

##### place_market_order

Execute a trade immediately at the current market price.

**Required fields:**
- `instrument` (string) - Currency pair, e.g. `EUR_USD`
- `units` (integer) - Number of units. Positive = buy/long, negative = sell/short. Example: `10000` to buy, `-5000` to sell.

**Optional fields:**
- `take_profit_price` (number) - Automatically attach a take-profit order at this price
- `stop_loss_price` (number) - Automatically attach a stop-loss order at this price
- `stop_loss_distance` (number) - Stop loss as a price distance instead of absolute price (cannot use both stop_loss_price and stop_loss_distance)

**Example - Buy with risk management:**
```json
{
  "action": "place_market_order",
  "instrument": "EUR_USD",
  "units": 10000,
  "take_profit_price": 1.0950,
  "stop_loss_price": 1.0850
}
```

**Example - Sell (short):**
```json
{
  "action": "place_market_order",
  "instrument": "GBP_USD",
  "units": -5000
}
```

---

##### place_limit_order

Place an order to execute when the price reaches a specified level or better. The order remains active until filled or cancelled.

**Required fields:**
- `instrument` (string) - Currency pair
- `units` (integer) - Positive = buy, negative = sell
- `price` (number) - The limit price at which to execute

**Optional fields:**
- `take_profit_price` (number) - Take-profit price to attach on fill
- `stop_loss_price` (number) - Stop-loss price to attach on fill
- `stop_loss_distance` (number) - Stop-loss distance to attach on fill

**Example:**
```json
{
  "action": "place_limit_order",
  "instrument": "EUR_USD",
  "units": 10000,
  "price": 1.0800,
  "take_profit_price": 1.0900,
  "stop_loss_price": 1.0750
}
```

---

##### place_stop_order

Place an order that triggers when the price reaches a specified level. Useful for breakout strategies. The order remains active until triggered or cancelled.

**Required fields:**
- `instrument` (string) - Currency pair
- `units` (integer) - Positive = buy, negative = sell
- `price` (number) - The trigger price

**Optional fields:**
- `take_profit_price` (number) - Take-profit price to attach on fill
- `stop_loss_price` (number) - Stop-loss price to attach on fill
- `stop_loss_distance` (number) - Stop-loss distance to attach on fill

**Example:**
```json
{
  "action": "place_stop_order",
  "instrument": "USD_JPY",
  "units": 5000,
  "price": 150.50,
  "stop_loss_distance": 0.50
}
```

---

##### modify_order

Modify the price, units, or trailing stop distance of an existing pending order. The tool automatically detects the order type and applies the appropriate modification.

**Required fields:**
- `order_id` (string) - The order ID to modify (get from `get_pending_orders`)

**Optional fields (at least one required for limit/stop/market-if-touched orders):**
- `price` (number) - New price level
- `units` (integer) - New unit amount

**For trailing stop loss orders:**
- `trailing_stop_distance` (number) - New trailing distance (required)

**For stop loss orders:**
- `price` (number) - New stop loss price, OR
- `stop_loss_distance` (number) - New stop loss distance

**Example:**
```json
{
  "action": "modify_order",
  "order_id": "12345",
  "price": 1.0825
}
```

---

##### cancel_order

Cancel a pending order.

**Required fields:**
- `order_id` (string) - The order ID to cancel (get from `get_pending_orders`)

**Example:**
```json
{
  "action": "cancel_order",
  "order_id": "12345"
}
```

---

##### close_position

Close the entire position (both long and short sides) for a specific instrument.

**Required fields:**
- `instrument` (string) - Currency pair to close, e.g. `EUR_USD`

Returns details of closed long/short sides and total profit/loss.

**Example:**
```json
{
  "action": "close_position",
  "instrument": "EUR_USD"
}
```

---

##### close_trade

Close a specific individual trade by its ID.

**Required fields:**
- `trade_id` (string) - The trade ID to close (get from `get_trades`)

Returns the closing price, units closed, and realized profit/loss.

**Example:**
```json
{
  "action": "close_trade",
  "trade_id": "67890"
}
```

---

#### Common Workflows

**Check prices then trade:**
1. `get_price` to see current bid/ask for your target pair
2. `place_market_order` to enter at market, or `place_limit_order` to set a target entry

**Monitor and manage positions:**
1. `get_account_summary` to check overall account health
2. `get_positions` to see all open positions
3. `get_trades` to see individual trade details and IDs
4. `close_trade` or `close_position` to exit

**Manage pending orders:**
1. `get_pending_orders` to list all unfilled orders
2. `modify_order` to adjust price or size
3. `cancel_order` to remove an order

**Technical analysis:**
1. `get_candles` with desired granularity and count to pull historical OHLCV data
2. Analyze trends, support/resistance, or other patterns

#### Important Notes

- **Units direction:** Positive units = buy/long, negative units = sell/short
- **Stop loss options:** Use either `stop_loss_price` (absolute price) or `stop_loss_distance` (relative distance), never both
- **Practice vs Live:** The environment is configured through your connected credentials. Practice uses simulated funds; live uses real money.
- **Market hours:** Forex markets are open 24/5 (Sunday evening to Friday evening UTC). Prices may not be tradeable outside these hours.
- **Order persistence:** Limit and stop orders use Good-Til-Cancelled (GTC) by default and remain active until filled or manually cancelled.
- **Price values:** All prices must be positive numbers.

## When To Use
- Use this skill for `Oanda Forex Trading` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: oanda forex trading, oanda forex trading 2, forex trading automation, currency trading bot, fx trading api, oanda api integration, cancel order, order id.
- Supported action names: `cancel_order`, `close_position`, `close_trade`, `get_account_summary`, `get_candles`, `get_pending_orders`, `get_positions`, `get_price`, `get_trades`, `modify_order`, `place_limit_order`, `place_market_order`, `place_stop_order`.

## Use Cases
- Forex trading automation
- currency trading bot
- FX trading API
- OANDA API integration
- foreign exchange automation
- algorithmic forex trading
- automated currency trading
- forex market data
- real-time forex prices
- currency pair quotes
- bid ask spread
- EUR USD trading
- GBP JPY trading
- forex candlestick data
- OHLC data retrieval
- historical forex data

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `13`.
x402 availability: not enabled for this product.

- `cancel_order` (action slug: `cancel-order`): Cancel a pending (unfilled) order by its ID. Price: `2` credits. Parameters: `order_id`.
- `close_position` (action slug: `close-position`): Close the entire position (both long and short sides) for a specific instrument. Returns details of closed sides and total P&L. Price: `2` credits. Parameters: `instrument`.
- `close_trade` (action slug: `close-trade`): Close a specific individual trade by its ID. Returns closing price, units closed, and realized P&L. Price: `2` credits. Parameters: `trade_id`.
- `get_account_summary` (action slug: `get-account-summary`): Get account overview including balance, margin, NAV, unrealized/realized P&L, and open trade/position/order counts. Credentials provided automatically. Price: `2` credits. Parameters: none.
- `get_candles` (action slug: `get-candles`): Get historical candlestick (OHLCV) data for a single instrument across 21 granularities from 5-second to monthly bars. Price: `2` credits. Parameters: `count`, `granularity`, `instrument`.
- `get_pending_orders` (action slug: `get-pending-orders`): Get all pending (unfilled) orders with order ID, type, instrument, units, price, time-in-force, and attached conditions. Price: `2` credits. Parameters: none.
- `get_positions` (action slug: `get-positions`): Get all currently open positions with instrument, long/short units, average prices, and unrealized/realized P&L. Price: `2` credits. Parameters: none.
- `get_price` (action slug: `get-price`): Get current bid/ask pricing for one or more currency pairs. Returns bid, ask, spread, timestamp, and tradeability status. Price: `2` credits. Parameters: `instrument`, `instruments`.
- `get_trades` (action slug: `get-trades`): Get all currently open trades with trade ID, instrument, units, entry price, unrealized/realized P&L, margin used, and attached order IDs. Price: `2` credits. Parameters: none.
- `modify_order` (action slug: `modify-order`): Modify a pending order's price, units, or trailing stop distance. Automatically detects order type and applies appropriate modification. Price: `2` credits. Parameters: `order_id`, `price`, `stop_loss_distance`, `trailing_stop_distance`, `units`.
- `place_limit_order` (action slug: `place-limit-order`): Place an order to execute when price reaches a specified level or better. Remains active until filled or cancelled (GTC). Price: `2` credits. Parameters: `instrument`, `price`, `stop_loss_distance`, `stop_loss_price`, `take_profit_price`, `units`.
- `place_market_order` (action slug: `place-market-order`): Execute a trade immediately at the current market price. Positive units = buy/long, negative units = sell/short. Price: `2` credits. Parameters: `instrument`, `stop_loss_distance`, `stop_loss_price`, `take_profit_price`, `units`.
- `place_stop_order` (action slug: `place-stop-order`): Place an order that triggers when price reaches a specified level. Useful for breakout strategies. Remains active until triggered or cancelled (GTC). Price: `2` credits. Parameters: `instrument`, `price`, `stop_loss_distance`, `stop_loss_price`, `take_profit_price`, `units`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "oanda-forex-trading-2"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "oanda-forex-trading-2"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "oanda-forex-trading-2"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "oanda-forex-trading-2"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "oanda-forex-trading-2"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "oanda-forex-trading-2"
  }
}
```

## Call This Tool
Product slug: `oanda-forex-trading-2`

Marketplace page: https://www.agentpmt.com/marketplace/oanda-forex-trading-2

- AgentPMT account route: first use `../agentpmt-account-mcp-rest-api-setup` to connect the main MCP server or REST API for an Agent Group where this tool is enabled.
- x402 route: not enabled for this product.
- AgentPMT overview: use `../what-is-agentpmt` for marketplace, Agent Group, workflow, MCP, REST, and payment concepts.

If those setup skills are not installed beside this product skill, use the downloads below.

Core AgentPMT setup skills:
- What AgentPMT is: ../what-is-agentpmt
  - ClawHub page: https://clawhub.ai/agentpmt/what-is-agentpmt
  - OpenClaw install: `openclaw skills install what-is-agentpmt`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup
  - ClawHub page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup
  - OpenClaw install: `openclaw skills install agentpmt-account-mcp-rest-api-setup`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`

skills.sh install script:

```bash
npx skills add AgentPMT/agent-skills --skill what-is-agentpmt
npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup
```

MCP call shape after the main AgentPMT MCP server is connected:

```json
{
  "method": "tools/call",
  "params": {
    "name": "Oanda-Forex-Trading",
    "arguments": {
      "action": "cancel_order",
      "order_id": "example order id"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "oanda-forex-trading-2",
  "parameters": {
    "action": "cancel_order",
    "order_id": "example order id"
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `cancel_order` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/oanda-forex-trading-2
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
