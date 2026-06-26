# Strength Model

How Taste computes signal strength for consumption signals. Strength determines how much weight an item carries in the taste model and recommendation ranking.

## Base strength by source type

| Source | Base strength | Rationale |
|--------|--------------|-----------|
| purchase | 0.80 | Spending money is a strong commitment signal |
| visit | 0.70 | Reservation/visit confirms intent but may include social obligation |
| stay | 0.75 | Hotel stays involve planning and cost |
| play | 0.60 | Music plays are lower friction but still signal preference |
| watch | 0.60 | Movie/show watches are moderate commitment |
| manual | 0.60 | User-reported; trust the user but weight conservatively |
| email_extraction | varies | Inherits base from source type (purchase/visit/stay) |
| calendar_extraction | 0.70 | Calendar entries confirm planned consumption |

## Frequency bonus

Repeat consumption is a strong signal. Each repeat visit/order for the same item adds a bonus to effective strength.

```
frequency_bonus = min(frequency_bonus_cap, frequency_bonus_per_visit × (signal_count - 1))
```

**Defaults:**
- `frequency_bonus_per_visit`: 0.05
- `frequency_bonus_cap`: 0.15

A restaurant visited 4 times gets +0.15 (capped). This bonus applies to the item's effective strength when ranking for recommendations, not to individual signal records.

## Recency bonus

Items consumed recently get a small boost to reflect current preference.

```
if (days_since_last_signal <= recency_bonus_days):
    recency_bonus = recency_bonus_value
else:
    recency_bonus = 0
```

**Defaults:**
- `recency_bonus_days`: 30
- `recency_bonus_value`: 0.05

## Temporal decay

Applies to all signals per `signal_policy.md`:

```
effective_strength = strength × 0.5^(days_since / halflife_days)
```

Default `halflife_days`: 180. Repeat signals reset the decay clock for that item.

## Effective item strength (for recommendations)

When ranking items for recommendation seed selection:

```
effective_item_strength = max(decayed_signal_strengths) + frequency_bonus + recency_bonus
```

Uses the strongest (most recent, highest base) signal for the item, plus bonuses. Capped at 1.0.

## Extraction confidence threshold

Email/calendar extractions have their own `extraction_confidence` (0.0–1.0). Only extractions above `extraction_confidence_threshold` (default: 0.6) are promoted to ConsumptionSignals. Extractions between 0.6 and 0.8 are promoted but with a strength penalty of -0.1.

**Config defaults:**
- `extraction_confidence_threshold`: 0.6
- `auto_promote_threshold`: 0.8 (above this, no penalty)

## Config location

All strength parameters are in `config.json` under `strength`:

```json
"strength": {
  "base_purchase": 0.80,
  "base_visit": 0.70,
  "base_stay": 0.75,
  "base_play": 0.60,
  "base_watch": 0.60,
  "base_manual": 0.60,
  "frequency_bonus_per_visit": 0.05,
  "frequency_bonus_cap": 0.15,
  "recency_bonus_days": 30,
  "recency_bonus_value": 0.05
}
```
