# Prompt Templates

These prompts are optional reference material for higher-level agent flows. The Python router works without them. Use them only if you want the agent itself to generate richer summaries, reflections, or procedures around the deterministic storage and routing layer.

## `compose.txt`

Use when turning selected memories into a compact packet with an external reasoning step.

## `reflect.txt`

Use when deriving lessons from task outcomes with an external reasoning step.

## `procedure.txt`

Use when extracting reusable steps from a successful run with an external reasoning step.

## `refresh.txt`

Use when deciding whether older memories should be retired or contradicted with an external reasoning step.

The concrete templates live in:

- `scripts/prompts/compose.txt`
- `scripts/prompts/reflect.txt`
- `scripts/prompts/procedure.txt`
- `scripts/prompts/refresh.txt`
