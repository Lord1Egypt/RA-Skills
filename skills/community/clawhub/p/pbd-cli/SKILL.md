---
name: pbd-cli
version: 1.0.0
description: "pbd-cli: Command-line tool for PaleBlueDot AI Platform. Core scenarios include: authentication, API Token management, usage & balance queries, and browsing available models."
metadata:
  requires:
    bins: ["pbd-cli"]

##   cliHelp: "pbd-cli --help"

# pbd-cli

**CRITICAL — Ensure the user is logged in (`pbd-cli login`) before executing commands, otherwise a session expired error will be returned.**

## Installation

### One-click Install
**Linux / macOS:**

```bash
curl -sSL https://raw.githubusercontent.com/PaleBlueDot-AI-Open/pbd-cli/main/install.sh | bash
```

This script automatically detects your OS and architecture, downloads the latest release, and installs to `/usr/local/bin`.

## Core Scenarios

The pbd-cli skill includes the following core scenarios:

### 1. Authentication

Supports two login modes:

| Mode | Command | Description |
|------|---------|-------------|
| Browser Login (Default) | `pbd-cli login` | Automatically opens browser for OAuth authentication |
| Manual Login | `pbd-cli login --manual` | Manually enter session cookie and user ID |

**Browser Login Flow (Recommended):**

1. Run `pbd-cli login`
2. Browser automatically opens the PaleBlueDot login page
3. User completes login in the browser
4. Browser calls back to local server, automatically obtains token
5. CLI calls `pbd-login` API to exchange for session
6. Saves configuration and completes login

**Manual Login Flow:**

1. User obtains session cookie from PaleBlueDot website in browser
2. Get user ID (can be found in personal settings on the web page)
3. Run `pbd-cli login --manual` and enter as prompted

### 2. Token Management

Manage API Tokens, including creating, viewing, deleting, and retrieving keys.

### 3. Usage Queries

Query account usage, balance, and subscription status.

### 4. Model Browsing

View available AI models for the current account.

## Command Overview

### Global Parameters

| Parameter | Description |
|-----------|-------------|
| `--config` | Specify config file path |
| `-f, --format` | Formatted output (default: raw JSON) |
| `--base-url` | Override base URL |

---

## Authentication

### login (Browser Mode)

Default method, automatically opens browser for OAuth login.

```bash
pbd-cli login                      # Browser login (default)
pbd-cli login --port 8085          # Specify callback port
pbd-cli login --base-url https://open.palebluedot.ai
```

**Flow Description:**

1. Starts local HTTP server listening for callback (port 8080-8090 auto-select)
2. Opens browser to `https://www.palebluedot.ai/login?redirect_uri=http://localhost:{port}/callback`
3. Waits for browser callback (5 minute timeout)
4. After successful callback, calls API to exchange for session
5. Saves configuration locally

**Successful Login Output:**

```
Opening browser for login...
If browser doesn't open, visit: https://www.palebluedot.ai/login?redirect_uri=...
Waiting for login...
Exchanging token for session...
Login successful! Logged in as user ID: 12345
```

### login --manual (Manual Mode)

Manually enter session cookie and user ID.

```bash
pbd-cli login --manual
```

Prompts for input:
- **Session Cookie**: Session cookie from browser (format: `session=xxx`)
- **User ID**: User ID (number)

### logout

Log out and clear local session.

```bash
pbd-cli logout
```

---

## Token Management

### token list

List all tokens.

```bash
pbd-cli token list        # Raw JSON output
```

Output fields:

| Field | Description |
|-------|-------------|
| ID | Token ID |
| NAME | Token name |
| QUOTA | Remaining quota |
| USED | Used quota |
| MODELS | Available model restrictions |
| STATUS | Status (enabled/disabled) |

### token create

Create a new token.

```bash
pbd-cli token create --name <name>
pbd-cli token create --name prod-key --quota 100000 --models gpt-4o,claude-3-5
```

| Parameter | Description |
|-----------|-------------|
| `--name` | Token name (required) |
| `--quota` | Remaining quota (default: unlimited) |
| `--expires` | Expiration timestamp |
| `--models` | Model whitelist (comma-separated) |

### token delete

Delete a token.

```bash
pbd-cli token delete <id>
```

### token get-key

Get the plaintext key for a token.

```bash
pbd-cli token get-key <id>
pbd-cli token get-key <id> -f  # Formatted output
```

---

## Usage Queries

### usage balance

Query balance and subscription status.

```bash
pbd-cli usage balance        # Raw JSON output
```

Output:
- Quota: Total quota
- Used: Used quota
- Remaining: Remaining quota
- Subscription: Subscription info

### usage logs

Query usage logs.

```bash
pbd-cli usage logs
pbd-cli usage logs --limit 50 --model gpt-4o
pbd-cli usage logs --page 2 --token my-token
```

| Parameter | Description |
|-----------|-------------|
| `--limit` | Items per page (default: 20) |
| `--page` | Page number (default: 1) |
| `--model` | Filter by model |
| `--token` | Filter by token name |

---

## Wallet Balance

### wallet

Query wallet balance.

```bash
pbd-cli wallet        # Raw JSON output
```

Output:
- Balance: Account balance
- Gift Balance: Gift balance

---

## Model Browsing

### models list

List available AI models.

```bash
pbd-cli models list        # Raw JSON output
```

---

## Common Error Handling

### session expired

```
Error: session expired — please run 'pbd-cli login'
```

**Solution**: Run `pbd-cli login` again to re-authenticate.

### Browser Cannot Open

If automatic browser opening fails, the CLI will print the login URL. Open it manually in your browser:

```
Warning: failed to open browser: ...
Please open this URL manually: https://www.palebluedot.ai/login?redirect_uri=...
```

### Login Timeout

Default wait time is 5 minutes. If timeout occurs, run `pbd-cli login` again.

### Authentication Failed (Manual Mode)

Ensure:
1. Session cookie format is correct (includes `session=xxx`)
2. User ID is correct (pure number)
3. Base URL is correct (if using custom deployment)

### Callback Port Occupied

If default port range (8080-8090) is occupied, use `--port` to specify a port:

```bash
pbd-cli login --port 9000
```

---

## Configuration File

Configuration file is stored at `~/.pbd-cli/config.yaml` with `0600` permissions (owner read/write only).

**Configuration Structure:**

```yaml
base_url: https://www.palebluedot.ai
cookie: session=xxx
user_id: 12345
api_key: ""  # Optional
```

| Field | Description |
|-------|-------------|
| `base_url` | API base URL |
| `cookie` | Session cookie for authentication |
| `user_id` | User ID |
| `api_key` | API Key (optional) |

**Security Note**: Configuration file uses `0600` permissions to ensure only the current user can read sensitive information.
