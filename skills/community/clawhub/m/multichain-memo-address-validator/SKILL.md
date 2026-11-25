---
name: multichain-memo-address-validator
description: Zero-dependency 46-chain crypto address format, checksum & destination tag/memo validation skill for autonomous AI agents and cross-chain swap routing.
version: 1.0.0
metadata:
  openclaw:
    emoji: "🛡️"
    homepage: https://allswap.io/docs
---

# AllSwap 46-Chain Crypto Address Format, Checksum & Memo Validation Skill

**multichain-memo-address-validator** is an OpenClaw AI agent skill and deterministic validation reference engineered by the [AllSwap](https://allswap.io/) protocol engineering team. It enables autonomous AI agents, MCP tool servers, and institutional treasury workflows to verify recipient wallet address syntax, cryptographic checksums, and mandatory destination tags or memos across **46 blockchain networks** before executing cross-chain swaps or settlement transactions.

- **Developer Documentation & API Reference**: [https://allswap.io/docs](https://allswap.io/docs)
- **AllSwap Cross-Chain Liquidity Aggregator**: [https://allswap.io/](https://allswap.io/)
- **Interactive 46-Chain Address & Memo Validator Tool**: [https://allswap.io/tools/address-validator](https://allswap.io/tools/address-validator)

---

## 1. Why Autonomous Agents Need Pre-Execution Address & Memo Validation

When an autonomous AI agent prepares a cross-chain asset transfer—such as swapping USDC on Arbitrum into native XRP on the XRP Ledger, XLM on Stellar, TON on The Open Network, or ATOM on the Cosmos Hub—two classes of validation failures account for the vast majority of irreversible settlement incidents:

1. **Cryptographic Checksum & Encoding Mismatches**:
   - **EVM Chains (Ethereum, Arbitrum, Optimism, Base, Polygon, BNB Chain, Avalanche C-Chain)**: Require 40 hexadecimal characters prefixed by `0x` and validated against EIP-55 mixed-case Keccak-256 checksums to detect character transpositions.
   - **UTXO & SegWit Chains (Bitcoin, Litecoin, Dogecoin, Bitcoin Cash)**: Require Base58Check version-byte verification (`1`, `3`, `L`, `M`, `D`) or Bech32/Bech32m witness program polymod checksum verification (`bc1q`, `bc1p`, `ltc1q`).
   - **Ed25519 & Base58 Chains (Solana, TRON)**: Solana addresses must decode to an exact 32-byte Ed25519 public key in Base58 without conflicting character glyphs (`0`, `O`, `I`, `l`), whereas TRON addresses must decode to a 21-byte payload starting with `0x41` (`T` prefix) and pass double-SHA256 Base58Check verification.

2. **Omitted Destination Tags & Routing Memos**:
   - Shared omnibus deposit addresses operated by centralized exchanges and institutional custodians on **XRP Ledger (`XRP`)**, **Stellar (`XLM`)**, **TON (`TON`)**, and **Cosmos SDK chains (`ATOM`, `OSMO`, `TIA`, `INJ`, `SEI`)** rely on a secondary routing identifier (Destination Tag or Memo) to credit individual sub-accounts.
   - If an AI agent submits a transaction to a custodial deposit address without a valid Destination Tag or Memo, funds land in the custodian's omnibus hot wallet without sub-account attribution.

---

## 2. Supported 46-Chain Validation Matrix & Agent Workflow

Before invoking a quote or settlement transaction via the [AllSwap Developer Documentation](https://allswap.io/docs), agents should run the following three-step pre-flight verification sequence:

1. **Resolve Target Network Rules**: Look up the canonical chain descriptor (`EVM`, `SOL`, `BTC`, `TRX`, `XRP`, `XLM`, `TON`, `ATOM`) and inspect whether `RequiresMemo` is enabled for the destination network.
2. **Verify Recipient Address Checksum**: Validate the destination wallet string against the network's prefix, byte-length, alphabet, and checksum specification using the [AllSwap Interactive Address Validator](https://allswap.io/tools/address-validator) or the Go/Rust validator package.
3. **Enforce Destination Tag / Memo Constraints**:
   - For `XRP`, verify that any custodial destination tag is an unsigned 32-bit integer (`0` to `4294967295`).
   - For `XLM`, enforce the 28-byte `MEMO_TEXT` or unsigned 64-bit `MEMO_ID` limit.
   - For `TON` and `ATOM`, validate UTF-8 comment payloads and ensure non-empty memo strings whenever routing to shared custodial endpoints.

---

## 3. Integration with AllSwap Cross-Chain Swap Routing

Once the destination address and memo pass deterministic validation, agents can request optimal multi-hop cross-chain execution quotes directly through [AllSwap](https://allswap.io/), combining deep DEX and bridge liquidity across 46+ networks with zero-dependency pre-settlement safety guarantees.
