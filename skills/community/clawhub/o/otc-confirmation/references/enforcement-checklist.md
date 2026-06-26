# OTC Enforcement Checklist

Before executing any operation, perform this mandatory check:

## Step 1: Trigger Evaluation

Ask yourself:

1. **Is this an external operation?**
   - Sending emails, tweets, messages to third parties
   - API calls to external services
   - Publishing content to public platforms

2. **Is this a dangerous local operation?**
   - File deletion (recursive, bulk)
   - System configuration changes
   - Service restarts or shutdowns
   - Recursive permission changes
   - Disk formatting or partitioning

3. **Does this modify security rules?**
   - Changes to SOUL.md, AGENTS.md confirmation mechanisms
   - Modifications to OTC configuration
   - Changes to access control or authentication

If **YES** to any → Proceed to Step 2 (OTC required)
If **NO** to all → Execute normally, optionally log: `OTC核查：不触发`

## Step 2: Absolute Denial Check

Before generating OTC, check if this is a **destructive irreversible operation**:

- Wiping entire disks or system partitions
- Deleting root-level system directories
- Formatting drives without backup
- Any operation that would render the system unbootable

If YES → **Refuse immediately**, do not offer OTC

## Step 3: Generate and Send OTC

```bash
# Generate code (stored in secure state file, never printed)
bash /path/to/scripts/generate_code.sh

# Send via email (reads code from state file internally)
bash /path/to/scripts/send_otc_email.sh "Brief operation description" "Session identifier"

# Reply in chat (do NOT mention the code)
echo "需要确认，请查看你的注册邮箱"
```

**If email sending fails → STOP. Do NOT proceed with the operation.**

## Step 4: Verify

Wait for user to reply with the code in the **same session**.

```bash
# Verify user input (reads expected code from state file)
bash /path/to/scripts/verify_code.sh "$USER_INPUT"

if [ $? -eq 0 ]; then
  # Execute operation
  echo "OTC通过，执行操作..."
else
  # Reject
  echo "确认码不匹配，操作取消"
fi
```

## Step 5: Log

After execution, log the result:

```
OTC核查：触发 → 已发送确认码 → 用户验证通过 → 操作已执行
```

## Audit Trail Format

Every operation should log its OTC status:

- `OTC核查：不触发` — Operation does not require confirmation
- `OTC核查：触发` — OTC required, code sent
- `OTC核查：拒绝` — Destructive operation, refused outright
- `OTC通过` — User verified, operation executed
- `OTC失败` — Verification failed, operation cancelled
