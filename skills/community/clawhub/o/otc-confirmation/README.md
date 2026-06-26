# OTC Confirmation 🔐

**One-Time Confirmation for AI Agent Operations**

A security skill that prevents AI agents from executing sensitive operations without explicit human approval. Built on a zero-knowledge architecture where the confirmation code never appears in the agent's context.

一次性确认码安全机制，防止 AI Agent 在无人类授权的情况下执行敏感操作。基于零知识架构——确认码永远不会出现在 Agent 上下文中。

---

## Why This Exists / 为什么需要它

AI agents can read files, run commands, send emails, and deploy code. Without guardrails, a prompt injection or hallucination could trigger irreversible actions. OTC Confirmation adds a human-in-the-loop gate:

```
Agent wants to send email → generates code (never sees it) → code sent to your inbox
→ you reply with code → agent verifies → operation proceeds
```

The agent only checks exit codes. It **never** captures, logs, or displays the confirmation code.

---

## Features

| Feature | Description |
|---------|-------------|
| 🧠 **Zero-Knowledge** | Code flows through secure state files (mode 600), never stdout |
| 🔒 **Cryptographic** | Generated via `/dev/urandom`, not predictable PRNGs |
| ⚡ **Atomic Single-Use** | State file deleted on verification — no replay attacks |
| 🚫 **No Silent Fallbacks** | Email failure = operation blocked, never falls through |
| 📧 **Multi-Backend** | SMTP (curl), send-email skill, himalaya, or custom scripts |
| 📦 **Zero Dependencies** | Pure bash + curl, no Python/Node required |
| 🛡️ **Security Pack** | Full architecture docs + Python reference implementations |

---

## 5-Minute Quick Start / 五分钟上手

### 1. Install / 安装

```bash
clawhub install otc-confirmation
```

### 2. Configure / 配置

Add to your OpenClaw config (`openclaw.json` or `config.yaml`):

```json
{
  "skills": {
    "entries": {
      "otc-confirmation": {
        "enabled": true,
        "env": {
          "OTC_EMAIL_RECIPIENT": "your@email.com",
          "OTC_EMAIL_BACKEND": "smtp",
          "OTC_SMTP_HOST": "smtp.gmail.com",
          "OTC_SMTP_PORT": "465",
          "OTC_SMTP_USER": "your-email@gmail.com",
          "OTC_SMTP_PASS": "your-app-password"
        }
      }
    }
  }
}
```

### 3. Use / 使用

In your agent's system prompt (SOUL.md), add the OTC enforcement rules. Then the agent calls:

```bash
# Step 1: Generate code (written to state file, nothing printed)
bash scripts/generate_code.sh

# Step 2: Send code via email (reads from state file)
bash scripts/send_otc_email.sh "Deploy to production" "session_main"

# Step 3: Wait for user to provide code, then verify
bash scripts/verify_code.sh "$USER_INPUT"
# Exit 0 = verified ✅  |  Exit 1 = failed ❌
```

That's it. The agent never sees the code — it only checks the exit code of `verify_code.sh`.

---

## Architecture / 架构

### Code Flow (Zero-Knowledge)

```
┌─────────────┐     state file      ┌──────────────┐     email      ┌───────┐
│ generate.sh │ ──── (mode 600) ───→│ send_email.sh│ ────────────→ │ Human │
└─────────────┘                     └──────────────┘               └───┬───┘
                                                                       │
                                         code                         │
┌─────────────┐     state file      ┌──────────────┐                  │
│  verify.sh  │ ──── compare ──────→│  exit 0 / 1  │ ←── reply ──────┘
└─────────────┘     (then delete)   └──────────────┘
```

**Key properties:**
- Agent context never contains the code (zero-knowledge)
- State file is `chmod 600` (owner-only read/write)
- State file is deleted after verification (single-use)
- Email failure = hard stop (no fallback)

### What Should Trigger OTC / 触发条件

