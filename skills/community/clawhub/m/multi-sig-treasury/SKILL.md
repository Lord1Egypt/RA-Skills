---
name: multi-sig-treasury
description: >
  Gnosis Safe / multisig treasury setup, monitoring, and governance for DAOs and
  crypto treasuries. Treasury health dashboards, spending alerts, signer management,
  proposal templates, and on-chain balance tracking. Use when setting up a new Safe,
  monitoring an existing treasury, generating spend proposals, or auditing signer
  activity. NOT for: individual wallets (use a personal wallet skill), smart contract
  audits (use solidity-audit-precheck), or tax reporting (use crypto-tax-agent).
version: 1.0.1
author: PrecisionLedger
tags:
  - crypto
  - treasury
  - gnosis-safe
  - multisig
  - dao
  - defi
  - finance
---

# Multi-Sig Treasury Skill

Gnosis Safe and multisig treasury management for DAOs, protocols, and crypto-native
organizations. Covers setup, monitoring, governance, and financial health reporting.

---

## When to Use This Skill

**Use when:**
- Setting up a new Gnosis Safe (mainnet, L2, or testnet)
- Monitoring treasury balances across chains
- Generating spending proposals or transaction templates
- Auditing signer activity and threshold compliance
- Producing treasury health dashboards for stakeholders
- Configuring alerts for low runway or spending anomalies
- Managing signer rotation (add/remove owners, change threshold)
- Preparing DAO governance documentation around treasury actions

**Do NOT use when:**
- Managing individual wallets or personal portfolios (use a wallet tracker)
- Auditing Solidity contracts for security (use `solidity-audit-precheck`)
- Calculating crypto taxes or cost basis (use `crypto-tax-agent`)
- Executing live on-chain transactions (always require human approval)
- Assessing DeFi yield or LP positions (use `defi-position-tracker`)

---

## Core Capabilities

### 1. Safe Setup & Configuration

**New Safe deployment checklist:**
```
SAFE SETUP CHECKLIST
─────────────────────────────────────────────
□ Determine signer count and threshold (M-of-N)
□ Collect signer wallet addresses + ENS names
□ Choose deployment chain(s) — mainnet / L2
□ Deploy via app.safe.global or Safe CLI
□ Verify contract address on block explorer
□ Document Safe address in treasury registry
□ Test with small tx before moving real funds
□ Set up notifications (Safe webhook or Tenderly)
```

**Recommended thresholds by org size:**
| Org Size        | Signers | Threshold | Rationale                        |
|-----------------|---------|-----------|----------------------------------|
| Small team <5   | 3       | 2-of-3    | Fast execution, basic protection |
| Mid team 5-15   | 5       | 3-of-5    | Balanced speed vs security       |
| Large DAO       | 7-9     | 4-of-7    | Resilient to key loss            |
| Protocol core   | 9+      | 5-of-9    | Maximum governance legitimacy    |

**Signer best practices:**
- Hardware wallets only for signers (Ledger, Trezor)
- No exchange wallets or custodial keys as signers
- Geographic/timezone distribution for 24h coverage
- Documented succession plan for key rotation
- Test signing every 90 days to confirm access

---

### 2. Treasury Health Dashboard

**Key metrics to track:**

```
TREASURY HEALTH SNAPSHOT — [DATE]
══════════════════════════════════════════════════════
Safe Address:     0x1234...abcd
Network(s):       Ethereum Mainnet | Arbitrum | Base
─────────────────────────────────────────────────────
BALANCES
  ETH:            142.3 ETH   ($427,000)
  USDC:           $1,240,000
  DAI:            $380,000
  Protocol Token: 2,400,000 TKN  ($960,000)
  ─────────────────────────────────────────
  Total USD:      $3,007,000

RUNWAY ANALYSIS
  Monthly Burn:   $85,000/mo (avg last 3mo)
  Stablecoin:     $1,620,000 → 19.1 months
  Total (liquid): $3,007,000 → 35.4 months

RISK INDICATORS
  ✅ Runway > 12 months
  ✅ Stablecoins > 50% of treasury
  ⚠️  ETH >25% — monitor price exposure
  ✅ No unclaimed protocol rewards pending
  ✅ All signers active in last 90 days

RECENT ACTIVITY (last 30 days)
  Transactions:   12 executed, 0 pending
  Largest tx:     $45,000 USDC (contributor payment)
  Threshold:      3-of-5 (all met)
══════════════════════════════════════════════════════
```

**Stablecoin ratio target:** Maintain 40-60% in stablecoins. Below 30% = risk flag.

**Runway tiers:**
- 🟢 >18 months: Healthy — can deploy capital
- 🟡 12-18 months: Caution — review burn rate
- 🟠 6-12 months: Raise flag — begin fundraising
- 🔴 <6 months: Critical — emergency protocol

