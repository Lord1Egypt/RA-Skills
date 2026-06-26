---
name: security
description: Security for Hyperliquid applications — Solidity vulnerabilities on HyperEVM, API signing security, nonce safety, HYPE/USDC decimal traps, and the pre-deploy checklist.
---

# Security on Hyperliquid

## What You Probably Got Wrong

**"HYPE has 18 decimals so math is the same as ETH."** HYPE has 18 decimals on HyperEVM, but USDC has 6. Mix them up and you're off by 1e12 — sending 1 trillion USDC instead of 1. This is the #1 bug in Hyperliquid dApps.

**"HyperEVM is just like Ethereum security-wise."** Almost. Same reentrancy, same precision loss, same access control issues. But also: Cancun opcodes without blobs, no MEV on HyperCore (so flash loan concerns are different), and HYPE as gas.

**"Signing an API request is always safe."** No. Always verify what you're signing. A malicious UI can get you to sign a different action than what's displayed. Verify the action payload before submitting.

---

## Critical Vulnerabilities (HyperEVM)

### 1. Token Decimal Mismatch

**USDC is 6 decimals. HYPE is 18 decimals.** Getting this wrong transfers absurd amounts.

```solidity
// ❌ WRONG — assumes 18 decimals for USDC
uint256 oneHundredUSDC = 100e18;  // Actually 100 trillion USDC

// ✅ CORRECT — check decimals dynamically
uint256 oneHundredUSDC = 100 * 10 ** IERC20Metadata(usdc).decimals();
// or if you know USDC is 6:
uint256 oneHundredUSDC = 100e6;   // $100 USDC
```

```solidity
// Decimal reference for HyperEVM
// HYPE: 18 decimals (native, like ETH)
// USDC: 6 decimals (always — same as Ethereum)
// WETH: 18 decimals
// HIP-1 tokens: varies (usually 6 or 8) — always check dynamically
```

**When mixing HYPE and USDC in calculations:**
```solidity
// Normalize to same decimal basis first
uint256 usdcNormalized = usdcAmount * 1e12;  // 6 → 18 decimals
uint256 total = hypeAmount + usdcNormalized;   // Now both 18 decimals
```

### 2. Reentrancy

Same as Ethereum. CEI pattern + ReentrancyGuard:

```solidity
import {ReentrancyGuard} from "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

function withdraw(uint256 amount) external nonReentrant {
    uint256 bal = balances[msg.sender];
    require(bal >= amount, "Insufficient balance");

    balances[msg.sender] = bal - amount;  // Effect BEFORE interaction

    (bool success,) = msg.sender.call{value: amount}("");
    require(success, "Transfer failed");
}
```

### 3. Precision Loss

Solidity has no floats. Division truncates.

```solidity
// ❌ WRONG — truncates to 0
uint256 fivePercent = 5 / 100;

// ✅ CORRECT — basis points
uint256 FEE_BPS = 500; // 5%
uint256 fee = (amount * FEE_BPS) / 10_000;

// ✅ ALWAYS multiply before dividing
uint256 result = (a * c) / b;  // Not: a / b * c
```

### 4. SafeERC20

Always use SafeERC20 for token operations:

```solidity
import {SafeERC20, IERC20} from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

using SafeERC20 for IERC20;

// ✅ CORRECT
token.safeTransfer(to, amount);
token.safeTransferFrom(from, to, amount);
token.safeApprove(spender, amount);

// ❌ WRONG — some tokens don't return bool
token.transfer(to, amount);
```

### 5. Oracle Safety

Don't use HyperSwap V2 spot prices as oracles — they can be manipulated in a single block.

For HyperEVM applications that need prices:

```solidity
// ❌ DANGEROUS — manipulable via a single large swap
function getPrice() internal view returns (uint256) {
    (uint112 reserve0, uint112 reserve1,) = hyperSwapPair.getReserves();
    return (reserve1 * 1e18) / reserve0;
}
```

For price data, prefer:
- HyperCore mark prices via the precompile or oracle feeds
- Time-weighted average prices (TWAP) over multiple blocks
- An external oracle if available

### 6. Access Control

Every state-changing function needs explicit access control:

```solidity
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";
import {AccessControl} from "@openzeppelin/contracts/access/AccessControl.sol";

// For simple ownership
contract MyVault is Ownable {
    function setFee(uint256 newFee) external onlyOwner {
        fee = newFee;
    }
}

// For complex roles (admin, operator, keeper)
contract ComplexVault is AccessControl {
    bytes32 public constant OPERATOR_ROLE = keccak256("OPERATOR_ROLE");

    function rebalance() external onlyRole(OPERATOR_ROLE) {
        // Only operators can rebalance
    }
}
```

### 7. HYPE Bridge Security

Interactions with `0x2222222222222222222222222222222222222222`:

