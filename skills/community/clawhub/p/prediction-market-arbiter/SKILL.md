---
name: Prediction Market Arbiter
description: "Cross-platform divergence scanner comparing Kalshi and Polymarket prices on identical events. Fuzzy title matching across 1000+ markets per run, configurable thresholds for volume, divergence percentage, and match quality. Detects arbitrage opportunities and market mispricings automatically. Zero cost — both APIs are free. Part of the OpenClaw Prediction Market Trading Stack — divergences feed into Market Morning Brief and pair with Kalshi Command Center for execution."
---

# Prediction Market Arbiter — Cross-Platform Divergence Scanner

## Overview

Prediction Market Arbiter is a systematic price comparison engine for prediction markets. It scans Kalshi and Polymarket simultaneously, identifies identical or near-identical events priced differently across platforms, and alerts you to potential arbitrage opportunities or market mispricings.

## What It Does

**Core Function:** Compare YES prices for the same event across Kalshi and Polymarket. When the same market exists on both platforms but with significant price divergences, alert the trader to potential inefficiency.

**Example:**
- Market: "Will Bitcoin exceed $100k by Dec 2026?"
- Kalshi price: 72¢ (72% implied probability)
- Polymarket price: 58¢ (58% implied probability)
- Divergence: 14 percentage points = **arbitrage signal**

The arbiter detects these inefficiencies automatically, filters by volume and match quality, and ranks them by spread size.

## Key Features

- **Fuzzy Title Matching** — Uses Jaccard similarity (word overlap) to identify the same event across different platform vocabularies
- **Configurable Divergence Threshold** — Default 8%; tune for your risk tolerance
- **Volume Filtering** — Combines Kalshi + Polymarket volume; minimum 1000 default
- **Match Confidence** — Only pairs markets with >60% title similarity (configurable)
- **Pagination** — Fetches top 1000 Kalshi markets (5 pages × 200) + top 200 Polymarket (by volume)
- **Cache Results** — Saves matches to JSON for programmatic access and follow-up analysis
- **Multi-Platform Support** — Uses Kalshi API (with client authentication) and Polymarket Gamma API (no auth required)

## When to Use This Skill

- You trade across Kalshi and Polymarket and want to find price inefficiencies automatically
- You're arbitraging prediction markets and need real-time divergence alerts
- You want to understand market structure: which platform leads on certain event types?
- You're analyzing prediction market microstructure and efficiency
- You need a scheduled divergence scanner (every 4 hours, daily, etc.)

## Requirements

### API Keys & Credentials

1. **Kalshi API Key** (free, required)
   - Sign up at https://kalshi.com
   - Navigate to Settings → API
   - Generate API credentials (key ID + private key file)
   - Cost: Free tier, unlimited reads

2. **Polymarket Access** (free, no authentication)
   - Gamma API is public: https://gamma-api.polymarket.com
   - No API key required
   - No cost

### Python & Dependencies

- Python 3.10 or higher
- Required packages:
  ```bash
  pip install kalshi-python requests pyyaml
  ```

## Configuration

Create or update your `config.yaml`:

```yaml
kalshi:
  enabled: true
  api_key_id: "your-key-id-here"
  private_key_file: "path/to/private.key"

prediction_market_arbiter:
  enabled: true
  check_interval_minutes: 240          # 4 hours (default)
  divergence_threshold_pct: 8.0        # Minimum % spread to alert
  fuzzy_match_threshold: 0.6           # Jaccard similarity threshold
  min_volume: 1000                     # Minimum combined volume
  kalshi_max_pages: 5                  # Pages to fetch (max 5 × 200 = 1000)
  polymarket_limit: 200                # Top markets by volume
```

### Threshold Tuning Guide

| Parameter | Default | When to Adjust |
|-----------|---------|-----------------|
| `divergence_threshold_pct` | 8.0% | Lower (5%) for more alerts; higher (15%) for only major spreads |
| `fuzzy_match_threshold` | 0.6 | Raise to 0.7+ to be stricter (fewer false matches); lower to 0.5 for loose matching |
| `min_volume` | 1000 | Lower for illiquid opportunities; raise to 5000+ for only liquid pairs |

## How It Works

### Phase 1: Fetch Markets

**Kalshi:** Paginate through active markets (status=open), fetching up to 5 pages of 200 markets each (max 1000 markets).
- Extract: title, ticker, yes_price (cents), volume, open interest

**Polymarket:** Fetch top 200 markets sorted by volume from Gamma API.
- Extract: question text (title), yes_price (in cents), volume

### Phase 2: Fuzzy Title Matching

For each Kalshi market, compare against all Polymarket markets using **Jaccard similarity**:

```
a_words = set(kalshi_title.lower().split())
b_words = set(polymarket_title.lower().split())

# Remove common stopwords (the, a, will, in, on, etc.)
a_words -= stopwords
b_words -= stopwords

similarity = len(a_words ∩ b_words) / len(a_words ∪ b_words)
```

Only pairs with similarity >= threshold advance to comparison.

