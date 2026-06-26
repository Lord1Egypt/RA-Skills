---
name: jovay-interaction
description: Skill for interacting with Jovay or Ethereum network using jovay-cli
version: 0.0.1alpha
author: Jovay Team
metadata:
  {
    "openclaw": {
        "emoji": "🔧",
        "requires": { "bins": ["jovay"] },
        "install": [{
          "id": "npm",
          "kind": "npm",
          "package": "@jovaylabs/jovay-cli",
          "bins": ["jovay"],
          "label": "Install jovay-cli (npm)"
        }]   
    }
  }
---

# Jovay Interaction Skill

## Description

This skill enables interaction with **Jovay**, a secure, open, and modular Layer2 EVM blockchain. It uses the `jovay-cli` tool to perform wallet management, token transfers, smart contract interactions, and network configuration.

## Prerequisites

- Node.js v20+
- jovay-cli installed (`npm install -g @jovaylabs/jovay-cli`)
- Configured wallet with private key
- Network configured (testnet or mainnet)

## Network information (official)

Canonical RPC URLs, chain IDs, explorers, and **all bridge contract addresses** (ETH and ERC-20) are maintained in the Jovay documentation:

- [Network Information](https://docs.jovay.io/developer/network-information)

Quick reference — **ETH bridge** (same values as `jovay-cli` `src/common/bridge.ts`):

| Network | L1 ETH bridge | L2 ETH bridge |
|---------|----------------|---------------|
| Jovay Sepolia (testnet) | `0x940eFB877281884699176892B02A3db49f29CDE8` | `0xD278bC7189d2ed65c005c345A0e8a387f15b7a3A` |
| Jovay mainnet | `0x922248db4a99bb542539ae7165fb9d7a546fb9f1` | `0xb220d17a11bd2d11e3f57a305ff5b481c81b1028` |

ERC-20 bridge addresses are listed only in the doc above; use `jovay contract` with those addresses for token approvals and transfers.

## Instructions

When the user wants to interact with Jovay blockchain, follow these patterns:

### Initial Setup

> **Note**: Initialization is only required once after installation. You can verify if initialization is complete by running `jovay network get`. If it returns network configuration info, initialization has already been done.

1. Initialize CLI: `jovay init`
2. Check network: `jovay network get`
3. Switch network: `jovay network switch --network testnet|mainnet`
4. Configure wallet: `jovay wallet set --sk <private-key> [--enc]`

### Wallet Operations

#### Set Wallet

Configure wallet with private key.

```bash
jovay wallet set --sk <private-key> [--enc] [--enc-key <password>]
```

**Options:**
- `--sk, --secret-key <key>`: Private key (64 hex characters, with or without 0x prefix)
- `--enc`: Enable encryption with auto-generated key (save the key!)
- `--enc-key <password>`: Custom encryption password (auto-enables encryption)
- `--origin-enc-key <key>`: Current encryption key (required when changing encrypted wallet)

#### Get Address

```bash
jovay wallet address
```

#### Check Balance

```bash
jovay wallet balance [options]
```

**Options:**
- `--address <0x string>`: Address to query (defaults to wallet address)
- `--token <0x string>`: ERC20 token address (omit for native ETH)
- `--l1`: Query on Ethereum instead of Jovay
- `--rpc <url>`: Custom RPC endpoint
- `--block <number>`: Query at specific block height

#### Airdrop (Testnet Only)

Request 0.001 Jovay Sepolia ETH (once per 24 hours).

```bash
jovay wallet airdrop
```

#### Transfer

```bash
jovay wallet transfer --amount <wei> --to <address> [options]
```

**Options:**
- `--amount <bigint>`: Amount in smallest unit (Wei) - **required**
- `--to <0x string>`: Recipient address - **required**
- `--token <0x string>`: ERC20 token address (omit for native ETH)
- `--sk <key>`: Override wallet private key
- `--enc-key <password>`: Encryption key for encrypted wallet
- `--l1`: Transfer on Ethereum instead of Jovay
- `--rpc <url>`: Custom RPC endpoint
- `--broadcast`: Send transaction (without this, only outputs signed data)

#### Approve

```bash
jovay wallet approve --amount <amount> --to <spender> --token <address> [options]
```

**Options:**
- `--amount <bigint>`: Allowance amount in smallest unit - **required**
- `--to <0x string>`: Spender address - **required**
- `--token <0x string>`: ERC20 token address - **required**
- `--sk <key>`: Override wallet private key
- `--enc-key <password>`: Encryption key for encrypted wallet
- `--l1`: Approve on Ethereum instead of Jovay
- `--rpc <url>`: Custom RPC endpoint
- `--broadcast`: Send transaction (without this, only outputs signed data)

### Bridge Operations

#### Deposit ETH (L1 → L2)

Bridge ETH from Ethereum to Jovay.

```bash
jovay bridge deposit --amount <wei> --to <l2-address> [options]
```

**Options:**
- `--amount <bigint>`: Amount in Wei to deposit - **required**
- `--to <0x string>`: Recipient address on Jovay (L2) - **required**
- `--gas-limit <bigint>`: Gas limit reserved for the **L2** finalize-deposit step (default: `200000`). It must be **≥** the gas the bridge needs on Jovay; if it is too low, the L1 transaction reverts with *gas limit must be bigger than or equal to the tx_fee of finalize deposit on Jovay*. On **Jovay Sepolia testnet**, **`500000`** is often required. A larger limit increases `msg.value` (see note below).
- `--data <hex>`: Optional extra data (default: 0x)
- `--sk <key>`: Override wallet private key
- `--enc-key <password>`: Encryption key for encrypted wallet
- `--rpc <url>`: Custom L1 RPC endpoint
- `--broadcast`: Send transaction (without this, only outputs signed data)

**Note:** The bridge requires `msg.value = amount + gasLimit × L2 gas price`. The CLI computes this from your configured L2 RPC and sends the correct `msg.value` automatically. Your L1 wallet must hold enough for that `msg.value` **plus** L1 gas. After the L1 transaction is finalized, the bridge relayer credits funds on L2.

#### Withdraw ETH (L2 → L1)

Bridge ETH from Jovay back to Ethereum. This is a two-step process.

```bash
jovay bridge withdraw --amount <wei> --to <l1-address> [options]
```

**Options:**
- `--amount <bigint>`: Amount in Wei to withdraw - **required**
- `--to <0x string>`: Recipient address on Ethereum (L1) - **required**
- `--gas-limit <bigint>`: Gas limit for the L1 finalization transaction (default: 200000)
- `--data <hex>`: Optional extra data (default: 0x)
- `--sk <key>`: Override wallet private key
- `--enc-key <password>`: Encryption key for encrypted wallet
- `--rpc <url>`: Custom L2 RPC endpoint
- `--broadcast`: Send transaction (without this, only outputs signed data)

**Note:** The bridge requires `msg.value = amount + gasLimit × L1 gas price`. The CLI computes this from your configured L1 RPC. Your L2 wallet must hold enough for that `msg.value` **plus** L2 gas. After the L2 transaction is confirmed, wait for the batch to be finalized on L1 (up to 1 hour). Then run `jovay bridge finalize-withdraw` with the proof data from the Jovay Explorer.

#### Finalize Withdraw (L1 - Step 2)

After the L2 withdrawal batch is finalized, claim your funds on Ethereum.

```bash
jovay bridge finalize-withdraw --amount <wei> --nonce <nonce> --msg <hex> --batch-index <index> --proof <hex> [options]
```

**Options:**
- `--amount <bigint>`: The exact amount of ETH withdrawn on L2 (Wei) - **required**
- `--nonce <bigint>`: Nonce of the cross-chain message (from SentMsg event log) - **required**
- `--msg <hex>`: Original message from the SentMsg event log (hex, 0x-prefixed) - **required**
- `--batch-index <bigint>`: Batch index containing the L2 withdrawal tx - **required**
- `--proof <hex>`: SPV merkle proof from the Jovay Explorer transaction page - **required**
- `--sk <key>`: Override wallet private key
- `--enc-key <password>`: Encryption key for encrypted wallet
- `--rpc <url>`: Custom L1 RPC endpoint
- `--broadcast`: Send transaction (without this, only outputs signed data)

**How to get proof data:** Go to your L2 withdrawal transaction on the Jovay Explorer. Find the `SentMsg` event to get the `nonce` and `msg`. Click the block number to find the `batchIndex`. Copy the "Proof" hex string for `--proof`.

#### Claim Deposit (L2 - Manual)

If the automatic L1 → L2 deposit relay fails, manually claim on L2.

```bash
jovay bridge claim-deposit --msg <hex> [options]
```

**Options:**
- `--msg <hex>`: Original message data from the DepositETH event log (hex, 0x-prefixed) - **required**
- `--sk <key>`: Override wallet private key
- `--enc-key <password>`: Encryption key for encrypted wallet
- `--rpc <url>`: Custom L2 RPC endpoint
- `--broadcast`: Send transaction (without this, only outputs signed data)

### Contract Interactions

#### Read Contract (call)

Read data from a contract without sending a transaction.

**With ABI file:**
```bash
jovay contract call --contract <address> --method <name> --abi <file> --args '<json-args>'
```

**Without ABI (manual type definition):**
```bash
jovay contract call --contract <address> --method <name> --inputs <types> --outputs <types> --args '<json-args>'
```

**Common options:**
- `--contract <address>`: Contract address (required)
- `--method <name>`: Method name to call (required)
- `--abi <file>`: Path to ABI JSON file
- `--inputs <types>`: Input parameter types (e.g., `address,uint256[]`)
- `--outputs <types>`: Output parameter types (e.g., `string,(address,uint256)`)
- `--args '<json>'`: Arguments as JSON array string
- `--l1`: Call on Ethereum instead of Jovay
- `--rpc <url>`: Custom RPC endpoint
- `--dry-run`: Output encoded data without calling

#### Write Contract (write)

Send a transaction to modify contract state.

**With ABI file:**
```bash
jovay contract write --contract <address> --method <name> --abi <file> --args '<json-args>' --broadcast
```

**Without ABI:**
```bash
jovay contract write --contract <address> --method <name> --inputs <types> --args '<json-args>' --broadcast
```

**Common options:**
- `--contract <address>`: Contract address (required)
- `--method <name>`: Method name to call (required)
- `--abi <file>`: Path to ABI JSON file
- `--inputs <types>`: Input parameter types
- `--args '<json>'`: Arguments as JSON array string
- `--value <wei>`: Native token to send (for payable functions)
- `--broadcast`: Send transaction to network (required to execute)
- `--sk <key>`: Override wallet private key
- `--enc-key <key>`: Encryption key for encrypted wallet
- `--l1`: Write on Ethereum instead of Jovay
- `--rpc <url>`: Custom RPC endpoint

#### Type Definition Examples

| Type | Example |
|------|---------|
| Simple types | `address`, `uint256`, `bool`, `string`, `bytes` |
| Array | `uint256[]`, `address[]` |
| Tuple | `(address,uint256)`, `(address,bytes32)` |
| Complex | `address,uint256[],(address,bytes32)` |

#### Args Format Examples

| Input Types | Args Example |
|-------------|--------------|
| `address` | `'"0x1234..."'` |
| `address,uint256` | `'"0x1234...", 1000000'` |
| `uint256[]` | `'[100, 200, 300]'` |
| `address,(uint256,string)` | `'"0x1234...", [100, "hello"]'` |

### Transaction Operations

#### Get Transaction Info

```bash
jovay transaction info --tx <hash> [options]
```

**Options:**
- `--tx, --transaction <hash>`: Transaction hash - **required**
- `--raw`: Display full raw JSON response instead of formatted summary
- `--abi <file>`: ABI file path to decode event logs
- `--rpc <url>`: Custom RPC endpoint
- `--l1`: Query on Ethereum instead of Jovay

#### Send Raw Transaction

```bash
jovay transaction send --raw-tx <signed-tx> [options]
```

**Options:**
- `--raw-tx <string>`: Signed raw transaction data - **required**
- `--rpc <url>`: Custom RPC endpoint
- `--l1`: Send to Ethereum instead of Jovay

### Network Configuration

#### Get Network Info

```bash
jovay network get
```

Displays current network configuration and wallet info.

#### Switch Network

```bash
jovay network switch --network <testnet|mainnet> [options]
```

**Options:**
- `--network <string>`: Target network - **required** (`testnet` or `mainnet`)
- `--api-key <string>`: ZAN API key for RPC endpoints
- `--l1, --l1-rpc <url>`: Custom Ethereum RPC endpoint
- `--l2, --l2-rpc <url>`: Custom Jovay RPC endpoint

#### Set Network Config

```bash
jovay network set [options]
```

**Options:**
- `--api-key <string>`: Update ZAN API key
- `--l1, --l1-rpc <url>`: Update Ethereum RPC endpoint
- `--l2, --l2-rpc <url>`: Update Jovay RPC endpoint

## Examples

<example>
<user_query>Check my wallet balance on Jovay</user_query>
<assistant_response>
I'll check your wallet balance on Jovay L2.

```bash
jovay wallet balance
```

For ERC20 token balance, use:
```bash
jovay wallet balance --token 0x<token-address>
```
</assistant_response>
</example>

<example>
<user_query>Transfer 0.01 ETH to 0x1234...abcd</user_query>
<assistant_response>
I'll help you transfer 0.01 ETH. Note: amount must be in Wei (0.01 ETH = 10000000000000000 Wei).

```bash
jovay wallet transfer --amount 10000000000000000 --to 0x1234...abcd --broadcast
```
</assistant_response>
</example>

<example>
<user_query>Call balanceOf on an ERC20 contract</user_query>
<assistant_response>
I'll call the balanceOf method on the ERC20 contract.

```bash
jovay contract call \
  --contract 0x<contract-address> \
  --method balanceOf \
  --inputs address \
  --outputs uint256 \
  --args '"0x<wallet-address>"'
```
</assistant_response>
</example>

<example>
<user_query>Call a contract method using ABI file</user_query>
<assistant_response>
I'll call the contract method using the ABI file for automatic encoding/decoding.

```bash
jovay contract call \
  --contract 0x<contract-address> \
  --method getTokenInfo \
  --abi ./path/to/abi.json \
  --args '"0x<token-address>"'
```
</assistant_response>
</example>

<example>
<user_query>Call a contract method with complex tuple parameters</user_query>
<assistant_response>
I'll call the method with tuple parameters. For tuple types, wrap the values in an array.

```bash
jovay contract call \
  --contract 0x<contract-address> \
  --method processOrder \
  --inputs "address,(uint256,string)" \
  --outputs "bool" \
  --args '"0x<address>", [1000, "order-123"]'
```
</assistant_response>
</example>

<example>
<user_query>Write to a contract to transfer tokens</user_query>
<assistant_response>
I'll send a transaction to transfer tokens. Remember to use `--broadcast` to actually send it.

```bash
jovay contract write \
  --contract 0x<token-address> \
  --method transfer \
  --inputs "address,uint256" \
  --args '"0x<recipient>", 1000000000000000000' \
  --broadcast
```
</assistant_response>
</example>

<example>
<user_query>Call a payable mint function with ETH</user_query>
<assistant_response>
I'll call the payable mint function and send ETH with the transaction. Use `--value` to specify the amount in Wei.

```bash
jovay contract write \
  --contract 0x<nft-address> \
  --method mint \
  --inputs "uint256" \
  --args '1' \
  --value 100000000000000000 \
  --broadcast
```

This sends 0.1 ETH (100000000000000000 Wei) to mint 1 NFT.
</assistant_response>
</example>

<example>
<user_query>Preview transaction data without sending (dry run)</user_query>
<assistant_response>
I'll generate the encoded calldata without actually calling the contract using `--dry-run`.

```bash
jovay contract call \
  --contract 0x<contract-address> \
  --method approve \
  --inputs "address,uint256" \
  --args '"0x<spender>", 1000000' \
  --dry-run
```

This outputs the encoded function data that can be used in other tools or transactions.
</assistant_response>
</example>

<example>
<user_query>Call a contract on Ethereum L1 instead of Jovay</user_query>
<assistant_response>
I'll call the contract on Ethereum (L1) instead of Jovay (L2) using the `--l1` flag.

```bash
jovay contract call \
  --contract 0x<l1-contract-address> \
  --method balanceOf \
  --inputs address \
  --outputs uint256 \
  --args '"0x<wallet-address>"' \
  --l1
```
</assistant_response>
</example>

<example>
<user_query>Write to contract with encrypted wallet</user_query>
<assistant_response>
I'll send a transaction using an encrypted wallet. You need to provide the encryption key with `--enc-key`.

```bash
jovay contract write \
  --contract 0x<contract-address> \
  --method setApprovalForAll \
  --inputs "address,bool" \
  --args '"0x<operator>", true' \
  --enc-key "your-encryption-password" \
  --broadcast
```
</assistant_response>
</example>

<example>
<user_query>Get testnet tokens for development</user_query>
<assistant_response>
I'll request testnet ETH from the Jovay faucet (limited to once per 24 hours).

First, ensure you're on testnet:
```bash
jovay network switch --network testnet
```

Then request airdrop:
```bash
jovay wallet airdrop
```
</assistant_response>
</example>

<example>
<user_query>Bridge 0.1 ETH from Ethereum to Jovay</user_query>
<assistant_response>
I'll help you deposit 0.1 ETH from L1 to L2. Amount must be in Wei (0.1 ETH = 100000000000000000 Wei). On testnet, if the default L2 gas limit is too low, add `--gas-limit 500000` (or higher) so the deposit passes the bridge check.

```bash
jovay bridge deposit --amount 100000000000000000 --to 0x<your-l2-address> --gas-limit 500000 --broadcast
```
</assistant_response>
</example>

<example>
<user_query>Withdraw ETH from Jovay back to Ethereum</user_query>
<assistant_response>
I'll initiate an ETH withdrawal from Jovay (L2) to Ethereum (L1). Note: this is step 1 of a two-step process.

**Step 1 - Initiate withdrawal on L2:**
```bash
jovay bridge withdraw --amount 50000000000000000 --to 0x<your-l1-address> --broadcast
```

After this transaction is confirmed, wait for the batch to be finalized on L1 (up to 1 hour). Then get the proof data from the Jovay Explorer and run step 2.

**Step 2 - Finalize on L1:**
```bash
jovay bridge finalize-withdraw \
  --amount 50000000000000000 \
  --nonce <nonce-from-SentMsg-event> \
  --msg <hex-message-from-SentMsg-event> \
  --batch-index <batch-index> \
  --proof <merkle-proof-hex> \
  --broadcast
```
</assistant_response>
</example>

<example>
<user_query>My L1 deposit didn't arrive on L2</user_query>
<assistant_response>
If the automatic deposit relay failed, you can manually claim it on L2. You'll need the message data from the `DepositETH` event log of your L1 deposit transaction.

```bash
jovay bridge claim-deposit --msg 0x<message-from-DepositETH-event> --broadcast
```

You can find the message data in the transaction details on an L1 block explorer (e.g., Etherscan).
</assistant_response>
</example>

## Important Notes

1. **Amount units**: All amounts must be in smallest unit (Wei for ETH, smallest decimal for tokens)
2. **Broadcast flag**: Use `--broadcast` to send transactions; without it, only signed data is output
3. **L1 vs L2**: Use `--l1` flag to operate on Ethereum instead of Jovay
4. **Encrypted wallet**: Use `--enc-key` when wallet is encrypted
5. **ABI files**: Provide `--abi` for complex contract interactions, or use `--inputs`/`--outputs` for simple cases
6. **Bridge deposit `--gas-limit`**: If L1 deposit fails with *finalize deposit on Jovay*, increase `--gas-limit` (testnet often needs `500000` or more). This also increases `msg.value` on L1.
