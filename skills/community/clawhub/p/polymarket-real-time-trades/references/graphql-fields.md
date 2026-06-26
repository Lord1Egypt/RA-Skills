# Bitquery EVM.PredictionTrades — Polymarket GraphQL Field Reference

Full reference for the fields available in the `EVM.PredictionTrades` **subscription** on the Bitquery streaming API, scoped to Polymarket on Polygon (matic). For real-time streaming, use a `subscription` with the same structure.

**Official documentation:** [Polymarket API - Get Prices, Trades & Market Data](https://docs.bitquery.io/docs/examples/polymarket-api/)

## Subscription Structure

```graphql
subscription MyQuery {
  EVM(network: matic) {
    PredictionTrades(where: { TransactionStatus: { Success: true } }) {
      Block { ... }
      Call { ... }
      Log { ... }
      Trade { ... }
      Transaction { ... }
    }
  }
}
```

---

## Filters (`where`)

| Filter | Description | Example |
|--------|-------------|---------|
| `TransactionStatus.Success` | Only successful transactions | `true` |
| (EVM scope) `network` | Blockchain network | `matic` (Polygon) |

**Polymarket filter (the active subscription filter):**
```graphql
EVM(network: matic) {
  PredictionTrades(where: { TransactionStatus: { Success: true } }) {
    # fields
  }
}
```

---

## Output Fields

### `Block`

| Field | Type | Description |
|-------|------|-------------|
| `Time` | String | ISO timestamp of the block |

### `Call`

| Field | Type | Description |
|-------|------|-------------|
| `Signature.Name` | String | Contract method called (e.g. `matchOrders`) |

### `Log`

| Field | Type | Description |
|-------|------|-------------|
| `Signature.Name` | String | Event name (e.g. `OrderFilled`) |
| `SmartContract` | String | Contract address that emitted the event |

### `Trade`

#### `Trade.OutcomeTrade`

| Field | Type | Description |
|-------|------|-------------|
| `Buyer` | String | Buyer address (taker) |
| `Seller` | String | Seller address (maker) |
| `Amount` | String | Outcome token amount (raw) |
| `CollateralAmount` | String/Float | Collateral token amount |
| `CollateralAmountInUSD` | Float | Notional in USD |
| `OrderId` | String | Order identifier |
| `Price` | Float | Price in collateral (0–1 for binary) |
| `PriceInUSD` | Float | Price in USD |
| `IsOutcomeBuy` | Boolean | True = buyer bought the outcome (Yes/Up) |

#### `Trade.Prediction.CollateralToken`

| Field | Type | Description |
|-------|------|-------------|
| `Name` | String | e.g. "USD Coin (PoS)" |
| `Symbol` | String | e.g. "USDC" |
| `SmartContract` | String | Token contract address |
| `AssetId` | String | Bitquery asset ID |

#### `Trade.Prediction`

| Field | Type | Description |
|-------|------|-------------|
| `ConditionId` | String | Condition ID (e.g. `0x7daf...`) |
| `OutcomeToken` | Object | Name, Symbol, SmartContract, AssetId |
| `Marketplace` | Object | Protocol metadata |
| `Question` | Object | Market question and metadata |
| `Outcome` | Object | Id, Index, Label (e.g. "Up", "Down") |

#### `Trade.Prediction.Marketplace`

| Field | Type | Description |
|-------|------|-------------|
| `SmartContract` | String | CTF/market contract address |
| `ProtocolVersion` | String | e.g. "1" |
| `ProtocolName` | String | e.g. "polymarket" |
| `ProtocolFamily` | String | e.g. "Gnosis_CTF" |

#### `Trade.Prediction.Question`

| Field | Type | Description |
|-------|------|-------------|
| `Title` | String | Market question title |
| `ResolutionSource` | String | URL or source for resolution (e.g. Chainlink) |
| `Image` | String | Image URL for the market |
| `MarketId` | String | Polymarket market ID |
| `Id` | String | Question ID (e.g. hex) |
| `CreatedAt` | String | ISO timestamp |

#### `Trade.Prediction.Outcome`

| Field | Type | Description |
|-------|------|-------------|
| `Id` | String | Outcome token ID |
| `Index` | Int | Outcome index (0, 1, …) |
| `Label` | String | Human label (e.g. "Up", "Down", "Yes", "No") |

### `Transaction`

| Field | Type | Description |
|-------|------|-------------|
| `From` | String | Transaction sender |
| `Hash` | String | Transaction hash |

---

## Example: Full subscription (all fields)

```graphql
subscription MyQuery {
  EVM(network: matic) {
    PredictionTrades(where: { TransactionStatus: { Success: true } }) {
      Block {
        Time
      }
      Call {
        Signature {
          Name
        }
      }
      Log {
        Signature {
          Name
        }
        SmartContract
      }
      Trade {
        OutcomeTrade {
          Buyer
          Seller
          Amount
          CollateralAmount
          CollateralAmountInUSD
          OrderId
          Price
          PriceInUSD
          IsOutcomeBuy
        }
        Prediction {
          CollateralToken {
            Name
            Symbol
            SmartContract
            AssetId
          }
          ConditionId
          OutcomeToken {
            Name
            Symbol
            SmartContract
            AssetId
          }
          Marketplace {
            SmartContract
            ProtocolVersion
            ProtocolName
            ProtocolFamily
          }
          Question {
            Title
            ResolutionSource
            Image
            MarketId
            Id
            CreatedAt
          }
          Outcome {
            Id
            Index
            Label
          }
        }
      }
      Transaction {
        From
        Hash
      }
    }
  }
}
```

---

## Notes on Polymarket prediction trades

- Trades are on **Polygon (matic)** only in this subscription.
- Collateral is typically USDC; `CollateralAmountInUSD` and `PriceInUSD` are provided for trader use.
- `IsOutcomeBuy: true` means the buyer bought the outcome (e.g. "Yes" or "Up"); false means they sold.
- Use `Question.MarketId` or `Question.Id` to filter or aggregate by market in application code.
