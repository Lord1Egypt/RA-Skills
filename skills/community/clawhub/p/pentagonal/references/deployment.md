# Deployment Guide

After Pentagonal compiles your contract, use these commands to deploy.

> **Note:** Pentagonal never handles private keys. It outputs deployment commands for you to execute.

## EVM Deployment

### Using Foundry (cast)

```bash
# Deploy with constructor args
cast send --rpc-url <RPC_URL> \
  --private-key $PRIVATE_KEY \
  --create <BYTECODE> \
  <CONSTRUCTOR_ARGS>

# Or use forge create
forge create --rpc-url <RPC_URL> \
  --private-key $PRIVATE_KEY \
  src/Contract.sol:ContractName \
  --constructor-args <ARGS>
```

### Using Hardhat

```javascript
const Contract = await ethers.getContractFactory("ContractName");
const contract = await Contract.deploy(...constructorArgs);
await contract.waitForDeployment();
console.log("Deployed to:", await contract.getAddress());
```

### Using Remix

1. Open [remix.ethereum.org](https://remix.ethereum.org)
2. Paste the compiled ABI and bytecode
3. Deploy via MetaMask or Injected Provider

## Solana Deployment

### Using Anchor

```bash
anchor build
anchor deploy --provider.cluster mainnet
```

### SPL Token

```bash
spl-token create-token
spl-token create-account <TOKEN_ADDRESS>
spl-token mint <TOKEN_ADDRESS> <AMOUNT>
```

## RPC Endpoints

| Chain | Public RPC |
|-------|-----------|
| Ethereum | `https://eth.llamarpc.com` |
| Polygon | `https://polygon-rpc.com` |
| Base | `https://mainnet.base.org` |
| Arbitrum | `https://arb1.arbitrum.io/rpc` |
| Optimism | `https://mainnet.optimism.io` |
| BSC | `https://bsc-dataseed.binance.org` |
| Solana | `https://api.mainnet-beta.solana.com` |

## Verification

After deployment, verify your contract on the block explorer:

```bash
# Etherscan / Basescan / etc.
forge verify-contract <CONTRACT_ADDRESS> \
  src/Contract.sol:ContractName \
  --chain <CHAIN_ID> \
  --etherscan-api-key <API_KEY>
```
