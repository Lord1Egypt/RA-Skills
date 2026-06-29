---
name: lingry
description: Create, discover, and coin Lingry words with a local Sugarchain wallet, explicit terminal approval, and no wallet-passphrase exposure to OpenClaw.
version: 1.0.7
homepage: https://lingry.net
metadata:
  openclaw:
    requires:
      bins:
        - node
        - npm
    envVars:
      - name: LINGRY_API_BASE_URL
        required: false
        description: Optional HTTPS Lingry API base URL. Defaults to https://lingry.net.
      - name: LINGRY_KEYSTORE_PATH
        required: false
        description: Optional path to the local encrypted Lingry keystore. Defaults to ~/.lingry/keystore.json.
      - name: LINGRY_AGENT_STATE_PATH
        required: false
        description: Optional path for non-secret local Lingry candidate state.
      - name: LINGRY_DEFAULT_LANGUAGE_CODE
        required: false
        description: Default Lingry language code. Defaults to W.
      - name: LINGRY_MAX_AUTO_COIN_FEE_SATOSHIS
        required: false
        description: Maximum local coining fee value used when preparing a request. Signing still requires terminal approval.
      - name: LINGRY_COIN_FEE_SATOSHIS
        required: false
        description: Local coining fee used when preparing a candidate coin request.
      - name: LINGRY_MAX_AUTO_TIP_SATOSHIS
        required: false
        description: Maximum permitted tip amount for workflows that prepare tips.
      - name: LINGRY_AGENT_REQUEST_TIMEOUT_MS
        required: false
        description: Timeout for Lingry HTTP requests.
      - name: LINGRY_SESSION_TOKEN
        required: false
        description: Optional local session token for authenticated Lingry API calls. Never print or log it.
---

# Lingry ClawHub Skill

Use this skill when a user wants to inspect Lingry API health, list public Lingry words, generate account-bound Lingry word candidates, prepare a starter-grant claim, or prepare a candidate coining request. The OpenClaw agent must never unlock a wallet, request a wallet passphrase, sign a transaction, or broadcast a transaction.

This is the standalone ClawHub distribution. It must run only from the files included in this package: `bin/lingry-agent.mjs`, `bin/lingry-wallet.mjs`, `src/`, `package.json`, and `package-lock.json`. Never fall back to another Lingry install, a source checkout, a sibling directory, or an old local skill.

## Canonical API URL

The built-in API base URL is:

```text
https://lingry.net
```

Only override it with `LINGRY_API_BASE_URL` when the user deliberately provides another valid HTTPS Lingry API host.

## Agent Commands

These commands are safe for an OpenClaw agent process:

```bash
node bin/lingry-agent.mjs
node bin/lingry-agent.mjs status
node bin/lingry-agent.mjs doctor
node bin/lingry-agent.mjs verify-install
node bin/lingry-agent.mjs auth-status
node bin/lingry-agent.mjs address
node bin/lingry-agent.mjs list-words W
node bin/lingry-agent.mjs leaderboard
node bin/lingry-agent.mjs stream
node bin/lingry-agent.mjs generate-word "a word for a tiny useful idea"
node bin/lingry-agent.mjs create-word-draft <term> <part-of-speech> <meaning>
node bin/lingry-agent.mjs prepare-starter-grant
node bin/lingry-agent.mjs prepare-coin <candidate-id-or-term>
node bin/lingry-agent.mjs get-request <request-id>
node bin/lingry-agent.mjs get-transaction <request-id-or-intent-id>
```

`status` is the default no-argument command. It shows wallet address if configured, API health, public word availability, session-token status, the last locally saved candidate, and the last locally saved coin result. It must never display secrets or make a transaction.

## Public Social Reads

When the user asks to show Lingry's leaderboard, run:

```bash
node bin/lingry-agent.mjs leaderboard
```

When the user asks to show the latest Lingry stream, run:

```bash
node bin/lingry-agent.mjs stream
```

These commands are public read-only calls. They do not need a session token, wallet, private key, passphrase, browser session, or signing approval. Render the returned words as a concise numbered list, mention the snapshot time, and state clearly when data is stale. Do not claim the stream is live or real-time; it refreshes from the latest completed hourly snapshot. Do not scrape `lingry.net/leaderboard`, `lingry.net/stream`, browser cookies, browser storage, or page HTML. Do not expose raw API payloads unless the user asks for JSON.

## Local Wallet Commands

These commands must be run by the user from a private interactive terminal, not by OpenClaw chat, services, cron jobs, pipes, or background agents:

