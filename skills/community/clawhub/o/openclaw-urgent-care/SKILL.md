---
name: openclaw-urgent-care
description: >
  Diagnose and recover from common OpenClaw failures — gateway offline, tools locked,
  provider errors, routing issues, and more. Use when OpenClaw stops responding,
  an update broke something, or you need to verify your setup is healthy.
  Full local recovery tool available at Claw Mart.
metadata:
  openclaw:
    emoji: 🚑
    version: "0.1.0"
    author: "Andre Bradford / S.C. Says Poetry LLC"
    tags:
      - recovery
      - troubleshooting
      - ops
      - gateway
      - repair
      - diagnostic
---

# OpenClaw Urgent Care

When your OpenClaw setup breaks, use this skill to diagnose what happened and get the
shortest safe path to recovery.

## When to use this skill

Use when:
- OpenClaw went silent after an update
- The gateway is unreachable or keeps crashing
- Your agent can see messages but can't do anything
- Commands that used to run automatically are now blocked
- A Discord channel is routing to the wrong agent
- Scheduled jobs stopped running
- A plugin or skill failed to install
- You want to verify your setup is healthy before making changes

Do NOT use for:
- Initial OpenClaw installation (use the official docs at openclaw.ai)
- Multi-agent architecture design
- Skill development or publishing

---

## Common Failure Modes

### 1. Gateway Offline

**Symptoms:** Agent stopped responding. Dashboard unreachable. Discord bot silent.

**Quick fix:**
```bash
openclaw gateway restart
```

If that doesn't work after an update:
```bash
openclaw gateway install
openclaw status
```

---

### 2. Agent Can See Messages But Can't Do Anything (v2026.3.2)

**Symptom:** Agent responds but can't run tools, execute commands, or take actions.

**Cause:** The v2026.3.2 update defaulted `tools.profile` to `messages` — restricting the agent to message-only mode.

**Fix:**
1. Open `~/.openclaw/openclaw.json`
2. Find or add: `"tools": { "profile": "full" }`
3. Run: `openclaw gateway restart`

> ⚠️ `full` grants full tool access. Review your security posture before applying.

---

### 3. Provider / Billing / Auth Failure

**Symptoms:** Gateway is up. Agent is silent. Session logs show `disabled:billing`, `usage limits`, or `authentication_error`.

**This is NOT a gateway problem.** The gateway is fine — the model provider is blocking calls.

**For `disabled:billing` (Anthropic cached penalty):**
1. Find: `~/.openclaw/agents/<agent>/agent/auth-profiles.json`
2. Remove the `usageStats.anthropic:default` entry
3. Restart: `openclaw gateway restart`

**For usage cap:**
- Raise the limit in your provider dashboard, or temporarily switch models.

**For auth error:**
- Verify and rotate your API key in `~/.openclaw/openclaw.json`.

---

### 4. Wrong Agent Handling a Channel (Routing / Binding)

**Symptom:** Discord messages go to the default agent instead of the intended one.

**Fix:** Check `~/.openclaw/openclaw.json` → `bindings`. Every non-default Discord account needs an explicit binding:

```json
{
  "agentId": "your-agent-name",
  "match": {
    "channel": "discord",
    "accountId": "your-account-id"
  }
}
```

Then: `openclaw gateway restart`

---

### 5. Channel Connected But Messages Don't Flow

**Symptom:** Channel shows connected/ready. Agent doesn't respond.

**Common causes:** `@mention` required, pairing not approved, allowlist blocking, missing OAuth scope.

**Check:**
```bash
openclaw channels status --probe
openclaw logs --follow
```

Look for: `allowlist blocked`, `pairing pending`, `permission denied`, `missing scope`.

---

### 6. Commands Require Unexpected Approval (Post-Update)

**Symptom:** Commands that ran automatically are now waiting for approval or timing out.

**Cause:** A recent update tightened exec approval defaults.

**Check:**
```bash
openclaw config get | grep -A10 exec
```

Review `ask`, `security`, and `host` settings. Update to match your intended defaults, then restart.

---

### 7. Scheduled Jobs Not Running

**Symptom:** Morning briefing didn't arrive. Cron jobs silent.

**Check:**
```bash
openclaw cron status
openclaw cron list
```

Common causes: scheduler disabled after update, wrong delivery `accountId`, quiet hours active.

---

### 8. Plugin / Skill Won't Load

**Symptom:** A skill fails after an update or fresh install.

**Check:**
```bash
openclaw skills list --failed
openclaw logs --follow
```

Common causes: missing runtime dependency, package shape changed, security scan blocked install.

---

### 9. Gateway Installed But Not Staying Up

**Symptom:** Service shows as loaded but keeps crashing. Dashboard unreachable. Restart loop.

**Check:**
```bash
openclaw gateway status
openclaw logs --follow
openclaw doctor
lsof -i :18789
```

Common causes: port 18789 conflict, auth/bind config error, startup config mismatch.

---

## Automated Recovery Tool

The full **OpenClaw Urgent Care** product automates all of the above:

- Runs preflight, collection, classification, and AI explanation in one command
- Covers all 11 failure modes with confidence scoring and evidence
- Safe auto-fix for gateway restart and tools.profile lockout
- Works completely offline — local model only, no cloud API needed
- Writes a full markdown recovery report

```bash
# Install once
bash /path/to/openclaw-urgent-care/install.sh

# Then run from anywhere
urgentcare
```

**Available at Claw Mart:** [shopclawmart.com](https://www.shopclawmart.com) → Search "OpenClaw Urgent Care"

One-time purchase · All future updates included

---

## Triage Checklist (copy-paste for fast debugging)

```bash
# Step 1 — Is the gateway up?
openclaw status

# Step 2 — Any errors in recent sessions?
openclaw logs --follow

# Step 3 — Is config valid?
openclaw config validate

# Step 4 — Gateway restart (safe to run anytime)
openclaw gateway restart

# Step 5 — If still broken after an update
openclaw gateway install
openclaw doctor
```

---

*Built by Andre Bradford / S.C. Says Poetry LLC*
*Full product: shopclawmart.com → OpenClaw Urgent Care*