```solidity
// Sending HYPE to the bridge address withdraws to HyperCore
// This is a state change — treat it like any external call

// ✅ SAFE pattern
function withdrawToHyperCore(address payable user, uint256 amount) external {
    require(msg.sender == user, "Not authorized");
    require(amount <= userBalances[user], "Insufficient balance");

    userBalances[user] -= amount;  // Update state BEFORE send

    (bool success,) = BRIDGE_ADDRESS.call{value: amount}("");
    require(success, "Bridge transfer failed");

    emit WithdrawnToHyperCore(user, amount);
}
```

---

## HyperCore API Security

### Signing Safety

Every HyperCore exchange action is an EIP-712 signed message. Security rules:

1. **Always verify what you're signing.** The SDK builds the message — review the action parameters before confirming.

2. **Verify nonces are correct.** Wrong nonce = order might be replayed or dropped.

3. **Use agent wallets for bots.** Never sign HyperCore actions with your main key in automated code.

4. **Don't expose signing keys.** Agent keys should have limited withdrawal permissions.

```python
# ✅ CORRECT: Verify order parameters before submitting
def place_safe_order(exchange, coin, is_buy, sz, px):
    # Sanity checks before signing
    assert sz > 0, "Zero size"
    assert px > 0, "Zero price"
    assert coin in APPROVED_COINS, f"Unknown coin: {coin}"
    assert sz <= MAX_ORDER_SIZE, f"Order too large: {sz}"

    # Log what we're about to sign
    print(f"Placing order: {coin} {'BUY' if is_buy else 'SELL'} {sz} @ {px}")

    return exchange.order(coin, is_buy, sz, px,
                          {"limit": {"tif": "Gtc"}})
```

### Nonce Replay Protection

HyperCore nonces protect against replay attacks. But:

- Don't expose your signed messages before submitting — they could be replayed with the same nonce
- Nonces are per-address — a compromised agent key can't replay mainnet nonces on testnet (different chainId in domain)

### Rate Limits and Error Handling

```python
import time
from functools import wraps

def with_retry(max_retries=3, delay=1.0):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    if "rate limit" in str(e).lower() and attempt < max_retries - 1:
                        time.sleep(delay * (2 ** attempt))  # Exponential backoff
                    else:
                        raise
        return wrapper
    return decorator

@with_retry(max_retries=3)
def place_order_with_retry(exchange, coin, is_buy, sz, px):
    return exchange.order(coin, is_buy, sz, px, {"limit": {"tif": "Gtc"}})
```

---

## Pre-Deploy Security Checklist

Run through this for EVERY HyperEVM contract before deploying to production:

### HyperEVM Contracts

- [ ] **Token decimals** — no hardcoded `1e18` for USDC (6 decimals) or unknown tokens
- [ ] **Reentrancy** — CEI pattern + `nonReentrant` on all external-calling functions
- [ ] **Access control** — every admin function has explicit restrictions
- [ ] **SafeERC20** — all token operations use SafeERC20
- [ ] **Integer math** — multiply before divide, no precision loss in critical paths
- [ ] **Input validation** — zero address, zero amount, bounds checks
- [ ] **Events** — every state change emits an event
- [ ] **Oracle safety** — not using DEX spot prices for critical price decisions
- [ ] **HYPE bridge** — bridge calls are safe (CEI, guarded)
- [ ] **No infinite approvals** — approve exact amounts
- [ ] **Contract verified** — verified on https://explorer.hyperliquid.xyz after deploy
- [ ] **Ownership** — production contracts owned by multisig, not EOA

### HyperCore API Integration

- [ ] **Agent wallet** — bot uses agent key, not main wallet key
- [ ] **Key management** — no private keys in code/logs/git
- [ ] **Nonce handling** — using SDK or timestamp-based nonces
- [ ] **Input validation** — position size limits, price sanity checks
- [ ] **Error handling** — rate limits handled with backoff
- [ ] **Testnet tested** — full integration test on testnet before mainnet
- [ ] **Withdrawal limits** — agent wallet can't drain beyond approved amount

---

## HyperEVM-Specific Notes

**Cancun opcodes available:** `TSTORE`, `TLOAD` (transient storage) work on HyperEVM.

**No blobs:** `BLOBHASH`, `BLOBBASEFEE` opcodes are NOT available despite Cancun compatibility. Don't use them.

**Priority fees are burned:** You can't use priority fee manipulation for MEV. Bots don't bid gas wars on HyperEVM like they do on Ethereum.

**Block time ~1-2s:** Contracts relying on block.timestamp should account for faster block production. Minimum deadlines should be longer than 1 block.

```solidity
// ✅ CORRECT: Use timestamps in seconds, not block numbers
// 5 minute deadline
uint256 deadline = block.timestamp + 5 * 60;

// ❌ RISKY: Block number arithmetic depends on block time
// "100 blocks" is only ~100-200 seconds on HyperEVM, not 20 minutes
```

---

## Automated Security Tools

```bash
# Static analysis
slither .                      # Common vulnerability detection
mythril analyze src/MyContract.sol  # Symbolic execution

# Foundry fuzzing
forge test --fuzz-runs 10000   # Fuzz all parameterized tests

# Gas optimization
forge test --gas-report
```

Run slither before any mainnet deployment. No high/medium findings unaddressed.
