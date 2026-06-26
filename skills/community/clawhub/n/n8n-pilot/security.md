# Security Hardening — n8n

Security best practices for self-hosted n8n instances, webhook security, RBAC, and dangerous pattern prevention.

---

## Instance Security

### Network Hardening

```yaml
# docker-compose.yml — production security
services:
  n8n-main:
    image: docker.n8n.io/n8nio/n8n
    ports:
      - "127.0.0.1:5678:5678"  # Bind to localhost only
    environment:
      - N8N_SECURE_COOKIES=true
      - N8N_EDITOR_BASE_URL=https://n8n.example.com
```

**Put n8n behind a reverse proxy (Nginx/Traefik) with TLS:**

```nginx
# nginx.conf
server {
    listen 443 ssl http2;
    server_name n8n.example.com;

    ssl_certificate /etc/letsencrypt/live/n8n.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/n8n.example.com/privkey.pem;

    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    location / {
        proxy_pass http://127.0.0.1:5678;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### Environment Variables for Security

| Variable | Purpose | Recommended Value |
|----------|---------|-------------------|
| `N8N_SECURE_COOKIES` | Force HTTPS cookies | `true` |
| `N8N_EDITOR_BASE_URL` | Public URL for editor | `https://n8n.example.com` |
| `WEBHOOK_URL` | Public webhook URL | `https://n8n.example.com` |
| `N8N_AUTH_EXCLUDED_ENDPOINTS` | Endpoints bypassing auth | (leave empty unless needed) |
| `N8N_PERSONALIZATION_ENABLED` | Disable telemetry | `false` |
| `N8N_DIAGNOSTICS_ENABLED` | Disable n8n diagnostics | `false` |
| `N8N_VERSION_NOTIFICATIONS_ENABLED` | Disable update notifications | `false` (if unwanted) |

### Disable Telemetry

```yaml
environment:
  - N8N_PERSONALIZATION_ENABLED=false
  - N8N_DIAGNOSTICS_ENABLED=false
```

---

## Webhook Security

### Authentication Options

| Level | Security | Configuration |
|-------|----------|--------------|
| **None** | 🔴 Anyone can trigger | `authentication: none` |
| **Header Auth** | 🟡 Shared secret | `authentication: headerAuth` |
| **Basic Auth** | 🟡 Username + password | `authentication: basicAuth` |
| **JWT** | 🟢 Token-based | `authentication: jwtAuth` |

### Secure Webhook Configuration

```json
{
  "type": "n8n-nodes-base.webhook",
  "parameters": {
    "path": "my-secure-endpoint",
    "authentication": "headerAuth",
    "headerAuth": {
      "name": "X-Webhook-Secret",
      "value": "={{ $env.WEBHOOK_SECRET }}"
    },
    "httpMethod": "POST",
    "responseMode": "onReceived",
    "options": {
      "rawBody": false
    }
  }
}
```

### Webhook Path Best Practices

- **Use unpredictable paths:** `/webhook/a7f3b2c9-process-order` not `/webhook/process-order`
- **Never expose sensitive operations** on unauthenticated webhooks
- **Rate limit** via reverse proxy (Nginx: `limit_req_zone`)
- **Validate input** in the first node after the webhook — never trust external data

### Input Validation Pattern

```javascript
// Code node — validate webhook input
const required = ['email', 'name', 'action'];
const input = $input.first().json;

for (const field of required) {
  if (!input[field]) {
    throw new Error(`Missing required field: ${field}`);
  }
}

// Sanitize email
if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(input.email)) {
  throw new Error('Invalid email format');
}

return $input.all();
```

---

## RBAC (Role-Based Access Control)

**Community Edition:** No built-in RBAC. Only one user type (owner).

**Enterprise Edition:** Full RBAC with roles:
- **Owner:** Full access
- **Admin:** Manage workflows, credentials, users
- **Editor:** Create/edit workflows, use shared credentials
- **Viewer:** View workflows and executions

### Workaround for Community Edition

If you need multi-user access on Community Edition:

1. **Use a reverse proxy** with HTTP Basic Auth to restrict access
2. **Create separate n8n instances** per team (Docker isolation)
3. **Upgrade to Enterprise** for proper RBAC

### Single User Best Practices (Community)

Even with one user, follow these practices:
- Use strong passwords (16+ characters)
- Enable 2FA if available
- Restrict network access (VPN or LAN-only)
- Use HTTPS exclusively
- Rotate the n8n API key periodically

