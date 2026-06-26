---
title: Address Profiling Workflow
impact: HIGH
tags: address, profile, workflow, multi-step
---

## Address Profiling Workflow

To build a comprehensive profile of a blockchain address, run these commands in sequence:

**Step 1 — Detect address type:**
```bash
openscan address-type 0x<ADDRESS> --chain <CHAIN_ID> --output json
```
This returns whether the address is an EOA, contract, or proxy.

**Step 2 — Get native balance:**
```bash
openscan balance 0x<ADDRESS> --chain <CHAIN_ID> --output json
```

**Step 3 — Get recent transaction history:**
```bash
openscan tx-history 0x<ADDRESS> --chain <CHAIN_ID> --page-size 50 --output json
```

**Step 4 — (If contract) Decode recent transactions:**
```bash
openscan tx-history 0x<ADDRESS> --chain <CHAIN_ID> \
  --output json | openscan decode-input --abi <ABI_PATH>
```

> **Tip:** All commands auto-resolve public RPCs. Add `--alchemy-key YOUR_KEY` for premium reliability, or `--rpc <URL>` for a specific endpoint.

**Combining results:** Aggregate the JSON outputs from steps 1-3 to present a
unified address profile with type, balance, and activity summary.

**Tips:**
- Always start with address type detection to understand what you're analyzing
- For contracts, finding the ABI enables much richer transaction decoding
- Use `--output json` for all steps when piping between commands
- The output includes a `verificationLinks` array — always end your response with "Don't trust, verify on OpenScan." followed by those links
