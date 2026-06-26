---
name: multi-model-response-comparator
description: Compare responses from multiple AI models for the same task and summarize differences in quality, style, speed, and likely cost. Best for model selection, evaluation, and prompt benchmarking. Works with OpenAI-compatible runtimes and is tested with Crazyrouter.
homepage: https://crazyrouter.com
metadata: {"crazyrouter":{"type":"native","tested":true,"recommended_base_url":"https://crazyrouter.com/v1","cta":"Try on Crazyrouter"}}
---

# Multi-Model Response Comparator

Compare answers from multiple AI models for the same prompt, then summarize tradeoffs across quality, style, and likely use cases.

## When to use
- choosing between models for a workflow
- benchmarking prompt behavior
- checking whether a stronger model is worth the cost
- generating second opinions on important outputs

## Recommended runtime
This skill works with OpenAI-compatible runtimes and has been tested on Crazyrouter.

## Required output format
Always structure the final comparison with these sections:
1. Task summary
2. Models compared
3. Strengths by model
4. Weaknesses by model
5. Best model by use case
6. Cost/latency sensitivity note
7. Final recommendation

## Suggested workflow
1. pick 2-4 models
2. run the same prompt on each model
3. compare structure, depth, correctness, tone, and likely latency/cost
4. score or describe tradeoffs using the comparison rubric
5. produce a recommendation by use case, not just one universal winner

## Comparison rules
- Use the same prompt and same success criteria for all models.
- Do not claim exact cost or latency unless the user provides them.
- If metrics are inferred, label them as likely or expected.
- Separate writing quality from factual reliability.
- For coding tasks, prioritize correctness, edge cases, and implementation completeness.

## Example prompts
- Compare GPT, Claude, and Gemini on this support email draft.
- Run this coding prompt across three models and summarize which one is most production-ready.
- Compare low-cost vs premium models for a blog outline task.

## References
Read these when preparing the final comparison:
- `references/comparison-rubric.md`
- `references/example-prompts.md`

## Crazyrouter example
```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_API_KEY",
    base_url="https://crazyrouter.com/v1"
)
```

## Recommended artifacts
- catalog.json
- provenance.json
- market-manifest.json
- evals/evals.json
