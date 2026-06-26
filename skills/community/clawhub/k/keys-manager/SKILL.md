---
name: keys-manager
description: Manage API keys locally from the terminal using the `keys` CLI. Use when users want to store, retrieve, search, import, export, or organize API keys and secrets. Handles .env file operations, profile-based key isolation, and secure key management workflows.
metadata:
  openclaw:
    requires:
      bins:
        - keys
    primaryEnv: ""
---

# Keys Manager

A skill for managing API keys and secrets locally using the `keys` CLI tool.

## Installation

The `keys` CLI must be installed first:

```bash
brew install stym06/tap/keys
```

Or with Go:

```bash
go install github.com/stym06/keys@latest
```

## Commands

### Store a key

```bash
keys add <name> <value>
```

If the key already exists, the user is prompted to overwrite, edit, or cancel.

### Retrieve a key

```bash
keys get <name>       # print value directly
keys get              # interactive typeahead picker
```

### Browse keys interactively

```bash
keys see
```

Opens a TUI with fuzzy search, checkboxes, clipboard copy, and age indicators.

- `space` — toggle selection
- `tab` — copy selected as `KEY=VAL`
- `ctrl+y` — copy selected as `export KEY=VAL`
- `ctrl+e` — export selected to `.env` file
- `enter` — add a new key (when no matches found)
- `esc` — quit

### Masked view

```bash
keys peek
```

Same as `see` but values are hidden as `***`. Press `r` to reveal individual keys. Useful for screen-sharing.

### Edit a key

```bash
keys edit <name>
```

Opens a TUI editor. `tab` switches fields, `enter` saves, `esc` cancels.

### Delete a key

```bash
keys rm <name>
```

### Export keys

```bash
keys env              # interactive selector, writes .env file
keys expose           # print export statements to stdout
```

### Import from .env

```bash
keys import <file>
```

Parses `.env` files — handles comments, quotes, and `export` prefixes. Reports new vs updated counts.

### Profiles

Isolate keys by project or environment:

```bash
keys profile use <name>     # switch profile
keys profile list           # list all profiles (* = active)
```

All `add`, `get`, `rm`, `see`, and other commands operate within the active profile.

### Inject keys into commands

```bash
$(keys inject API_KEY DB_HOST) ./my-script.sh          # inline env vars
docker run $(keys inject -d API_KEY DB_HOST) my-image  # Docker -e flags
$(keys inject --all) ./my-script.sh                    # all keys from active profile
$(keys inject --all --profile dev) ./my-script.sh      # all keys from specific profile
```

Outputs keys as space-separated `KEY=VAL` pairs (or `-e KEY=VAL` with `--docker`) for use in command substitution.

### Audit key access

```bash
keys audit              # summary: access count + last used per key
keys audit --log        # full access log (most recent first)
keys audit --log -n 20  # last 20 events
keys audit --clear      # clear the audit log
```

Tracks when keys are accessed via `get`, `inject`, and `expose`. Useful for understanding which keys agents and scripts are using.

### Check required keys

```bash
keys check              # reads .keys.required from current directory
keys check reqs.txt     # custom file
```

Reads key names from a file (one per line, `#` comments supported) and reports which are present or missing. Exits with code 1 if any are missing — useful for CI and agent pre-flight checks.

Example `.keys.required`:
```
# Agent dependencies
OPENAI_KEY
SERP_API_KEY
DATABASE_URL
```

### Sync keys between machines

```bash
# On machine A (has the keys)
keys sync serve
# Serving 12 keys from profile "default"
# Passphrase: olive-quilt-haven
# Waiting for connections...

# On machine B (wants the keys)
keys sync pull                       # auto-discover via mDNS
keys sync pull 192.168.1.10:7331     # or connect directly
```

Peer-to-peer sync over the local network. Auto-discovers peers via mDNS (Bonjour), encrypted with a one-time passphrase (AES-256-GCM). Works over WiFi, Tailscale, or any reachable network. Smart merge: adds new keys, updates older ones, skips newer local ones.

### Delete all keys

```bash
keys nuke
```

Requires typing `nuke` to confirm. Only affects the active profile.

### Version

```bash
keys version
keys --version
```

## Authentication

On macOS, `keys` prompts for Touch ID before any command that accesses keys. Authentication is cached per terminal session — the first command triggers Touch ID, subsequent commands in the same shell skip the prompt.

Commands that skip authentication: `profile`, `completion`, `version`, `help`.

On non-macOS systems or when biometrics are unavailable, access is allowed without prompting.

## Examples

### Typical workflow

```bash
keys add OPENAI_KEY sk-proj-abc123
keys add STRIPE_KEY sk_test_4eC3
keys get OPENAI_KEY
keys see                    # browse and copy
keys env                    # generate .env for a project
```

### Multi-project setup

```bash
keys profile use projectA
keys import .env
keys profile use projectB
keys add DB_HOST prod-db.example.com
keys profile list
```

### Quick export to shell

```bash
eval $(keys expose)
```

## Guidelines

- Always use `keys get <name>` when the user knows the exact key name
- Use `keys get` (no args) when the user wants to search/pick interactively
- Use `keys peek` instead of `keys see` when the user is screen-sharing or wants masked output
- Use `keys profile` to separate keys across different projects or environments
- Use `keys import` for bulk loading from existing `.env` files
- Suggest `keys env` when the user needs to generate a `.env` file for a specific project
- Use `keys inject` when the user wants to pass keys directly to a command or Docker container without creating files
- Use `keys audit` to review which keys are being accessed and how often
- Use `keys check` before running agents to verify all required keys are available
- Use `keys sync serve` + `keys sync pull` to transfer keys between machines without cloud services
