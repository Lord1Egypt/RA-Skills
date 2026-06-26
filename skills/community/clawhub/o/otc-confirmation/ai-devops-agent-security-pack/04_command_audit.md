# 04 — Command Audit

> If you can't prove what happened, it didn't happen safely.

## Why Audit Logging Matters

AI agents operate autonomously, often executing dozens of operations per session. Without audit logging, you have no way to:

- Investigate incidents ("What exactly did the agent do at 3:47 AM?")
- Detect anomalies ("Why did the agent make 200 API calls in 5 minutes?")
- Demonstrate compliance ("Can you prove no unauthorized data was accessed?")
- Improve security ("Which operations should we add to the CONFIRM list?")

## Audit Log Schema

Every operation produces an audit record with these fields:

```json
{
  "timestamp": "2026-03-08T13:45:00.123Z",
  "event_id": "evt_a7f3b2c1d4e5",
  "session_id": "sess_main_1709884800",
  "agent_id": "laicai",
  "agent_role": "admin",
  
  "operation": {
    "type": "exec_command",
    "command": "kubectl rollout restart deployment/api-server",
    "target": "staging",
    "parameters": {
      "namespace": "default",
      "deployment": "api-server"
    }
  },
  
  "decision": {
    "action": "CONFIRMED",
    "reason": "exec_command requires OTC confirmation",
    "guard_rule": "confirm-exec-commands",
    "otc_verified": true,
    "otc_attempts": 1
  },
  
  "result": {
    "status": "success",
    "exit_code": 0,
    "duration_ms": 2340
  },
  
  "context": {
    "triggered_by": "user_request",
    "user_id": "1467396478723952780",
    "channel": "discord",
    "conversation_id": "conv_abc123"
  }
}
```

### Field Details

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | ISO 8601 | When the operation was attempted |
| `event_id` | string | Unique identifier for this audit event |
| `session_id` | string | Agent session that initiated the operation |
| `agent_id` | string | Which agent performed the operation |
| `operation.type` | enum | Category of operation |
| `operation.command` | string | The actual command/action (sanitized) |
| `decision.action` | enum | ALLOW / DENY / CONFIRMED / CONFIRM_FAILED |
| `decision.otc_verified` | bool | Whether OTC confirmation was obtained |
| `result.status` | enum | success / failure / timeout / error |

## Operation Types

```python
class OperationType(Enum):
    # File operations
    FILE_READ = "file_read"
    FILE_WRITE = "file_write"
    FILE_DELETE = "file_delete"
    FILE_CHMOD = "file_chmod"
    
    # Command execution
    EXEC_COMMAND = "exec_command"
    EXEC_SCRIPT = "exec_script"
    
    # Network operations
    HTTP_REQUEST = "http_request"
    API_CALL = "api_call"
    
    # Communication
    SEND_EMAIL = "send_email"
    SEND_MESSAGE = "send_message"
    POST_SOCIAL = "post_social"
    
    # Infrastructure
    DEPLOY = "deploy"
    RESTART_SERVICE = "restart_service"
    SCALE_RESOURCE = "scale_resource"
    
    # Data operations
    DB_QUERY = "db_query"
    DB_MODIFY = "db_modify"
    DATA_EXPORT = "data_export"
    
    # Security operations
    OTC_GENERATE = "otc_generate"
    OTC_VERIFY = "otc_verify"
    PERMISSION_CHECK = "permission_check"
    CONFIG_CHANGE = "config_change"
```

## Sanitization Rules

Audit logs must capture enough detail for forensics without exposing secrets:

```python
SANITIZE_PATTERNS = {
    # Passwords and tokens
    r'(?i)(password|passwd|pass|token|secret|key|api_key)\s*[=:]\s*\S+': 
        r'\1=***REDACTED***',
    
    # Email content (keep recipient, redact body)
    r'(--mail-data\s+).+': 
        r'\1***REDACTED_BODY***',
    
    # File content in write operations
    r'(echo\s+["\']).*?(["\']\s*>)': 
        r'\1***CONTENT***\2',
    
    # Authorization headers
    r'(Authorization:\s*)(Bearer\s+)?\S+': 
        r'\1***REDACTED***',
    
    # Connection strings
    r'((?:mysql|postgres|mongodb)://\S+?:)\S+(@)': 
        r'\1***@\2',
}

def sanitize_command(command: str) -> str:
    """Remove sensitive data from commands before logging."""
    sanitized = command
    for pattern, replacement in SANITIZE_PATTERNS.items():
        sanitized = re.sub(pattern, replacement, sanitized)
    return sanitized
```

