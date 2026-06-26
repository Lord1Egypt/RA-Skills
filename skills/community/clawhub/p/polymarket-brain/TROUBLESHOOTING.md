# 🚨 Polymarket-Brain Troubleshooting Guide

## OBSTACLES ENCOUNTERED & SOLUTIONS (v1.1 - Updated 2026-03-19)

---

## 1️⃣ PATH HANDLING WITH SPACES

### Problem:
```
Error: "The filename, directory name, or volume label syntax is incorrect."
Path: C:\Users\Legion 5i Pro\.browseros\skills\polymarket-brain
```

### Root Cause:
Windows command prompt breaks on paths with spaces when using quotes in certain contexts.

### Solution:
**ALWAYS use short path format (8.3 naming):**
```cmd
# ❌ WRONG (may fail):
cd "C:\Users\Legion 5i Pro\.browseros\skills\polymarket-brain"

# ✅ CORRECT (always works):
cd C:\Users\Legion~1\.browseros\skills\polymarket-brain
```

### Rule:
- `Legion 5i Pro` → `Legion~1`
- Test path first: `cd C:\Users\Legion~1` before running scripts
- In Python scripts, use `os.path.expanduser()` or raw strings: `r"C:\path"`

---

## 2️⃣ DISCORD 403 FORBIDDEN ERROR

### Problem:
```
HTTP Error 403: Forbidden
Discord webhook returns 403 during POST request
```

### Root Cause:
`urllib.request` missing User-Agent header. Discord blocks requests without it.

### Solution:
**Add User-Agent header to ALL Discord requests:**
```python
# ❌ WRONG (gets 403):
req = urllib.request.Request(webhook_url, data=data)

# ✅ CORRECT (works):
req = urllib.request.Request(
    webhook_url,
    data=data,
    headers={"User-Agent": "Polymarket-Brain/1.0", "Content-Type": "application/json"}
)
```

### Files Fixed:
- `polymarket_brain_orchestrator.py` (Phase 4)
- `cnbc-geopolitics-fetcher/src/discord_poster.py` (Phase 1)

---

## 3️⃣ DISCORD 400 BAD REQUEST ERROR

### Problem:
```
HTTP Error 400: Bad Request
Message rejected by Discord API
```

### Root Cause:
Message exceeds Discord's 2000 character limit. Header with `"━" * 50` was 4700 chars.

### Solution:
**Limit all messages to < 2000 characters:**
```python
# ❌ WRONG (too long):
header = "━" * 50  # Creates excessive length

# ✅ CORRECT (safe):
separator = "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"  # 40 chars fixed
```

### Message Length Rules:
- Max: 2000 chars per Discord message
- Header: ~400 chars (safe)
- Market analysis: ~800-1200 chars (safe)
- Summary: ~300 chars (safe)

---

## 4️⃣ DISCORD 429 RATE LIMIT ERROR

### Problem:
```
HTTP Error 429: Too Many Requests
Discord rate limiting rapid sequential posts
```

### Root Cause:
Sending multiple messages without delays triggers rate limiting.

### Solution:
**Add 1.2 second delay between ALL Discord posts:**
```python
import time

# After each message:
time.sleep(1.2)
```

### Where Added:
- `send_discord.py`: Between market messages
- `polymarket_brain_orchestrator.py`: Phase 4 loop
- `discord_poster.py`: Phase 1 article loop

---

## 5️⃣ INVALID POLYMARKET URLs

### Problem:
```
URL: https://polymarket.com/event/will-crude-oil-cl-hit__-by-end-of-march
Result: 404 Not Found (double underscores __ break URL)
```

### Root Cause:
Market URLs had double underscores (`__`) from copy-paste errors.

### Solution:
**Find and replace ALL double underscores:**
```python
# ❌ WRONG:
"https://polymarket.com/event/will-crude-oil-cl-hit__-by-end-of-march"

# ✅ CORRECT:
"https://polymarket.com/event/will-crude-oil-cl-hit-by-end-of-march"
```

### Files Fixed:
- `polymarket_brain_orchestrator.py` (market_urls dict)
- `config.json` (if present)
- Any hardcoded URL strings

### Verification:
Test each URL in browser before deployment.

---

## 6️⃣ WRONG WEBHOOK URL

### Problem:
```
Phase 1 posts to Phase 4 webhook
Phase 4 posts to Phase 1 webhook
Result: Wrong channels, confusion
```

### Root Cause:
Orchestrator used single `DISCORD_WEBHOOK` variable for both phases.

### Solution:
**Use separate webhook variables:**
```python
# ❌ WRONG:
DISCORD_WEBHOOK = "https://discord.com/..."  # Used for both phases

# ✅ CORRECT:
PHASE1_DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1482043765471445333/..."
PHASE4_DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1483478506070474922/..."
```

### Configuration:
- Phase 1 (CNBC News): `1482043765471445333`
- Phase 4 (Market Analysis): `1483478506070474922`

---

## 7️⃣ PLACEHOLDER TEXT IN OUTPUT

