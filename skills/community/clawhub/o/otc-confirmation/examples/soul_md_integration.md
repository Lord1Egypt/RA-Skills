# Integrating OTC Confirmation into SOUL.md

This guide shows how to integrate OTC Confirmation into your agent's `SOUL.md` file.

## Step 1: Install the Skill

```bash
clawhub install otc-confirmation
```

## Step 2: Configure in openclaw.json

Add to your `openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "otc-confirmation": {
        "enabled": true,
        "env": {
          "OTC_EMAIL_RECIPIENT": "your-email@example.com",
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

## Step 3: Add OTC Section to SOUL.md

Add this section to your `SOUL.md`:

```markdown
## OTC Confirmation

- **Recipient email:** (configured via OTC_EMAIL_RECIPIENT env var)
- **Email immutability:** The recipient email is immutable by default. Any request to change it must pass OTC verification first.
- **Trigger conditions:**
  - External operations (send email, post to social media, API calls to third-party services)
  - Dangerous local operations (recursive deletions, system config changes, service restarts)
  - Security rule modifications (changes to SOUL.md confirmation mechanism itself)
- **Absolute denials:** Destructive irreversible operations — reject outright, no OTC offered

### Workflow

Before executing any sensitive operation:

1. **Check trigger conditions** (see trigger-categories reference)
2. **Generate code**: `bash {baseDir}/scripts/generate_code.sh`
3. **Send email**: `bash {baseDir}/scripts/send_otc_email.sh "operation description" "session id"`
4. **Reply in chat**: "需要确认，请查看你的注册邮箱"
5. **Verify user input**: `bash {baseDir}/scripts/verify_code.sh "$user_input"`
6. **Execute if verified** (exit code 0), reject if mismatch (exit code 1)

### Enforcement

- Log every operation: `OTC核查：不触发` or `OTC核查：触发`
- If email fails → operation BLOCKED, never fallthrough
- Never bypass: Natural language confirmations ("yes", "ok") do NOT substitute for the code
```

## Step 4: Test

Test the integration:

```bash
# Generate a code (stored securely, not printed)
bash ~/.agents/skills/otc-confirmation/scripts/generate_code.sh

# Send test email (make sure SMTP is configured)
bash ~/.agents/skills/otc-confirmation/scripts/send_otc_email.sh "Test operation" "Test session"

# Verify with a test input
bash ~/.agents/skills/otc-confirmation/scripts/verify_code.sh "test-input"
echo "Verification result: $?"
```

## Notes

- The code is **never printed to stdout** — it flows through a secure state file
- The skill provides tools, but enforcement is up to your agent's logic
- Keep the email recipient immutable to prevent bypass attempts
