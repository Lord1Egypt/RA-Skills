# Construct the EVM Transaction

Assemble the `to`, `value`, and `data` fields for the token launch transaction. Sending the transaction to the network is handled separately in Step 9.

## Contract addresses (BNB mainnet)

| Contract | Address |
|---|---|
| Portal | `0xe2cE6ab80874Fa9Fa2aAE65D277Dd6B8e65C9De0` |
| VaultPortal | `0x90497450f2a706f1951b5bdda52B4E5d16f34C06` |

All launches from this skill use `tokenVersion = TOKEN_TAXED_V3` (`6`). Standard (non-tax)
tokens are out of scope for this skill.

## Resolving `quoteToken`, `quoteAmt`, and `value`

`quoteToken` and its `decimals` come from `references/quote-tokens.md` (Step 1). Convert the
human-entered launch-buy amount using that token's own `decimals` — do **not** assume 18:

```typescript
import { parseUnits } from "viem";

// quoteToken: resolved address (0x000...000 for native BNB, or an ERC-20 address)
// quoteDecimals: resolved decimals for quoteToken
const quoteAmt = parseUnits(quoteAmtHuman, quoteDecimals);

// msg.value only applies when quoting in native BNB; otherwise it is 0 and the
// ERC-20 quoteToken must already be approved to the target contract (Portal/VaultPortal)
// for at least `quoteAmt`.
const isNativeQuote = quoteToken === "0x0000000000000000000000000000000000000000";
const value = isNativeQuote ? quoteAmt : 0n;
```

## A — Tax token without vault (Portal, TOKEN_TAXED_V3)

Set `migratorType` to `1` (V2_MIGRATOR) and `tokenVersion` to `6` (TOKEN_TAXED_V3). Fill in the tax parameters as determined in Step 4. 

```typescript
import { encodeFunctionData } from "viem";

const to    = "0xe2cE6ab80874Fa9Fa2aAE65D277Dd6B8e65C9De0"; // Portal
const data  = encodeFunctionData({
  abi: PORTAL_ABI,
  functionName: "newTokenV6",
  args: [{
    name, symbol, meta: ipfsCid,
    dexThresh:          1,               // FOUR_FIFTHS (80%)
    salt,
    migratorType:       1,               // must be V2_MIGRATOR for tax tokens
    quoteToken,                          // resolved in Step 1 (see quote-tokens.md)
    quoteAmt,                            // base units, using quoteToken's own decimals
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

## B — Tax token with vault (VaultPortal, TOKEN_TAXED_V3)

```typescript
const to    = "0x90497450f2a706f1951b5bdda52B4E5d16f34C06"; // VaultPortal
const data  = encodeFunctionData({
  abi: VAULT_PORTAL_ABI,
  functionName: "newTokenV6WithVault",
  args: [{
    name, symbol, meta: ipfsCid,
    dexThresh:          1,               // FOUR_FIFTHS (80%)
    salt,
    migratorType:       1,
    quoteToken,                          // resolved in Step 1 (see quote-tokens.md)
    quoteAmt,                            // base units, using quoteToken's own decimals
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
| `value` | `quoteAmt` if `quoteToken` is native BNB, otherwise `0n` — use `0n` to skip launch buy |
| `data` | ABI-encoded calldata from `encodeFunctionData` above |
| `chainId` | `56` (BNB mainnet) |

Pass `{ to, value, data }` to whatever signing/sending mechanism is available (Step 9).

## Key constraints

- `migratorType` must be `1` (V2_MIGRATOR) for all tax tokens.
- `mktBps + deflationBps + dividendBps + lpBps` must equal `10000` for tax tokens.
- `tokenVersion` must be `6` (TOKEN_TAXED_V3) when calling `newTokenV6WithVault`.
- `value` must equal `quoteAmt` when `quoteToken` is native BNB, and `0n` otherwise. Use
  `quoteAmt = 0n` to skip the launch buy entirely.
- When `quoteToken` is an ERC-20 (non-native) token, it must be approved to the `to` contract
  (Portal or VaultPortal) for at least `quoteAmt` before sending this transaction.
- `minimumShareBalance` may be provided in unit of ether (e.g. `100`) but must be converted to wei (`parseEther("100")`) before encoding in the transaction data.  
