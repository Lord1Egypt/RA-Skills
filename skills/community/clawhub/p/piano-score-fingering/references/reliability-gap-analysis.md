# Reliability Gaps and Release Criteria

| Stage | Recurring problem | Current response | Remaining limit |
| --- | --- | --- | --- |
| Recognition | False notes/rests, missed chords, wrong hand/clef/key/accidental | Locked score facts, independent regional checks, OMR as candidate | One visual pass cannot establish complete correctness. |
| Fingering | Unexplained same-pitch changes, excessive dyad spread, postprocessors overwriting decisions | Repeated-note/tie/chord/span/accompaniment constraints and final validation | Agreement with every editor is not guaranteed. |
| Long RH phrases | Edge-of-hand positions after slow held notes, leaps, or cross-bar descents | Guarded phrase patterns plus local review tasks | No unique automatic professional solution for every phrase. |
| Placement | Drift, staff overlap, misplaced LH labels, diagonal chords | Separate page/keyboard geometry, stacked chords, four audits, ownership-bounded nudges | Unverified anchors cannot support a ready-to-use formal PDF. |
| Runtime/delivery | Long waits, error-only returns, repeated OMR attempts | Stage/run timeouts, bounded OMR, early reports and source/plan retention | All uncertain score facts cannot be repaired automatically. |

Recognition regression covers rest boundaries, LH treble clef, key/geometry checks, OMR isolation, transactional anchors/event topology, trailing-rest page boundaries, source changes, and retained failure artifacts. Foundational tests cover scales, accompaniment, dyads, ties/repeats, and chord-event normalization. Current counts come from generated regression JSON.

Formal visual rendering requires verified anchors. An explicit provisional OMR preview may print safe candidate labels, with unprinted notes counted and review-required status retained.

## Evidence needed for broad release claims

- At least three independent, manually assessed level-5-or-below solo pieces, original PDF/images, and at least 100 frozen readable editorial anchors.
- Fresh generation without reference fingers; report each piece, both hands, denominators, and failed scopes.
- At least 80% editorial agreement without excluding failures.
- At least 90% ownership/source-anchor/clearance/final-render accuracy on independently verified original pages.
- Untouched holdout evidence and retained failed cases.
- Source copies, current plans, reports, and local review scopes even when thresholds fail.

Partial anchors and candidate geometry can demonstrate useful component improvements. They do not establish whole-score semantic accuracy or universal repertoire quality. State the measured scope rather than declaring broad high availability.
