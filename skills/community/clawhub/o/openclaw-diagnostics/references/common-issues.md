# OpenClaw Common Issues Diagnostic Rules

This document contains diagnostic rules and checklists for common issues.

## 🔍 Diagnostic Process

### 1. Gather Information
Run `scripts/get-diagnostic-info.sh` to get:
- `openclaw.json` config
- OpenClaw status
- Recent logs

### 2. Run Basic Checks
Run `scripts/check-common-issues.sh` to check common config issues.

### 3. Analyze the Problem
Refer to the diagnostic rules below based on issue type.

---

## 📋 Diagnostic Rules for Common Issues

### Issue: Group Messages Not Responding

**Checklist:**
1. ✅ Is the bot in the group?
2. ✅ Did the user @ mention the bot?
3. ✅ What is `ackReactionScope` set to?
4. ✅ Does `groupPolicy` allow this group?

**Config Analysis:**

| Config | Value | Behavior |
|--------|-------|----------|
| `ackReactionScope` | `group-mentions` | Only reply to @ messages |
| `ackReactionScope` | `all` | Reply to all messages |
| `groupPolicy` | `open` | Allow all groups |
| `groupPolicy` | `allowlist` | Only allow listed groups |
| `groupPolicy` | `denylist` | Allow all except listed groups |

**Common Mistakes:**
- ❌ `groupPolicy: "open"` being flagged as "empty config" — actually `"open"` is fully valid
- ❌ Not confirming whether user @ mentioned the bot first

---

### Issue: DM Not Responding

**Checklist:**
1. ✅ Has the user completed pairing?
2. ✅ Is the user in `allowFrom` list?
3. ✅ Any errors in logs?

**Config Analysis:**

| Config | Description |
|--------|-------------|
| `pairing` | Controls who can DM the bot |
| `allowFrom` | User whitelist |

---

### Issue: Cron Jobs Not Running

**Checklist:**
1. ✅ Is Gateway running?
2. ✅ Is the cron expression correct?
3. ✅ Is the job blocked by mute hours?
4. ✅ Check logs to confirm if triggered

**Reference:** `a632126a` (Troubleshooting - Automation)

---

### Issue: OAuth Auth Failure

**Checklist:**
1. ✅ Run `openclaw models status` to check credential health
2. ✅ Has the token expired?
3. ✅ Is the API key valid?

**Reference:** `87e3285b` (Auth Monitoring)

---

### Issue: Channel Connection Failed

**Checklist:**
1. ✅ Run `openclaw status` to see channel status
2. ✅ Check channel-specific config (Token, Webhook, etc.)
3. ✅ Look for error messages in logs

**Reference:** `092023ff` (Troubleshooting - Channels)

---

## ⚠️ Diagnostic Notes

1. **Don't Over-Diagnose**
   - If config is valid, don't suggest "improvements"
   - Example: `groupPolicy: "open"` is valid, no need to change to object form

2. **Confirm Basics First**
   - Did user @ mention the bot?
   - Is Gateway running?
   - Does config file exist?

3. **Check Logs**
   - Logs usually contain the most direct error info
   - Prioritize ERROR and WARN in logs

4. **Reference Documents**
   - Cite relevant document slugs in diagnosis
   - For details, read from `assets/default-snapshot.json`

---

## 📚 Related Document Index

| Issue Type | Recommended Slugs |
|------------|-------------------|
| Group Messages | `008888be`, `0bfb808e` |
| DM Pairing | `919c126f` |
| Scheduled Tasks | `b239629c`, `e3051492` |
| Auth Issues | `c35ad50f`, `87e3285b` |
| Channel Connection | `092023ff`, channel-specific docs |
| Message Routing | `a99b0ed8` |
