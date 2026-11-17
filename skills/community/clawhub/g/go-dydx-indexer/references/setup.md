# go-dydx-indexer: setup and reference

## Requirements

- Go 1.26.10 or newer, per the module's `go.mod`.
- Runtime dependency: `github.com/oapi-codegen/runtime`.

## Install

```bash
go get github.com/psyb0t/go-dydx-indexer
```

The package name is `dydxindexer`. The module path ends in `go-dydx-indexer`, so import it with an explicit name:

```go
import dydxindexer "github.com/psyb0t/go-dydx-indexer"
```

## Base URLs

The paths in the spec start after `/v4`, so the base URL includes it:

| Network | Base URL |
|---|---|
| Mainnet | `https://indexer.dydx.trade/v4` |
| Testnet | `https://indexer.v4testnet.dydx.exchange/v4` |

No auth header is needed.

## Client

- `dydxindexer.NewClientWithResponses(server string, opts ...ClientOption)` returns a `*ClientWithResponses`. Each method returns a typed response struct.
- `dydxindexer.NewClient` is the lower-level variant returning `*http.Response`.
- Options: `WithHTTPClient` (your own `*http.Client`, for timeouts and proxies), `WithRequestEditorFn`, `WithBaseURL`.

## Operations

Typed methods are the operation ID plus `WithResponse`:

| Area | Operations |
|---|---|
| Chain | `GetHeight`, `GetTime` |
| Markets | `ListPerpetualMarkets`, `GetPerpetualMarket` (orderbook for one ticker), `GetCandles`, `GetTrades`, `GetHistoricalFunding`, `Get` (sparklines) |
| Addresses | `GetAddress`, `GetSubaccount`, `GetParentSubaccount`, `RegisterToken`, `TestNotification` |
| Positions | `ListPositions`, `ListPositionsForParentSubaccount`, `GetAssetPositions`, `GetAssetPositionsForParentSubaccount` |
| Orders and fills | `ListOrders`, `ListOrdersForParentSubaccount`, `GetOrder`, `GetFills`, `GetFillsForParentSubaccount` |
| Transfers and funding | `GetTransfers`, `GetTransfersForParentSubaccount`, `GetTransferBetween`, `GetFundingPayments`, `GetFundingPaymentsForParentSubaccount` |
| PnL and history | `GetHistoricalPnl`, `GetHistoricalPnlForParentSubaccount`, `GetPnl`, `GetPnlForParentSubaccount`, `GetTradeHistory`, `GetTradeHistoryForParentSubaccount` |
| Rewards | `GetTradingRewards`, `GetAggregations` |
| Affiliates | `GetMetadata`, `GetAffiliateAddress`, `UpdateCode`, `GetSnapshot`, `GetTotalVolume` |
| Vaults | `GetMegavaultHistoricalPnl`, `GetVaultsHistoricalPnl`, `GetMegavaultPositions` |
| Compliance and search | `Screen`, `GetComplianceScreen`, `SearchTrader` |
| Turnkey | `UploadAddress`, `SignIn`, `AppleLoginRedirect` |

`GetAffiliateAddress` and `GetComplianceScreen` are renamed by `make generate`; the upstream spec gives them the same IDs as `GetAddress` and `Screen`.

Check the exact parameter types of a method with `go doc github.com/psyb0t/go-dydx-indexer <Method>` before using it.

## Types

- Decimal values (prices, sizes, volumes, PnL) are strings.
- `IsoString` is a `string` alias holding an ISO 8601 timestamp.
- Numeric query parameters with no format, such as `Limit`, are `*float64`.
- Finite values are named string types with constants, for example `CandleResolutionN1HOUR`, `CandleResolutionN1DAY`.

## Errors

| Case | What you get |
|---|---|
| Network failure, bad URL, undecodable JSON | non-nil `err` |
| 200 | `JSON200` set |
| Any other status | `StatusCode()` and raw `Body`, `JSON200` nil |
