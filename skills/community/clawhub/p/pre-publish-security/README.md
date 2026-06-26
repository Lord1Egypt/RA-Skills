# Pre-Publish Security Protocol v2.0

**Prevents security breaches like exposed credentials in open-source releases.**

## What's New in v2.0

✅ **Smart Frequency Management** - Different scans run at optimal intervals  
✅ **State Tracking** - Knows when each scan last ran  
✅ **Git History Deep Scan** - Catches secrets in commit history  
✅ **Dependency CVE Scanner** - npm/Python vulnerability detection  
✅ **Environment Variable Leak Detection** - Finds exported secrets  
✅ **Automated Scheduling** - Weekly/monthly scans run automatically  

---

## Scan Types & When They Run

### 🚀 Quick Scan (Every Push)
- **Runtime:** ~5 seconds
- **Auto-runs:** Yes (pre-push hook)
- **Checks:** Current files, documentation, basic patterns

### 🕵️ History Scan (Monthly)
- **Runtime:** 2-5 minutes  
- **Auto-runs:** When >30 days since last
- **Checks:** Full git history for secrets

### 📦 Dependency Scan (Weekly)
- **Runtime:** ~30 seconds
- **Auto-runs:** When >7 days since last  
- **Checks:** npm/Python CVEs

### 🔐 Full Audit (On-Demand)
- **Runtime:** 3-6 minutes
- **Auto-runs:** No (manual only)
- **Checks:** Everything above + env vars + hooks

---

## Quick Start

### Install Pre-Push Hook
```bash
# Blocks bad pushes automatically
~/.openclaw/workspace/skills/pre-publish-security/install-hooks.sh ~/repo
```

### Run First-Time History Scan
```bash
# One-time deep dive (or monthly)
~/.openclaw/workspace/skills/pre-publish-security/audit-full.sh ~/repo history
```

### Check Audit Status
```bash
~/.openclaw/workspace/skills/pre-publish-security/schedule.sh status
```

### Run Scheduled Audits
```bash
# Auto-determines which scans to run
~/.openclaw/workspace/skills/pre-publish-security/schedule.sh run ~/repo
```

---

## What It Catches

✅ **Proven Catches:**
- GitHub PAT in git remote URL (CRITICAL)
- `[ORG]` placeholder in homepage (CRITICAL)
- `example.com` in docs (CRITICAL)
- Secrets in git history (CRITICAL)
- npm vulnerabilities (HIGH)
- Missing LICENSE (HIGH)
- Unsafe code patterns (HIGH)

---

## Commands Reference

| Command | Purpose | When |
|---------|---------|------|
| `audit-simple.sh <path>` | Quick scan only | Every push (automatic) |
| `audit-full.sh <path> quick` | Quick scan with tracking | Testing |
| `audit-full.sh <path> history` | Git history scan | Monthly or after incidents |
| `audit-full.sh <path> dependencies` | Dependency CVEs | Weekly |
| `audit-full.sh <path> full` | Everything | Before releases |
| `schedule.sh status` | Show audit history | Checking status |
| `schedule.sh run <path>` | Smart scheduled run | Weekly cron |

---

## State Tracking

**File:** `audit-state.json`

Tracks:
- Last run timestamp for each scan type
- Total scan counts (lifetime)
- Cumulative findings by severity

**View status:**
```bash
~/.openclaw/workspace/skills/pre-publish-security/schedule.sh status
```

---

## Integration Status

| Integration | Status | Details |
|-------------|--------|---------|
| Pre-push hook | ✅ Installed | `openclaw-pii-anonymizer-latest` |
| History scan | ✅ Complete | No secrets found |
| Dependency scan | ⏳ Pending | Run weekly |
| Cron automation | 🔄 Optional | Can add to weekly housekeeping |

---

## Severity Levels

- **CRITICAL** → Blocks push (secrets, credentials)
- **HIGH** → Requires approval (vulns, missing LICENSE)
- **MEDIUM** → Warning (TODOs, missing README)
- **LOW** → Informational

---

## Files

```
pre-publish-security/
├── README.md                    # This file
├── AUDIT-SCHEDULE.md            # Detailed frequency guide
├── SKILL.md                     # ClawHub metadata
├── audit-simple.sh              # Fast scan for pre-push
├── audit-full.sh                # Full scanner with tracking
├── schedule.sh                  # Status & automated runner
├── audit-state.json             # State tracking
├── install-hooks.sh             # Hook installer
├── agents/                      # Sub-agent definitions
│   ├── security-auditor.md
│   ├── code-quality.md
│   ├── docs-validator.md
│   └── license-checker.md
└── patterns/                    # Detection patterns
```

---

## Next Steps

1. ✅ First history scan complete
2. 📅 Add to weekly housekeeping (optional)
3. 🔧 Install on other repos as needed
4. 📊 Monitor `schedule.sh status` weekly

---

## Enhancements Implemented

- [x] Git History Deep Scan
- [x] Dependency CVE Scanner (npm/Python)
- [x] Environment Variable Leak Detection
- [x] State Tracking & Frequency Management
- [x] Automated Scheduling System
- [ ] Pre-commit hook (optional, in addition to pre-push)
- [ ] AI-powered secret detection (future)
- [ ] GitHub Actions integration (future)
- [ ] Whitelist system (future)

---

## Lessons Learned

**2026-03-15:** Exposed GitHub PAT led to this protocol.  
**2026-03-15:** Added smart frequency management - not everything needs to run every time.

**Never again.**
