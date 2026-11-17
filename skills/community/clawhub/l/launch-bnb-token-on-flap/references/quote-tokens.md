# Choosing a Quote Token

By default a launch quotes against native **BNB** (`quoteToken = 0x0000000000000000000000000000000000000000`). Flap also supports launching directly against a range of other stablecoins, crypto assets, and RWA (real-world asset / tokenized stock) tokens as the quote asset.

## Fetch the current quote token list

```
GET https://flap.sh/api/launch/quote-tokens
```

The response lists supported quote tokens **across all chains Flap supports** (BNB, XLAYER, MORPH, Robinhood, MONAD). This skill only launches on **BNB Chain (chainId 56)** — always filter the response down to the entry with `chainId == 56` and ignore every other chain's entries.

```typescript
const res = await fetch("https://flap.sh/api/launch/quote-tokens");
const { chains } = await res.json();

const bnb = chains.find((c: { chainId: number }) => c.chainId === 56);
if (!bnb) throw new Error("BNB chain not found in quote-tokens response");

// bnb.quoteTokens: Array<{
//   symbol: string;
//   name: string;
//   address: string;   // "0x0000...0000" for native BNB
//   decimals: number;
//   logoUrl: string | null;
//   category: "crypto" | "rwa";
//   curve: { r: string; h: string; k: string };
// }>
```

## Response shape (per quote token)

| Field | Notes |
|---|---|
| `symbol` | Ticker of the quote token (e.g. `BNB`, `USDT`, `SPYB`). |
| `name` | Display name. |
| `address` | ERC-20 address, or `0x0000000000000000000000000000000000000000` for native BNB. |
| `decimals` | Token decimals — use when converting a human-entered `quoteAmt` to base units (do **not** assume 18; some entries use 6, e.g. `XAUT`). |
| `category` | `"crypto"` (native/stablecoin/major crypto assets) or `"rwa"` (tokenized real-world assets, e.g. stocks). |
| `curve.r` / `curve.h` / `curve.k` | Bonding-curve pricing parameters for that quote token. Informational — not needed to construct the launch transaction. |

As of this writing, BNB Chain lists 20 quote tokens (`BNB`, `USDT`, `U`, `USD1`, `SPCXB`, `SKHYB`, `SPYB`, `XAUT`, `QQQB`, `NVDAB`, `AAPLB`, `TSLAB`, `MSFTB`, `GOOGLB`, `BTCB`, `SOL`, `HOODB`, `BABAB`, `GMEB`). Always re-fetch the endpoint rather than hardcoding this list — Flap adds new quote tokens over time.

## Using the selected quote token

1. Ask the user which quote token to launch against (default to native `BNB` if they don't care).
2. Resolve its `address` and `decimals` from the fetched list above.
3. Set `quoteToken` in the launch params (Step 8, `construct-tx.md`) to that `address`.
4. Convert the human-entered `quoteAmt` (Step 5) to base units using that token's `decimals` (not a hardcoded 18) — e.g. `parseUnits(quoteAmtHuman, decimals)` instead of `parseEther`.
5. **If `quoteToken` is not native BNB**, the wallet must hold and `approve` a sufficient balance of that ERC-20 token to the launch contract (`Portal` or `VaultPortal`) before sending the launch transaction — `msg.value` only covers the case where `quoteToken` is native BNB. If `quoteToken` is native BNB, `msg.value` must equal `quoteAmt` as before.

## Salt finding with a non-BNB quote token

Vanity salt mining (Step 7, `salt-finding.md`) is unaffected by the choice of quote token — it depends only on the token implementation and Portal address, not on `quoteToken`.
