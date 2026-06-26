# Aggregation

## Goal
Merge multiple OSINT findings into one structured result.

## Inputs to aggregate
- profile checks
- HIBP breach results
- domain checks
- IP checks
- web-confirmed findings

## Aggregation rules
- keep raw evidence separate from summary judgments
- score per finding first, then estimate an overall confidence band
- prefer exact > likely > weak > not_verifiable > no_result
- do not let one noisy platform dominate the final score

## Suggested overall confidence logic
- strong: several strong signals or exact matches with corroboration
- likely: multiple aligned signals, limited conflict
- possible: some useful signals but not enough corroboration
- weak: little evidence or conflicting evidence

## Final summary should include
- target
- target type
- strongest findings
- weaker/ambiguous findings
- overall confidence
- caveats
