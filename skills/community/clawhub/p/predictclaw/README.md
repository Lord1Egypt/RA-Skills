# PredictClaw

[中文说明 / Chinese Version](./README.zh-CN.md)

PredictClaw is the predict.fun-native OpenClaw skill for browsing markets, checking wallet readiness, viewing funding guidance, withdrawing funds, placing buys, inspecting positions, and scanning hedge opportunities.

This repository packages PredictClaw as a standalone OpenClaw skill with its own CLI, runtime configuration, and tests.

PredictClaw's version source of truth is the repository-root `pyproject.toml`. When checking GitHub or building from source, use this repository root directly.

## What PredictClaw Is For

PredictClaw gives OpenClaw a predictable command surface for predict.fun workflows:

- market discovery and market detail lookup
- wallet readiness and deposit guidance
- trading through EOA or Predict Account paths
- position journaling and query flows
- optional hedge analysis for users who enable model access

For the advanced funding route, PredictClaw supports a **Vault funding overlay** on top of the official Predict Account path. In that route, **Predict Account remains** the deposit address, trade identity, and order path while Vault acts as the funding source.

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

### Local repo development

From the repository root:

```bash
uv sync
uv run pytest -q
uv run python scripts/predictclaw.py --help
```

Use the repository root for development and tests only. Do not treat it as the canonical location for end-user `.env` edits or normal installed-skill CLI usage.

## How configuration actually works

PredictClaw only reads standard environment variables. The supported, tested inputs are:

- the process environment, for example `export PREDICT_ENV=testnet`
- a local `~/.openclaw/skills/predictclaw/.env` file, auto-loaded by `scripts/predictclaw.py` when present; in manifests and examples, that same installed path may appear as `{baseDir}`

If both are present, exported environment variables win and `.env` only fills missing values.

If your OpenClaw host version injects environment variables into the skill process, that also works because PredictClaw receives normal env vars either way. Older docs used `skills.entries.predictclaw.env`; treat that as a host-version-specific convenience, not the canonical PredictClaw config surface.

The SKILL frontmatter metadata now declares the external runtime and conditionally used env surfaces so ClawHub users can review them before installation. The mode-specific requirements are still documented below and enforced by the runtime config validator; not every listed variable is required at the same time.

## Mode-first onboarding (recommended)

Choose the mode first, then fill only the minimum fields for that mode.

- `read-only`
  - Use for browsing only.
  - Minimum fields: `PREDICT_ENV`, `PREDICT_WALLET_MODE`, `PREDICT_API_KEY` for mainnet reads.
- `eoa`
  - Use for direct signer trading without Predict Account overlay.
  - Minimum fields: `PREDICT_ENV`, `PREDICT_WALLET_MODE=eoa`, `PREDICT_API_KEY`, `PREDICT_EOA_PRIVATE_KEY`.
- `predict-account + ERC_MANDATED_*` (recommended funded-trading path)
  - Use when Predict Account stays the trading identity and Vault may fund it.
  - Ask first: **Do you already have a vault?**
  - **Have a vault** -> minimum fields: `PREDICT_ENV`, `PREDICT_WALLET_MODE=predict-account`, `PREDICT_API_KEY`, `PREDICT_ACCOUNT_ADDRESS`, `PREDICT_PRIVY_PRIVATE_KEY`, `ERC_MANDATED_MCP_COMMAND`, `ERC_MANDATED_CHAIN_ID`, `ERC_MANDATED_VAULT_ADDRESS`, optional `ERC_MANDATED_CONTRACT_VERSION`.
  - **Need a vault** -> deploy or redeploy a vault first with the pure `mandated-vault` bootstrap flow, then come back to overlay.
- pure `mandated-vault` (recommended governance/control-plane path)
  - Use for bootstrap, governance, and vault-only control-plane workflows.
  - Minimum fields: `PREDICT_ENV`, `PREDICT_WALLET_MODE=mandated-vault`, `PREDICT_API_KEY`, `PREDICT_EOA_PRIVATE_KEY`, `ERC_MANDATED_MCP_COMMAND`, `ERC_MANDATED_CHAIN_ID`.

Advanced executor/authority/bootstrap private keys remain mode-specific follow-up inputs. Do not present them as day-one required fields unless the current workflow actually executes vault-side actions.
Do not treat the full derivation tuple as the primary first-step answer for overlay onboarding when the user already has a deployed vault.

## First-time setup (recommended)

