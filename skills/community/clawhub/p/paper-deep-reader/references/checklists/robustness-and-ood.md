# Checklist: Robustness and Out-of-Distribution Behavior

Run this after the general checklist.

Use this checklist when the paper makes claims that are supposed to survive outside a single friendly IID benchmark setting, or when deployment, transfer, safety, long-tail behavior, or distribution shift matters to the paper's practical value.

## Scope of the claim

- [ ] I stated whether the paper is claiming narrow benchmark improvement or broader generalization.
- [ ] I checked whether the note distinguishes IID gains from true robustness or transfer claims.
- [ ] I recorded the regime boundaries the paper actually tests.

## Shift and stress evaluation

- [ ] I checked whether the paper evaluates under domain shift, distribution shift, noisy inputs, adversarial conditions, long-tail slices, or harder environments when relevant.
- [ ] I noted whether these tests are direct and meaningful or only cosmetic.
- [ ] I recorded which important shifts remain untested.

## Failure behavior

- [ ] I looked for explicit failure cases rather than only average-case improvements.
- [ ] I checked whether aggregate scores hide severe failures on important subgroups, tasks, or operating regimes.
- [ ] I recorded whether the method degrades gracefully or collapses sharply outside the main benchmark setting.

## Interpretation

- [ ] I checked whether the paper is using robustness language that exceeds the evidence.
- [ ] I distinguished interpolation within benchmark families from transfer to genuinely new settings.
- [ ] I recorded whether the claimed gain appears stable, fragile, or unknown under shift.

## Practical implications

- [ ] I noted whether deployment-minded conclusions depend on evidence the paper does not actually provide.
- [ ] I recorded at least one regime where I would still be cautious even if the headline result is strong.

## Skepticism / failure risks

- [ ] I considered whether the method mainly wins on curated IID settings while remaining brittle elsewhere.
- [ ] I considered whether the robustness tests are too weak, too few, or too close to the training distribution.
- [ ] I recorded at least one concrete unresolved robustness question when the evidence is limited.

## If the answer is weak, reflect it in the note

- [ ] I changed the claim-evidence matrix accordingly.
- [ ] I recorded at least one caveat in `## Evidence` or `## Limitations and failure modes`.
- [ ] I weakened my verdict if broad generalization claims are weakly supported.
