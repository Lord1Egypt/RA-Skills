# Prompt — Model Selection

## Purpose

Help the agent (or a human) pick the cheapest OpenAI model that satisfies a task before making a billed call.

## Reusable template

```
Task: {{task_description}}
Quality bar: {{quality_bar}}   # e.g. "good enough", "publication quality", "must reason"
Input size: {{approx_input_tokens}} tokens
Output size: {{approx_output_tokens}} tokens
Budget sensitivity: {{budget_sensitivity}}   # low | medium | high

Choose the cheapest OpenAI model that meets the quality bar:
- Trivial classification/transform -> gpt-4.1-nano
- General chat/summarize/extract  -> gpt-4o-mini (default)
- Higher-quality writing/analysis -> gpt-4.1 or gpt-4o
- Hard multi-step reasoning        -> o4-mini, then o3
- Only if nothing else works       -> gpt-5
- Embeddings                       -> text-embedding-3-small (then -large)

Then set max_tokens/max_output_tokens to ~{{approx_output_tokens}} and justify the choice in one line.
```

## Variables

| Variable | Meaning |
|----------|---------|
| `{{task_description}}` | What the model must do. |
| `{{quality_bar}}` | Required output quality. |
| `{{approx_input_tokens}}` | Rough input size. |
| `{{approx_output_tokens}}` | Rough output size → token cap. |
| `{{budget_sensitivity}}` | How much cost matters. |

## Example

```
Task: classify support tickets into {billing, technical, other}
Quality bar: good enough
Input size: 150 tokens
Output size: 5 tokens
Budget sensitivity: high
-> Choose gpt-4.1-nano, max_tokens=5. Justification: trivial classification, high budget sensitivity.
```

## Bad

> "Use gpt-5 to classify these tickets." — Overkill; wastes money on a trivial task with no quality benefit.

## Good

> "Use gpt-4.1-nano with max_tokens=5 for ticket classification; escalate to gpt-4o-mini only if accuracy is poor."

> Verification needed: confirm model IDs with <https://platform.openai.com/docs/api-reference>.
