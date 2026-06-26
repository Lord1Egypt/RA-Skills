---
name: openclaw-credential-vault
description: Encrypted credential management for OpenClaw — keeps API keys, tokens, and passwords out of the AI agent's context window. AES-256-GCM encryption, subprocess-scoped injection, automatic output scrubbing.
version: 1.0.0-beta.5
metadata:
  openclaw:
    emoji: "🔐"
    homepage: https://github.com/karanuppal/openclaw-credential-vault
    requires:
      bins:
        - openclaw
      config:
        - ~/.openclaw/vault/tools.yaml
        - ~/.openclaw/vault/*.enc
    install:
      - id: openclaw-credential-vault
        kind: node
        package: openclaw-credential-vault
        bins: [openclaw-credential-vault]
        label: Install Credential Vault plugin (npm)
---

# OpenClaw Credential Vault

Encrypted credential management for OpenClaw. Keeps API keys, tokens, and passwords out of the AI agent's context window — where they could be exfiltrated, leaked into transcripts, or exposed through tool output.

## What You Get

- **Credentials never enter the AI's context.** Decrypted and injected only into the specific subprocess that needs them, then scrubbed from output before the agent sees it.
- **Encryption at rest.** Each credential individually encrypted with AES-256-GCM, Argon2id key derivation.
- **Automatic output scrubbing.** Multiple independent scrubbing layers catch credentials in tool output, outbound messages, and session transcripts.
- **~700 tests** across 36 files covering crypto, injection, scrubbing, adversarial attacks, and end-to-end scenarios.
- **Open source.** Full source code at [GitHub](https://github.com/karanuppal/openclaw-credential-vault) — review hook/injection/scrubbing implementation before installing.

## Storage and File Access

The vault stores all data under `~/.openclaw/vault/`:

- `~/.openclaw/vault/*.enc` — Individual encrypted credential files (AES-256-GCM, one per tool). File permissions are set to owner-only (600).
- `~/.openclaw/vault/tools.yaml` — Injection rules mapping tools to credentials (which command patterns trigger which credential injection, which URL patterns get auth headers).
- `~/.openclaw/vault/.vault-meta.json` — Vault metadata (initialization timestamp, version).
- `~/.openclaw/vault/audit.log` — Credential access audit log.

No environment variables are required. The vault derives its encryption key from the system and does not store keys in env vars or config files.

## Install

Install the plugin via npm:

```bash
npm install -g openclaw-credential-vault
```

Then restart the gateway to load the plugin. The plugin registers four OpenClaw hooks:

- `before_exec` — Injects credentials into subprocess environment for matching commands
- `after_exec` — Scrubs credential patt[VAULT:gmail-app]ut
- `before_send` — Scrubs credentials from outbound messages
- `session_transcript` — Scrubs credentials from session transcripts

To review the hook implementations before installing, see [src/hooks/](https://github.com/karanuppal/openclaw-credential-vault/tree/main/src/hooks) in the GitHub repository.

## Quick Start

```bash
# Initialize the vault
openclaw vault init

# Add a credential (interactive — picks the right injection type)
openclaw vault add github --key "ghp_your_token_here"

# Verify it works end-to-end (injection + scrubbing)
openclaw vault test github

# Add more
openclaw vault add stripe --key "sk_live_..."
openclaw vault add npm --key "npm_..."
```

That's it. Your agent can now use `gh`, call Stripe APIs, and publish npm packages without ever seeing the credentials.

## How It Works

When the agent runs a tool like `gh pr list`:

1. **before_exec hook** matches `gh` against `tools.yaml` injection rules
2. Decrypts `~/.openclaw/vault/github.enc` using the derived key
3. Injects the token as `GITHUB_TOKEN` into the subprocess environment only
4. `gh` runs with the credential, returns results
5. The subprocess exits — the credential dies with it
6. **after_exec hook** scrubs output for any credential patterns before the agent sees it
7. The agent gets clean results — no credential anywhere in context

For API calls, the `before_exec` hook injects Authorization headers into matching URL patterns (configured in `tools.yaml`).

## Commands

- `vault init` — Initialize vault and create `~/.openclaw/vault/` directory
- `vault add <tool> --key <cred>` — Add a credential (interactive usage selection: API, CLI)
- `vault list` — Show all stored credentials and status
- `vault show <tool>` — Show credential details and injection config
- `vault test <tool>` — Verify injection and scrubbing work end-to-end
- `vault rotate <tool> --key <new>` — Rotate a credential (re-encrypts in place)
- `vault rotate --check` — Show credentials overdue for rotation
- `vault remove <tool>` — Remove credential file and injection rules

### Non-Interactive Mode

```bash
# API header injection
openclaw vault add stripe --key "sk_live_..." --use api --url "api.stripe.com/*" --yes

# CLI env injection
openclaw vault add github --key "ghp_..." --use cli --command gh --env GITHUB_TOKEN --yes
```

## Security Model

1. **Agent never sees credentials** — injection happens in `before_exec` hook, not in the agent's context
2. **Encryption at rest** — AES-256-GCM with per-credential salts, stored in `~/.openclaw/vault/*.enc`
3. **Key derivation** — Argon2id (memory-hard, resistant to GPU cracking)
4. **Subprocess isolation** — credentials exist only in the child process environment, die when it exits
5. **Output scrubbing** — 4 independent hooks (`after_exec`, `before_send`, `session_transcript`, plus pattern-based fallback) catch credential leaks
6. **Audit logging** — all credential access logged to `~/.openclaw/vault/audit.log`
7. **Open source** — full source code and 700-test suite available for review at [GitHub](https://github.com/karanuppal/openclaw-credential-vault)

## Links

- GitHub: https://github.com/karanuppal/openclaw-credential-vault
- npm: https://www.npmjs.com/package/openclaw-credential-vault
- Issues: https://github.com/karanuppal/openclaw-credential-vault/issues