1. Install the skill and run `uv sync`.
2. Pick a bootstrap file:
    - `template.env` -> secret-free local fixture bootstrap
    - `template.readonly.env` -> live read-only market reads
    - `template.eoa.env` -> direct private-key trading
    - `template.predict-account.env` -> Predict Account trading
    - `template.predict-account-vault.env` -> Predict Account + vault
    - `template.mandated-vault.env` -> internal/compatibility bootstrap template
3. Copy the chosen template to `.env` inside `~/.openclaw/skills/predictclaw/`.
4. Fill only the variables required for that mode.
5. Verify the install with `uv run python scripts/predictclaw.py --help`.
6. Then run a mode-appropriate command:
   - fixture bootstrap -> `uv run python scripts/predictclaw.py markets trending`
   - live read-only -> `uv run python scripts/predictclaw.py markets trending`
   - `eoa` / `predict-account` -> `uv run python scripts/predictclaw.py wallet status --json`
   - `predict-account + vault` -> `uv run python scripts/predictclaw.py wallet status --json`

### Choose your route first

- `read-only` for browsing only.
- When the goal is to keep Predict Account as the trading identity and let Vault only fund it, immediately choose `predict-account + ERC_MANDATED_*`.
- pure `mandated-vault` is a separate control-plane path for creating a new Vault or directly operating Vault control-plane flows.

If you want Vault funding without changing the trading identity, start from `template.predict-account.env`, use `PREDICT_WALLET_MODE=predict-account`, and treat that as the default answer for the "keep the official trading identity, let Vault fund it" workflow. Do not start from pure `wallet bootstrap-vault` unless you are creating a new vault or working on the control plane directly.

For overlay onboarding, ask the vault question first:

- **Have a vault** -> provide `ERC_MANDATED_VAULT_ADDRESS`, then let PredictClaw resolve or validate the remaining vault metadata where possible.
- **Need a vault** -> deploy or redeploy a vault first with the pure `mandated-vault` bootstrap flow.

Do not treat the full derivation tuple as the primary first-step answer for overlay onboarding unless the user is explicitly on the advanced/manual recovery path.

## Bootstrap templates

- `template.env` -> safest first install; uses `test-fixture` + `read-only` so the CLI can start without secrets or network access
- `template.readonly.env` -> live market reads; mainnet market reads require PREDICT_API_KEY
- `template.eoa.env` -> EOA signer flow, pinned to mainnet with `https://api.predict.fun`
- `template.predict-account.env` -> Predict Account signer flow, pinned to mainnet with `https://api.predict.fun`
- `template.predict-account-vault.env` -> canonical user-facing template for Predict Account + vault
- `template.mandated-vault.env` -> internal/compatibility bootstrap template used during vault creation or recovery

### Recommended operating model

- For user-facing funded trading, recommend `predict-account + vault`.
- In that model, Predict Account remains the trading identity and deposit address, while Vault acts as the funding/control plane.
- `mandated-vault` is not a standalone user mode; it remains the internal/bootstrap path used when a vault still needs to be created or prepared.

## Real first-install paths

### A. CLI boots successfully

```bash
uv sync
uv run python scripts/predictclaw.py --help
```

### B. Secret-free local verification

Copy `template.env` and run:

```bash
uv run python scripts/predictclaw.py markets trending
```

This uses `test-fixture`, so it proves the skill boots and routes commands correctly without touching the live API.
Fixture mode only knows the bundled fixture market IDs (`123`, `456`, `789`, `101`, `202`). For real market IDs, switch to the live read-only template first.

### C. Live read-only market reads

Copy `template.readonly.env` to read live production markets on mainnet.

```bash
uv run python scripts/predictclaw.py markets trending
uv run python scripts/predictclaw.py market <market_id> --json
```

If mainnet reads fail with `401 unauthorized`, your `PREDICT_API_KEY` is missing or invalid.

### D. Signer-backed flows

wallet status requires signer configuration. `wallet status --json` is the right next step for `eoa` and `predict-account`, but it is not the first command to run in `read-only` mode.

### E. Mode-first minimum field rule

Do not paste the full env matrix first. Ask which mode the user is choosing, then show only the minimum fields for that mode. Add advanced authority/executor/bootstrap keys only when the selected flow actually needs vault-side execution.

## Configuration examples

The snippets below are `.env` examples. Put them in `~/.openclaw/skills/predictclaw/.env` (the same installed path sometimes shown as `{baseDir}`) or export the same names in your shell.

