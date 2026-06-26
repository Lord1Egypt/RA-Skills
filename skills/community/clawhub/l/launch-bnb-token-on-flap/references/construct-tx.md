# Construct the EVM Transaction

Assemble the `to`, `value`, and `data` fields for the token launch transaction. Sending the transaction to the network is handled separately in Step 9.

## Contract addresses (BNB mainnet)

| Contract | Address |
|---|---|
| Portal | `0xe2cE6ab80874Fa9Fa2aAE65D277Dd6B8e65C9De0` |
| VaultPortal | `0x90497450f2a706f1951b5bdda52B4E5d16f34C06` |

## A — Standard token (Portal, TOKEN_V2_PERMIT)

Encode the calldata using viem's `encodeFunctionData`:

```typescript
import { encodeFunctionData, parseEther } from "viem";

const to    = "0xe2cE6ab80874Fa9Fa2aAE65D277Dd6B8e65C9De0"; // Portal (BNB mainnet)
const value = parseEther(quoteAmtBnb);                      // msg.value == quoteAmt
const data  = encodeFunctionData({
  abi: PORTAL_ABI,
  functionName: "newTokenV6",
  args: [{
    name,
    symbol,
    meta:               ipfsCid,
    dexThresh:          1,               // FOUR_FIFTHS (80%)
    salt,
    migratorType:       0,               // V3_MIGRATOR
    quoteToken:         "0x0000000000000000000000000000000000000000",
    quoteAmt:           value,
    beneficiary:        "0x0000000000000000000000000000000000000000",
    permitData:         "0x",
    extensionID:        "0x0000000000000000000000000000000000000000000000000000000000000000",
    extensionData:      "0x",
    dexId:              0,               // DEX0 = PancakeSwap
    lpFeeProfile:       0,               // LP_FEE_PROFILE_STANDARD
    buyTaxRate:         0,
    sellTaxRate:        0,
    taxDuration:        0n,
    antiFarmerDuration: 0n,
    mktBps:             0,
    deflationBps:       0,
    dividendBps:        0,
    lpBps:              0,
    minimumShareBalance: 0n,
    dividendToken:      "0x0000000000000000000000000000000000000000",
    commissionReceiver: "0x0000000000000000000000000000000000000000",
    tokenVersion:       2,               // TOKEN_V2_PERMIT
  }],
});
```

## B — Tax token without vault (Portal, TOKEN_TAXED_V3)

Same `to` address. Set `migratorType` to `1` (V2_MIGRATOR) and `tokenVersion` to `6` (TOKEN_TAXED_V3). Fill in the tax parameters as determined in Step 4. 

```typescript
const to    = "0xe2cE6ab80874Fa9Fa2aAE65D277Dd6B8e65C9De0"; // Portal
const value = parseEther(quoteAmtBnb);
const data  = encodeFunctionData({
  abi: PORTAL_ABI,
  functionName: "newTokenV6",
  args: [{
    name, symbol, meta: ipfsCid,
    dexThresh:          1,               // FOUR_FIFTHS (80%)
    salt,
    migratorType:       1,               // must be V2_MIGRATOR for tax tokens
    quoteToken:         "0x0000000000000000000000000000000000000000",
    quoteAmt:           value,
    beneficiary,                         // required for tax token without vault
    permitData:         "0x",
    extensionID:        "0x0000000000000000000000000000000000000000000000000000000000000000",
    extensionData:      "0x",
    dexId:              0,
    lpFeeProfile:       0,
    buyTaxRate,
    sellTaxRate,
    taxDuration,
    antiFarmerDuration,
    mktBps,
    deflationBps,
    dividendBps,
    lpBps,
    minimumShareBalance,
    dividendToken:      "0x0000000000000000000000000000000000000000",
    commissionReceiver: "0x0000000000000000000000000000000000000000",
    tokenVersion:       6,               // TOKEN_TAXED_V3
  }],
});
```

## C — Tax token with vault (VaultPortal, TOKEN_TAXED_V3)

```typescript
const to    = "0x90497450f2a706f1951b5bdda52B4E5d16f34C06"; // VaultPortal
const value = parseEther(quoteAmtBnb);
const data  = encodeFunctionData({
  abi: VAULT_PORTAL_ABI,
  functionName: "newTokenV6WithVault",
  args: [{
    name, symbol, meta: ipfsCid,
    dexThresh:          1,               // FOUR_FIFTHS (80%)
    salt,
    migratorType:       1,
    quoteToken:         "0x0000000000000000000000000000000000000000",
    quoteAmt:           value,
    permitData:         "0x",
    extensionID:        "0x0000000000000000000000000000000000000000000000000000000000000000",
    extensionData:      "0x",
    dexId:              0,
    lpFeeProfile:       0,
    buyTaxRate,
    sellTaxRate,
    taxDuration,
    antiFarmerDuration,
    mktBps,
    deflationBps,
    dividendBps,
    lpBps,
    minimumShareBalance,
    dividendToken:      "0x0000000000000000000000000000000000000000",
    commissionReceiver: "0x0000000000000000000000000000000000000000",
    tokenVersion:       6,               // must be TOKEN_TAXED_V3
    vaultFactory:       vaultFactoryAddress,
    vaultData,                           // encoded bytes from vault-factory.md
  }],
});
```

## Transaction envelope summary

| Field | Value |
|---|---|
| `to` | Portal or VaultPortal address (see above) |
| `value` | `parseEther(quoteAmtBnb)` — use `0n` to skip launch buy |
| `data` | ABI-encoded calldata from `encodeFunctionData` above |
| `chainId` | `56` (BNB mainnet) |

Pass `{ to, value, data }` to whatever signing/sending mechanism is available (Step 9).

## Key constraints

- `migratorType` must be `1` (V2_MIGRATOR) for all tax tokens.
- `mktBps + deflationBps + dividendBps + lpBps` must equal `10000` for tax tokens.
- `tokenVersion` must be `6` (TOKEN_TAXED_V3) when calling `newTokenV6WithVault`.
- `value` must equal `quoteAmt`. Use `0n` to skip the launch buy. 
- `minimumShareBalance` may be provided in unit of ether (e.g. `100`) but must be converted to wei (`parseEther("100")`) before encoding in the transaction data.  
