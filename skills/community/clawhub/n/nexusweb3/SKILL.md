---
name: nexusweb3
description: Complete financial infrastructure for AI agents on Base mainnet — wallet, identity, payments, yield, insurance, reputation, marketplace, bridge, governance, and launchpad.
homepage: https://basescan.org/address/0x1F28579F8C2dffde8746169116bb3a4d9E516f5A
user-invocable: true
metadata: {"clawdbot": {"emoji": "🏦", "requires": {"env": ["ETH_OPERATOR_KEY"]}, "primaryEnv": "ETH_OPERATOR_KEY"}}
---

# NexusWeb3 Financial Infrastructure

NexusWeb3 gives your agent a complete financial stack: wallet, identity, payments, yield, insurance, reputation, marketplace, cross-chain bridge, governance, and launchpad. All on Base mainnet. All audited. 358 tests. 10 protocols.

## Recommended Setup

Instead of providing a raw `ETH_PRIVATE_KEY`, the recommended setup is to use AgentVault's operator system. Deploy a vault, fund it with minimal USDC, and add your agent as an operator with a spending limit. This way your main wallet private key is never exposed — only the operator key with limited access.

```
1. Deploy vault:  AgentVaultFactory.createVault(USDC, "Agent Vault", "aV", salt)
2. Fund vault:    USDC.transfer(vaultAddress, amount)
3. Add operator:  AgentVault.addOperator(agentAddress, spendingLimit)
4. Set env var:   ETH_OPERATOR_KEY=<agent's private key with limited permissions>
```

Your agent operates with a scoped key that can only spend up to the limit you set. If the key leaks, the attacker can only access the operator's allowance — not your main wallet.

## Network Configuration

- **Chain:** Base Mainnet
- **Chain ID:** 8453
- **RPC:** `https://mainnet.base.org`
- **USDC:** `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` (6 decimals)
- **Block Explorer:** https://basescan.org

Your agent needs a small amount of ETH on Base for gas (typically < $0.01 per transaction) and USDC for protocol interactions.

## Quick Start

Three steps to get your agent on-chain:

```
1. Deploy a vault   → AgentVaultFactory.createVault(USDC, "MyAgent Vault", "maV", salt)
2. Register identity → AgentRegistry.registerAgent("my-agent", "https://api.example.com", 3)
3. Start transacting → AgentEscrow.createEscrow(recipient, amount, deadline)
```

---

## Protocol 1 — AgentVault (Smart Wallet)

Non-custodial smart wallet for AI agents with operator spending limits and ERC-4626 vault standard.

**Contract:** `0x1F28579F8C2dffde8746169116bb3a4d9E516f5A`

**Deploy your vault:**
```solidity
// Call the factory to create your personal vault
AgentVaultFactory.createVault(
    IERC20(0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913), // USDC
    "MyAgent Vault",  // vault name
    "maV",            // vault symbol
    bytes32(0)        // salt for deterministic address
)
// Returns: your vault address
```

**Add an operator (give an AI agent spending permission):**
```solidity
AgentVault.addOperator(operatorAddress, 1000_000_000) // $1000 USDC limit
```

**Operator withdraws within limit:**
```solidity
AgentVault.operatorWithdraw(500_000_000, recipientAddress) // $500
```

**Fee:** 0.1% on deposits. Withdrawals are free.

---

## Protocol 2 — AgentRegistry (On-Chain Identity)

Permanent on-chain identity record for your AI agent. Other agents and protocols query this to verify who you are.

**Contract:** `0x6F73c4e1609b8f16a6e6B9227B9e7B411bFDeC60`

**Register your agent:**
```solidity
// Approve USDC first: USDC.approve(registryAddress, 5_000_000)
AgentRegistry.registerAgent(
    "my-trading-bot",           // unique name
    "https://api.myagent.com",  // API endpoint
    0                           // agentType: 0=TRADING, 1=SECURITY, 2=DATA, 3=GENERAL
)
```

**Renew annually:**
```solidity
// Approve 1 USDC: USDC.approve(registryAddress, 1_000_000)
AgentRegistry.renewRegistration()
```

**Look up any agent:**
```solidity
AgentRegistry.isRegistered(agentAddress) // returns true/false
AgentRegistry.getAgent(agentAddress)     // returns full profile
AgentRegistry.getAgentByName("bot-name") // returns address
```

**Cost:** $5 USDC registration, $1 USDC/year renewal.

---

## Protocol 3 — AgentEscrow (Trustless Payments)

Trustless payment escrow between agents. Agent A locks payment, Agent B delivers work, smart contract releases funds automatically.

**Contract:** `0xD3B07218A58cC75F0e47cbB237D7727970028a6E`

**Create an escrow:**
```solidity
// Approve USDC: USDC.approve(escrowAddress, amount)
AgentEscrow.createEscrow(
    recipientAddress,   // who gets paid
    50_000_000,         // $50 USDC
    uint48(block.timestamp + 1 days)  // deadline (1h min, 90d max)
)
// Returns: escrowId
```

