# Known CLI Behavior

Use this file as the shared source of command-shape quirks across lemma skills.
Link here from specialized skills instead of re-documenting these rules everywhere.

## Payload Shape Rules

- `lemma function run` expects `--payload` with `input_data`.
- `lemma function update` payload is usually config-oriented, for example `{"config": {...}}`.
- prefer `--payload-file` for larger JSON payloads to avoid shell escaping drift.

Example:

```bash
lemma function run create-expense --pod-id <pod-id> \
  --payload '{"input_data":{"merchant":"Uber","amount":19.75}}'
```

## Command Naming Rules

- prefer flat Typer command names such as `workflow graph-update` and `workflow run-start`
- avoid legacy nested spellings such as `workflow graph update`

## Integration Operation Rules

- run `lemma integration operation get <app> <operation>` before writing payloads
- run a real `lemma integration operation execute ...` smoke test and save the response artifact before function coding

## Drift Control

- when a command shape changes, update this file first
- then link affected skill docs to the updated rule instead of duplicating one-off wording
