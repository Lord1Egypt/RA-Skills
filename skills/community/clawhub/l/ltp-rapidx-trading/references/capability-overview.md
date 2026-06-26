# RapidX Capability Overview

Use `rapidx schema --json` or MCP `rapidx/tools` as the runtime source of truth. This reference is a compact map for Agent planning.

## Runtime Layers

| Layer | Purpose |
|---|---|
| CLI | Atomic local operations through `rapidx <domain> <action> --json` |
| MCP | Structured Agent tools served by `rapidx mcp serve` |
| Core | Shared schemas, credential resolution, RapidX API client, preview, automation, audit, and self-check |
| Skills | Agent guidance for setup, review, trading, automation, and readback |

## Diagnostics And Discovery

| CLI | MCP tool |
|---|---|
| `rapidx --version` | - |
| `rapidx schema --json` | `rapidx/tools` |
| `rapidx update check --json` | `rapidx/update/check` |
| `rapidx auth check` | - |
| `rapidx doctor --json` | - |
| `rapidx self-check --json` | `rapidx/self-check` |
| `rapidx mcp serve` | starts the MCP server |

## Automation

Automation sessions are local authorization sessions. They do not map to RapidX HTTP endpoints.

| CLI | MCP tool |
|---|---|
| `rapidx automation start` | `rapidx/automation/start` |
| `rapidx automation list` | `rapidx/automation/list` |
| `rapidx automation status` | `rapidx/automation/status` |
| `rapidx automation extend` | `rapidx/automation/extend` |
| `rapidx automation stop` | `rapidx/automation/stop` |

## Market

| CLI | MCP tool |
|---|---|
| `rapidx market get-ticker` | `rapidx/market/get-ticker` |
| `rapidx market get-orderbook` | `rapidx/market/get-orderbook` |
| `rapidx market get-klines` | `rapidx/market/get-klines` |
| `rapidx market get-funding-rate` | `rapidx/market/get-funding-rate` |
| `rapidx market get-mark-price` | `rapidx/market/get-mark-price` |
| `rapidx market get-symbol-info` | `rapidx/market/get-symbol-info` |
| `rapidx market get-open-interest` | `rapidx/market/get-open-interest` |

## Portfolio

| CLI | MCP tool | RapidX API |
|---|---|---|
| `rapidx portfolio overview` | `rapidx/portfolio/overview` | `GET /api/v1/trading/account` |
| `rapidx portfolio assets` | `rapidx/portfolio/assets` | `GET /api/v1/trading/portfolio/assets` |
| `rapidx portfolio statement` | `rapidx/portfolio/statement` | `GET /api/v1/trading/statement` |
| `rapidx portfolio user-fee-rate` | `rapidx/portfolio/user-fee-rate` | `GET /api/v1/trading/userFeeRate` |
| `rapidx portfolio position-bracket` | `rapidx/portfolio/position-bracket` | `GET /api/v1/trading/positionBracket` |
| `rapidx portfolio set-position-mode` | `rapidx/portfolio/set-position-mode` | `POST /api/v1/trading/account` |

## Orders

| CLI | MCP tool | RapidX API |
|---|---|---|
| `rapidx order place-preview` | `rapidx/order/place-preview` | preview for place |
| `rapidx order replace-preview` | `rapidx/order/replace-preview` | preview for replace |
| `rapidx order cancel-preview` | `rapidx/order/cancel-preview` | preview for cancel |
| `rapidx order place` | `rapidx/order/place` | `POST /api/v1/trading/order` |
| `rapidx order replace` | `rapidx/order/replace` | `PUT /api/v1/trading/order` |
| `rapidx order cancel` | `rapidx/order/cancel` | `DELETE /api/v1/trading/order` |
| `rapidx order cancel-all` | `rapidx/order/cancel-all` | `DELETE /api/v1/trading/cancelAll` |
| `rapidx order query` | `rapidx/order/query` | `GET /api/v1/trading/order` |
| `rapidx order open-orders` | `rapidx/order/open-orders` | `GET /api/v1/trading/orders` |
| `rapidx order history` | `rapidx/order/history` | `GET /api/v1/trading/history/orders` |