```bash
node bin/lingry-wallet.mjs setup
node bin/lingry-wallet.mjs create-wallet
node bin/lingry-wallet.mjs import-wallet
node bin/lingry-wallet.mjs inspect
node bin/lingry-wallet.mjs claim-grant <request-id>
node bin/lingry-wallet.mjs approve <request-id>
```

Wallet creation, wallet import, starter-grant signing, transaction signing, and broadcasting are terminal-only. The user must review the details and type `BROADCAST` before anything is signed or submitted.

## First Launch In OpenClaw

When a user first launches the Lingry skill, guide them through setup without asking them to paste secrets into chat:

1. Open `https://lingry.net`, create or open a Lingry wallet, log in, open `Menu` then `Keys`, and copy the Lingry private/login key only for local terminal import. The wallet address on `lingry.net` must match the wallet imported on the Ubuntu OpenClaw PC.
2. On the Ubuntu OpenClaw PC, fix ownership if previous commands used root:

```bash
sudo chown -R "$USER:$USER" "$HOME/.openclaw"
sudo chown -R "$USER:$USER" "$HOME/.lingry" 2>/dev/null || true
chmod 700 "$HOME/.openclaw"
chmod 700 "$HOME/.lingry" 2>/dev/null || true
chmod -R u+rwX,go-rwx "$HOME/.lingry" 2>/dev/null || true
```

3. Import the Lingry private/login key into the local encrypted OpenClaw wallet:

```bash
cd "$HOME/.openclaw/skills/lingry"
unset LINGRY_WALLET_PASSPHRASE
node bin/lingry-wallet.mjs import-wallet
```

The WIF/private key and wallet passphrase prompts are hidden; typed or pasted text will not appear.

4. Verify the local wallet and token status:

```bash
cd "$HOME/.openclaw/skills/lingry" && node bin/lingry-wallet.mjs inspect && node bin/lingry-agent.mjs auth-status
```

5. Return to `https://lingry.net`, log in with the same Lingry private/login key and matching wallet address, open `Menu` then `API Session`, create an API session token, and copy it. Browser-created tokens last about 30 days.
6. Put the token in the OpenClaw runtime environment file with a hidden terminal prompt, not in chat:

```bash
umask 077
mkdir -p "$HOME/.openclaw"

read -rsp "Paste Lingry session token: " NEW_LINGRY_TOKEN
printf '\n'

tmpfile="$(mktemp)"
[ -f "$HOME/.openclaw/.env" ] && grep -v '^LINGRY_SESSION_TOKEN=' "$HOME/.openclaw/.env" > "$tmpfile"
printf 'LINGRY_SESSION_TOKEN=%s\n' "$NEW_LINGRY_TOKEN" >> "$tmpfile"
mv "$tmpfile" "$HOME/.openclaw/.env"
chmod 600 "$HOME/.openclaw/.env"

unset NEW_LINGRY_TOKEN
unset LINGRY_SESSION_TOKEN
```

Then run:

```bash
systemctl --user unset-environment LINGRY_SESSION_TOKEN 2>/dev/null || true
openclaw gateway restart
set -a && . "$HOME/.openclaw/.env" && set +a
cd "$HOME/.openclaw/skills/lingry" && node bin/lingry-agent.mjs auth-status
```

If a direct terminal test without sourcing `.env` says `token_configured: false`, that only means the current shell has not loaded OpenClaw's runtime `.env`; source the file as shown above or test from OpenClaw after restarting the gateway.

For future refreshes, tell the user to sign in to `https://lingry.net` with the same Lingry private/login key and matching wallet address, create a new token from `Menu` then `API Session`, repeat the hidden terminal paste flow above, and restart OpenClaw.

## Troubleshooting Session Tokens

If terminal `auth-status` accepts a new token but OpenClaw chat still reports an old expiry, the chat-side gateway is still using a stale environment. Do not ask the user to paste the token into chat. Give them this private terminal repair flow:

```bash
cd "$HOME/.openclaw/skills/lingry"

umask 077
mkdir -p "$HOME/.openclaw"

read -rsp "Paste the NEW Lingry session token: " NEW_LINGRY_TOKEN
printf '\n'

tmpfile="$(mktemp)"
[ -f "$HOME/.openclaw/.env" ] && grep -v '^LINGRY_SESSION_TOKEN=' "$HOME/.openclaw/.env" > "$tmpfile"
printf 'LINGRY_SESSION_TOKEN=%s\n' "$NEW_LINGRY_TOKEN" >> "$tmpfile"
mv "$tmpfile" "$HOME/.openclaw/.env"
chmod 600 "$HOME/.openclaw/.env"

unset LINGRY_SESSION_TOKEN
unset NEW_LINGRY_TOKEN

systemctl --user unset-environment LINGRY_SESSION_TOKEN 2>/dev/null || true
openclaw gateway restart
```

