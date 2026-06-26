# CI/CD Pipelines and Jobs

Verified against `glab 1.90.0`.

## Inspecting Pipelines

```bash
glab ci list
glab ci list -s failed -F json
glab ci list -r main
glab ci status
glab ci status --branch=main
glab ci status --live
glab pipeline ci view
glab pipeline ci view -b main
glab ci view -p 123
```

`glab pipeline ci view` is the common alias shown in help examples. `glab ci view` is also supported.

## Working with Jobs

```bash
glab ci trace
glab ci trace lint
glab ci trace lint -p 123
glab ci retry
glab ci retry lint
glab ci retry lint -p 123
```

`glab ci retry` retries jobs, not whole pipelines.

## Running Pipelines

```bash
glab ci run
glab ci run -b main
glab ci run --mr
glab ci run -b main --variables DEPLOY_ENV:staging
glab ci run -b main --variables-env KEY1:val1 --variables-env KEY2:val2
glab ci run -b main --variables-file CONFIG_JSON:config.json
glab ci run -b main --variables-from variables.json
glab ci run -b main --input "replicas:int(3)" --input "debug:bool(false)"
```

Use the current flag names:

- `--variables` for inline values
- `--variables-env` for environment-style values
- `--variables-file KEY:file` for file variables
- `--variables-from file.json` for a JSON array of variable objects

Do not use `-V`.

## Canceling and Deleting

```bash
glab ci cancel pipeline 123
glab ci cancel job 456
glab ci delete 123 --dry-run
glab ci delete --older-than 24h --status=failed --dry-run
```

`glab ci cancel` requires a subcommand: `pipeline` or `job`.

## Common Failures

### `pipeline not found`

1. Check whether the branch already has a pipeline:

   ```bash
   glab ci list -r main
   glab ci status --branch=main
   ```

2. If needed, create one explicitly:

   ```bash
   glab ci run -b main
   ```

### Need One Specific Pipeline

Use the pipeline ID flag instead of passing the ID positionally:

```bash
glab ci view -p 123
glab ci trace lint -p 123
glab ci retry lint -p 123
```

### MR Blocked on Pipeline

```bash
glab ci status --live
glab pipeline ci view
glab mr merge 123 --auto-merge
```