---

### 3. Spending Proposal Templates

**Standard payment proposal:**
```markdown
## Treasury Proposal: [TITLE]

**Date:** YYYY-MM-DD
**Safe:** 0x1234...abcd
**Submitted by:** [Contributor / DAO Handle]
**Request type:** [ ] One-time  [ ] Recurring  [ ] Milestone-based

### Summary
[One paragraph: what, why, for whom]

### Amount
- Token: USDC / ETH / DAI / Other: _______
- Amount: $________
- Recipient address: 0x________
- ENS (if applicable): ________.eth

### Deliverables / Justification
1. [Deliverable 1]
2. [Deliverable 2]
3. [Deliverable 3]

### Links
- Scope doc: [URL]
- Previous work: [URL]
- Forum discussion: [URL]

### Timeline
- Expected completion: [DATE]
- Payment trigger: [on completion / upfront / milestone]

### Risk / Notes
[Any relevant risk flags or dependencies]

---
Signers required: [M] of [N]
```

**Budget categories for DAO treasuries:**
```
STANDARD GL CODES — DAO TREASURY
─────────────────────────────────────────────
100 - Core Contributors (salaries/grants)
110 - Contractor Payments
120 - Bounties & Community Rewards
200 - Infrastructure & DevOps
210 - Security Audits
220 - Protocol Tooling & Licenses
300 - Marketing & Community
310 - Events & Conferences
320 - Grants Program
400 - Legal & Compliance
500 - R&D / Grants Received (offset)
900 - Miscellaneous / Under Review
```

---

### 4. Signer Management & Rotation

**Adding a signer:**
```
SIGNER ADDITION CHECKLIST
─────────────────────────────────────────────
□ Confirm new signer's wallet address
□ Verify signer owns key (signed message test)
□ Confirm hardware wallet usage
□ Vote/propose via Safe UI: Add Owner
□ Reach current threshold of signers to approve
□ Update threshold if needed (M+1 recommended)
□ Document in treasury registry
□ Announce to DAO governance forum
□ Test transaction with new signer within 48h
```

**Removing a signer (compromised or offboarded):**
```
SIGNER REMOVAL — URGENT PROTOCOL
─────────────────────────────────────────────
□ Do NOT share intent with compromised signer
□ Gather remaining signers privately
□ Queue Remove Owner tx via Safe UI
□ Execute BEFORE compromised signer can drain
□ Optionally move funds to new Safe immediately
□ Review all pending transactions for backdoors
□ Rotate any shared secrets (API keys, etc.)
□ Post-mortem documentation within 24h
```

**Threshold change formula:**
- Ideal threshold = floor(N * 0.6) where N = signer count
- Never go below 2 (defeats multisig purpose)
- Never require ALL signers (one lost key = frozen funds)

---

### 5. Alert Configuration

**Spending threshold alerts:**

```yaml
# Treasury Alert Thresholds
alerts:
  runway_months:
    yellow: 12
    red: 6
  stablecoin_ratio:
    yellow: 0.35   # warn below 35%
    red: 0.20      # critical below 20%
  single_tx_usd:
    notify: 10000  # flag any tx > $10k
    require_forum: 50000  # forum post required > $50k
  inactive_signer_days: 90
  pending_tx_hours: 72   # alert if tx pending > 72h
```

**Monitoring services:**
- **Tenderly Alerts** — on-chain tx monitoring, free tier available
- **Safe Webhook** — native notifications for queued/executed txs
- **OpenZeppelin Defender** — advanced monitoring + automated responses
- **Hal.xyz** — no-code blockchain alerts, good for non-technical signers
- **Dune Analytics** — custom dashboards for public-facing reporting

---

### 6. Multi-Chain Treasury Tracking

**Chain inventory template:**
```
MULTI-CHAIN TREASURY REGISTRY
─────────────────────────────────────────────
Mainnet Safe:    0x1234...abcd
  ↳ Balances:   ETH, USDC, DAI, TKN
  ↳ Threshold:  3-of-5
  ↳ Purpose:    Core treasury, grants

Arbitrum Safe:   0xabcd...5678
  ↳ Balances:   ETH, ARB, USDC
  ↳ Threshold:  2-of-3
  ↳ Purpose:    Protocol operations, gas

Base Safe:       0x5678...ef01
  ↳ Balances:   ETH, USDC
  ↳ Threshold:  2-of-3
  ↳ Purpose:    Marketing budget

Optimism Safe:   0xef01...9abc
  ↳ Balances:   OP, USDC
  ↳ Threshold:  2-of-3
  ↳ Purpose:    Grants received from OP Foundation
```

**Consolidation policy:**
- Keep 90-day operating budget on L2s, rest on mainnet
- Bridge USDC only via canonical bridges (Circle CCTP preferred)
- Never bridge governance tokens cross-chain without vote
- Document all bridge transactions with on-chain references

