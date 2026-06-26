---
name: predictclaw
description: Predict.fun skill with a PolyClaw-style CLI for markets, wallet funding, trading, positions, and hedging.
metadata: {"openclaw":{"emoji":"🔮","homepage":"https://predict.fun","requires":{"bins":["uv","erc-mandated-mcp"],"env":["PREDICT_ENV","PREDICT_WALLET_MODE","PREDICT_API_KEY","PREDICT_EOA_PRIVATE_KEY","PREDICT_ACCOUNT_ADDRESS","PREDICT_PRIVY_PRIVATE_KEY","ERC_MANDATED_MCP_COMMAND","ERC_MANDATED_VAULT_ADDRESS","ERC_MANDATED_FACTORY_ADDRESS","ERC_MANDATED_VAULT_ASSET_ADDRESS","ERC_MANDATED_VAULT_AUTHORITY","ERC_MANDATED_AUTHORITY_PRIVATE_KEY","ERC_MANDATED_EXECUTOR_PRIVATE_KEY","ERC_MANDATED_BOOTSTRAP_PRIVATE_KEY","OPENROUTER_API_KEY"]},"install":[{"id":"uv-brew","kind":"brew","formula":"uv","bins":["uv"],"label":"Install uv (brew)"},{"id":"erc-mandated-mcp-node","kind":"node","package":"@erc-mandated/mcp","bins":["erc-mandated-mcp"],"label":"Install erc-mandated-mcp (manual prerequisite for vault flows)"}]}}
---

# PredictClaw

PredictClaw is the predict.fun-native OpenClaw skill for browsing markets, checking wallet readiness, viewing funding guidance, withdrawing funds, placing buys, inspecting positions, and scanning hedge opportunities.

PredictClaw's version source of truth is the repository-root `pyproject.toml`. When checking GitHub or packaging metadata, use this repository root directly.

## Install

### ClawHub / packaged install

```bash
clawhub install predictclaw
cd ~/.openclaw/skills/predictclaw
uv sync
cp template.env .env
```

The installed skill directory `~/.openclaw/skills/predictclaw` is the only canonical user config root. In OpenClaw manifests and examples, this same installed path may appear as `{baseDir}`. Any repository checkout or workspace copy is a development-only artifact, not a user config root.

### Manual install

1. Copy or symlink this repository into `~/.openclaw/skills/predictclaw/`
2. From the installed skill directory, run:

```bash
cd {baseDir} && uv sync
cd {baseDir} && cp template.env .env
```

## How configuration actually works

PredictClaw only reads standard environment variables. The supported, tested inputs are:

- the process environment, for example `export PREDICT_ENV=testnet`
- a local `~/.openclaw/skills/predictclaw/.env` file, auto-loaded by `scripts/predictclaw.py` when present; in manifests and examples, that same installed path may appear as `{baseDir}`

If both are present, exported environment variables win and `.env` only fills missing values.

If your OpenClaw host version injects environment variables into the skill process, that also works because PredictClaw receives normal env vars either way. Older docs used `skills.entries.predictclaw.env`; treat that as a host-version-specific convenience, not the canonical PredictClaw config surface.

The SKILL frontmatter metadata now declares the external runtime and conditionally used env surfaces so ClawHub users can review them before installation. The mode-specific requirements are still documented below and enforced by the runtime config validator; not every listed variable is required at the same time.

## Mode-first onboarding

Choose the mode first, then show only the minimum fields for that mode.

- `read-only`
  - Browsing only.
  - Minimum fields: `PREDICT_ENV`, `PREDICT_WALLET_MODE`, and `PREDICT_API_KEY` for mainnet reads.
- `eoa`
  - Direct signer trading.
  - Minimum fields: `PREDICT_ENV`, `PREDICT_WALLET_MODE=eoa`, `PREDICT_API_KEY`, `PREDICT_EOA_PRIVATE_KEY`.
