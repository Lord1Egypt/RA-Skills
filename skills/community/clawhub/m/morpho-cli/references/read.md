# Read Command Response Schemas

All read commands return JSON to stdout with a `tool` and `timestamp` field.

## query-vaults

**Options:** `--chain` (required), `--asset-symbol`, `--asset-address`, `--sort` (`apy_desc`, `apy_asc`, `tvl_desc`, `tvl_asc`), `--limit` (1–100, default 100), `--skip` (offset), `--fields` (comma-separated: `address`, `name`, `symbol`, `apyPct`, `tvl`, `tvlUsd`, `feePct`)

```json
{
  "vaults": [
    {
      "address": "0x...",
      "name": "Steakhouse USDC",
      "chain": "base",
      "asset": {
        "address": "0x...",
        "symbol": "USDC",
        "decimals": 6,
        "chain": "base"
      },
      "apyPct": "5.34",
      "tvl": "125000000000",
      "tvlUsd": "125000000.00",
      "feePct": "10",
      "rewards": [
        {
          "asset": { "address": "0x...", "symbol": "MORPHO", "decimals": 18, "chain": "base" },
          "supplyAprPct": "1.20"
        }
      ],
      "version": "v1",
      "type": "MorphoVault"
    }
  ],
  "chain": "base",
  "count": 12,
  "pagination": { "total": 50, "limit": 12, "skip": 0 },
  "tool": "morpho_query_vaults",
  "timestamp": "2026-03-17T00:00:00.000Z"
}
```

- `apyPct` — percentage string (e.g., `"5.34"` = 5.34%)
- `feePct` — total fee as percentage (e.g., `"10"` = 10%). For v1 this is the performance fee; for v2 it is `performanceFee + managementFee`
- `tvl` — raw integer string, divide by `10^asset.decimals`
- `rewards` — optional array of reward token incentives with APR percentages
- `version` — `"v1"` or `"v2"`. V1 = MetaMorpho vaults, V2 = newer vault contracts. Always present
- `type` — `"MorphoVault"` or `"FeeWrapper"` (v2 only, absent for v1). FeeWrapper adds a fee layer on top of another vault
- Results include both v1 and v2 vaults merged and sorted together
- `--fields` controls which optional fields are returned; omit to get all
- `--sort` and `--skip` enable server-side sorting and pagination

## get-vault

**Options:** `--chain` (required), `--address` (required)

```json
{
  "vault": {
    "address": "0x...",
    "name": "Steakhouse USDC",
    "chain": "base",
    "asset": {
      "address": "0x...",
      "symbol": "USDC",
      "decimals": 6,
      "chain": "base"
    },
    "curator": "string (optional)",
    "allocator": "string (optional)",
    "apyPct": "5.34",
    "tvl": "125000000000",
    "tvlUsd": "125000000.00",
    "feePct": "10",
    "rewards": [
      {
        "asset": { "address": "0x...", "symbol": "MORPHO", "decimals": 18, "chain": "base" },
        "supplyAprPct": "1.20"
      }
    ],
    "allocations": [
      {
        "market": {
          "uniqueKey": "0x...",
          "loanAsset": { "address": "0x...", "symbol": "USDC" },
          "collateralAsset": { "address": "0x...", "symbol": "WETH" }
        },
        "supplyAssets": "50000000000",
        "supplyAssetsUsd": "50000.00"
      }
    ],
    "version": "v1",
    "type": "MorphoVault"
  },
  "chain": "base",
  "tool": "morpho_get_vault",
  "timestamp": "2026-03-17T00:00:00.000Z"
}
```

- Throws `NOT_FOUND` error if vault address does not exist on either v1 or v2
- The tool automatically tries both v1 and v2 APIs — no version parameter needed
- `version` — `"v1"` or `"v2"`. Always present
- `type` — `"MorphoVault"` or `"FeeWrapper"` (v2 only, absent for v1)
- `allocations` — per-market breakdown of vault's deployed capital (optional, may be absent). For v2 vaults, adapter addresses are used as `uniqueKey` identifiers
- `allocations[].market.loanAsset` / `collateralAsset` — may be null or absent (always absent for v2 adapters)
- `allocations[].supplyAssetsUsd` — optional, may be absent

## query-markets