`OPENROUTER_API_KEY` only matters for non-fixture `hedge scan` / `hedge analyze` usage. It is not required for market, wallet, or buy flows.

### bootstrap-safe fixture mode

```dotenv
PREDICT_ENV=test-fixture
PREDICT_WALLET_MODE=read-only
```

Use this for secret-free CLI verification and local market browsing only. It does not hit the live API. Switch to `eoa`, `predict-account`, or `predict-account + vault` before using wallet or trade subcommands.

### live read-only mode

```dotenv
PREDICT_ENV=mainnet
PREDICT_WALLET_MODE=read-only
PREDICT_API_KEY=YOUR_PREDICT_API_KEY
```

Mainnet market reads require `PREDICT_API_KEY`.

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

### predict-account + vault onboarding

The user-facing advanced mode is `predict-account + vault`, not a standalone `mandated-vault` mode.

Start from the canonical template:

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

If you already have a vault, bind it through `ERC_MANDATED_VAULT_ADDRESS` and the related authority/asset values.

If you do not yet have a vault, use the bootstrap helper first.

### Internal bootstrap subflow (`mandated-vault`)

The older `mandated-vault` path still exists internally as the bootstrap/compatibility subflow that creates or prepares a vault before you return to the user-facing `predict-account + vault` route.

```dotenv
PREDICT_ENV=mainnet
PREDICT_API_BASE_URL=https://api.predict.fun
PREDICT_API_KEY=YOUR_PREDICT_API_KEY
PREDICT_WALLET_MODE=mandated-vault
PREDICT_EOA_PRIVATE_KEY=0xYOUR_EOA_PRIVATE_KEY
ERC_MANDATED_MCP_COMMAND=erc-mandated-mcp
ERC_MANDATED_CHAIN_ID=56
```

PredictClaw uses the fixed product factory `0x6eFC613Ece5D95e4a7b69B4EddD332CeeCbb61c6`, derives the signer address from `PREDICT_PRIVATE_KEY`, previews the deployment first, requires explicit confirmation before broadcast, then backfills `.env` with the deployed vault address and resolved values.

On `--confirm`, PredictClaw automatically enables the MCP broadcast gate for that subprocess and bridges the bootstrap signer key. The standard flow does not require manually setting `ERC_MANDATED_ENABLE_BROADCAST=1` or `ERC_MANDATED_BOOTSTRAP_PRIVATE_KEY`, but it no longer auto-edits `.env` for you.

Preview first:

```bash
uv run python scripts/predictclaw.py wallet bootstrap-vault --json
```

Confirm and broadcast:

```bash
uv run python scripts/predictclaw.py wallet bootstrap-vault --confirm --json
```

Optional bootstrap amount / funding controls:

```dotenv
ERC_MANDATED_FUNDING_MAX_AMOUNT_PER_TX=5000000000000000000
ERC_MANDATED_FUNDING_MAX_AMOUNT_PER_WINDOW=10000000000000000000
ERC_MANDATED_FUNDING_WINDOW_SECONDS=3600
```

### Internal bootstrap compatibility paths

If you intentionally need the internal bootstrap path directly, these legacy/compatibility variants still exist:

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

Use this only when you intentionally need the internal bootstrap path to target an already deployed vault.

#### Full derivation tuple

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

`ERC_MANDATED_EXECUTOR_PRIVATE_KEY` is optional. When it is unset, PredictClaw reuses `ERC_MANDATED_AUTHORITY_PRIVATE_KEY` as the executor signer for the current Preflight MVP contract. This is the advanced/manual recovery path; if the predicted vault is still undeployed, PredictClaw can still surface preparation details and `manual-only` guidance without broadcasting.

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

If you already have a deployed vault, this is the primary overlay path: provide `ERC_MANDATED_VAULT_ADDRESS` and let PredictClaw resolve the remaining vault metadata where possible.

If you do **not** have a vault yet, the recommended answer is to deploy or redeploy one first with the pure `mandated-vault` bootstrap flow. The full derivation tuple (`ERC_MANDATED_FACTORY_ADDRESS`, `ERC_MANDATED_VAULT_ASSET_ADDRESS`, `ERC_MANDATED_VAULT_NAME`, `ERC_MANDATED_VAULT_SYMBOL`, `ERC_MANDATED_VAULT_AUTHORITY`, and `ERC_MANDATED_VAULT_SALT`) remains available as an advanced/manual path rather than the default first step.

