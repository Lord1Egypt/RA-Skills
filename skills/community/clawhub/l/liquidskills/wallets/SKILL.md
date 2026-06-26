---
name: wallets
description: Wallets on Hyperliquid — MetaMask + chain ID 999 setup, HyperCore API wallets, agent wallet patterns, EIP-712 signing for exchange actions. Essential for any agent that needs to interact with Hyperliquid.
---

# Wallets on Hyperliquid

## What You Probably Got Wrong

**"I can use my Ethereum wallet directly."** For HyperEVM: yes, same wallet, add the chain. For HyperCore: the API uses EIP-712 typed data signatures — you need to understand the signing scheme, not just connect MetaMask.

**"Private key = full access."** For automated agents, use the API wallet pattern — approve a subaccount agent key with limited permissions. The agent key can trade but can't withdraw beyond the approved limit. Main wallet stays cold.

**"Any nonce works."** HyperCore nonces are NOT sequential. They use a rolling-set scheme — you can use any nonce that's greater than the lowest in your recent 20 nonces. This is fundamentally different from Ethereum. Getting this wrong means rejected orders.

---

## HyperEVM: Adding to MetaMask

Add HyperEVM to any EVM-compatible wallet:

| Parameter | Mainnet | Testnet |
|-----------|---------|---------|
| **Chain ID** | 999 | 998 |
| **RPC URL** | https://rpc.hyperliquid.xyz/evm | https://rpc.hyperliquid-testnet.xyz/evm |
| **Chain Name** | HyperEVM | HyperEVM Testnet |
| **Currency Symbol** | HYPE | HYPE |
| **Block Explorer** | https://explorer.hyperliquid.xyz | https://explorer-testnet.hyperliquid.xyz |

```typescript
// Programmatically add to MetaMask
await window.ethereum.request({
  method: 'wallet_addEthereumChain',
  params: [{
    chainId: '0x3E7',  // 999 in hex
    chainName: 'HyperEVM',
    nativeCurrency: { name: 'HYPE', symbol: 'HYPE', decimals: 18 },
    rpcUrls: ['https://rpc.hyperliquid.xyz/evm'],
    blockExplorerUrls: ['https://explorer.hyperliquid.xyz'],
  }],
});
```

**Same address as Ethereum.** Your Ethereum address works on HyperEVM. Same private key, same address, different chain.

---

## HyperCore: How Signing Works

HyperCore uses **EIP-712 typed data** signatures for all exchange actions. This is NOT a standard EVM transaction — it's a signed message that the HyperCore API validates.

### The Signing Flow

```
1. Build the action payload (order, cancel, transfer, etc.)
2. Hash it with EIP-712 (domain + struct hash)
3. Sign with your private key (standard eth_signTypedData_v4)
4. POST to /exchange with { action, nonce, signature, vaultAddress? }
```

### Domain Separator for HyperCore

```typescript
const domain = {
  name: 'Exchange',
  version: '1',
  chainId: 1337,           // HyperCore always uses chainId 1337 for signing
  verifyingContract: '0x0000000000000000000000000000000000000000',
};
```

**Critical:** The chainId for EIP-712 signing in HyperCore is ALWAYS 1337 — regardless of whether you're on mainnet or testnet. This is NOT the HyperEVM chain ID (999/998).

---

## API Wallet Pattern (For Agents)

**Never use your main wallet private key in an automated bot.** Use the API wallet pattern:

### Step 1: Create an Agent Wallet

Generate a new private key. This is your agent key — it will have limited permissions.

```python
from eth_account import Account

# Generate a new random private key for the agent
agent_key = Account.create()
print(f"Agent address: {agent_key.address}")
print(f"Agent key: {agent_key.key.hex()}")
```

### Step 2: Approve the Agent Wallet

The main wallet approves the agent key via the API:

```python
from hyperliquid.exchange import Exchange
from hyperliquid.utils import constants

# Using the main wallet
exchange = Exchange(main_wallet, constants.MAINNET_API_URL)

# Approve agent key to trade on behalf of main wallet
result = exchange.approve_agent(
    agent_address=agent_key.address,
    agent_name="MyTradingBot"
)
```

### Step 3: Agent Uses Its Own Key

The agent wallet submits orders independently, signing with its own key:

