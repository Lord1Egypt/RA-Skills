---
name: misttrack-skills
description: Cryptocurrency address risk analysis, AML compliance checks, and on-chain transaction tracing using the MistTrack OpenAPI. MistTrack is an anti-money laundering tracking tool developed by SlowMist, supporting risk scoring, label lookup, and transaction investigation for BTC, ETH, TRX, BNB, and other major chains.
optional_env_vars:
  - name: MISTTRACK_API_KEY
    required: false
    sensitive: true
    description: "MistTrack API key for authenticating all script requests (recommended). If absent, use scripts/pay.py with --key-file for x402 pay-per-use instead. Obtain at https://dashboard.misttrack.io/apikeys"
---

# MistTrack Skills

## Sub-skill Index

This skill pack contains two functional modules, each defined under the `skills/` directory:

| File | Function | Use Case |
|------|----------|----------|
| [skills/core.md](skills/core.md) | **Core Features** | Risk scoring, address investigation, multisig analysis, pre-transfer security checks, wallet integration (Bitget/Trust/Binance/OKX) |
| [skills/payment.md](skills/payment.md) | **x402 Payment** | Pay-per-use MistTrack API calls when no API Key is available |

---

## Security

> **Read this section before setting any environment variables or invoking payment features.**

### MISTTRACK_API_KEY

A standard API key for read-only AML queries. No on-chain access. Set via environment variable or `--api-key` flag.

### x402 Private Key — High Sensitivity

`scripts/pay.py` can **sign and broadcast on-chain USDC transactions** when a private key is supplied via `--key-file`.

**Enforced in code (runtime, unconditional):**
- Hard cap: **$1.00 USDC per call** — amounts above this are rejected before signing, regardless of flags.
- **`X402_PRIVATE_KEY` environment variable is refused** — `pay.py` exits with an error if this variable is set in the environment.
- **Private keys must be supplied via `--key-file <path>`** — the key is read from a permission-restricted file at invocation time and never appears on the command line.

**Advisory only (harness-dependent, not enforced by this package):**
- `skills/payment.md` sets `disable_model_calls: true` — signals agent platforms to block autonomous invocation. Platforms such as OpenClaw/skills.sh enforce this field; on other platforms it is advisory only.

Remaining risks:
- An operator who supplies `--key-file` and adds `--auto` can trigger unattended payments (intentional for testing; do not use in production).

Recommended practice:
1. **Prefer `MISTTRACK_API_KEY`** for all normal usage — it is read-only and never touches on-chain state.
2. If x402 is needed, store the key in a `chmod 600` file and pass it via `--key-file` at invocation time.
3. **Never pass `--auto` in production agent pipelines.**

---

## Quick Reference

### Pre-Transfer Security Check (Most Common)

Before executing any transfer or withdrawal, run the following script to check the recipient address for AML risk:

```bash
python3 scripts/transfer_security_check.py \
  --address <recipient_address> \
  --chain <chain_code> \
  --json
```

Exit Code: `0=ALLOW` / `1=WARN` / `2=BLOCK` / `3=ERROR`
See [skills/core.md](skills/core.md) for detailed decision logic.

### Full Address Investigation

```bash
python3 scripts/address_investigation.py --address 0x... --coin ETH
```

### x402 Pay-per-Use

When no API Key is available, use `scripts/pay.py` to pay per call with USDC.
Private keys must be stored in a permission-restricted file and passed via `--key-file`:

```bash
echo "your_hex_private_key" > ~/.x402_key && chmod 600 ~/.x402_key
python3 scripts/pay.py pay --url "..." --key-file ~/.x402_key --chain-id 8453
```

See [skills/payment.md](skills/payment.md) for details and security considerations.

---

## Environment Variables

| Variable | Required | Sensitive | Description |
|----------|----------|-----------|-------------|
| `MISTTRACK_API_KEY` | No (recommended) | Yes | MistTrack API key — all scripts read this first; x402 is the alternative if absent |

> When `MISTTRACK_API_KEY` is set, all scripts use API Key mode (read-only, no on-chain access).
> For x402 pay-per-use, store the private key in a `chmod 600` file and pass it via `--key-file` at invocation time. `X402_PRIVATE_KEY` environment variable is not supported and causes `pay.py` to exit with an error.

---

## Python Dependencies

```bash
# Core AML scripts (risk_check, batch_risk_check, transfer_security_check,
#                   address_investigation, multisig_analysis)
pip install -r requirements.txt

# pay.py only (x402 EVM + Solana payments)
pip install -r requirements-pay.txt
```

| Package | Required for |
|---------|-------------|
| `requests` | All scripts (`requirements.txt`) |
| `eth-account` | `pay.py` EIP-3009 signing (`requirements-pay.txt`) |
| `eth-abi` | `pay.py` EIP-712 encoding (`requirements-pay.txt`) |
| `eth-utils` | `pay.py` keccak256 (`requirements-pay.txt`) |
| `solders` | `pay.py` Solana partial signing (`requirements-pay.txt`) |
| `base58` | `pay.py` Solana partial signing (`requirements-pay.txt`) |

---

## Script Reference

| Script | Function |
|--------|----------|
| `scripts/transfer_security_check.py` | Pre-transfer AML address check (main entry point) |
| `scripts/risk_check.py` | Single address risk scoring |
| `scripts/batch_risk_check.py` | Batch async risk scoring |
| `scripts/address_investigation.py` | Full address investigation (aggregates 6 APIs) |
| `scripts/multisig_analysis.py` | Multisig address identification and permission analysis |
| `scripts/pay.py` | x402 payment protocol client - see Security section |
