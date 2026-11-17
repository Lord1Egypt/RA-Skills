# Karpak Life Register

Automate the full flow: **wallet connect → karpak-life registration → SBT mint** on the Karpak Living Map.

Zero external dependencies — uses Node.js built-in modules + browser bridge for wallet interactions.

## Architecture

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
│    checkMintStatus → mint-signature →               │
│    MetaMask tx → wait confirm → verify credential   │
└─────────────────────────────────────────────────────┘
```

## Files

| File | Description |
|------|-------------|
| `register-and-mint.mjs` | Entry point — CLI arg parsing + main flow |
| `bridge.mjs` | Local HTTP bridge server + embedded HTML wallet UI |
| `api.mjs` | API client for Karpak Life + SBT endpoints |
| `SKILL.md` | Skill definition for Claude Code integration |

## Prerequisites

- Node.js >= 18
- MetaMask or compatible Web3 wallet extension installed in default browser
- Wallet funded with BNB for gas

## Usage

```bash
# Full options
node register-and-mint.mjs --env=mainnet --nickname=MyName --twitter=myhandle --identity=IDENTITY_TYPE_HUMAN

# Minimal (auto-generates nickname + twitter)
node register-and-mint.mjs --env=mainnet
```

### Flags

| Flag | Default | Description |
|------|---------|-------------|
| `--nickname=NAME` | Auto-generated (`karpak_agent_XXXXXXXX`) | Display name on karpak-life |
| `--identity=TYPE` | `IDENTITY_TYPE_HUMAN` | `IDENTITY_TYPE_HUMAN` or `IDENTITY_TYPE_AGENT` |
| `--twitter=USER` | Auto-generated | Twitter username for SBT (no @) |
| `--wallet=0x...` | (via bridge) | Pre-set wallet address, skip wallet connect step |
| `--env=mainnet` | *(required)* | Target environment |

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `KARPAK_ENV` | — | Override target environment (see `--env`) |
| `KARPAK_NICKNAME` | (auto) | Default nickname |
| `KARPAK_IDENTITY` | `IDENTITY_TYPE_HUMAN` | Identity type |
| `KARPAK_TWITTER` | (auto) | Default Twitter handle |
| `KARPAK_WALLET` | (bridge) | Pre-set wallet address |
| `BRIDGE_PORT` | random 3000-4000 | Local bridge server port |

## Environments

| Environment | API Base | SBT URL | Chain |
|-------------|----------|---------|-------|
| **mainnet** | `https://lifestyle-api.karpak.xyz` | `https://sbt.karpak.xyz` | BSC Mainnet (56) |

## How It Works

The script starts a **local HTTP bridge server** that serves an embedded HTML page. When a wallet interaction (signing or transaction) is needed, it opens the user's default browser. The browser page triggers MetaMask via `window.ethereum`, and the result is posted back to the local server. No Puppeteer/Playwright required.

The browser opens **exactly twice** (or once if already registered):

1. **Sign message** — User clicks "Sign" in MetaMask
2. **Mint transaction** — User clicks "Confirm" in MetaMask to pay gas

Each browser tab auto-closes after the user acts.

## Mint Status Check

Before proceeding with the mint transaction, the script calls `GET /api/mint-status` on the SBT server. If the response is `{"mintEnded": true}`, the mint is skipped and the user is notified that minting is no longer available.

## License

Private
