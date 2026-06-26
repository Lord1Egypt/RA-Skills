# 📺 Stonkmode Architecture

**Status**: Production Ready  
**Version**: 2.0.0  
**Last Updated**: 2026-04-19

---

## Overview

Stonkmode is InvestorClaw's **entertainment layer**—a presentation-only system that wraps portfolio analysis in witty, contextual commentary from 30+ fictional cable finance TV personalities. 

**Key principle**: Data analysis runs normally. Stonkmode only changes *how results are narrated* to the user.

---

## Architecture Flow

```
complete_analysis.json (7 dimensions)
        ↓
  _detect_market_condition()
        ↓
  [bull|bear|bonds|yawny|volatile|crash|...]
        ↓
  _calculate_archetype_weights()
        ↓
  {high_energy: 0.25, digital: 0.32, serious: 0.13, ...}
        ↓
  select_pair_weighted(archetypes)
        ↓
  (lead_id, foil_id) → (e.g., "skip_contrarian", "victor_voss")
        ↓
  get_pairing_dynamic(lead_arch, foil_arch)
        ↓
  "Skip finished a point... Victor has opened his mouth..."
        ↓
  Dr. Stonk commentary (news + portfolio context)
        ↓
  Dashboard HTML with narration panel
```

---

## 1. Market Condition Detection

### `_detect_market_condition(analysis_data) → day_type`

Analyzes three signal types to classify the trading day:

| Signal | Source | Range | Interpretation |
|--------|--------|-------|-----------------|
| **News** | `dimensions.news.posture` | Positive/Neutral/Negative | Market sentiment from headlines |
| **Analyst** | `dimensions.analyst.recommendations` | -2 to +2 | Consensus bias (Strong Buy → Strong Sell) |
| **Volatility** | `dimensions.performance.weighted_volatility` | 0.0 to 1.0+ | Market chaos level |

### Day Types

| Type | Condition | Archetype Bias |
|------|-----------|-----------------|
| **strong_bull** | Analyst avg > 1.5 + Positive news | high_energy (3x), digital (2.5x) |
| **bull** | Analyst > 0.5 + Positive news | high_energy (2.5x), digital (2x) |
| **bear** | Analyst < -0.5 OR Negative news | bears (2.5x), serious (1.8x) |
| **crash** | Analyst < -1.0 + Negative news | bears (3.5x), serious (2x) |
| **bonds_day** | Bond YTM > 4% OR flight-to-safety | mentors (3x), serious (2x) |
| **volatile** | Volatility > 25% | wildcards (2.5x), cosmic (2x) |
| **yawny** | Volatility < 0.5% + Neutral | digital (2.5x) — Krystal/Zara dominate |
| **sideways** | Low movement + Neutral sentiment | policy_veterans (1.8x), serious (1.5x) |
| **mixed_signals** | Conflicting (positive news, negative analyst) | wildcards (2x), policy_veterans (1.8x) |

---

## 2. Archetype Weighting

### `_calculate_archetype_weights(analysis_data) → {archetype: weight}`

Maps day type to weighted probabilities for each archetype:

```python
weights = {
    "high_energy":     0.0,  # Blitz, Brick, Sal
    "serious":         0.0,  # Prescott, Amara, Carmen
    "mentors":         0.0,  # Big Jim, Baron Von Cashflow, Sunny
    "policy_veterans": 0.0,  # Skip, Biff
    "wildcards":       0.0,  # Glorb, ARIA-7, Professor What?
    "cosmic":          0.0,  # Chico, Farley
    "digital":         0.0,  # Krystal, Zara, Priya
    "bears":           0.0,  # Victor, Hans-Dieter
}
```

**Normalization ensures diversity**: Even in strong bull market, bears still have 0.2x weight (2.6% selection probability across many runs).

---

## 3. Host Selection

### `select_pair_weighted(archetypes, weights) → (lead_id, foil_id)`