**Example — Successful Match:**
```
Kalshi:     "Will the Federal Reserve cut rates before June 2026?"
Polymarket: "Will the Fed cut interest rates by June 2026?"

After stopword removal:
a_words = {federal, reserve, cut, rates, june, 2026}
b_words = {fed, cut, interest, rates, june, 2026}

Intersection: {cut, rates, june, 2026}
Union: {federal, reserve, fed, interest, cut, rates, june, 2026}
Similarity: 4/8 = 0.50
```

**Example — No Match (Different Events):**
```
Kalshi:     "Will Bitcoin exceed $100,000 by December 2026?"
Polymarket: "Will Ethereum hit $10,000 by end of 2026?"

After stopword removal:
a_words = {bitcoin, exceed, 100000, december, 2026}
b_words = {ethereum, hit, 10000, end, 2026}

Intersection: {2026}
Union: {bitcoin, exceed, 100000, december, ethereum, hit, 10000, end, 2026}
Similarity: 1/9 = 0.11 (NO MATCH — correctly rejected)
```

**Tuning note:** Markets with similar topics but different vocabulary (e.g., "Bitcoin" vs "BTC") may not match at default thresholds. Lower `fuzzy_match_threshold` to 0.4-0.5 for broader matching, or use the aggressive config profile.

### Phase 3: Filter by Volume

Combined volume = Kalshi volume + Polymarket volume
- If combined volume < min_volume threshold, drop the pair
- Filters out low-liquidity pairs where arbitrage isn't actionable

### Phase 4: Calculate Divergence

For each matched pair:

```
delta = |kalshi_price - polymarket_price|  (in cents)
midpoint = (kalshi_price + polymarket_price) / 2
delta_pct = (delta / midpoint) × 100
```

If delta_pct >= threshold, add to alerts.

### Phase 5: Sort & Alert

Sort divergences by largest spread first. Return top N (default 5 in alerts).

Example output:
```
📊 Cross-platform divergences (>=8%):
  Bitcoin exceeds $100,000 by EOY 2026?
    Kalshi 72¢ vs PM 58¢ (↓14%)
  Will Trump win 2028?
    Kalshi 68¢ vs PM 61¢ (↑7%) [No match - below threshold]
```

### Cache Results

Write all matches (top 20) to JSON:

```json
{
  "matches": [
    {
      "kalshi_title": "Will Bitcoin exceed $100,000 by Dec 2026?",
      "pm_title": "Bitcoin above 100k by EOY 2026?",
      "kalshi_price": 72,
      "pm_price": 58,
      "delta": 14,
      "delta_pct": 19.4,
      "match_score": 0.82
    }
  ],
  "kalshi_count": 847,
  "pm_count": 198,
  "timestamp": 1709856000.123
}
```

## Divergence Interpretation

### Common Divergence Patterns

**1. Polymarket Leads on Hype Events**
- Recent news → PM moves first (higher volume of retail traders)
- Look for Kalshi underpriced relative to PM on breaking news

**2. Kalshi Leads on Structural Events**
- Predictable political cycles, economic data → Kalshi often ahead
- PM sometimes lags

**3. Liquidity-Driven Spreads**
- If one platform is much more liquid, it's often the "fair price"
- Illiquid platform = potential mispricing

**4. Time-of-Day Effects**
- US markets hours: Kalshi often tighter
- Asian hours: PM may be the pricing engine

## Scheduling

### Command-Line Usage

```bash
# Single run (no persistence)
python arbiter.py

# With custom config
python arbiter.py --config /path/to/config.yaml

# Dry run (display matches, don't send alerts)
python arbiter.py --dry-run

# Force run even if interval hasn't elapsed
python arbiter.py --force
```

### As a Cron Job (Every 4 Hours)

```bash
# Add to crontab -e:
0 */4 * * * cd /path/to/prediction-market-arbiter && python scripts/arbiter.py >> /tmp/arbiter.log 2>&1
```

### As an OpenClaw Scheduled Task

```yaml
skills:
  prediction-market-arbiter:
    enabled: true
    schedule: "0 */4 * * *"  # Every 4 hours
    timeout_seconds: 120
```

## Example Output

### Alert Message

```
📊 Cross-platform divergences (>=8%):
  Will Bitcoin exceed $100,000 by Dec 2026?
    Kalshi 72¢ vs PM 58¢ (↓14%)

  Will a Democrat win the 2028 presidential election?
    Kalshi 48¢ vs PM 55¢ (↑7%) [No match - below threshold]

  Will the Federal Reserve cut rates before June 2026?
    Kalshi 38¢ vs PM 45¢ (↑7%) [No match - below threshold]

Found 3 divergences across 847 Kalshi + 198 Polymarket markets.
```

### Cache Output

File: `state/cross_platform_cache.json`

