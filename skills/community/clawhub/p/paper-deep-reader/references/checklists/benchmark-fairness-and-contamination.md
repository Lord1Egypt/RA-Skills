# Checklist: Benchmark Fairness and Contamination

Run this after the general checklist.

## Task and metric validity

- [ ] I stated what capability, behavior, or system property the benchmark is intended to measure.
- [ ] I checked whether the metric actually tracks that target rather than an easy proxy.
- [ ] I noted whether aggregate metrics hide important slice-level failures.
- [ ] I recorded any mismatch between leaderboard improvement and real task validity.

## Comparison fairness

- [ ] I checked whether baselines were compared under similar prompt budgets, tool access, decoding settings, or evaluation privileges.
- [ ] I checked whether hidden tuning, prompt engineering, or evaluator access could tilt the comparison.
- [ ] I recorded whether the benchmark favors one family of systems by construction.
- [ ] I noted whether the strongest relevant baselines were included.

## Contamination and leakage

- [ ] I checked whether the paper tested for train-test leakage, memorization, or benchmark contamination.
- [ ] I noted whether contamination checks were direct, indirect, weak, or absent.
- [ ] I checked whether data reuse, web overlap, or prior public exposure could affect the results.
- [ ] I recorded whether leakage risk is different across compared systems.

## Judge or evaluator risk

- [ ] I checked whether the evaluator, rubric, or judge model could inject bias.
- [ ] I noted whether inter-rater consistency, calibration, or judge sensitivity was reported when relevant.
- [ ] I checked whether the evaluation pipeline could be gamed without improving the claimed capability.

## Skepticism / failure risks

- [ ] I considered whether the benchmark is mainly measuring familiarity with the format rather than the target capability.
- [ ] I considered whether apparent gains could come mostly from benchmark-specific tuning.
- [ ] I recorded at least one place where the benchmark may be too narrow, too fragile, or too easy to game.

## If the answer is weak, reflect it in the note

- [ ] I changed the claim-evidence matrix accordingly.
- [ ] I recorded at least one caveat in `## Limitations and failure modes`.
- [ ] I weakened my verdict if the support is narrow.
