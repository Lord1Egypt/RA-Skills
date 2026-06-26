# Lessons Learned (from $590 deposited → $216 current)

## Catastrophic Mistakes

### 1. Inverted Probabilities ($150+ loss)
Odds API `outcomes[]` order is NOT home/away. Must match by `outcomes[i].name`.
One bug caused 80% loss rate — betting the wrong side of every trade.

### 2. Duplicate Positions ($44 loss)
YES on Player A + NO on Player B in the same match = same position doubled.
Always dedup by base event ticker before trading.

### 3. Full-Port on Coin Flips ($88 at risk)
Djokovic NO × 200 contracts = 86% of bankroll on one position.
Even with edge, concentration kills. Quarter-Kelly max.

### 4. Rogue Automated Trading ($72+ loss)
Scripts/bots placing trades during heartbeat cycles without human oversight.
Now: ALL trading scripts disabled. Only conscious decisions with documented edge.

### 5. Fragment Matching ($28 loss)
3-letter auto-matcher matched Swedish basketball to NBA games.
Never use fragment matching for event identification.

## Market-Specific Insights

### Tennis
- **Qualifying/Challengers** = 5-40% EV gaps (BEST source)
- **Main draw (Indian Wells, etc.)** = within 1-3% of Pinnacle (efficient)
- **Live edges close in 2-3 minutes** — must execute within this window
- **Sofascore** is the best free source for challenger odds
- **Set probability model:** P(win from 0-1 down) ≈ p² where p = set win probability

### Basketball (NCAAB)
- **Small conference tournaments** = 4-9% EV
- **Big conference tournaments** = efficiently priced (1-2% from books)
- **NBA/NHL live** = 1¢ spreads, zero edge
- **Halftime leads** = market adjusts correctly within minutes

### Weather
- **NWS forecasts** help but shift frequently
- **High variance** — even correct bets lose often
- **JC banned weather trading** — too much variance for the bankroll

### General
- **Pre-game lines tighten by tip-off** — early entry can capture wider spreads
- **Don't chase** — if the edge closes, walk away
- **Take profits at 10-15%** — stop riding to resolution
- **"NO on favorites"** = JC's preferred strategy when edge exists