Only if automatic resolution fails should you manually add advanced vault metadata such as `ERC_MANDATED_VAULT_ASSET_ADDRESS`, `ERC_MANDATED_VAULT_AUTHORITY`, or authority/executor private keys.

Optional overlay caps:

```dotenv
ERC_MANDATED_FUNDING_MAX_AMOUNT_PER_TX=5000000000000000000
ERC_MANDATED_FUNDING_MAX_AMOUNT_PER_WINDOW=10000000000000000000
ERC_MANDATED_FUNDING_WINDOW_SECONDS=3600
```

In the overlay route, Predict Account remains the deposit/trading account while Vault funds the Predict Account through MCP-backed session and asset-transfer planning.

This is the correct route when Predict Account remains the deposit/trading identity and Vault only supplies funds.

## Wallet Modes

PredictClaw supports four user-facing modes:

- `read-only` — browse market data only; no signer-backed wallet actions.
- `eoa` — direct signer path for wallet, trade, and funding flows.
- `predict-account` — smart-wallet funding/trading path using `PREDICT_ACCOUNT_ADDRESS` plus `PREDICT_PRIVY_PRIVATE_KEY`.
- `predict-account + vault` — Predict Account remains the trading identity while Vault acts as the advanced funding source.

### Recommended route

If the goal is to keep Predict Account as the trading identity while Vault only funds it, use:

- `PREDICT_WALLET_MODE=predict-account`
- plus the required `ERC_MANDATED_*` overlay inputs (`predict-account + ERC_MANDATED_*`)

This is the default route for the Predict Account trading-identity workflow. It exposes `vault-to-predict-account` semantics in `wallet status --json` and `wallet deposit --json`.

### How to answer "what address should I fund?"

- In `predict-account + vault`, the default user-facing answer is: fund the Vault deposit flow first.
- Predict Account remains the trading identity and receives the downstream vault-driven top-up afterward.
- `wallet deposit --json` / `wallet status --json` therefore distinguish:
  - the default funding entry (`manualTopUpAddress` / `fundingAddress`) -> Vault
  - the trading identity / recipient (`predictAccountAddress`, `tradingIdentityAddress`) -> Predict Account
- Only answer with the Predict Account deposit page when the active route is plain `predict-account` without the vault funding overlay.

### Internal bootstrap note

<<<<<<< HEAD
`mandated-vault` is an advanced explicit opt-in mode. Treat it as a separate control-plane path, not a co-equal answer for Predict Account trading.

Bundled factory defaults and the returned manual env block make pure bootstrap more convenient, but they do not replace deployment-time signer inputs or the overlay-specific env required by the `predict-account` funding route.

For the default pure bootstrap flow, users only need an EOA signer, deployment-fee funding, and any optional amount caps. PredictClaw handles the product-configured factory, previews before broadcast, requires explicit confirmation, and returns a manual env block after success.

Pure `mandated-vault` does **not** provide predict.fun trading parity. `wallet approve`, `wallet withdraw`, `buy`, `positions`, `position`, `hedge scan`, and `hedge analyze` fail closed with `unsupported-in-mandated-vault-v1`.
=======
`mandated-vault` still exists in the runtime as an internal/bootstrap compatibility subflow, but it is **not a standalone user mode**. It is used when PredictClaw needs to create or prepare a vault before returning to `predict-account + vault`.
>>>>>>> 7e22c30 (docs: reframe vault onboarding as predict-account plus vault)

### Common configuration mistakes

- `read-only` is browse-only. Start with `markets ...`, not signer-backed wallet or trade commands.
- `wallet status` requires signer configuration. In `read-only`, start with `markets trending` or `market <id> --json` instead.
- `mainnet` market reads require `PREDICT_API_KEY`; missing keys fail early and invalid keys return `401 unauthorized`.
- `eoa` requires `PREDICT_EOA_PRIVATE_KEY` and rejects Predict Account or mandated-vault inputs.
- `predict-account` requires both `PREDICT_ACCOUNT_ADDRESS` and `PREDICT_PRIVY_PRIVATE_KEY`.
- `mainnet` requires `PREDICT_API_KEY`.
- pure `mandated-vault` needs a working `ERC_MANDATED_MCP_COMMAND`; in overlay mode the default path is an explicit `ERC_MANDATED_VAULT_ADDRESS`, with asset and authority metadata resolved automatically where possible and only escalated to manual fields when that resolution fails.

