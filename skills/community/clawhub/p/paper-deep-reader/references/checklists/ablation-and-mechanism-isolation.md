# Checklist: Ablation and Mechanism Isolation

Run this after the general checklist.

Use this checklist when a paper claims that a particular component, design choice, operator, loss term, memory mechanism, inference strategy, or training trick is responsible for the observed gain.

## Claimed mechanism

- [ ] I stated clearly what component or mechanism the authors say drives the improvement.
- [ ] I checked whether that claim is central or merely suggestive.
- [ ] I recorded what the method becomes when that component is removed.
- [ ] I distinguished the named mechanism from surrounding implementation changes.

## Isolation quality

- [ ] I checked whether the strongest ablation actually isolates the claimed mechanism.
- [ ] I noted whether multiple changes were bundled together so that the source of the gain remains ambiguous.
- [ ] I checked whether the paper compares against the most informative reduced or stripped-down variant.
- [ ] I recorded whether an ablation is missing exactly where the mechanism claim is strongest.

## Alternative explanations

- [ ] I considered whether the gain could come from scale, tuning, regularization, better optimization, or extra context rather than the claimed component.
- [ ] I checked whether the paper ruled out these alternative explanations directly.
- [ ] I recorded whether the mechanism claim is stronger than the ablation evidence really supports.

## Robustness of the mechanism claim

- [ ] I checked whether the claimed component still helps across tasks, scales, seeds, or regimes that matter.
- [ ] I noted whether the component helps only in one narrow benchmark setup.
- [ ] I recorded whether the gain changes sign or vanishes when the surrounding configuration changes.

## Interpretation discipline

- [ ] I avoided writing as if the component is proven decisive when the evidence is only correlational or partial.
- [ ] I distinguished “this component is necessary,” “this component helps,” and “this component is one plausible contributor.”
- [ ] I recorded the strongest support for the mechanism claim and the strongest remaining ambiguity.

## Skepticism / failure risks

- [ ] I considered whether the ablations are decorative rather than diagnostic.
- [ ] I considered whether the paper is attributing gain to the most narratively attractive component rather than the best-supported one.
- [ ] I recorded at least one unresolved alternative explanation when isolation is incomplete.

## If the answer is weak, reflect it in the note

- [ ] I changed the claim-evidence matrix accordingly.
- [ ] I recorded at least one caveat in `## Evidence` or `## Limitations and failure modes`.
- [ ] I weakened my verdict if the mechanism remains poorly isolated.
