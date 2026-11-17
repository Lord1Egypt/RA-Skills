# Reliability Architecture

| Layer | Failure | Response |
| --- | --- | --- |
| Score facts | Missed heads, false notes, wrong clef/key/accidental/chord | Verify local counts, rests, duration, and pitch before generation. Never infer missing notes from patterns. |
| Source reuse | Old coordinates used on a new PDF/render | Bind source paths, dimensions, and SHA-256. Rebuild after changes. |
| Fingering | Repeated/tied pitch changes, duplicate chord fingers, dyad/bass conflicts | Enforce constraints, guarded repairs, and transposed regressions. |
| Phrase planning | Local choices leave no preparation for later notes | Review complete phrases and search disagreement. Hand-size sensitivity can prioritize review. |
| Annotation | Drift, excessive distance, diagonal digits, collisions | Audit anchors, ownership, clearance, and final rendering separately; move labels only. |
| Delivery | Long execution returns only an error | Write reports early; retain sources, plans, logs, crops, and review scopes. |

Prefer original structured semantics. Without verified original-page coordinates, deliver annotated MusicXML and state that original-page annotation was not performed.

For visual inputs, original PNGs supply coordinates; optional OMR proposes semantics for independent measure review. Candidates cannot verify themselves.

Use draft → review → verified → locked. The fact lock covers score facts and source fingerprints. Fact/page changes reopen affected scopes; changing fingerings or label layout must not alter score facts.

Complete visual output requires independent counts for every target measure, passing hard constraints and at least 90% search stability, at least 90% for each of four geometry checks, and no unresolved recognition queue.

```bash
python3 scripts/audit_hand_size_stability.py locked-plan.json fingered-plan.json \
  -o hand-size-stability.json
```

This optional audit preserves current fingers, creates an adjacent-size candidate, and reports disagreements by page/measure/hand. Sensitivity is not an automatic correction.

Do not generalize a single editor/score/regression result to all repertoire. OMR, old plans, projections, and nearby ink are not verified heads. Do not turn one chord fix into a universal pattern. Foundational scales, accompaniment, chords, ties, and repeats have deterministic regressions; long phrases still require musical review.
