# Security Guide - N8N Automation Secure

## Security Architecture Overview

This skill implements defense-in-depth security with multiple layers of protection:

### Layer 1: Credential Management
- Environment variables only (never in config files)
- No credential storage in repository
- Runtime validation on every use
- Automatic redaction in logs

### Layer 2: Input Validation
- URL format validation (HTTPS only)
- Data sanitization before API calls
- Parameter validation
- SQL injection prevention

### Layer 3: Access Control
- Three permission levels (readonly, restricted, full)
- Granular operation permissions
- Confirmation requirements for dangerous actions
- Principle of least privilege

### Layer 4: Monitoring & Audit
- Complete action logging
- Timestamp tracking
- User attribution
- Suspicious activity detection

### Layer 5: Rate Limiting
- Per-operation limits
- Per-user quotas
- DoS prevention
- Configurable thresholds

### Layer 6: Isolation
- Sandbox support
- Process isolation
- Network segmentation (optional)
- Containerization support

## Threat Model

### Protected Assets
1. **N8N API Keys** - Primary credential for automation platform
2. **Workflows** - Business logic and process definitions
3. **Executions** - Runtime data and process state
4. **Connectors** - Third-party service credentials
5. **System Resources** - CPU, memory, disk access

### Attack Vectors & Mitigations

#### Vector 1: Credential Theft
**Attack:** Stealing N8N API keys from config files
**Mitigation:**
- Credentials only in environment variables (RAM)
- No persistent storage of secrets
- Automatic redaction in logs
- Memory cleanup after use

#### Vector 2: Unauthorized Workflow Execution
**Attack:** Execute workflows without permission
**Mitigation:**
- Permission-based access control
- Confirmation required for executions
- Audit logging of all executions
- Rate limiting prevents abuse

#### Vector 3: Workflow Tampering
**Attack:** Modify or delete workflows maliciously
**Mitigation:**
- Write operations require explicit confirmation
- Two-factor confirmation (display + type)
- Pre-change validation (show diff)
- Rollback capability (audit trail)

#### Vector 4: Data Exfiltration
**Attack:** Steal workflow data or execution results
**Mitigation:**
- HTTPS enforcement
- Certificate validation
- Input/output sanitization
- Data encryption at rest (n8n-side)

#### Vector 5: Denial of Service
**Attack:** Overload n8n instance with requests
**Mitigation:**
- Rate limiting per operation
- Per-user quotas
- Request throttling
- Circuit breakers

#### Vector 6: Code Injection
**Attack:** Inject malicious code via workflows
**Mitigation:**
- Input validation and sanitization
- Function node restrictions
- Sandbox execution environment
- Code review requirements

## Credential Security

### Environment Variables

**Why environment variables?**
1. **Process Isolation:** Only accessible to child processes
2. **No Persistence:** Cleared when process exits
3. **Access Control:** System-level permissions apply
4. **Auditable:** System logs show who set them

**Best Practices:**

```bash
# ✅ GOOD: Set at system level
# /etc/environment
N8N_URL="https://your-n8n.com"
N8N_API_KEY="your-key"

# ✅ GOOD: Temporary for script execution
N8N_URL="..." N8N_API_KEY="..." ./script.sh

# ❌ BAD: In bashrc (compromised user = compromised keys)
echo 'export N8N_API_KEY="..."' >> ~/.bashrc

# ❌ BAD: In config file
# openclaw.json
{
  "env": {
    "N8N_API_KEY": "..."  # Vulnerable to file read attacks
  }
}
```

### Key Rotation

**Rotate API keys regularly:**
1. Generate new key in n8n
2. Update environment variables
3. Test with new key
4. Revoke old key after 24 hours

```bash
# Key rotation script
#!/bin/bash
OLD_KEY="$N8N_API_KEY"
NEW_KEY="$(openssl rand -hex 32)"

echo "Generating new key..."
echo "Update N8N with: $NEW_KEY"

echo "Testing new key..."
export N8N_API_KEY="$NEW_KEY"
curl -X GET "$N8N_URL/api/v1/workflows" \
  -H "X-N8N-API-KEY: $NEW_KEY"

if [ $? -eq 0 ]; then
  echo "New key works. Revoke old key in n8n."
else
  echo "New key failed. Keeping old key."
  export N8N_API_KEY="$OLD_KEY"
fi
```