```json
{
  "matches": [
    {
      "kalshi_title": "Will Bitcoin exceed $100,000 by December 2026?",
      "pm_title": "Bitcoin above 100k by EOY 2026?",
      "kalshi_price": 72,
      "pm_price": 58,
      "delta": 14,
      "delta_pct": 19.4,
      "match_score": 0.82
    },
    {
      "kalshi_title": "Will Democrats win the 2028 presidency?",
      "pm_title": "Democratic nominee will win the 2028 U.S. Presidential Election",
      "kalshi_price": 48,
      "pm_price": 55,
      "delta": 7,
      "delta_pct": 14.3,
      "match_score": 0.75
    }
  ],
  "kalshi_count": 847,
  "pm_count": 198,
  "timestamp": 1709856000.123
}
```

## API Reference

### Main Function

```python
from arbiter import check_cross_platform

result = check_cross_platform(
    state={},
    dry_run=False,
    force=False
)

# result = True if matches found, False otherwise
```

### Configuration Object

```python
cfg = {
    "divergence_threshold_pct": 8.0,
    "fuzzy_match_threshold": 0.6,
    "min_volume": 1000,
    "kalshi_max_pages": 5,
    "polymarket_limit": 200,
    "check_interval_minutes": 240,
}
```

## Troubleshooting

### No Matches Found

Possible causes:
1. **Threshold too strict** — Raise divergence_threshold_pct or lower fuzzy_match_threshold
2. **Low market overlap** — Most Kalshi markets don't have Polymarket equivalents
3. **Both platforms down** — Check status pages

### Wrong Matches (False Positives)

If fuzzy matching is pairing unrelated markets:
```yaml
# Increase strictness
fuzzy_match_threshold: 0.75  # Default 0.6
```

### API Failures

**Kalshi API error:**
- Check API key validity: `kalshi_api_key_id` and `private_key_file` path
- Verify key has "read-only" permission (sufficient for this skill)

**Polymarket API error:**
- Polymarket Gamma API is public; if it fails, their servers are down
- Check https://gamma-api.polymarket.com/markets directly in browser

### Performance

Typical run: 30-90 seconds
- Kalshi fetch: 10-30s (paginating 5 pages)
- Polymarket fetch: 5-15s
- Matching: <5s
- If taking >2 minutes, reduce kalshi_max_pages or polymarket_limit

## Performance & Cost

### Typical Run Metrics

- **Runtime:** 30-90 seconds
- **API calls:**
  - Kalshi: 5 calls (page 1-5)
  - Polymarket: 1 call (top 200 by volume)
- **Cost:** $0 (all reads, no premium APIs)

### Scaling

For 6 runs per day (every 4 hours):
- **Kalshi:** 30 API calls/day (free tier handles 1000s)
- **Polymarket:** 6 API calls/day (public API)
- **Total cost:** $0

## OpenClaw Ecosystem Integration

Cross-platform price comparison engine for the Prediction Market Trading Stack.

| Connected Skill | How It Connects |
|----------------|-----------------|
| **Market Morning Brief** | Divergences appear in your daily morning digest |
| **Kalshi Command Center** | Trade the Kalshi side of flagged divergences |
| **Polymarket Command Center** | Browse the Polymarket side for context |
| **Kalshalyst** | Compare contrarian edges against cross-platform pricing |

**Install the complete stack:**
```bash
clawhub install kalshalyst kalshi-command-center polymarket-command-center prediction-market-arbiter xpulse portfolio-drift-monitor market-morning-brief personality-engine
```

## Implementation Notes

Battle-tested in production trading environments. Design principles:

1. **Standalone config/logging** — works with any OpenClaw setup
2. **Direct alerts** — sends divergences straight to you
3. **All thresholds and matching logic** — refined through live cross-platform trading
4. **Standalone scripts** — zero external dependencies beyond listed packages

## Configuration Example

### conservative.yaml (Wide Spreads Only)

```yaml
prediction_market_arbiter:
  divergence_threshold_pct: 15.0
  fuzzy_match_threshold: 0.8
  min_volume: 5000
```

### aggressive.yaml (Early Detection)

```yaml
prediction_market_arbiter:
  divergence_threshold_pct: 5.0
  fuzzy_match_threshold: 0.5
  min_volume: 500
```

## Further Reading

- See `references/fuzzy-matching.md` for detailed explanation of title matching and threshold tuning

## Support & Iteration

Common iteration paths:

1. **Threshold Tuning** — Adjust divergence_threshold_pct and fuzzy_match_threshold based on your alert frequency
2. **Volume Filtering** — Increase min_volume to focus on only liquid pairs
3. **Scheduling** — Change check_interval_minutes (240 = 4 hours, 60 = 1 hour, etc.)
4. **Platform Expansion** — Add new platforms (Manifold Markets, Betfair, etc.) by implementing _fetch_X_markets() functions

## License & Attribution

**Author**: KingMadeLLC


---

## Feedback & Issues

Found a bug? Have a feature request? Want to share results?

- **GitHub Issues**: [github.com/kingmadellc/openclaw-prediction-stack/issues](https://github.com/kingmadellc/openclaw-prediction-stack/issues)
- **X/Twitter**: [@KingMadeLLC](https://x.com/KingMadeLLC)

Part of the **OpenClaw Prediction Stack** — the first prediction market skill suite on ClawHub.
