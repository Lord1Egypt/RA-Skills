# Edge Rules

Use these as lightweight heuristics, not certainty machines.

## 1. Up-side value

Possible up-side value when:
- `p_up_pct` is clearly above the market's up ask
- the gap is not trivial
- data is fresh

Example:
- model up 62%
- up ask 0.53

This suggests the market is pricing lower than the model.

## 2. Down-side value

Possible down-side value when:
- `p_down_pct` is clearly above the market's down ask
- the gap is not trivial
- data is fresh

## 3. Ignore tiny gaps

If the gap is only around 1-2 percentage points, treat it as noise unless the user explicitly wants micro-edge discussion.

## 4. Mention timing

If `rem_secs` is low, mention that the window is tight and noise risk is higher.

## 5. Mention stale data

If timestamps or TTL suggest stale data, say that before making any interpretation.

## 6. Good default answer shape

- strongest up setup
- strongest down setup
- one or two possible model-vs-market mismatches
- one caveat
