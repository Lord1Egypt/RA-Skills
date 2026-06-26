# 05 — Rate Limiting

> Slowing down attacks without slowing down work.

## Why Rate Limiting for AI Agents?

AI agents can execute operations at machine speed. Without rate limiting:

- A compromised agent could exfiltrate data in milliseconds
- A misconfigured agent could send thousands of emails
- Brute-force attacks on OTC codes could succeed in minutes
- Runaway loops could consume API quotas or cloud resources

Rate limiting adds a **temporal dimension** to security — even if an attacker bypasses other controls, they can only cause damage at a controlled rate.

## Rate Limiting Layers

```
┌─────────────────────────────────────────────┐
│     Layer 1: Global Operations Rate         │
│     (Max operations per minute/hour)        │
├─────────────────────────────────────────────┤
│     Layer 2: Per-Operation Rate             │
│     (Max emails/hour, max deploys/day)      │
├─────────────────────────────────────────────┤
│     Layer 3: OTC Verification Rate          │
│     (Anti-brute-force for confirmation)     │
├─────────────────────────────────────────────┤
│     Layer 4: Resource-Specific Limits       │
│     (API quotas, file operation caps)       │
└─────────────────────────────────────────────┘
```

## Configuration

```yaml
rate_limits:
  global:
    max_operations_per_minute: 30
    max_operations_per_hour: 500
    burst_allowance: 10  # Allow short bursts above the limit
    
  per_operation:
    send_email:
      max_per_hour: 10
      max_per_day: 50
      cooldown_seconds: 30  # Minimum time between sends
      
    exec_command:
      max_per_minute: 10
      max_per_hour: 200
      
    deploy:
      max_per_hour: 3
      max_per_day: 10
      cooldown_seconds: 300  # 5 min between deploys
      
    file_delete:
      max_per_minute: 5
      max_per_hour: 50
      
    api_call:
      max_per_minute: 20
      max_per_hour: 500
      
  otc_verification:
    max_attempts: 5          # Per pending code
    lockout_duration: 300    # 5 minutes after max attempts
    code_expiry: 600         # 10 minutes TTL
    max_pending_codes: 3     # Max concurrent pending confirmations
    
  resource_limits:
    max_file_size_mb: 100
    max_output_length: 10000
    max_concurrent_operations: 5
```

## Implementation

### Token Bucket Algorithm

```python
import time
from threading import Lock

class TokenBucket:
    """Rate limiter using token bucket algorithm.
    
    Allows bursts up to bucket_size, refills at rate tokens/second.
    """
    
    def __init__(self, rate: float, bucket_size: int):
        self.rate = rate              # Tokens per second
        self.bucket_size = bucket_size # Max burst
        self.tokens = bucket_size     # Current tokens
        self.last_refill = time.time()
        self.lock = Lock()
    
    def consume(self, tokens: int = 1) -> bool:
        """Try to consume tokens. Returns True if allowed."""
        with self.lock:
            now = time.time()
            elapsed = now - self.last_refill
            
            # Refill tokens based on elapsed time
            self.tokens = min(
                self.bucket_size,
                self.tokens + elapsed * self.rate
            )
            self.last_refill = now
            
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False
    
    def time_until_available(self) -> float:
        """Seconds until a token will be available."""
        if self.tokens >= 1:
            return 0
        return (1 - self.tokens) / self.rate
```

### OTC Brute-Force Protection

```python
class OTCRateLimiter:
    """Protect OTC verification from brute-force attacks."""
    
    def __init__(self, max_attempts=5, lockout_duration=300):
        self.max_attempts = max_attempts
        self.lockout_duration = lockout_duration
        self.attempts = {}  # session_id -> [timestamps]
        self.lockouts = {}  # session_id -> lockout_until
    
    def check_allowed(self, session_id: str) -> tuple[bool, str]:
        """Check if verification attempt is allowed."""
        now = time.time()
        
        # Check lockout
        if session_id in self.lockouts:
            if now < self.lockouts[session_id]:
                remaining = int(self.lockouts[session_id] - now)
                return False, f"Locked out. Try again in {remaining}s"
            else:
                del self.lockouts[session_id]
                self.attempts.pop(session_id, None)
        
        return True, "OK"
    
    def record_attempt(self, session_id: str, success: bool):
        """Record a verification attempt."""
        now = time.time()
        
        if success:
            # Reset on success
            self.attempts.pop(session_id, None)
            return
        
        # Record failed attempt
        if session_id not in self.attempts:
            self.attempts[session_id] = []
        
        self.attempts[session_id].append(now)
        
        # Clean old attempts (sliding window)
        window = 600  # 10 minutes
        self.attempts[session_id] = [
            t for t in self.attempts[session_id] 
            if now - t < window
        ]
        
        # Check if lockout threshold reached
        if len(self.attempts[session_id]) >= self.max_attempts:
            self.lockouts[session_id] = now + self.lockout_duration
            audit_log.record("OTC_LOCKOUT", session_id, 
                           attempts=len(self.attempts[session_id]))
```

