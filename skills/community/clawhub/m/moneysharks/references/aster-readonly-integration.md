# Aster Read-Only Integration

Use this layer to connect MoneySharks to real Aster market and account data without directly placing live orders.

## Scope
Allowed:
- fetch market data
- fetch account balances
- fetch positions
- fetch open orders
- reconcile state from real exchange responses
- feed real data into scanning, journaling, paper trading, and approval-gated proposals

Not included here:
- direct autonomous order submission
- unattended live trading

## Environment variables
- `ASTER_API_KEY`
- `ASTER_API_SECRET`
- `ASTER_BASE_URL` (optional; defaults to futures API base)

## Expected endpoints
Use the Aster skills/API foundation for:
- public market data endpoints
- private account endpoints
- private positions/orders endpoints

## Implementation guidance
- keep network fetch logic separate from strategy logic
- sanitize logs
- mask secrets
- fail closed when account reads fail
- do not treat stale account data as authoritative
