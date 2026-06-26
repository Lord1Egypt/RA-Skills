---
name: otc-confirmation
description: One-Time Confirmation code security mechanism for sensitive agent operations. Generates a cryptographically secure single-use code, delivers it via a private channel (email), and requires the user to reply with the code before execution proceeds. The code never appears in stdout, logs, or chat — it flows through a secure state file. Use when the agent needs to confirm dangerous, irreversible, or externally-visible operations.
metadata: {"openclaw": {"requires": {"env": ["OTC_EMAIL_RECIPIENT", "OTC_SMTP_USER", "OTC_SMTP_PASS"], "anyBins": ["curl"]}, "primaryEnv": "OTC_EMAIL_RECIPIENT"}}
---

# OTC Confirmation 3.0

A security pattern that prevents unauthorized or accidental execution of sensitive operations by requiring out-of-band confirmation via a one-time code.

## What's New in 3.0

- 🔐 **Code never touches stdout** — flows through a secure state file (mode 600), preventing leakage via logs or agent context
- 🔒 **Cryptographically secure generation** — uses `/dev/urandom` instead of `$RANDOM`
- 🛡️ **Atomic single-use enforcement** — state file is deleted on successful verification
- 🚫 **No silent fallbacks** — email failure is always fatal, never falls through to execution
- 🧹 **No arbitrary file sourcing** — credentials loaded exclusively via environment variables
- ✅ **Proper metadata declaration** — required env vars declared in skill metadata

## How It Works

```
User request (sensitive op)
  → Agent runs generate_code.sh (code stored in state file, never printed)
  → Agent runs send_otc_email.sh (reads code from state file, sends email)
  → Agent replies in chat: "需要确认，请查看邮箱"
  → User reads email, replies with code in ORIGINAL chat session
  → Agent runs verify_code.sh (reads state file, compares, deletes on match)
  → Agent executes operation
```

The code is **single-use** — the state file is deleted immediately after successful verification.

**Key security property:** The agent never captures or sees the code in its context. It only checks exit codes.

## Quick Start

### 1. Install

```bash
clawhub install otc-confirmation
```

### 2. Configure

**Option A: OpenClaw Config (Recommended)**

Add to `openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "otc-confirmation": {
        "enabled": true,
        "env": {
          "OTC_EMAIL_RECIPIENT": "user@example.com",
          "OTC_EMAIL_BACKEND": "smtp",
          "OTC_SMTP_HOST": "smtp.gmail.com",
          "OTC_SMTP_PORT": "587",
          "OTC_SMTP_USER": "your-email@gmail.com",
          "OTC_SMTP_PASS": "your-app-password"
        }
      }
    }
  }
}
```

**Option B: Environment Variables**

```bash
export OTC_EMAIL_RECIPIENT=user@example.com
export OTC_EMAIL_BACKEND=smtp
export OTC_SMTP_HOST=smtp.gmail.com
export OTC_SMTP_PORT=587
export OTC_SMTP_USER=your-email@gmail.com
export OTC_SMTP_PASS=your-app-password
```

### 3. Use in Your Agent

```bash
SKILL_DIR="{baseDir}"

# Step 1: Generate code (stored in secure state file, nothing printed to stdout)
bash "$SKILL_DIR/scripts/generate_code.sh"

# Step 2: Send email (reads code from state file internally)
bash "$SKILL_DIR/scripts/send_otc_email.sh" "Send email to john@example.com" "Discord #work"

# Step 3: Reply in chat (do NOT mention the code)
echo "需要确认，请查看你的注册邮箱"

# Step 4: Wait for user input, then verify (reads expected code from state file)
bash "$SKILL_DIR/scripts/verify_code.sh" "$USER_INPUT"

if [ $? -eq 0 ]; then
  echo "OTC通过，执行操作..."
  # Execute the operation
else
  echo "确认码不匹配，操作取消"
fi
```

## Email Backends

### SMTP (Default, Zero Dependencies)

Uses curl to send email directly via SMTP. No additional tools required.

```bash
export OTC_EMAIL_BACKEND=smtp
export OTC_SMTP_HOST=smtp.gmail.com
export OTC_SMTP_PORT=587
export OTC_SMTP_USER=your-email@gmail.com
export OTC_SMTP_PASS=your-app-password
```

