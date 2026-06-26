---
name: locker-vault
description: |
  Secure credential and secrets management for OpenClaw agents using Locker Secrets Manager.
  Provides read-only and read-write vault access with in-memory caching, vault-reference patterns,
  and strict rules to prevent credential leakage. Use this skill whenever an agent needs to access
  API keys, tokens, passwords, database credentials, webhook URLs, or any sensitive configuration.
  Also use when creating cron jobs, scheduled tasks, integrations, or any process that requires
  credentials — the skill ensures vault item IDs are stored instead of raw values. Triggers:
  "secret", "credential", "API key", "token", "password", "vault", "locker", "access key",
  "env var", "environment variable", ".env", "sensitive", "connection string", "webhook secret".
---

# Locker Vault — Secrets Management for OpenClaw Agents

## Why This Skill Exists

Agents that handle credentials face three risks: leaking secrets in logs/files, making redundant API calls that slow down processing, and losing access when credentials rotate. This skill eliminates all three by establishing a single pattern: **every credential lives in Locker's vault, is accessed through a cached client, and is referenced by ID — never by value.**

The cache layer is particularly important. Without it, every time an agent needs a credential during a conversation (which can happen dozens of times in a single session), it would make a round-trip CLI call to Locker. The cache holds decrypted values in-memory for a configurable TTL, dramatically reducing latency and API load while still respecting rotation schedules.

---

## Core Principles

These aren't arbitrary rules — they protect the business and the customer:

1. **Vault is the single source of truth.** Credentials are created, read, updated, and deleted exclusively through Locker. No `.env` files, no hardcoded values, no environment variables with raw secrets.

2. **References, not values.** When an agent creates a config file, cron job, script, or integration, it stores `vault://SECRET_KEY_NAME` (the vault reference) — never the actual token/password. At runtime, the vault-client resolves the reference.

3. **Cache before call.** The vault-client maintains an in-memory cache with configurable TTL. Repeated reads for the same secret within the TTL window return instantly from cache — no CLI subprocess, no network call, no latency.

4. **Permission boundaries are real.** A read-only agent cannot create, update, or delete secrets. Period. The agent's mode is set in its configuration, and the vault-client enforces it before any CLI call is made.

5. **Secrets never appear in output.** When logging, responding to users, or writing files, mask credential values. Show `vault://DB_PASSWORD` or `*****`, never the actual value.

---

## Permission Levels

### Read-Only (`VAULT_MODE=ro`)

For agents that consume credentials but should never manage them — SDR agents, customer-facing bots, monitoring agents.

**Allowed operations:**
- `get(key)` — Retrieve a secret value (cached)
- `list()` — List available secret keys (cached)
- `exists(key)` — Check if a secret exists

**Blocked operations (will throw error):**
- `create()`, `update()`, `delete()` — All write operations

### Read-Write (`VAULT_MODE=rw`)

For agents that manage infrastructure, rotate credentials, or onboard new integrations — DevOps agents, admin agents, integration agents.

**Allowed operations:**
- Everything from read-only, plus:
- `create(key, value)` — Store a new secret
- `createRandom(key)` — Generate and store a random secret
- `update(key, value)` — Update an existing secret
- `delete(key)` — Remove a secret (use with caution)

---

## Architecture

```
Agent Code
    │
    ▼
┌─────────────────────────────┐
│   vault-client.js           │
│   ┌───────────────────┐     │
│   │  In-Memory Cache  │     │  TTL-based, per-key expiry
│   │  Map<key, {val,   │     │  Default: 300s (5 min)
│   │   expiry}>         │     │  Configurable per agent
│   └───────┬───────────┘     │
│           │ cache miss      │
│           ▼                 │
│   ┌───────────────────┐     │
│   │  Permission Gate  │     │  Checks VAULT_MODE before
│   │  ro / rw          │     │  allowing write operations
│   └───────┬───────────┘     │
│           │                 │
│           ▼                 │
│   ┌───────────────────┐     │
│   │  CLI Executor     │     │  Spawns: locker secret <cmd>
│   │  (child_process)  │     │  Parses stdout, handles errors
│   └───────────────────┘     │
└─────────────────────────────┘
    │
    ▼
Locker CLI → Locker Cloud API (E2E encrypted)
```

### Cache Behavior

The cache is designed to balance freshness with performance:

- **On `get(key)`:** Check cache first. If key exists and hasn't expired, return cached value immediately (zero latency). If expired or missing, call CLI, store result with new TTL, return value.
- **On `create/update(key, value)`:** Execute CLI write, then update cache with new value and fresh TTL. This means subsequent reads see the new value instantly.
- **On `delete(key)`:** Execute CLI delete, then evict key from cache.
- **On `list()`:** Cached separately with its own TTL (default: 60s, shorter because the list changes more frequently).
- **Cache clear:** `clearCache()` evicts everything — useful after bulk operations or credential rotation.
- **TTL override per-key:** `get(key, { ttl: 600 })` can override the default TTL for secrets that rarely change (like database hosts).

