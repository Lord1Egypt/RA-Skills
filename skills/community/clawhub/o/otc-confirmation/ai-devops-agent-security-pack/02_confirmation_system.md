# 02 — Confirmation System (OTC Deep Dive)

> The human-in-the-loop mechanism that stops your agent from doing something you'll regret.

## Why One-Time Confirmation?

Passwords protect access. MFA protects identity. OTC protects **intent**.

When an AI agent decides to execute a high-risk operation, the question isn't "is this agent authorized?" (it is — you gave it the tools). The question is: **"Did the human actually want this specific action right now?"**

OTC answers this by requiring the human to confirm each high-risk operation individually, through a secure out-of-band channel.

## Architecture

```
┌────────────┐     ┌──────────────┐     ┌─────────────┐
│   Agent     │────▶│  OTC Guard   │────▶│  Operation  │
│ (requests   │     │ (generates   │     │ (executes   │
│  operation) │     │  code, sends │     │  only after │
│             │◀────│  via email)  │◀────│  verify)    │
│ (receives   │     │ (verifies    │     │             │
│  user code) │     │  code)       │     │             │
└────────────┘     └──────────────┘     └─────────────┘
                          │
                   ┌──────▼──────┐
                   │ State File  │
                   │ (mode 600)  │
                   │ /tmp/otc_*  │
                   └─────────────┘
                          │
                   ┌──────▼──────┐
                   │   Email     │
                   │  (SMTP)     │
                   │ ───────────▶│──── Human reads code
                   └─────────────┘
```

### Key Insight: Zero-Knowledge Agent

The agent **never sees the confirmation code**. This is the critical security property:

1. `generate_code.sh` creates a code and writes it to a state file (mode 600)
2. `send_otc_email.sh` reads the state file and sends the code via email
3. The agent sees only "OTC email sent successfully" on stderr
4. The human reads the code from email and types it into the chat
5. `verify_code.sh` reads the state file, compares, and returns exit code

At no point does the code appear in the agent's context window, stdout, or conversation history. Even if the agent is compromised via prompt injection, it cannot extract the code.

## Code Lifecycle

```
generate_code.sh
    │
    ├── Creates state directory: ${TMPDIR}/otc_state_$(id -u)/
    │   └── permissions: 700
    │
    ├── Generates code: cf-[a-z0-9]{4}
    │   └── source: /dev/urandom → base64 → tr -dc a-z0-9
    │
    └── Writes to: ${state_dir}/pending
        └── permissions: 600

send_otc_email.sh "operation description" "session_id"
    │
    ├── Reads code from state file (never echoes)
    ├── Renders email template (zh/en/auto)
    ├── Sends via SMTP (curl --ssl-reqd)
    │
    ├── On success: exit 0, stderr "OTC email sent"
    └── On failure: exit 1, stderr error message
        └── ⚠️ OPERATION BLOCKED — no fallthrough

verify_code.sh "user_input"
    │
    ├── Reads expected code from state file
    ├── Compares (case-insensitive)
    │
    ├── Match: rm state file → exit 0
    │   └── Code consumed, cannot be reused
    │
    └── Mismatch: exit 1 (state file preserved)
        └── User can retry with correct code
```

## Security Properties

### Property 1: Code Secrecy

