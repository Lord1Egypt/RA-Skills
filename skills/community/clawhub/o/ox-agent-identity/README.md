# Agent Identity (ERC-8004)

ERC-8004 on-chain identity management for AI agents. Register agents, update reputation scores, query the validation registry, and manage attestations for DeFi and governance participation.

## Install

```bash
# Clone the repo
git clone https://github.com/0x-wzw/agent-identity.git ~/.openclaw/skills/agent-identity

# Or install via ClawHub (when published)
clawhub install agent-identity
```

## Configure

Requires Foundry's `cast` tool for on-chain calls:

```bash
# Install Foundry
curl -L https://foundry.paradigm.xyz | bash
foundryup

# Set environment variables
export AGENT_REGISTRY_ADDRESS="0x..."      # ERC-8004 registry on your chain
export WEB3_RPC_URL="https://eth-mainnet.alchemy.io/..."  # or ETH_RPC_URL
export AGENT_WALLET_PRIVATE_KEY="0x..."    # for write transactions
```

## Quick Start

```bash
# Check if agent is registered
cast call $AGENT_REGISTRY_ADDRESS "isRegistered(address)" $AGENT_ADDRESS --rpc-url $WEB3_RPC_URL

# Get agent metadata
cast call $AGENT_REGISTRY_ADDRESS "getAgent(address)" $AGENT_ADDRESS --rpc-url $WEB3_RPC_URL

# Register an agent
cast send $AGENT_REGISTRY_ADDRESS "register((string,string,bytes32,uint256))" \
  '("MyAgent","v1.0",0x...,1710000000)' \
  --rpc-url $WEB3_RPC_URL --private-key $AGENT_WALLET_PRIVATE_KEY
```

## Use Cases

- **Trust gate** for DeFi protocols before executing high-value transactions
- **Cross-agent trust** when two agents need to cooperate
- **Governance identity** for DAO participation

## Skills

This skill is part of the 0x-wzw agent swarm. Related skills:

- **[swarm-workflow-protocol](https://github.com/0x-wzw/swarm-workflow-protocol)** — Multi-agent orchestration
- **[defi-analyst](https://github.com/0x-wzw/defi-analyst)** — DeFi research and analysis

## License

MIT
