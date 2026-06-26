# Polymarket-Brain v1.1 - Complete Skill Documentation

## 🎯 Purpose

Automated geopolitical and macroeconomic analysis pipeline that:
1. Fetches breaking news from CNBC World Politics
2. Routes to expert analysts (geopolitics-expert / the-fed-agent)
3. Matches analyses to Polymarket prediction markets
4. Delivers actionable trading recommendations to Discord

**End Goal:** Identify market mispricing opportunities where expert probability diverges from market odds.

---

## 🏗️ Architecture (4 Phases)

### Phase 1: CNBC News Fetching
**Component:** `cnbc-geopolitics-fetcher`

```python
# Execution
cd cnbc-geopolitics-fetcher
python scripts/fetch_cnbc_geopolitics.py --config references/config.md --count 5
```

**Behavior:**
- Fetches exactly 5 articles from CNBC World Politics RSS
- Deduplicates against `references/sent_urls.txt` history
- Posts NEW articles individually to Discord (not batched)
- Exit code 0 always (even when no new articles)

**Webhook:** `https://discord.com/api/webhooks/1482043765471445333/...`

**History Management:**
- Tracks all sent URLs in `sent_urls.txt`
- Skips duplicates forever
- Growth = fewer posts over time (expected, not broken)

**No New Articles Behavior:**
- Does NOT post to Discord
- Returns exit code 0
- **Orchestrator skips Phases 2-4** (no analysis, no market matching, no Discord posts)
- **Prints console notification only** (not sent to Discord)
- Clean exit with clear status message

---

### Phase 2: Expert Analysis

**Classification Logic:**

| News Content | Classification | Expert Skill |
|--------------|----------------|--------------|
| Military strikes, troop movements, Iran, Russia, Middle East, oil, war | **Geopolitics** | `geopolitics-expert` |
| Fed decisions, inflation, employment, Treasury yields, rates, currency | **Macroeconomics** | `the-fed-agent` |
| Mixed (war + markets, oil + Fed) | **Both** | Run both skills |

**Expert Models:**

#### geopolitics-expert
**Frameworks:**
- **IRGCistan**: Military-dominated state analysis
- **Hormuz Siege**: Blockade impact assessment
- **Five Pathways**: Conflict termination probabilities

**Outputs:**
- Conflict duration probability
- Commodity impacts (oil, gold, USD)
- Trading opportunities

#### the-fed-agent
**Frameworks:**
- **Dot Plot Analysis**: Fed stance changes
- **Oil Stagflation**: Energy shock impact
- **FX Strategies**: EUR/USD positioning

**Outputs:**
- Rate hike probability
- Stagflation risk assessment
- Currency recommendations

---

### Phase 3: Market Matching

**8 Monitored Polymarket Markets:**

| # | Market Name | Resolution Date | Expert Probability |
|---|-------------|-----------------|-------------------|
| 1 | Will Iranian regime fall by June 30? | Jun 30, 2026 | 15% |
| 2 | US-Iran ceasefire by December 31 | Dec 31, 2026 | 55% |
| 3 | Iran conflict ends by December 31 | Dec 31, 2026 | 60% |
| 4 | US forces enter Iran by December 31 | Dec 31, 2026 | 35% |
| 5 | Iran leadership change by December 31 | Dec 31, 2026 | 85% |
| 6 | Fed decision in March | Mar 2026 | 95% |
| 7 | Will crude oil CL hit $100+ by end of March | Mar 2026 | 90% |
| 8 | US recession by end of 2026 | End 2026 | 40% |

**Matching Process:**
1. Extract market odds from Polymarket (hardcoded in v1.1)
2. Apply expert probability assessment from Phase 2
3. Calculate edge (market vs expert mispricing)
4. Generate recommendation (Strong Yes/No, Lean, Fair Value)

**Recommendation Logic:**

| Market Odds | Expert Prob | Gap | Recommendation |
|-------------|-------------|-----|----------------|
| < 30% Yes | Expert > 50% | 20%+ | **Strong Yes** ✅ |
| > 70% Yes | Expert < 50% | 20%+ | **Strong No** ❌ |
| Similar | Similar | < 10% | **Fair Value** ⚖️ |
| Expert > 70% | Market < 70% | - | **Underpricing** |
| Expert < 40% | Market > 60% | - | **Overpricing** |

---

### Phase 4: Discord Dispatch

**Message Format:**

**Header:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧠 POLYMARKET-BRAIN WORKFLOW ACTIVATED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Time: YYYY-MM-DD HH:MM:SS
Version: 1.1
Markets Analyzing: X
```

**Each Market (sent individually, 1.2s delay):**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧠 POLYMARKET-BRAIN ANALYSIS: MARKET N/X
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 MARKET: [Market Name]

📅 Resolution Date: [Date]
📊 Market Odds: XX% Yes
🎯 Expert Probability: XX% Yes
💡 Recommendation: [Emoji] [Text]

📝 REASONING:
[Detailed reasoning from expert analysis]

🔗 Link: [Polymarket URL]

📈 Edge: XX% market mispricing

Analyzed by: [expert] | Confidence: HIGH
```

