# Prompt — Cost Control

## Purpose

Reusable prompt that constrains an agent to minimize billed inference while preserving quality.

## Reusable template

```text
Run this task with strict cost control: {{task_description}}.

Rules:
- Hub discovery (hf_search_models, hf_model_info, hf_search_datasets, hf_list_inference_models) is FREE — use it freely.
- Inference (hf_chat, hf_embeddings) is BILLED — minimize it.
- For chat: set max_tokens = {{max_tokens}}; prefer the smallest model that meets quality.
- For embeddings: send inputs as ONE batch array; never one call per item.
- Cache and reuse: do not re-embed unchanged text; do not re-run identical deterministic prompts.
- After each inference call, report the model id and the returned usage.

Budget intent: {{budget_intent}}   # e.g. "stay minimal", "quality over cost within reason"
Do NOT expose the token.
```

## Variables

| Variable | Meaning |
|----------|---------|
| `{{task_description}}` | The task to perform. |
| `{{max_tokens}}` | Upper bound for chat generation. |
| `{{budget_intent}}` | How aggressively to minimize cost. |

## Example

```text
Run this task with strict cost control: answer 5 FAQ questions.
Rules: max_tokens = 80; prefer a small model; batch nothing for chat but report usage each time.
Budget intent: stay minimal.
```

## Bad

```text
Embed each of these 500 documents one at a time and answer with no token limit.
```

(500 separate billed calls plus unbounded generation — expensive.)

## Good

```text
Embed all 500 documents in a single batched hf_embeddings call, cache the vectors,
and answer with hf_chat using a small model and max_tokens=80. Report usage.
```
