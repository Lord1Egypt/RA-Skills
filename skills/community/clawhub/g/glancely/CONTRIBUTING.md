# Contributing

## Adding a component

Use the scaffolder rather than hand-writing files:

```bash
python3 glancely/skills/scaffold_component/scripts/scaffold.py \
  --name <snake_case> --title "<Title>" \
  --field <name>:<type> [--field ...] \
  [--cron "<cron expr>" --notify "<text>"]
```

Field types: `int`, `float`, `text`, `bool`.

The new folder will already have a passing `tests/test_smoke.py`. Customize
`scripts/log.py` and `scripts/stats.py` from there.

## Tests

Each component owns its tests under `skills/<name>/tests/`. Run all tests:

```bash
python3 -m pytest glancely/
```

## Component contract

The dashboard, scaffolder, and migration runner all rely on one contract.
Read [`docs/component-contract.md`](docs/component-contract.md) before
changing anything in `core/`.

## Don't

- Don't add a central registry of components. The "drop a folder" property
  is load-bearing for the scaffolder.
- Don't ship a shared Google OAuth client.
- Don't add inter-component imports. Components must be independent so a
  user can disable any one of them by setting `panel.enabled = false` (or
  by deleting the folder).
