# CDP Mint & Burn

Mint synthetic assets (iAssets) against CDPs and burn them to reduce debt.

## Tools

### mint_cdp

Mint iAssets (iUSD, iBTC, iETH, iSOL) against CDP collateral. Increases debt ratio.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `address` | `string` | Yes | User Cardano bech32 address |
| `cdpTxHash` | `string` | Yes | Transaction hash of the CDP UTxO |
| `cdpOutputIndex` | `number` | Yes | Output index of the CDP UTxO |
| `amount` | `string` | Yes | Amount of iAssets to mint (in smallest unit) |

### burn_cdp

Burn iAssets to reduce or eliminate CDP debt. Improves health ratio.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `address` | `string` | Yes | User Cardano bech32 address |
| `cdpTxHash` | `string` | Yes | Transaction hash of the CDP UTxO |
| `cdpOutputIndex` | `number` | Yes | Output index of the CDP UTxO |
| `amount` | `string` | Yes | Amount of iAssets to burn (in smallest unit) |

## Examples

### Mint iUSD against an existing CDP

Mint additional iUSD from a CDP that has excess collateral headroom.

**Prompt:** "Mint 500 iUSD from my CDP"

**Workflow:**
1. Call `get_cdps_by_owner({ owners: ["addr1qx...abc"] })` to find the CDP
2. Call `analyze_cdp_health` to verify the CDP can safely support more debt
3. Call `mint_cdp({ address: "addr1qx...abc", cdpTxHash: "abc123...def", cdpOutputIndex: 0, amount: "500000000" })`
4. Returns unsigned transaction CBOR for signing

**Sample response:**
```
Mint ready.
Amount: 500 iUSD
New debt: 1,500 iUSD
New collateral ratio: 200%
Transaction ready for signing.
```

### Burn iAssets to improve CDP health

Reduce CDP debt by burning iAssets, improving the collateral ratio.

**Prompt:** "Burn 200 iUSD to improve my CDP health"

**Workflow:**
1. Call `get_cdps_by_owner({ owners: ["addr1qx...abc"] })` to find the CDP
2. Call `burn_cdp({ address: "addr1qx...abc", cdpTxHash: "abc123...def", cdpOutputIndex: 0, amount: "200000000" })`
3. Returns unsigned transaction — iUSD is burned from user wallet, debt reduced

**Sample response:**
```
Burn ready.
Burning: 200 iUSD
Remaining debt: 1,300 iUSD
New collateral ratio: 231%
```

### Fully repay CDP debt

Burn all remaining iAsset debt to fully repay a CDP before closing it.

**Prompt:** "Repay all my iUSD debt"

**Workflow:**
1. Call `get_cdps_by_owner({ owners: ["addr1qx...abc"] })` to find CDP and check debt amount
2. Call `burn_cdp` with the full debt amount
3. After signing, the CDP has zero debt and can be closed with `close_cdp`

**Sample response:**
```
Full repayment ready.
Burning: 1,500 iUSD (entire debt)
Remaining debt: 0 iUSD
CDP is now debt-free and can be closed.
```

## Example Prompts

- "Mint 1000 iUSD from my CDP"
- "How much more iBTC can I mint without risking liquidation?"
- "Burn 100 iUSD to reduce my CDP debt"
- "Repay all debt on my CDP"
