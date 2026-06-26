# Security Audit Schedule & Tracking

## Scan Types & Frequency

### 🚀 Quick Scan (Every Push)
**Runtime:** ~5 seconds  
**Runs:** Automatically via pre-push hook

**Checks:**
- Current file secret patterns
- Documentation placeholders
- Basic license/README presence

**When:** Every `git push`

---

### 🕵️ Git History Deep Scan (Monthly)
**Runtime:** 2-5 minutes  
**Runs:** Automatically when >30 days since last, or on-demand

**Checks:**
- Full git history for secrets
- Deleted-but-still-accessible credentials
- Historical security issues

**When:**
- First time setup
- Monthly thereafter
- After any security incident
- Before major releases

**Command:**
```bash
~/.openclaw/workspace/skills/pre-publish-security/audit-full.sh . history
```

---

### 📦 Dependency CVE Scan (Weekly)
**Runtime:** ~30 seconds  
**Runs:** Automatically when >7 days since last

**Checks:**
- npm audit (Node.js)
- safety check (Python)
- Known CVEs in dependencies

**When:**
- Weekly
- After dependency updates
- Before releases

**Command:**
```bash
~/.openclaw/workspace/skills/pre-publish-security/audit-full.sh . dependencies
```

---

### 🔐 Full Audit (On-Demand)
**Runtime:** 3-6 minutes  
**Runs:** Manual only

**Includes:**
- Quick scan
- Git history scan
- Dependency scan
- Environment variable leak detection
- Pre-commit hook check

**When:**
- Before major releases
- Security review requests
- Post-incident audits

**Command:**
```bash
~/.openclaw/workspace/skills/pre-publish-security/audit-full.sh . full
```

---

## Automated Scheduling

### Check Audit Status
```bash
~/.openclaw/workspace/skills/pre-publish-security/schedule.sh status
```

**Output:**
```
Last Scans:
  quickScan: 2026-03-15 16:47:00
  historyScan: never
  dependencyScan: never

Scan Counts:
  quickScan: 12
  historyScan: 0
  dependencyScan: 0
```

### Run Scheduled Audits
```bash
# Auto-determines which scans to run based on time since last
~/.openclaw/workspace/skills/pre-publish-security/schedule.sh run ~/path/to/repo
```

**Logic:**
- Always runs quick scan
- Runs dependency scan if >7 days
- Runs history scan if >30 days or never run

---

## Cron Integration (Optional)

Add to weekly housekeeping or standalone:

```bash
# Weekly security audit
openclaw cron add \
  --name "weekly-security-audit" \
  --cron "0 3 * * 0" \
  --announce \
  --message "Run comprehensive security audit: ~/.openclaw/workspace/skills/pre-publish-security/schedule.sh run ~/.openclaw/workspace/skills/openclaw-pii-anonymizer-latest"
```

---

## State Tracking

**File:** `~/.openclaw/workspace/skills/pre-publish-security/audit-state.json`

**Schema:**
```json
{
  "lastRun": {
    "quickScan": "2026-03-15 16:47:00",
    "historyScan": null,
    "dependencyScan": null
  },
  "scanCount": {
    "quickScan": 12,
    "historyScan": 0,
    "dependencyScan": 0
  },
  "findings": {
    "total": 2,
    "critical": 1,
    "high": 1,
    "medium": 0,
    "low": 0
  }
}
```

**Tracks:**
- Last run timestamp for each scan type
- Total scan count (lifetime)
- Cumulative findings by severity

---

## Report Storage

**Location:** `/tmp/security-audit-<timestamp>.md`

**Retention:** Manual cleanup (add to housekeeping script if desired)

**Format:** Markdown with severity badges, findings, and recommended actions

---

## Integration Summary

| Integration | Status | Auto-Run | Frequency |
|-------------|--------|----------|-----------|
| Pre-push hook | ✅ Installed | Yes | Every push |
| Scheduled runner | ✅ Ready | No (manual) | On-demand |
| Cron job | ⏸️ Optional | No | Weekly (if configured) |
| Housekeeping | 🔄 Possible | No | Weekly (if added) |

---

## Next Steps

1. ✅ Installed on: `openclaw-pii-anonymizer-latest`
2. 📅 Schedule first history scan: Run `audit-full.sh . history`
3. 🔧 Add to housekeeping (optional): Update `housekeeping.sh`
4. 📊 Monitor state: `schedule.sh status`

---

## Frequency Decision Tree

```
Is this a git push?
  → YES: Quick scan (automatic)
  → NO: Continue...

Has dependency scan run in last 7 days?
  → NO: Run dependency scan
  → YES: Skip

Has history scan run in last 30 days?
  → NO: Run history scan
  → YES: Skip

Major release or security incident?
  → YES: Run full audit
  → NO: Done
```
