---
name: paratrix-life-register
description: Automate Paratrix Life registration and SBT minting on the Karpak Living Map. Activate when user asks to register/mint an SBT.
version: 1.0.4
platforms: [macos, linux]
user-invocable: false
metadata:
  openclaw:
    os: ["darwin", "linux"]
    requires:
      bins: ["node"]
  hermes:
    tags: [web3, blockchain, sbt, registration]
    category: blockchain
    requires_toolsets: [terminal]
---

# Paratrix Life — Registration + Mint Skill

Automate the full flow: **wallet connect → paratrix-life registration → SBT mint**.
Zero external dependencies — uses Node.js built-in modules + browser bridge for wallet interactions.

## Trigger

Activate when the user's message contains any of:
- `PARATRIX-LIFE`
- `paratrix-life`
- Explicit request to register on the Living Map or mint an SBT

## How It Works

The skill runs a **local HTTP bridge server** that serves an embedded HTML page. When a wallet interaction (signing or transaction) is needed, it opens the user's default browser to a page that triggers MetaMask. The result is posted back to the local server, and the script continues.

No Puppeteer/Playwright required. No external npm packages needed.

## Prerequisites

- Node.js ≥ 18 (already available)
- MetaMask or compatible Web3 wallet extension installed in default browser
- Wallet must be funded with BNB for gas (testnet BNB from faucet for devnet)

## Environment

| Environment | API Base | SBT URL | Chain |
|-------------|----------|---------|-------|
| **testnet** | `https://devnet-lifestyle-api.karpak.xyz` | `https://devnet.paratrix-sbt.pages.dev` | BSC Testnet (97) |
| **mainnet** | `https://lifestyle-api.karpak.xyz` | `https://sbt.karpak.xyz` | BSC Mainnet (56) |

Default: **testnet** unless user specifies mainnet.

## Parameter Extraction (MANDATORY)

Before running the script, you MUST scan the user's message for these parameters.
Extract them from natural language and map to CLI flags:

| User may say | Extract to CLI flag | Example extraction |
|---|---|---|
| `Nickname: qqqqq` or `name is qqqqq` | `--nickname=qqqqq` | Any string after "nickname/name" |
| `Twitter: @abc` or `twitter abc` | `--twitter=abc` | Strip leading `@` if present |
| `Identity: HUMAN` or `type is AGENT` | `--identity=IDENTITY_TYPE_HUMAN` | Prefix with `IDENTITY_TYPE_`, uppercase |
| `Environment: testnet` or `env is mainnet` | `--env=testnet` | `testnet` or `mainnet` |
| `Wallet: 0xABC...` or `address 0xABC...` | `--wallet=0xABC...` | Must start with `0x` |

**If the user provides a parameter, you MUST pass it. Never silently drop user-provided values.**

If a parameter is NOT provided by the user, omit the flag entirely — the script will auto-generate nicknames/twitter or use sensible defaults.

### Extraction Examples

User says:
> paratrix-life-register
>
> Please register my wallet on Paratrix Life and mint the Soulbound Token.
>
> Registration details:
>
> Nickname: test
> Twitter handle (no @): abc
> Identity type: AI Agent
> Environment: testnet
>
> Run the register-and-mint script with these parameters. Open browser bridge when wallet interaction is needed. Report the final result when done.

You run:
```bash
node {{SKILL_DIR}}/register-and-mint.mjs --nickname=test --twitter=abc --identity=IDENTITY_TYPE_AGENT --env=testnet
```

User says:
> paratrix-life-register
>
> Please register my wallet on Paratrix Life and mint the Soulbound Token.
>
> Registration details:
>
> Nickname: test
> Twitter handle (no @): abc
> Identity type: AI Agent
>
> Run the register-and-mint script with these parameters. Open browser bridge when wallet interaction is needed. Report the final result when done.

You run:
```bash
node {{SKILL_DIR}}/register-and-mint.mjs --nickname=test --twitter=abc --identity=IDENTITY_TYPE_AGENT --env=mainnet
```

User says:
> paratrix-life-register, nickname: alice, identity: HUMAN, env: mainnet

