# Polymarket-Brain Pre-Test Checklist

## ✅ Verified Components

### 1. Webhook Configuration
- **Phase 1 (CNBC News):** `1482043765471445333` ✓
- **Phase 4 (Analysis):** `1483478506070474922` ✓

### 2. Code Fixes Applied
- ✓ User-Agent header added (fixes 403 errors)
- ✓ Message length < 2000 chars (fixes 400 errors)
- ✓ 1.2s delay between Discord posts (prevents rate limiting)
- ✓ `time` module imported in CNBC fetcher
- ✓ Separate webhooks for Phase 1 and Phase 4

### 3. Test Results
- ✓ Both webhooks return 204 (success)
- ✓ Phase 1: 5 articles posted successfully
- ✓ Phase 4: Header + 5 markets sent successfully
- ✓ No 403/400 errors in latest run

## ⚠️ Potential Issues to Watch

### 1. History File Behavior
- **Current:** `sent_urls.txt` prevents duplicate posts
- **Test Mode:** Clears history before running
- **Production:** Keeps history (expected behavior)

### 2. Expert Analysis
- **Status:** Analysis inputs saved to `output/` folder
- **Note:** Actual expert analysis requires manual trigger or integration
- **Current:** Uses mock analysis data for market matching

### 3. Polymarket Market Data
- **Status:** Hardcoded market data in orchestrator
- **Limitation:** Not fetching live odds from Polymarket API
- **Workaround:** Manual updates needed for current odds

## 📋 Recommended Test Flow

1. **Clear history** (for fresh test):
   ```
   type nul > ..\cnbc-geopolitics-fetcher\references\sent_urls.txt
   ```

2. **Run orchestrator**:
   ```
   python polymarket_brain_orchestrator.py
   ```

3. **Check Discord**:
   - Phase 1 channel: 5 CNBC articles
   - Phase 4 channel: Header + market analysis

## 🔧 Files Modified

1. `polymarket_brain_orchestrator.py` - Webhook separation + delays + User-Agent
2. `send_discord.py` - JSON key fix + delays
3. `cnbc-geopolitics-fetcher/scripts/fetch_cnbc_geopolitics.py` - time import + delay
4. `cnbc-geopolitics-fetcher/config/webhook_config.json` - Phase 1 webhook URL

---

**Ready for production testing.**
