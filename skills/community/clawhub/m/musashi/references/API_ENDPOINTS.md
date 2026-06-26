# API Endpoints Reference

All APIs are free. No paid keys required.

## GoPlus Security

**Base URL:** `https://api.gopluslabs.io/api/v1`

```
GET /token_security/{chain_id}?contract_addresses={address}
```

Chain IDs: ETH=1, BSC=56, Polygon=137, Arbitrum=42161, Base=8453

Key response fields:
- `is_honeypot`, `is_mintable`, `can_take_back_ownership`
- `is_proxy`, `is_open_source`, `is_blacklisted`
- `buy_tax`, `sell_tax`, `slippage_modifiable`, `transfer_pausable`
- `holder_count`, `lp_holder_count`, `lp_holders[]`
- `owner_address`, `creator_address`

## DexScreener

**Base URL:** `https://api.dexscreener.com`
**Rate Limit:** ~30 req/min

```
GET /latest/dex/tokens/{tokenAddress}          # All pairs for a token
GET /latest/dex/pairs/{chainId}/{pairAddress}   # Specific pair
GET /latest/dex/search?q={query}                # Search by name/symbol
GET /token-boosts/latest/v1                     # Trending/boosted tokens
```

Key response fields per pair:
- `priceUsd`, `priceNative`
- `volume.h24`, `volume.h6`, `volume.h1`, `volume.m5`
- `liquidity.usd`, `liquidity.base`, `liquidity.quote`
- `txns.h24.buys`, `txns.h24.sells`
- `fdv`, `marketCap`, `pairCreatedAt`

## GeckoTerminal

**Base URL:** `https://api.geckoterminal.com/api/v2`
**Rate Limit:** 10 calls/min

```
GET /networks/{network}/tokens/{address}           # Token data
GET /networks/{network}/tokens/{address}/pools      # Token pools
GET /networks/{network}/pools/{address}/ohlcv/{tf}  # OHLCV candles
GET /networks/{network}/new_pools                   # New pools
GET /networks/trending_pools                        # Trending pools
```

Networks: eth, bsc, polygon_pos, arbitrum, base

## DefiLlama

**Base URL:** `https://api.llama.fi`
**Rate Limit:** Generous

```
GET /v2/chains                           # All chains with TVL
GET /v2/historicalChainTvl/{chain}        # Historical TVL
GET /stablecoins                         # All stablecoins
GET /stablecoins/chains                  # Stablecoins per chain
```

Chain names: Ethereum, BSC, Polygon, Arbitrum, Base

## CoinGecko

**Base URL:** `https://api.coingecko.com/api/v3`
**Rate Limit:** 10-30/min (free tier)

```
GET /global                    # Total market cap, BTC dominance
GET /search/trending           # Trending coins
GET /coins/categories          # Categories with market data
```

## Farcaster (via Neynar) -- Optional

**Base URL:** `https://api.neynar.com/v2/farcaster`
**Auth:** Free API key from [neynar.com](https://neynar.com) in header (`api_key: YOUR_KEY`). This is the only API that requires a key, and it is optional -- the agent can browse Farcaster directly via the browser tool instead.

```
GET /cast/search?q={query}&limit=25    # Search casts
```

## Public Chain RPCs

```
Ethereum:  https://eth.llamarpc.com
BSC:       https://bsc-dataseed.binance.org
Polygon:   https://polygon-rpc.com
Arbitrum:  https://arb1.arbitrum.io/rpc
Base:      https://mainnet.base.org
```

## 0G Infrastructure

```
0G Chain RPC:    https://evmrpc-testnet.0g.ai (Galileo Testnet, Chain ID 16602)
0G Storage:      https://indexer-storage-testnet-turbo.0g.ai (Turbo indexer)
0G Compute:      https://compute-marketplace.0g.ai/inference (marketplace)
0G Explorer:     https://chainscan-galileo.0g.ai/
0G Storage Scan: https://storagescan-galileo.0g.ai/
0G Faucet:       https://faucet.0g.ai/
```
