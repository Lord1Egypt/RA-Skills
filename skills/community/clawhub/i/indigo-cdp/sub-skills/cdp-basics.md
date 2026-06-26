# CDP Basics

Open, manage, and close Collateralized Debt Positions on Indigo.

## Tools

### open_cdp

Open a new CDP with collateral.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `address` | `string` | Yes | User Cardano bech32 address |
| `asset` | `"iUSD" \| "iBTC" \| "iETH" \| "iSOL"` | Yes | iAsset to mint |
| `collateralAmount` | `string` | Yes | ADA collateral in lovelace |

### deposit_cdp

Add collateral to an existing CDP to improve health ratio.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `address` | `string` | Yes | User Cardano bech32 address |
| `cdpTxHash` | `string` | Yes | Transaction hash of the CDP UTxO |
| `cdpOutputIndex` | `number` | Yes | Output index of the CDP UTxO |
| `collateralAmount` | `string` | Yes | Additional ADA in lovelace |

### withdraw_cdp

Remove excess collateral from a CDP.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `address` | `string` | Yes | User Cardano bech32 address |
| `cdpTxHash` | `string` | Yes | Transaction hash of the CDP UTxO |
| `cdpOutputIndex` | `number` | Yes | Output index of the CDP UTxO |
| `collateralAmount` | `string` | Yes | ADA to withdraw in lovelace |

### close_cdp

Close a CDP entirely, burning all debt and reclaiming collateral.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `address` | `string` | Yes | User Cardano bech32 address |
| `cdpTxHash` | `string` | Yes | Transaction hash of the CDP UTxO |
| `cdpOutputIndex` | `number` | Yes | Output index of the CDP UTxO |

## Examples

### Open a new iUSD CDP

Create a CDP by depositing ADA collateral to mint iUSD.

**Prompt:** "Open a CDP with 5000 ADA to mint iUSD"

**Workflow:**
1. Call `open_cdp({ address: "addr1qx...abc", asset: "iUSD", collateralAmount: "5000000000" })`
2. Returns unsigned transaction CBOR for signing
3. User signs and submits to create the CDP on-chain

**Sample response:**
```
CDP opened successfully.
Collateral: 5,000 ADA
Asset: iUSD
Transaction ready for signing.
```

### Deposit additional collateral

Add more ADA to an existing CDP to improve its health ratio and reduce liquidation risk.

**Prompt:** "Add 1000 ADA to my iUSD CDP"

**Workflow:**
1. Call `get_cdps_by_owner({ owners: ["addr1qx...abc"] })` to find the CDP
2. Call `deposit_cdp({ address: "addr1qx...abc", cdpTxHash: "abc123...def", cdpOutputIndex: 0, collateralAmount: "1000000000" })`
3. Returns unsigned transaction CBOR for signing

**Sample response:**
```
Deposit ready.
CDP: abc123...def
Additional collateral: 1,000 ADA
New total collateral: 6,000 ADA
```

### Close a CDP and reclaim collateral

Close a fully repaid CDP to get back all deposited ADA.

**Prompt:** "Close my iUSD CDP and return my collateral"

**Workflow:**
1. Call `get_cdps_by_owner({ owners: ["addr1qx...abc"] })` to find the CDP
2. Verify the CDP debt is zero or user has enough iAssets to burn
3. Call `close_cdp({ address: "addr1qx...abc", cdpTxHash: "abc123...def", cdpOutputIndex: 0 })`
4. Returns unsigned transaction — burns remaining debt and returns all collateral

**Sample response:**
```
CDP closed.
Returned: 5,000 ADA
Burned debt: 0 iUSD
```

## Example Prompts

- "Open a new CDP with 10,000 ADA for iBTC"
- "Deposit more collateral into my CDP"
- "Withdraw 500 ADA from my iUSD CDP"
- "Close my CDP and get my ADA back"
