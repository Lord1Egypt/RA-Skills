# OTC Enforcement Discipline

## Critical Rule: No Execution Without Verification

**If OTC is triggered, the operation MUST NOT proceed until the code is verified.**

### Failure Modes to Avoid

1. **Email send failure → skip to execution**
   - ❌ WRONG: "Email failed, but user clearly wants this, so I'll just do it"
   - ✅ RIGHT: "Email failed, operation BLOCKED until email succeeds"

2. **Assuming user intent bypasses OTC**
   - ❌ WRONG: "User explicitly asked for this, so OTC doesn't apply"
   - ✅ RIGHT: "User request triggers OTC → must verify regardless of clarity"

3. **Using alternative methods to bypass OTC**
   - ❌ WRONG: "OTC email failed, let me use another tool to do the operation directly"
   - ✅ RIGHT: "OTC email failed → fix OTC email → retry → verify → then execute"

4. **Natural language confirmation**
   - ❌ WRONG: User says "yes do it" → execute
   - ✅ RIGHT: User must reply with exact code string

### Enforcement Flow

```
Operation requested
  ↓
Trigger evaluation → OTC required?
  ↓ YES
Generate code (stored in state file, never on stdout)
  ↓
Send email → Success?
  ↓ NO → STOP, report error, do NOT execute
  ↓ YES
Wait for user code
  ↓
Verify code → Match?
  ↓ NO → STOP, operation cancelled
  ↓ YES → State file deleted (single-use)
Execute operation
```

### Error Handling

If email sending fails:

1. Report the error to user
2. Do NOT proceed with the operation
3. Do NOT use alternative methods to execute
4. Fix the email configuration
5. Retry the entire OTC flow

### Self-Check Questions

Before executing any operation that triggered OTC:

1. Did I generate a code? (YES required)
2. Did the email send successfully? (YES required)
3. Did the user reply with the exact code? (YES required)
4. Did verify_code.sh return exit code 0? (YES required)

If ANY answer is NO → DO NOT EXECUTE

### Logging Requirement

Every OTC-triggered operation must log:

```
OTC核查：触发
邮件发送：成功/失败
用户验证：通过/失败/未回复
操作执行：是/否
```

Note: The confirmation code itself is NEVER included in logs.
This creates an audit trail for security review.