## Input Validation

### URL Validation

```javascript
function validateN8NUrl(url) {
  // 1. Must be HTTPS
  if (!url.match(/^https:\/\//i)) {
    throw new Error('URL must use HTTPS');
  }

  // 2. Valid domain format
  if (!url.match(/^https:\/\/[a-z0-9.-]+(\.[a-z0-9.-]+)+$/i)) {
    throw new Error('Invalid domain format');
  }

  // 3. No credentials in URL
  if (url.includes('@')) {
    throw new Error('URL must not contain credentials');
  }

  // 4. No suspicious parameters
  if (url.match(/(\b(key|token|secret|password|auth)\b)/i)) {
    throw new Error('URL must not contain secret keywords');
  }

  // 5. No localhost (unless explicitly allowed)
  if (url.match(/127\.0\.0\.1|localhost/) && !ALLOW_LOCALHOST) {
    throw new Error('Localhost URLs are not allowed');
  }

  return url;
}
```

### Data Sanitization

```javascript
function sanitizeData(data) {
  const sensitiveKeys = [
    'password', 'apiKey', 'api_key', 'secret', 'token',
    'credential', 'auth', 'private_key', 'access_token'
  ];

  function clean(obj) {
    if (!obj || typeof obj !== 'object') return obj;

    for (const key in obj) {
      const lowerKey = key.toLowerCase();
      const isSensitive = sensitiveKeys.some(s => lowerKey.includes(s));

      if (isSensitive) {
        obj[key] = '***REDACTED***';
      } else if (typeof obj[key] === 'object') {
        clean(obj[key]);
      } else if (typeof obj[key] === 'string') {
        // Remove potential script tags
        obj[key] = obj[key].replace(/<script[^>]*>.*?<\/script>/gi, '');
      }
    }

    return obj;
  }

  return clean(JSON.parse(JSON.stringify(data)));
}
```

## Permission System

### Permission Levels

#### Readonly Mode
- **Can:** List workflows, view details, execute (with confirmation)
- **Cannot:** Create, update, delete workflows
- **Use Case:** Production environments, read-only monitoring
- **Risk Level:** 🟢 LOW

```bash
export N8N_PERMISSION_MODE="readonly"
```

#### Restricted Mode
- **Can:** All readonly + create/execute workflows
- **Cannot:** Update/delete existing workflows (without 2-factor confirmation)
- **Use Case:** Development environments
- **Risk Level:** 🟡 MEDIUM

```bash
export N8N_PERMISSION_MODE="restricted"
```

#### Full Mode
- **Can:** All operations (with confirmation for destructive actions)
- **Use Case:** Isolated environments, trusted users
- **Risk Level:** 🔴 HIGH

```bash
export N8N_PERMISSION_MODE="full"
```

### Permission Enforcement

```javascript
function checkPermission(action, mode) {
  const permissions = {
    readonly: ['list', 'view', 'status', 'executions'],
    restricted: ['list', 'view', 'status', 'executions', 'create', 'execute'],
    full: ['*']
  };

  const allowed = permissions[mode] || permissions.readonly;

  if (allowed.includes('*') || allowed.includes(action)) {
    return true;
  }

  throw new Error(`Action '${action}' not permitted in '${mode}' mode`);
}

// Usage
try {
  checkPermission('delete', 'readonly');
  // Delete workflow...
} catch (error) {
  console.error('Permission denied:', error.message);
}
```

## Audit Logging

### Log Format

```json
{
  "timestamp": "2024-04-04T00:30:45.123Z",
  "user": "nelson",
  "session": "main",
  "action": "WORKFLOW_EXECUTE",
  "workflowId": "abc123",
  "workflowName": "CI Build",
  "status": "success",
  "durationMs": 234,
  "ip": "127.0.0.1",
  "userAgent": "curl/7.68.0",
  "inputHash": "a1b2c3d4",  // Hashed for privacy
  "permissionMode": "readonly"
}
```

### Log Management

