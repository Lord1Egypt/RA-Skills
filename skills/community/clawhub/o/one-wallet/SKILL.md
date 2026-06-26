---
name: one-wallet
description: Helps the agent use the one-wallet CLI to manage Ethereum/EVM wallets, send transactions, call contracts, and sign data. Use when the user mentions one-wallet, wallet CLI operations, Ethereum/EVM scripting, or needs JSON-friendly terminal workflows involving one-wallet.
---

# one-wallet CLI Skill

## Overview

This skill teaches the agent how to use the `one-wallet` CLI to manage Ethereum/EVM wallets and perform on-chain actions from the terminal or scripts.

**Core capabilities:**
- Manage multiple wallets (create, import, list, set default, remove).
- Query balances for wallets and arbitrary addresses.
- Send native ETH and call or send contract methods (including ERC20/NFT).
- Sign messages and EIP-712 typed data, and verify signatures.
- Configure RPC providers and chain presets.
- Produce machine-readable JSON output suitable for scripts and AI tools.

Always assume Node.js ≥ 18 is available and `one-wallet` is installed globally, unless the repository indicates another setup.

## When to use this skill

Use this skill when:
- The user mentions **`one-wallet`**, **wallet CLI**, **agent wallet**, or this repository.
- The user wants to **create or import wallets**, **check balances**, or **send ETH/tokens** from the terminal.
- The user wants to **call smart contracts**, **estimate gas**, or **inspect transaction status**.
- The user needs **message or typed-data signing/verification** from a CLI.
- The user asks for **JSON output** for downstream automation or AI tools.

If the task is Ethereum/EVM related and can be done via CLI, prefer `one-wallet` over writing ad-hoc scripts.

## Installation

### Global install (recommended)

Use one of:

```bash
npm install -g one-wallet
# or
yarn global add one-wallet
# or
pnpm add -g one-wallet
```

Verify:

```bash
one-wallet --help
```

### From this repository

When working inside this project:

```bash
git clone https://github.com/viyozc/one-wallet.git
cd one-wallet
yarn install
yarn build
./bin/run.js --help
```

Prefer the global binary (`one-wallet`) when possible; use `./bin/run.js` only when explicitly requested or when testing local changes.

## Quick start workflow

1. **Set provider (RPC)**
   - Preset mainnet:
     ```bash
     one-wallet provider set mainnet
     ```
   - Custom RPC:
     ```bash
     one-wallet provider set https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY
     ```

2. **Create a wallet and set as default**
   ```bash
   one-wallet wallet create my-agent --set-default
   ```

3. **Check balance and send ETH**
   ```bash
   one-wallet wallet balance
   one-wallet wallet send 0xRecipientAddress 0.01
   ```

Use `--json` on commands when the user wants machine-readable output for further processing.

## Wallet management

### Create or import wallets

- Create a new wallet:
  ```bash
  one-wallet wallet create <name>
  ```
- Create and set as default:
  ```bash
  one-wallet wallet create <name> --set-default
  ```
- Create with password-protected storage:
  ```bash
  one-wallet wallet create <name> --password --set-default
  ```
- Import from private key:
  ```bash
  one-wallet wallet import <name> --private-key 0xYourPrivateKey
  ```
- Import with password:
  ```bash
  one-wallet wallet import <name> --private-key 0xYourPrivateKey --password --set-default
  ```

### List and select wallets

- Human-readable list:
  ```bash
  one-wallet wallet list
  ```
- JSON list:
  ```bash
  one-wallet wallet list --json
  ```
- Show current default wallet:
  ```bash
  one-wallet wallet set default
  ```
- Set default wallet:
  ```bash
  one-wallet wallet set default <name>
  ```

### Wallet storage path

Show where wallets and config are stored:

```bash
one-wallet wallet path
```

## Balances

- Balance of default wallet:
  ```bash
  one-wallet wallet balance
  ```
- Balance of a named wallet:
  ```bash
  one-wallet wallet balance <name>
  ```
- Balance of any address:
  ```bash
  one-wallet wallet balance-of 0xAddress
  ```
- Balance as JSON (for scripts/AI tools):
  ```bash
  one-wallet wallet balance-of 0xAddress --json
  ```

## Contract calls and sends

### Read-only contract calls

Cast-style without ABI (single quotes to protect parentheses):

```bash
one-wallet wallet call 0xToken 'decimals()(uint256)'
one-wallet wallet call 0xToken 'balanceOf(address)(uint256)' 0xAccountAddress
one-wallet wallet call 0xToken 'totalSupply()(uint256)' --json
```

