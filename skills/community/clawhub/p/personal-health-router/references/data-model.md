# Public Data Model

This is the public, config-driven version of the Healthcare schema.

## Raw tables

### Nutrition meals
Minimum fields:
- datetime
- food description
- calories
- protein
- sodium
- carbs
- fat
- fiber

Recommended:
- image attachment
- estimated weight
- portion note
- confidence
- note
- micronutrients when available

### Sleep recovery
Minimum fields:
- date
- source app
- total sleep
- sleep score
- recovery state
- fatigue risk
- confidence
- one-line summary

Recommended:
- deep sleep
- REM
- awake time
- core/light sleep
- normalized minute fields
- HRV
- body signals
- advice
- reason
- missing fields

### Exercise workouts
Minimum fields:
- datetime
- source app
- workout type
- total duration
- total duration minutes
- calories
- load
- one-line summary
- confidence

Recommended:
- average HR
- max HR
- pace/speed
- distance
- rationale
- advice
- reason
- missing fields

## Derived tables

### Nutrition daily history
One row per local day. Aggregate nutrition metrics and short assessment.

### Monthly health calendar
One row per local day. Merge nutrition, sleep, and exercise into a dashboard-ready daily record.

### Weekly health assessment
One row per completed week. Cross-domain summary with counts, risks, and next-step recommendations.

## Public boundary

The internal table schema and dashboard blocks are English-only. If a deployment requires different field labels (e.g., for legacy reasons), they must be handled through `field_aliases` in the configuration. Chinese user input is supported via mapping/recognition layers outside these scripts, but the persistence layer remains English-only.
