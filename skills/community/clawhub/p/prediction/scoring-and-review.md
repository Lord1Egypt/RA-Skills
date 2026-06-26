# Scoring and Review

Use this file after the outcome resolves or when the review date arrives.

## Score the forecast

- For binary outcomes, use Brier score: `(forecast - outcome)^2` where outcome is 1 for yes and 0 for no.
- Lower is better: 0 is perfect, 0.25 is a coin-flip level at 50%, 1.0 is maximally wrong.
- For scenario forecasts, score the assigned probability to the realized scenario and note whether the scenario set itself was incomplete.

## Miss types to tag

| Miss type | What happened |
|-----------|---------------|
| base-rate neglect | The story overrode the historical rate |
| planning optimism | Timeline or execution was too rosy |
| driver miss | The wrong variable was treated as decisive |
| update failure | New evidence arrived and the forecast stayed stale |
| resolution error | The question was framed badly from the start |
| overconfidence | Probability was too extreme for the evidence quality |

## Post-mortem prompts

Ask:
- What did the forecast get right?
- What did it miss?
- Which evidence mattered most in hindsight?
- Was the reference class wrong, too broad, or too narrow?
- Should any lesson enter `memory.md` or `reference-classes.md`?

## Improvement loop

- Move durable miss patterns into `memory.md`.
- Update reusable rates in `reference-classes.md`.
- Archive dead forecasts and keep the live scorecard compact.
- Favor learning from repeated mistakes, not one-off bad luck.
