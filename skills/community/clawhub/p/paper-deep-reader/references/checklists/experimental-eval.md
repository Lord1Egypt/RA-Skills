# Checklist: Experimental Evaluation

Run this after the general checklist.

Use this checklist when a paper's main claims are supported by experiments, simulations, benchmarks, held-out evaluations, or comparative quantitative results.

## Claim-to-experiment alignment

- [ ] I identified the paper's main empirical or experimental claims precisely.
- [ ] I checked whether the reported experiments actually answer those claims rather than a weaker proxy question.
- [ ] I stated which result is meant to support which claim.
- [ ] I noted when a broad conclusion is supported only by narrow settings.

## Experimental design quality

- [ ] I recorded the datasets, benchmarks, simulation environments, or tasks that matter most.
- [ ] I checked whether the chosen settings are representative of the paper's stated target use case.
- [ ] I noted whether the evaluation regime is narrow, synthetic, or unusually favorable.
- [ ] I checked whether the most relevant baseline conditions were actually tested.

## Result quality and interpretation

- [ ] I identified the strongest quantitative result and what it really shows.
- [ ] I checked whether the gains are large, small, unstable, or only visible in selective settings.
- [ ] I noted whether variance, confidence intervals, repeated runs, or sensitivity analyses were reported when they matter.
- [ ] I distinguished statistically or numerically visible gains from practically meaningful gains.

## Comparison quality

- [ ] I checked whether the strongest relevant baselines were included.
- [ ] I noted whether comparison settings are plausibly apples-to-apples.
- [ ] I checked whether training budget, inference budget, data access, or evaluation privileges differ across methods.
- [ ] I recorded any comparison asymmetry that could materially change the verdict.

## Stress tests and scope

- [ ] I checked whether the paper tested robustness, stress cases, or failure modes beyond the easiest benchmark setting.
- [ ] I noted what regimes remain untested.
- [ ] I recorded whether the evidence supports general improvement or only benchmark-local improvement.

## Skepticism / failure risks

- [ ] I considered whether the paper is drawing a broader conclusion than the experiments justify.
- [ ] I considered whether the experimental setup could flatter the proposed method.
- [ ] I recorded at least one place where the evidence is narrower, weaker, or less decisive than the headline suggests.

## If the answer is weak, reflect it in the note

- [ ] I changed the claim-evidence matrix accordingly.
- [ ] I recorded at least one caveat in `## Evidence` or `## Limitations and failure modes`.
- [ ] I weakened my verdict if the evidence is narrow or comparison quality is weak.
