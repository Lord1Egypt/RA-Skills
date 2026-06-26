# Prompt — Model Selection

## Purpose

Reusable prompt that guides an agent to select an appropriate, **runnable** Hugging Face model for a task before spending on inference.

## Reusable template

```text
Select a Hugging Face model for this task: {{task_description}}.

Constraints:
- Task type: {{task_type}}            # e.g. text-generation, feature-extraction
- Preferred size: {{size_preference}} # e.g. small/medium/any
- Language(s): {{languages}}
- License requirement: {{license_requirement}}  # e.g. permissive/commercial-ok/any

Steps:
1. Use hf_search_models (free) with filter "{{task_type}}", sorted by downloads, to list candidates.
2. Use hf_model_info (free) to check pipeline_tag and cardData.license for the top candidate.
3. Use hf_list_inference_models (free) to confirm the candidate is runnable via the router.
4. If not runnable, choose a listed model that best fits the constraints.

Output: the chosen model id, why it fits, its license, and confirmation it is runnable.
Do NOT call hf_chat or hf_embeddings yet. Do NOT expose the token.
```

## Variables

| Variable | Meaning |
|----------|---------|
| `{{task_description}}` | What the model must do. |
| `{{task_type}}` | Pipeline tag (text-generation, feature-extraction, ...). |
| `{{size_preference}}` | Size/cost preference. |
| `{{languages}}` | Required languages. |
| `{{license_requirement}}` | Acceptable license terms. |

## Example

```text
Select a Hugging Face model for this task: summarize support tickets.
Constraints: Task type: text-generation; Preferred size: small; Languages: English; License requirement: commercial-ok.
```

## Bad

```text
Use Llama to summarize this.
```

(No task type, no license check, no confirmation the model is runnable — risks `model_not_supported` and license violations.)

## Good

```text
Find a small, commercial-friendly text-generation model via hf_search_models,
verify its license with hf_model_info, confirm it appears in hf_list_inference_models,
then report the chosen model id and license. Do not run inference yet.
```