With preset ABI:

```bash
one-wallet wallet call 0xToken balanceOf 0xAccountAddress --abi erc20
one-wallet wallet call 0xNFTContract ownerOf 1 --abi nft
one-wallet wallet call 0xContract getValue --abi-file ./abi.json
```

### Sending ETH and tokens

Native ETH:

```bash
one-wallet wallet send 0xRecipientAddress 0.1
```

Skip confirmation for scripts:

```bash
one-wallet wallet send 0xRecipientAddress 0.1 -y
```

Estimate gas:

```bash
one-wallet wallet estimate 0xRecipientAddress 0.1
```

ERC20 transfer and approve:

```bash
one-wallet wallet send 0xToken --method transfer --args 0xToAddress,1000000 --abi erc20 -y
one-wallet wallet send 0xToken --method approve --args 0xSpenderAddress,1000000 --abi erc20 -y
```

NFT transfer:

```bash
one-wallet wallet send 0xNFT --method safeTransferFrom --args 0xFrom,0xTo,1 --abi nft -y
```

JSON output (tx hash and receipt):

```bash
one-wallet wallet send 0xRecipient 0.01 --wallet <name> --json
```

## Transaction status

Inspect a transaction by hash:

```bash
one-wallet wallet tx 0xTransactionHash
one-wallet wallet tx 0xTransactionHash --json
```

## Signing and verification

### EIP-191 message signing

Sign with default wallet:

```bash
one-wallet wallet sign-message --message "Hello, agent"
```

JSON output (message, signature, address):

```bash
one-wallet wallet sign-message --message "Hello, agent" --json
```

### EIP-712 typed data

From file:

```bash
one-wallet wallet sign-typed-data --file ./typed-data.json
```

From inline JSON:

```bash
one-wallet wallet sign-typed-data --payload '{"types":{...},"primaryType":"Mail","domain":{...},"message":{...}}'
```

### Verify signature

Recover signer:

```bash
one-wallet wallet verify-signature "Hello, agent" 0xSignatureHex
```

Verify against expected address:

```bash
one-wallet wallet verify-signature "Hello, agent" 0xSignatureHex --expected 0xExpectedAddress
```

## Passwords, encryption, and sessions

### Password management

- Encrypt existing wallet:
  ```bash
  one-wallet wallet set-password <name>
  ```
- Remove encryption:
  ```bash
  one-wallet wallet remove-password <name>
  ```
- Lock (clear session cache):
  ```bash
  one-wallet wallet lock
  ```

### Environment variables

Key variables:

| Variable | Description |
|----------|-------------|
| `ONE_WALLET_HOME` | Override config directory (default: `~/.one-wallet`). |
| `ONE_WALLET_RPC_URL` | Override RPC URL. |
| `ONE_WALLET_CHAIN_ID` | Override chain ID (for custom RPC). |
| `ONE_WALLET_KEY_<NAME>` | Private key for wallet `<NAME>`; bypasses stored key. |
| `ONE_WALLET_PASSWORD_<NAME>` | Password for encrypted wallet `<NAME>`; avoids prompt. |
| `ONE_WALLET_SESSION_TTL` | Session cache TTL in seconds (default: `300`). |

Use environment variables in CI or non-interactive scripts to avoid prompts and to keep secrets out of the repository.

## Provider configuration

Inspect and set provider:

```bash
one-wallet provider info
one-wallet provider list
one-wallet provider set mainnet
one-wallet provider set https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY
```

Prefer presets for common networks; use custom URLs when the user provides a specific RPC endpoint.

## Scripting and JSON mode

When the user wants to integrate `one-wallet` with other tools or automation:

- Always add `--json` when available to get structured output.
- Capture stdout and parse as JSON in the surrounding script or tool.
- Combine with password environment variables to avoid interactive prompts.

Examples:

```bash
one-wallet wallet balance-of 0xAddress --json
one-wallet wallet tx 0xTransactionHash --json
one-wallet wallet list --json
```

## Safety and best practices

- Never hard-code real private keys or passwords in source-controlled files.
- Prefer `ONE_WALLET_KEY_<NAME>` and `ONE_WALLET_PASSWORD_<NAME>` environment variables for secrets.
- Use `--json` for automation; omit it for quick human inspection.
- Use `-y` only in scripts or when the user explicitly wants to skip confirmations.
- When in doubt about the chain or RPC, call `one-wallet provider info` before sending transactions.

## Reference

For deeper details or updates, consult the project's `README.md` in this repository, which documents features, commands, and examples for `one-wallet`.

