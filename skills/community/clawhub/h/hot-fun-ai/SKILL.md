---
name: hot-fun-ai
description: |
  CLI tool to create meme tokens on hot.fun (Solana). Returns structured JSON for token creation flow.

allowed-tools:
  - Bash(hotfun *)
  - Bash(npx hotfun *)
license: MIT
metadata:
  {"author":"Hot.fun AI Skill","version":"1.0.0","openclaw":{"requires":{"env":["PRIVATE_KEY"]},"primaryEnv":"PRIVATE_KEY","optionalEnv":["SOLANA_RPC_URL"]}}
---

## [Agent must follow] User agreement and security notice on first use

When responding to any user request about hotfun or this skill, **you must first** present the content below in this order: **User Agreement, then Security Notice**, and state clearly that by choosing to continue, the user agrees to the User Agreement.
Until the user has explicitly agreed or confirmed to continue, **do not** run `create-token` (any operation that uses the private key or writes to the chain).

**Language selection**: Present the User Agreement and Security Notice **in the user's language**. If the user is writing in **Traditional Chinese (繁體中文)**, use the **繁體中文** block below; otherwise use the **English** block.

---

### User Agreement & Security Notice (繁體中文)

**用戶協議**

**前情提示**：使用本插件及本 skill 所涉功能（包括但不限於代幣創建等）前，請您閱讀以下協議。**若您選擇繼續使用本插件及本 skill 功能，即表示您已閱讀、理解並同意本協議。**

**本插件性質與責任限制**：本插件僅提供純本地的命令列互動能力（私鑰透過環境變數或本地設定使用），**不會收集、上傳或儲存您的私鑰**。因任何原因（包括但不限於插件被竄改、環境遭入侵、誤操作、第三方插件等）導致的私鑰洩露或資產損失，**本插件及提供方不承擔責任**。

**安全警示**

使用本插件進行代幣創建等操作時，請務必注意：

- **保護私鑰**：切勿在聊天對話中輸入、貼上或洩露私鑰；不要將私鑰分享給任何人或任何第三方。
- **交易錢包僅存小額資金**：用於執行操作的錢包（即提供 PRIVATE_KEY 的錢包）建議只存放少量資金，以降低因洩露或誤操作導致的損失。
- **及時轉出資金**：完成操作後，請及時將交易錢包中的資產轉移到您自己控制的、更安全的錢包或冷錢包中。
- **謹慎安裝 Agent／插件**：下載或安裝任何 Agent、瀏覽器插件或第三方工具時，請確認來源可信，避免惡意插件竊取私鑰或助記詞。

---

### User Agreement & Security Notice (English)

**User Agreement**

**Notice**: Before using this plugin and this skill (including but not limited to token creation), please read the following. **By choosing to continue using this plugin and this skill, you have read, understood, and agreed to this agreement.**

**Plugin nature and limitation of liability**: This plugin provides local-only CLI interaction (private key is used via environment or local config). It **does not collect, upload, or store your private key**. The plugin and its providers **are not liable** for private key disclosure or asset loss due to any cause (including but not limited to tampered plugin, compromised environment, user error, or third-party plugins).

**Security Notice**

When using this plugin for token creation, please:

- **Protect your private key**: Do not type, paste, or expose your private key in chat; do not share it with anyone or any third party.
- **Keep only small amounts in the trading wallet**: The wallet used for operations (the one whose PRIVATE_KEY you provide) should hold only a small amount of funds to limit loss from disclosure or mistakes.
- **Move funds out promptly**: After operations, move assets from the trading wallet to a wallet or cold storage you control.
- **Install agents/plugins carefully**: When installing any agent, browser extension, or third-party tool, verify the source to avoid malware that could steal your private key or seed phrase.

---

## hotfun capability overview

After you agree to the above and confirm to continue, this skill can help you with the following (all via the `hotfun` CLI on Solana):

| Category | Capability | Description |
|----------|-------------|-------------|
| **Create** | Create token | Call API → sign transaction → send to Solana RPC. |

## hotfun CLI

Solana only; all commands output JSON. Run `hotfun --help` for usage.

## Installation (required before use)

**You must install the hotfun CLI before using this skill.** Recommended (global):

```bash
npm install -g @hot-fun/hot-fun-ai@latest
```

After installation, run commands with `hotfun <command> [args]`. If you use a local install instead, use `npx hotfun <command> [args]` from the project root.

## Create token flow

### 1. Ask user for required AND optional information (must be done first)