### Problem:
```
Phase 4 shows: "Expert analysis indicates market mispricing. See full analysis in output files."
Expected: Actual expert reasoning
```

### Root Cause:
Hardcoded placeholder text instead of dynamic reasoning from expert models.

### Solution:
**Add reasoning field to each market mapping:**
```python
# ❌ WRONG:
"reasoning": "Expert analysis indicates market mispricing..."

# ✅ CORRECT:
"reasoning": "IRGC institutional depth makes regime collapse unlikely. Recent assassinations trigger loyalty purges, not system failure."
```

### Expert Reasoning Sources:
- geopolitics-expert: IRGCistan, Hormuz Siege, Five Pathways models
- the-fed-agent: Dot Plot, Oil Stagflation, FX Strategies models

---

## 8️⃣ IMPORT ERROR (time module)

### Problem:
```
NameError: name 'time' is not defined
time.sleep(1.2) fails in CNBC fetcher
```

### Root Cause:
`time` module not imported at module level.

### Solution:
**Add import at top of file:**
```python
# ❌ WRONG:
import requests
# time.sleep() called but not imported

# ✅ CORRECT:
import requests
import time
```

### Files Fixed:
- `cnbc-geopolitics-fetcher/src/discord_poster.py`

---

## 9️⃣ HISTORY FILE BEHAVIOR

### Problem:
```
User expects: Fresh test posts all articles
Actual: "No new articles" (history preserved)
```

### Root Cause:
History file (`sent_urls.txt`) prevents duplicate posts (expected behavior).

### Solution:
**Manual clear for test mode:**
```cmd
# Production (normal):
python polymarket_brain_orchestrator.py
# History preserved, only NEW articles posted

# Test (fresh):
type nul > ..\cnbc-geopolitics-fetcher\references\sent_urls.txt
python polymarket_brain_orchestrator.py
# History cleared, ALL articles posted
```

### Rule:
- NEVER auto-clear history in production
- ONLY manual clear for testing
- Document this behavior clearly

---

## 𝟭𝟬️⃣ HISTORY FILE CONFUSION

### Problem:
```
Expected fresh articles but none posted
Workflow runs but no Discord messages
```

### Root Cause:
History file (`sent_urls.txt`) preserves URLs across runs. In PROD mode, only NEW articles are posted.

### Solution:
**Understand run modes:**
```cmd
# Production (preserves history):
set POLYMARKET_BRAIN_MODE=PROD
python polymarket_brain_orchestrator.py
# Only NEW articles posted, skips analysis if none

# Test (clears history):
set POLYMARKET_BRAIN_MODE=TEST
python polymarket_brain_orchestrator.py
# ALL articles posted (fresh start)
```

### Rule:
- NEVER auto-clear history in production
- ONLY manual clear for testing
- When no new articles: Phases 2-4 skipped, console notification only

---

## 𝟭𝟭️⃣ PYTHON SCRIPT EXECUTION

### Problem:
```
Script fails to run from certain directories
ModuleNotFoundError: No module named 'X'
```

### Root Cause:
Running script from wrong working directory.

### Solution:
**ALWAYS cd to skill directory first:**
```cmd
# ❌ WRONG (may fail):
python C:\Users\Legion~1\.browseros\skills\polymarket-brain\polymarket_brain_orchestrator.py

# ✅ CORRECT (always works):
cd C:\Users\Legion~1\.browseros\skills\polymarket-brain
python polymarket_brain_orchestrator.py
```

---

## 📋 PRE-RUN CHECKLIST

Before running polymarket-brain:

1. ✅ **Path Test**: `cd C:\Users\Legion~1\.browseros\skills\polymarket-brain`
2. ✅ **Syntax Check**: `python -m py_compile polymarket_brain_orchestrator.py`
3. ✅ **Webhook Config**: Verify both webhooks in orchestrator
4. ✅ **History File**: Decide test vs production mode
5. ✅ **Timeout**: Set 180 seconds for bash command

---

## 🆘 QUICK DEBUG COMMANDS

```cmd
# Test Phase 1 webhook:
python -c "import requests; r=requests.post('https://discord.com/api/webhooks/1482043765471445333/...', json={'content':'test'}); print(r.status_code)"

# Test Phase 4 webhook:
python -c "import requests; r=requests.post('https://discord.com/api/webhooks/1483478506070474922/...', json={'content':'test'}); print(r.status_code)"

# Check history file:
type ..\cnbc-geopolitics-fetcher\references\sent_urls.txt

# Clear history (test mode):
type nul > ..\cnbc-geopolitics-fetcher\references\sent_urls.txt

# Validate URLs:
python -c "import json; d=json.load(open('polymarket_brain_orchestrator.py')); print(d['market_urls'])"
```

---

## 📞 ESCALATION PATH

If stuck:

1. Check TROUBLESHOOTING.md (this file)
2. Review SKILL.md for architecture
3. Test webhooks directly with curl/requests
4. Check output/ directory for analysis files
5. Verify history file state
6. Run with verbose/DEBUG mode if available

---

**Version:** 1.1 | **Last Updated:** 2026-03-18 | **Status:** Production Ready
