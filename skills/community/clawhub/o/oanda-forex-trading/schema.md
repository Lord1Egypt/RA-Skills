# Oanda Forex Trading Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `oanda-forex-trading-2`

x402 availability: not enabled for this product.

## `cancel_order`

Action slug: `cancel-order`

Price: `2` credits

Cancel a pending (unfilled) order by its ID.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `order_id` | `string` | yes | The order ID to cancel (get from get_pending_orders). |

Sample parameters:

```json
{
  "order_id": "example order id"
}
```

Generated JSON parameter schema:

```json
{
  "order_id": {
    "description": "The order ID to cancel (get from get_pending_orders).",
    "required": true,
    "type": "string"
  }
}
```

## `close_position`

Action slug: `close-position`

Price: `2` credits

Close the entire position (both long and short sides) for a specific instrument. Returns details of closed sides and total P&L.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `instrument` | `string` | yes | Currency pair to close (e.g., 'EUR_USD'). |

Sample parameters:

```json
{
  "instrument": "example instrument"
}
```

Generated JSON parameter schema:

```json
{
  "instrument": {
    "description": "Currency pair to close (e.g., 'EUR_USD').",
    "required": true,
    "type": "string"
  }
}
```

## `close_trade`

Action slug: `close-trade`

Price: `2` credits

Close a specific individual trade by its ID. Returns closing price, units closed, and realized P&L.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `trade_id` | `string` | yes | The trade ID to close (get from get_trades). |

Sample parameters:

```json
{
  "trade_id": "example trade id"
}
```

Generated JSON parameter schema:

```json
{
  "trade_id": {
    "description": "The trade ID to close (get from get_trades).",
    "required": true,
    "type": "string"
  }
}
```

## `get_account_summary`

Action slug: `get-account-summary`

Price: `2` credits

Get account overview including balance, margin, NAV, unrealized/realized P&L, and open trade/position/order counts. Credentials provided automatically.

Parameters:

This action does not require parameters.

Sample parameters:

```json
{}
```

Generated JSON parameter schema:

```json
{}
```

## `get_candles`

Action slug: `get-candles`

Price: `2` credits

Get historical candlestick (OHLCV) data for a single instrument across 21 granularities from 5-second to monthly bars.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `count` | `integer` | no | Number of candles to retrieve (default: 100, max: 5000). |
| `granularity` | `string` | yes | Candle time granularity. Seconds: S5, S10, S15, S30. Minutes: M1, M2, M4, M5, M10, M15, M30. Hours: H1, H2, H3, H4, H6, H8, H12. Other: D (daily), W (weekly), M (monthly). |
| `instrument` | `string` | yes | Currency pair in OANDA format (e.g., 'EUR_USD'). |

Sample parameters:

```json
{
  "count": 100,
  "granularity": "S5",
  "instrument": "example instrument"
}
```

Generated JSON parameter schema:

```json
{
  "count": {
    "default": 100,
    "description": "Number of candles to retrieve (default: 100, max: 5000).",
    "maximum": 5000,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "granularity": {
    "description": "Candle time granularity. Seconds: S5, S10, S15, S30. Minutes: M1, M2, M4, M5, M10, M15, M30. Hours: H1, H2, H3, H4, H6, H8, H12. Other: D (daily), W (weekly), M (monthly).",
    "enum": [
      "S5",
      "S10",
      "S15",
      "S30",
      "M1",
      "M2",
      "M4",
      "M5",
      "M10",
      "M15",
      "M30",
      "H1",
      "H2",
      "H3",
      "H4",
      "H6",
      "H8",
      "H12",
      "D",
      "W",
      "M"
    ],
    "required": true,
    "type": "string"
  },
  "instrument": {
    "description": "Currency pair in OANDA format (e.g., 'EUR_USD').",
    "required": true,
    "type": "string"
  }
}
```

## `get_pending_orders`

Action slug: `get-pending-orders`

Price: `2` credits

Get all pending (unfilled) orders with order ID, type, instrument, units, price, time-in-force, and attached conditions.

Parameters:

This action does not require parameters.

Sample parameters:

```json
{}
```

Generated JSON parameter schema:

```json
{}
```

## `get_positions`

Action slug: `get-positions`

Price: `2` credits

Get all currently open positions with instrument, long/short units, average prices, and unrealized/realized P&L.