**Options:** `--chain` (required), `--loan-asset` (required), `--collateral-asset` (required), `--sort-by` (`supplyApy`, `borrowApy`, `netSupplyApy`, `netBorrowApy`, `supplyAssetsUsd`, `borrowAssetsUsd`, `totalLiquidityUsd`; default: `supplyAssetsUsd`), `--sort-direction` (`asc`, `desc`; default: `desc`), `--limit` (1–100, default 100), `--skip` (offset), `--fields` (comma-separated: `supplyApy`, `borrowApy`, `totalSupply`, `totalBorrow`, `totalCollateral`, `totalLiquidity`, `supplyAssetsUsd`, `borrowAssetsUsd`, `collateralAssetsUsd`, `liquidityAssetsUsd`)

```json
{
  "markets": [
    {
      "id": "0x...",
      "chain": "base",
      "loanAsset": {
        "address": "0x...",
        "symbol": "USDC",
        "decimals": 6,
        "chain": "base"
      },
      "collateralAsset": {
        "address": "0x...",
        "symbol": "WETH",
        "decimals": 18,
        "chain": "base"
      },
      "lltv": "0.86",
      "borrowApyPct": "3.12",
      "supplyApyPct": "2.10",
      "totalSupply": "5000000",
      "totalBorrow": "3500000",
      "totalCollateral": "1500",
      "totalLiquidity": "1500000",
      "utilization": "0.7000",
      "supplyAssetsUsd": "5000000.00",
      "borrowAssetsUsd": "3500000.00",
      "collateralAssetsUsd": "4200000.00",
      "liquidityAssetsUsd": "1500000.00",
      "rewards": [
        {
          "asset": { "address": "0x...", "symbol": "MORPHO", "decimals": 18, "chain": "base" },
          "supplyAprPct": "1.20",
          "borrowAprPct": "0.50"
        }
      ]
    }
  ],
  "chain": "base",
  "count": 8,
  "pagination": { "total": 200, "limit": 8, "skip": 0 },
  "tool": "morpho_query_markets",
  "timestamp": "2026-03-17T00:00:00.000Z"
}
```

- `lltv` — denominated decimal string (e.g., `"0.86"` = 86%)
- `borrowApyPct`, `supplyApyPct` — percentage values (e.g., `"3.12"` = 3.12%)
- `totalSupply`, `totalBorrow` — formatted decimal strings in loan asset units
- `totalCollateral` — formatted decimal string in collateral asset units (not loan asset)
- `totalLiquidity` — formatted decimal string in loan asset units (supply - borrow)
- `utilization` — decimal string with 4 decimal places (e.g., `"0.7000"` = 70%). Auto-computed when `totalSupply` and `totalBorrow` are present; not a `--fields` choice
- `collateralAssetsUsd`, `liquidityAssetsUsd` — USD-denominated string values
- `rewards` — optional array of reward token incentives with supply and borrow APR percentages
- `--fields` controls which optional fields are returned; omit to get all
- `--sort-by` and `--sort-direction` enable server-side sorting

## get-market

**Options:** `--chain` (required), `--id` (required)

```json
{
  "market": {
    "id": "0x...",
    "chain": "base",
    "loanAsset": { "address": "0x...", "symbol": "USDC", "decimals": 6, "chain": "base" },
    "collateralAsset": { "address": "0x...", "symbol": "WETH", "decimals": 18, "chain": "base" },
    "lltv": "0.86",
    "borrowApyPct": "3.12",
    "supplyApyPct": "2.10",
    "totalSupply": "5000000",
    "totalBorrow": "3500000",
    "totalCollateral": "1500",
    "totalLiquidity": "1500000",
    "utilization": "0.7000",
    "supplyAssetsUsd": "5000000.00",
    "borrowAssetsUsd": "3500000.00",
    "collateralAssetsUsd": "4200000.00",
    "liquidityAssetsUsd": "1500000.00",
    "rewards": [
      {
        "asset": { "address": "0x...", "symbol": "MORPHO", "decimals": 18, "chain": "base" },
        "supplyAprPct": "1.20",
        "borrowAprPct": "0.50"
      }
    ]
  },
  "chain": "base",
  "tool": "morpho_get_market",
  "timestamp": "2026-03-17T00:00:00.000Z"
}
```

- Same fields as `query-markets` items — all total/USD fields are formatted decimal strings via `formatUnits`
- Throws `NOT_FOUND` error if market ID does not exist

## get-positions

**Options:** `--chain` (required), `--user-address` (required), `--vault-address` (optional), `--market-id` (optional)

