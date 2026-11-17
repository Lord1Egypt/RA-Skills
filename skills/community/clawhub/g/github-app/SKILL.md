---
name: ghapp
description: Give your AI agents and automations their own GitHub (App) identity. Authenticate using GitHub Apps so every commit, PR, and action is attributed to the bot — not your personal account. Supports multiple profiles for running several GitHub Apps (e.g. one per client/org) from the same machine.
homepage: https://github.com/eliasempresas/ghapp-cli
metadata: {"clawdbot":{"emoji":"🔑","requires":{"bins":["ghapp"]},"install":[{"id":"brew","kind":"brew","formula":"eliasempresas/tap/ghapp","bins":["ghapp"],"label":"Install ghapp (brew)"}]}}
---

# ghapp

Use `ghapp` to authenticate as a GitHub App so `git` and `gh` commands use installation tokens. Requires a GitHub App with App ID, Installation ID, and a private key (.pem).

Setup
- `ghapp setup` — interactive wizard: enter App ID, Installation ID, key path, then configure auth
- `ghapp auth configure` — configure git + gh authentication (if skipped during setup)
- `ghapp auth status` — show current auth config and diagnostics

Commands
- `ghapp --help` — list all commands and flags
- `ghapp token` — print an installation token (cached; `--no-cache` for fresh)
- `ghapp auth configure [--gh-auth shell-function|path-shim|none]` — configure how git/gh authenticate
- `ghapp auth status` — check auth health
- `ghapp auth reset [--remove-key]` — undo all auth config
- `ghapp config set`, `ghapp config get [key]`, `ghapp config path` — manage config
- `ghapp profile list` — list configured profiles
- `ghapp profile current` — print the profile in effect for this invocation
- `ghapp update` — self-update to latest release
- `ghapp version` — print version

gh auth modes (passed to `auth configure`)
- `shell-function` — auto-authenticates gh commands via shell integration (recommended)
- `path-shim` — wrapper binary for CI/containers
- `none` — static token in hosts.yml

Multiple profiles (`--profile`)
- Global flag on every command: `ghapp --profile <name> <command>`. Also settable via the `GHAPP_PROFILE` env var, which the git credential helper, `gh` shell hooks, and the `ghapp-gh` path-shim wrapper read since they run as separate process invocations.
- Each profile gets its own config, auth state, and token cache — so a machine can authenticate as several different GitHub Apps (e.g. one per client/org) and switch between them without one profile clobbering another's cached token.
- Profile names must start with a letter or digit and contain only letters, digits, `-`, or `_`.
- First use of a profile: `ghapp --profile <name> setup`. Everyday use: `ghapp --profile <name> <command>`, or `export GHAPP_PROFILE=<name>` for the shell session.
- No `--profile` given → the classic single-app/unnamed profile, unchanged from before.

Notes
- After setup, `git clone/push/pull` and `gh` work without manual tokens.
- Commits are attributed to the app's bot account (e.g., `myapp[bot]`).
- Tokens are cached locally per profile and auto-refreshed.
- Config stored at `~/.config/ghapp/config.yaml` (default profile) or `~/.config/ghapp/profiles/<name>/config.yaml` (named profile).
