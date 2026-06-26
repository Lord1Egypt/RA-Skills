# Polymarket-Brain v1.1 - Production Deployment

## 🚀 Quick Start (30 Seconds)

```cmd
cd C:\Users\Legion 5i Pro\.browseros\skills\polymarket-brain
python polymarket_brain_orchestrator.py
```

**That's it.** The workflow runs end-to-end automatically.

---

## 📋 What This Skill Does

**Automated geopolitical → macroeconomic → Polymarket trading analysis:**

1. **Fetches CNBC news** (5 articles from World Politics)
2. **Classifies & routes** to expert analysts (geopolitics-expert / the-fed-agent)
3. **Matches to Polymarket markets** (8 monitored markets)
4. **Posts analysis to Discord** (header + markets + summary)

**Output:** Actionable trading recommendations with expert probability vs market odds.

---

## 🏗️ Architecture (4 Phases)

```
┌─────────────────────────────────────────────────────────────┐
│ PHASE 1: CNBC News Fetch                                    │
│ • Fetches 5 articles from CNBC World Politics               │
│ • Deduplicates against sent_urls.txt history                │
│ • Posts new articles to Discord (webhook 1482043765471445333)│
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ PHASE 2: Expert Analysis                                    │
│ • Classifies: geopolitics / macro / mixed                   │
│ • Routes: geopolitics-expert OR the-fed-agent               │
│ • Generates probability assessments                         │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ PHASE 3: Market Matching                                    │
│ • Matches analyses to 8 Polymarket markets                  │
│ • Calculates expert probability vs market odds              │
│ • Generates recommendations (Strong Yes/No, Lean, Fair)     │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ PHASE 4: Discord Dispatch                                   │
│ • Sends header message                                      │
│ • Sends each market analysis (one-by-one, 1.2s delay)       │
│ • Sends summary message                                     │
│ • Webhook: 1483478506070474922                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 Installation (Fresh Environment)

### Prerequisites
- Python 3.9+
- Discord webhooks (2 channels)
- Access to CNBC World Politics RSS

### Step 1: Clone Skills
```bash
# Copy entire skills folder to new environment
xcopy /E /I "C:\Users\Legion 5i Pro\.browseros\skills" "D:\new-env\skills"
```

### Step 2: Verify Dependencies
```bash
# Check required Python packages
pip list | findstr "requests crawl4ai"
```

### Step 3: Configure Webhooks
Edit `cnbc-geopolitics-fetcher/references/config.md`:
```
DISCORD_WEBHOOK=https://discord.com/api/webhooks/1482043765471445333/YOUR_KEY_HERE
```

Edit `polymarket-brain/polymarket_brain_orchestrator.py`:
```python
PHASE1_DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1482043765471445333/YOUR_KEY"
PHASE4_DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1483478506070474922/YOUR_KEY"
```

### Step 4: Test Run
```bash
cd polymarket-brain
python polymarket_brain_orchestrator.py
```

---

## 🔧 Configuration Files

| File | Purpose | Edit? |
|------|---------|-------|
| `polymarket_brain_orchestrator.py` | Main workflow script | ✅ Webhooks |
| `cnbc-geopolitics-fetcher/references/config.md` | CNBC webhook | ✅ Webhook |
| `cnbc-geopolitics-fetcher/references/sent_urls.txt` | URL history | ⚠️ Clear for test |
| `polymarket-brain/output/` | Analysis outputs | 📁 Auto-created |

---

## 🧪 Testing

### Run Modes

**Production Mode (preserves history):**
```cmd
set POLYMARKET_BRAIN_MODE=PROD
cd C:\Users\Legion~1\.browseros\skills\polymarket-brain
python polymarket_brain_orchestrator.py
```

**Test Mode (clears history for fresh posts):**
```cmd
set POLYMARKET_BRAIN_MODE=TEST
cd C:\Users\Legion~1\.browseros\skills\polymarket-brain
python polymarket_brain_orchestrator.py
```

### Expected Output (PROD with new articles)
- ✅ Phase 1: New articles posted to Discord
- ✅ Phase 2: Expert analyses prepared
- ✅ Phase 3: Markets matched
- ✅ Phase 4: Analysis sent to Discord

### Expected Output (PROD with no new articles)
- ✅ Phase 1: No new articles (all in history)
- ⚠️ Phases 2-4: **Skipped** (no analysis runs)
- 📝 Console notification printed (NOT sent to Discord)
- ✅ Clean exit

---

## 📊 Monitored Markets (8 Total)

| # | Market | Resolution | Expert Prob |
|---|--------|------------|-------------|
| 1 | Will Iranian regime fall by June 30? | Jun 30, 2026 | 15% |
| 2 | US-Iran ceasefire by Dec 31 | Dec 31, 2026 | 55% |
| 3 | Iran conflict ends by Dec 31 | Dec 31, 2026 | 60% |
| 4 | US forces enter Iran by Dec 31 | Dec 31, 2026 | 35% |
| 5 | Iran leadership change by Dec 31 | Dec 31, 2026 | 85% |
| 6 | Fed decision in March | Mar 2026 | 95% |
| 7 | Oil hits $100+ by end of March | Mar 2026 | 90% |
| 8 | US recession by end of 2026 | End 2026 | 40% |

---

## 💡 Recommendation Logic

| Signal | Condition | Action |
|--------|-----------|--------|
| **Strong Yes** | Expert > Market by 20%+ | Buy YES |
| **Lean Yes** | Expert > Market by 10-20% | Consider YES |
| **Fair Value** | <10% gap | Hold |
| **Lean No** | Expert < Market by 10-20% | Consider NO |
| **Strong No** | Expert < Market by 20%+ | Buy NO |

---

## 🚨 Common Issues & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| **403 Forbidden** | Missing User-Agent header | Added to urllib requests |
| **400 Bad Request** | Message > 2000 chars | Shortened separator to 40 chars |
| **Rate limiting** | Rapid posts | Added 1.2s delay between messages |
| **No articles posted** | All URLs in history | Clear `sent_urls.txt` for test |
| **Invalid Polymarket URL** | Double underscores (`__`) | Fixed to single hyphens |
| **Placeholder reasoning** | Hardcoded text | Now uses actual expert analysis |

---

## 📁 File Structure

```
polymarket-brain/
├── polymarket_brain_orchestrator.py    # Main script
├── SKILL.md                            # Detailed documentation
├── README.md                           # This file
├── VERSION                             # v1.1
├── output/                             # Analysis outputs (auto-created)
└── logs/                               # Execution logs (auto-created)

cnbc-geopolitics-fetcher/
├── scripts/
│   └── fetch_cnbc_geopolitics.py       # News fetcher
├── references/
│   ├── config.md                       # Webhook config
│   └── sent_urls.txt                   # URL history
└── SKILL.md                            # Documentation
```

---

## 🔄 Version History

| Version | Date | Changes |
|---------|------|---------|
| **v1.1** | 2026-03-18 | Production deploy, migration docs, troubleshooting |
| **v1.0** | 2026-03-18 | Initial orchestration, all 4 phases working |

---

## 📞 Support

**Skill Location:** `C:\Users\Legion 5i Pro\.browseros\skills\polymarket-brain\`

**Run Command:**
```cmd
cd C:\Users\Legion 5i Pro\.browseros\skills\polymarket-brain
python polymarket_brain_orchestrator.py
```

**Discord Webhooks:**
- Phase 1 (News): `1482043765471445333`
- Phase 4 (Analysis): `1483478506070474922`
