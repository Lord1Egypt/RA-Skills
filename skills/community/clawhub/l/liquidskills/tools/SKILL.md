---
name: tools
description: Development tools for Hyperliquid — Foundry, Hardhat, viem, wagmi for HyperEVM; Python SDK and TypeScript SDK for HyperCore API. What works, what to use, how to set up.
---

# Hyperliquid Development Tools

## What You Probably Got Wrong

**"I need special tools for Hyperliquid."** For HyperEVM, standard EVM tools work unchanged. Foundry, Hardhat, viem, wagmi, Remix — all work. Just point them at the right RPC and chain ID.

**"The Python SDK is optional."** If you're interacting with HyperCore (trading, positions, HIP-1 tokens), use the official SDK. Rolling your own API calls with manual EIP-712 signing is error-prone and unsupported.

**"ethers.js is fine."** It works, but viem is preferred for new projects — smaller, better TypeScript, more explicit about what it's doing.

---

## HyperEVM Tools (Standard EVM Tooling)

### Foundry (Recommended for Contracts)

Foundry works with HyperEVM unchanged. Point it at the right RPC:

```bash
# Install Foundry
curl -L https://foundry.paradigm.xyz | bash
foundryup

# Initialize a project
forge init my-project
cd my-project

# Deploy to HyperEVM testnet
forge create src/MyContract.sol:MyContract \
  --rpc-url https://rpc.hyperliquid-testnet.xyz/evm \
  --private-key $PRIVATE_KEY \
  --broadcast

# Deploy to HyperEVM mainnet
forge create src/MyContract.sol:MyContract \
  --rpc-url https://rpc.hyperliquid.xyz/evm \
  --private-key $PRIVATE_KEY \
  --broadcast

# Verify contract (Blockscout)
forge verify-contract <ADDRESS> src/MyContract.sol:MyContract \
  --verifier blockscout \
  --verifier-url https://explorer.hyperliquid.xyz/api
```

**foundry.toml for HyperEVM:**
```toml
[profile.default]
src = "src"
out = "out"
libs = ["lib"]

[rpc_endpoints]
hyperliquid = "https://rpc.hyperliquid.xyz/evm"
hyperliquid_testnet = "https://rpc.hyperliquid-testnet.xyz/evm"

[etherscan]
hyperliquid = { key = "empty", chain = 999, url = "https://explorer.hyperliquid.xyz/api" }
hyperliquid_testnet = { key = "empty", chain = 998, url = "https://explorer-testnet.hyperliquid.xyz/api" }
```

### Hardhat (Alternative)

```javascript
// hardhat.config.ts
import { HardhatUserConfig } from "hardhat/config";

const config: HardhatUserConfig = {
  solidity: "0.8.24",
  networks: {
    hyperliquid: {
      url: "https://rpc.hyperliquid.xyz/evm",
      chainId: 999,
      accounts: [process.env.PRIVATE_KEY!],
    },
    hyperliquidTestnet: {
      url: "https://rpc.hyperliquid-testnet.xyz/evm",
      chainId: 998,
      accounts: [process.env.PRIVATE_KEY!],
    },
  },
};

export default config;
```

### viem (Recommended for Frontend/Scripts)

```typescript
import { createPublicClient, createWalletClient, http } from 'viem';
import { privateKeyToAccount } from 'viem/accounts';
import { defineChain } from 'viem';

// Define HyperEVM chain
const hyperliquid = defineChain({
  id: 999,
  name: 'HyperEVM',
  nativeCurrency: { name: 'HYPE', symbol: 'HYPE', decimals: 18 },
  rpcUrls: {
    default: { http: ['https://rpc.hyperliquid.xyz/evm'] },
  },
  blockExplorers: {
    default: { name: 'Explorer', url: 'https://explorer.hyperliquid.xyz' },
  },
});

// Public client (reads)
const publicClient = createPublicClient({
  chain: hyperliquid,
  transport: http(),
});

// Wallet client (writes)
const account = privateKeyToAccount(process.env.PRIVATE_KEY as `0x${string}`);
const walletClient = createWalletClient({
  account,
  chain: hyperliquid,
  transport: http(),
});

// Read a contract
const balance = await publicClient.readContract({
  address: tokenAddress,
  abi: erc20Abi,
  functionName: 'balanceOf',
  args: [userAddress],
});

// Write a contract
const txHash = await walletClient.writeContract({
  address: tokenAddress,
  abi: erc20Abi,
  functionName: 'transfer',
  args: [recipient, amount],
});
```

### wagmi (React Frontend)

```typescript
// wagmi config for HyperEVM
import { createConfig, http } from 'wagmi';
import { defineChain } from 'viem';
import { injected, walletConnect } from 'wagmi/connectors';

const hyperliquid = defineChain({
  id: 999,
  name: 'HyperEVM',
  nativeCurrency: { name: 'HYPE', symbol: 'HYPE', decimals: 18 },
  rpcUrls: {
    default: { http: ['https://rpc.hyperliquid.xyz/evm'] },
  },
});

export const wagmiConfig = createConfig({
  chains: [hyperliquid],
  connectors: [
    injected(),
    walletConnect({ projectId: process.env.NEXT_PUBLIC_WC_PROJECT_ID! }),
  ],
  transports: {
    [hyperliquid.id]: http('https://rpc.hyperliquid.xyz/evm'),
  },
});
```

