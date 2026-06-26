# Stock Watcher Pro — First-Run Setup

Welcome to Stock Watcher Pro! This guide walks your agent through the complete setup. Run these steps once, and you're good to go.

---

## Step 1: Create Directory Structure

```bash
# Create all required directories
mkdir -p data/briefings data/filings data/sources data/thesis-log
mkdir -p config scripts examples dashboard-kit

# Lock down sensitive directories
chmod 700 data data/briefings data/filings data/sources data/thesis-log
```

## Step 2: Copy Configuration Files

Copy the default configuration from the skill package to your workspace `config/` directory so scripts and the agent can find them:

```bash
# Find the skill package directory
# Verification: skill files installed by clawhub install
if [ -n "$SKILL_DIR" ] && [ -f "$SKILL_DIR/config/watchlist-config.json" ]; then
  cp "$SKILL_DIR/config/watchlist-config.json" config/watchlist-config.json
  cp "$SKILL_DIR/config/source-categories.md" config/source-categories.md
  chmod 600 config/watchlist-config.json
  echo "✅ Config files copied to config/"
else
  echo "⚠️ Could not find skill config files. Manually copy config/watchlist-config.json from the stock-watcher-pro skill package to your workspace config/ directory."
fi
```

If you want to customize the briefing schedule, alert thresholds, or timezone, edit `config/watchlist-config.json` now. The defaults work for US Eastern time zone users.

## Step 3: Initialize Data Files

Create empty data files with the correct schema:

```bash
# Portfolio (empty — you'll add holdings next)
cat > data/portfolio.json << 'EOF'
{
  "portfolio_name": "My Portfolio",
  "base_currency": "USD",
  "created_at": "",
  "holdings": []
}
EOF

# Watchlist (empty)
cat > data/watchlist.json << 'EOF'
{
  "watchlist": []
}
EOF

# Lock down financial data
chmod 600 data/portfolio.json data/watchlist.json
```

## Step 4: Copy Automation Scripts

```bash
# Copy scripts from skill package to workspace scripts/
# Verification: skill files installed by clawhub install
if [ -n "$SKILL_DIR" ] && [ -d "$SKILL_DIR/scripts" ]; then
  cp "$SKILL_DIR/scripts/stock-watcher-scheduler.sh" scripts/stock-watcher-scheduler.sh
  cp "$SKILL_DIR/scripts/edgar-check.sh" scripts/edgar-check.sh
  chmod 700 scripts/stock-watcher-scheduler.sh scripts/edgar-check.sh
  echo "✅ Scripts copied and made executable"
else
  echo "⚠️ Could not find skill scripts. Manually copy from the stock-watcher-pro/scripts/ directory to your workspace scripts/ directory."
fi
```

## Step 5: Add Your First Holdings

Now tell your agent what you're tracking. Examples:

- "Add AAPL — I own 50 shares at $178.50. My thesis: spatial computing will become a core revenue driver."
- "Add TSLA to my watchlist — waiting for a pullback to $180."
- "Add MSFT — 100 shares at $410. Thesis: enterprise AI adoption will accelerate cloud revenue growth."

The agent will:
1. Save your holdings to `data/portfolio.json`
2. Automatically run source discovery for each ticker
3. Build a custom source network in `data/sources/[TICKER].json`
4. Start monitoring SEC EDGAR for recent filings

## Step 6: Configure Briefing Schedule (Optional)

The default schedule is:
- **Pre-Market:** 6:00 AM local time (weekdays)
- **Mid-Day:** 12:30 PM ET (weekdays)
- **Post-Market:** 4:30 PM ET (weekdays)

To change this, edit `config/watchlist-config.json` and update the `briefing_schedule` section.

If your agent supports scheduled tasks (heartbeats, cron, or Trigger.dev), run:
```bash
bash scripts/stock-watcher-scheduler.sh setup
```

Otherwise, just ask your agent for briefings on demand: "Give me my pre-market briefing."

## Step 7: Verify Setup

Ask your agent:

> "Show me my portfolio setup and confirm everything is working."

The agent should:
- ✅ List your holdings from `data/portfolio.json`
- ✅ Show discovered sources for each ticker
- ✅ Confirm EDGAR monitoring is active (CIK numbers found)
- ✅ Display your briefing schedule
- ✅ Report any issues (missing configs, tickers not found, etc.)

---

## You're Done! 🎉

Your first pre-market briefing will arrive on the next trading day. In the meantime, try:

- "What's happening with AAPL right now?"
- "Check for any new SEC filings"
- "How's my thesis holding up?"
- "Give me a practice briefing for today"

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| "Config file not found" | Re-run Step 2 — make sure files are in `config/` |
| "No EDGAR results for [TICKER]" | The company may not file with the SEC (foreign, OTC). News monitoring still works. |
| "Briefings not arriving" | Check that your scheduling is set up (Step 6) or request them manually. |
| "Permission denied" | Re-run the `chmod` commands from Steps 1 and 3. |

⚠️ **Reminder:** Stock Watcher Pro provides information only. It is not financial advice. Always do your own research and consult a qualified financial advisor before making investment decisions.