### send-email Skill

If you have the `send-email` skill installed:

```bash
export OTC_EMAIL_BACKEND=send-email
```

### himalaya CLI

If you have `himalaya` installed:

```bash
export OTC_EMAIL_BACKEND=himalaya
```

### Custom Script

Use your own email sending script:

```bash
export OTC_EMAIL_BACKEND=custom
export OTC_CUSTOM_EMAIL_SCRIPT=/path/to/your/send_email.sh
```

Your script must accept three arguments: `<to> <subject> <body>`

**Security note:** Ensure the custom script has restricted permissions and is located in a trusted directory. The skill validates that the script exists and is executable before invoking it.

## Trigger Conditions

OTC should be triggered for:

1. **External operations**: Sending emails, posting to social media, API calls to third parties
2. **Dangerous local operations**: Recursive deletions, system config changes, service restarts
3. **Security rule modifications**: Changes to SOUL.md, AGENTS.md confirmation mechanisms

See `references/trigger-categories.md` for detailed categories.

## Enforcement Checklist

Before every operation, follow the enforcement checklist:

1. Evaluate trigger conditions
2. Check absolute denial list (destructive irreversible operations → refuse outright)
3. Generate and send OTC if required
4. Verify user input
5. Log the result

See `references/enforcement-checklist.md` for the complete workflow.

## Integration Guides

- **SOUL.md integration**: `examples/soul_md_integration.md`
- **AGENTS.md integration**: `examples/agents_md_integration.md`

## Security Rules

1. **Code secrecy**: The code is NEVER printed to stdout, displayed in chat, or included in logs. It flows exclusively through a secure state file (mode 600).
2. **Single-use**: The state file is atomically deleted after successful verification. Each operation requires a fresh code.
3. **Session binding**: The code must be verified in the same session/channel where the operation was requested.
4. **No bypass**: Natural language confirmations ("yes", "do it", "approved") do NOT substitute for the code. Only the exact code string counts.
5. **Email immutability**: The recipient email address should be treated as immutable by default. Any request to change it must itself pass OTC verification first.
6. **No silent fallback**: If email sending fails, the operation is BLOCKED. The agent must never fall through to execution.
7. **Escalation**: If the same operation fails OTC 3 times consecutively, alert the user and refuse further attempts until a new session.

## Scripts Reference

### generate_code.sh

Generate a cryptographically secure random OTC code.

```bash
bash scripts/generate_code.sh [prefix] [length]
# Default: cf-XXXX (prefix="cf", length=4)
# Code is stored in a secure state file (mode 600)
# Nothing is printed to stdout
```

### send_otc_email.sh

Send OTC confirmation email. Reads the code from the state file.

```bash
bash scripts/send_otc_email.sh <operation> [session] [lang]
# Example:
bash scripts/send_otc_email.sh "Send email to john@example.com" "Discord #work"
# If email fails → exits with error (never falls through)
```

### verify_code.sh

Verify user input against the stored code.

```bash
bash scripts/verify_code.sh <user_input>
# Exit code 0: verified (state file deleted — single-use)
# Exit code 1: mismatch or no pending code
```

### send_email_smtp.sh

Low-level SMTP email sending (used internally by send_otc_email.sh).

```bash
bash scripts/send_email_smtp.sh <to> <subject> <body>
# Requires OTC_SMTP_* environment variables
```

## Troubleshooting

### Email not sending

1. Verify SMTP credentials are configured: `test -n "$OTC_SMTP_USER" && echo "set" || echo "not set"`
2. Test SMTP connection: `curl -v smtp://$OTC_SMTP_HOST:$OTC_SMTP_PORT`
3. Check firewall/network: Ensure port 587 (or 465) is open
4. Gmail users: Use an [App Password](https://support.google.com/accounts/answer/185833), not your regular password

### Code verification failing

1. Check for extra whitespace: User input must match exactly
2. Ensure code is used in the same session where it was requested
3. Verify code hasn't been used already (single-use — state file is deleted after success)

### Backend not found

If using `send-email` or `himalaya` backend:

```bash
# Check if command exists
command -v send-email
command -v himalaya

# Install if missing
clawhub install send-email  # or install himalaya
```

## License

MIT

## Author

Lewis-404