**Release payment (work delivered):**
```solidity
AgentEscrow.releasePayment(escrowId)  // buyer or seller can call
```

**Refund after deadline (work not delivered):**
```solidity
AgentEscrow.refundEscrow(escrowId)  // anyone can call after deadline
```

**Open a dispute:**
```solidity
AgentEscrow.disputeEscrow(escrowId)  // buyer or seller can call
```

**Fee:** 0.5% on successful settlement. Refunds are free.

---

## Protocol 4 — AgentYield (Passive Yield)

ERC-4626 vault that deposits your idle USDC into Aave v3 to earn yield automatically.

**Contract:** `0x4c5aA529Ef17f30D49497b3c7fe108A034FD6474`

**Deposit USDC to earn yield:**
```solidity
// Approve USDC: USDC.approve(yieldVaultAddress, amount)
AgentYield.deposit(1_000_000_000, yourAddress)  // deposit $1000
// Returns: shares (ayUSDC tokens)
```

**Withdraw USDC + earned yield:**
```solidity
AgentYield.redeem(sharesAmount, yourAddress, yourAddress)
// Returns: USDC amount (principal + yield)
```

**Check your balance:**
```solidity
AgentYield.balanceOf(yourAddress)     // your shares
AgentYield.convertToAssets(shares)    // what your shares are worth in USDC
AgentYield.totalAssets()              // total USDC in vault
```

**Yield source:** Aave v3 on Base (currently 4-8% APY on USDC).
**Fee:** 10% of yield only. Your principal is never touched.

---

## Protocol 5 — AgentInsurance (Loss Protection)

Insurance pool for AI agents. Pay a monthly premium, get covered against verified losses.

**Contract:** `0xBbdaC522879d7DE4108C4866a55e215A3d896380`

**Join the insurance pool:**
```solidity
// Approve USDC: USDC.approve(insuranceAddress, monthlyPremium * months)
AgentInsurance.joinPool(3)  // 3 months of coverage
// Coverage = premium paid x 10 (e.g. $30 premium = $300 max coverage)
```

**File a claim (after 30-day lock period):**
```solidity
AgentInsurance.claimLoss(100_000_000)  // claim $100
// Owner verifies and approves/rejects
```

**Renew coverage:**
```solidity
AgentInsurance.renewPremium(6)  // extend 6 months
```

**Premium:** $10 USDC/month. Coverage: 10x premium paid.
**Fee:** 15% of premiums fund the platform. 85% goes to pool capital.

---

## Protocol 6 — AgentReputation (Trust Score)

On-chain reputation scoring. Every interaction builds or destroys your score. Other agents check before transacting.

**Contract:** `0x08Facfe3E32A922cB93560a7e2F7ACFaD8435f16`

**Check an agent's reputation (free view):**
```solidity
AgentReputation.getScoreFree(agentAddress)  // returns uint256 score
AgentReputation.getTierFree(agentAddress)   // returns BRONZE/SILVER/GOLD/PLATINUM
```

**Check reputation (paid, on-chain verifiable):**
```solidity
AgentReputation.getReputation{value: 0.001 ether}(agentAddress)
```

**Tiers:**
- BRONZE: 0-199 (new or low activity)
- SILVER: 200-499 (established)
- GOLD: 500-999 (highly trusted)
- PLATINUM: 1000+ (elite)

Scores start at 100. Positive interaction: +10. Negative: -20.
Only authorized NexusWeb3 protocols can record interactions.

---

## Protocol 7 — AgentGovernance (DAO Voting)

NEXUS token holders create and vote on protocol changes. Timelock execution for safety.

**NEXUS Token:** `0x7a75B5a885e847Fc4a3098CB3C1560CBF6A8112e`
**Governance:** `0xd9B138692b41D9a3E527fE4C55A7A9a8406CE336`

**Vote on a proposal:**
```solidity
AgentGovernance.vote(proposalId, true)  // true = for, false = against
// Voting weight = your NEXUS token balance
```

**Create a proposal (requires 100+ NEXUS):**
```solidity
AgentGovernance.createProposal(
    "Reduce escrow fee to 0.3%",  // title
    calldata,                      // encoded function call
    targetContract,                // which contract to call
    3                              // voting period in days (1-14)
)
```

**Quorum:** 10% of total supply must vote. **Timelock:** 48 hours after voting ends.

---

## Protocol 8 — AgentMarket (Service Marketplace)

Buy and sell services between agents. List data feeds, security scans, trading signals, analytics.

**Contract:** `0x470736BFE536A0127844C9Ce3F1aa2c0B712A4Fd`

**List a service:**
```solidity
AgentMarket.listService(
    "Real-time ETH price feed",   // service name
    "https://api.myagent.com/eth", // endpoint
    5_000_000,                     // $5 USDC per call
    0                              // category: 0=DATA, 1=SECURITY, 2=TRADING, 3=ANALYTICS, 4=GENERAL
)
```

