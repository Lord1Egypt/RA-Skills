# Progress Model (v0.2)

Use EMA and confidence to avoid overreacting to one quiz.

## Metrics

- `last_score`: Most recent quiz percent.
- `ema_score`: Exponential moving average with alpha=0.35.
- `delta_vs_ema`: last_score - ema_score.
- `confidence` (0-100): increases with attempts + consistency.
- `level`: derived from ema_score (0-44 beginner, 45-74 intermediate, 75-100 advanced).

## Why EMA

EMA smooths noisy results and gives a better signal for plan adjustments than raw last-score only.

## Adaptation suggestions

- `ema_score` rising and confidence > 60: raise difficulty gradually.
- `ema_score` flat and weak areas stable: keep level, rotate examples.
- `ema_score` falling with low confidence: reduce scope, revisit fundamentals.