`open-orders` means current non-terminal orders, not "open a new order". `order.history` accepts optional `begin` and `end` timestamps in milliseconds; if omitted, RapidX applies the upstream default range.

## Transactions

| CLI | MCP tool | RapidX API |
|---|---|---|
| `rapidx transaction executions` | `rapidx/transaction/executions` | `GET /api/v1/trading/executions` |

## Positions

| CLI | MCP tool | RapidX API |
|---|---|---|
| `rapidx position query` | `rapidx/position/query` | `GET /api/v1/trading/position` |
| `rapidx position history` | `rapidx/position/history` | `GET /api/v1/trading/history/position` |
| `rapidx position get-leverage` | `rapidx/position/get-leverage` | `GET /api/v1/trading/perp/leverage` |
| `rapidx position set-leverage` | `rapidx/position/set-leverage` | `POST /api/v1/trading/position/leverage` |
| `rapidx position close` | `rapidx/position/close` | `DELETE /api/v1/trading/position` |
| `rapidx position close-all` | `rapidx/position/close-all` | `DELETE /api/v1/trading/positions` |

`position.close` does not take `side` or `quantity`. In NET mode, omit `positionSide`; in HEDGE mode, pass the actual `LONG` or `SHORT` side.

## Algo Orders

| CLI | MCP tool | RapidX API |
|---|---|---|
| `rapidx algo place` | `rapidx/algo/place` | `POST /api/v1/algo/order` |
| `rapidx algo replace` | `rapidx/algo/replace` | `PUT /api/v1/algo/order` |
| `rapidx algo cancel` | `rapidx/algo/cancel` | `DELETE /api/v1/algo/order` |
| `rapidx algo query` | `rapidx/algo/query` | `GET /api/v1/algo/order` |
| `rapidx algo open-orders` | `rapidx/algo/open-orders` | `GET /api/v1/algo/openOrders` |
| `rapidx algo history` | `rapidx/algo/history` | `GET /api/v1/algo/history/orders` |

`algo.open-orders` means current non-terminal algo orders. `algo.history` accepts optional `begin` and `end` timestamps in milliseconds; if omitted, RapidX applies the upstream default range.

## Generic Preview And Live Verification

| CLI | MCP tool |
|---|---|
| `rapidx trade preview` | `rapidx/trade/preview` |
| `rapidx trade verify-live` | `rapidx/trade/verify-live` |

Use `rapidx/trade/preview` for non-order writes such as `position.set-leverage`, `position.close`, `portfolio.set-position-mode`, `algo.place`, `algo.replace`, and `algo.cancel`.

## Symbol Format

Recommended input symbols:

```text
BINANCE_PERP_<BASE>_<QUOTE>
OKX_PERP_<BASE>_<QUOTE>
```

Examples:

```text
BINANCE_PERP_BTC_USDT
BINANCE_PERP_ETH_USDT
OKX_PERP_BTC_USDT
```

`OKX_SWAP_<BASE>_<QUOTE>` is accepted as an input alias and normalizes to `OKX_PERP_<BASE>_<QUOTE>`.

## Status Meanings

| Status | Meaning |
|---|---|
| `PASS` | Tool or command completed successfully |
| `INVALID_INPUT` | Local schema or input validation failed |
| `BLOCKED` | Preview, safety, compatibility, or policy check blocked the action |
| `NOT_FOUND` | Requested resource was not found |
| `PERMISSION_SCOPE_ERROR` | Credentials do not cover the requested scope |
| `BUSINESS_ERROR` | RapidX or venue business rule rejected the request |
| `NOT_VERIFIED` | Requested state could not be proven |
| `FAIL` | Startup, auth, network, malformed response, or unexpected failure |
