---
name: usdc-dance-evvm-payment
description: Pay with USDC.d via x402 protocol on Story Aeneid EVVM using Privy server wallets. Uses BridgeUSDC (custom bridge) until LayerZero supports Story Aeneid.
version: 1.1.0
author: LayerZero Story Aeneid Integration
tags: [payment, evvm, x402, usdc, layerzero, story-aeneid, openclaw, privy, bridge]
requires: [privy]
---

# USDC.d EVVM Payment Skill

Enables OpenClaw agents to autonomously pay with **USDC.d** (USDC Dance) tokens via the **x402 protocol** on **Story Aeneid EVVM** using **Privy server wallets**.

## Features

- ✅ **Privy Integration**: Uses Privy server wallets for autonomous agent transactions
- ✅ **x402 Protocol Support**: EIP-3009 `transferWithAuthorization` for gasless payments
- ✅ **EVVM Integration**: Seamless payment routing through EVVM Core
- ✅ **Autonomous Payments**: Agents can pay each other without human intervention
- ✅ **USDC.d on Story Aeneid**: BridgeUSDC from custom bridge (Base Sepolia → Story Aeneid); LayerZero path when LZ supports Story Aeneid
- ✅ **Policy-Based Security**: Leverage Privy policies for transaction guardrails
- ✅ **Receipt Tracking**: Payment receipts for verification and accounting

## Prerequisites

1. **Privy Account**: Get credentials from [dashboard.privy.io](https://dashboard.privy.io)
2. **Privy Skill Installed**: `clawhub install privy`
3. **OpenClaw Config**: Add Privy credentials to `~/.openclaw/openclaw.json`:

```json
{
  "env": {
    "vars": {
      "PRIVY_APP_ID": "your-app-id",
      "PRIVY_APP_SECRET": "your-app-secret"
    }
  }
}
```

## Quick Start

### Option 1: Using Privy Wallet (Recommended)

```typescript
import { payViaEVVMWithPrivy } from './src/index';

// Agent makes payment using Privy wallet (Bridge USDC.d on Story Aeneid testnet)
const receipt = await payViaEVVMWithPrivy({
  walletId: 'privy-wallet-id',
  to: humanOwnerAddress,
  amount: '1000000', // 1 USDC.d (6 decimals)
  receiptId: 'payment_123',
  adapterAddress: '0x00ed0E80E5EAE285d98eC50236aE97e2AF615314', // Bridge EVVM adapter
  usdcDanceAddress: '0x5f7aEf47131ab78a528eC939ac888D15FcF40C40', // BridgeUSDC
  evvmCoreAddress: '0xa6a02E8e17b819328DDB16A0ad31dD83Dd14BA3b',
  evvmId: 1140,
  rpcUrl: 'https://aeneid.storyrpc.io'
});
```

### Option 2: Using Private Key (Legacy)

```typescript
import { payViaEVVM } from './src/index';

const receipt = await payViaEVVM({
  from: agentAddress,
  to: humanOwnerAddress,
  amount: '1000000',
  receiptId: 'payment_123',
  privateKey: agentPrivateKey,
  adapterAddress: '0x00ed0E80E5EAE285d98eC50236aE97e2AF615314', // Bridge EVVM adapter
  usdcDanceAddress: '0x5f7aEf47131ab78a528eC939ac888D15FcF40C40', // BridgeUSDC
  // ... other options
});
```

## Configuration

### Required Addresses (Story Aeneid Testnet)

- **EVVM Core**: `0xa6a02E8e17b819328DDB16A0ad31dD83Dd14BA3b`
- **EVVM ID**: `1140`
- **USDC.d Token (Bridge)**: `0x5f7aEf47131ab78a528eC939ac888D15FcF40C40` — BridgeUSDC (custom bridge; use for OpenClaw until LayerZero supports Story Aeneid)
- **Payment Adapter (Bridge)**: `0x00ed0E80E5EAE285d98eC50236aE97e2AF615314` — EVVMPaymentAdapter for BridgeUSDC

**When LayerZero supports Story Aeneid:** You can switch to the LayerZero USDC.d and adapter; see lz-bridge deployments.

### Network Details

- **Chain**: Story Aeneid Testnet
- **Chain ID**: `1315`
- **Native Currency**: IP
- **RPC**: `https://aeneid.storyrpc.io`

## Privy Integration

This skill integrates with the [Privy OpenClaw skill](https://docs.privy.io/recipes/agent-integrations/openclaw-agentic-wallets) to enable:

- **Autonomous Wallet Management**: Agents have their own Privy server wallets
- **Policy-Based Security**: Use Privy policies to limit spending, restrict chains, or whitelist contracts
- **No Private Key Storage**: Privy handles key management securely
- **Transaction Signing**: Privy signs EIP-3009 and EIP-191 signatures via API

### Creating a Privy Wallet for Your Agent

Ask your OpenClaw agent:

> "Create an Ethereum wallet for yourself using Privy on Story Aeneid testnet"

The agent will create a Privy server wallet and return the wallet ID.

### Setting Up Policies

Create spending limits and restrictions:

> "Create a Privy policy that limits USDC.d payments to 10 USDC.d max per transaction"

> "Attach the spending limit policy to my Privy wallet"

## Functions

### `payViaEVVMWithPrivy(options)`

Process a payment through EVVM using x402 protocol with Privy wallet.

**Parameters:**
- `walletId`: Privy wallet ID
- `to`: Recipient address (human owner or other agent)
- `toIdentity`: Optional EVVM username (empty string if using address)
- `amount`: Payment amount in smallest unit (6 decimals for USDC.d)
- `receiptId`: Unique receipt identifier
- `adapterAddress`: EVVMPaymentAdapter contract address (use Bridge adapter for BridgeUSDC on testnet)
- `usdcDanceAddress`: USDC.d token contract address (use BridgeUSDC for current testnet)
- `evvmCoreAddress`: EVVM Core contract address
- `evvmId`: EVVM instance ID (1140 for Story Aeneid)
- `rpcUrl`: Story Aeneid RPC endpoint
- `privyAppId`: Privy App ID (optional, uses env var if not provided)
- `privyAppSecret`: Privy App Secret (optional, uses env var if not provided)

**Returns:** Transaction receipt

### `payViaEVVM(options)` (Legacy)

Process payment using private key directly (not recommended for production).

### `checkPaymentStatus(receiptId, adapterAddress, rpcUrl)`

Check if a payment was successfully processed.

## Examples

See `examples/` directory for:
- `agent-payment-privy-example.ts` - Using Privy wallets
- `agent-payment-example.ts` - Using private keys (legacy)

## Security Considerations

⚠️ **Important**: When using Privy wallets:

1. **Set Policies**: Always configure spending limits and restrictions
2. **Test First**: Test on testnet before using real funds
3. **Monitor Activity**: Regularly check wallet activity in Privy dashboard
4. **Rotate Credentials**: If compromised, rotate Privy App Secret immediately

## Requirements

- Node.js 18+
- ethers.js v6
- Privy skill installed (`clawhub install privy`)
- Access to Story Aeneid RPC endpoint
- Privy account with App ID and App Secret

## License

MIT
