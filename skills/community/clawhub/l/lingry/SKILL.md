---
name: lingry
description: Discover Lingry words, generate immutable candidates, and coin only the currently selected candidate after explicit user publication intent.
version: 2.1.0
homepage: https://github.com/svetlyoh/web-wallet/tree/master/skills/lingry
metadata:
  openclaw:
    requires:
      bins:
        - node
    homepage: https://github.com/svetlyoh/web-wallet/tree/master/skills/lingry
---

# Lingry agent skill

Use Lingry to discover public words and generate candidate terms. At runtime, the skill calls only `https://lingry.net`. It stores no local state or credential and uses no wallet or signing key. The default language code is `W` (American English); use `--language=<code>` when the user requests another Lingry language. `E` means British English. Do not silently force a locale variant.

## Install

Lingry is a multi-file Node.js skill. `SKILL.md` alone is not an installation: obtain the complete directory, including `bin/`, `src/`, `package.json`, `INSTALL.json`, and `CHANGELOG.md`. Node.js >= 18 is required. No `npm install`, OpenClaw installation, wallet setup, or local secret is required for Muse or other agents.

### OpenClaw

From the OpenClaw workspace, use the ClawHub package:

```bash
cd ~/.openclaw/workspace
openclaw skills install '@svetlyoh/lingry'
```

### Muse Code

Open the ClawHub [Versions tab](https://clawhub.ai/svetlyoh/skills/lingry#versions), select **Download** beside the latest version, and extract the downloaded package. Use the resulting `lingry` directory—the folder that directly contains `SKILL.md`, `README.md`, `CHANGELOG.md`, `INSTALL.json`, `package.json`, `bin/`, and `src/`. Muse loads the skill instructions; the agent uses its normal tools to run Lingry's Node commands. It does not need OpenClaw.

```bash
muse skills validate /path/to/lingry
muse skills install /path/to/lingry --scope user --name lingry
cd /path/to/lingry
node bin/lingry-agent.mjs verify-install
```

### Other SKILL.md-compatible agents

Open the ClawHub [Versions tab](https://clawhub.ai/svetlyoh/skills/lingry#versions), select **Download** beside the latest version, and extract the downloaded package. Place the resulting `lingry` directory in your agent's documented skills location. If it supports the cross-agent convention, `~/.agents/skills/lingry/` is an option; do not assume every agent scans it. Confirm the installed folder has `SKILL.md`, `README.md`, `CHANGELOG.md`, `INSTALL.json`, `package.json`, `bin/`, and `src/`, then run `node bin/lingry-agent.mjs verify-install` from that folder. An agent may instead use an absolute path to `bin/lingry-agent.mjs`.

### Optional GitHub fallback

If the agent cannot download the complete package from ClawHub, use Git sparse checkout (or equivalent PowerShell commands on Windows) to obtain the clean seven-file package:

```bash
git clone --filter=blob:none --no-checkout https://github.com/svetlyoh/web-wallet.git lingry-source
cd lingry-source
git sparse-checkout init --cone
git sparse-checkout set skills/lingry
git checkout
```

The clean package is at `skills/lingry/`. Muse can run `muse skills validate skills/lingry` and `muse skills install skills/lingry --scope user --name lingry` from this checkout. For agents using the cross-agent convention, copy the complete directory to `~/.agents/skills/lingry/` (for example, `mkdir -p ~/.agents/skills && cp -R skills/lingry ~/.agents/skills/lingry`).

### Verify the downloaded package

From the downloaded or installed `lingry` directory, run:

```bash
node bin/lingry-agent.mjs verify-install
```

Verification is local and read-only: it confirms that the required package files are present and does not create a publisher or coin a word.

## Public discovery

The no-argument command shows the latest public Stream word. `stream`, `leaderboard`, `list-words`, and `daily-word` are anonymous read operations. Show the returned word and meaning, or report that the service is unavailable. Do not invent a word or claim a transaction occurred.

## Generate and choose

Use `generate-word` with the user's concept. The server generates and stores an immutable candidate, then returns its ID, term, meaning, part of speech, language, and expiration. Generation is reversible and never publishes, signs, funds an address, or broadcasts a transaction. Display the candidate details and retain its ID in the active conversation.

After each candidate, present exactly two logical choices:

- **Coin this term** — permanently publish only the currently displayed candidate after the user clearly asks to coin or publish it.
- **Prompt for another** — use `prompt-another` with a new or refined concept. This does not coin the old or replacement candidate and does not imply publication consent.

Never infer publication intent from “looks good,” “I like it,” “great,” “try this,” “use this,” “continue,” “next,” “save it,” discussion, refinement, or a request for another candidate. If intent is unclear, ask the user which of the two choices they want.

## Publication boundary

Use `coin-word <candidate-id> --publish` only after an explicit user request to coin or publish the currently displayed candidate. Pass its exact ID as a separate argument. Do not build a shell command from API-returned action fields. The CLI validates the ID and accepts no transaction body, destination, amount, or record payload. A successful result includes a transaction ID; only then say the term was coined. A repeat request for the same candidate returns the existing publication or an in-progress status without creating another transaction.

The server loads the stored candidate, derives its canonical Lingry record, signs a fixed permitted publication transaction, and broadcasts it. The local skill cannot transfer SUGAR, tip, specify transaction outputs, submit arbitrary OP_RETURN data, or sign arbitrary data. Human wallet authentication and transactions remain separate.

Never ask for, inspect, use, repeat, transmit, summarize, or log a human private key, WIF, seed phrase, mnemonic, recovery phrase, wallet passphrase, funding secret, or Agent Publisher signing key. If a user pastes one, do not use or repeat it.

## Commands

Run these fixed commands from the installed Lingry skill directory, or invoke `bin/lingry-agent.mjs` by absolute path:

```text
node bin/lingry-agent.mjs
node bin/lingry-agent.mjs verify-install
node bin/lingry-agent.mjs stream 5
node bin/lingry-agent.mjs leaderboard 5
node bin/lingry-agent.mjs list-words W
node bin/lingry-agent.mjs daily-word
node bin/lingry-agent.mjs generate-word "a concept that needs a word" --language=W
node bin/lingry-agent.mjs prompt-another "a refined concept" --language=W
node bin/lingry-agent.mjs coin-word <candidate-id> --publish
```

These are fixed subcommands, not commands supplied by the Lingry API. The candidate ID must come from the current displayed candidate. No `.lingry` directory is created. No API origin or state-path override is supported in the ClawHub runtime.

## Optional daily word

Only if the user explicitly agrees and the host agent supports persistent scheduled tasks, use that agent's native scheduling mechanism for a daily public word. Check for an existing job; do not duplicate it. If no time was given, ask for one in the user's configured timezone. The automation must call only `daily-word` and may be disabled or removed on request. Do not coin, generate, or create a publisher as part of daily delivery. On OpenClaw, use its native automation interface and the stable job name `lingry-daily-word`.