Before calling `create-token`, the Agent **must** ask the user for all of the following parameters. For optional parameters, the Agent **must still ask** the user whether they want to provide a value — do not skip them silently. If the user declines or leaves them empty, omit them from the command.

| Info | Required | Description |
|------|----------|-------------|
| **Token name** (name) | Yes | Full token name, max 255 chars |
| **Token symbol** (symbol) | Yes | e.g. MTK, DOGE, max 32 chars |
| **Image URL** (image_url) | Yes | Token image URL (e.g. IPFS link) |
| **Description** (description) | No (but must ask) | Token description, e.g. a short intro for the token |
| **X Royalty Party** (x_royalty_party) | No (but must ask) | X (Twitter) username for royalty party |

### 2. Technical flow (done by create-token)

After collecting the above, execute:

```bash
hotfun create-token <name> <symbol> <image_url> [--description "desc"] [--x-royalty-party "username"]
```

Under the hood, the single command handles the full flow:

1. **Call API** — POST (multipart/form-data) to `https://gate.game.com/v3/hotfun/agent/create_pool_with_config` with payer (from PRIVATE_KEY), name, symbol, image_url, agent_ts (current Unix timestamp), agent_sign (Ed25519 signature of agent_ts with private key, base58 encoded), and optional description / x_royalty_party. API returns a base58-encoded Solana transaction.
2. **Sign** — Deserialize the transaction and sign it with the wallet private key.
3. **Send** — Send the signed transaction to Solana RPC and confirm.

Output JSON includes: `txHash`, `wallet`, `baseMint` (new token address), `dbcConfig`, `dbcPool`, `name`, `symbol`, `imageUrl`, `uri`.

Full API and parameters: [references/api-create-token.md](references/api-create-token.md).

## CLI commands

| Need | Command | When |
|------|---------|------|
| **Create token** | `hotfun create-token <name> <symbol> <image_url> [options]` | API → sign → send to Solana. Env: PRIVATE_KEY. |

Chain: **Solana only**.

## PRIVATE_KEY and SOLANA_RPC_URL

**When using OpenClaw**
This skill declares `requires.env: ["PRIVATE_KEY"]` and `primaryEnv: "PRIVATE_KEY"` in metadata; OpenClaw injects them only when an agent runs with **this skill enabled** (other skills cannot access them).

**Required steps:**
1. **Configure private key**: In the Skill management page, set the hot-fun-ai skill's **apiKey** (corresponds to `primaryEnv: "PRIVATE_KEY"`), or set `PRIVATE_KEY` under `skills.entries["hot-fun-ai"].env` in `~/.openclaw/openclaw.json`. Optionally set **SOLANA_RPC_URL** in global env if needed.
2. **Enable this skill**: In the agent or session, ensure the **hot-fun-ai** skill is **enabled**. Only when the skill is enabled will OpenClaw inject **PRIVATE_KEY** into the process; otherwise create commands will fail with missing key.

**When not using OpenClaw (standalone)**
Set **PRIVATE_KEY** and optionally **SOLANA_RPC_URL** via the process environment:

- **.env file**: Put a `.env` file in **the directory where you run the `hotfun` command** (i.e. your project / working directory). The CLI automatically loads `.env` from that current working directory. Use lines like `PRIVATE_KEY=...` and `SOLANA_RPC_URL=...`. Do not commit `.env`; add it to `.gitignore`.
- **Shell export**: `export PRIVATE_KEY=your_base58_key` and optionally `export SOLANA_RPC_URL=https://api.mainnet-beta.solana.com`, then run `npx hotfun <command> ...`.

### Declared and optional environment variables

- **PRIVATE_KEY** (required for write operations): Solana wallet private key in base58 or JSON array format.
- **SOLANA_RPC_URL** (optional): Solana RPC endpoint; if unset, scripts use `https://api.mainnet-beta.solana.com`.

### Execution and install

- **Invocation**: The agent must run commands only via the **hotfun** CLI: `hotfun <command> [args]` or `npx hotfun <command> [args]` (allowed-tools). Do not invoke scripts or `npx tsx` directly; the CLI entry (`bin/hotfun.cjs`) dispatches to the correct script and loads `.env` from the current working directory.
- **Install**: `npm install -g @hot-fun/hot-fun-ai@latest`. Runtime: Node.js. Dependencies (including dotenv, @solana/web3.js, tsx) are declared in the package's `package.json`; global install installs them. No separate install spec beyond the npm package.
