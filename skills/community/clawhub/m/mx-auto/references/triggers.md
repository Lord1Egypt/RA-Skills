# Trigger Workflow

Use this reference when listing, refreshing, or running App triggers.

## Commands

```bash
bash {baseDir}/scripts/run.sh triggers list
bash {baseDir}/scripts/run.sh triggers list --format json
bash {baseDir}/scripts/run.sh triggers run --trigger-name "小红书测试"
bash {baseDir}/scripts/run.sh triggers run --trigger-id trigger_xxx --input-json '{"keyword":"AI employee"}'
```

Legacy forms remain valid:

```bash
bash {baseDir}/scripts/run.sh --list-triggers
bash {baseDir}/scripts/run.sh --trigger-name "小红书测试"
```

## Runtime API

- Refresh catalog from `GET /trigger-services`.
- Execute through `POST /local/commands/send`.
- Command body:

```json
{
  "target": "trigger.execute",
  "payload": { "triggerId": "trigger_xxx", "input": {} },
  "wait": true,
  "leaseTtlMs": 60000
}
```

## Resolution

- Prefer exact `triggerName` for human requests.
- Resolve exact cached trigger name first, then explicit `triggerId`.
- Do not fuzzy-match names for execution.
- If name resolution fails, include cached candidate names when available.

## Snapshot

Cache only callable and available triggers:

- `id`
- `name`
- `summary`
- `status`
- `callable`
- `available`
- `lastRunAt`
- `updatedAt`

## Output

- Human list: count, names, status, useful summary.
- JSON list: `mode`, `sourceMode`, `loadedAt`, `registryPath`, `triggerCount`, `triggers[]`.
- Run result: `target`, `commandId`, `resultType`, final status, key result.
