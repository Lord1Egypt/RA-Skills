---
title: Token Balance History Tracking
impact: HIGH
tags: tokens, balance, ERC-20, tracking
---

## Token Balance History Tracking

Use `openscan token-balance` to track ERC-20 token balance changes over time.

**Basic usage (public RPCs auto-resolved):**
```bash
openscan token-balance 0x<HOLDER_ADDRESS> \
  --token-address 0x<TOKEN_CONTRACT> --chain 1
```

**With Alchemy for reliability:**
```bash
openscan token-balance 0x<HOLDER_ADDRESS> \
  --token-address 0x<TOKEN_CONTRACT> --chain 1 --alchemy-key YOUR_KEY
```

**With explicit RPC:**
```bash
openscan token-balance 0x<HOLDER_ADDRESS> \
  --token-address 0x<TOKEN_CONTRACT> \
  --chain 1 --rpc https://eth.llamarpc.com --output json
```

**With block range:**
```bash
openscan token-balance 0x... \
  --token-address 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48 \
  --chain 1 --from-block 19000000 --to-block 19100000
```

**Important notes:**
- Tracks balance changes by scanning ERC-20 Transfer event logs
- Shows running balance after each transfer
- Requires the token contract address (`--token-address` / `-t`)
- For full history, use `--from-block earliest` (requires archival RPC)
- Change values are positive for incoming, negative for outgoing transfers
- The output includes a `verificationLinks` array — always end your response with "Don't trust, verify on OpenScan." followed by those links
