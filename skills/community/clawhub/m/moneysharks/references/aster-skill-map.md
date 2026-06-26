# Aster Skill Map

MoneySharks is an orchestration layer over the Aster skills hub.

## Futures v3
- auth: `aster-api-auth-v3`
- account: `aster-api-account-v3`
- trading: `aster-api-trading-v3`
- market data: `aster-api-market-data-v3`
- websocket: `aster-api-websocket-v3`
- errors: `aster-api-errors-v3`

## Futures v1 fallback
- auth: `aster-api-auth-v1`
- account: `aster-api-account-v1`
- trading: `aster-api-trading-v1`
- market data: `aster-api-market-data-v1`
- websocket: `aster-api-websocket-v1`
- errors: `aster-api-errors-v1`

## Use in MoneySharks
- auth skills: credential signing and private request flow
- account skills: balances, positions, transfers, income
- trading skills: create/cancel/query orders
- market data skills: time, tickers, depth, trades, klines, funding
- websocket skills: market/user streams
- errors skills: rate-limits, retries, circuit-breakers
