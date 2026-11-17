# Signal Weighting and Decay

See `references/strength_model.md` for the full model.

## Key parameters

- Config: `decay.halflife_days` (default 180)
- Frequency bonus: +0.05 per repeat visit, capped at +0.15
- Recency bonus: +0.05 if last signal within 30 days

## Temporal decay formula

Effective strength = base_strength × decay_factor + frequency_bonus + recency_bonus

Where decay_factor = 0.5 ^ (days_elapsed / halflife_days)