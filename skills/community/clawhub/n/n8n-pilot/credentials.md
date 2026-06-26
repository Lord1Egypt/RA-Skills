# Credential Management — n8n

Guide to creating, managing, and securing n8n credentials.

---

## Credential Types & Automability

| Type | Auth Method | Create via API? | Notes |
|------|------------|-----------------|-------|
| `httpHeaderAuth` | Header (Bearer token) | ✅ Yes | Simplest — just name + value |
| `httpBasicAuth` | Username + password | ✅ Yes | Basic auth |
| `oAuth2Api` | OAuth2 flow | ❌ Browser required | Must complete consent flow in UI |
| `telegramBotApi` | Bot token | ✅ Yes | Just the token |
| `postgresApi` | Connection string | ✅ Yes | Host, port, db, user, password |
| `mysqlApi` | Connection string | ✅ Yes | Same as PostgreSQL |
| `smtpAccount` | SMTP credentials | ✅ Yes | Host, port, user, password |
| `slackApi` | Bot token | ✅ Yes | Token-based |
| `googleApiOAuth2` | OAuth2 flow | ❌ Browser required | Gmail, Sheets, Calendar, Drive |
| `githubApi` | Personal access token | ✅ Yes | Token + optional 2FA |

## Creating Credentials via API

### API Key / Header Auth

```bash
curl -X POST "${N8N_BASE_URL}/api/v1/credentials" \
  -H "X-N8N-API-KEY: ${N8N_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Bearer Token",
    "type": "httpHeaderAuth",
    "data": {
      "name": "Authorization",
      "value": "Bearer sk-abc123"
    }
  }'
```

### Basic Auth

```bash
curl -X POST "${N8N_BASE_URL}/api/v1/credentials" \
  -H "X-N8N-API-KEY: ${N8N_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "API Basic Auth",
    "type": "httpBasicAuth",
    "data": {
      "user": "myuser",
      "password": "mypassword"
    }
  }'
```

### Database Connection

```bash
curl -X POST "${N8N_BASE_URL}/api/v1/credentials" \
  -H "X-N8N-API-KEY: ${N8N_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "PostgreSQL Production",
    "type": "postgresApi",
    "data": {
      "host": "postgres.internal",
      "port": 5432,
      "database": "myapp",
      "user": "n8n_user",
      "password": "secure_password"
    }
  }'
```

### Telegram Bot

```bash
curl -X POST "${N8N_BASE_URL}/api/v1/credentials" \
  -H "X-N8N-API-KEY: ${N8N_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Telegram Bot",
    "type": "telegramBotApi",
    "data": {
      "accessToken": "123456:ABC-DEF"
    }
  }'
```

## Listing & Managing Credentials

```bash
# List all credentials (names and IDs only — values are encrypted)
curl -X GET "${N8N_BASE_URL}/api/v1/credentials" \
  -H "X-N8N-API-KEY: ${N8N_API_KEY}"

# Get credential details
curl -X GET "${N8N_BASE_URL}/api/v1/credentials/{id}" \
  -H "X-N8N-API-KEY: ${N8N_API_KEY}"

# Delete credential
curl -X DELETE "${N8N_BASE_URL}/api/v1/credentials/{id}" \
  -H "X-N8N-API-KEY: ${N8N_API_KEY}"
```

**⚠️ Important:** The API returns credential data (including secrets) in plain text for users with access. Never log or store credential responses insecurely.

## OAuth2 Credentials

OAuth2 credentials **cannot be fully automated** — they require browser interaction for the consent flow.

### Process for OAuth2 (e.g., Google, Slack):

1. **Create credential via API** with `clientId` and `clientSecret`:
   ```bash
   curl -X POST "${N8N_BASE_URL}/api/v1/credentials" \
     -H "X-N8N-API-KEY: ${N8N_API_KEY}" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Google OAuth2",
       "type": "googleApiOAuth2",
       "data": {
         "clientId": "xxx.apps.googleusercontent.com",
         "clientSecret": "GOCSPX-xxx"
       }
     }'
   ```

2. **User completes consent flow** in the n8n UI (Settings → Credentials → click → Connect)

3. **n8n stores the refresh/access tokens** automatically after consent

### OAuth2 Redirect URI

Set the redirect URI in your OAuth provider:
```
https://YOUR_N8N_DOMAIN/rest/oauth2-credential/callback
```

For local development:
```
http://localhost:5678/rest/oauth2-credential/callback
```

## Encryption Key Management

### How Credential Encryption Works

n8n encrypts ALL credential values using **AES-256-GCM** with the `N8N_ENCRYPTION_KEY`. This key is stored in the database but derived from the environment variable.

### Critical Rules

1. **Never lose the encryption key** — credentials become permanently unrecoverable without it
2. **Same key across all instances** — in queue mode, main + workers must share the same key
3. **Store securely** — use `.env` file (not in docker-compose.yml in production), or a secrets manager
4. **Back it up** — include in your backup strategy alongside the database

### Generating a Secure Encryption Key

```bash
# Generate a random 32-character key
openssl rand -hex 16
# or
node -e "console.log(require('crypto').randomBytes(16).toString('hex'))"
```

### Key Rotation

n8n does NOT support automatic key rotation. To rotate:

1. Export all credentials via API
2. Save the export securely
3. Change `N8N_ENCRYPTION_KEY`
4. Restart n8n (credentials will be encrypted with new key)
5. Re-import credentials if needed

**This is a disruptive operation. Plan for downtime.**

## Credential Security Best Practices

### Principle of Least Privilege

- Create separate credentials for each service/workflow
- Use read-only API keys when the workflow only reads data
- Scope OAuth2 permissions to minimum required (e.g., Gmail read-only, not full access)
- Rotate API keys periodically (every 90 days)

### Credential Naming Convention

```
[Environment] [Service] [Scope] [Owner]

Examples:
- PROD PostgreSQL Read-Only (Pipeline)
- PROD Telegram Bot (Alerts)
- DEV GitHub Token (CI)
- STAGING Gmail OAuth (Testing)
```

### Never Hardcode Credentials in Code Nodes

```javascript
// ❌ NEVER DO THIS
const apiKey = "sk-abc123def456";
await this.helpers.httpRequest({ url: "...", headers: { "Authorization": `Bearer ${apiKey}` } });

// ✅ Use credentials configured in n8n
// Create an HTTP Header Auth credential, assign it to the HTTP Request node
```

### Environment Variables in Workflows

For values that change between environments (dev/staging/prod), use environment variables:

```json
{
  "parameters": {
    "url": "={{ $env.API_BASE_URL }}",
    "headers": {
      "Authorization": "={{ $env.API_KEY }}"
    }
  }
}
```

Set in docker-compose.yml:
```yaml
environment:
  - API_BASE_URL=https://api.production.example.com
  - API_KEY=${N8N_API_KEY}
```

**⚠️ Environment variables are visible in the workflow editor. Don't store secrets this way. Use n8n credentials instead.**