## The mandated MCP dependency (`ERC_MANDATED_MCP_COMMAND`)

`ERC_MANDATED_MCP_COMMAND` is the launcher command that PredictClaw uses to talk to the mandated-vault MCP runtime. The default value is `erc-mandated-mcp`.

This is the practical bridge between PredictClaw and the Vault control plane:

1. **Vault prediction / preparation** — predict a vault address when only the derivation tuple is available.
2. **Vault bootstrap execution** — preview and confirm pure mandated-vault deployment through `vault_bootstrap`.
3. **Vault overlay orchestration** — expose `vault-to-predict-account` routing, funding-policy context, and session planning.
4. **Control-plane safety boundary** — if the MCP is missing or unhealthy, PredictClaw surfaces a fail-closed error instead of silently guessing.

If your environment packages that runtime through something like an `@erc-mandated/mcp` package, point `ERC_MANDATED_MCP_COMMAND` at the launcher it installs. PredictClaw's public contract is the command path, not a hard-coded package manager dependency.

For the default safe path, run:

```bash
uv run python scripts/predictclaw.py setup mandated-mcp
```

PredictClaw only detects whether an `erc-mandated-mcp` launcher is available. It does not globally install packages and does not auto-edit `.env` in the default path. Install the external `erc-mandated-mcp` runtime yourself, then set `ERC_MANDATED_MCP_COMMAND` manually.

The MCP orchestrates transport and preparation; the vault contract policy authorizes what the vault can actually execute.

## Command Surface

```bash
uv run python scripts/predictclaw.py markets trending
uv run python scripts/predictclaw.py markets search "election"
uv run python scripts/predictclaw.py market 123 --json
uv run python scripts/predictclaw.py wallet status --json
uv run python scripts/predictclaw.py wallet approve --json
uv run python scripts/predictclaw.py wallet deposit --json
uv run python scripts/predictclaw.py wallet bootstrap-vault --json
uv run python scripts/predictclaw.py wallet bootstrap-vault --confirm --json
uv run python scripts/predictclaw.py wallet withdraw usdt 1 0xb30741673D351135Cf96564dfD15f8e135f9C310 --json
uv run python scripts/predictclaw.py wallet withdraw bnb 0.1 0xb30741673D351135Cf96564dfD15f8e135f9C310 --json
uv run python scripts/predictclaw.py buy 123 YES 25 --json
uv run python scripts/predictclaw.py positions --json
uv run python scripts/predictclaw.py position pos-123-yes --json
uv run python scripts/predictclaw.py hedge scan --query election --json
uv run python scripts/predictclaw.py hedge analyze 101 202 --json
```

## Core workflow notes

- `wallet status` reports signer mode, funding guidance, balances, and approval readiness.
- `wallet deposit` is a funding-guidance command: in `predict-account + vault`, it shows the Vault deposit flow as the default funding entry, while still separating the Predict Account recipient / trading identity and the orchestration vault metadata.
- `wallet bootstrap-vault` is the pure mandated-vault preview / confirmation entry point.
- The default bootstrap flow uses the fixed factory `0x6eFC613Ece5D95e4a7b69B4EddD332CeeCbb61c6` and backfills `.env` after a confirmed deployment.
- `wallet redeem-vault --preview --json` previews vault-share redemption and reports `redeemableNow`, `blockingReason`, and decoded contract errors such as `ERC4626ExceededMaxRedeem`.
- `wallet withdraw` validates checksum destination, positive amount, available balance, and BNB gas headroom before attempting transfer logic.
- In fixture mode, withdraw commands return deterministic placeholder transaction hashes instead of touching a chain.
- In `predict-account + ERC_MANDATED_*` overlay, `wallet status` / `wallet deposit` expose:
  - `manualTopUpAddress`
  - `tradingIdentityAddress`
  - `predictAccountAddress`
  - `tradeSignerAddress`
  - `orchestrationVaultAddress`
  - `vaultAddress`
  - `fundingRoute = vault-to-predict-account`