```python
# Agent trades using its own key, but against main wallet's account
agent_exchange = Exchange(
    agent_key,
    constants.MAINNET_API_URL,
    account_address=main_wallet.address  # Trading on behalf of main wallet
)

# Place order
order_result = agent_exchange.order(
    "ETH",
    is_buy=True,
    sz=0.1,
    limit_px=2000.0,
    order_type={"limit": {"tif": "Gtc"}}
)
```

**Benefits:**
- Agent key can be compromised without losing your main wallet funds
- Set withdrawal limits: agent can't drain beyond a threshold
- Revoke agent access anytime from main wallet
- Different agents for different strategies

---

## Nonce Management on HyperCore

HyperCore nonces are NOT sequential like Ethereum. They use a **rolling-set scheme**.

**How it works:**
- Each signer has a set of "recent nonces" (the 20 highest nonces seen)
- Any new nonce must be greater than the LOWEST nonce in the set
- Once the set has 20 entries, the lowest is evicted as new ones are added
- This allows batching and out-of-order submission within a window

**Practical implications:**

```python
# ✅ CORRECT: Use timestamp-based nonces (milliseconds since epoch)
import time
nonce = int(time.time() * 1000)  # milliseconds — always increasing

# ✅ CORRECT: The SDK handles nonces automatically
# hyperliquid-python-sdk manages nonce generation internally

# ❌ WRONG: Don't manually track sequential nonces
nonce = last_nonce + 1  # This breaks with concurrent requests
```

**The recommended approach:** Use the official SDK — it handles nonce generation (typically millisecond timestamps) correctly.

---

## 🚨 NEVER COMMIT SECRETS TO GIT

This applies to Hyperliquid exactly as it does to Ethereum. Bots scrape GitHub in real-time.

**Things that must NEVER be committed:**
- Main wallet private keys
- Agent wallet private keys
- API credentials

```bash
# .gitignore MUST include:
.env
.env.*
*.key
*.pem
secrets/
```

```python
# ✅ Load from environment
import os
from eth_account import Account

private_key = os.environ['HYPERLIQUID_PRIVATE_KEY']
wallet = Account.from_key(private_key)

# ❌ NEVER hardcode
private_key = "0xdeadbeef..."  # DON'T DO THIS
```

**If you leaked a key:**
1. Assume it's compromised immediately
2. Move all funds to a new wallet NOW
3. Revoke agent approvals from the compromised wallet
4. Rotate to new keys
5. Clean git history (but the key is already burned)

---

## CRITICAL Guardrails for AI Agents

1. **NEVER use main wallet for automated trading.** Use agent wallet pattern.
2. **NEVER store private keys in chat logs, code, or version control.**
3. **NEVER move funds without human confirmation** for amounts above threshold.
4. **Always verify the action before signing.** Check the order params, size, price.
5. **Use a dedicated wallet with limited funds** for agent operations.
6. **Set withdrawal limits** on agent wallets via the API.
7. **Log all transactions** (never log keys).
8. **Test on testnet first.** Use api.hyperliquid-testnet.xyz.
9. **Implement position size limits.** Require human approval above threshold.
10. **Monitor for anomalies.** Alert if agent places orders outside expected parameters.

---

## Multisig for HyperEVM

For HyperEVM contracts holding significant value, use a multisig:

- Safe (Gnosis Safe) works on HyperEVM — it's EVM-compatible
- For contract ownership, use a multisig not a single EOA
- HyperCore doesn't have native multisig but you can control HyperCore accounts from a HyperEVM multisig via custom contract logic

---

## Wallet Libraries

**TypeScript/JavaScript:**
```typescript
import { createWalletClient, http, privateKeyToAccount } from 'viem';
import { hyperliquid } from './chains';

const account = privateKeyToAccount(process.env.PRIVATE_KEY as `0x${string}`);
const client = createWalletClient({
  account,
  chain: hyperliquid,
  transport: http('https://rpc.hyperliquid.xyz/evm'),
});
```

**Python:**
```python
from eth_account import Account
from hyperliquid.exchange import Exchange
from hyperliquid.utils import constants

wallet = Account.from_key(os.environ['PRIVATE_KEY'])
exchange = Exchange(wallet, constants.MAINNET_API_URL)
info = exchange.info  # Read-only info client
```
