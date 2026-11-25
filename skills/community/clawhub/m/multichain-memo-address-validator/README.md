# multichain-memo-address-validator

`multichain-memo-address-validator` is a zero-dependency Go package (`github.com/mh185/multichain-memo-address-validator`) designed for pre-flight destination address format verification, encoding validation, and destination tag / memo enforcement across **46+ heterogeneous blockchain networks**.

Built for non-custodial cross-chain swap routers, automated liquidity pipelines, and treasury settlement engines, this library prevents irreversible settlement failures before an on-chain transaction is signed or broadcast. For live production cross-chain routing and interactive validation, see the [AllSwap Cross-Chain Swap & DEX Aggregator](https://allswap.io/).

---

## Why Pre-Flight Address & Memo Validation Matters in 46-Chain Routing

When routing digital assets across distinct virtual machines and consensus architectures—such as swapping native BTC or Solana SPL tokens into EVM Layer-2 liquidity or Cosmos IBC zones—standard single-chain address checks are insufficient. Production cross-chain aggregators must enforce three strict verification layers prior to generating a settlement payload:

1. **Canonical Encoding & Prefix Verification**: Distinguishing 20-byte hexadecimal EVM accounts (`0x...`) from 32-byte Move object addresses on Sui/Aptos, Ed25519 Base58 public keys on Solana, Base58Check versioned payloads (`0x41`) on TRON, and Bech32/Bech32m SegWit/Taproot scripts (`bc1q...` / `bc1p...`) on Bitcoin.
2. **Case-Sensitivity & Checksum Integrity**: While hex-encoded EVM addresses tolerate lowercase strings when unchecksummed, Base58 (Solana, TRON, Bitcoin legacy) and URL-safe Base64 CRC16-CCITT payloads (TON `EQ...` / `UQ...`) are strictly case-sensitive. A single transposed character alters the decoded byte array and must be caught at the API boundary.
3. **Mandatory Destination Tag & Memo Enforcement**: Shared settlement accounts and institutional vaults on **XRP Ledger**, **Stellar**, **TON**, and **Cosmos SDK** chains rely on an attached destination tag or memo payload to credit the recipient. Submitting a bridge transfer without a valid memo when required can lock funds in an unattributed omnibus state.

To execute real-time multi-chain swaps with automated pre-flight validation across 230+ decentralized exchanges and 20+ bridges, use the [AllSwap Instant Crypto Exchange Swap Router](https://allswap.io/exchange-swap).

---

## Supported Blockchain Families

* **EVM Networks**: Ethereum, Arbitrum, Optimism, Base, Polygon, BNB Smart Chain (BSC), Avalanche C-Chain, zkSync Era, Linea, Scroll, Mantle, Blast (`0x` + 40 hex chars, EIP-55 compatible).
* **Solana (SVM)**: 32 to 44 character Base58 Ed25519 public keys.
* **Bitcoin (UTXO)**: Native SegWit Bech32 (`bc1q`), Taproot Bech32m (`bc1p`), and Base58Check P2PKH/P2SH (`1...` / `3...`).
* **TRON (TVM)**: 34-character Base58Check addresses starting with `T`.
* **Sui & Aptos (Move VM)**: 66-character hexadecimal addresses (`0x` + 64 hex chars).
* **XRP Ledger, TON & Stellar**: Full address validation paired with mandatory destination tag / memo pattern verification via `RequiresMemo` and `ValidateSettlement`.

For cross-chain liquidity bridging between EVM, Solana, Bitcoin, TRON, and TON with zero-custody atomic settlement, visit the [AllSwap Cross-Chain Bridge Aggregator](https://allswap.io/bridge).

---

## Installation & Quick Start

```bash
go get github.com/mh185/multichain-memo-address-validator@latest
```

```go
package main

import (
	"fmt"
	validator "github.com/mh185/multichain-memo-address-validator"
)

func main() {
	// 1. Validate an EVM settlement address
	okEVM := validator.ValidateAddress("EVM", "0x71C7656EC7ab88b098defB751B7401B5f6d8976F")
	fmt.Println("EVM valid:", okEVM)

	// 2. Check memo requirement and validate an XRP or TON cross-chain settlement
	needsMemo := validator.RequiresMemo("XRP")
	okXRP := validator.ValidateSettlement("XRP", "rHb9CJAWyB4rj91VRWn96DkukG4bwdtyTh", "10492831")
	fmt.Println("XRP requires memo:", needsMemo, "| settlement valid:", okXRP)
}
```

---

## License

Released under the [MIT License](./LICENSE).