## Log Storage

### Local File Storage (Simple)

```python
import json
from pathlib import Path
from datetime import datetime

AUDIT_DIR = Path.home() / ".openclaw" / "audit"

def write_audit_log(event: dict):
    """Append audit event to daily log file."""
    date_str = datetime.utcnow().strftime("%Y-%m-%d")
    log_file = AUDIT_DIR / f"audit-{date_str}.jsonl"
    
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    
    with open(log_file, "a") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")
```

### Structured Storage (Production)

For production deployments, consider:

- **SQLite** — Local, zero-config, good for single-agent setups
- **PostgreSQL** — Multi-agent, queryable, supports JSON columns
- **Elasticsearch** — Full-text search across logs, dashboards
- **S3 + Athena** — Cost-effective long-term storage with ad-hoc queries

## Querying Audit Logs

### Common Queries

```python
class AuditQuery:
    def denied_operations(self, since: datetime) -> list:
        """Find all denied operations — potential attack indicators."""
        return self.query(
            decision_action="DENY",
            timestamp_gte=since
        )
    
    def failed_otc_attempts(self, since: datetime) -> list:
        """Find failed OTC verifications — brute force indicators."""
        return self.query(
            decision_action="CONFIRM_FAILED",
            timestamp_gte=since
        )
    
    def operations_by_agent(self, agent_id: str, since: datetime) -> list:
        """Get all operations by a specific agent — behavior review."""
        return self.query(
            agent_id=agent_id,
            timestamp_gte=since
        )
    
    def high_risk_operations(self, since: datetime) -> list:
        """Find operations that were high-risk (confirmed or denied)."""
        return self.query(
            decision_action_in=["CONFIRMED", "DENY", "CONFIRM_FAILED"],
            timestamp_gte=since
        )
    
    def external_communications(self, since: datetime) -> list:
        """Track all outbound communications."""
        return self.query(
            operation_type_in=["send_email", "send_message", "post_social", "api_call"],
            timestamp_gte=since
        )
```

### Daily Summary Report

```python
def generate_daily_summary(date: datetime.date) -> dict:
    """Generate a human-readable daily audit summary."""
    events = load_events_for_date(date)
    
    return {
        "date": str(date),
        "total_operations": len(events),
        "by_decision": {
            "allowed": count(events, decision="ALLOW"),
            "confirmed": count(events, decision="CONFIRMED"),
            "denied": count(events, decision="DENY"),
            "failed_confirm": count(events, decision="CONFIRM_FAILED"),
        },
        "by_type": group_count(events, key="operation.type"),
        "unique_agents": unique(events, key="agent_id"),
        "alerts": [
            e for e in events 
            if e["decision"]["action"] in ("DENY", "CONFIRM_FAILED")
        ],
    }
```

## Retention Policy

| Log Type | Retention | Rationale |
|----------|-----------|-----------|
| Security events (DENY, CONFIRM_FAILED) | 1 year | Forensics & compliance |
| Confirmed operations | 90 days | Audit trail |
| Allowed operations | 30 days | Debugging |
| Read-only operations | 7 days | Noise reduction |

### Automated Cleanup

```bash
#!/bin/bash
# Clean up old audit logs based on retention policy
AUDIT_DIR="$HOME/.openclaw/audit"

# Keep security events for 365 days
find "$AUDIT_DIR" -name "audit-*.jsonl" -mtime +365 -exec rm {} \;

# Archive logs older than 30 days
find "$AUDIT_DIR" -name "audit-*.jsonl" -mtime +30 -mtime -365 \
    -exec gzip {} \;
```

## Integration with Alerting

### Real-Time Alerts

Configure alerts for critical patterns:

```yaml
alerts:
  - name: "multiple-denied-operations"
    condition: "count(decision=DENY) > 5 within 10 minutes"
    severity: HIGH
    notify: email
    
  - name: "otc-brute-force"
    condition: "count(decision=CONFIRM_FAILED) > 3 within 5 minutes"
    severity: CRITICAL
    notify: [email, sms]
    action: lock_agent
    
  - name: "unusual-operation-volume"
    condition: "count(*) > 100 within 1 hour"
    severity: MEDIUM
    notify: email
    
  - name: "after-hours-operation"
    condition: "hour(timestamp) NOT BETWEEN 8 AND 22 AND decision IN (CONFIRMED, ALLOW)"
    severity: LOW
    notify: daily_digest
```