```bash
#!/bin/bash
# scripts/audit-logger.sh

AUDIT_LOG="/data/.openclaw/logs/n8n-audit.log"
MAX_LOG_SIZE="10485760"  # 10MB
ARCHIVE_DIR="/data/.openclaw/logs/archive"

log_action() {
  local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%S.%3NZ")
  local user="${USER:-unknown}"
  local action="$1"
  local status="$2"
  local details="$3"

  # Create log entry
  cat >> "$AUDIT_LOG" <<EOF
{"timestamp":"$timestamp","user":"$user","action":"$action","status":"$status","details":$details}
EOF

  # Rotate if too large
  if [ $(stat -f%z "$AUDIT_LOG" 2>/dev/null || stat -c%s "$AUDIT_LOG") -gt $MAX_LOG_SIZE ]; then
    rotate_logs
  fi
}

rotate_logs() {
  local archive_file="$ARCHIVE_DIR/n8n-audit-$(date +%Y%m%d-%H%M%S).log"
  mkdir -p "$ARCHIVE_DIR"
  mv "$AUDIT_LOG" "$archive_file"
  gzip "$archive_file"
  touch "$AUDIT_LOG"
  chmod 600 "$AUDIT_LOG"
}

# Usage
log_action "WORKFLOW_EXECUTE" "success" '{"workflowId":"abc123"}'
```

### Log Analysis

```bash
# Search for suspicious activity
grep -i "delete\|remove\|dangerous" /data/.openclaw/logs/n8n-audit.log

# Check for errors
grep "status\":\"error" /data/.openclaw/logs/n8n-audit.log

# Count by user
jq -r '.user' /data/.openclaw/logs/n8n-audit.log | sort | uniq -c

# Find unusual patterns
jq 'select(.durationMs > 5000)' /data/.openclaw/logs/n8n-audit.log
```

## Rate Limiting

### Implementation

```javascript
class RateLimiter {
  constructor(maxRequests, windowMs) {
    this.maxRequests = maxRequests;
    this.windowMs = windowMs;
    this.requests = [];
  }

  async check(key = 'default') {
    const now = Date.now();

    // Clean old requests outside window
    this.requests = this.requests.filter(req =>
      req.key === key && (now - req.timestamp) < this.windowMs
    );

    // Check limit
    const count = this.requests.filter(req => req.key === key).length;
    if (count >= this.maxRequests) {
      const resetTime = new Date(now + this.windowMs);
      throw new Error(
        `Rate limit exceeded. ${count}/${this.maxRequests} requests. ` +
        `Resets at ${resetTime.toISOString()}`
      );
    }

    // Record request
    this.requests.push({ key, timestamp: now });
  }
}

// Usage
const apiLimiter = new RateLimiter(10, 60000);  // 10 req/min
const executionLimiter = new RateLimiter(5, 60000);  // 5 exec/min

await apiLimiter.check('nelson');
// ... make API call
```

### Configuration

```bash
# Default limits
export N8N_RATE_LIMIT_API="10/minute"
export N8N_RATE_LIMIT_EXECUTION="5/minute"
export N8N_RATE_LIMIT_BULK="1/5minutes"
```

## Confirmation Requirements

### Two-Factor Confirmation

```javascript
async function confirmDangerousAction(action, details) {
  console.log('\n⚠️  DANGEROUS ACTION');
  console.log('Action:', action);
  console.log('Details:', JSON.stringify(details, null, 2));

  // Step 1: Require typing confirmation
  const readline = require('readline');
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  const confirmation = await new Promise(resolve => {
    rl.question('\nType "I confirm" to proceed: ', resolve);
  });

  rl.close();

  if (confirmation !== 'I confirm') {
    throw new Error('Action cancelled by user');
  }

  // Step 2: Log the action before executing
  await logAction(action, 'pending', details);

  // Step 3: Execute with timeout
  const result = await executeWithTimeout(action, details, 30000);

  // Step 4: Log the result
  await logAction(action, 'completed', { ...details, result });

  return result;
}

function executeWithTimeout(action, details, timeoutMs) {
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => {
      reject(new Error('Action timed out'));
    }, timeoutMs);

    // Execute action
    try {
      const result = performAction(action, details);
      clearTimeout(timer);
      resolve(result);
    } catch (error) {
      clearTimeout(timer);
      reject(error);
    }
  });
}
```

## Sandbox Isolation

### Docker Sandbox

