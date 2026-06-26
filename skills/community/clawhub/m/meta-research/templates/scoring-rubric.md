# Idea Scoring Rubric

Use this rubric during the Brainstorming phase to systematically evaluate candidate
research directions. Score each criterion 1-5, then compute the mean.

## FINER Criteria (1-5 each)

| Criterion   | 1 (Poor)                        | 3 (Adequate)                    | 5 (Excellent)                    |
|-------------|--------------------------------|--------------------------------|----------------------------------|
| Feasible    | No data/compute/skills exist   | Possible with significant effort | All resources available now       |
| Interesting | Only we would care             | Niche community interest        | Broad scientific or practical value |
| Novel       | Direct reimplementation        | Incremental over prior work     | Distinct new claim or evidence    |
| Ethical     | Unresolvable ethical issues    | Requires careful mitigation     | Clear ethics path, minimal risk   |
| Relevant    | Pure leaderboard chasing       | Advances a narrow subfield      | Advances understanding or practice |

## AI-Specific Criteria (1-5 each)

| Criterion      | 1 (Poor)                         | 3 (Adequate)                     | 5 (Excellent)                      |
|----------------|----------------------------------|----------------------------------|------------------------------------|
| Evaluable      | No clear metric or baseline      | Standard metric, weak baselines  | Clear metric + strong baselines + stopping rule |
| Reproducible   | Cannot share code/data/weights   | Partial release possible         | Full release: code + data + weights |
| Robust         | Only tested on one easy case     | Standard benchmarks only         | Hard cases, distribution shift, confounders tested |
| Risk Control   | No failure modes identified      | Some risks acknowledged          | Known failure modes + mitigation plan documented |

## Scoring Table Template

Copy and fill this table for each candidate idea:

```
| Idea | Feasible | Interesting | Novel | Ethical | Relevant | Evaluable | Reproducible | Robust | Risk-Ctrl | Mean |
|------|----------|-------------|-------|---------|----------|-----------|-------------|--------|-----------|------|
| #1   |          |             |       |         |          |           |             |        |           |      |
| #2   |          |             |       |         |          |           |             |        |           |      |
| #3   |          |             |       |         |          |           |             |        |           |      |
```

## Decision Rules

- **Mean ≥ 4.0**: Strong candidate — proceed to trajectory sketching and falsification
- **Mean 3.5-3.9**: Viable candidate — proceed but identify and mitigate weak areas
- **Mean 3.0-3.4**: Marginal — only pursue if no better alternatives exist
- **Mean < 3.0**: Reject — document reasoning and move on
- **Any criterion = 1**: Automatic flag — must be resolved before proceeding regardless of mean

## Disagreement Resolution

If multiple reviewers score an idea:
1. Compute individual means
2. Flag any criterion where scores differ by ≥ 2 points
3. Discuss flagged criteria explicitly
4. Re-score after discussion
5. Use the post-discussion scores as the final ranking