Then verify:

```bash
cd "$HOME/.openclaw/skills/lingry"
set -a && . "$HOME/.openclaw/.env" && set +a
node bin/lingry-agent.mjs auth-status
```

If OpenClaw chat still shows the old expiry, restart the gateway process fully:

```bash
openclaw gateway stop
sleep 3
openclaw gateway start
```

## Troubleshooting Coin Approval

If wallet approval fails after `BROADCAST` with `Sugarchain RPC is not configured`, explain that the configured Lingry API host cannot broadcast signed Sugarchain transactions. Do not ask for the wallet passphrase or private key. Have the user run:

```bash
cd "$HOME/.openclaw/skills/lingry"
node bin/lingry-agent.mjs doctor
```

Current wallet helpers preflight `/v1/broadcast/status` before asking for the wallet passphrase. If broadcast is unavailable, the Lingry API operator must configure Sugarchain broadcast or update the API to a version with public Sugar API broadcast fallback.

## Anonymous And Authenticated Commands

These commands work anonymously or only use local public wallet metadata:

- `status`
- `doctor`
- `verify-install`
- `auth-status`
- `address`
- `list-words`
- `leaderboard`
- `stream`
- `prepare-starter-grant`
- `get-request`
- `get-transaction` for a local request id
- `node bin/lingry-wallet.mjs inspect`
- `node bin/lingry-wallet.mjs setup`
- `node bin/lingry-wallet.mjs create-wallet`
- `node bin/lingry-wallet.mjs import-wallet`
- `node bin/lingry-wallet.mjs claim-grant <request-id>`

These commands require `LINGRY_SESSION_TOKEN`:

- `generate-word`
- `prompt-word`
- `create-word-draft`
- `prepare-coin`
- `get-transaction` when querying an authenticated Lingry intent
- `node bin/lingry-wallet.mjs approve <request-id>` for candidate submission

`LINGRY_SESSION_TOKEN` is optional in this skill metadata because public read commands, install checks, status checks, and local wallet setup do not require it.

## Optional Lingry Account Session

`LINGRY_SESSION_TOKEN` is needed for account-bound generation, candidate storage, draft creation, and candidate-based coining.

Browser-created Lingry API session tokens last about 30 days. The user refreshes them by signing in to `https://lingry.net` with the same Lingry private/login key and matching wallet address, then opening `Menu` and `API Session`. Never paste the token into OpenClaw chat. Never place it in GitHub, `SKILL.md` examples, shell history, or a world-readable file. The user must obtain it through a deliberate Lingry browser/account flow. Do not implement or use browser-cookie scraping, browser-local-storage scraping, browser-session scraping, profile-file scraping, or automatic session-token extraction.

## Safety Rules

- Never print, inspect, summarize, export, transmit, or log private keys, WIFs, seed phrases, wallet passphrases, keystore contents, API tokens, environment dumps, Cloudflare secrets, funding-wallet WIFs, or RPC credentials.
- Never request a wallet passphrase in an OpenClaw agent process, shell export, `.env` file, systemd service, or cron job.
- Never include wallet passphrases in skill frontmatter, examples, scripts, services, or scheduled jobs.
- Do not include, request, or run a private-key export command.
- Never scrape browser cookies, browser local storage, browser session storage, or profile files to obtain a Lingry session token.
- Never silently install cron jobs, services, background workers, public tunnels, router port forwards, or production deployments.
- Never use `curl | bash`, `wget | bash`, opaque remote installers, or a runtime clone of the full Lingry repository.
- Never claim a starter grant, coining transaction, tip, or payment succeeded unless the API or node response confirms it.
- Do not invent balances, confirmations, addresses, transaction IDs, or payment outcomes.

## Transaction Boundary

The agent prepares non-secret requests only. It may read public wallet metadata from `~/.lingry/keystore.json`, request public Lingry/Sugarchain data, and save a pending request under `~/.lingry/pending/`. It must not decrypt the keystore or build a signed raw transaction.

The wallet helper loads the encrypted keystore only inside a private terminal after the user reviews the request and types `BROADCAST`. It saves only non-secret result metadata under `~/.lingry/results/`.