- `predict-account + ERC_MANDATED_*`
  - Recommended funded-trading path.
  - Ask first: **Do you already have a vault?**
  - **Have a vault** -> minimum fields: `PREDICT_ENV`, `PREDICT_WALLET_MODE=predict-account`, `PREDICT_API_KEY`, `PREDICT_ACCOUNT_ADDRESS`, `PREDICT_PRIVY_PRIVATE_KEY`, `ERC_MANDATED_MCP_COMMAND`, `ERC_MANDATED_CHAIN_ID`, `ERC_MANDATED_VAULT_ADDRESS`, optional `ERC_MANDATED_CONTRACT_VERSION`.
  - **Need a vault** -> deploy or redeploy a vault first with the pure `mandated-vault` bootstrap path, then return to overlay.
- pure `mandated-vault`
  - Recommended governance/control-plane path.
  - Minimum fields: `PREDICT_ENV`, `PREDICT_WALLET_MODE=mandated-vault`, `PREDICT_API_KEY`, `PREDICT_EOA_PRIVATE_KEY`, `ERC_MANDATED_MCP_COMMAND`, `ERC_MANDATED_CHAIN_ID`.

Advanced authority / executor / bootstrap private keys are follow-up fields, not default first-screen requirements. Only surface them when the selected workflow really executes vault-side actions.
Do not treat the full derivation tuple as the primary first-step answer for overlay onboarding when the user already has a deployed vault.

## Mode reminders

1. Run `uv sync` in the installed skill directory.
2. Pick a bootstrap file:
    - `template.env` -> secret-free local fixture bootstrap
    - `template.readonly.env` -> live read-only market reads
    - `template.eoa.env` -> direct private-key trading
    - `template.predict-account.env` -> recommended funded-trading path (Predict Account trades, Vault can fund it)
    - `template.mandated-vault.env` -> recommended governance/control-plane path for advanced pure vault workflows
3. Copy the chosen file to `.env` inside `~/.openclaw/skills/predictclaw/`.
4. Fill only the variables required for that mode.
5. Verify with:

```bash
cd {baseDir} && uv run python scripts/predictclaw.py --help
cd {baseDir} && uv run python scripts/predictclaw.py markets trending
```

`wallet status` requires signer configuration. For `read-only`, start with `markets trending` or `market <id> --json` instead.

mainnet market reads require PREDICT_API_KEY. Non-mainnet usage remains explicit-only and is no longer the packaged default.

`test-fixture` only knows the bundled local market IDs (`123`, `456`, `789`, `101`, `202`). Switch to the live read-only template before querying a real production market ID.

## Recommended operating model

- For user-facing funded trading, recommend `predict-account + ERC_MANDATED_*`.
- In that model, Predict Account remains the trading identity and deposit address, while Vault acts as the funding/control plane.
- For governance-first or bootstrap-only workflows, recommend pure `mandated-vault` instead.
- Do not present pure `mandated-vault` as a co-equal default for trading because it still fails closed on buy / positions / hedge flows.
- For overlay onboarding, ask whether the user already has a vault before asking for advanced vault metadata.

For signer-backed modes, the next verification step is:

```bash
cd {baseDir} && uv run python scripts/predictclaw.py wallet status --json
cd {baseDir} && uv run python scripts/predictclaw.py wallet status --json
```

Canonical user-facing templates now include:

- `template.predict-account.env`
- `template.predict-account-vault.env`

`template.mandated-vault.env` remains only as the internal/bootstrap compatibility template.

## Configuration examples

The snippets below are `.env` examples. Put them in `{baseDir}/.env` or export the same names in your shell.

The installed skill directory `~/.openclaw/skills/predictclaw` remains the only canonical user config root; `{baseDir}` is just the manifest/example placeholder for that installed path.

`OPENROUTER_API_KEY` appears in the signer examples only for optional `hedge scan` / `hedge analyze` usage. It is not required for market, wallet, or buy flows and is only needed for non-fixture hedge analysis.

Do not lead with the full env matrix when a user only asks how to configure the skill. Ask for the mode first, then show only the minimum fields for that mode.

### bootstrap-safe fixture mode

```dotenv
PREDICT_ENV=test-fixture
PREDICT_WALLET_MODE=read-only
```

Use this for secret-free CLI verification and local market browsing only. It does not hit the live API.

### live read-only mode

```dotenv
PREDICT_ENV=mainnet
PREDICT_WALLET_MODE=read-only
PREDICT_API_KEY=YOUR_PREDICT_API_KEY
```

Use the live templates as mainnet-first examples.

### eoa mode

