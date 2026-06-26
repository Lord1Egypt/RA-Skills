---
name: hk-horse-racing
description: Fetches Hong Kong Jockey Club race cards with horse details, odds, and recommended picks per race. Supports date selection, class filtering, exclusions, single-race fetch, advanced scoring, and enhanced form analysis.
---
# HK Horse Racing Skill

This skill provides two core functions:
- **Race card data** - Fetches Hong Kong Jockey Club race cards for a given date, including meeting details, race conditions, and complete horse data (jockey, trainer, barrier, weight, past runs, gear, win/place odds).
- **Recommended picks** - Analyzes the field and returns up to 4 recommended horses per race with reasoning (win odds, barrier, weight, recent form, gear), plus an estimated win probability.

English output only. Additional features: exclude by horse number or barrier, single-race fetch (`raceNo`), 15‑minute caching, and 60‑second rate limiting between fresh API fetches. Advanced scoring includes trainer/jockey bonuses, barrier effectiveness, and weight penalty.

**Repository:** https://github.com/StevenHo1394/openclaw/tree/main/skills/hk-horse-racing

## Tools

### `fetchRaceCard(params)`

Fetch race card for a given date (default: today in HKT). Includes race details, per-horse win/place odds, and recommendations for each race.

**Parameters (object):**
- `date` (string, optional): Date in `YYYY-MM-DD` format. Default: today (HKT).
- `classFilter` (array of strings, optional): Filter races by class (e.g., `["Class 4"]`).
- `excludeHorseNos` (array of numbers, optional): List of horse numbers to exclude from the `horses` array and from recommendations (e.g., `[7]`).
- `excludeBarriers` (array of numbers, optional): List of barrier numbers to exclude from the `horses` array and from recommendations (e.g., `[7]`).
- `raceNo` (number, optional): If provided, returns only this specific race. Omit to get all races for the date.
- `advancedScoring` (boolean, optional): Enable advanced scoring that includes trainer/jockey bonuses, barrier effectiveness, weight penalty, and light weight bonus. Default: `false`.
- `tjBonusWeight` (number, optional): Weight for trainer/jockey combo bonus when `advancedScoring=true`. Range 0-0.3. Default: `0.15`.
- `barrierBonusWeight` (number, optional): Weight for barrier effectiveness bonus when `advancedScoring=true`. Range 0-0.2. Default: `0.12`.
- `newsBoost` (boolean, optional): When `advancedScoring=true`, also include news sentiment boost (stub, not implemented). Default: `false`.
- `lightWeightBonus` (number, optional): Bonus for horses with weight < 120lb when `advancedScoring=true`. Range 0-0.2. Default: `0.05`.
- `formAnalysis` (boolean, optional): Enable enhanced form analysis — recency-weighted form, trend detection (improving/declining), consistency scoring, last-start win bonus, consistency bonus, improving form bonus, declining form penalty, and debutant handling. Default: true.

**Returns (object):**
```json
{
  "meeting": {
    "venue": "Happy Valley",
    "date": "2026-03-18",
    "weather": null,
    "trackCondition": "GOOD"
  },
  "races": [
    {
      "raceNo": 2,
      "distance": 1650,
      "class": "Class 4",
      "going": "GOOD",
      "horses": [
        {
          "horseNo": 1,
          "horseName": "MIGHTY STEED",
          "horseId": "HK_2023_J384",
          "weight": 135,
          "jockey": "Z Purton",
          "jockeyAllowance": null,
          "trainer": "K W Lui",
          "pastRuns": [7,7,3,3,7,1],
          "gear": ["CP"],
          "winOdds": 3.2,
          "placeOdds": 1.5
        }
        // ... other runners (SB horses excluded)
      ],
      "recommendations": [
        {
          "horseName": "MIGHTY STEED",
          "reason": "Win odds 3.2; barrier 7; weight 135; recent form avg 4.7; gear: CP; TJ bonus +10.0%; Barrier +2.0%",
          "winProbability": 17.2
        }
        // ... up to 4 best horses
      ]
    }
    // ...
  ],
  "source": "hkjc-api",
  "timestamp": "2026-03-17T17:58:31.793Z"
}
```

**Note:** The returned JSON object structure remains the same as previous versions; enabling `formAnalysis` only affects the internal scoring and the resulting `winProbability` values in the recommendations.


