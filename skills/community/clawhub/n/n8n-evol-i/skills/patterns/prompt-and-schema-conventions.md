---
name: pattern-prompt-and-schema-conventions
description: File naming and injection syntax for the harness's prompt + schema infrastructure.
user-invocable: false
---

# Pattern: prompt + schema conventions

The harness centralizes LLM prompt + structured-output schema files under `<workspace>/n8n-prompts/`.

## File layout

```text
n8n-prompts/
  prompts/
    <name>_prompt.txt              # the prompt body
    <name>_schema.json             # JSON schema for the structured output
    <name>_prompt_optimized.txt    # optimized variant from iterate-prompt --export
  datasets/
    <name>.json                    # [{input, expected}, ...] for evaluation
  evals/
    <name>_eval.py                 # optional custom evaluation harness
```

## Injection syntax

In a workflow template, inject the prompt + schema with placeholders:

```json
{
  "type": "n8n-nodes-base.openAi",
  "parameters": {
    "messages": {
      "values": [
        {"role": "system", "content": "{{@txt:n8n-prompts/prompts/summary_prompt.txt}}"}
      ]
    },
    "options": {
      "responseFormat": "json_object",
      "jsonSchema": "{{@json:n8n-prompts/prompts/summary_schema.json}}"
    }
  }
}
```

`{{@txt:...}}` inlines text. `{{@json:...}}` inlines a JSON-stringified version (so it embeds correctly in another JSON value).

## Schema shape

Use a standard JSON Schema with `type: object`, `properties`, `required`, and `additionalProperties: false` for n8n / OpenAI structured outputs:

```json
{
  "type": "object",
  "properties": {
    "title": {"type": "string"},
    "summary": {"type": "string"}
  },
  "required": ["title", "summary"],
  "additionalProperties": false
}
```

## Optimization

`iterate-prompt.md` exports an optimized variant to `<name>_prompt_optimized.txt`. Templates can inject the optimized version once you're happy with it (just change the placeholder filename in the template).

## Seed examples

`${CLAUDE_PLUGIN_ROOT}/primitives/prompts/example_summary_prompt.txt` and `example_summary_schema.json` show the canonical pair shape. Copy + adapt.