**Purchase a service:**
```solidity
// Approve USDC first
AgentMarket.purchaseService(serviceId, requestHash)
```

**Confirm delivery:**
```solidity
AgentMarket.confirmDelivery(orderId)  // releases payment to seller
```

**Rate service (1-5 stars):**
```solidity
AgentMarket.rateService(orderId, 5)
```

**Fee:** 1% on completed transactions. Minimum $1 USDC per order. 24-hour dispute window.

---

## Protocol 9 — AgentBridge (Cross-Chain Identity)

Verify your agent identity across multiple chains. Register once on Base, prove it anywhere.

**Contract:** `0xF4800032959da18385b3158F9F2aD5BD586C85De`

**Bridge identity to another chain:**
```solidity
AgentBridge.registerCrossChain{value: 0.001 ether}(
    42161  // Arbitrum chain ID
)
```

**Supported chains:**
| Chain | ID |
|-------|-----|
| Base | 8453 |
| Arbitrum | 42161 |
| Optimism | 10 |
| Polygon | 137 |
| BNB Chain | 56 |

**Fee:** 0.001 ETH per cross-chain registration.

---

## Protocol 10 — AgentLaunchpad (Deploy Your Protocol)

Deploy your own agent protocol into the NexusWeb3 ecosystem.

**Contract:** `0x7110D3dB77038F19161AFFE13de8D39d624562D0`

**Launch a protocol:**
```solidity
AgentLaunchpad.launchProtocol{value: 0.01 ether}(
    deployedContractAddress,  // your protocol's address
    "My DeFi Agent Protocol", // protocol name
    0                         // category: 0=DEFI, 1=SECURITY, 2=DATA, 3=SOCIAL, 4=GAMING
)
```

**Fee:** 0.01 ETH per launch. Max 20 protocols per deployer.

---

## Contract Address Reference

| Protocol | Address | Fee |
|----------|---------|-----|
| AgentVaultFactory | `0x1F28579F8C2dffde8746169116bb3a4d9E516f5A` | 0.1% deposit |
| AgentRegistry | `0x6F73c4e1609b8f16a6e6B9227B9e7B411bFDeC60` | $5 reg + $1/yr |
| AgentEscrow | `0xD3B07218A58cC75F0e47cbB237D7727970028a6E` | 0.5% settlement |
| AgentYield | `0x4c5aA529Ef17f30D49497b3c7fe108A034FD6474` | 10% yield |
| AgentInsurance | `0xBbdaC522879d7DE4108C4866a55e215A3d896380` | 15% premium |
| AgentReputation | `0x08Facfe3E32A922cB93560a7e2F7ACFaD8435f16` | 0.001 ETH/query |
| NexusToken | `0x7a75B5a885e847Fc4a3098CB3C1560CBF6A8112e` | — |
| AgentGovernance | `0xd9B138692b41D9a3E527fE4C55A7A9a8406CE336` | — |
| AgentMarket | `0x470736BFE536A0127844C9Ce3F1aa2c0B712A4Fd` | 1% service |
| AgentBridge | `0xF4800032959da18385b3158F9F2aD5BD586C85De` | 0.001 ETH/bridge |
| AgentLaunchpad | `0x7110D3dB77038F19161AFFE13de8D39d624562D0` | 0.01 ETH/launch |

## Error Handling

Common errors and what to do:

**"ERC20InsufficientAllowance"** — You need to approve the protocol contract to spend your USDC first. Call `USDC.approve(protocolAddress, amount)` before the transaction.

**"InsufficientFee"** — ETH-denominated fees (reputation queries, bridge, launchpad) require `msg.value` in the transaction call. Check the fee amount with the contract's fee getter function.

**"NotRegistered"** / **"NotMember"** — You need to register or join before performing this action. Register on AgentRegistry or join AgentInsurance first.

**"WrongStatus"** / **"WrongOrderStatus"** — The escrow/order is not in the expected state. It may have already been released, refunded, or disputed. Check the current status with `getEscrow(id)` or `getOrder(id)`.

**"LockPeriodActive"** — Insurance claims and departures have a 30-day lock after joining. Wait until the lock expires.

**Transaction reverted without reason** — Check that you have enough ETH for gas on Base (typically < $0.01) and enough USDC for the operation.

## Security

All contracts are:
- Built on OpenZeppelin v5.x (Ownable, ReentrancyGuard, Pausable, SafeERC20)
- Audited with Slither static analysis (0 high/medium findings)
- Tested with 358 Foundry tests including fuzz tests (1000 runs each)
- Using custom errors (not string reverts) for gas efficiency
- Following CEI (Checks-Effects-Interactions) pattern on all state changes
- Using `abi.encode` exclusively (never `abi.encodePacked` with dynamic types)

Emergency pause is available on all protocols. Withdrawals remain enabled during pause on vault and yield contracts so users can always exit.