**Summary:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧠 POLYMARKET-BRAIN WORKFLOW COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Summary:
• Total Markets Analyzed: X
• Strong Buys (Yes): X
• Strong Sells (No): X
• Expert Sources: [list]
• Data Source: CNBC World Politics

⏱️ Workflow Time: [timestamp]
🔄 Next Update: Check back for fresh analysis

Disclaimer: This is automated analysis. Not financial advice.
```

**Rate Limit:** 1.2 seconds between ALL messages (prevents Discord 429 rate limiting)

**Webhook:** `https://discord.com/api/webhooks/1483478506070474922/...`

---

## 🔧 Installation & Migration

### Fresh Environment Setup

#### Step 1: Copy Skills
```bash
# Windows
xcopy /E /I "C:\Users\Legion 5i Pro\.browseros\skills" "D:\new-env\.browseros\skills"

# Linux/Mac
cp -r ~/.browseros/skills /new/path/.browseros/skills
```

#### Step 2: Verify Python Dependencies
```bash
pip install requests crawl4ai python-dateutil
pip list | findstr "requests crawl4ai"
```

#### Step 3: Configure Webhooks

**CNBC Fetcher:**
Edit `cnbc-geopolitics-fetcher/references/config.md`:
```
DISCORD_WEBHOOK=https://discord.com/api/webhooks/1482043765471445333/YOUR_KEY_HERE
```

**Polymarket Brain:**
Edit `polymarket_brain_orchestrator.py` (lines 15-16):
```python
PHASE1_DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1482043765471445333/YOUR_KEY"
PHASE4_DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1483478506070474922/YOUR_KEY"
```

#### Step 4: Test Run
```bash
cd polymarket-brain
python polymarket_brain_orchestrator.py
```

**Expected:** 5 articles posted, 5-8 markets analyzed, all sent to Discord.

---

## 🚨 Troubleshooting Guide

### Issue: 403 Forbidden on Discord Post
**Cause:** Missing User-Agent header in urllib requests

**Fix:**
```python
req = urllib.request.Request(webhook_url, data=data, headers={
    'User-Agent': 'Polymarket-Brain/1.1',
    'Content-Type': 'application/json'
})
```

### Issue: 400 Bad Request
**Cause:** Message exceeds Discord 2000 character limit

**Fix:** Shorten separator from `"━" * 50` to fixed 40 chars

### Issue: No Articles Posted to Discord
**Cause:** All URLs already in `sent_urls.txt` history

**Fix:** This is EXPECTED behavior. History growth = fewer new articles.
For testing: `type nul > references/sent_urls.txt`

### Issue: Invalid Polymarket URL (404)
**Cause:** Double underscores in URL (`__`) instead of hyphens

**Fix:**
```python
# Wrong: https://polymarket.com/event/will-crude-oil-cl-hit__-by-end-of-march
# Right: https://polymarket.com/event/will-crude-oil-cl-hit-100-by-end-of-march
```

### Issue: Placeholder Reasoning in Messages
**Cause:** Hardcoded text instead of expert analysis

**Fix:** Use actual `reasoning` field from expert analysis output

### Issue: Rate Limiting (429 Too Many Requests)
**Cause:** Rapid sequential posts without delay

**Fix:** Add `time.sleep(1.2)` between ALL Discord messages

### Issue: PowerShell Variable Parsing Errors
**Cause:** PowerShell one-liners with `%VARIABLE%` syntax

**Fix:** Use batch files (`.bat`) instead of PowerShell for Windows

### Issue: Path with Spaces Fails
**Cause:** `"Legion 5i Pro"` breaks command parsing

**Fix:** Use short name `Legion~1` or full quotes:
```cmd
cd "C:\Users\Legion 5i Pro\.browseros\skills\polymarket-brain"
```

---

## 📁 File Structure

```
polymarket-brain/
├── polymarket_brain_orchestrator.py    # Main orchestrator (edit webhooks here)
├── SKILL.md                            # This documentation
├── README.md                           # Quick start guide
├── VERSION                             # v1.1
├── output/                             # Analysis JSON outputs (auto-created)
│   ├── analysis_input_1.json
│   ├── analysis_input_2.json
│   └── ...
└── logs/                               # Execution logs (auto-created)

cnbc-geopolitics-fetcher/
├── scripts/
│   └── fetch_cnbc_geopolitics.py       # News fetcher script
├── references/
│   ├── config.md                       # Webhook config (LOCKED - edit here)
│   └── sent_urls.txt                   # URL history (clear for test)
├── SKILL.md                            # Detailed fetcher docs
└── LOCKED.md                           # Protection marker (READ BEFORE EDIT)
```

---

## 🧪 Testing Commands

### Production Run
```cmd
cd C:\Users\Legion 5i Pro\.browseros\skills\polymarket-brain
python polymarket_brain_orchestrator.py
```

