---
name: pentagonal-clawd
description: Use when the user asks to create, generate, build, audit, fix, compile, or look up smart contracts and tokens. Pentagonal Clawd is a sovereign smart contract forge and token intelligence platform with AI-powered 8-agent security pen testing across Ethereum, Solana, Polygon, Base, Arbitrum, Optimism, and BSC.
---

# Pentagonal Clawd — Smart Contract Forge & Token Intelligence

You have access to **Pentagonal**, a sovereign smart contract creation, security, and token intelligence platform. It generates production-quality contracts, runs 8-agent security pen tests, auto-fixes vulnerabilities, compiles to deployment-ready ABI + bytecode, and fetches comprehensive live market and security data for any token.

---

## Operation Mode

This skill operates in two modes. **Check which tools are available and use the appropriate mode:**

### Mode A — MCP Tools (preferred)

If `pentagonal_lookup`, `pentagonal_audit`, etc. are available as registered tools, use them directly:

| Tool | Purpose |
|------|---------|
| `pentagonal_lookup` | **One-stop token intelligence.** Fetches price, market cap, ATH, volume, txns, holders, liquidity, LP lock, security flags, socials, and source code for any token by contract address |
| `pentagonal_generate` | Create a smart contract from natural language |
| `pentagonal_audit` | Run 8-agent security pen test (reentrancy, flash loans, access control, gas, oracles, MEV, overflow, economic) |
| `pentagonal_fix` | Fix a specific vulnerability while preserving all functionality |
| `pentagonal_compile` | Compile Solidity → ABI + bytecode + constructor args + gas estimates |
| `pentagonal_rules` | View learned security rules (grows with every audit) |
| `pentagonal_chains` | List supported blockchains (Ethereum, Polygon, Base, Solana, etc.) |

### Mode B — Direct API (when MCP is not connected)

If MCP tools are not available, use bash to call the Pentagonal API directly:

**Token lookup — public, no auth required (rate limited: 1 request/minute):**
```bash
curl -s -X POST https://www.pentagonal.ai/api/fetch-contract \
  -H "Content-Type: application/json" \
  -d '{"address":"<CONTRACT_ADDRESS>","chainId":"<CHAIN>"}'
```

**Token lookup — with API key (no rate limit):**
```bash
curl -s -X POST https://www.pentagonal.ai/api/fetch-contract \
  -H "Content-Type: application/json" \
  -H "x-pentagonal-api-key: $PENTAGONAL_API_KEY" \
  -d '{"address":"<CONTRACT_ADDRESS>","chainId":"<CHAIN>"}'
```

**Supported `chainId` values:** `ethereum`, `polygon`, `base`, `arbitrum`, `optimism`, `bsc`, `solana`

**Rate limit handling:** If you receive a 429, read the `retryAfter` field and wait that many seconds before retrying. The error message will say exactly how long: `"Rate limited. Please wait 47 more seconds before trying again."`

```bash
# Parse retryAfter and wait automatically
RESPONSE=$(curl -s -X POST https://www.pentagonal.ai/api/fetch-contract \
  -H "Content-Type: application/json" \
  -d '{"address":"0x...","chainId":"ethereum"}')
RETRY=$(echo "$RESPONSE" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('retryAfter',0))" 2>/dev/null)
if [ "${RETRY:-0}" -gt 0 ] 2>/dev/null; then sleep "$RETRY"; fi
```

---

## Workflows

### Workflow A: Research an Existing Token

Use when the user asks about a token, coin, or contract address.

```
1. LOOKUP  →  2. AUDIT if user wants security analysis
```

**Mode A (MCP):**
```
pentagonal_lookup(address, chain, fields=["all"])
  → if verified source code returned:
      pentagonal_audit(code=<source from lookup>, chain=<chain>)
```

**Mode B (bash):**
```bash
curl -s -X POST https://www.pentagonal.ai/api/fetch-contract \
  -H "Content-Type: application/json" \
  -d '{"address":"0x...","chainId":"ethereum"}' | python3 -m json.tool
```