**Weighted sampling** (not deterministic):
1. Select **lead archetype** by weighted probability
2. Select random **lead persona** from that archetype pool
3. Select **foil archetype** from complementary archetypes (FOIL_POOLS)
4. Select random **foil persona** from foil archetype pool

**Example**: Bull day + weighted selection
- Lead: high_energy (25% prob) → selects "blitz_thunderbuy"
- Foil: serious (12% prob) → selects "prescott_pennington_smythe"
- Dynamic: "Blitz just called this a GENERATIONAL BUYING OPPORTUNITY and Prescott Pennington-Smythe is removing his glasses..."

---

## 4. Pairing Dynamics

### `get_pairing_dynamic(lead_arch, foil_arch, lead_id, foil_id) → narrative`

Pre-written **tension narratives** for every archetype combination + special cases for individual wildcard personas.

**Examples**:
- `(high_energy, serious)`: "Blitz is slamming his desk. Prescott is removing his glasses very slowly."
- `(bears, bears)`: "Hans-Dieter and Victor have found each other. The producer is watching ratings tick up..."
- `(wildcards_aria_7, any)`: "An android just calculated a 73.2% probability that the co-host's take is driven by confirmation bias..."

**Special handling**: Wildcard personas have individual dynamics (Glorb's "Sacred Balance," Professor What?'s temporal ethics, King Donny's superlatives).

---

## 5. Dr. Stonk Commentary

### `_generate_stonkmode_narration(analysis_data, total_value) → narration_dict`

Enriches narration with:
- **Portfolio context**: Total value, allocation
- **Market condition**: "STRONG BULL rally" vs "bonds day"
- **News tailwinds**: "Key tailwind: Apple's Smart Glasses..."
- **Risk alerts**: "Monitor: credit spread widening"

**Dr. Stonk persona**: Logical Vulcan from planet Hephaestus. Comments on archetype dynamics and market nuance. Provides educational framing without editorializing.

---

## 6. Dashboard Integration

### HTML Payload Structure

```json
{
  "stonkmode_narration": {
    "lead_id": "skip_contrarian",
    "lead_name": "Skip \"Well, Actually\" Contrarian",
    "foil_id": "victor_voss",
    "foil_name": "Victor \"The Vulture\" Voss",
    "dynamic": "Skip finished a point about monetary policy...",
    "stonk_commentary": "Dr. Stonk here. Your portfolio is $39,462 in a STRONG BULL rally..."
  }
}
```

### Rendering (app.js)

```javascript
Dashboard.renderStonkmodeNarration() {
  // Display:
  // - Lead persona name
  // - Pairing dynamic (tension narrative)
  // - Foil persona name
  // - Dr. Stonk commentary with tailwinds/risks
}
```

---

## 7. Character Roster (30 Personas)

### By Archetype

**high_energy** (3): Blitz Thunderbuy, Brick Stonksworth, Sal Decibelli  
**serious** (5): Aldrich Whisperdeal, Prescott Pennington-Smythe, Dominique Valcourt, Amara Osei, Carmen Torres  
**mentors** (3): Big Jim Cashonly, Sunny Rainyday-Fund, Baron Von Cashflow  
**policy_veterans** (2): Biff Chadsworth III, Skip Contrarian  
**wildcards** (9): Dorin Goleli, ARIA-7, Professor Goldbug, Chaz Leveridge, Lafayette Beaumont, Glorb, King Donny, Zsa Zsa Von Portfolio, Wendell The Pattern, Professor What?  
**cosmic** (2): Chico Reyes, Farley McGee  
**digital** (3): Krystal Kash, Zara Zhao, Priya Hodl  
**bears** (2): Victor Voss, Hans-Dieter Braun  

### Selection Diversity Over 20 Runs

Even in strong bull market (weighted: high_energy 26%, digital 32.5%), all 8 archetypes appear:
- serious: 9 selections
- high_energy: 8
- digital: 6
- cosmic: 6
- policy_veterans: 4
- mentors: 3
- bears: 2
- wildcards: 2

**No echo chamber**: Bearish skeptics still voice concerns in bullish markets.

---

## 8. Refresh Flow

### Dashboard Refresh Lifecycle

```
User clicks [⟳ Refresh] button
        ↓
POST /api/refresh endpoint
        ↓
subprocess: portfolio_complete.py --auto
        ↓
  Regenerates: complete_analysis.json (7 dimensions)
        ↓
subprocess: dashboard.py --auto --stonkmode
        ↓
  Detects market condition
  Weights archetypes
  Selects new host pairing (random)
  Generates narration with news context
  Renders updated HTML
        ↓
Returns: dashboard_path, generated_at
        ↓
Browser: Reloads dashboard.html with fresh narration
```

---

## 9. Female Character Distribution

**Female personas** (biased for "yawny" days):
- Krystal Kash (digital, high-energy irreverence)
- Zara Zhao (digital, "algorithm understood the assignment")
- Priya Hodl (digital, crypto focus)
- Dominique Valcourt (serious, professional rigor)
- Amara Osei (serious, ESG/TCFD specialist)
- Carmen Torres (serious, technical analysis)
- Zsa Zsa Von Portfolio (wildcard, ex-husband metaphors)

**Yawny day tuning**: Prefers digital (2.5x) → Krystal/Zara/Priya likely paired.

---

## 10. Backwards Compatibility

**Fallback behavior** (if stonkmode unavailable):
- Dashboard still renders (no narration panel, no Market Commentary tab)
- Dr. Stonk commentary absent
- Refresh button works (no stonkmode regeneration)
- All 7 dimension analyses intact

**Feature flag**: `INVESTORCLAW_STONKMODE_DISABLED=true` disables stonkmode globally.

---

## Testing Stonkmode

### Manual Testing

```bash
# Generate dashboard with stonkmode
python3 commands/dashboard.py --auto --stonkmode

# Open in browser
open ~/portfolio_reports/2026-04-19/dashboard.html

# Check for:
# - [📺 Market Commentary] tab showing pairing
# - Dr. Stonk commentary with market context
# - Key tailwinds/risks mentioned
```

### Programmatic Testing

```python
from commands.dashboard import _detect_market_condition, _calculate_archetype_weights

analysis = json.load(open("complete_analysis.json"))

day_type = _detect_market_condition(analysis)
print(f"Detected day type: {day_type}")

weights = _calculate_archetype_weights(analysis)
print(f"Archetype weights: {weights}")
```

---

## Performance Notes

- **Detection**: ~5ms (simple signal calculations)
- **Weighting**: ~2ms (archetype weight multipliers)
- **Selection**: ~1ms (random.choices with weights)
- **Narration generation**: ~10ms (persona lookup + dynamic template)
- **Total stonkmode overhead**: <20ms (negligible vs. analysis pipeline)

---

## Future Enhancements

1. **Persistence**: Save host pairings + commentary to database for historical analysis
2. **Training data**: Use pairing narratives to fine-tune market sentiment classifier
3. **A/B testing**: Compare user engagement (stonkmode on vs off)
4. **Mobile UI**: Optimize narration panel for smaller screens
5. **Voice**: Generate audio narration from stonkmode text (text-to-speech)
6. **Streaming**: Real-time host pairings during market hours (vs. snapshot model)

---

## References

- **Personas**: `rendering/stonkmode_personas.py` (30 characters + archetypes)
- **Pairings**: `rendering/stonkmode_pairings.py` (archetype pools, foil rules, 100+ dynamics)
- **Dashboard**: `commands/dashboard.py` (market detection, weighting, narration)
- **HTML template**: `rendering/pwa/dashboard.html` (4-tab UI + narration panel)
- **App logic**: `rendering/pwa/assets/app.js` (renderStonkmodeNarration)