### Fresh Test (Clear History)
```cmd
type nul > C:\Users\Legion 5i Pro\.browseros\skills\cnbc-geopolitics-fetcher\references\sent_urls.txt
cd C:\Users\Legion 5i Pro\.browseros\skills\polymarket-brain
python polymarket_brain_orchestrator.py
```

### Verify Webhooks
```python
import requests
webhook = "https://discord.com/api/webhooks/1482043765471445333/YOUR_KEY"
response = requests.post(webhook, json={"content": "test"})
print(response.status_code)  # Should be 204
```

---

## 📊 Expert Probability Reference

### Geopolitics-Expert Mappings

| Market | Expert Prob | Reasoning Framework |
|--------|-------------|---------------------|
| Iran regime fall | 15% | IRGC institutional depth, loyalty purges |
| US-Iran ceasefire | 55% | Trump unilateral stance, forever war risk |
| Iran conflict ends | 60% | Five Pathways, 35% forever war |
| US forces enter Iran | 35% | Ground invasion unlikely, air sufficient |
| Iran leadership change | 85% | ALREADY OCCURRED (Mojtaba appointed) |
| Oil $100+ March | 90% | Hormuz closure 40%, oil $140-160 risk |

### The-Fed-Agent Mappings

| Market | Expert Prob | Reasoning Framework |
|--------|-------------|---------------------|
| Fed decision March | 95% | Fed HOLD at 95% per CME FedWatch |
| US recession 2026 | 40% | Stagflationary pressure, oil shocks |

---

## 🔐 Security & Best Practices

### Webhook Security
- **Never commit** webhook URLs to version control
- **Use environment variables** in production:
  ```python
  import os
  PHASE1_WEBHOOK = os.environ.get('PHASE1_DISCORD_WEBHOOK')
  ```

### Rate Limiting
- **Always** add 1.2s delay between Discord posts
- **Monitor** for 429 responses
- **Implement** exponential backoff if needed

### History Management
- **Never delete** `sent_urls.txt` in production
- **Only clear** for testing purposes
- **Backup** before clearing: `copy sent_urls.txt sent_urls.txt.bak`

### Error Handling
- **Always exit 0** even when no new articles
- **Log all errors** to `logs/` directory
- **Notify user** clearly when workflow stops

---

## 🔄 Version History

| Version | Date | Changes |
|---------|------|---------|
| **v1.1** | 2026-03-19 | **No-new-news fix:** Skip Phases 2-4 when no new articles, console notification only (no Discord post), PROD/TEST mode via env var |
| **v1.1** | 2026-03-18 | Production deploy, migration docs, troubleshooting guide, expert reasoning populated |
| **v1.0** | 2026-03-18 | Initial orchestration, all 4 phases working, webhooks fixed, URLs valid |

---

## 📞 Quick Reference

**Skill Location:** `C:\Users\Legion 5i Pro\.browseros\skills\polymarket-brain\`

**Run Command:**
```cmd
cd C:\Users\Legion 5i Pro\.browseros\skills\polymarket-brain
python polymarket_brain_orchestrator.py
```

**Webhooks:**
- Phase 1 (News): `1482043765471445333`
- Phase 4 (Analysis): `1483478506070474922`

**History File:** `..\cnbc-geopolitics-fetcher\references\sent_urls.txt`

**Test Mode:** Clear history file before run

---

## 🎓 Learning Path for New Environments

1. **Read this SKILL.md** completely (you're here now ✅)
2. **Read README.md** for quick start
3. **Copy skills folder** to new environment
4. **Configure webhooks** in both config files
5. **Install dependencies:** `pip install requests crawl4ai`
6. **Test run** with history cleared
7. **Verify Discord** receives all messages
8. **Deploy to production** (stop clearing history)

**Time Estimate:** 15-30 minutes for full setup

---

## 💾 Backup & Restore

### Backup Command
```cmd
xcopy /E /I "C:\Users\Legion 5i Pro\.browseros\skills\polymarket-brain" "D:\backup\polymarket-brain"
xcopy /E /I "C:\Users\Legion 5i Pro\.browseros\skills\cnbc-geopolitics-fetcher" "D:\backup\cnbc-geopolitics-fetcher"
```

### Restore Command
```cmd
xcopy /E /I "D:\backup\polymarket-brain" "C:\Users\Legion 5i Pro\.browseros\skills\polymarket-brain"
xcopy /E /I "D:\backup\cnbc-geopolitics-fetcher" "C:\Users\Legion 5i Pro\.browseros\skills\cnbc-geopolitics-fetcher"
```

---

## 🎯 Success Criteria

✅ Phase 1: 5 articles fetched, posted to Discord
✅ Phase 2: Expert analyses generated (geopolitics/fed)
✅ Phase 3: Markets matched with recommendations
✅ Phase 4: All messages sent to Discord (no 403/400 errors)
✅ URLs: All Polymarket links valid (no 404)
✅ Reasoning: Actual expert analysis (no placeholders)
✅ Rate Limiting: No 429 errors (1.2s delays working)

**If all ✅, deployment successful.**
