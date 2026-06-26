---
name: mayar
display_name: Mayar CLI
version: "0.1.8"
description: >
  Interact with the Mayar payment platform (invoices, products, payments,
  customers, transactions, webhooks, QR codes) from any AI agent or shell.
  Zero dependencies — Node.js 18+ only.
author: Mayar bot
license: MIT
homepage: https://github.com/mayarid/mayar-cli
repository: https://github.com/mayarid/mayar-cli.git
tags:
  - payments
  - invoices
  - mayar
  - indonesia
  - cli
  - tool
runtime: node>=18
install_command: npx -y mayar@latest
invoke_prefix: npx -y mayar@latest
env:
  MAYAR_API_KEY:
    description: Mayar API key. Obtain from web.mayar.id → Integration → API Key.
    required: true
    secret: true
  MAYAR_API_URL:
    description: Override API base URL. Defaults to https://api.mayar.id.
    required: false
    default: https://api.mayar.id
auth:
  type: bearer
  resolution_order:
    - flag: --api-key
    - env: MAYAR_API_KEY
    - file: ~/.config/mayar/config.json
capabilities:
  - invoices
  - products
  - payments
  - customers
  - transactions
  - webhooks
  - qrcode
  - balance
  - whoami
---

# Mayar CLI — Agent Skill

This document describes how AI agents (Claude Code, OpenClaw, and others)
should install, authenticate, and use the `mayar` CLI tool.

## Quick start for agents

```bash
# Always use the latest version — no install step required
npx -y mayar@latest whoami
```

## Authentication flow

**Step 1 — detect active user**

Run `whoami` to check if a valid API key is already configured:

```bash
npx -y mayar@latest whoami --json
```

Successful output contains `"valid": true` and the merchant's `name`, `email`,
and `accountId`. If the key is valid, proceed directly to the requested task.

**Step 2 — handle missing or invalid key**

If `whoami` exits non-zero or returns `"valid": false`, the agent MUST stop
and ask the user for their API key using one of the following options:

> **Option A — environment variable (recommended for non-interactive agents):**
>
> Ask the user to set:
> ```bash
> export MAYAR_API_KEY=<their_key>
> ```
> Then re-run the original command.

> **Option B — one-time flag (single command):**
>
> Ask the user to provide the key and pass it as:
> ```bash
> npx -y mayar@latest --api-key <their_key> whoami
> ```

> **Option C — interactive setup (terminal agents only):**
>
> If the agent has access to an interactive TTY:
> ```bash
> npx -y mayar@latest init
> ```

Agents must NEVER fabricate or guess an API key. Always stop and ask the user.

Get a key at: **https://web.mayar.id → Integration → API Key**

## Usage reference

All commands use the pattern:

```
npx -y mayar@latest <command> [subcommand] [args] [flags]
```

### Account

```bash
npx -y mayar@latest whoami              # verify key + show merchant identity
npx -y mayar@latest balance             # account balance
```

### Invoices

```bash
npx -y mayar@latest invoice list [--page N --pageSize N]
npx -y mayar@latest invoice get <id>
npx -y mayar@latest invoice close <id>
npx -y mayar@latest invoice reopen <id>
npx -y mayar@latest invoice create --data '<json>'
npx -y mayar@latest invoice create --data @file.json
```

### Products

```bash
npx -y mayar@latest product list [--page N --pageSize N]
npx -y mayar@latest product search <keyword>
npx -y mayar@latest product type <ebook|course|membership|saas|event|webinar>
npx -y mayar@latest product get <id>
npx -y mayar@latest product close <id>
npx -y mayar@latest product reopen <id>
```

### Payments

```bash
npx -y mayar@latest payment list
npx -y mayar@latest payment get <id>
npx -y mayar@latest payment close <id>
npx -y mayar@latest payment reopen <id>
npx -y mayar@latest payment create --data '<json>'
```

### Customers

```bash
npx -y mayar@latest customer list [--page N --pageSize N]
npx -y mayar@latest customer create --data '<json>'
```

### Transactions

```bash
npx -y mayar@latest tx list   [--page N --pageSize N]   # paid
npx -y mayar@latest tx unpaid [--page N --pageSize N]   # unpaid
```

### Dynamic QR

```bash
npx -y mayar@latest qrcode <amount_in_idr>
```

### Webhooks

```bash
npx -y mayar@latest webhook register <url>
npx -y mayar@latest webhook test <url>
npx -y mayar@latest webhook history [--page N --pageSize N]
```

## Global flags

| Flag              | Description                                           |
| ----------------- | ----------------------------------------------------- |
| `--json`          | Output raw JSON (machine-readable, pipe to `jq`)      |
| `--api-key <key>` | Override saved key for this invocation                |
| `--page N`        | Pagination page (default 1)                           |
| `--pageSize N`    | Items per page (default 10)                           |
| `-v, --version`   | Print version                                         |
| `-h, --help`      | Print help                                            |

## JSON output

Always use `--json` when the agent needs to parse the response:

```bash
npx -y mayar@latest invoice list --json | jq '.data[] | {id, status}'
npx -y mayar@latest whoami --json | jq '{valid, name: .decoded.name}'
```

## Error handling

- Non-zero exit code = command failed
- `"valid": false` in `whoami --json` = invalid or expired API key
- HTTP errors print `API <status> — <message>` on stderr

## Agent decision tree

```
START
  └─ run: npx -y mayar@latest whoami --json
        ├─ exit 0 + valid=true  →  proceed with task
        └─ exit non-zero or valid=false
              └─ ask user:
                    "Please provide your Mayar API key.
                     You can either:
                     (A) set the MAYAR_API_KEY environment variable, or
                     (B) run: npx -y mayar@latest init
                     Get your key from https://web.mayar.id → Integration → API Key"
```
