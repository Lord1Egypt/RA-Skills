# Polymarket CLI command map

Use this file when you need a broader command inventory than the main skill file.

## Read-only commands

These are generally safe to run without extra confirmation.

### Core discovery

```bash
polymarket status
polymarket --help
polymarket --version
polymarket markets list --limit 10
polymarket markets get MARKET_ID_OR_SLUG
polymarket markets search "QUERY" --limit 5
polymarket markets tags MARKET_ID
polymarket events list --limit 10
polymarket events get EVENT_ID
polymarket events tags EVENT_ID
polymarket tags list
polymarket tags get TAG
polymarket tags related TAG
polymarket tags related-tags TAG
polymarket series list --limit 10
polymarket series get SERIES_ID
polymarket comments list --entity-type event --entity-id EVENT_ID
polymarket comments get COMMENT_ID
polymarket comments by-user 0xWALLET
polymarket profiles get 0xWALLET
polymarket sports list
polymarket sports market-types
polymarket sports teams --league NFL --limit 32
```

### CLOB read-only

```bash
polymarket clob ok
polymarket clob price TOKEN_ID --side buy
polymarket clob midpoint TOKEN_ID
polymarket clob spread TOKEN_ID
polymarket clob batch-prices "TOKEN1,TOKEN2" --side buy
polymarket clob midpoints "TOKEN1,TOKEN2"
polymarket clob spreads "TOKEN1,TOKEN2"
polymarket clob book TOKEN_ID
polymarket clob books "TOKEN1,TOKEN2"
polymarket clob last-trade TOKEN_ID
polymarket clob market 0xCONDITION_ID
polymarket clob markets
polymarket clob price-history TOKEN_ID --interval 1d --fidelity 30
polymarket clob tick-size TOKEN_ID
polymarket clob fee-rate TOKEN_ID
polymarket clob neg-risk TOKEN_ID
polymarket clob time
polymarket clob geoblock
```

### Public wallet and market data

```bash
polymarket data positions 0xWALLET
polymarket data closed-positions 0xWALLET
polymarket data value 0xWALLET
polymarket data traded 0xWALLET
polymarket data trades 0xWALLET --limit 50
polymarket data activity 0xWALLET
polymarket data holders 0xCONDITION_ID
polymarket data open-interest 0xCONDITION_ID
polymarket data volume EVENT_ID
polymarket data leaderboard --period month --order-by pnl --limit 10
polymarket data builder-leaderboard --period week
polymarket data builder-volume --period month
```

### Read-only but wallet-aware

These do not place trades, but may read authenticated account state if a wallet is configured.
Do not run wallet-management commands like `wallet show` or `wallet address`; the user should run those directly.

```bash
polymarket approve check
polymarket approve check 0xADDRESS
polymarket clob orders
polymarket clob orders --market 0xCONDITION_ID
polymarket clob order ORDER_ID
polymarket clob trades
polymarket clob balance --asset-type collateral
polymarket clob balance --asset-type conditional --token TOKEN_ID
polymarket clob rewards --date 2024-06-15
polymarket clob earnings --date 2024-06-15
polymarket clob earnings-markets --date 2024-06-15
polymarket clob reward-percentages
polymarket clob current-rewards
polymarket clob market-reward 0xCONDITION_ID
polymarket clob order-scoring ORDER_ID
polymarket clob orders-scoring "ORDER1,ORDER2"
polymarket clob api-keys
polymarket clob account-status
polymarket clob notifications
```

## Sensitive commands

Confirm with the user before running any of these.

### Wallet/config writers

These are user-only. Do not run them as the agent.

```bash
polymarket setup
polymarket wallet create
polymarket wallet create --force
polymarket wallet import 0xPRIVATE_KEY
polymarket wallet address
polymarket wallet show
polymarket wallet reset
polymarket wallet reset --force
```

### Trading and cancellations

```bash
polymarket clob create-order --token TOKEN_ID --side buy --price 0.50 --size 10
polymarket clob market-order --token TOKEN_ID --side buy --amount 5
polymarket clob post-orders --tokens "TOKEN1,TOKEN2" --side buy --prices "0.40,0.60" --sizes "10,10"
polymarket clob cancel ORDER_ID
polymarket clob cancel-orders "ORDER1,ORDER2"
polymarket clob cancel-market --market 0xCONDITION_ID
polymarket clob cancel-all
polymarket clob update-balance --asset-type collateral
polymarket clob create-api-key
polymarket clob delete-api-key
polymarket clob delete-notifications "NOTIF1,NOTIF2"
```

### On-chain actions

```bash
polymarket approve set
polymarket ctf split --condition 0xCONDITION_ID --amount 10
polymarket ctf merge --condition 0xCONDITION_ID --amount 10
polymarket ctf redeem --condition 0xCONDITION_ID
polymarket ctf redeem-neg-risk --condition 0xCONDITION_ID --amounts "10,5"
polymarket bridge deposit 0xWALLET
polymarket bridge status 0xDEPOSIT_ADDRESS
```

## Output format

Prefer JSON for automation:

```bash
polymarket -o json markets list --limit 5
polymarket -o json markets search "bitcoin" --limit 5
polymarket -o json clob book TOKEN_ID
polymarket -o json data positions 0xWALLET
```

## Auth and config notes

The CLI checks private key sources in this order:
1. `--private-key`
2. `POLYMARKET_PRIVATE_KEY`
3. `~/.config/polymarket/config.json`

Config example:

```json
{
  "private_key": "0x...",
  "chain_id": 137,
  "signature_type": "proxy"
}
```

Signature types:
- `proxy` (default)
- `eoa`
- `gnosis-safe`

## Install

```bash
brew tap Polymarket/polymarket-cli https://github.com/Polymarket/polymarket-cli
brew install polymarket
```
