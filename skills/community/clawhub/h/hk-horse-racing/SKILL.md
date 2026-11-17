---
name: hk-horse-racing
description: Fetches Hong Kong Jockey Club race cards, available WIN/PLA odds, recommendations, official results, and dividends. Supports date selection, exclusions, single-race fetch, and advanced scoring.
---
# HK Horse Racing Skill

This skill provides three core functions:
- **Race card data** - Reads Hong Kong Jockey Club's public English race-card page for a given date, including meeting details and runner data (jockey, trainer, barrier, weight, past runs, and gear).
- **Recommended picks** - Analyzes the field and returns up to 4 recommended horses per race with reasoning (win odds, barrier, weight, recent form, gear), plus an estimated win probability.
- **Official race results** - Reads official placings, final win odds, and dividends from HKJC's public results page.

English output only. Additional features: exclude by horse number or barrier, single-race fetch (`raceNo`), 15-minute caching, and a 60-second cooldown between fresh requests. Advanced scoring includes trainer/jockey bonuses, barrier effectiveness, and weight penalty.

**Repository:** https://github.com/StevenHo1394/openclaw/tree/main/skills/hk-horse-racing

## Tools

### `fetchRaceCard(params)`

Fetch race card for a given date (default: today in HKT). Reads runner details from the public HKJC race-card page and fetches official WIN/PLA odds when available.

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
  "source": "hkjc-public-racecard-page",
  "oddsSource": "hkjc-api",
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
- Race cards come from HKJC's public server-rendered page at `racing.hkjc.com`; a date with no published card returns an empty `races` array.
- Live WIN/PLA odds are requested from the HKJC odds API first using the ISO race date and meeting venue. If it is unavailable or returns no odds, the skill falls back to odds present in the public race-card page. Race-card pages may omit odds columns; in that case, the odds API can still supply them. Missing odds remain `null`; the skill does not estimate them. `oddsSource` reports `hkjc-api`, `hkjc-public-racecard-page`, or `mixed`.

### `fetchRaceResults(params)`

Fetch official results for a date or the latest available meeting. If `raceNo` is omitted, all races linked from the meeting page are returned.

**Parameters (object):**
- `date` (string, optional): Date in `YYYY-MM-DD` format. Omit to use the latest results available on HKJC's public page.
- `raceNo` (number, optional): Return only the specified race.

The result includes each runner's placing, final win odds, and official dividends by betting pool. These are final results, not live odds.

## Prerequisites

- Node.js environment (Node 18+ recommended)
- Internet access to reach HKJC's public racing pages and (for available live odds) the HKJC GraphQL endpoint.
- The skill uses `hkjc-api` for its accepted WIN/PLA odds query; race-card and results data use public HKJC HTML pages.

## Installation

1. Ensure the skill directory exists: `/home/node/.openclaw/workspace/skills/hk-horse-racing/`
2. Run `npm install` inside that directory to install dependencies. OpenClaw will typically run `npm install` automatically when the skill is loaded if you set `installCommand` in the plugin manifest.
3. Add the skill to the desired agent's allowed skills via `openclaw configure` or agent config.

## Rate Limiting

To avoid overloading the HKJC source, the skill enforces a **1-minute cooldown** between fresh API fetches. Cached data (within 15 minutes) is served without delay. If you attempt a fresh fetch sooner than 60 seconds after the previous one, the skill throws an error: `Rate limit: please wait Xs before fetching new data.`

## Notes

- The package's race-meeting GraphQL query may be rejected by HKJC with `WHITELIST_ERROR`. Live odds are attempted through the API first and then fall back to any odds available on the official public HTML race-card page. The skill does not bypass HKJC access controls.
- HKJC pages and odds may be unavailable or change structure. HTTP failures and unexpected page structure are surfaced as errors.
- The skill does not estimate missing place odds. `placeOdds` is `null` until the live odds source publishes a value; use `fetchRaceResults` for official settled dividends.
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

### v1.2.4
- Send the ISO-formatted race date to the HKJC odds API so odds are requested for the intended meeting instead of potentially receiving stale odds.
- Allow the public race-card parser to handle pages that omit WIN/PLA odds columns, so API odds can still be fetched and merged with runner data.
- Document that missing public-card odds columns are supported and missing odds are not estimated.

### v1.2.3
- Fetch live WIN/PLA odds from the HKJC odds API first, then silently fall back to odds available in the public race-card page if the API is blocked, unavailable, or returns no odds.
- Parse WIN/PLA odds from public race-card runner tables when those values are present, and retain `null` when neither source provides an odds value.
- Report the odds source as `hkjc-api`, `hkjc-public-racecard-page`, or `mixed`.

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