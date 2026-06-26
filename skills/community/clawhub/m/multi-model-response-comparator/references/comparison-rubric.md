# Comparison Rubric

Use this rubric when comparing outputs from 2-4 models on the same prompt.

## Required output structure

1. Task summary
2. Models compared
3. Side-by-side strengths
4. Side-by-side weaknesses
5. Best model by use case
6. Cost/latency sensitivity note
7. Final recommendation

## Core dimensions

Score each model 1-5 on these dimensions when relevant:

- instruction following
- correctness / factual reliability
- completeness
- clarity / structure
- tone fit
- production readiness
- likely cost efficiency
- likely latency efficiency

## Decision heuristics

### Prefer the cheapest acceptable model when
- the task is repetitive
- errors are low-risk
- outputs are easy to review
- speed matters more than nuance

### Prefer the strongest model when
- correctness matters
- the task is high-stakes
- editing time is expensive
- outputs need deeper reasoning or stronger writing quality

### Recommend a split strategy when
- one low-cost model is good enough for drafts
- one premium model is better for final review
- different teams have different quality thresholds

## Comparison notes

- Do not claim exact latency/cost unless provided.
- If real metrics are unavailable, say "likely" or "expected".
- Distinguish writing quality from factual reliability.
- For coding tasks, emphasize correctness, edge cases, and implementation completeness.
- For marketing/writing tasks, emphasize clarity, tone control, and usefulness without fluff.
