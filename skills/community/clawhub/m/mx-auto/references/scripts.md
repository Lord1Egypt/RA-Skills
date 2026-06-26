# Scripts Workflow

Use this reference when listing, showing, or running local App scripts/examples.

## Commands

```bash
bash {baseDir}/scripts/run.sh scripts list
bash {baseDir}/scripts/run.sh scripts list --format json
bash {baseDir}/scripts/run.sh scripts show xiaohongshu.note.search.v1.json --format json
bash {baseDir}/scripts/run.sh scripts run xiaohongshu.note.search.v1.json --input-json '{"keyword":"美食探店"}' --wait true --format json
```

## Runtime API

- List/show scripts from `GET /examples/catalog`.
- Run scripts through `POST /local/commands/send` with `target: "script.run"`.

Run body:

```json
{
  "target": "script.run",
  "payload": {
    "name": "xiaohongshu.note.search.v1.json",
    "inputOverrides": {}
  },
  "wait": true,
  "leaseTtlMs": 60000
}
```

## Resolution

- Run only exact script `name` matches.
- Do not fuzzy-match script names for execution.
- If no exact match exists, list candidate names from the current catalog.

## Input

- `--input-json` must be a JSON object.
- Pass it as `inputOverrides`.
- Do not invent required fields.
- If Runtime or script reports missing input, surface the error clearly.

## Output

- List: script count, name, platform label, runner.
- Show: manifest metadata and input schema.
- Run: preserve `target`, `commandId`, `resultType`, `status`, and message.