The code is never exposed to:
- Agent stdout (scripts output nothing to stdout)
- Agent stderr (only status messages, no codes)
- Conversation context (agent never captures the code)
- Log files (no code logging)
- Error messages (failures don't include the code)

### Property 2: Single Use

After verification (success or consumption):
- State file is deleted (`rm -f`)
- Code cannot be replayed
- A new code must be generated for the next operation

### Property 3: Channel Isolation

- Code is **sent** via email (out-of-band)
- Code is **received** via chat (in-band)
- These are different channels — compromising one doesn't compromise both
- The human must have access to both channels to confirm

### Property 4: Session Binding

The code must be entered in the **same session** where the operation was requested. Due to session isolation, a code entered in a different session (different chat, different channel) won't be routed to the correct verification context.

## Threat Analysis

### Threat: Prompt Injection Bypasses OTC

**Attack**: Injected prompt tells agent to skip OTC and execute directly.

**Defense**: The OTC check is implemented in the agent's core system prompt (SOUL.md) as the highest priority rule. Additionally, the execution scripts themselves enforce the check — even if the agent's reasoning is compromised, the scripts won't execute without verification.

### Threat: Agent Reads State File Directly

**Attack**: Agent uses `cat /tmp/otc_state_*/pending` to read the code.

**Defense**: 
- State file is mode 600 (owner read/write only)
- State directory is mode 700
- In sandboxed environments, the agent may not have filesystem access
- The agent's system prompt explicitly prohibits reading the state file
- Audit logging detects suspicious file access patterns

### Threat: Brute Force Code Guessing

**Attack**: Attacker tries all possible codes (cf-[a-z0-9]{4} = 1,679,616 combinations).

**Defense**:
- Rate limiting on verification attempts (see [05_rate_limit.md](05_rate_limit.md))
- Code expires after configurable timeout (default: 10 minutes)
- Human is notified of failed attempts
- Account lockout after N consecutive failures

### Threat: Email Interception

**Attack**: Attacker intercepts the OTC email.

**Defense**:
- SMTP with TLS encryption (--ssl-reqd)
- Email is ephemeral — code is single-use and short-lived
- The attacker would also need access to the chat channel to submit the code
- For higher security, use end-to-end encrypted email

### Threat: Replay Attack

**Attack**: Attacker captures a valid code and reuses it for a different operation.

**Defense**:
- Code is consumed (state file deleted) on first successful verification
- Code is bound to the session where it was generated
- Future enhancement: HMAC operation binding (see code_examples/confirmation_service.py)

## Advanced: HMAC Operation Binding

The current shell-based implementation provides strong security for personal use. For enterprise deployments, consider HMAC-based operation binding:

```python
import hmac, hashlib

def generate_bound_code(operation_type, parameters, secret_key):
    """Generate a code bound to a specific operation."""
    operation_hash = hashlib.sha256(
        f"{operation_type}:{json.dumps(parameters)}".encode()
    ).hexdigest()
    
    code = generate_random_code()
    
    binding = hmac.new(
        secret_key.encode(),
        f"{code}:{operation_hash}".encode(),
        hashlib.sha256
    ).hexdigest()
    
    store_pending(code_hash=hash(code), binding=binding, operation_hash=operation_hash)
    return code  # Send to human via secure channel

def verify_bound_code(user_code, operation_type, parameters, secret_key):
    """Verify code matches AND is bound to the correct operation."""
    pending = load_pending()
    
    operation_hash = hashlib.sha256(
        f"{operation_type}:{json.dumps(parameters)}".encode()
    ).hexdigest()
    
    if operation_hash != pending.operation_hash:
        raise SecurityError("Operation mismatch — code was generated for a different operation")
    
    expected_binding = hmac.new(
        secret_key.encode(),
        f"{user_code}:{operation_hash}".encode(),
        hashlib.sha256
    ).hexdigest()
    
    if not hmac.compare_digest(expected_binding, pending.binding):
        raise SecurityError("Code mismatch")
    
    consume_pending()  # Delete state — single use
    return True
```

This ensures a code generated for "send email to alice@example.com" cannot be used to approve "delete production database", even if both operations are pending simultaneously.

## Configuration Reference

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OTC_EMAIL_RECIPIENT` | Yes | Email address to receive confirmation codes |
| `OTC_SMTP_USER` | Yes | SMTP username for sending emails |
| `OTC_SMTP_PASS` | Yes | SMTP password |
| `OTC_SMTP_HOST` | No | SMTP server (default: smtp.gmail.com) |
| `OTC_SMTP_PORT` | No | SMTP port (default: 465) |
| `OTC_STATE_DIR` | No | State file directory (default: /tmp/otc_state_$(id -u)) |

### Trigger Categories

Operations that should require OTC confirmation:

| Category | Examples | Risk Level |
|----------|----------|------------|
| External Communication | Email, social media, messaging | High |
| Destructive Operations | File deletion, service shutdown | Critical |
| Security Changes | Permission modifications, key rotation | Critical |
| Financial Operations | Purchases, transfers | Critical |
| Data Export | Backup to external, API data push | High |

See [references/trigger-categories.md](../references/trigger-categories.md) for the complete list.
