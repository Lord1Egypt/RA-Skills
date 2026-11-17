# Lingry agent skill

The skill discovers public Lingry words, requests a server-generated word candidate, and publishes only the selected immutable candidate after an explicit user request. The service origin is fixed at `https://lingry.net`.

## Install

`openclaw/skills/lingry/` is the canonical source directory. The clean GitHub-import folder for ClawHub is [`skills/lingry/`](https://github.com/svetlyoh/web-wallet/tree/master/skills/lingry); it mirrors the staged release, without development files. The skill is multi-file: `SKILL.md` alone cannot run it. Node.js >= 18 is required; there are no npm runtime dependencies, so no `npm install` is needed. The version source of truth is the source directory's `package.json`.

### OpenClaw

```bash
cd ~/.openclaw/workspace
openclaw skills install '@svetlyoh/lingry'
```

### Muse Code

Open the ClawHub [Versions tab](https://clawhub.ai/svetlyoh/skills/lingry#versions), select **Download** beside the latest version, and extract the downloaded package. Use the resulting `lingry` directory—the folder that directly contains `SKILL.md`, `README.md`, `CHANGELOG.md`, `INSTALL.json`, `package.json`, `bin/`, and `src/`:

```bash
muse skills validate /path/to/lingry
muse skills install /path/to/lingry --scope user --name lingry
cd /path/to/lingry
node bin/lingry-agent.mjs verify-install
```

Muse loads the instructions; its agent runs the Node CLI through normal tools. OpenClaw is not required.

### Other agents

Open the ClawHub [Versions tab](https://clawhub.ai/svetlyoh/skills/lingry#versions), select **Download** beside the latest version, and extract the package. Place the resulting `lingry` directory in your agent's supported skills directory. `~/.agents/skills/lingry/` is one option for agents that support the cross-agent convention. Run `node bin/lingry-agent.mjs verify-install` from the installed directory.

### Optional GitHub fallback

If the agent cannot download the complete package from ClawHub, use Git sparse checkout to obtain the clean seven-file package:

```bash
git clone --filter=blob:none --no-checkout https://github.com/svetlyoh/web-wallet.git lingry-source
cd lingry-source
git sparse-checkout init --cone
git sparse-checkout set skills/lingry
git checkout
cd skills/lingry
node bin/lingry-agent.mjs verify-install
```

From the checkout, copy `skills/lingry/` to the agent's documented skills location if needed. On Windows, use the equivalent PowerShell copy commands.

## Workflow

Use `generate-word "a concept"` to obtain an immutable candidate. Show the term, meaning, part of speech, and language. Then offer **Coin this term** and **Prompt for another**. `prompt-another "new concept"` only generates a new candidate. To publish, the user must explicitly request coining of the currently displayed candidate; the agent then uses `coin-word <candidate-id> --publish`. The server returns a transaction ID after publication. Retry with the same ID is idempotent.

`W` is Lingry's American English code and the default. `E` is British English. Pass `--language=<code>` to select another supported language.

## Security model

The client stores no state or long-lived authentication secret. Generating a candidate creates no Agent Publisher identity, transaction, or publication. It never asks for or handles a user's wallet secrets.

The coin request contains only a strictly validated, high-entropy candidate ID and an empty JSON body. The client cannot construct arbitrary cryptocurrency transactions, send SUGAR, specify transaction outputs, submit arbitrary OP_RETURN data, or perform general blockchain signing. Canonical word-record construction, blockchain signing, and broadcast are performed by Lingry's server. The server creates or reuses its own publisher only when coining is requested and enforces publication by candidate ID.

The client rejects redirects and responses over 128 KiB, uses a fixed HTTPS origin, and presents sanitized errors. It never runs API-returned text as commands. A candidate expires after the server's configured lifetime.

This source repository retains tests and development files. Publishers must use the staged `dist/clawhub-lingry/` payload, not blindly upload the source directory. See the repository's [release checklist](https://github.com/svetlyoh/web-wallet/blob/master/openclaw/skills/lingry/RELEASING.md) for the manual ClawHub and GitHub Release steps. Server deployment and skill publication are separate operations.
