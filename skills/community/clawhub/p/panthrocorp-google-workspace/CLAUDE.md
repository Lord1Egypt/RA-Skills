# google-workspace

## Overview

Gmail (read-only), Contacts (read-only), Calendar (configurable), Drive (configurable with comments), Docs (configurable), and Sheets (configurable) for OpenClaw agents. Security-first design: write operations are always opt-in and gated at code, config, and GCP levels.

## Architecture

- `cmd/` — Cobra CLI. Service commands (`gmail`, `calendar`, `contacts`, `drive`, `docs`, `sheets`, `auth`, `config`) register on `rootCmd`. Helper functions `gmailClient()`, `calendarClient()`, `contactsClient()`, `driveClient()`, `docsClient()`, `sheetsClient()` handle config loading, scope validation, token decryption, and API client construction inline.
- `internal/config/config.go` — JSON config model with a unified `ServiceMode` type (`off`/`readonly`/`readwrite`) used by Calendar, Drive, Docs, and Sheets. Gmail and Contacts are simple on/off booleans. `Config.OAuthScopes()` derives the OAuth scope list from the current config; scopes expand as services are enabled. Changing any value requires re-authentication to issue a new token with the updated scopes. Custom `UnmarshalJSON` handles backwards compatibility for the Drive field (previously a bool).
- `internal/oauth/` — OAuth2 Desktop flow with a localhost redirect. `InteractiveLogin` prompts for the **code value only** (the part after `code=` and before `&scope=` in the redirect URL). The browser fails to load `http://localhost`, and the operator copies the code parameter value from the URL bar. This differs from zoho-mail, which takes the full redirect URL.
- `internal/google/` — Thin typed wrappers around Google API services. Each wrapper exposes only the operations the skill permits. Write methods on multi-mode services (Calendar, Drive, Docs, Sheets) check `mode != ModeReadWrite` at runtime and return an error. Gmail and Contacts wrappers have no write methods at all.
- `internal/crypto/` — AES-256-GCM with HKDF-SHA256 key derivation. Wire format: `salt (16B) || nonce (12B) || ciphertext+tag`.

## Scope enforcement (three layers)

1. Code: Gmail and Contacts wrappers have no write methods. Calendar, Drive, Docs, and Sheets write methods guard on `config.ModeReadWrite`.
2. Config: CLI commands check mode before calling the client. Readonly config never requests write scopes, so the token physically cannot perform write operations.
3. Google Cloud project: only Gmail API, Calendar API, People API, Google Drive API, Google Docs API, and Google Sheets API should be enabled, providing server-side enforcement.

## ServiceMode config model

`ServiceMode` is a unified string type with three values: `off`, `readonly`, `readwrite`. `CalendarMode` is a type alias for backwards compatibility. The Drive field was previously a `bool`; custom `UnmarshalJSON` on Config maps `true`→`readonly` and `false`→`off` for legacy configs. This is a one-way migration: once re-saved, old binaries cannot read the new format.

## Required environment variables

| Variable | Purpose |
|----------|---------|
| `GOOGLE_WORKSPACE_TOKEN_KEY` | Passphrase for AES-256-GCM token encryption |
| `GOOGLE_CLIENT_ID` | Google OAuth2 client ID |
| `GOOGLE_CLIENT_SECRET` | Google OAuth2 client secret |

Config directory defaults to `~/.openclaw/credentials/google-workspace/`. Override with `GOOGLE_WORKSPACE_CONFIG_DIR` or `--config-dir`.

## OAuth flow note

`InteractiveLogin` expects only the `code` value from the redirect URL, not the full URL. After the browser fails to load `http://localhost`, the operator copies the value of the `code=` parameter only and pastes it into the terminal. See `internal/oauth/oauth.go` for the implementation.

## Mode and scope changes

If any `ServiceMode` changes (e.g. Drive `readonly` to `readwrite`), the stored token was issued with the old scopes. The operator must run `google-workspace auth login` again to issue a new token with the expanded scopes. The binary does not detect scope mismatches at runtime.

## Drive auto-detection

`DriveClient.DownloadFile` checks the file's MIME type before downloading. Google Workspace types (`application/vnd.google-apps.document`, `.spreadsheet`, `.presentation`) are exported via `Files.Export` (Docs as plain text, Sheets as CSV, Slides as plain text). All other files use `Files.Get` with `alt=media` for a raw byte download.

## Drive comments

All comments (on any file type including Docs and Sheets) are managed via the Drive API (`drive comment`, `drive comments list`, `drive comment reply`). The Google Docs API does not have a comments endpoint. Drive comments require `readwrite` mode (full `drive` scope).

## Docs editing

`docs edit` supports three modes via flags: `--insert-text` with optional `--index` for positional insert, `--find`/`--replace-with` for find-and-replace-all, and `--requests-json` for raw Docs API batch updates. Only one mode per invocation.