Parameters:

This action does not require parameters.

Sample parameters:

```json
{}
```

Generated JSON parameter schema:

```json
{}
```

## `get_price`

Action slug: `get-price`

Price: `2` credits

Get current bid/ask pricing for one or more currency pairs. Returns bid, ask, spread, timestamp, and tradeability status.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `instrument` | `string` | no | Single trading instrument/currency pair in OANDA format (e.g., 'EUR_USD', 'GBP_JPY'). Provide instrument or instruments. |
| `instruments` | `array` | no | List of trading instruments for batch pricing (e.g., ['EUR_USD', 'GBP_USD', 'USD_JPY']). Provide instrument or instruments. |

Sample parameters:

```json
{
  "instrument": "example instrument",
  "instruments": [
    "example instrument"
  ]
}
```

Generated JSON parameter schema:

```json
{
  "instrument": {
    "description": "Single trading instrument/currency pair in OANDA format (e.g., 'EUR_USD', 'GBP_JPY'). Provide instrument or instruments.",
    "required": false,
    "type": "string"
  },
  "instruments": {
    "description": "List of trading instruments for batch pricing (e.g., ['EUR_USD', 'GBP_USD', 'USD_JPY']). Provide instrument or instruments.",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  }
}
```

## `get_trades`

Action slug: `get-trades`

Price: `2` credits

Get all currently open trades with trade ID, instrument, units, entry price, unrealized/realized P&L, margin used, and attached order IDs.

Parameters:

This action does not require parameters.

Sample parameters:

```json
{}
```

Generated JSON parameter schema:

```json
{}
```

## `modify_order`

Action slug: `modify-order`

Price: `2` credits

Modify a pending order's price, units, or trailing stop distance. Automatically detects order type and applies appropriate modification.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `order_id` | `string` | yes | The order ID to modify (get from get_pending_orders). |
| `price` | `number` | no | New price level for limit/stop/take-profit/stop-loss orders. |
| `stop_loss_distance` | `number` | no | New stop loss distance for stop loss orders. Cannot be used with price for stop loss modifications. |
| `trailing_stop_distance` | `number` | no | New trailing distance for trailing stop loss orders. |
| `units` | `integer` | no | New unit amount for limit/stop orders. |

Sample parameters:

```json
{
  "order_id": "example order id",
  "price": 1,
  "stop_loss_distance": 1,
  "trailing_stop_distance": 1,
  "units": 1
}
```

Generated JSON parameter schema:

```json
{
  "order_id": {
    "description": "The order ID to modify (get from get_pending_orders).",
    "required": true,
    "type": "string"
  },
  "price": {
    "description": "New price level for limit/stop/take-profit/stop-loss orders.",
    "required": false,
    "type": "number"
  },
  "stop_loss_distance": {
    "description": "New stop loss distance for stop loss orders. Cannot be used with price for stop loss modifications.",
    "required": false,
    "type": "number"
  },
  "trailing_stop_distance": {
    "description": "New trailing distance for trailing stop loss orders.",
    "required": false,
    "type": "number"
  },
  "units": {
    "description": "New unit amount for limit/stop orders.",
    "required": false,
    "type": "integer"
  }
}
```

## `place_limit_order`

Action slug: `place-limit-order`

Price: `2` credits

Place an order to execute when price reaches a specified level or better. Remains active until filled or cancelled (GTC).

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `instrument` | `string` | yes | Currency pair (e.g., 'EUR_USD'). |
| `price` | `number` | yes | The limit price at which to execute. |
| `stop_loss_distance` | `number` | no | Stop loss distance to attach on fill. Cannot be used with stop_loss_price. |
| `stop_loss_price` | `number` | no | Stop loss price to attach on fill. Cannot be used with stop_loss_distance. |
| `take_profit_price` | `number` | no | Take profit price to attach on fill. |
| `units` | `integer` | yes | Number of units. Positive = buy, negative = sell. |

Sample parameters:

```json
{
  "instrument": "example instrument",
  "price": 1,
  "stop_loss_distance": 1,
  "stop_loss_price": 1,
  "take_profit_price": 1,
  "units": 1
}
```

Generated JSON parameter schema:

