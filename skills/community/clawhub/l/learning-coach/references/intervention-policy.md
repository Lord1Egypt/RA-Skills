# Intervention Policy (v0.3)

Use `scripts/intervention_rules.py` to convert learning signals into pacing guidance.

Modes:
- `speed-up`: when EMA and confidence are high.
- `stabilize`: when performance is moderate/variable.
- `slow-down`: when EMA drops or confidence is low with negative delta.

Always explain why a mode was chosen and provide 2-4 concrete actions.
