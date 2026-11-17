# Fellow Gotchas

- **Fellow is not user-invocable** — If triggered directly by a user prompt, Fellow responds with a redirect to Mentor. Only Mentor can invoke `fellow.experiment.run` with a valid ExperimentRequest payload.
- **Baseline failure aborts the entire cycle** — If the champion baseline evaluation fails (benchmark error, harness crash), the whole experiment cycle is aborted. No variants are tested until the baseline issue is resolved.
- **Entity observations are never promoted to Chronicle** — Fellow's journals may include entity observations for lineage tracking, but Elephas does not extract Chronicle candidates from Fellow journals. Experiment artifacts stay internal.
- **Promotion threshold is strict** — A variant must beat the baseline by at least `improvement_threshold` (default 0.03) to be promotable. Variants failing guardrails are rejected even if they beat the baseline.
- **Mentor provides direction, Fellow provides optimization** — Fellow never decides what to improve; it only evaluates what Mentor sends. If Mentor's experiment program is flawed, Fellow will faithfully optimize the wrong thing.
