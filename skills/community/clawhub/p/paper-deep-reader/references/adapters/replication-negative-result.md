# Adapter: Replication / Negative Result

Use this adapter when the paper's main contribution is a replication study, failed replication, stress test of a prior claim, robustness challenge, negative empirical result, or systematic demonstration that a published effect is weaker, narrower, or less reliable than previously thought.

## What to prioritize

1. The original claim, result, or paper being tested.
2. The degree of fidelity between the replication attempt and the original setup.
3. What exactly failed to replicate: headline metric, effect size, qualitative behavior, or downstream usefulness.
4. Whether the negative result is about the claimed mechanism, the evaluation setup, or implementation dependence.
5. Alternative explanations for the mismatch.
6. What uncertainty remains after the negative evidence is presented.

## Questions to answer in the note

- What prior claim is being interrogated?
- What counts as a faithful replication in this context?
- Which parts of the original setup were matched, approximated, or unavailable?
- What results replicated, and what results did not?
- Is the negative result narrow, moderate, or devastating for the original claim?
- What explanations are plausible: implementation detail, data shift, hidden tuning, benchmark fragility, statistical noise, or conceptual error?
- What should a careful reader now believe about the original claim?

## Minimum insertions into the note

Add or expand these sections:

### Problem setup

- target prior claim or body of claims
- why replication or stress testing is needed
- criteria for success or failure of replication

### Technical core

- replication protocol or stress-test design
- matched versus unmatched components of the original setup
- deviations from the original procedure and why they matter
- evaluation criteria for judging replication success

### Evidence

- side-by-side comparison with the original results when possible
- quantitative or qualitative mismatch between original and replicated findings
- sensitivity analyses and alternate implementations
- evidence that narrows down likely causes of the discrepancy

### Limitations and failure modes

Include discussion of:

- incomplete access to the original stack
- ambiguity about what counts as faithful reproduction
- whether the negative result is benchmark-specific or broader
- remaining uncertainty about untested variants of the original claim

## Special reading rules

- Distinguish “not reproduced here” from “false in general.”
- Treat fidelity to the original setup as a first-class technical issue.
- Look for whether the paper identifies the failure boundary, not just the existence of a failure.
- Be careful with rhetoric: a persuasive negative result can still overreach if replication fidelity is weak.
- Ask whether the replication targets the original mechanism, only the original metric, or merely a public implementation.

## Typical failure patterns to watch for

- replication setup diverges from the original in a way that muddies interpretation
- negative result is real but narrower than the paper implies
- original result depended on hidden tuning or undocumented infrastructure
- authors conflate failure of one implementation with failure of the underlying idea
- evidence does not isolate the source of disagreement
- benchmark or data shift explains the mismatch more than the proposed critique does
- uncertainty is rhetorically collapsed into falsification

## Reusable note prompts

- “This paper re-examines the claim that … by …”
- “The replication is high-fidelity in … but weaker in …”
- “What fails to reproduce is … whereas … remains plausible”
- “The strongest explanation for the mismatch appears to be …”
- “After this paper, the original claim should be updated from … to …”
