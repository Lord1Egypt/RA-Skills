---
name: iterate-prompt
description: Optimize a prompt against a paired schema + dataset using DSPy.
user-invocable: false
---

# iterate-prompt

## When

A prompt under `n8n-prompts/prompts/` needs measurable improvement.

## Pre-call setup (the agent must do these)

1. Write the prompt body to `<workspace>/n8n-prompts/prompts/<name>_prompt.txt`.
2. Write the JSON output schema to `<workspace>/n8n-prompts/prompts/<name>_schema.json`.
3. Build a dataset of `[{input, expected}]` pairs at `<workspace>/n8n-prompts/datasets/<dataset>.json`.

The agent constructs the `dspy.Signature` subclass in-process at invocation time (the helper uses the schema's `properties` and `required` to wire DSPy's `InputField` / `OutputField` definitions).

## How

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/helpers/iterate_prompt.py --prompt <name> [--dataset <name>] [--optimizer miprov2|bootstrap] [--export]
```

## Side effects

- Loads the prompt, schema, and dataset.
- Configures DSPy via `OPENAI_API_KEY` / `OPENROUTER_API_KEY` / `ANTHROPIC_API_KEY`.
- Evaluates baseline, optimizes via the chosen optimizer, evaluates again.
- With `--export`, if the optimized score ≥ baseline, writes `<name>_prompt_optimized.txt` next to the prompt.

## Optional dep

DSPy is an optional extra. Install with `pip install n8n-evol-I[dspy]`. The helper prints an install hint if dspy is missing.
