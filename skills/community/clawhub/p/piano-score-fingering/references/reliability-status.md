# Reliability Status and Evidence Boundaries

Use current generated reports as evidence. Historical percentages are diagnostic snapshots, not guarantees for the installed version or every score.

## Current component evidence

The maintained local October 30, 2026 run recorded:

| Measurement | Result | Scope |
| --- | --- | --- |
| Partial editorial agreement across 8 pieces | 223/256, 87.1% | Visible frozen reference fingers; not every note or full recognition. |
| Untouched fingering holdout, Gurlitt Op.117 No.8 | 28/31, 90.3% | One short piece, partly labeled; not a broad repertoire estimate. |
| Foundational regression | 2111/2128, 99.2% | Technical patterns; every named group above 80%. |
| Independent candidate-layout holdout, Gurlitt Op.117 No.7 | 89/90, 98.9% conservative placement; 90/99 printed, 90.9% coverage | Candidate geometry only; semantics remain review-required. |
| Four-PDF candidate geometry aggregate | 93.3% conservative placement; 96.5% coverage | Visible candidate labels; not fully verified whole-score accuracy. |

Source scores, frozen reference answers, and private reports remain outside the package. These figures must be regenerated from retained local evidence before being reused as current claims. Recognition regressions and skill structure validation also passed in that run.

## Important failures retained

Before Spring Ends initially achieved 53/99 (53.5%) on an independent attempt. After its failures were inspected, it became development data; later 90/99 (90.9%) cannot be called an untouched holdout result.

Water Lily and Acacia Flower were likewise development data after answer inspection. Gurlitt No.8 was reserved for the final fingering test. Its layout later informed a generic ownership fix, so No.7 supplied a separate untouched geometry test.

Gurlitt No.1 exported invalid MusicXML with divisions=0 and could not enter generation; it remains a recognition failure. The importer now reports an invalid rhythmic timebase explicitly. Do not remove this failure when discussing OMR reliability.

Earlier public MXL diagnostics involving Canon, Greensleeves, and Fur Elise exposed substantially lower editorial agreement. They have different difficulty/editorial scope and cannot be merged into level-5 acceptance or silently dropped. A historical 199/298 (66.8%) diagnostic remains evidence of limited generalization, not a substitute for the current private/holdout reports.

## Main limitations

OMR may export an apparently structured file with incorrect rhythm, rests, chord topology, octaves, or missing measures. Source ink near a coordinate does not verify those facts.

Long-phrase fingering still has multiple plausible choices. Search agreement is only a review signal; a historical Canon trial found that 4/7-event disagreement covered about 13% of editorial mismatches. Greater lookahead alone did not consistently improve results and sometimes cost more.

Hand-size presets are personal assumptions rather than accuracy switches. Preserve M as the neutral default, then review adjacent-size sensitivity when useful.

## Claims and delivery

Report editorial exact match, hard-rule compliance, search stability, recognition completeness, and candidate/formal placement separately. Explicit provisional output is a review aid, not formal semantic acceptance. Follow visual-benchmark-protocol.md for any future whole-score target claim.