```dotenv
PREDICT_ENV=mainnet
PREDICT_WALLET_MODE=eoa
PREDICT_API_BASE_URL=https://api.predict.fun
PREDICT_API_KEY=YOUR_PREDICT_API_KEY
PREDICT_EOA_PRIVATE_KEY=0xYOUR_EOA_PRIVATE_KEY
```

### predict-account mode

```dotenv
PREDICT_ENV=mainnet
PREDICT_WALLET_MODE=predict-account
PREDICT_API_BASE_URL=https://api.predict.fun
PREDICT_API_KEY=YOUR_PREDICT_API_KEY
PREDICT_ACCOUNT_ADDRESS=0xYOUR_PREDICT_ACCOUNT
PREDICT_PRIVY_PRIVATE_KEY=0xYOUR_PRIVY_EXPORTED_KEY
```

### predict-account + vault route

The user-facing advanced mode is `predict-account + vault`, not a standalone `mandated-vault` mode.

Use the canonical template:

```dotenv
PREDICT_ENV=mainnet
PREDICT_API_BASE_URL=https://api.predict.fun
PREDICT_API_KEY=YOUR_PREDICT_API_KEY
PREDICT_WALLET_MODE=predict-account
PREDICT_ACCOUNT_ADDRESS=0xYOUR_PREDICT_ACCOUNT
PREDICT_PRIVY_PRIVATE_KEY=0xYOUR_PRIVY_EXPORTED_KEY
ERC_MANDATED_VAULT_ADDRESS=0xYOUR_DEPLOYED_VAULT
ERC_MANDATED_VAULT_ASSET_ADDRESS=0xYOUR_ASSET
ERC_MANDATED_VAULT_AUTHORITY=0xYOUR_AUTHORITY
ERC_MANDATED_AUTHORITY_PRIVATE_KEY=0xYOUR_VAULT_AUTHORITY_KEY
ERC_MANDATED_MCP_COMMAND=erc-mandated-mcp
ERC_MANDATED_CONTRACT_VERSION=v0.3.0-agent-contract
ERC_MANDATED_CHAIN_ID=56
```

If the vault does not exist yet, run the bootstrap helper first.

### Internal bootstrap subflow (`mandated-vault`)

The older `mandated-vault` path remains only as the internal/bootstrap compatibility subflow used to create or prepare a vault before returning to `predict-account + vault`.

```dotenv
PREDICT_ENV=mainnet
PREDICT_API_BASE_URL=https://api.predict.fun
PREDICT_API_KEY=YOUR_PREDICT_API_KEY
PREDICT_WALLET_MODE=mandated-vault
PREDICT_EOA_PRIVATE_KEY=0xYOUR_EOA_PRIVATE_KEY
ERC_MANDATED_MCP_COMMAND=erc-mandated-mcp
ERC_MANDATED_CHAIN_ID=56
```

PredictClaw uses the fixed product factory `0x6eFC613Ece5D95e4a7b69B4EddD332CeeCbb61c6`, previews first, requires explicit confirmation, and backfills `.env` with the deployed vault address and resolved values.

On `--confirm`, PredictClaw automatically enables the MCP broadcast gate for that subprocess and bridges the bootstrap signer key. The standard flow does not require manually setting `ERC_MANDATED_ENABLE_BROADCAST=1` or `ERC_MANDATED_BOOTSTRAP_PRIVATE_KEY`, but it no longer auto-edits `.env`.

Preview first:

```bash
cd {baseDir} && uv run python scripts/predictclaw.py wallet bootstrap-vault --json
```

Confirm and broadcast:

```bash
cd {baseDir} && uv run python scripts/predictclaw.py wallet bootstrap-vault --confirm --json
```

### Internal bootstrap compatibility paths

If you intentionally need the internal bootstrap path directly, the following compatibility variants remain:

#### Explicit deployed vault

```dotenv
PREDICT_ENV=mainnet
PREDICT_API_BASE_URL=https://api.predict.fun
PREDICT_API_KEY=YOUR_PREDICT_API_KEY
PREDICT_WALLET_MODE=mandated-vault
ERC_MANDATED_VAULT_ADDRESS=0xYOUR_DEPLOYED_VAULT
ERC_MANDATED_MCP_COMMAND=erc-mandated-mcp
ERC_MANDATED_CHAIN_ID=56
```

