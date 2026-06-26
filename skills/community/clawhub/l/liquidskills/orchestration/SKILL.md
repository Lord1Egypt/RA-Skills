---
name: orchestration
description: How an AI agent plans, builds, and deploys a complete Hyperliquid application. The three-phase build system for HyperEVM dApps and HyperCore integrations. Use when building any full application on Hyperliquid.
---

# dApp Orchestration on Hyperliquid

## What You Probably Got Wrong

**"I'll just deploy to mainnet immediately."** Never skip testnet. HyperEVM testnet (chain ID 998) and HyperCore testnet API are available. Test there first. Mainnet mistakes cost real HYPE and USDC.

**"I'll handle HyperCore and HyperEVM separately."** Plan both layers from the start. If your app uses HyperEVM contracts AND HyperCore API, coordinate them from day one. Late integration always reveals architectural problems.

**"Secrets in env are fine."** AI agents are the #1 source of leaked credentials. Before committing anything, verify no private keys or API credentials are in the codebase.

---

## The Three-Phase Build System

| Phase | Environment | What Happens |
|-------|-------------|-------------|
| **Phase 1** | Local + testnet | Contracts on testnet, HyperCore testnet API. Iterate fast. |
| **Phase 2** | Mainnet contracts + local UI | Deploy to mainnet. Test with real state. Polish UI. |
| **Phase 3** | Production | Deploy frontend. Final QA. Monitor. |

---

## Phase 1: Build and Test Locally

### 1.1 HyperEVM Contracts

```bash
# Fork HyperEVM mainnet for local testing
anvil --fork-url https://rpc.hyperliquid.xyz/evm --chain-id 999

# Or work against testnet directly
# Chain ID: 998, RPC: https://rpc.hyperliquid-testnet.xyz/evm
```

**Contract development flow:**
1. Write contracts in `src/` (Foundry) or `contracts/` (Hardhat)
2. Write deploy scripts
3. Write tests (≥90% coverage of custom logic)
4. Run security checklist (`security/SKILL.md`)
5. Deploy to testnet

```bash
# Deploy to HyperEVM testnet
forge create src/MyVault.sol:MyVault \
  --rpc-url https://rpc.hyperliquid-testnet.xyz/evm \
  --private-key $PRIVATE_KEY \
  --broadcast

# Run tests
forge test -vvv
forge test --fuzz-runs 1000
```

### 1.2 HyperCore API Integration

**Test against the testnet API, never mainnet:**

```python
# .env
HYPERLIQUID_API_URL=https://api.hyperliquid-testnet.xyz
PRIVATE_KEY=0x...  # Testnet wallet key

# config.py
import os
from hyperliquid.info import Info
from hyperliquid.exchange import Exchange
from hyperliquid.utils import constants
from eth_account import Account

def get_clients():
    wallet = Account.from_key(os.environ['PRIVATE_KEY'])
    api_url = os.environ.get('HYPERLIQUID_API_URL', constants.MAINNET_API_URL)
    return Info(api_url), Exchange(wallet, api_url)
```

```typescript
// TypeScript: environment-based config
const isTestnet = process.env.HYPERLIQUID_TESTNET === 'true';
const client = new HyperliquidClient({ testnet: isTestnet });
```

**Validate Phase 1:**
- [ ] All contract tests pass
- [ ] HyperCore API integration tested on testnet
- [ ] Nonce handling tested (concurrent orders, high frequency)
- [ ] Bridge operations tested (HyperCore ↔ HyperEVM)
- [ ] Error cases handled (rejected orders, insufficient balance, price out of range)

### 1.3 Frontend (Local)

```typescript
// For development, point at testnet
const CHAIN_CONFIG = process.env.NODE_ENV === 'development'
  ? {
      chainId: 998,
      rpcUrl: 'https://rpc.hyperliquid-testnet.xyz/evm',
    }
  : {
      chainId: 999,
      rpcUrl: 'https://rpc.hyperliquid.xyz/evm',
    };
```

**Use ONE loading state per button.** Each button has its own `isLoading` / `isPending` state. Never share.

**Four-state flow (MANDATORY for token interactions):**
1. Not connected → Connect Wallet button
2. Wrong network → Switch to HyperEVM button
3. Needs approval → Approve button
4. Ready → Action button

```typescript
const needsApproval = !allowance || allowance < amount;
const wrongNetwork = chain?.id !== 999; // HyperEVM mainnet
const notConnected = !address;

{notConnected ? (
  <ConnectButton />
) : wrongNetwork ? (
  <button onClick={() => switchChain({ id: 999 })} disabled={isSwitching}>
    {isSwitching ? "Switching..." : "Switch to HyperEVM"}
  </button>
) : needsApproval ? (
  <button onClick={handleApprove} disabled={isApproving}>
    {isApproving ? "Approving..." : "Approve"}
  </button>
) : (
  <button onClick={handleDeposit} disabled={isDepositing}>
    {isDepositing ? "Depositing..." : "Deposit"}
  </button>
)}
```

---

## 🚨 NEVER COMMIT SECRETS TO GIT

Before touching Phase 2 (real mainnet), read this carefully.

**This applies to ALL credentials:**
- Wallet private keys (HyperEVM + HyperCore signing key)
- Agent wallet private keys
- RPC URLs with embedded API keys
- Any API credentials

