# Capability Facts

Capability facts are derived from closed work, not self-reported claims.

Each fact captures:

- `scenario_signature`
- `skill_name`
- `workflow_name`
- `style_family`
- `variant_label`
- `closure_type`
- closure metrics
- confidence
- sample size
- timestamp
- anonymized payload

Facts are distilled from:

- run event logs
- skill traces
- summary and checkpoint state
- closure outcome metadata

The manager also derives a local capability graph summary:

- scenario nodes
- skill nodes
- workflow nodes
- closure rate
- failure rate
- human intervention rate

Exports are redacted by default. Raw chat transcripts stay local unless the operator explicitly shares them elsewhere.
