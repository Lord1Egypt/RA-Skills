---
name: onchain-contract-token-analysis
description: Analyze smart contracts, token mechanics, permissions, fee flows, upgradeability, market risks, and likely attack surfaces for onchain projects. Use when reviewing ERC-20s, launchpads, vaults, staking systems, LP fee routing, ownership controls, proxy setups, or suspicious token behavior.
user-invocable: true
metadata: {"openclaw":{"emoji":"🔍","skillKey":"onchain-contract-token-analysis"}}
---

# Onchain Contract / Token Analysis

Use this skill when the task is to assess a token, protocol, launch module, vault, staking system, router, or related onchain project from a security, permissions, tokenomics, or behavior perspective.

## Core objective

Produce a practical analysis that answers:

- What the system does
- Who controls it
- How value and fees move
- What privileged actions exist
- What users can lose money from
- Whether there are obvious red flags or design risks

## Workflow

### 1. Identify the scope

First determine which of these the request actually targets:

- token contract
- factory / launcher
- vault / staking / locker
- router / hook / proxy / module
- admin / governance / registry
- full protocol system

If the scope is unclear, infer it from the files, addresses, ABI names, deployment scripts, or docs.

### 2. Map the architecture

Before judging risk, build a compact model of the system:

- main contracts
- ownership / admin roles
- external dependencies
- upgradeability pattern
- event flow
- token creation flow
- fee routing flow

Prefer a short system map over long prose.

### 3. Check control and permissions

Always verify:

- `owner`, `admin`, `governor`, `operator`, `manager`, `signer`
- role-based access control
- pausable / blacklist / whitelist powers
- mint / burn / seize / rescue / withdraw permissions
- parameter setters
- upgrade authority
- emergency functions

Call out who can do what, and whether those powers are bounded or dangerous.

### 4. Check token mechanics

For ERC-20 and tokenized systems, verify:

- total supply model
- mintability
- burnability
- transfer restrictions
- fee on transfer / tax
- max wallet / max tx rules
- trading enable switch
- blacklist / antibot logic
- rebasing / reflection / hidden balance logic
- allowance edge cases

If the token claims to be standard, confirm whether behavior actually matches that claim.

### 5. Check fee and value flow

Trace where user funds or protocol fees go:

- LP fee recipients
- treasury recipients
- locker / vault recipients
- protocol fee splits
- conversion / swap path
- withdrawal path
- claim path

Do not just name recipients. Explain whether they are:

- immutable
- admin-changeable
- delayed
- claim-based
- dependent on offchain identity or signatures

### 6. Check upgradeability and mutability

If proxies or modules exist, verify:

- proxy type
- implementation admin
- initialization safety
- reinitialization protection
- storage layout assumptions
- upgrade trust model

If not upgradeable, still check whether behavior can change through configurable modules.

### 7. Check attack surface

Look for:

- arbitrary external calls
- reentrancy opportunities
- unchecked token callbacks
- unsafe approvals
- signature replay
- missing nonce / deadline checks
- address(0) edge cases
- misconfigured recipient logic
- accounting mismatch
- stale state after recipient updates
- rounding leakage
- griefing / denial-of-service vectors

When risk depends on business assumptions, state that explicitly.

### 8. Check market-facing risk

When the target is a token or launch flow, explicitly assess:

- honeypot-like behavior
- sell restrictions
- hidden tax changes
- admin ability to freeze exits
- liquidity custody
- locker guarantees
- whether front-end labels could misclassify the asset

Do not overclaim. Distinguish:

- confirmed malicious logic
- dangerous centralization
- poor design
- heuristic / market-behavior false positives

## Output format

Default to this structure:

### Summary

One short paragraph stating what the system is and the top conclusion.

### Findings

List issues in severity order:

- severity
- title
- affected contract / function
- why it matters
- exploit or failure mode
- whether it is confirmed or conditional

### Trust model

State:

- who controls upgrades
- who controls fees
- who controls pauses or restrictions
- what users must trust offchain

### Token / fee flow

Explain:

- how tokens are created
- where fees accrue
- who can claim them
- what can change later

### Open questions

List anything blocked by missing source, missing ABI, missing deployment info, or offchain dependencies.

## Special guidance

### When reviewing a suspicious token

Be precise:

- "can blacklist holders" is stronger than "looks risky"
- "owner can change tax" is stronger than "may be a scam"
- "no onchain sell restriction found" is stronger than "not a honeypot"

### When reviewing a launch module

Always distinguish:

- launcher logic
- underlying token implementation
- LP locker behavior
- fee locker behavior
- who receives economic rights

### When chain data is required

If the task depends on live state, verify with current chain or explorer data instead of assuming from source alone.

## Do not

- Do not call something malicious without code-based support
- Do not confuse admin centralization with exploitability
- Do not ignore offchain identity dependencies when they control payouts
- Do not stop at contract syntax; trace actual economic outcomes