**Notes:**
- Stand-by (SB) horses are excluded from the `horses` list.
- `recommendations` are derived from win odds and recent form; only horses with both are considered.
- Probabilities are normalized implied probabilities from market odds, adjusted by form.
- When `advancedScoring=true`, additional bonuses may be applied: top jockey + top trainer combo (+tjBonusWeight), barrier effectiveness (+/- depending on distance class), and weight penalty for horses carrying significantly above average weight.
- **Chinese names**: Chinese horse/trainer/jockey names (name_ch fields) may be present in the source data but are not guaranteed to exist. The skill returns English names by default; if an English name is missing, the field shows `(no English name)`. Chinese names are not used in output.

## Prerequisites

- Node.js environment (Node 18+ recommended)
- Internet access to reach HKJC API (no authentication required)
- The skill depends on `hkjc-api` npm package, which will be installed automatically.

## Installation

1. Ensure the skill directory exists: `/home/node/.openclaw/workspace/skills/hk-horse-racing/`
2. Run `npm install` inside that directory to install dependencies. OpenClaw will typically run `npm install` automatically when the skill is loaded if you set `installCommand` in the plugin manifest.
3. Add the skill to the desired agent's allowed skills via `openclaw configure` or agent config.

## Rate Limiting

To avoid overloading the HKJC source, the skill enforces a **1-minute cooldown** between fresh API fetches. Cached data (within 15 minutes) is served without delay. If you attempt a fresh fetch sooner than 60 seconds after the previous one, the skill throws an error: `Rate limit: please wait Xs before fetching new data.`

## Notes

- The HKJC API is unofficial and may have rate limits or downtime.
- Place odds provided by the skill may be estimates rather than actual dividends, especially when the live API doesn't publish plaOdds values. For reliable place betting, verify against actual results when possible, and consider using win odds combined with form analysis as a more reliable alternative when place odds are unavailable.
- For fetching official race results (including final positions and dividends), see the `scripts/get_hk_race_results.js` script which uses the hkjc-api package directly.
- Odds are fetched separately per race (WIN and PLA by default). Additional odds types can be added by modifying the skill.
- If the API does not return past performance data, that field will be empty.
- The skill caches results for 15 minutes to reduce load.
- `advancedScoring` features are experimental and use heuristics; tune `tjBonusWeight`, `barrierBonusWeight`, and `lightWeightBonus` as needed. Weight penalty and light weight bonus apply automatically when `advancedScoring=true`.

## Troubleshooting

If the skill fails to install or run:
- Check Node.js version (`node --version`).
- Ensure `npm install` completed without errors (look for `hkjc-api` in `node_modules`).
- Verify outbound network connectivity.
- Check agent logs for errors.

## Version History

### v1.2.2
- Enabled formAnalysis by default for improved horse selection accuracy
- Fixed barrierBonusWeight inconsistency (standardized to 0.12)
- Reduced A. Basel jockey penalty from -0.03 to -0.018 based on validation
- Enhanced barrier 1 at 1200m effectiveness (+1.8% boost) based on live usage validation

### v1.2.1
- Updated documentation with lessons learned from live usage (public-friendly format)
- Added validated model rules, QP betting refinements, barrier insights

### v1.2.0
- Added weight penalty in advanced scoring: horses carrying >2 lb above average weight incur a small score penalty.
- Added class‑drop bonus stub (requires historical class data to activate).
- Refined advanced scoring defaults: `tjBonusWeight` 0.15, `barrierBonusWeight` 0.12.
- Added `lightWeightBonus` (default 0.05) to reward horses under 120 lb in advanced scoring.
- Expanded top jockey and trainer sets.
- Clarified Chinese name handling and removed agent‑specific examples.
- Added disclaimer about betting risk.

### v1.1.0
- Added advanced scoring: trainer/jockey top‑pair bonus, barrier effectiveness by distance, news sentiment placeholder.
- New parameters: `advancedScoring`, `tjBonusWeight`, `barrierBonusWeight`, `newsBoost`.
- Changed license from ISC to MIT.
- Removed agent‑specific examples (e.g., Jonah).
- Clarified Chinese name handling: may exist but not guaranteed; English‑only output.

### v1.0.0
- Initial stable release with race card fetch, top 4 recommendations, strict English output, exclusions, single‑race fetch, rate limiting, and caching.

## Disclaimer

This skill is provided for informational purposes only. It does not constitute financial or betting advice. The author makes no guarantees regarding the accuracy, completeness, or timeliness of the data and recommendations. You are solely responsible for any betting decisions and any resulting losses. Use this skill at your own risk.

---

**Author:** Steven Ho
**License:** MIT