# ROB Management

Open, cancel, adjust, claim, and redeem Limited Redemption Protocol positions on Indigo Protocol.

All write operations return an unsigned transaction (CBOR hex) for client-side signing.

## Tools

### open_rob

Open a new ROB position with ADA and a max price limit.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `address` | `string` | Yes | User Cardano bech32 address |
| `asset` | `iUSD` \| `iBTC` \| `iETH` \| `iSOL` | Yes | Target iAsset |
| `lovelacesAmount` | `string` | Yes | ADA amount in lovelace to deposit |
| `maxPrice` | `string` | Yes | Max price as an on-chain integer string |

**Example prompt:** "Open an ROB position for iUSD with 500 ADA at max price 1.05"

### cancel_rob

Cancel an existing ROB position and reclaim deposited ADA.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `address` | `string` | Yes | User Cardano bech32 address |
| `robTxHash` | `string` | Yes | Transaction hash of the ROB UTxO |
| `robOutputIndex` | `number` | Yes | Output index of the ROB UTxO |

**Example prompt:** "Cancel my ROB position"

### adjust_rob

Adjust ADA amount in an ROB position (positive to increase, negative to decrease). Optionally update the max price.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `address` | `string` | Yes | User Cardano bech32 address |
| `robTxHash` | `string` | Yes | Transaction hash of the ROB UTxO |
| `robOutputIndex` | `number` | Yes | Output index of the ROB UTxO |
| `lovelacesAdjustAmount` | `string` | Yes | Lovelace adjustment (positive to add, negative to remove) |
| `newMaxPrice` | `string` | No | New max price as on-chain integer string |

**Example prompt:** "Add 200 ADA to my ROB position and raise max price to 1.10"

### claim_rob

Claim received iAssets from a filled or partially filled ROB position.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `address` | `string` | Yes | User Cardano bech32 address |
| `robTxHash` | `string` | Yes | Transaction hash of the ROB UTxO |
| `robOutputIndex` | `number` | Yes | Output index of the ROB UTxO |

**Example prompt:** "Claim iAssets from my ROB position"

### redeem_rob

Redeem iAssets against one or more ROB positions.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `address` | `string` | Yes | User Cardano bech32 address |
| `redemptionRobs` | `array` | Yes | Array of ROB positions and amounts to redeem against |
| `priceOracleTxHash` | `string` | Yes | Transaction hash of the price oracle UTxO |
| `priceOracleOutputIndex` | `number` | Yes | Output index of the price oracle UTxO |
| `iassetTxHash` | `string` | Yes | Transaction hash of the iAsset UTxO |
| `iassetOutputIndex` | `number` | Yes | Output index of the iAsset UTxO |

Each entry in `redemptionRobs` contains:

| Field | Type | Description |
|-------|------|-------------|
| `txHash` | `string` | Transaction hash of the ROB UTxO |
| `outputIndex` | `number` | Output index of the ROB UTxO |
| `iAssetAmount` | `string` | Amount of iAssets to redeem against this ROB |

**Example prompt:** "Redeem 100 iUSD against the cheapest ROB positions"

## Typical Workflows

1. **Provide liquidity** — `open_rob` to place a new order, then `claim_rob` once filled.
2. **Manage position** — `adjust_rob` to increase/decrease ADA or update price limit; `cancel_rob` to exit entirely.
3. **Redeem iAssets** — Use `get_order_book` (Order Book sub-skill) to find positions, then `redeem_rob` to execute.