```json
{
  "instrument": {
    "description": "Currency pair (e.g., 'EUR_USD').",
    "required": true,
    "type": "string"
  },
  "price": {
    "description": "The limit price at which to execute.",
    "required": true,
    "type": "number"
  },
  "stop_loss_distance": {
    "description": "Stop loss distance to attach on fill. Cannot be used with stop_loss_price.",
    "required": false,
    "type": "number"
  },
  "stop_loss_price": {
    "description": "Stop loss price to attach on fill. Cannot be used with stop_loss_distance.",
    "required": false,
    "type": "number"
  },
  "take_profit_price": {
    "description": "Take profit price to attach on fill.",
    "required": false,
    "type": "number"
  },
  "units": {
    "description": "Number of units. Positive = buy, negative = sell.",
    "required": true,
    "type": "integer"
  }
}
```

## `place_market_order`

Action slug: `place-market-order`

Price: `2` credits

Execute a trade immediately at the current market price. Positive units = buy/long, negative units = sell/short.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `instrument` | `string` | yes | Currency pair (e.g., 'EUR_USD'). |
| `stop_loss_distance` | `number` | no | Stop loss as price distance instead of absolute price. Cannot be used with stop_loss_price. |
| `stop_loss_price` | `number` | no | Stop loss price level. Cannot be used with stop_loss_distance. |
| `take_profit_price` | `number` | no | Take profit price level. Automatically creates a take profit order on fill. |
| `units` | `integer` | yes | Number of units to trade. Positive = buy/long, negative = sell/short. Example: 10000 to buy, -5000 to sell. |

Sample parameters:

```json
{
  "instrument": "example instrument",
  "stop_loss_distance": 1,
  "stop_loss_price": 1,
  "take_profit_price": 1,
  "units": 1
}
```

Generated JSON parameter schema:

```json
{
  "instrument": {
    "description": "Currency pair (e.g., 'EUR_USD').",
    "required": true,
    "type": "string"
  },
  "stop_loss_distance": {
    "description": "Stop loss as price distance instead of absolute price. Cannot be used with stop_loss_price.",
    "required": false,
    "type": "number"
  },
  "stop_loss_price": {
    "description": "Stop loss price level. Cannot be used with stop_loss_distance.",
    "required": false,
    "type": "number"
  },
  "take_profit_price": {
    "description": "Take profit price level. Automatically creates a take profit order on fill.",
    "required": false,
    "type": "number"
  },
  "units": {
    "description": "Number of units to trade. Positive = buy/long, negative = sell/short. Example: 10000 to buy, -5000 to sell.",
    "required": true,
    "type": "integer"
  }
}
```

## `place_stop_order`

Action slug: `place-stop-order`

Price: `2` credits

Place an order that triggers when price reaches a specified level. Useful for breakout strategies. Remains active until triggered or cancelled (GTC).

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `instrument` | `string` | yes | Currency pair (e.g., 'USD_JPY'). |
| `price` | `number` | yes | The trigger price for the stop order. |
| `stop_loss_distance` | `number` | no | Stop loss distance to attach on fill. Cannot be used with stop_loss_price. |
| `stop_loss_price` | `number` | no | Stop loss price to attach on fill. Cannot be used with stop_loss_distance. |
| `take_profit_price` | `number` | no | Take profit price to attach on fill. |
| `units` | `integer` | yes | Number of units. Positive = buy, negative = sell. |

Sample parameters:

```json
{
  "instrument": "example instrument",
  "price": 1,
  "stop_loss_distance": 1,
  "stop_loss_price": 1,
  "take_profit_price": 1,
  "units": 1
}
```

Generated JSON parameter schema:

```json
{
  "instrument": {
    "description": "Currency pair (e.g., 'USD_JPY').",
    "required": true,
    "type": "string"
  },
  "price": {
    "description": "The trigger price for the stop order.",
    "required": true,
    "type": "number"
  },
  "stop_loss_distance": {
    "description": "Stop loss distance to attach on fill. Cannot be used with stop_loss_price.",
    "required": false,
    "type": "number"
  },
  "stop_loss_price": {
    "description": "Stop loss price to attach on fill. Cannot be used with stop_loss_distance.",
    "required": false,
    "type": "number"
  },
  "take_profit_price": {
    "description": "Take profit price to attach on fill.",
    "required": false,
    "type": "number"
  },
  "units": {
    "description": "Number of units. Positive = buy, negative = sell.",
    "required": true,
    "type": "integer"
  }
}
```