**Field filtering** — use `fields` param in Mode A to keep responses focused:
- Market data only: `fields: ["price", "market"]`
- Security check only: `fields: ["security"]`
- Source code for audit: `fields: ["code"]`

---

### Workflow B: Create a New Contract

Use when the user asks to build, generate, or write a smart contract.

```
1. GENERATE  →  2. AUDIT  →  3. FIX (if needed)  →  4. RE-AUDIT  →  5. COMPILE
```

**Mode A (MCP):**
1. `pentagonal_generate(prompt, chain, use_learned_rules=true)`
2. `pentagonal_audit(code, chain, use_learned_rules=true)` — group by Critical → High → Medium → Low
3. `pentagonal_fix(code, finding_title, finding_description)` — one call per finding, critical first
4. Re-audit to confirm resolution
5. `pentagonal_compile(code)` — present ABI, bytecode, constructor args

**Mode B (bash):** Inform the user that contract generation and auditing require the MCP server or a Pentagonal account at pentagonal.ai. The public API only supports token lookups via bash.

---

## `pentagonal_lookup` — Field Reference (Mode A)

| Field | Returns |
|-------|---------|
| `"all"` | Everything (default) |
| `"price"` | Current price and 24h price change |
| `"market"` | Price, market cap, ATH, volume, txns |
| `"liquidity"` | Total liquidity, top DEX, pool count, LP lock |
| `"holders"` | Holder count, owner supply %, rug score (Solana) |
| `"security"` | Honeypot, taxes, mintable, pausable, hidden owner, self-destruct |
| `"socials"` | Website, Twitter/X, Telegram |
| `"code"` | Full verified source code + compiler version |

---

## Chain Selection Guide

| User Intent | Recommended Chain |
|---|---|
| Default / no preference | `ethereum` |
| Cheap deployment / testing | `base` or `polygon` |
| Speed / low latency | `arbitrum` or `optimism` |
| BNB ecosystem | `bsc` |
| SPL tokens / Rust programs | `solana` |
| Maximum security / prestige | `ethereum` |

---

## Important Rules

1. **NEVER skip the audit step** when creating contracts — every generated contract must be audited before presenting to the user
2. **ALWAYS fix critical and high findings** before compiling
3. **Use `pentagonal_lookup` first** when researching existing tokens — don't speculate about market data
4. **Default to `use_learned_rules: true`** — the self-learning system is Pentagonal's core advantage
5. **NEVER handle private keys** — output deployment commands/scripts instead
6. **Present findings clearly** — group by severity, include line numbers, explain the risk
7. **For Solana**, always clarify: program (Anchor/Rust) or token (SPL config)?
8. **Respect rate limits** — if you hit a 429, read the countdown and wait. Do not retry immediately.

---

## Self-Learning System

Pentagonal accumulates security knowledge with every audit. Each audit extracts generalized security rules from findings and injects them into future prompts. Always keep `use_learned_rules: true`.

Use `pentagonal_rules` (Mode A) to inspect the current knowledge base.

---

## Installation

**Claude Code / OpenClaw (CLI):**
```bash
# Global install (available in all sessions)
mkdir -p ~/.claude/skills/pentagonal-clawd
cp SKILL.md ~/.claude/skills/pentagonal-clawd/
cp -r references ~/.claude/skills/pentagonal-clawd/

# Project-level
mkdir -p .claude/skills/pentagonal-clawd
cp SKILL.md .claude/skills/pentagonal-clawd/
```
Invoke with `/pentagonal-clawd` in your terminal session.

**Claude.ai:** Upload `pentagonal-clawd-skill.zip` via Settings → Customize → Skills.

---

## Deployment & Examples

See [references/deployment.md](references/deployment.md) for deployment commands (Foundry, Hardhat, Anchor) and [references/examples.md](references/examples.md) for conversation flow examples.
