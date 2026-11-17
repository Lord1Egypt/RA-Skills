# go-twelvedata: setup and reference

This module is unofficial and not affiliated with Twelve Data.

## Requirements

- Go 1.26.10 or newer, per the module's `go.mod`.
- A Twelve Data API key exported as `TWELVEDATA_API_KEY`.
- A plan and data permissions that cover the requested instruments and endpoints.

## Install

```bash
go get github.com/psyb0t/go-twelvedata
```

## Base URL

Use `https://api.twelvedata.com`.

## Auth

Set `req.Header.Set("Authorization", "apikey "+key)` in a `twelvedata.WithRequestEditorFn`. The spec alternatively permits `apikey` in the query string. Prefer the header to keep credentials out of URL logs.

## Client

- `twelvedata.NewClientWithResponses(server, opts...)`. Options: `twelvedata.WithRequestEditorFn`, `twelvedata.WithHTTPClient` (an HTTP client with your timeout), `twelvedata.WithBaseURL`.
- Each operation has `Client.X` (raw HTTP response), `ClientWithResponses.XWithResponse` (parsed response) and `NewXRequest` (request only).
- Generated parameter types carry the provider's `x-go-name` names. For instance, `outputsize` becomes `PageSize`, while `dp` becomes `DecimalPlaces`.
- Provider extensions such as `x-required-group` are documentation, not generated validation. Set an instrument identifier such as `Symbol` where the endpoint requires one.

## Main operations

The generated client covers every path in the spec. These are common entry points:

| Method | Endpoint |
| --- | --- |
| `GetPriceWithResponse` | `GET /price` |
| `GetQuoteWithResponse` | `GET /quote` |
| `GetTimeSeriesWithResponse` | `GET /time_series` |
| `GetTimeSeriesCrossWithResponse` | `GET /time_series/cross` |
| `GetExchangeRateWithResponse` | `GET /exchange_rate` |
| `GetCurrencyConversionWithResponse` | `GET /currency_conversion` |
| `GetStocksWithResponse` | `GET /stocks` |
| `GetForexPairsWithResponse` | `GET /forex_pairs` |
| `GetCryptocurrenciesWithResponse` | `GET /cryptocurrencies` |
| `GetExchangesWithResponse` | `GET /exchanges` |
| `GetSymbolSearchWithResponse` | `GET /symbol_search` |
| `GetProfileWithResponse` | `GET /profile` |
| `GetStatisticsWithResponse` | `GET /statistics` |
| `GetIncomeStatementWithResponse` | `GET /income_statement` |
| `GetBalanceSheetWithResponse` | `GET /balance_sheet` |
| `GetCashFlowWithResponse` | `GET /cash_flow` |
| `GetEarningsCalendarWithResponse` | `GET /earnings_calendar` |
| `GetDividendsWithResponse` | `GET /dividends` |
| `GetTimeSeriesRsiWithResponse` | `GET /rsi` |
| `GetTimeSeriesMacdWithResponse` | `GET /macd` |
| `GetApiUsageWithResponse` | `GET /api_usage` |
| `AdvancedWithResponse` | `POST /batch` |

The remaining operations cover other technical indicators, funds, analyst data, holders, corporate actions and market metadata. Look up each generated signature and parameter type with `go doc`, as the skill's "Finding endpoints and types" section shows.

## Responses

| Field or method | Holds |
| --- | --- |
| `JSON200` | Decoded JSON success body, when present |
| `JSON400`, `JSON401`, `JSON403`, `JSON429` | Typed error bodies where the endpoint defines them |
| `Body`, `StatusCode()`, `Status()`, `HTTPResponse` | Raw response and status |

A nil Go error does not mean HTTP success. Check the status and decoded field before dereferencing it. API errors carry `code`, `message` and `status`. Optional fields can be nil.

`GetPrice` returns `JSON200.Price` as a string. Many price and candle fields are strings, while number schemas map to `float64`. The client does not parse string prices into a numeric type.

Keep the default JSON format when using decoded status fields. If you request CSV, consume the raw response body.

## Ranges and pagination

Time series take `Interval`, with optional `StartDate`, `EndDate` and `PageSize` (`outputsize` on the wire). Listing endpoints such as stocks use `page` and `outputsize`. Check the endpoint's generated parameter and response types. Pagination is caller-managed; the client has no iterator.

## Rate limits and access

Endpoint access and API credit limits depend on the subscription and data permissions. The provider spec includes per-endpoint credit metadata. `GetApiUsageWithResponse` exposes usage and plan limits. The generated client has no automatic retries or throttling. Handle HTTP 429 with bounded backoff and a caller deadline.

Batch calls consume credits for their constituent requests and can return per-request errors. Check each batch result.
