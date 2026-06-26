# ModelPilot Benchmark Report

- Version: 1.5.0
- Generated at: 2026-06-08T00:00:00+00:00
- Local only: true
- Rounds requested: 2
- Prompt count: 5

## Summary

| Model | Decision | Reason | Success | Format | Think leak | Avg seconds |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| example-candidate-a:latest | replace_ready | Two rounds passed mechanical checks. Human semantic review is still required. | 10/10 | 10/10 | 0 | 3.42 |
| example-candidate-b:nothink | not_recommended | 1 outputs show possible thinking leakage. | 10/10 | 10/10 | 1 | 3.10 |

## Replacement Decision

- `example-candidate-a:latest` can be considered for replacement after manual semantic review.
- `example-candidate-b:nothink` should not be promoted into automated workflows until no-think output is clean.
- Keep the previous model and config available for rollback.

## Risks and Limits

- This example uses fictional data.
- Mechanical checks do not prove semantic quality.
- Do not delete old models based only on a benchmark report.