```bash
# .gitignore MUST include:
.env
.env.*
*.key
*.pem
secrets/
__pycache__/
```

**Pre-commit check:**
```bash
# Check for private keys
grep -rn "0x[a-fA-F0-9]\{64\}" src/ contracts/ --include="*.ts" --include="*.py" --include="*.sol"
# If this matches ANYTHING in source files, STOP. Use environment variables.

# Check for hardcoded RPC keys
grep -rn "alchemyapi.io\|infura.io" src/ contracts/
```

---

## Phase 2: Deploy to Mainnet

### HyperEVM Contract Deployment

```bash
# Deploy to HyperEVM mainnet
forge create src/MyVault.sol:MyVault \
  --rpc-url https://rpc.hyperliquid.xyz/evm \
  --private-key $PRIVATE_KEY \
  --broadcast \
  --verify \
  --verifier blockscout \
  --verifier-url https://explorer.hyperliquid.xyz/api

# Record the deployed address in your config
export CONTRACT_ADDRESS=0x...
```

**Post-deployment checklist:**
- [ ] Contract verified on https://explorer.hyperliquid.xyz
- [ ] Ownership transferred to multisig (not EOA) for production
- [ ] All read functions return expected values
- [ ] Test one small transaction end-to-end
- [ ] Bridge a small amount of HYPE to test the bridge

### HyperCore Integration: Switch to Mainnet

```python
# Switch from testnet to mainnet
import os

# ONLY change the API URL — everything else is the same
API_URL = os.environ.get('HYPERLIQUID_API_URL',
                          'https://api.hyperliquid.xyz')  # Default to mainnet

# Verify you're on the right network before first trade
info = Info(API_URL)
meta = info.meta()
print(f"Connected to: {API_URL}")
print(f"Universe has {len(meta['universe'])} perp markets")
```

**Start with tiny amounts.** First real mainnet test: the smallest allowed order. Verify everything before scaling.

### Frontend Update

```typescript
// Update for production
const wagmiConfig = createConfig({
  chains: [hyperliquid],  // Chain ID 999
  transports: {
    [hyperliquid.id]: http(process.env.NEXT_PUBLIC_HL_RPC_URL || 'https://rpc.hyperliquid.xyz/evm'),
  },
});
```

**Design rule:** Make the UI actually good. No placeholder styling, no LLM-default purple gradients.

---

## Phase 3: Production Deploy

### Pre-Deploy Checklist

- [ ] All testnet tests passing
- [ ] Contracts deployed and verified on mainnet
- [ ] HyperCore integration verified with small real orders
- [ ] No hardcoded testnet values in production code
- [ ] Secrets in environment variables, not in code
- [ ] Agent wallet funded and approved (if using automated trading)

### Frontend Deployment

**Vercel (recommended for Hyperliquid dApps):**
```bash
cd packages/nextjs
vercel --prod
```

**IPFS (decentralized alternative):**
```bash
yarn build
# Upload to IPFS — any IPFS pinning service works
# Set next.config trailingSlash: true for IPFS routing
```

### Production QA

Before going live, fetch `qa/SKILL.md` and give it to a separate reviewer agent.

Key HyperEVM-specific QA items:
- [ ] Chain ID 999 in all mainnet config
- [ ] HYPE shown as gas token everywhere (not ETH)
- [ ] "Switch to HyperEVM" button works (not "Switch to Ethereum")
- [ ] USDC shown as 6 decimals
- [ ] HyperCore/HyperEVM bridge flows tested
- [ ] Block explorer links point to https://explorer.hyperliquid.xyz

---

## Monitoring Post-Launch

### HyperEVM Contract Monitoring

```typescript
// Watch for contract events in real-time
const unwatch = publicClient.watchContractEvent({
  address: contractAddress,
  abi: vaultAbi,
  eventName: 'Deposit',
  onLogs: (logs) => {
    for (const log of logs) {
      console.log(`Deposit: ${log.args.amount} from ${log.args.user}`);
    }
  },
});
```

### HyperCore Position Monitoring

```python
import asyncio
import websockets
import json

# WebSocket for real-time updates
async def monitor_fills(address):
    async with websockets.connect('wss://api.hyperliquid.xyz/ws') as ws:
        # Subscribe to user fills
        await ws.send(json.dumps({
            "method": "subscribe",
            "subscription": {"type": "userFills", "user": address}
        }))

        async for message in ws:
            data = json.loads(message)
            if data.get('channel') == 'userFills':
                for fill in data['data']:
                    print(f"Fill: {fill['coin']} {fill['side']} {fill['sz']} @ {fill['px']}")
```

---

## Key Directories for Foundry + Next.js Projects

```
my-project/
├── src/                          # Solidity contracts
├── script/                       # Deploy scripts
├── test/                         # Foundry tests
├── lib/                          # Dependencies (OpenZeppelin, etc.)
├── foundry.toml                  # Chain configs
├── frontend/
│   ├── app/                      # Pages
│   ├── components/               # React components
│   ├── lib/
│   │   ├── chains.ts             # HyperEVM chain definitions
│   │   ├── wagmi.ts              # wagmi config
│   │   └── hypercore.ts          # HyperCore API helpers
│   └── .env.local                # NEVER COMMIT THIS
└── .gitignore                    # Includes .env*
```