### Remix IDE

Works with HyperEVM via Injected Provider (MetaMask) or by adding a custom RPC in the Remix environment. No special configuration needed beyond having MetaMask on chain 999.

---

## HyperCore SDK Tools

### Python SDK (Official)

```bash
pip install hyperliquid-dex
```

```python
from hyperliquid.info import Info
from hyperliquid.exchange import Exchange
from hyperliquid.utils import constants
from eth_account import Account
import os

# Setup
wallet = Account.from_key(os.environ['PRIVATE_KEY'])
info = Info(constants.MAINNET_API_URL)
exchange = Exchange(wallet, constants.MAINNET_API_URL)

# Read operations (no signing needed)
user_state = info.user_state(wallet.address)
positions = user_state['assetPositions']

# Get orderbook
book = info.l2_snapshot("ETH")

# Place an order (requires signing)
order_result = exchange.order(
    "ETH",
    is_buy=True,
    sz=0.1,
    limit_px=2000.0,
    order_type={"limit": {"tif": "Gtc"}}
)

# Cancel an order
cancel_result = exchange.cancel("ETH", order_id=12345)
```

**SDK GitHub:** https://github.com/hyperliquid-dex/hyperliquid-python-sdk

### TypeScript SDK

```bash
npm install @nktkas/hyperliquid
```

```typescript
import { HyperliquidClient } from '@nktkas/hyperliquid';
import { privateKeyToAccount } from 'viem/accounts';

// Info (read-only, no signing)
const client = new HyperliquidClient({ testnet: false });

// Get market info
const meta = await client.info.perpetuals.getMetaAndAssetCtxs();

// Get user state
const state = await client.info.perpetuals.getClearinghouseState({
  user: '0x...',
});

// Exchange (requires wallet for signing)
const account = privateKeyToAccount(process.env.PRIVATE_KEY as `0x${string}`);
const exchangeClient = new HyperliquidClient({ account, testnet: false });

// Place order
const result = await exchangeClient.exchange.placeOrder({
  orders: [{
    a: 1,           // asset index (ETH perp)
    b: true,        // is buy
    p: '2000',      // price
    s: '0.1',       // size
    r: false,       // reduce only
    t: { limit: { tif: 'Gtc' } },
  }],
  grouping: 'na',
});
```

**SDK GitHub:** https://github.com/nktkas/hyperliquid

---

## Choosing Your Stack (2026)

| Need | Tool |
|------|------|
| HyperEVM contract development | **Foundry** (forge + cast + anvil) |
| HyperEVM frontend (React) | **wagmi + viem** |
| HyperCore API (Python) | **hyperliquid-dex** (official SDK) |
| HyperCore API (TypeScript) | **@nktkas/hyperliquid** |
| Quick contract interaction | **cast** (CLI) or Remix |
| Fork testing HyperEVM | **anvil --fork-url https://rpc.hyperliquid.xyz/evm** |
| Contract verification | **forge verify-contract** (Blockscout) |

---

## Essential cast Commands for HyperEVM

```bash
# Check balance
cast balance 0xYourAddress --rpc-url https://rpc.hyperliquid.xyz/evm

# Read contract
cast call 0xContractAddr "balanceOf(address)(uint256)" 0xWallet \
  --rpc-url https://rpc.hyperliquid.xyz/evm

# Send transaction
cast send 0xContractAddr "transfer(address,uint256)" 0xTo 1000000 \
  --private-key $PRIVATE_KEY \
  --rpc-url https://rpc.hyperliquid.xyz/evm

# Gas price
cast gas-price --rpc-url https://rpc.hyperliquid.xyz/evm

# Chain ID
cast chain-id --rpc-url https://rpc.hyperliquid.xyz/evm
# → 999

# Fork mainnet locally
anvil --fork-url https://rpc.hyperliquid.xyz/evm
```

---

## Block Explorers

| Network | Explorer |
|---------|----------|
| HyperEVM Mainnet | https://explorer.hyperliquid.xyz |
| HyperEVM Testnet | https://explorer-testnet.hyperliquid.xyz |

Both explorers are Blockscout-based. Use Blockscout APIs for programmatic explorer access.

---

## Testing Setup

```bash
# Fork HyperEVM mainnet for local testing
anvil --fork-url https://rpc.hyperliquid.xyz/evm --chain-id 999

# Fork at specific block (reproducible tests)
anvil --fork-url https://rpc.hyperliquid.xyz/evm --fork-block-number 1234567

# Run Foundry tests against fork
forge test --fork-url https://rpc.hyperliquid.xyz/evm
```

For HyperCore API testing, always use the testnet:
```
Testnet API: https://api.hyperliquid-testnet.xyz
Testnet RPC: https://rpc.hyperliquid-testnet.xyz/evm
Testnet Chain ID: 998
```

---

## What Changed / What's Current (2026)

- **Foundry is the default** for HyperEVM contract development
- **viem preferred over ethers.js** for new TypeScript projects
- **hyperliquid-dex** is the official Python SDK (pip install hyperliquid-dex)
- **@nktkas/hyperliquid** is the community TypeScript SDK with good maintenance
- **Blockscout** is the block explorer for HyperEVM (not Etherscan)