#### Predicted / undeployed vault

```dotenv
PREDICT_ENV=mainnet
PREDICT_API_BASE_URL=https://api.predict.fun
PREDICT_API_KEY=YOUR_PREDICT_API_KEY
PREDICT_WALLET_MODE=mandated-vault
ERC_MANDATED_FACTORY_ADDRESS=0xYOUR_FACTORY
ERC_MANDATED_VAULT_ASSET_ADDRESS=0xYOUR_ASSET
ERC_MANDATED_VAULT_NAME=Mandated Vault
ERC_MANDATED_VAULT_SYMBOL=MVLT
ERC_MANDATED_VAULT_AUTHORITY=0xYOUR_AUTHORITY
ERC_MANDATED_VAULT_SALT=0xYOUR_SALT
ERC_MANDATED_MCP_COMMAND=erc-mandated-mcp
ERC_MANDATED_CONTRACT_VERSION=v0.3.0-agent-contract
ERC_MANDATED_CHAIN_ID=56
```

`ERC_MANDATED_EXECUTOR_PRIVATE_KEY` is optional. When it is unset, PredictClaw reuses `ERC_MANDATED_AUTHORITY_PRIVATE_KEY` as the executor signer for the current Preflight MVP contract. This advanced/manual path can still expose `manual-only` create-vault preparation guidance when you intentionally stay on the manual route.

For advanced overrides, `ERC_MANDATED_BOOTSTRAP_PRIVATE_KEY` can replace the default bootstrap signer resolution and `ERC_MANDATED_ENABLE_BROADCAST` can explicitly force the execute-mode gate on or off. In the standard `--confirm` path, PredictClaw auto-bridges both values to the MCP subprocess for you.

### predict-account + vault overlay (recommended advanced funding route)

```dotenv
PREDICT_ENV=mainnet
PREDICT_API_BASE_URL=https://api.predict.fun
PREDICT_API_KEY=YOUR_PREDICT_API_KEY
PREDICT_WALLET_MODE=predict-account
PREDICT_ACCOUNT_ADDRESS=0xYOUR_PREDICT_ACCOUNT
PREDICT_PRIVY_PRIVATE_KEY=0xYOUR_PRIVY_EXPORTED_KEY
ERC_MANDATED_VAULT_ADDRESS=0xYOUR_DEPLOYED_VAULT
ERC_MANDATED_MCP_COMMAND=erc-mandated-mcp
ERC_MANDATED_CONTRACT_VERSION=v0.3.0-agent-contract
ERC_MANDATED_CHAIN_ID=56
```

Ask first: **Do you already have a vault?**

- **Have a vault** -> this is the default overlay path. Provide `ERC_MANDATED_VAULT_ADDRESS` and let PredictClaw resolve the remaining vault metadata where possible.
- **Need a vault** -> deploy or redeploy a vault first with the pure `mandated-vault` bootstrap path, then return to overlay.

Only if automatic resolution fails should you manually add advanced vault metadata such as `ERC_MANDATED_VAULT_ASSET_ADDRESS`, `ERC_MANDATED_VAULT_AUTHORITY`, or authority/executor private keys.

In the overlay route, Predict Account remains the deposit/trading account while Vault funds the Predict Account through MCP-backed session and asset-transfer planning.

If you do **not** have a vault yet, the recommended answer is to deploy or redeploy one first with the pure `mandated-vault` bootstrap flow. The full derivation tuple (`ERC_MANDATED_FACTORY_ADDRESS`, `ERC_MANDATED_VAULT_ASSET_ADDRESS`, `ERC_MANDATED_VAULT_NAME`, `ERC_MANDATED_VAULT_SYMBOL`, `ERC_MANDATED_VAULT_AUTHORITY`, and `ERC_MANDATED_VAULT_SALT`) remains available as an advanced/manual path rather than the default first step.

The optional `ERC_MANDATED_FUNDING_*` envs cap Vault→Predict transfers by per-tx amount, per-window cumulative amount, and window duration. On BSC mainnet USDT, `5U = 5000000000000000000` and `10U = 10000000000000000000`.

## Wallet-mode contract

PredictClaw exposes four user-facing modes.