### Composite Rate Limiter

```python
class AgentRateLimiter:
    """Composite rate limiter that checks all layers."""
    
    def __init__(self, config):
        self.global_limiter = TokenBucket(
            rate=config.global.max_per_minute / 60,
            bucket_size=config.global.burst_allowance
        )
        
        self.operation_limiters = {}
        for op_type, limits in config.per_operation.items():
            self.operation_limiters[op_type] = TokenBucket(
                rate=limits.max_per_hour / 3600,
                bucket_size=limits.get("burst", 3)
            )
        
        self.otc_limiter = OTCRateLimiter(
            max_attempts=config.otc.max_attempts,
            lockout_duration=config.otc.lockout_duration
        )
    
    def check(self, operation_type: str, session_id: str = None) -> tuple[bool, str]:
        """Check if an operation is within rate limits."""
        
        # Layer 1: Global rate
        if not self.global_limiter.consume():
            wait = self.global_limiter.time_until_available()
            return False, f"Global rate limit exceeded. Retry in {wait:.1f}s"
        
        # Layer 2: Per-operation rate
        if operation_type in self.operation_limiters:
            if not self.operation_limiters[operation_type].consume():
                wait = self.operation_limiters[operation_type].time_until_available()
                return False, f"{operation_type} rate limit exceeded. Retry in {wait:.1f}s"
        
        # Layer 3: OTC-specific (if applicable)
        if operation_type == "otc_verify" and session_id:
            allowed, reason = self.otc_limiter.check_allowed(session_id)
            if not allowed:
                return False, reason
        
        return True, "OK"
```

## Response to Rate Limit Violations

### Graduated Response

```python
def handle_rate_limit(operation, violation_count):
    """Escalate response based on violation frequency."""
    
    if violation_count <= 3:
        # Soft limit: delay and warn
        return {
            "action": "DELAY",
            "delay_seconds": 5 * violation_count,
            "message": f"Rate limited. Waiting {5 * violation_count}s."
        }
    
    elif violation_count <= 10:
        # Medium limit: deny with cooldown
        return {
            "action": "DENY",
            "cooldown_seconds": 60,
            "message": "Too many operations. Cooling down for 1 minute."
        }
    
    else:
        # Hard limit: lock and alert
        return {
            "action": "LOCK",
            "duration_seconds": 300,
            "alert": True,
            "message": "Excessive operations detected. Agent locked for 5 minutes."
        }
```

## Monitoring Rate Limits

### Metrics to Track

| Metric | Alert Threshold | Description |
|--------|----------------|-------------|
| `rate_limit.hit_count` | > 10/hour | How often limits are triggered |
| `rate_limit.otc_failures` | > 3/10min | Failed OTC attempts |
| `rate_limit.lockout_count` | > 0 | Any lockouts are notable |
| `rate_limit.utilization` | > 80% | Approaching limits |
| `rate_limit.burst_events` | > 5/hour | Burst capacity usage |

### Dashboard Query Examples

```sql
-- Operations approaching rate limits
SELECT operation_type, 
       COUNT(*) as ops_per_hour,
       MAX(configured_limit) as limit
FROM audit_log
WHERE timestamp > NOW() - INTERVAL '1 hour'
GROUP BY operation_type
HAVING COUNT(*) > MAX(configured_limit) * 0.8;

-- OTC brute force detection
SELECT session_id,
       COUNT(*) as failed_attempts,
       MIN(timestamp) as first_attempt,
       MAX(timestamp) as last_attempt
FROM audit_log
WHERE operation_type = 'otc_verify'
  AND decision = 'CONFIRM_FAILED'
  AND timestamp > NOW() - INTERVAL '10 minutes'
GROUP BY session_id
HAVING COUNT(*) >= 3;
```
