# Futu / moomoo OpenAPI Reference

Official docs:
- Futu OpenAPI: <https://openapi.futunn.com/futu-api-doc/en/>
- moomoo OpenAPI: <https://openapi.moomoo.com/moomoo-api-doc/en/>

## Package and import patterns

- `pip install futu-api` -> `import futu` / `from futu import ...`
- `pip install moomoo-api` -> `import moomoo` / `from moomoo import ...`
- This skill lazy-loads one of those modules at runtime so help text still works when neither package is installed.

## Connections and contexts

| API area | Constructor | Notes |
|---------|-------------|-------|
| Quotes | `OpenQuoteContext(host, port)` | Market data, snapshots, global state |
| Securities trading | `OpenSecTradeContext(host, port, filter_trdmarket=TrdMarket.US)` | Stock/ETF trading context for one trade market |

Always close contexts with `ctx.close()`.

Use `get_acc_list()` before live trading to confirm the target account, especially when multiple accounts are visible in OpenD.

## Return pattern

- Success: `ret == RET_OK` (or `0`)
- Failure: `ret != RET_OK`; payload is usually an error string
- Query methods typically return `pandas.DataFrame`
- `get_global_state()` returns a `dict`

## Quote APIs

| Method | Returns | Notes |
|-------|---------|-------|
| `get_global_state()` | `dict` | OpenD status, login state, market state |
| `get_market_snapshot(code_list)` | `DataFrame` | Snapshot quotes for up to 400 codes per request |
| `request_history_kline(code, ktype, start='', end='', max_count=..., extended_time=False)` | `(ret, data, page_req_key)` | Historical K-lines |
| `get_cur_kline(code, num, ktype)` | `DataFrame` | Current-session K-lines |
| `get_order_book(code)` | `dict` | Level 2 entitlement may be required |
| `get_rt_ticker(code, num)` | `DataFrame` | Tick-by-tick trades |
| `get_rt_data(code)` | `DataFrame` | Intraday data |

Supported K-line enums commonly used in this skill:
- `KLType.K_1M`
- `KLType.K_5M`
- `KLType.K_15M`
- `KLType.K_30M`
- `KLType.K_60M`
- `KLType.K_DAY`
- `KLType.K_WEEK`
- `KLType.K_MON`
- `KLType.K_QUARTER`
- `KLType.K_YEAR`

## Trade APIs

### Live-trading safety

- Live trading must unlock the account with `unlock_trade(password=...)` before placing, modifying, or canceling orders.
- Paper trading does not need unlock.
- The documented cancel path is `modify_order(ModifyOrderOp.CANCEL, ...)`; the official docs do not present a separate `cancel_order()` helper.

| Method | Purpose | Notes |
|-------|---------|-------|
| `get_acc_list()` | Account discovery | Use before real trading |
| `unlock_trade(password=None, password_md5=None, is_unlock=True)` | Unlock or lock live trading | Pass `is_unlock=False` to re-lock |
| `place_order(...)` | Place an order | `OrderType.NORMAL` = limit, `OrderType.MARKET` = market |
| `modify_order(modify_order_op, order_id, price, qty, ...)` | Modify or cancel an order | `ModifyOrderOp.NORMAL` edits; `ModifyOrderOp.CANCEL` cancels |
| `accinfo_query(...)` | Funds / buying power | Returns account balances |
| `position_list_query(...)` | Positions | Supports `code`, `position_market`, `refresh_cache` |
| `order_list_query(...)` | Open orders | Not historical order history |
| `history_order_list_query(...)` | Historical orders | Supports `start` / `end` |
| `deal_list_query(...)` | Today's deals | Live trading only |
| `history_deal_list_query(...)` | Historical deals | Live trading only |

Useful enums:
- `TrdEnv.SIMULATE`, `TrdEnv.REAL`
- `TrdSide.BUY`, `TrdSide.SELL`
- `OrderType.NORMAL`, `OrderType.MARKET`
- `ModifyOrderOp.NORMAL`, `ModifyOrderOp.CANCEL`
- `TrdMarket.US`, `TrdMarket.HK`, `TrdMarket.SG`, `TrdMarket.JP`

## Notes for this skill

- `trade.py` unlocks only for the requested live mutation, then re-locks the account.
- `portfolio.py --orders` shows open orders. Historical orders moved to `--history-orders`.
- `quote.py` supports explicit `--start` / `--end` ranges for historical K-lines.
