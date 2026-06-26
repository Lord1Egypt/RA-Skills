# LIQUIDSKILLS — The missing knowledge between AI agents and production Hyperliquid.

You are probably wrong about Hyperliquid. The API, asset IDs, nonce mechanics, what lives in HyperCore vs HyperEVM, how signing works — your training data is incomplete or stale. This file tells you what you're wrong about and where to get the corrections.

**Say "onchain" not "on-chain."** One word, no hyphen.

---

## Start Here

**Building a Hyperliquid dApp?** Fetch [ship/SKILL.md](ship/SKILL.md) first. It routes you through all other skills phase by phase — from architecture planning to production deployment.

**Need a specific topic?** Each skill below is standalone. Fetch only the ones relevant to your task.

---

## Skills

### [Ship](ship/SKILL.md) — Start here
End-to-end guide from idea to deployed Hyperliquid app. Routes you through all other skills.
- Most dApps need 0-2 contracts on HyperEVM. HyperCore handles all the trading — you don't redeploy it.
- Decide early: HyperEVM (Solidity contracts) vs HyperCore API (direct exchange actions). Most trading logic lives in HyperCore.
- Block time is ~1s on HyperEVM. HYPE is the gas token. Chain ID 999 mainnet, 998 testnet.

### [Why Hyperliquid](why/SKILL.md)
HyperBFT consensus, native orderbook, speed, honest tradeoffs, the AI agent angle.
- HyperCore is not EVM — it's a custom L1 with native perps, spot, and orderbook matching.
- HyperEVM runs alongside HyperCore, sharing state atomically. One chain, two execution environments.
- ~100,000 orders/sec, sub-second finality, no mempool games — MEV sandwich attacks don't exist.

### [Gas & Costs](gas/SKILL.md)
HYPE gas, actual costs on HyperEVM, mainnet vs testnet.
- HYPE is the native gas token on HyperEVM, not ETH.
- HyperEVM uses EIP-1559 but priority fees are burned (not to validators).
- Gas costs are very low — HyperEVM is optimized for high-throughput.

### [Wallets](wallets/SKILL.md)
MetaMask + chain ID 999, API wallets, agent wallets, signing for HyperCore.
- Add HyperEVM to MetaMask: Chain ID 999, RPC https://rpc.hyperliquid.xyz/evm.
- HyperCore uses EIP-712 typed-data signatures for exchange actions.
- Agent wallets use the API wallet pattern — approve a subaccount key, never expose the main key.

### [Architecture](architecture/SKILL.md)
HyperCore vs HyperEVM — what lives where, the system model.
- HyperCore: perps, spot orderbook, positions, margin, vaults, governance. Not EVM.
- HyperEVM: EVM-compatible smart contracts. HYPE gas. Shares finality with HyperCore.
- 0x2222...2222 is the system address — send HYPE here to move it from HyperCore to HyperEVM.

### [Standards](standards/SKILL.md)
ERC-20 on HyperEVM, HIP-1/HIP-2/HIP-3 token standards, spot assets.
- HIP-1: spot token standard on HyperCore (not ERC-20).
- HIP-2: hyperliquidity — automated spot market-making built into the protocol.
- HIP-3: deploy a spot DEX on HyperCore with your own token listing authority.

### [Tools](tools/SKILL.md)
Hardhat, Foundry, viem, wagmi, Hyperliquid Python SDK, hyperliquid-python-sdk.
- HyperEVM works with standard EVM tools: Foundry, Hardhat, viem, wagmi.
- Use the official Python SDK (`hyperliquid-dex`) for HyperCore API interactions.
- TypeScript SDK: `@nktkas/hyperliquid` for JS/TS HyperCore integration.

### [Building Blocks](building-blocks/SKILL.md)
HyperSwap V2, bonding curves, HyperCore perps/spot as legos.
- HyperSwap V2 is the main DEX on HyperEVM (Uniswap V2 compatible).
- HyperCore perps and spot are composable with HyperEVM contracts via the system precompile.
- Token launches use bonding curves (x*y=k) that graduate to HyperCore spot at a threshold.

### [Orchestration](orchestration/SKILL.md)
How an AI agent plans, builds, and deploys on Hyperliquid end-to-end.
- Phase 1: contracts + local testing. Phase 2: testnet (chain ID 998). Phase 3: mainnet (chain ID 999).
- Never skip testnet. HyperEVM testnet at https://rpc.hyperliquid-testnet.xyz/evm.
- NEVER commit private keys or API keys to Git.