- `read-only` — browse market data only; no signer-backed wallet actions.
- `eoa` — direct signer path for wallet, trade, and funding flows.
- `predict-account` — smart-wallet funding/trading path using `PREDICT_ACCOUNT_ADDRESS` plus `PREDICT_PRIVY_PRIVATE_KEY`.
- `predict-account + vault` — user-facing advanced route where Predict Account remains the trading identity and Vault acts as the advanced funding source.

## How to answer funding-address questions

- In `predict-account + vault`, the default user-facing answer is the Vault deposit flow.
- Predict Account remains the trading identity and receives the downstream vault-driven top-up afterward.
- `wallet deposit --json` / `wallet status --json` therefore distinguish the default funding entry (`manualTopUpAddress` / `fundingAddress`) from the trading identity (`predictAccountAddress`, `tradingIdentityAddress`).
- Only answer with the Predict Account deposit address when the active route is plain `predict-account` without the vault overlay.

## First-time setup

- Default local posture is `test-fixture` or `mainnet`.
- `mainnet` market reads require `PREDICT_API_KEY`.
- Explicit non-mainnet routing is supported only when you opt into it yourself.
- `read-only` is browse-only. Start with `markets ...`, not signer-backed wallet or trade commands.
- `wallet status requires signer configuration`.
- `eoa` requires `PREDICT_EOA_PRIVATE_KEY` and rejects Predict Account or mandated-vault inputs.
- `predict-account` requires both `PREDICT_ACCOUNT_ADDRESS` and `PREDICT_PRIVY_PRIVATE_KEY`.
- `wallet deposit` shows the default funding entry for the active signer mode.
- `wallet bootstrap-vault` is the helper used during `predict-account + vault` onboarding when a vault still needs to be created or prepared.
- `wallet redeem-vault --preview --json` inspects vault-share redeemability before any real redeem flow is attempted.
- Redeem preview returns machine-readable `redeemableNow`, `blockingReason`, and `contractError` fields, including contract errors such as `ERC4626ExceededMaxRedeem`.
- `wallet withdraw` performs safety validation before any transfer logic.
- `mandated-vault` remains only as an internal/bootstrap compatibility path and is not a standalone user mode.
- Default bootstrap only needs the signer EOA, deployment fee funding, and any optional `ERC_MANDATED_FUNDING_*` amount caps.
- In `predict-account + ERC_MANDATED_*` overlay, `wallet status` / `wallet deposit` expose `manualTopUpAddress`, `tradingIdentityAddress`, `orchestrationVaultAddress`, and `vault-to-predict-account` funding semantics while Predict Account remains the trade identity.
- In that route, the default funding ingress is the Vault deposit flow, not the Predict Account address.
- Vault-related JSON also exposes `vaultAuthority`, `vaultExecutor`, `bootstrapSigner`, `allowedTokenAddresses`, and `allowedRecipients` so OpenClaw can reason about configured permissions.
- Overlay `buy` can proceed when the Predict Account balance is sufficient; otherwise it returns deterministic `funding-required` guidance that points to `wallet deposit --json`.
- Pure `mandated-vault` needs a working `ERC_MANDATED_MCP_COMMAND`; in overlay mode the default path is an explicit `ERC_MANDATED_VAULT_ADDRESS`, with asset/authority metadata resolved automatically where possible and only escalated to manual fields when that resolution fails.
- To detect whether the runtime is already available, run `cd {baseDir} && uv run python scripts/predictclaw.py setup mandated-mcp`.
- The default path does not globally install packages and does not auto-edit `.env`.
- Install the external `erc-mandated-mcp` runtime yourself, then set `ERC_MANDATED_MCP_COMMAND` manually.
- Hedge analysis uses OpenRouter; `OPENROUTER_API_KEY` is only required for non-fixture hedge analysis, and fixture mode stays secret-free.