```json
{
  "positions": [
    {
      "userAddress": "0x...",
      "chain": "base",
      "vault": {
        "address": "0x...",
        "name": "Steakhouse USDC",
        "chain": "base",
        "asset": { "address": "0x...", "symbol": "USDC", "decimals": 6, "chain": "base" }
      },
      "suppliedAmount": { "address": "0x...", "symbol": "USDC", "decimals": 6, "chain": "base", "value": "10000" },
      "borrowedAmount": null,
      "collateralAmount": null,
      "shares": "9876543210"
    },
    {
      "userAddress": "0x...",
      "chain": "base",
      "market": {
        "id": "0x...",
        "chain": "base",
        "loanAsset": { "address": "0x...", "symbol": "USDC", "decimals": 6, "chain": "base" },
        "collateralAsset": { "address": "0x...", "symbol": "WETH", "decimals": 18, "chain": "base" },
        "lltv": "0.86"
      },
      "suppliedAmount": { "address": "0x...", "symbol": "USDC", "decimals": 6, "chain": "base", "value": "0" },
      "borrowedAmount": { "address": "0x...", "symbol": "USDC", "decimals": 6, "chain": "base", "value": "500" },
      "collateralAmount": { "address": "0x...", "symbol": "WETH", "decimals": 18, "chain": "base", "value": "1" }
    }
  ],
  "chain": "base",
  "count": 2,
  "userAddress": "0x...",
  "tool": "morpho_get_positions",
  "timestamp": "2026-03-17T00:00:00.000Z"
}
```

- Vault positions have `vault` field, market positions have `market` field
- `suppliedAmount.value`, `borrowedAmount.value`, `collateralAmount.value` — formatted decimal strings (human-readable, e.g., `"500"` = 500 USDC, `"1"` = 1 WETH)
- `shares` — vault share count (raw integer string)

## get-position

**Options:** `--chain` (required), `--user-address` (required), `--vault-address` (optional), `--market-id` (optional)

```json
{
  "position": { ... },
  "chain": "base",
  "tool": "morpho_get_position",
  "timestamp": "2026-03-17T00:00:00.000Z"
}
```

- Same position shape as `get-positions` items
- Throws `NOT_FOUND` error if no position exists

## get-token-balance

**Options:** `--chain` (required), `--user-address` (required), `--token-address` (required)

```json
{
  "chain": "base",
  "userAddress": "0x...",
  "asset": {
    "address": "0x...",
    "symbol": "USDC",
    "decimals": 6,
    "chain": "base"
  },
  "balance": "1000000000",
  "erc20Allowances": {
    "morpho": "0",
    "bundler": "0",
    "permit2": "115792089237316195423570985008687907853269984665640564039457584007913129639935"
  },
  "permit2BundlerAllowance": {
    "amount": "0",
    "expiration": "0",
    "nonce": "0"
  },
  "erc2612Nonce": 0,
  "canTransfer": true,
  "tool": "morpho_get_token_balance",
  "timestamp": "2026-03-17T00:00:00.000Z"
}
```

- `balance` — raw integer string, divide by `10^asset.decimals`
- `erc20Allowances` — raw integer strings for each spender (Morpho core, Bundler, Permit2)
- `permit2BundlerAllowance` — Permit2 sub-allowance for the Bundler contract
  - `amount` — raw integer allowance
  - `expiration` — Unix timestamp string
  - `nonce` — permit nonce string
- `erc2612Nonce` — current ERC-2612 permit nonce (integer)
- `canTransfer` — whether the user can transfer this token (not paused/blocklisted)

## health-check

```json
{
  "status": "healthy",
  "timestamp": "2026-03-17T00:00:00.000Z",
  "version": "0.1.0",
  "environment": "development",
  "tool": "morpho_health_check",
  "services": {
    "api": "operational",
    "chains": {
      "base": "operational",
      "ethereum": "operational"
    }
  }
}
```

- `status` — `"healthy"` | `"degraded"` | `"unhealthy"`
- `environment` — runtime environment (e.g., `"development"`, `"production"`)
- `services.api` / `services.chains.*` — `"operational"` | `"degraded"` | `"down"` | `"error"`

## get-supported-chains

```json
{
  "chains": [
    {
      "slug": "base",
      "name": "Base",
      "chainId": "8453",
      "explorerUrl": "https://basescan.org",
      "isTestnet": false
    }
  ],
  "tool": "morpho_get_supported_chains",
  "timestamp": "2026-03-17T00:00:00.000Z"
}
```