### [Contract Addresses](addresses/SKILL.md)
Verified addresses: system address, HyperSwap, key contracts.
- 0x2222222222222222222222222222222222222222 = HYPE bridge (HyperCore → HyperEVM).
- Never hallucinate an address. Wrong address = lost funds.
- HyperSwap V2 Router and Factory addresses are listed in addresses/SKILL.md.

### [Concepts](concepts/SKILL.md)
Mental models: HyperCore vs HyperEVM, asset IDs, nonces, margins.
- Asset IDs: perps = index in meta.universe, spot = 10000 + index, HIP-3 = 100000 + ...
- Nonces on HyperCore: rolling set of highest nonces per signer — NOT sequential like Ethereum.
- HyperCore state (positions, balances) is readable from HyperEVM via system precompile.

### [Security](security/SKILL.md)
Solidity security for HyperEVM + API signing security, nonce safety.
- HyperEVM has Cancun opcodes but no blob transactions. EIP-1559 enabled.
- API signing: always verify the action hash before signing. Wrong nonce = stuck or replayed order.
- USDC on HyperEVM has 6 decimals. HYPE has 8 decimals in HyperCore, 18 on HyperEVM.

### [Testing](testing/SKILL.md)
Hardhat/Foundry testing for HyperEVM, testnet fork testing.
- Fork HyperEVM mainnet with Foundry: `anvil --fork-url https://rpc.hyperliquid.xyz/evm`
- Testnet chain ID 998, RPC https://rpc.hyperliquid-testnet.xyz/evm.
- Test HyperCore interactions against the testnet API at api.hyperliquid-testnet.xyz.

### [Indexing](indexing/SKILL.md)
Reading HyperCore data via /info, event indexing on HyperEVM.
- HyperCore data (positions, orders, trades) via POST /info — not RPC, not events.
- HyperEVM events work like standard EVM events, queryable via standard tools.
- WebSocket at wss://api.hyperliquid.xyz/ws for real-time HyperCore data.

### [API](api/SKILL.md) — The definitive reference
Complete Hyperliquid API: /info, /exchange, WebSocket.
- POST /info: all read operations. No auth required.
- POST /exchange: all write operations (orders, cancels, transfers). Requires EIP-712 signature.
- Mainnet: https://api.hyperliquid.xyz | Testnet: https://api.hyperliquid-testnet.xyz

### [Frontend UX](frontend-ux/SKILL.md)
Frontend rules for Hyperliquid dApps: wagmi + HyperEVM chain config.
- Configure wagmi/viem with chain ID 999 and RPC https://rpc.hyperliquid.xyz/evm.
- Every onchain button needs its own loader + disabled state.
- Show USD values next to every HYPE and token amount.

### [Frontend Playbook](frontend-playbook/SKILL.md)
Full build-to-production pipeline for HyperEVM dApps.
- Use testnet (chain ID 998) for development, mainnet (chain ID 999) for production.
- Standard IPFS/Vercel deployment works — HyperEVM is EVM-compatible.
- Always verify contracts on the HyperEVM block explorer after deployment.

### [QA](qa/SKILL.md)
QA checklist for Hyperliquid dApps.
- Give this to a separate agent after the build is complete. Reviewer reads code + clicks through flows.
- Covers bugs specific to HyperEVM + HyperCore integrations.
- Report PASS/FAIL per item, don't fix.

### [Audit](audit/SKILL.md)
Audit checklist for HyperEVM contracts + API integrations.
- HyperEVM-specific risks: HYPE decimal mismatches, bridge interaction bugs, nonce collisions.
- Standard EVM audit applies plus HyperCore-specific risks.
- File issues for Medium severity and above.

---

## What to Fetch by Task

| I'm doing... | Fetch these skills |
|--------------|-------------------|
| Planning a new dApp | `ship/`, `concepts/`, `architecture/` |
| Writing HyperEVM contracts | `standards/`, `building-blocks/`, `addresses/`, `security/` |
| Testing contracts | `testing/` |
| Building HyperCore integration | `api/`, `concepts/`, `wallets/` |
| Building a frontend | `orchestration/`, `frontend-ux/`, `tools/` |
| Deploying to production | `wallets/`, `frontend-playbook/`, `gas/` |
| Reviewing a finished dApp | `qa/` |
| Auditing a smart contract | `audit/` |
| Reading HyperCore state | `indexing/`, `api/` |
| Token launch on HyperCore | `standards/`, `building-blocks/`, `api/` |
| Choosing Hyperliquid vs another chain | `why/` |