| Category | Examples |
|----------|----------|
| **External Communication** | Sending emails, posting to social media, API calls to external services |
| **Destructive Operations** | File deletion, service shutdown, database drops, disk operations |
| **Security Changes** | Permission modifications, key rotation, firewall rules, config changes |
| **Financial Operations** | Purchases, transfers, billing changes |
| **Deployment** | Production deploys, infrastructure changes |

---

## Security Architecture Pack / 安全架构文档包

Beyond the core scripts, this skill includes a comprehensive security design document package for teams building secure AI agent systems:

```
ai-devops-agent-security-pack/
├── 00_overview.md                  ← Five-layer defense architecture
├── 01_agent_security_architecture  ← Threat model + trust boundaries
├── 02_confirmation_system.md       ← HMAC-bound OTC deep design
├── 03_permission_guard.md          ← RBAC + 3D scope system
├── 04_command_audit.md             ← Audit logging + sanitization
├── 05_rate_limit.md                ← Token bucket + brute-force defense
├── 06_risk_detection.md            ← Pattern matching + behavioral analysis
│
├── examples/
│   ├── devops_workflow.md          ← End-to-end deployment security walkthrough
│   └── openclaw_config.yaml        ← Ready-to-use integration config
│
└── code_examples/                  ← Python reference implementations
    ├── confirmation_service.py     ← HMAC-bound confirmation (runnable demo)
    ├── permission_guard.py         ← Role-based access control (runnable demo)
    └── audit_logger.py             ← JSONL structured audit logging (runnable demo)
```

**Two implementation paths:**

| Path | When to Use | Tech |
|------|-------------|------|
| **Shell Scripts** (included) | Production use today — lightweight, zero deps | Bash + curl |
| **Python Examples** (reference) | Building your own platform — extensible, typed | Python 3.10+ |

The shell scripts are the **production implementation**. The Python examples are **reference designs** showing how to build these concepts into larger systems.

---

## Integration Examples / 集成示例

### SOUL.md Integration

See `examples/soul_md_integration.md` for a complete template.

Key rules to add:
```markdown
## OTC Pre-Check (mandatory)
Before ANY qualifying operation, state:
"OTC check: [triggered/not triggered] — reason: [...]"

If triggered:
1. Run generate_code.sh
2. Run send_otc_email.sh with operation description
3. Tell user: "Check your email for confirmation code"
4. Wait for code → run verify_code.sh
5. Only proceed if exit code is 0
```

### Multi-Agent Setup

For teams with multiple bots, install the skill in one workspace and reference scripts by absolute path from other bots' SOUL.md:

```markdown
# In other bots' SOUL.md:
OTC scripts: /home/user/.openclaw/workspace/skills/otc-confirmation/scripts/
```

---

## Email Backends / 邮件后端

| Backend | Config Value | Requirements |
|---------|-------------|--------------|
| **SMTP** (default) | `smtp` | curl with SSL support |
| **send-email** | `send-email` | [send-email skill](https://clawhub.com) installed |
| **himalaya** | `himalaya` | [himalaya](https://github.com/pimalaya/himalaya) CLI |
| **Custom** | `custom` | Your script at `OTC_CUSTOM_BACKEND` path |

---

## FAQ

**Q: Can the agent bypass OTC by reading the state file directly?**
A: You should instruct the agent (in SOUL.md) to never read the state file. The scripts handle all file I/O internally. A well-configured agent treats the scripts as black boxes and only checks exit codes.

**Q: What if email delivery fails?**
A: The operation is blocked. There is no fallback. This is by design — silent fallbacks are the #1 cause of security bypasses in agent systems.

**Q: Can I use this without OpenClaw?**
A: Yes. The scripts are standalone bash. Set the required environment variables and call them directly.

**Q: How long is a code valid?**
A: Until it's verified or the state file is overwritten by a new generation. There is no time-based expiry in the shell implementation. The Python reference implementation includes configurable expiry (default 10 minutes).

---

## Version

Current: **3.1.0**

## License

MIT

## Author

[Lewis-404](https://github.com/Lewis-404) · [GitHub Repo](https://github.com/Lewis-404/otc-confirmation)
