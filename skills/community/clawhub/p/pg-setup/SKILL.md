---
name: pg-setup
description: Use when setting up ProxyGate for the first time, installing the CLI, configuring auth (API key or wallet), or connecting to the gateway. Make sure to use this skill whenever someone mentions "get started with proxygate", "install proxygate", "setup wallet", "configure proxygate", "connect to gateway", "login", or wants to start using ProxyGate APIs, even if they don't explicitly say "setup".
---

# ProxyGate Setup

First-time setup for ProxyGate — install CLI, authenticate, start using APIs.

## Two ways to authenticate

| Method | Best for | Command |
|--------|----------|---------|
| **API key** | AI agents, automated access, quick start | `proxygate login --key pg_live_...` |
| **Wallet keypair** | On-chain operations (deposit, withdraw) | `proxygate login --keypair ~/id.json` |

Most users should start with an **API key** — it's the fastest path to making API calls. Get one at [app.proxygate.ai/keys](https://app.proxygate.ai/keys).

You can add both later (dual mode: API key for proxy, keypair for vault ops).

## Process

### 1. Check existing install

```bash
proxygate --version 2>/dev/null || echo "NOT_INSTALLED"
proxygate whoami 2>/dev/null || echo "NOT_CONFIGURED"
```

- Installed and configured → skip to verify
- Installed but not configured → skip to authenticate
- Not installed → start from install

### 2. Install the CLI

```bash
npm install -g @proxygate/cli
# or
pnpm add -g @proxygate/cli
```

### 3. Authenticate

**Option A: API key (recommended for agents)**
```bash
proxygate login --key pg_live_abc123...
```
Get a key at [app.proxygate.ai/keys](https://app.proxygate.ai/keys). No Solana wallet needed.

**Option B: Wallet keypair (for on-chain operations)**
```bash
proxygate login --keypair ~/.proxygate/keypair.json
# or generate a new one:
proxygate login --generate
```

**Option C: Interactive menu**
```bash
proxygate login
# Shows a menu:
#   1. API key     — For AI agents and automated access
#   2. Wallet      — Connect a Solana keypair for on-chain operations
```

Supported keypair formats: JSON array (64 numbers), seed array (32 numbers), Base58 private key (Phantom export), Base64, Hex.

### 4. Verify

```bash
proxygate whoami                    # check auth mode + balance
proxygate apis -q weather           # browse available APIs
proxygate proxy agent-us-weather /   # make your first API call
```

### 5. Install Claude Code skills (optional)

```bash
proxygate skills install
```

## Auth management

```bash
proxygate whoami                    # check current auth mode
proxygate login --key pg_live_...   # add/change API key
proxygate login --keypair ~/id.json # add/change wallet
proxygate logout                    # remove API key (keep wallet)
proxygate logout --all              # remove all auth (with confirmation)
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `command not found: proxygate` | `npm install -g @proxygate/cli` |
| `Authentication failed` | Check your API key at app.proxygate.ai/keys |
| `Not configured` | Run `proxygate login` |
| `Gateway unreachable` | Verify URL: `https://gateway.proxygate.ai` |
| Balance shows 0 | Deposit USDC — use `/pg-buy` |

## Success criteria

- [ ] CLI installed (`proxygate --version` returns a version)
- [ ] `proxygate whoami` shows auth mode and balance
- [ ] `proxygate apis` shows available APIs
- [ ] `proxygate proxy <service> <path>` returns a response

## Related skills

| Need | Skill |
|------|-------|
| First-time setup | **This skill** |
| Buy API access | `pg-buy` |
| Sell API capacity | `pg-sell` |
| Job marketplace | `pg-jobs` |
| Check status | `pg-status` |
| Update CLI/SDK | `pg-update` |
