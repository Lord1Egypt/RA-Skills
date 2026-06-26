---
name: audit
description: Smart contract audit checklist for HyperEVM — covers Solidity security, HyperEVM-specific risks, API signing security, and bonding curve/AMM patterns. Run before every mainnet deployment.
---

# HyperEVM Contract Audit Checklist

Run this before every mainnet deployment. Use a SEPARATE agent that didn't write the code.

---

## HyperEVM-Specific Checks

```
[ ] No blob transactions — HyperEVM uses Cancun without blobs; don't reference blob opcodes
[ ] Priority fees go to zero address — don't design fee logic assuming MEV/tip extraction
[ ] EIP-1559 is enabled — base fee burns are standard; account for this in gas estimates
[ ] Chain ID checks — if using signatures with chainId, verify it's 999 (mainnet) or 998 (testnet)
[ ] HYPE is the native token (18 decimals) — not ETH, not WETH; msg.value is in HYPE wei
[ ] 0x2222...2222 is the HyperCore bridge — never send funds there from a contract unless bridging
[ ] No assumptions about Ethereum L1 finality — this is HyperBFT, not PoS Ethereum
[ ] No ERC-4337 (account abstraction) paymasters exist yet on HyperEVM — don't depend on them
```

## Reentrancy

```
[ ] All external calls follow Checks-Effects-Interactions pattern
[ ] State updated BEFORE making external calls (transfer, call, send)
[ ] ReentrancyGuard used on all functions that move value
[ ] No cross-function reentrancy (func A calls external, func B reads state set by A)
[ ] ERC-1155 safeTransfer callbacks checked — they can reenter
```

```solidity
// ❌ Wrong — external call before state update
function withdraw(uint256 amount) external {
    (bool success,) = msg.sender.call{value: amount}("");
    balances[msg.sender] -= amount; // State updated AFTER call — reentrancy risk
}

// ✅ Correct
function withdraw(uint256 amount) external nonReentrant {
    balances[msg.sender] -= amount; // State updated first
    (bool success,) = msg.sender.call{value: amount}("");
    require(success, "Transfer failed");
}
```

## Integer Arithmetic

```
[ ] No overflow possible (Solidity 0.8+ reverts on overflow by default — verify version)
[ ] Division before multiplication pattern not present (precision loss)
[ ] Correct order: multiply first, divide last
[ ] Rounding direction checked — does it round in favor of user or protocol?
[ ] No precision loss when converting between HYPE wei and token amounts
[ ] Dust amounts handled — what happens with 1 wei operations?
```

```solidity
// ❌ Precision loss
uint256 result = (amount / total) * SCALE;

// ✅ No precision loss
uint256 result = (amount * SCALE) / total;
```

## Access Control

```
[ ] Owner/admin functions protected with onlyOwner or role-based checks
[ ] No functions that should be owner-only are public
[ ] Ownership transfer is two-step (transferOwnership → acceptOwnership), not one-step
[ ] No hardcoded admin addresses — use constructor param or Ownable
[ ] Renounce ownership is intentional if present
[ ] Pause/unpause restricted to authorized addresses only
[ ] Emergency withdraw restricted to owner with timelock or delay
```

## Token Handling (ERC-20 on HyperEVM)

```
[ ] Token decimals NOT assumed to be 18 — always query decimals()
[ ] balanceOf checked before and after external transfers (fee-on-transfer tokens)
[ ] approve() + transferFrom() pattern used (not transfer() for receiving)
[ ] SafeERC20 used for all token interactions (handles non-standard returns)
[ ] Zero-address checks on token parameters
[ ] No transfer to address(0) without intent to burn
```

## Bonding Curve Specific

```
[ ] x*y=k invariant preserved after every trade (or only increases due to fees)
[ ] Buy and sell use consistent reserve values within a single transaction
[ ] Slippage protection: minOut parameter enforced
[ ] Graduation threshold is immutable or protected
[ ] LP burn on graduation is irreversible (send to 0xdead, not address(0))
[ ] Post-graduation: buy/sell disabled or requires different path
[ ] Creator allocation (if any) is vested or delayed — not immediately liquid
[ ] Fee calculation can't round to 0 for small amounts
[ ] Max buy limit per transaction (if any) is enforced in contract, not just UI
```

## AMM / Liquidity Pool

```
[ ] Initial LP seeding uses correct ratio to current price
[ ] LP tokens are burned (not held by a recoverable address)
[ ] Flash loan attacks considered — price manipulation via flash loan
[ ] Sandwich attack exposure evaluated — is TWAP used where needed?
[ ] Minimum liquidity lock in pool (UniV2 style MINIMUM_LIQUIDITY = 1000)
[ ] getAmountOut calculation matches actual swap calculation
```

## Oracle / Price Feed

```
[ ] No spot price used as oracle — use TWAP
[ ] Oracle manipulation window is economically unfeasible
[ ] Stale price protection — check oracle timestamp
[ ] Fallback if oracle fails
```

## Native Value (HYPE) Handling

```
[ ] msg.value checked against expected amount
[ ] Excess HYPE returned to sender if over-payment accepted
[ ] receive() and fallback() functions intentional — don't accidentally accept HYPE
[ ] Contract balance tracked correctly (doesn't double-count)
[ ] No stuck HYPE — every path to receive HYPE has a corresponding path to return/use it
```

```solidity
// Return excess HYPE
function buy(uint256 minTokensOut) external payable {
    uint256 cost = calculateCost(/* ... */);
    require(msg.value >= cost, "Insufficient HYPE");
    
    // Process purchase...
    
    // Return excess
    if (msg.value > cost) {
        (bool success,) = msg.sender.call{value: msg.value - cost}("");
        require(success, "Refund failed");
    }
}
```

## Events

```
[ ] Every state-changing function emits an event
[ ] Events include enough data to reconstruct state offchain
[ ] Indexed parameters on address fields (enables filtering)
[ ] No sensitive data in events (private keys, passwords — obvious but check)
```

## Gas & Limits

```
[ ] No unbounded loops over dynamic arrays
[ ] No array size grows unbounded (would break future calls)
[ ] Storage reads minimized — cache in memory where values reused
[ ] Block gas limit not exceeded by single operation
```

## Upgradability

```
[ ] If non-upgradeable: storage layout change impossible — accept this
[ ] If proxy pattern: storage collision check (EIP-1967 slots used?)
[ ] If upgradeable: initializer called once only (initializer modifier)
[ ] If upgradeable: no constructor logic (use initializer)
[ ] If upgradeable: admin key management documented
```

## Deployment

```
[ ] Constructor arguments verified correct (not testnet addresses in mainnet deploy)
[ ] Contract verified on HyperEVM explorer post-deploy
[ ] Initial state correct after deployment (balances, ownership, paused/unpaused)
[ ] Deploy script is idempotent or has deploy-once protection
[ ] Private key used for deploy rotated or no longer holds deployment funds
```

## Pre-Deploy Final Check

```
[ ] All unit tests pass
[ ] Fuzz tests run with FOUNDRY_FUZZ_RUNS >= 10000
[ ] Invariant tests find no violations
[ ] Manual end-to-end test on testnet (full user flow)
[ ] Contract address in frontend config matches deployed address
[ ] ABI exported from compile output (not copied from old build)
[ ] One person who didn't write it reviewed the critical functions
```