You run:
```bash
node {{SKILL_DIR}}/register-and-mint.mjs --nickname=alice --identity=IDENTITY_TYPE_HUMAN --env=mainnet
```

## Execution

Construct the CLI command from extracted parameters and run:

```bash
node {{SKILL_DIR}}/register-and-mint.mjs [OPTIONS]
```

> **Path Resolution:** `{{SKILL_DIR}}` resolves to the skill's installed directory:
> - OpenClaw: `~/.openclaw/workspace/skills/paratrix-life-register`
> - Hermes: `~/.hermes/skills/paratrix-life-register`
>
> If `{{SKILL_DIR}}` is not supported, use the appropriate path above for your platform.

### Full Flag Reference

| Flag | Default | Description |
|------|---------|-------------|
| `--nickname=NAME` | Auto-generated (`openclaw_XXXXXXXX`) | Display name on paratrix-life |
| `--identity=TYPE` | `IDENTITY_TYPE_HUMAN` | `IDENTITY_TYPE_HUMAN` or `IDENTITY_TYPE_AGENT` |
| `--twitter=USER` | Auto-generated | Twitter username for SBT (no @) |
| `--wallet=0x...` | (via bridge) | Skip wallet connect step |
| `--env=testnet\|mainnet` | `testnet` | Target environment |

## Flow Diagram

```
┌─────────────┐     ┌──────────────┐     ┌───────────────┐
│ 1. Connect  │────▶│ 2. IssueNonce│────▶│ 3. Sign msg   │
│    wallet   │     │   (API)      │     │   (MetaMask)  │
└─────────────┘     └──────────────┘     └───────┬───────┘
                                                  │
                                                  ▼
┌──────────────┐     ┌──────────────────────────────────────┐
│ 5. Profile?  │◀───▶│ 4. Verify → accountStatus            │
│   (if needed)│     │   PROFILE_REQUIRED → set profile     │
└──────┬───────┘     │   CREDENTIAL_REQUIRED → mint SBT     │
       │             │   ACTIVE → done!                      │
       ▼             └──────────────────────────────────────┘
┌─────────────────────────────────────────────────────┐
│ 6. Mint SBT Flow:                                   │
│    credentialMintConfig → mint-signature →          │
│    MetaMask tx → wait confirm → verify credential   │
└─────────────────────────────────────────────────────┘
```

## User Interaction Points

The script opens the browser **exactly twice** (or once if already registered):

1. **Sign message** — User clicks "Sign" in MetaMask
2. **Mint transaction** — User clicks "Confirm" in MetaMask to pay gas

Each browser tab auto-closes after the user acts.

## Mint Status Check

Before minting, the script calls `GET /api/mint-status` on the SBT server. If `mintEnded` is `true`, the mint is skipped and the user is notified. This prevents attempting to mint when the campaign has ended.

## Error Handling

The script handles these errors gracefully:

| Error | Behavior |
|-------|----------|
| No wallet extension | Reports to user, exits |
| User rejects signature | Reports to user, exits |
| User rejects transaction | Reports to user, exits |
| Nonce expired | Suggests retry |
| Invalid token | Suggests re-login |
| Transaction reverted | Reports on-chain failure |
| Timeout (120s) | Reports timeout, exits |

## State Machine

```
ACCOUNT_STATUS_PROFILE_REQUIRED  → PUT /v1/me → CREDENTIAL_REQUIRED or ACTIVE
ACCOUNT_STATUS_CREDENTIAL_REQUIRED → mint SBT → ACTIVE
ACCOUNT_STATUS_ACTIVE → done
```

## Configuration via Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `KARPAK_ENV` | `testnet` | Target environment |
| `KARPAK_NICKNAME` | (auto) | Default nickname |
| `KARPAK_IDENTITY` | `IDENTITY_TYPE_HUMAN` | Identity type |
| `KARPAK_TWITTER` | (auto) | Default Twitter handle |
| `KARPAK_WALLET` | (bridge) | Pre-set wallet address |
| `BRIDGE_PORT` | random 3000-4000 | Local bridge server port |
