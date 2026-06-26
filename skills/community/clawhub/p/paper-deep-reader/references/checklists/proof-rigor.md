# Checklist: Proof Rigor

Run this after the general checklist.

## Claim fidelity

- [ ] I stated the main theorem, proposition, or formal guarantee in a way that preserves its actual scope.
- [ ] I recorded the exact object of the claim: consistency, identifiability, convergence, approximation, robustness, lower bound, or existence.
- [ ] I distinguished the paper's strongest formal claim from weaker corollaries, intuitions, or informal interpretations.
- [ ] I did not upgrade a conditional, asymptotic, or local result into an unconditional or global one.

## Assumptions and regime

- [ ] I listed the assumptions that the main result really depends on.
- [ ] I distinguished structural assumptions from technical convenience assumptions when the paper makes that possible.
- [ ] I stated the regime clearly: finite-sample, asymptotic, noiseless, realizable, overparameterized, convex, local, or distribution-specific.
- [ ] I noted at least one assumption that seems strong, hidden, or easy to forget in downstream discussion.

## Proof architecture

- [ ] I summarized the proof strategy at a level more informative than “the authors prove it.”
- [ ] I identified the key lemmas, decomposition, reduction, construction, or invariants that carry the argument.
- [ ] I noted whether the proof is constructive, existential, perturbative, asymptotic, reduction-based, or concentration-heavy.
- [ ] I recorded where the main intellectual load sits: new technique, sharper bound, cleaner reduction, or stronger assumptions.

## Interpretation and limits

- [ ] I checked whether the theorem actually supports the paper's broader narrative.
- [ ] I noted what the result does not establish: practical superiority, finite-sample usefulness, computational tractability, or robustness beyond the proven regime.
- [ ] I distinguished mathematical sufficiency from empirical relevance when the paper spans both theory and experiments.
- [ ] I recorded at least one meaningful special case, boundary case, or failure regime when possible.

## Skepticism / failure risks

- [ ] I considered whether the result is mainly technically correct but substantively narrow.
- [ ] I considered whether the theorem depends on assumptions that remove the hardest part of the real problem.
- [ ] I checked whether asymptotic or worst-case language is being rhetorically sold as ordinary-case practical advantage.
- [ ] I recorded at least one caveat about the result's interpretive reach.

## If the answer is weak, reflect it in the note

- [ ] I changed the claim-evidence matrix accordingly.
- [ ] I recorded at least one caveat in `## Limitations and failure modes`.
- [ ] I weakened my verdict if the formal support is narrower than the paper's narrative suggests.