```bash
cd {baseDir} && uv run python scripts/predictclaw.py --help
cd {baseDir} && uv run python scripts/predictclaw.py wallet status --json
cd {baseDir} && uv run python scripts/predictclaw.py wallet deposit --json
cd {baseDir} && uv run python scripts/predictclaw.py wallet bootstrap-vault --json
cd {baseDir} && uv run python scripts/predictclaw.py wallet bootstrap-vault --confirm --json
cd {baseDir} && uv run python scripts/predictclaw.py wallet redeem-vault --share-token 0x4a88c1c95d0f59ee87c3286ed23e9dcdf4cf08d7 --holder 0x7df0ba782D85B93266b595d496088ABFAc823950 --all --preview --json
cd {baseDir} && uv run python scripts/predictclaw.py wallet withdraw usdt 1 0xb30741673D351135Cf96564dfD15f8e135f9C310 --json
```

## Command surface

```bash
cd {baseDir} && uv run python scripts/predictclaw.py markets trending
cd {baseDir} && uv run python scripts/predictclaw.py markets search "election"
cd {baseDir} && uv run python scripts/predictclaw.py market 123 --json
cd {baseDir} && uv run python scripts/predictclaw.py wallet status --json
cd {baseDir} && uv run python scripts/predictclaw.py wallet approve --json
cd {baseDir} && uv run python scripts/predictclaw.py wallet deposit --json
cd {baseDir} && uv run python scripts/predictclaw.py wallet bootstrap-vault --json
cd {baseDir} && uv run python scripts/predictclaw.py wallet bootstrap-vault --confirm --json
cd {baseDir} && uv run python scripts/predictclaw.py wallet withdraw usdt 1 0xb30741673D351135Cf96564dfD15f8e135f9C310 --json
cd {baseDir} && uv run python scripts/predictclaw.py wallet withdraw bnb 0.1 0xb30741673D351135Cf96564dfD15f8e135f9C310 --json
cd {baseDir} && uv run python scripts/predictclaw.py buy 123 YES 25 --json
cd {baseDir} && uv run python scripts/predictclaw.py positions --json
cd {baseDir} && uv run python scripts/predictclaw.py position pos-123-yes --json
cd {baseDir} && uv run python scripts/predictclaw.py hedge scan --query election --json
cd {baseDir} && uv run python scripts/predictclaw.py hedge analyze 101 202 --json
```

## Environment variables