---

## Dangerous Pattern Prevention

### Pattern Detection Checklist

Before deploying any workflow, scan for:

| Pattern | Risk Level | Detection |
|---------|-----------|-----------|
| Loop without limit | 🔴 Critical | Split In Batches without batchSize, Code with while(true) |
| Delete without filter | 🔴 Critical | Database DELETE/HTTP DELETE without WHERE/filter |
| Webhook without auth | 🟡 Warning | Webhook node with authentication=none |
| HTTP to private IPs | 🟡 Warning | HTTP Request to 10.x, 172.16-31.x, 192.168.x, localhost |
| Mass email/Send | 🟡 Warning | Loop + email/Send node without cap |
| No error handling | 🟡 Warning | No Error Trigger workflow configured |
| Hardcoded secrets | 🔴 Critical | Code node containing API keys/tokens in plaintext |
| Unvalidated webhook input | 🟡 Warning | Webhook → no validation node before processing |
| Write to production DB | 🟢 Info | Database node targeting production instance |

### Automated Scanning

```python
# Scan workflow JSON for dangerous patterns
import json

def scan_workflow(workflow_json):
    dangers = []
    nodes = workflow_json.get('nodes', [])
    
    for node in nodes:
        node_type = node.get('type', '')
        params = node.get('parameters', {})
        
        # Unauthenticated webhook
        if node_type == 'n8n-nodes-base.webhook':
            if params.get('authentication') == 'none' or not params.get('authentication'):
                dangers.append(f"🟡 {node['name']}: Webhook without authentication")
        
        # Delete operations without filter
        if 'delete' in node_type.lower() or (params.get('operation') == 'delete'):
            if not params.get('filters') and not params.get('conditions'):
                dangers.append(f"🔴 {node['name']}: Delete without filter conditions")
        
        # Split In Batches without size
        if node_type == 'n8n-nodes-base.splitInBatches':
            if not params.get('batchSize') or params.get('batchSize') == 0:
                dangers.append(f"🔴 {node['name']}: Split In Batches without batchSize")
        
        # Code node with potential hardcoded secrets
        if node_type == 'n8n-nodes-base.code':
            code = params.get('jsCode', '')
            secret_patterns = ['api_key', 'password', 'token', 'secret', 'Bearer ', 'sk-']
            for pattern in secret_patterns:
                if pattern in code.lower():
                    dangers.append(f"🔴 {node['name']}: Possible hardcoded secret in Code node")
                    break
    
    return dangers
```

---

## Credential Encryption

See `credentials.md` for full details. Key points:

- All credentials encrypted with AES-256-GCM
- `N8N_ENCRYPTION_KEY` must be backed up securely
- Loss of encryption key = permanent credential loss
- In queue mode, all workers must share the same key

---

## Execution Security

### Prevent Resource Exhaustion

```yaml
# docker-compose.yml
environment:
  - EXECUTIONS_DATA_PRUNE=true      # Auto-delete old executions
  - EXECUTIONS_DATA_MAX_AGE=336     # Keep 14 days (336 hours)
  - EXECUTIONS_TIMEOUT=300          # Kill workflows after 5 minutes
  - EXECUTIONS_TIMEOUT_MAX=600      # Absolute max 10 minutes
  - N8N_PAYLOAD_SIZE_MAX=16          # Max payload size in MB
```

### Rate Limiting via Reverse Proxy

```nginx
# nginx.conf
limit_req_zone $binary_remote_addr zone=webhook:10m rate=10r/m;

location /webhook/ {
    limit_req zone=webhook burst=20 nodelay;
    proxy_pass http://127.0.0.1:5678;
}
```

---

## Backup Security

### What to Back Up

1. **PostgreSQL database** (contains workflows, credentials, execution history)
2. **n8n data volume** (encryption key, config files)
3. **Environment variables** (.env file with passwords and encryption key)

### What NOT to Back Up

- Execution history older than retention period (pruned automatically)
- Test workflow data (clean up before backup)

### Backup Encryption

```bash
# Encrypted backup
docker exec postgres pg_dump -U n8n n8n | \
  gpg --symmetric --cipher-algo AES256 -o n8n_backup_$(date +%Y%m%d).sql.gpg

# Restore
gpg --decrypt n8n_backup_20260502.sql.gpg | \
  docker exec -i postgres psql -U n8n n8n
```