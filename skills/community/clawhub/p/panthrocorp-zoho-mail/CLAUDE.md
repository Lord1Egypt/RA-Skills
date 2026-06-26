# zoho-mail

## Overview

Full read/write Zoho Mail skill for OpenClaw agents. Unlike the google-workspace skill, this has no read-only restriction: it can list, read, send, reply, delete, and mark messages.

## Architecture

- `cmd/` — Cobra CLI. Subcommand groups `mail`, `folders`, `auth`, and `config` each register on `rootCmd`. `zohoClient()` in `cmd/mail.go` centralises config loading, token decryption, and API client construction.
- `internal/zoho/client.go` — Thin HTTP wrapper over the Zoho Mail REST API (`https://mail.zoho.eu/api`). Account ID is discovered on first API call via `GET /accounts` and cached in `Client.accountID`. All message and folder operations path-encode this ID.
- `internal/oauth/oauth.go` — OAuth2 flow with a localhost redirect (`http://localhost:8080/callback`). `InteractiveLogin` asks the operator to paste the **full redirect URL** back into the terminal (e.g. `http://localhost:8080/callback?code=...`). The code is then extracted from the URL. This differs from google-workspace, which asks for the code value only.
- `internal/crypto/` — AES-256-GCM with HKDF-SHA256 key derivation. Wire format: `salt (16B) || nonce (12B) || ciphertext+tag`. Same pattern as google-workspace.
- `persistingTokenSource` in `cmd/mail.go` — wraps the OAuth2 token source and saves a refreshed token back to disk whenever the access token changes. This keeps the stored token current without manual re-authentication.

## Key differences from google-workspace

- Full write access. No service modes and no config-level gating.
- OAuth redirect URL is `http://localhost:8080/callback`. The operator pastes the **full redirect URL** (not just the code).
- EU data centre only: all API and auth endpoints use `zoho.eu` domains.
- Config is minimal: only `email` field (`config.json`). No scope selection logic.

## Required environment variables

| Variable | Purpose |
|----------|---------|
| `ZOHO_MAIL_TOKEN_KEY` | Passphrase for AES-256-GCM token encryption |
| `ZOHO_CLIENT_ID` | Zoho API Console client ID |
| `ZOHO_CLIENT_SECRET` | Zoho API Console client secret |

Config directory defaults to `~/.openclaw/credentials/zoho-mail/`. Override with `ZOHO_MAIL_CONFIG_DIR` or `--config-dir`.

## OAuth scopes

`ZohoMail.messages.ALL`, `ZohoMail.folders.ALL`, `ZohoMail.accounts.READ` — defined in `internal/oauth/oauth.go`.