| Variable | Purpose |
| --- | --- |
| `PREDICT_STORAGE_DIR` | Local journal and position storage |
| `PREDICT_ENV` | Defaults to `mainnet` in code; `template.env` intentionally bootstraps `test-fixture`; accepted values are `mainnet`, `testnet`, or `test-fixture` |
| `PREDICT_WALLET_MODE` | Explicit mode override: `read-only`, `eoa`, `predict-account`, or `mandated-vault` |
| `PREDICT_API_BASE_URL` | Optional REST base override; packaged live templates pin this to `https://api.predict.fun`, while leaving it empty uses the env-specific default |
| `PREDICT_API_KEY` | Mainnet-authenticated predict.fun API access; required for mainnet market reads and trading |
| `PREDICT_EOA_PRIVATE_KEY` | EOA trading and funding path |
| `PREDICT_ACCOUNT_ADDRESS` | Predict Account smart-wallet address |
| `PREDICT_PRIVY_PRIVATE_KEY` | Privy-exported signer for Predict Account mode |
| `ERC_MANDATED_VAULT_ADDRESS` | Explicit deployed mandated vault address |
| `ERC_MANDATED_FACTORY_ADDRESS` | Product default factory for pure bootstrap and manual derivation override; current default is `0x6eFC613Ece5D95e4a7b69B4EddD332CeeCbb61c6` |
| `ERC_MANDATED_VAULT_ASSET_ADDRESS` | ERC-4626 asset used in mandated-vault prediction/create preparation |
| `ERC_MANDATED_VAULT_NAME` | Vault name used in mandated-vault prediction/create preparation |
| `ERC_MANDATED_VAULT_SYMBOL` | Vault symbol used in mandated-vault prediction/create preparation |
| `ERC_MANDATED_VAULT_AUTHORITY` | Authority address and create-vault `from` address for manual preparation |
| `ERC_MANDATED_VAULT_SALT` | Deterministic salt used for vault prediction/create preparation |
| `ERC_MANDATED_AUTHORITY_PRIVATE_KEY` | Preflight Vault signer key for the current single-key MVP contract |
| `ERC_MANDATED_EXECUTOR_PRIVATE_KEY` | Optional dedicated executor signer; falls back to `ERC_MANDATED_AUTHORITY_PRIVATE_KEY` when unset |
| `ERC_MANDATED_BOOTSTRAP_PRIVATE_KEY` | Optional execute-mode bootstrap signer override; when unset, PredictClaw falls back to `PREDICT_EOA_PRIVATE_KEY`, then `ERC_MANDATED_AUTHORITY_PRIVATE_KEY` |
| `ERC_MANDATED_ENABLE_BROADCAST` | Optional execute-mode MCP gate override; `wallet bootstrap-vault --confirm` auto-bridges this to `1` unless you explicitly override it |
| `ERC_MANDATED_MCP_COMMAND` | MCP launcher command (defaults to `erc-mandated-mcp`) |
| `ERC_MANDATED_CONTRACT_VERSION` | Passed through to the mandated-vault MCP client |
| `ERC_MANDATED_CHAIN_ID` | Optional explicit chain selection for the MCP bridge |
| `ERC_MANDATED_ALLOWED_ADAPTERS_ROOT` | Optional 32-byte hex `allowedAdaptersRoot` used for Vault execution mandates; defaults to `0x11…11` for the current single-key MVP / PoC path |
| `ERC_MANDATED_FUNDING_MAX_AMOUNT_PER_TX` | Optional Vault→Predict funding-policy `maxAmountPerTx` in raw token units |
| `ERC_MANDATED_FUNDING_MAX_AMOUNT_PER_WINDOW` | Optional Vault→Predict funding-policy `maxAmountPerWindow` in raw token units |
| `ERC_MANDATED_FUNDING_WINDOW_SECONDS` | Optional Vault→Predict funding-policy `windowSeconds` |
| `OPENROUTER_API_KEY` | Optional OpenRouter credential; only required for non-fixture hedge analysis |
| `PREDICT_MODEL` | OpenRouter model override |
| `PREDICT_SMOKE_ENV` | Enables the smoke suite |
| `PREDICT_SMOKE_API_BASE_URL` | Optional smoke REST base override |
| `PREDICT_SMOKE_PRIVATE_KEY` | Enables signer/JWT smoke checks |
| `PREDICT_SMOKE_ACCOUNT_ADDRESS` | Predict Account smoke mode |
| `PREDICT_SMOKE_PRIVY_PRIVATE_KEY` | Predict Account smoke signer |
| `PREDICT_SMOKE_API_KEY` | Smoke REST auth |

## Architecture note

- **SDK for chain-aware/signed flows**
- **REST for auth, data, order submission, and query**

## Safety notes

- Do not treat fixture mode as proof of funded-wallet behavior.
- Do not assume live liquidity from docs alone.
- Keep only limited funds on automation keys.
- Withdrawal commands are public; transfer validation happens before chain interaction, but users still own the operational risk.
- When the goal is to keep Predict Account as the trading identity and let Vault only fund it, immediately choose `predict-account + ERC_MANDATED_*`.
- `mandated-vault` is an advanced explicit opt-in mode. Treat it as a separate control-plane path, not a co-equal answer for Predict Account trading.
- `predict-account + ERC_MANDATED_*` is the recommended advanced trading route when you want Vault to fund the Predict Account while keeping the official Predict Account order model.
- Explicit-vs-predicted vault semantics: `ERC_MANDATED_VAULT_ADDRESS` targets an existing vault directly; otherwise PredictClaw uses the derivation tuple to ask the MCP for the predicted vault address.
- `wallet bootstrap-vault --json` is preview-only, requires explicit confirmation before broadcast, and backfills `.env` after a confirmed deployment.
- Advanced/manual derivation flows can still return create-vault preparation details (`predictedVault`, transaction summary, `manual-only`) without broadcasting.
- Trust boundary: the MCP orchestrates transport and preparation; the vault contract policy authorizes what the vault can actually execute.
- Pure `mandated-vault` does not provide predict.fun trading parity. `wallet approve`, `wallet withdraw`, `buy`, `positions`, `position`, `hedge scan`, and `hedge analyze` fail closed with `unsupported-in-mandated-vault-v1`.
- Overlay funding currently plans the vault leg and surfaces deterministic `funding-required` guidance when buy needs top-up; it does not auto-execute the funding leg in the current local signer context.
