# Vault Patterns — Common Use Cases

## Pattern 1: SDR Agent (Read-Only)

The SDR agent needs CRM tokens, WhatsApp API keys, and enrichment service credentials, but should never be able to modify them.

```javascript
const vault = require('./vault-client');

async function initSDR() {
  await vault.init({ mode: 'ro', cacheTTL: 600 }); // 10 min cache — these rarely change

  // These are all cached after first call
  const crmToken = await vault.get('RD_CRM_API_TOKEN');
  const whatsappKey = await vault.get('EVOLUTION_API_KEY');
  const drivaKey = await vault.get('DRIVA_API_KEY');

  return { crmToken, whatsappKey, drivaKey };
}

// Second call in the same session → instant from cache
async function sendWhatsApp(lead, message) {
  const apiKey = await vault.get('EVOLUTION_API_KEY'); // cache hit
  // ... send message
}
```

### Config for this pattern:
```json
{
  "vault": {
    "mode": "ro",
    "cacheTTL": 600
  }
}
```

---

## Pattern 2: DevOps Agent (Read-Write)

The DevOps agent manages infrastructure credentials, rotates tokens, and sets up new integrations.

```javascript
const vault = require('./vault-client');

async function rotateDBPassword() {
  await vault.init({ mode: 'rw' });

  // Generate new password
  const newPassword = await vault.createRandom('DB_PASSWORD_PROD');

  // Update the database with new password
  await updateDatabasePassword(newPassword);

  // Clear cache so all agents get the new password
  vault.clearCache();

  return 'Password rotated successfully';
}

async function onboardNewIntegration(name, apiKey) {
  await vault.init({ mode: 'rw' });

  // Store the credential
  await vault.create(`INTEGRATION_${name.toUpperCase()}_KEY`, apiKey);

  // Return vault reference (not the value!)
  return vault.ref(`INTEGRATION_${name.toUpperCase()}_KEY`);
  // → "vault://INTEGRATION_SLACK_KEY"
}
```

---

## Pattern 3: Cron Job / Scheduled Task

Agents creating scheduled tasks must store vault references, not values.

```javascript
const vault = require('./vault-client');

// When creating the task
function createSyncTask() {
  const taskConfig = {
    name: 'crm-sync',
    schedule: '0 */4 * * *',
    script: 'tasks/crm-sync.js',
    // Vault references — resolved at runtime
    secrets: {
      crmToken: vault.ref('RD_CRM_API_TOKEN'),
      supabaseKey: vault.ref('SUPABASE_SERVICE_KEY'),
    }
  };

  // Save task config (contains only references, no secrets)
  fs.writeFileSync('config/tasks.json', JSON.stringify(taskConfig, null, 2));
}

// tasks/crm-sync.js — executed by cron
async function runSync() {
  const vault = require('../vault-client');
  await vault.init({ mode: 'ro' });

  // Load task config
  const config = JSON.parse(fs.readFileSync('config/tasks.json'));

  // Resolve vault references to actual values
  const secrets = await vault.resolveVaultRefs(config.secrets);

  // Now use actual values
  await syncToCRM(secrets.crmToken);
  await backupToSupabase(secrets.supabaseKey);
}
```

---

## Pattern 4: Multi-Service Integration

When an agent orchestrates multiple services, resolve all vault refs at once.

```javascript
const vault = require('./vault-client');

async function initServices() {
  await vault.init({ mode: 'ro', cacheTTL: 300 });

  const config = await vault.resolveVaultRefs({
    crm: {
      baseUrl: 'https://api.rdstation.com/v3',
      token: 'vault://RD_CRM_API_TOKEN',
    },
    whatsapp: {
      baseUrl: 'https://api.evolution.io',
      token: 'vault://EVOLUTION_API_KEY',
      instanceId: 'vault://EVOLUTION_INSTANCE_ID',
    },
    enrichment: {
      baseUrl: 'https://api.driva.com.br',
      token: 'vault://DRIVA_API_KEY',
    },
    ai: {
      baseUrl: 'https://api.anthropic.com/v1',
      token: 'vault://ANTHROPIC_API_KEY',
    },
  });

  // config now has all actual values, and each was fetched only once
  // (cache prevents duplicate calls if same key appears in multiple places)
  return config;
}
```

---

## Pattern 5: Credential Reception

When a user provides credentials (e.g., "here's my new API key"), the agent must immediately store them in the vault and never keep the value.

```javascript
// Agent receives credential from operator
async function handleNewCredential(keyName, keyValue) {
  const vault = require('./vault-client');
  await vault.init({ mode: 'rw' });

  // Store immediately
  await vault.create(keyName, keyValue);

  // Return only the reference
  const reference = vault.ref(keyName);

  // CRITICAL: Do not include keyValue in any response or log
  return `Credential stored securely as ${reference}`;
}
```

In the agent's response to the user:
```
✅ "Credential stored securely as vault://NEW_API_KEY"
❌ "I saved your API key sk-abc123..." ← NEVER
```

---

## Pattern 6: Cache Warming

For agents that need fast startup, pre-load frequently used secrets.

```javascript
async function warmCache() {
  const vault = require('./vault-client');
  await vault.init({ mode: 'ro', cacheTTL: 600 });

  // Warm cache with all frequently used secrets in parallel
  await Promise.all([
    vault.get('RD_CRM_API_TOKEN'),
    vault.get('EVOLUTION_API_KEY'),
    vault.get('DRIVA_API_KEY'),
    vault.get('ANTHROPIC_API_KEY'),
    vault.get('SUPABASE_SERVICE_KEY'),
  ]);

  const stats = vault.cacheStats();
  console.log(`Cache warmed: ${stats.size} secrets loaded`);
}
```

---

## Pattern 7: Graceful Fallback

For non-critical secrets, handle missing keys without crashing.

```javascript
async function getOptionalConfig() {
  const vault = require('./vault-client');
  await vault.init({ mode: 'ro' });

  // Strict for critical secrets — will throw if missing
  const crmToken = await vault.get('RD_CRM_API_TOKEN', { strict: true });

  // Non-strict for optional features — returns null if missing
  const slackWebhook = await vault.get('SLACK_WEBHOOK_NOTIFICATIONS');

  if (slackWebhook) {
    // Enable Slack notifications
  } else {
    console.log('Slack notifications disabled (vault://SLACK_WEBHOOK_NOTIFICATIONS not set)');
  }
}
```

---

## Naming Convention

Use consistent key naming across the organization:

```
SERVICE_PURPOSE_QUALIFIER

Examples:
  RD_CRM_API_TOKEN          → RD Station CRM API token
  EVOLUTION_API_KEY          → Evolution WhatsApp API key
  EVOLUTION_INSTANCE_ID      → Evolution instance identifier
  DRIVA_API_KEY              → Driva enrichment API key
  ANTHROPIC_API_KEY          → Anthropic (Claude) API key
  DB_PASSWORD_PROD           → Production database password
  DB_PASSWORD_STAGING        → Staging database password
  SUPABASE_SERVICE_KEY       → Supabase service role key
  SLACK_WEBHOOK_SALES        → Slack webhook for sales channel
  LOCKER_ACCESS_KEY_ID       → Bootstrap: Locker's own access key
```

Rules:
- UPPERCASE with underscores
- Service prefix first (RD_, EVOLUTION_, DB_)
- Purpose in the middle (API_KEY, PASSWORD, WEBHOOK)
- Environment suffix when needed (_PROD, _STAGING, _DEV)
