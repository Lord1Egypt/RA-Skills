# Lessons from Existing Task Records

This structure reflects recurring LC/ARK task-record outcomes. Guard against these failure modes when applying it elsewhere.

## 1. README status drift

Some packages still reported “source not started” after GOAL, receipts, and repository commits showed completion.

Rule: keep only navigation and derived status in README. Recompute summaries from GOAL, execution, review, and current facts at every milestone.

## 2. Binary completion hides missing review

Some GOAL files used one checked box for both “Worker finished” and “system confirmed correct,” making independent-review regressions impossible to represent accurately.

Rule: enforce the three-state model. Implementation is not approval; approval binds an exact `REVIEW` or explicitly selected `SELF` receipt to an exact snapshot.

## 3. Design and execution are mixed

Appending results directly to an implementation plan makes the original plan, field deviations, and final facts indistinguishable over time.

Rule: design stores decisions and plans; execution stores actual actions; review stores independent judgments.

## 4. Reviewer results exist only in chat or large orchestration files

High-quality findings and re-review loops can become buried in long coordination records.

Rule: give each Reviewer an append-only review file with per-item verdicts. GOAL references receipts rather than duplicating findings.

## 5. Test quantity does not prove target coverage

Broad suites sometimes passed without reaching the exact negative branch, strict fixture, or real target. Long commands were also interrupted and only became attributable after splitting.

Rule: freeze risk-to-validation mappings first. Record exact commands, counts, durations, and interruptions. Treat broad suites as supplemental evidence.

## 6. Plans drift from current code

Long-lived packages span multiple baselines, leaving stale names, tool counts, and workflows in plans.

Rule: recheck current HEAD, callers, and schema whenever starting or resuming. Historical plans are navigation aids, not current truth.

## 7. Parallel coordination needs single-writer aggregate files

Fixed Worker/Reviewer pairs, write lanes, integration windows, and gates work well; shared aggregate records become conflict-prone when everyone edits them.

Rule: Workers write their own GOAL/execution files, Reviewers write their own review files, and the Orchestrator alone writes root GOAL and coordination files.

## 8. Independent review finds distinct classes of defects

Reviewers have found stale state, transaction-order bugs, races, fixtures that miss target branches, and Agent-surface inconsistencies that more Worker self-testing did not naturally reveal.

Rule: inspect real code or artifacts and realistic negative cases. Use an independent context and the configured reasoning level.

## 9. Defensive review can crowd out business correctness

Some reviews spent multiple iterations on extreme malformed inputs or resource-exhaustion shapes that were outside the supported contract, while the important business state machine received less attention.

Rule: prioritize confirmed business paths, real consumer contracts, and high-consequence persistence, authority, recovery, and security invariants. Require plausible reachability and evidence for blocking `P2` findings. Consolidate speculative long-tail hardening as non-blocking residual work instead of expanding the current task.