```dockerfile
# Dockerfile.sandbox
FROM node:18-slim

# Non-root user
RUN useradd -m -u 1000 n8n-client
USER n8n-client

# Read-only filesystem
WORKDIR /app
COPY --chown=n8n-client:n8n-client . /app

# Minimal capabilities
COPY --chown=n8n-client:n8n-client script.sh /app/
RUN chmod +x /app/script.sh

# Network isolation (optional)
# --network=none for no external access
# --network=isolated for restricted access

ENTRYPOINT ["/app/script.sh"]
```

```bash
# Build and run
docker build -f Dockerfile.sandbox -t n8n-sandbox .
docker run --rm \
  --read-only \
  --network=isolated \
  --tmpfs /tmp:rw,size=100m \
  -e N8N_URL="$N8N_URL" \
  -e N8N_API_KEY="$N8N_API_KEY" \
  n8n-sandbox
```

### OpenClaw Sandbox Configuration

```json
{
  "agents": {
    "n8n-automation": {
      "sandbox": "require",
      "tools": {
        "allowlist": [
          "curl",
          "read",
          "write"
        ],
        "denylist": [
          "exec",
          "shell",
          "system"
        ]
      },
      "filesystem": {
        "read": [
          "/data/.openclaw/logs/",
          "/tmp/"
        ],
        "write": [
          "/data/.openclaw/logs/"
        ]
      }
    }
  }
}
```

## Incident Response

### Detecting Breaches

```bash
#!/bin/bash
# scripts/security-monitor.sh

AUDIT_LOG="/data/.openclaw/logs/n8n-audit.log"

# Check for suspicious patterns
alert_count=0

# 1. Multiple failed attempts
failed_attempts=$(grep -c "status\":\"error" "$AUDIT_LOG" || echo 0)
if [ "$failed_attempts" -gt 10 ]; then
  echo "⚠️ ALERT: $failed_attempts failed attempts detected"
  ((alert_count++))
fi

# 2. Dangerous operations
dangerous_ops=$(grep -c "delete\|remove" "$AUDIT_LOG" || echo 0)
if [ "$dangerous_ops" -gt 5 ]; then
  echo "⚠️ ALERT: $dangerous_ops dangerous operations detected"
  ((alert_count++))
fi

# 3. Unusual timing
night_activity=$(grep -E 'T(00|01|02|03|04|05):' "$AUDIT_LOG" | wc -l)
if [ "$night_activity" -gt 10 ]; then
  echo "⚠️ ALERT: Unusual night activity detected"
  ((alert_count++))
fi

# 4. Rate limit violations
rate_violations=$(grep -c "Rate limit" "$AUDIT_LOG" || echo 0)
if [ "$rate_violations" -gt 0 ]; then
  echo "⚠️ ALERT: $rate_violations rate limit violations"
  ((alert_count++))
fi

# Report summary
if [ "$alert_count" -gt 0 ]; then
  echo "🚨 SECURITY ALERT: $alert_count suspicious activities detected"
  echo "Review audit log: $AUDIT_LOG"
  exit 1
else
  echo "✅ No suspicious activities detected"
  exit 0
fi
```

### Response Procedure

1. **Immediate Actions:**
   - Rotate all API keys
   - Revoke access for affected users
   - Enable stricter permission mode
   - Increase audit logging frequency

2. **Investigation:**
   - Review audit logs for the breach period
   - Identify affected workflows
   - Check for unauthorized executions
   - Validate system integrity

3. **Recovery:**
   - Restore from backups if needed
   - Patch vulnerabilities
   - Update security policies
   - Schedule security review

## Compliance

### GDPR Compliance

- **Data Minimization:** Only log necessary information
- **Right to Erasure:** Audit logs can be anonymized
- **Access Control:** Role-based permissions
- **Audit Trail:** Complete activity logging

### SOC 2 Compliance

- **Control 1: Access Control** - Permission system
- **Control 2: Change Management** - Confirmation requirements
- **Control 3: Monitoring** - Audit logging
- **Control 4: Incident Response** - Security monitoring

### NIST Framework

- **Identify:** Asset inventory, threat modeling
- **Protect:** Access control, data security
- **Detect:** Audit logging, monitoring
- **Respond:** Incident response procedures
- **Recover:** Backup and restore procedures

## Summary

This security guide provides:
- Defense-in-depth architecture
- Comprehensive threat modeling
- Practical implementations
- Monitoring and audit procedures
- Incident response guidelines
- Compliance considerations

Security is not a feature, it's a mindset. Every code change should be reviewed through this security lens.
