---
name: pl-scores
description: Get live Premier League football scores, goal scorers, bookings, and broadcast channels via ESPN API. Use when user asks about Premier League match scores, results, who scored, bookings, or TV channels. Only covers PL (English top flight).
---

# Premier League Scores

Fetches live and recent Premier League match data from ESPN's API — includes scores, goal scorers with minutes, yellow/red cards, and broadcast TV channel.

## What It Shows

- Match scores (live and full-time)
- Goal scorers with exact minute timestamps
- Penalty and own-goal markers
- Yellow and red card bookings
- Broadcast TV channel (US coverage)
- Recent match results

## Usage

### Get all current matchday scores

Run the script directly:
```bash
python3 skills/pl-scores/pl_scores.py
```

### Example Output

```
Premier League — 3 match(es)

Newcastle 1 - 2 Sunderland
  [FT]  📺 USA Net
  ⚽ 10' — A. Gordon (Newcastle)
  ⚽ 57' — C. Talbi (Sunderland)
  ⚽ 90' — B. Brobbey (Sunderland)
  🟨 44' — T. Hume (Sunderland)
  ...

Spurs 0 - 3 Nottm Forest
  [FT]  📺 USA Net
  ⚽ 45' — Igor Jesus (Nottm Forest)
  ⚽ 62' — M. Gibbs-White (Nottm Forest)
  ⚽ 87' — T. Awoniyi (Nottm Forest)
```

## Requirements

- Python 3 (standard library only — no extra packages)
- Internet connection (fetches from ESPN API)

## Data Source

ESPN API: `https://site.api.espn.com/apis/site/v2/sports/soccer/eng.1/scoreboard`

## Limitations

- Broadcast channel reflects US coverage (NBCSN, USA Net, etc.), not UK
- Only covers Premier League (English top flight)
- Data refresh rate depends on ESPN's update frequency
- No half-time scores or detailed match stats beyond scorers and bookings

## Future Additions

Could extend to:
- Championship / lower leagues
- Expected goals (xG)
- Lineups when available
- Head-to-head records
- Upcoming fixtures