### Why CLI Over SDK

The Locker Node.js SDK package isn't reliably published on npm. The CLI (`locker`) is stable, well-documented, works in any environment where it's installed, and OpenClaw agents have shell access. The vault-client.js wrapper provides the ergonomic API that a native SDK would, with the added benefit of the cache layer.

---

## Setup

### 1. Install Locker CLI on the Agent Host

```bash
# Download and install (check locker.io/secrets/download for latest)
curl -fsSL https://locker.io/secrets/install.sh | bash

# Verify installation
locker --version
```

### 2. Authenticate the CLI

```bash
# Login with access key (non-interactive, suitable for servers)
export LOCKER_ACCESS_KEY_ID="your-access-key-id"
export LOCKER_SECRET_ACCESS_KEY="your-secret-access-key"

# Verify access
locker secret list
```

The access key pair is created in the Locker dashboard under your project settings. Create separate access keys for read-only and read-write agents — this provides an additional security layer beyond the vault-client's permission gate.

### 3. Place vault-client.js in Agent Workspace

Copy `scripts/vault-client.js` into the agent's workspace. The script has zero npm dependencies — it uses only Node.js built-in modules (`child_process`, `util`).

### 4. Configure the Agent

In the agent's configuration (OpenClaw `config.json` or SOUL.md environment block):

```json
{
  "vault": {
    "mode": "ro",
    "cacheTTL": 300,
    "listCacheTTL": 60,
    "cliPath": "locker",
    "accessKeyId": "vault://LOCKER_ACCESS_KEY_ID",
    "secretAccessKey": "vault://LOCKER_SECRET_ACCESS_KEY"
  }
}
```

For the bootstrap case (the vault client needs credentials to access the vault), the access key pair is the ONE exception where environment variables are acceptable — set `LOCKER_ACCESS_KEY_ID` and `LOCKER_SECRET_ACCESS_KEY` as env vars on the host. Everything else goes through the vault.

---

## Usage Patterns

### Reading a Secret (Any Agent)

```javascript
const vault = require('./vault-client');

// Initialize (once per session)
await vault.init({ mode: 'ro', cacheTTL: 300 });

// Get a secret — returns from cache if available
const apiKey = await vault.get('OPENAI_API_KEY');

// Check existence without retrieving value
const hasKey = await vault.exists('SLACK_WEBHOOK');

// List all available keys
const keys = await vault.list();
```

### Creating/Updating Secrets (Read-Write Agents Only)

```javascript
await vault.init({ mode: 'rw', cacheTTL: 300 });

// Store a new credential
await vault.create('NEW_API_KEY', 'sk-abc123...');

// Generate a random secret (great for tokens, passwords)
await vault.createRandom('SESSION_SECRET');

// Update existing
await vault.update('DB_PASSWORD', 'new-password-here');

// Delete (requires rw mode)
await vault.delete('OLD_TOKEN');
```

### Vault References in Configs

When an agent creates a config file, cron job, or integration config, it must use vault references:

```javascript
// CORRECT — Store vault reference, resolve at runtime
const cronConfig = {
  schedule: '0 */6 * * *',
  task: 'sync_crm',
  credentials: {
    crm_token: 'vault://RD_CRM_API_TOKEN',
    webhook_url: 'vault://SLACK_WEBHOOK_SALES'
  }
};

// WRONG — Never store actual values
const cronConfig = {
  credentials: {
    crm_token: 'Bearer eyJhbGci...',  // ← NEVER DO THIS
  }
};
```

### Resolving Vault References at Runtime

```javascript
const { resolveVaultRefs } = require('./vault-client');

// Takes any object and resolves all vault:// references
const config = await resolveVaultRefs({
  apiUrl: 'https://api.example.com',         // Not a ref, passed through
  token: 'vault://EXAMPLE_API_TOKEN',         // Resolved from vault
  dbPassword: 'vault://DB_PASSWORD_PROD',     // Resolved from vault
});
// config.token now contains the actual value, config.apiUrl unchanged
```

### Cache Management

```javascript
// Force refresh a specific key (bypasses cache)
const fresh = await vault.get('API_KEY', { skipCache: true });

// Clear entire cache (after bulk rotation)
vault.clearCache();

// Set per-key TTL (database host rarely changes = longer cache)
const dbHost = await vault.get('DB_HOST', { ttl: 3600 }); // 1 hour

// Get cache stats (for debugging/monitoring)
const stats = vault.cacheStats();
// { size: 12, hits: 847, misses: 23, hitRate: '97.4%' }
```

---

## Integration with OpenClaw

### In SOUL.md / AGENTS.md

Add to the agent's bootstrap instructions:

