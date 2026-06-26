# Integrating OTC Confirmation into AGENTS.md

This guide shows how to integrate OTC Confirmation into your agent's `AGENTS.md` workflow file.

## Step 1: Add OTC Check to Workflow

Add this section to your `AGENTS.md`:

```markdown
## OTC Enforcement Protocol

### Before Every Sensitive Operation

1. **Evaluate trigger conditions**:
   - Is this an external operation?
   - Is this a dangerous local operation?
   - Does this modify security rules?

2. **If YES to any**:
   - Check absolute denial list (destructive irreversible operations)
   - If absolute denial → Refuse immediately
   - Otherwise → Generate and send OTC code

3. **If NO to all**:
   - Execute normally
   - Log: `OTC核查：不触发`

### OTC Generation and Verification

The code never appears in stdout or chat — it flows through a secure state file:

1. Generate: `bash {baseDir}/scripts/generate_code.sh`
2. Send: `bash {baseDir}/scripts/send_otc_email.sh "operation description" "session id"`
3. Reply in chat: "需要确认，请查看你的注册邮箱"
4. Wait for user input
5. Verify: `bash {baseDir}/scripts/verify_code.sh "$USER_INPUT"` (exit 0 = pass)

If email sending fails → operation is BLOCKED. Never fallthrough.

### Audit Logging

Every operation must log its OTC status:

- `OTC核查：不触发` — Safe operation, no confirmation needed
- `OTC核查：触发` — OTC required, code sent
- `OTC核查：拒绝` — Destructive operation, refused
- `OTC通过` — User verified, operation executed
- `OTC失败` — Verification failed, operation cancelled
```

## Step 2: Add to Memory System

If you use a memory system (like `memory/YYYY-MM-DD.md`), log OTC events:

```markdown
## HH:MM — OTC Confirmation for [Operation] [P1]
- Trigger: [External/Dangerous/Security]
- Email sent: yes/no
- User verification: 通过/失败
- Result: 已执行/已取消
```

## Step 3: Periodic Self-Check

Add to your heartbeat or periodic check:

```markdown
## OTC Self-Check (Weekly)

1. Review last 7 days of operations
2. Check if any sensitive operations bypassed OTC
3. Verify email recipient is still correct
4. Test code generation and email sending
5. Update enforcement checklist if needed
```

## Example Workflow

### Scenario: User asks to send an email

```
1. User: "Send an email to john@example.com with the report"

2. Agent evaluates:
   - Is this external? YES (sending email)
   - Trigger OTC

3. Agent generates code:
   bash scripts/generate_code.sh
   → Code stored in secure state file (agent never sees it)

4. Agent sends OTC email:
   bash scripts/send_otc_email.sh "Send email to john@example.com" "Discord #work"
   → Reads code from state file, sends to configured recipient

5. Agent replies in chat:
   "需要确认，请查看你的注册邮箱"

6. User checks email, replies: "cf-k8m2"

7. Agent verifies:
   bash scripts/verify_code.sh "cf-k8m2"
   → Exit code 0 (success), state file deleted (single-use)

8. Agent executes:
   "OTC通过，正在发送邮件..."
   [sends email]

9. Agent logs:
   ## 14:30 — OTC Confirmation for Email Send [P1]
   - Trigger: External operation
   - Email sent: yes
   - User verification: 通过
   - Result: 邮件已发送至 john@example.com
```

## Notes

- Always check the enforcement checklist before operations
- Never skip OTC for convenience
- The code is never visible to the agent — it only checks exit codes
- Log every OTC event for audit trail