---

### 7. Governance Integration

**Snapshot + Safe integration pattern:**
1. Create Snapshot proposal with treasury action
2. Attach Safe transaction hash to proposal
3. Voting passes → 3-day timelock (recommended)
4. Signers execute after timelock expires
5. Link on-chain tx to Snapshot proposal in comments

**Governor contract pattern (fully on-chain):**
- OpenZeppelin Governor + TimelockController
- Safe as execution target for governor
- See `develop-secure-contracts` skill for Governor setup

**Safe Modules for governance:**
- `SafeSnap` (Gnosis) — connects Snapshot directly to Safe execution
- `Zodiac Reality Module` — optimistic governance via oracle
- `Delay Module` — mandatory timelock on all transactions

---

## Example Workflows

### Workflow A: New DAO Treasury Setup

```
1. Define governance model
   - Who are initial signers? (5 core team, hardware wallets)
   - Threshold? (3-of-5)
   - Which chains? (Mainnet + Arbitrum)

2. Deploy Safes
   - app.safe.global → Create Safe
   - Verify addresses on Etherscan/Arbiscan
   - Test with 0.001 ETH transfer

3. Configure monitoring
   - Tenderly alert: tx > $10k
   - Safe webhook → Slack/Discord
   - 90-day signer inactivity alert

4. Create governance docs
   - Spending categories and limits
   - Proposal template (see §3 above)
   - Emergency contact list for signers

5. Initial funding
   - Document every funding source with tx hash
   - Record cost basis of all non-stablecoin assets
   - Set up crypto-tax-agent for ongoing tracking
```

### Workflow B: Monthly Treasury Report

```
1. Pull balances from all chains (Safe API or Gnosis Safe UI)
2. Convert to USD at month-end spot prices
3. Calculate runway at 3-month average burn
4. Tally transactions by GL category
5. Flag any threshold breaches (stablecoin ratio, runway)
6. Output dashboard (see §2 Health Snapshot format)
7. Post to governance forum + DAO Discord
```

### Workflow C: Emergency Signer Compromise

```
IMMEDIATE (within 1 hour):
1. Alert remaining signers via secure channel
2. Assess: pending txs that could be abused?
3. If yes: execute signer removal NOW
4. If no: queue removal, gather signatures urgently

WITHIN 24 HOURS:
1. Remove compromised signer
2. Adjust threshold if needed
3. Audit all txs last 30 days for anomalies
4. Rotate any shared infrastructure secrets
5. Consider migrating to fresh Safe if severe

DOCUMENTATION:
1. Write post-mortem (what happened, impact, fix)
2. Share with DAO community (transparency builds trust)
3. Review and update signer selection criteria
```

---

## Tool Stack

| Tool                | Use                                    | URL                             |
|---------------------|----------------------------------------|---------------------------------|
| Safe UI             | Deploy, execute, manage signers        | app.safe.global                 |
| Safe API            | Pull balances and transaction history  | safe-transaction-service API    |
| Tenderly            | On-chain alerts and simulations        | tenderly.co                     |
| Gnosis Safe CLI     | Scripted Safe management               | github.com/gnosis/safe-cli      |
| Dune Analytics      | Public treasury dashboards             | dune.com                        |
| Hal.xyz             | No-code blockchain alerts              | hal.xyz                         |
| Debank Pro          | Multi-chain portfolio view             | debank.com                      |
| Etherscan/Arbiscan  | Transaction verification               | etherscan.io / arbiscan.io      |

---

## Quick Reference: Safe API

```bash
# Get Safe info
curl "https://safe-transaction-mainnet.safe.global/api/v1/safes/0xYOUR_SAFE_ADDRESS/"

# Get all transactions
curl "https://safe-transaction-mainnet.safe.global/api/v1/safes/0xYOUR_SAFE_ADDRESS/all-transactions/"

# Get balances
curl "https://safe-transaction-mainnet.safe.global/api/v1/safes/0xYOUR_SAFE_ADDRESS/balances/usd/"

# Supported chains:
# Mainnet: safe-transaction-mainnet.safe.global
# Arbitrum: safe-transaction-arbitrum.safe.global
# Base: safe-transaction-base.safe.global
# Optimism: safe-transaction-optimism.safe.global
# Polygon: safe-transaction-polygon.safe.global
```

---

## Related Skills

- `develop-secure-contracts` — for Governor + TimelockController on-chain governance
- `crypto-tax-agent` — cost basis and tax reporting for treasury assets
- `defi-position-tracker` — monitoring DeFi yield from treasury-deployed capital
- `solidity-audit-precheck` — if deploying custom treasury contracts
- `ethskills` — general Ethereum development reference