```markdown
## Credentials Policy

All credentials are managed through Locker Vault. Follow these rules without exception:

1. Use `vault-client.js` for ALL secret access
2. Never write credentials to files, logs, or chat responses
3. Store vault references (`vault://KEY_NAME`) in configs, never raw values
4. Cache is automatic — don't worry about repeated reads being slow
5. If you need a new credential stored, and you're read-only, ask the operator
```

### In OpenClaw Agent Config

```json5
{
  agents: [{
    id: "sdr-datatem",
    workspace: "/opt/agents/sdr-datatem",
    tools: {
      allow: ["read_file", "exec"],  // exec needed for CLI calls
      deny: ["write", "edit", "browser", "gateway"]
    },
    env: {
      VAULT_MODE: "ro",
      VAULT_CACHE_TTL: "300",
      LOCKER_ACCESS_KEY_ID: "ak_xxxx",      // Bootstrap exception
      LOCKER_SECRET_ACCESS_KEY: "sk_xxxx"    // Bootstrap exception
    }
  }]
}
```

### In Cron Jobs / Scheduled Tasks

Agents creating scheduled tasks MUST use this pattern:

```javascript
// The scheduled script reads from vault at execution time
const taskScript = `
const vault = require('./vault-client');

async function run() {
  await vault.init({ mode: 'ro' });
  const token = await vault.get('CRM_API_TOKEN');
  // Use token for the actual task...
  await syncCRM(token);
}

run().catch(console.error);
`;

// Save the script — note: no credentials in the file
fs.writeFileSync('/opt/tasks/sync-crm.js', taskScript);
```

---

## Error Handling

The vault-client provides clear error messages:

| Error | Cause | Action |
|-------|-------|--------|
| `VAULT_PERMISSION_DENIED` | Write operation in ro mode | Check agent's VAULT_MODE setting |
| `VAULT_KEY_NOT_FOUND` | Secret doesn't exist in vault | Verify key name, check `list()` |
| `VAULT_CLI_NOT_FOUND` | `locker` binary not in PATH | Install Locker CLI on host |
| `VAULT_AUTH_FAILED` | Invalid or expired access keys | Rotate access key pair in dashboard |
| `VAULT_TIMEOUT` | CLI call took > 10s | Check network, Locker API status |
| `VAULT_PARSE_ERROR` | Unexpected CLI output | Check CLI version compatibility |

All errors are non-fatal by default — the vault-client returns `null` on failure and logs the error. For critical secrets, use strict mode:

```javascript
// Throws on error instead of returning null
const dbPass = await vault.get('DB_PASSWORD', { strict: true });
```

---

## Security Checklist

Before deploying an agent with vault access, verify:

- [ ] Agent's VAULT_MODE matches its actual needs (ro for most agents)
- [ ] Locker access key has minimum required permissions
- [ ] `vault-client.js` is in the workspace but not editable by end-users
- [ ] Agent's tool deny-list blocks `write` and `edit` (for ro agents)
- [ ] No credentials appear in SOUL.md, AGENTS.md, or any workspace file
- [ ] Cron jobs and tasks use vault references, not raw values
- [ ] Logs are configured to redact secret values
- [ ] Cache TTL is appropriate for the credential rotation schedule

---

## Anti-Patterns

### Never Store Credentials Locally

```javascript
// ❌ WRONG: Writing to .env
fs.writeFileSync('.env', `API_KEY=${apiKey}`);

// ❌ WRONG: Hardcoding in config
const config = { token: 'sk-live-abc123' };

// ❌ WRONG: Logging the value
console.log(`Using API key: ${apiKey}`);

// ✅ CORRECT: Use vault reference
const config = { token: 'vault://API_KEY' };

// ✅ CORRECT: Log the reference
console.log('Using API key: vault://API_KEY');
```

### Never Cache to Disk

```javascript
// ❌ WRONG: Persisting cache to file
fs.writeFileSync('cache.json', JSON.stringify(cache));

// ✅ CORRECT: Cache lives only in memory, dies with process
// (vault-client.js handles this automatically)
```

### Never Expose in Responses

```javascript
// ❌ WRONG: Including in chat/API response
return `Your API key is ${apiKey}`;

// ✅ CORRECT: Confirm without revealing
return 'API key configured successfully (vault://API_KEY)';
```

---

## File Reference

| File | Purpose | When to Read |
|------|---------|-------------|
| `scripts/vault-client.js` | Node.js wrapper with cache, permission gate, CLI executor | Copy to agent workspace during setup |
| `references/cli-reference.md` | Complete Locker CLI command reference | When you need exact CLI syntax |
| `references/vault-patterns.md` | Common patterns for different use cases | When implementing a new integration |

---

## Quick Decision Tree

```
Need a credential?
├─ Already in vault? → vault.get('KEY_NAME')
│   ├─ In cache? → Returns instantly (0ms)
│   └─ Not in cache? → CLI call (~200ms), caches result
├─ Not in vault yet?
│   ├─ Agent is rw? → vault.create('KEY_NAME', value)
│   └─ Agent is ro? → Ask operator to add it
└─ Creating a config/cron/task?
    └─ Always store 'vault://KEY_NAME', never the value
```
