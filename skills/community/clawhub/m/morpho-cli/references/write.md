# Write Command Response Schemas

All `prepare-*` commands return a `PrepareResult` envelope containing an `operation` (the prepared transaction data) and an optional `simulation` (transaction simulation results). Simulation runs by default; pass `--no-simulate` to skip. `simulate-transactions` returns a standalone `TransactionSimulationResult`.

## prepare-deposit / prepare-withdraw / prepare-supply / prepare-borrow / prepare-repay / prepare-supply-collateral / prepare-withdraw-collateral

```json
{
  "operation": {
    "operation": "deposit",
    "chain": "base",
    "summary": "Deposit 1000 USDC into Steakhouse USDC vault",
    "transactions": [
      {
        "to": "0x...",
        "data": "0x...",
        "value": "0",
        "chainId": "8453",
        "description": "Approve 1000 USDC to vault"
      },
      {
        "to": "0x...",
        "data": "0x...",
        "value": "0",
        "chainId": "8453",
        "description": "Deposit 1000 USDC into vault"
      }
    ],
    "requirements": [
      {
        "type": "approval",
        "token": "0x...",
        "spender": "0x...",
        "amount": "1000000000"
      }
    ],
    "simulationPlan": {
      "version": 1,
      "protocol": "morpho",
      "operation": "deposit",
      "entrypointTxIndex": 0,
      "subject": {
        "kind": "vault_position",
        "chain": "base",
        "userAddress": "0x...",
        "vaultAddress": "0x..."
      },
      "intent": {
        "kind": "deposit_assets",
        "assets": "1000000000",
        "shares": "0"
      },
      "assets": [
        { "address": "0x...", "symbol": "USDC", "decimals": 6, "chain": "base" }
      ],
      "observations": [],
      "logDecoding": {},
      "analysis": { "kind": "vault_analysis" }
    },
    "warnings": [
      {
        "level": "warning",
        "message": "Insufficient vault liquidity for full withdrawal",
        "code": "INSUFFICIENT_LIQUIDITY"
      }
    ],
    "preview": {
      "vault": {
        "sharesReceived": "987654321",
        "positionAssets": "1000000000",
        "positionShares": "987654321"
      }
    }
  },
  "simulation": {
    "chain": "base",
    "allSucceeded": true,
    "totalGasUsed": "245000",
    "executionResults": [ "..." ],
    "analysis": { "..." : "..." },
    "warnings": []
  }
}
```

### Top-level fields