- Default funding now goes through the Vault deposit flow.
- Predict Account remains the trading identity / order account.
- The internal orchestration target remains the Predict Account, but the user-facing funding ingress is the Vault.
- Optional Vault funding-policy envs let you cap Vault→Predict transfers by per-tx amount, cumulative window amount, and window duration.
- Vault-related JSON now also surfaces `vaultAuthority`, `vaultExecutor`, `bootstrapSigner`, `allowedTokenAddresses`, and `allowedRecipients` so users and OpenClaw can reason about permissions directly.
- Those funding-policy amounts use raw token units; for BSC mainnet USDT (18 decimals), `5 U = 5000000000000000000` and `10 U = 10000000000000000000`.
- If the Predict Account already has enough balance, `buy` continues through the normal official Predict Account order path.
- If balance is short, `buy` fails cleanly with deterministic `funding-required` guidance and points users to `wallet deposit --json`; it does not auto-execute the vault funding leg in the current local signer context.

### Redeem preview

Use the preview-only redeem diagnostic before attempting any future exit flow:

```bash
uv run python scripts/predictclaw.py wallet redeem-vault --share-token 0x4a88c1c95d0f59ee87c3286ed23e9dcdf4cf08d7 --holder 0x7df0ba782D85B93266b595d496088ABFAc823950 --all --preview --json
```

This reads the share token, underlying asset, `maxRedeem`, `maxWithdraw`, and a simulated redeem call. The response includes `redeemableNow`, `blockingReason`, and `contractError`. The current flow is intentionally `preview-only`.

## Runtime Modes

- `test-fixture` — uses local JSON fixtures and deterministic wallet/hedge/trade behavior; ideal for development, integration tests, and secret-free first-install verification.
- `mainnet` — requires `PREDICT_API_KEY` even for market reads and should be treated as a live-trading environment.
- `testnet` — still supported only when you explicitly opt into a non-mainnet environment; it is no longer a packaged default or recommended onboarding path.

## Environment Variables

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
| `OPENROUTER_API_KEY` | Hedge analysis model access |
| `PREDICT_MODEL` | OpenRouter model override |
| `PREDICT_SMOKE_ENV` | Enables the smoke suite |
| `PREDICT_SMOKE_API_BASE_URL` | Optional smoke REST base override |
| `PREDICT_SMOKE_PRIVATE_KEY` | Enables signer/JWT smoke checks |
| `PREDICT_SMOKE_ACCOUNT_ADDRESS` | Predict Account smoke mode |
| `PREDICT_SMOKE_PRIVY_PRIVATE_KEY` | Predict Account smoke signer |
| `PREDICT_SMOKE_API_KEY` | Smoke REST auth |

## Hedge notes

- Hedge analysis uses OpenRouter over plain HTTP with a JSON-only contract.
- `OPENROUTER_API_KEY` is only required for non-fixture hedge analysis.
- Fixture mode uses deterministic keyword- and pairing-based hedge portfolios so CLI and integration tests stay secret-free.
- The current public command surface remains PolyClaw-parity plus `wallet deposit` / `wallet withdraw`; there is no public `sell` command in v1.

## Project Layout

- `scripts/predictclaw.py` — top-level CLI router
- `scripts/` — command-specific entry points
- `lib/` — config, auth, REST, wallet, funding, trade, positions, hedge, and MCP bridge logic
- `tests/` — unit, integration, and smoke coverage for the Python skill package

## Verification Layers

```bash
# unit + command tests
uv run pytest -q

# fixture-backed end-to-end CLI checks
uv run pytest tests/integration -q

# env-gated smoke (passes or skips)
uv run pytest tests/smoke/test_testnet_smoke.py -q
```

## Safety Notes

- Do not treat fixture mode as proof of funded-wallet behavior.
- Do not assume live liquidity from docs alone.
- Keep only limited funds on automation keys.
- Withdrawal commands are public; transfer validation happens before chain interaction, but users still own the operational risk.
- `predict-account + ERC_MANDATED_*` is the recommended advanced trading route when you want Vault to fund the Predict Account while keeping the official Predict Account order model.
- Explicit-vs-predicted vault semantics: `ERC_MANDATED_VAULT_ADDRESS` targets an existing vault directly; otherwise PredictClaw uses the derivation tuple to ask the MCP for the predicted vault address.
- If a predicted vault is undeployed, `wallet bootstrap-vault --json` returns preview details (`predictedVault`, transaction summary, confirmation required) without broadcasting.
- Advanced/manual derivation flows can still return create-vault preparation details with `manual-only` guidance when you intentionally stay on the manual path.
- Pure `mandated-vault` does not provide predict.fun trading parity and intentionally fails closed for unsupported paths with `unsupported-in-mandated-vault-v1`.
