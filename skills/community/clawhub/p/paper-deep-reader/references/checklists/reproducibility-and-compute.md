# Checklist: Reproducibility and Compute

Run this after the general checklist.

## Resource accounting

- [ ] I recorded the model size, data scale, hardware, training budget, or wall-clock information when it materially affects the result.
- [ ] I checked whether compute, data, or hyperparameter asymmetries make the comparison hard to interpret.
- [ ] I noted whether the claimed gain could mostly reflect scale rather than method.
- [ ] I recorded any missing resource information that blocks a fair comparison.

## Implementation-sensitive detail

- [ ] I stated the training or optimization details that materially affect the result.
- [ ] I recorded important preprocessing, augmentation, filtering, batching, or decoding choices.
- [ ] I noted whether the method depends on a large hidden engineering stack.
- [ ] I checked whether the appendix or code release promises contain details missing from the main text.

## Rebuildability

- [ ] I judged whether a strong practitioner could reproduce the core result from the paper.
- [ ] I identified the most important missing detail that would block faithful reimplementation.
- [ ] I distinguished between exact reproduction, approximate reproduction, and vague conceptual imitation.

## Comparison integrity

- [ ] I checked whether baselines received comparable tuning effort.
- [ ] I noted whether private data, unavailable infrastructure, or proprietary components make the comparison asymmetric.
- [ ] I checked whether the evaluation setup depends on infrastructure the reader cannot realistically reconstruct.

## Skepticism / failure risks

- [ ] I considered whether the paper is selling a method gain that may actually be a compute gain.
- [ ] I considered whether reproducibility is being deferred to future code release without enough paper detail.
- [ ] I recorded at least one implementation-sensitive caveat when the paper is underspecified.

## If the answer is weak, reflect it in the note

- [ ] I changed the claim-evidence matrix accordingly.
- [ ] I recorded at least one caveat in `## Implementation / reproduction notes` or `## Limitations and failure modes`.
- [ ] I weakened my verdict if the result seems difficult to verify independently.
