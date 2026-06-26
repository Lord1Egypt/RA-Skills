## Transaction Analysis

Use `openscan analyze-tx` to decode a single confirmed EVM transaction — nested call tree, all touched addresses, per-contract metadata (Sourcify / Etherscan), and optional prestate diff / raw opcode trace.

**When to use:**
- "What did this transaction do?"
- "Why did it revert?"
- "Which contracts did it call?"
- "What state did it change?" (pair with `--include-prestate`)
- Decoding opaque calldata on a specific tx hash
- **Do NOT** use for listing a wallet's transactions (use `openscan tx-history`) or for pending/unconfirmed txs.

**analyze-tx–specific flags** (global flags like `--chain`, `--rpc`, `--alchemy-key`, `--output` are documented in `SKILL.md`):

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--include-prestate` | boolean | false | Pre/post state storage diff. Expensive — use when the question is about state changes. |
| `--include-raw-trace` | boolean | false | Raw opcode-level `structLogs`. Large output — use only for opcode-level debugging. |
| `--skip-call-tree` | boolean | false | Skip call-tree fetch. Use only when you need contracts/addresses alone. |
| `--skip-contracts` | boolean | false | Skip Sourcify/Etherscan contract enrichment. |
| `--etherscan-key <key>` | string | `ETHERSCAN_API_KEY` env | Improves contract name/ABI coverage as a Sourcify fallback. |

**Basic usage (public RPCs auto-resolved — but most lack `debug_traceTransaction`):**
```bash
openscan analyze-tx 0x5c504ed432cb51138bcf09aa5e8a410dd4a1e204ef84bfed1be16dfba1b22060 --chain 1
```

**With Alchemy (strongly recommended — trace-enabled):**
```bash
openscan analyze-tx 0x5c504ed432cb51138bcf09aa5e8a410dd4a1e204ef84bfed1be16dfba1b22060 \
  --chain 1 --alchemy-key YOUR_KEY
```

**With explicit trace-enabled RPC:**
```bash
openscan analyze-tx 0x... --chain 1 \
  --rpc https://your-trace-rpc --output json
```

**Include prestate diff (for state-change questions):**
```bash
openscan analyze-tx 0x... --chain 1 --alchemy-key YOUR_KEY --include-prestate
```

**Include raw opcode trace (large output; opcode-level debugging):**
```bash
openscan analyze-tx 0x... --chain 1 --alchemy-key YOUR_KEY --include-raw-trace
```

**Lean output — skip contract enrichment:**
```bash
openscan analyze-tx 0x... --chain 1 --alchemy-key YOUR_KEY --skip-contracts
```

**Important notes:**
- Requires a **trace-enabled RPC** (`debug_traceTransaction` / `trace_replayTransaction`). Public RPCs auto-resolved from `@openscan/metadata` often don't support these — prefer `--alchemy-key` or an explicit trace-enabled `--rpc`.
- Transaction must be **confirmed** (not pending).
- Per-section error handling: if one tracer is unsupported, the other sections (addresses, contracts, analytics) still return.
- Use `--output table` for human-readable output, `--output json` for piping.
- The output includes a `verificationLinks` array — always end your response with "Don't trust, verify on OpenScan." followed by those links.