- **`operation`** — the prepared operation (see below)
- **`simulation`** — transaction simulation results (optional, absent when `--no-simulate` is used or simulation fails). See [simulate-transactions](#simulate-transactions) for the full schema.

### operation fields


- **`operation`** — `"deposit"` | `"withdraw"` | `"supply"` | `"borrow"` | `"repay"` | `"supply_collateral"` | `"withdraw_collateral"`
- **`chain`** — chain slug (`"base"` | `"ethereum"`)
- **`summary`** — human-readable description of the operation
- **`transactions`** — ordered array of unsigned transactions to sign and send
  - `to` — contract address
  - `data` — encoded calldata
  - `value` — ETH value (usually `"0"`)
  - `chainId` — `"1"` (Ethereum) or `"8453"` (Base)
  - `description` — what this transaction does
- **`requirements`** — approvals/permits needed (already included in `transactions`)
  - `type` — `"approval"` | `"permit"` | `"permit2"` | `"unsupported"`
  - All types include `token` (address) and `spender` (address)
  - `"approval"` / `"permit"` / `"permit2"`: include `amount` (string), and optionally `deadline` (string)
  - `"unsupported"`: includes `reason` (string) and optionally `notes` (string)
- **`simulationPlan`** — used internally for simulation; pass to `simulate-transactions --analysis-context` for manual re-simulation
- **`warnings`** — array of warnings (may be empty)
  - `level` — `"info"` | `"warning"` | `"error"`
  - `message` — human-readable description
  - `code` — machine-readable code (optional)
- **`preview`** — pre-computed position preview from SDK math (optional)
  - **`vault`** — for vault operations (`deposit`, `withdraw`)
    - `sharesReceived` — vault shares minted or burned (optional)
    - `assetsReceived` — assets received, withdraw only (optional)
    - `positionAssets` — total position value in assets after operation
    - `positionShares` — total share balance after operation
  - **`market`** — for market operations (`supply`, `borrow`, `repay`, `supply_collateral`, `withdraw_collateral`)
    - `supplyAssets` — user supply in assets after operation
    - `borrowAssets` — user borrow in assets after operation
    - `collateral` — user collateral after operation
    - `healthFactor` — health factor after operation (optional)
    - `isHealthy` — whether position is above liquidation threshold (optional)
    - `maxBorrowableAssets` — max additional borrowable in loan token assets (optional)
    - `utilizationBefore` / `utilizationAfter` — market utilization before and after
    - `borrowApyBefore` / `borrowApyAfter` — borrow APY before and after (optional)

## simulate-transactions

```json
{
  "chain": "base",
  "allSucceeded": true,
  "totalGasUsed": "245000",
  "executionResults": [
    {
      "transactionIndex": 0,
      "success": true,
      "gasUsed": "45000",
      "returnData": "0x...",
      "logs": [
        {
          "address": "0x...",
          "contract": "ERC20 (USDC)",
          "eventName": "Approval",
          "description": "Approved 1000 USDC to vault",
          "args": { "owner": "0x...", "spender": "0x...", "value": "1000000000" },
          "formatted": { "owner": "0x...", "spender": "0x...", "value": "1000 USDC" }
        }
      ]
    },
    {
      "transactionIndex": 1,
      "success": true,
      "gasUsed": "200000",
      "returnData": "0x...",
      "logs": [
        {
          "address": "0x...",
          "contract": "ERC4626",
          "eventName": "Deposit",
          "description": "Deposited 1000 USDC into vault",
          "args": { "sender": "0x...", "owner": "0x...", "assets": "1000000000", "shares": "987654321" },
          "formatted": { "sender": "0x...", "owner": "0x...", "assets": "1000 USDC", "shares": "987654321" }
        }
      ]
    }
  ],
  "analysis": {
    "protocol": "morpho",
    "operation": "deposit",
    "vault": {
      "vaultAddress": "0x...",
      "sharesBefore": "0",
      "sharesAfter": "987654321",
      "assetsBefore": "0",
      "assetsAfter": "1000000000",
      "shareDelta": "987654321",
      "assetDelta": "1000000000",
      "projectedApy": "0.0534"
    },
    "warnings": []
  },
  "observations": [
    {
      "key": "usdc_balance",
      "raw": "0x...",
      "decoded": "987654321",
      "type": "uint256"
    }
  ],
  "warnings": []
}
```

### Fields

- **`chain`** — chain slug (`"base"` | `"ethereum"`)
- **`allSucceeded`** — `true` if every transaction executed without revert
- **`totalGasUsed`** — sum of gas across all transactions
- **`executionResults`** — per-transaction results
  - `success` — `false` if reverted
  - `gasUsed` — gas used (`"0"` on failure)
  - `returnData` — hex return data (optional, absent on failure)
  - `revertReason` — present only on failure (e.g., `"ERC4626ExceededMaxWithdraw"`)
  - `logs` — decoded event logs (optional, present when analysis context was passed and transaction emitted decodable events)
    - `address` — emitting contract address
    - `contract` — contract name (e.g., `"ERC20 (USDC)"`, `"Morpho Blue"`)
    - `eventName` — event name (e.g., `"Approval"`, `"Deposit"`, `"Supply"`)
    - `description` — human-readable summary of the event
    - `args` — raw event arguments as key-value pairs
    - `formatted` — human-readable formatted arguments
- **`analysis`** — Morpho-specific pre/post state (optional, present when analysis context was passed and all transactions succeeded)
  - `protocol` — `"morpho"`
  - `operation` — `"deposit"` | `"withdraw"` | `"supply"` | `"borrow"` | `"repay"` | `"supply_collateral"` | `"withdraw_collateral"`
  - **`vault`** — present for vault operations (`deposit`, `withdraw`)
    - `vaultAddress` — vault contract address
    - `sharesBefore` / `sharesAfter` — user's vault shares before and after
    - `assetsBefore` / `assetsAfter` — user's asset value before and after
    - `shareDelta` / `assetDelta` — change in shares and assets
    - `projectedApy` — estimated APY (optional)
    - `marketStates` — per-market snapshots (optional), each with:
      - `marketId`, `totalSupplyAssets`, `totalBorrowAssets`, `totalSupplyShares`, `totalBorrowShares`, `utilization`
  - **`market`** — present for market operations (`supply`, `borrow`, `repay`, `supply_collateral`, `withdraw_collateral`)
    - `marketId` — market unique key
    - `supplyBefore` / `supplyAfter` — user's supply before and after
    - `borrowBefore` / `borrowAfter` — user's borrow before and after
    - `supplyDelta` / `borrowDelta` — change in supply and borrow
    - `utilizationBefore` / `utilizationAfter` — market utilization change (optional)
    - `borrowRateBefore` / `borrowRateAfter` — borrow rate change (optional)
    - `borrowAPYBefore` / `borrowAPYAfter` — borrow APY change (optional)
    - `healthFactor` — post-operation health factor (optional)
    - `liquidationRisk` — risk level string (optional)
  - **`warnings`** — Morpho-specific warnings, each with `level`, `message`, and optional `code`
- **`observations`** — decoded on-chain reads after simulation (optional, only when simulation plan had observations and all transactions succeeded)
  - `key` — observation identifier (e.g., `"usdc_balance"`)
  - `raw` — raw hex return data (optional)
  - `decoded` — decoded value as string (optional)
  - `type` — Solidity type (e.g., `"uint256"`)
  - `error` — error message if decoding failed (optional)
- **`warnings`** — top-level warnings, each with `level` (`"info"` | `"warning"` | `"error"`), `message`, and optional `code`
