---
name: polymarket-weather-bucket-thresholds
description: Global temperature bucket threshold strategy via Simmer. Buy YES under 15%, sell full position at 45%, max ~$2 entries, max 5 trades/scan, every 2 minutes.
metadata:
  author: "Brian"
  version: "1.0.0"
  displayName: "Global Temperature Bucket Thresholds (Simmer)"
  difficulty: "intermediate"
---

# Global Temperature Bucket Thresholds (Simmer)

Rules:
- Entry: buy YES when current_probability < 0.15
- Exit: sell entire YES position when current_probability >= 0.45
- Max entry spend: ~$2 (default uses 1.80 to avoid slippage overshoot)
- Max trades per scan: 5
- Schedule: every 2 minutes
- Safeguards: strict — skip any market with context warnings
- Dry-run by default. Use `--live` to place trades.
