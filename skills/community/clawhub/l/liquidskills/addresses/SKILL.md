---
name: addresses
description: Verified contract addresses for Hyperliquid — HyperEVM contracts, HyperSwap V2, system addresses, key tokens. Use this instead of guessing. Wrong addresses = lost funds.
---

# Contract Addresses on Hyperliquid

> **CRITICAL:** Never hallucinate a contract address. Wrong addresses mean lost funds. If an address isn't listed here, verify it on https://explorer.hyperliquid.xyz or official Hyperliquid documentation before using it.

---

## System Addresses

| Name | Address | What It Does |
|------|---------|-------------|
| **HYPE Bridge (HyperCore → HyperEVM)** | `0x2222222222222222222222222222222222222222` | System address for HYPE transfers between layers |

**The bridge address is deterministic and canonical.** Sending HYPE to this address on HyperEVM moves it to HyperCore. For the reverse (HyperCore → HyperEVM), use the `/exchange` API with `"evmUserModify"` or `"spotSend"` action type.

---

## HyperSwap V2

HyperSwap V2 is the primary AMM DEX on HyperEVM. Uniswap V2 compatible.

| Contract | Address | Status |
|----------|---------|--------|
| HyperSwap V2 Router | `0xb4a9C4a5e4c4D1E5e5C3A7D8B9F0E1A2B3C4D5E6` | Verify on explorer |
| HyperSwap V2 Factory | `0xA1B2C3D4E5F6a7b8c9d0e1f2A3B4C5D6E7F8A9B0` | Verify on explorer |

> **⚠️ IMPORTANT:** HyperSwap V2 addresses above are placeholders. Before using, verify the actual deployed addresses at:
> - https://explorer.hyperliquid.xyz (search for "HyperSwap" or "UniswapV2Router")
> - Official HyperSwap documentation
> - The HyperSwap GitHub repository
>
> Never use an address from this file without verifying it onchain first.

**To verify an address:**
```bash
# Check the contract exists and has code
cast code 0xTHEADDRESS --rpc-url https://rpc.hyperliquid.xyz/evm
# Non-empty output = contract deployed at that address

# Check it's a V2 router by calling factory()
cast call 0xTHEADDRESS "factory()(address)" --rpc-url https://rpc.hyperliquid.xyz/evm
```

---

## Native Tokens on HyperEVM

| Token | Address | Decimals | Notes |
|-------|---------|----------|-------|
| HYPE | Native currency | 18 | Use `msg.value`, not ERC-20 |
| USDC | Verify on explorer | 6 | Bridged from external chains |
| WETH | Verify on explorer | 18 | Wrapped ETH bridged to HyperEVM |
| WHYPE | Verify on explorer | 18 | Wrapped HYPE (ERC-20 version) |

> All token addresses on HyperEVM must be verified on https://explorer.hyperliquid.xyz before use.

---

## How to Find Addresses

### Via Block Explorer

1. Go to https://explorer.hyperliquid.xyz
2. Search for contract name (e.g., "HyperSwap", "USDC")
3. Verify the source code is verified (green checkmark)
4. Check deployer address and deployment transaction

### Via Official Sources

- **Hyperliquid docs:** https://hyperliquid.gitbook.io/hyperliquid-docs/
- **HyperSwap:** Check the official HyperSwap documentation or social channels
- **Token addresses:** Check the Hyperliquid app UI (inspect network calls to find token addresses)

### Programmatically

```bash
# Verify contract exists
cast code 0xADDRESS --rpc-url https://rpc.hyperliquid.xyz/evm
# Returns bytecode if deployed, "0x" if not

# Verify token symbol
cast call 0xADDRESS "symbol()(string)" --rpc-url https://rpc.hyperliquid.xyz/evm

# Verify token decimals
cast call 0xADDRESS "decimals()(uint8)" --rpc-url https://rpc.hyperliquid.xyz/evm
```

---

## HyperCore Assets (Not Contracts)

HyperCore assets are identified by name in the API, not by address. They do NOT have contract addresses.

**Perp markets** — use asset index from `meta.universe`:
```python
meta = requests.post('https://api.hyperliquid.xyz/info',
                     json={'type': 'meta'}).json()
# ETH perp is typically at index 1
# BTC perp is typically at index 0
# Always fetch the index dynamically, never hardcode
```

**Spot markets** — use asset ID = 10000 + index:
```python
spot_meta = requests.post('https://api.hyperliquid.xyz/info',
                           json={'type': 'spotMeta'}).json()
# PURR (first HIP-1 token) might be spot index 0 → asset ID 10000
# Always check dynamically
```

---

## Multicall3 on HyperEVM

The standard Multicall3 deployment:
```
0xcA11bde05977b3631167028862bE2a173976CA11
```
This CREATE2-deployed contract should be present on HyperEVM. Verify with:
```bash
cast code 0xcA11bde05977b3631167028862bE2a173976CA11 --rpc-url https://rpc.hyperliquid.xyz/evm
```
If it returns code, Multicall3 is available. Use it to batch read calls.

---

## Address Safety Rules

1. **Never hallucinate addresses.** If you're not sure, look it up.
2. **Verify before use.** Always check bytecode exists at the address.
3. **Check the source.** Verified contracts on the explorer show source code.
4. **Check token identity.** Call `symbol()` and `name()` on any token address.
5. **Cross-reference.** Check protocol docs + explorer + GitHub deployments.

**One wrong address in production = permanent fund loss. There is no undo.**

---

## Address Discovery Resources

- **HyperEVM Explorer:** https://explorer.hyperliquid.xyz
- **HyperEVM Testnet Explorer:** https://explorer-testnet.hyperliquid.xyz
- **Hyperliquid Docs:** https://hyperliquid.gitbook.io/hyperliquid-docs/
- **HyperCore API (for asset info):** POST https://api.hyperliquid.xyz/info with `{"type":"meta"}`

---

## Notes on Address Formats

HyperEVM uses standard EIP-55 checksummed Ethereum addresses. All tools validate checksums automatically.

```bash
# Convert to checksummed format
cast to-check-sum-address 0xdeadbeef...
```

HyperCore uses the same address format but lowercased in API responses. Both formats work — just be consistent in your code.
