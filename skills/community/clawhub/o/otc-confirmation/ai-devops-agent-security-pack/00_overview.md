# AI DevOps Agent Security Pack — Overview

> **Why your AI agent needs a safety net before it `rm -rf`s your production.**

## The Problem

AI agents are powerful. They can deploy code, manage infrastructure, send emails, and execute shell commands — all autonomously. But with great power comes great risk:

- An agent misinterprets a prompt and runs a destructive command
- A prompt injection tricks the agent into exfiltrating secrets
- A well-meaning agent sends an email to the wrong recipient
- An automated pipeline deletes resources without human awareness

**The core tension**: You want agents to be autonomous (that's the point), but you need guardrails for actions that can't be undone.

## The Solution: Defense in Depth

This security pack implements a **layered defense model** for AI agent operations:

```
┌─────────────────────────────────────────────┐
│            Layer 5: Risk Detection          │
│         (Pattern matching, anomaly          │
│          detection, threat scoring)         │
├─────────────────────────────────────────────┤
│            Layer 4: Rate Limiting           │
│        (Brute-force protection,             │
│         operation throttling)               │
├─────────────────────────────────────────────┤
│            Layer 3: Command Audit           │
│        (Full operation logging,             │
│         forensic trail)                     │
├─────────────────────────────────────────────┤
│            Layer 2: Permission Guard        │
│        (Role-based access control,          │
│         scope enforcement)                  │
├─────────────────────────────────────────────┤
│            Layer 1: OTC Confirmation        │
│        (Human-in-the-loop for               │
│         high-risk operations)               │
└─────────────────────────────────────────────┘
```

Each layer is **independently useful** but **strongest when combined**.

## What's in This Pack

| Document | Purpose |
|----------|---------|
| [01 — Agent Security Architecture](01_agent_security_architecture.md) | Big-picture security design for AI agent systems |
| [02 — Confirmation System](02_confirmation_system.md) | Deep dive into OTC (One-Time Confirmation) mechanism |
| [03 — Permission Guard](03_permission_guard.md) | Role-based access control for agent operations |
| [04 — Command Audit](04_command_audit.md) | Operation logging and forensic trail |
| [05 — Rate Limiting](05_rate_limit.md) | Brute-force protection and operation throttling |
| [06 — Risk Detection](06_risk_detection.md) | Pattern matching and anomaly detection engine |

### Examples & Code

| File | Description |
|------|-------------|
| [DevOps Workflow](examples/devops_workflow.md) | End-to-end DevOps scenario with all layers |
| [OpenClaw Config](examples/openclaw_config.yaml) | Ready-to-use OpenClaw integration config |
| [Confirmation Service](code_examples/confirmation_service.py) | HMAC-bound confirmation with hash storage |
| [Permission Guard](code_examples/permission_guard.py) | Permission guard implementation |
| [Audit Logger](code_examples/audit_logger.py) | Structured audit logging system |

## Design Principles

### 1. Zero Silent Failures

When a safety check fails, the operation **stops**. No fallbacks, no "try the next method", no "well, the user probably meant yes". A failed check means a blocked operation, period.

```
❌ Email send failed → try SMS → try Slack → just do it anyway
✅ Email send failed → BLOCKED. Fix the email. Try again.
```

### 2. Secrets Never Touch stdout

Confirmation codes, API keys, passwords — nothing sensitive ever appears in agent-visible output. Codes are stored in permission-restricted state files (mode 600) and read directly by verification scripts. The agent never sees the code.

### 3. Operation Binding

A confirmation code is bound to a specific operation. You can't use a code generated for "send email" to approve "delete database". Each code carries an operation hash that must match at verification time.

### 4. Atomic Single-Use

Codes are consumed on first use (whether successful or not). The state file is deleted immediately after verification. No replay, no reuse.

### 5. Fail Closed

When in doubt, deny. Unknown operation types → require confirmation. Missing configuration → block execution. Ambiguous user intent → ask for clarification.

## Who Is This For

- **AI agent developers** building autonomous systems that interact with infrastructure
- **DevOps engineers** integrating AI assistants into deployment pipelines
- **Platform teams** establishing security policies for AI-powered tooling
- **Individual users** running personal AI assistants (like OpenClaw) with system access

## Quick Start

1. Install the OTC Confirmation Skill:
   ```bash
   clawhub install otc-confirmation
   ```

2. Configure SMTP for secure code delivery:
   ```bash
   export OTC_EMAIL_RECIPIENT="your@email.com"
   export OTC_SMTP_USER="smtp-user"
   export OTC_SMTP_PASS="smtp-password"
   ```

3. Integrate into your agent's system prompt (see [examples/soul_md_integration.md](../examples/soul_md_integration.md))

4. Read the architecture docs for deeper customization

## License

MIT — Use freely, contribute back if you can.
