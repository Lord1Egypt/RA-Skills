# Cross-turn Aggregation

1. Preserve the source label for each segment.
2. Merge exact duplicate statements.
3. Deduplicate actions by `(task, owner)`.
4. Keep conflicting variants and route them to human review.
5. Add `sources` and `aggregation_summary` metadata after aggregation.
