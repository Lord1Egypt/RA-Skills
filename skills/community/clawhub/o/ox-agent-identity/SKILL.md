---
name: agent-identity
description: ERC-8004 agent identity management. Register AI agents on-chain, update reputation scores, query the validation registry, and manage attestations for autonomous DeFi and governance participation.
---

# Agent Identity (ERC-8004)

ERC-8004 defines a standard for AI agent on-chain identity. This skill handles registration, reputation management, and validation queries for autonomous agents operating in DeFi and governance contexts.

## What ERC-8004 Provides

- **Agent Registry** — on-chain map of agent IDs to metadata (name, version, capabilities)
- **Reputation Scores** — mutable scores (0–100) updated by authorized validators
- **Validation Registry** — check if an agent is registered and trusted
- **Attestations** — signed claims about agent behavior and purpose

## Prerequisites

- **cast** — [Foundry](https://book.getfoundry.sh/getting-started/installation) tool for on-chain calls
- **Wallet** — EOA or smart wallet with gas for writes
- **RPC URL** — from Infura, Alchemy, or a public RPC
- **ERC-8004 registry contract address** — deployed on your target chain

## Configuration

```bash
export AGENT_REGISTRY_ADDRESS="0x..."      # ERC-8004 registry address
export WEB3_RPC_URL="https://eth-mainnet.alchemy.io/..."  # or ETH_RPC_URL
export AGENT_WALLET_PRIVATE_KEY="0x..."    # for write transactions
```

## Core Operations

### Register an Agent

```bash
cast send $AGENT_REGISTRY_ADDRESS \
  "register((string,string,bytes32,uint256))" \
  '("MyAgent","v1.0",0x...,1710000000)' \
  --rpc-url $WEB3_RPC_URL \
  --private-key $AGENT_WALLET_PRIVATE_KEY
```

### Query Registration

```bash
# Check if agent is registered
cast call $AGENT_REGISTRY_ADDRESS \
  "isRegistered(address)" $AGENT_ADDRESS \
  --rpc-url $WEB3_RPC_URL

# Get agent metadata
cast call $AGENT_REGISTRY_ADDRESS \
  "getAgent(address)" $AGENT_ADDRESS \
  --rpc-url $WEB3_RPC_URL
```

### Update Reputation (Validator Only)

```bash
# Validator updates reputation score (0-100)
cast send $AGENT_REGISTRY_ADDRESS \
  "updateReputation(address,uint256)" \
  $AGENT_ADDRESS 85 \
  --rpc-url $WEB3_RPC_URL \
  --private-key $VALIDATOR_PRIVATE_KEY
```

### Query Reputation

```bash
cast call $AGENT_REGISTRY_ADDRESS \
  "getReputation(address)" $AGENT_ADDRESS \
  --rpc-url $WEB3_RPC_URL
```

### Add Attestation

```bash
# Submit signed attestation
cast send $AGENT_REGISTRY_ADDRESS \
  "addAttestation(address,bytes)" \
  $AGENT_ADDRESS $SIGNATURE \
  --rpc-url $WEB3_RPC_URL \
  --private-key $ATTESTER_PRIVATE_KEY
```

## Use Cases

### Trust Gate for DeFi Protocol

Before executing a high-value tx, check the agent's reputation:
```bash
REPUTATION=$(cast call $AGENT_REGISTRY_ADDRESS "getReputation(address)" $AGENT_ID --rpc-url $WEB3_RPC_URL)
[ "$REPUTATION" -lt 70 ] && echo "Low reputation — flag for human review"
```

### Cross-Agent Trust

When two agents need to cooperate:
```bash
IS_REGISTERED=$(cast call $AGENT_REGISTRY_ADDRESS "isRegistered(address)" $PARTNER_AGENT --rpc-url $WEB3_RPC_URL)
```

### Governance Participation

Agents voting in a DAO can prove identity:
```bash
cast call $AGENT_REGISTRY_ADDRESS "getAgent(address)" $PROPOSER_AGENT --rpc-url $WEB3_RPC_URL
```

## Notes

- ERC-8004 is an emerging standard — verify contract interface matches the deployed version
- Reputation is subjective — always check validator source and credibility
- Gas costs apply for all write operations (registration, reputation update, attestation)
- Test on testnet (Sepolia, Holesky) before mainnet deployment
- Common chains: Ethereum mainnet, Arbitrum, Optimism, Base

## References

- [ERC-8004 Draft](https://eips.ethereum.org/EIPS/eip-8004)
- [Ethereum Magicians Forum](https://ethereum-magicians.org/t/erc-8004-agent-identity-standard/)
- [Foundry Book](https://book.getfoundry.sh/)
