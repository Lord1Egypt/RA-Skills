# Report Templates

Use the user's language. Keep benchmark descriptions short, concrete, and capability-focused.

## Template A — single-model strength and weakness report

Use for: `analyze model x`, `write a report on model x`, `what is this model good or bad at`.

```markdown
# [model] benchmark report

## scope and identity
- target model:
- normalized model row names searched:
- access date or time window:
- core dimensions covered:
- benchmark universe restriction: only benchmarks from the approved source document
- important exclusions:

## executive summary
[3-6 sentences summarizing the strongest dimensions, biggest gaps, and how confident the evidence is.]

## strengths by core dimension
### [dimension]
- finding:
- evidence:
- why it matters:

### [dimension]
- finding:
- evidence:
- why it matters:

## weaknesses or gaps
### [dimension]
- finding:
- evidence:
- why it matters:

## benchmark evidence table
| benchmark | what it tests | score | variant or split | time point | comparison note | warning |
| --- | --- | --- | --- | --- | --- | --- |

## anchor comparisons
- code or agentic coding:
- multimodal:
- intelligence or reasoning:

## predecessor comparison
- compared predecessor:
- where it improved:
- where gains are unclear:
- where no clean comparison was available:

## data-defect warnings and confidence
- inline warning summary:
- overall confidence: high / medium / low
- what most limits the conclusion:

## methodology and exclusions
- sources prioritized:
- benchmark variants intentionally excluded:
- any vendor-reported rows or image-extracted rows:
```

## Template B — domain leader report

Use for: `best models in coding`, `who leads in multimodal`, `top models for deep research`, `models that perform best in finance`.

```markdown
# [domain] benchmark leaders

## scope
- domain:
- core dimensions used:
- benchmark shortlist:
- access date or time window:
- benchmark universe restriction:

## executive summary
[Summarize the current leaders, the most important benchmark signals, and the major caveats.]

## current leaders
### frontier leaders
- [model]: [why it leads]
- [model]: [why it leads]

### specialized or workflow-specific leaders
- [model]: [what exact sub-task it leads]
- [model]: [what exact sub-task it leads]

## benchmark evidence table
| model | benchmark | what it tests | score | variant or split | time point | warning |
| --- | --- | --- | --- | --- | --- | --- |

## interpretation
- where the leaders agree across benchmarks:
- where the leaders split by sub-skill:
- which benchmark differences are not directly comparable:

## data-defect warnings and confidence
- warning summary:
- overall confidence:

## methodology and exclusions
- why these benchmarks were chosen:
- overlap benchmarks that changed the answer:
- excluded benchmarks and why:
```

## Template C — benchmark explainer or benchmark lookup

Use for: `what does benchmark x test`, `how should i read benchmark x`, `what score does model x have on benchmark x`.

```markdown
# [benchmark] explainer

## what it tests
[One short paragraph.]

## why it is relevant
[One short paragraph.]

## scoring notes
- main score:
- important sub-scores or splits:
- comparison traps:

## current lookup
- target model row:
- score:
- variant or split:
- time point:
- source note:

## data-defect warning
[Only if applicable.]
```

## Writing rules
- For every benchmark mention, include a short `what it tests` description.
- Prefer 5-12 words in the `what it tests` field.
- Put warnings close to the affected benchmark, not only in the appendix.
- Use dimension-level synthesis first; do not dump long benchmark lists unless the user explicitly asks for exhaustive coverage.
- If evidence is mixed, say which benchmarks disagree instead of flattening them into one verdict.
