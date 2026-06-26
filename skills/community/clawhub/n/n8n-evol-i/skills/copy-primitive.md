---
name: copy-primitive
description: Copy a single primitive template (any) from the harness into the workspace. General-purpose; does not register in env YAMLs.
user-invocable: false
---

# copy-primitive

## When

You want to drop a single primitive template into your workspace WITHOUT going through `create-lock` (which bundles the lock pair + opt-ins and registers in env YAMLs). Common cases:

- Copying just `rate_limit_check` into a workspace that won't use locking.
- Copying a primitive into a brand-new workspace before bootstrap-env exists, so you can iterate on the template before deploy.
- Force-updating one primitive after a harness upgrade without touching the others.

For the lock pair specifically, prefer `create-lock.md` — it copies AND registers in every env YAML. Use this skill when you need finer control or when the bundled-flow doesn't fit.

## How

```bash
# List what's available
python3 ${CLAUDE_PLUGIN_ROOT}/helpers/copy_primitive.py --list

# Copy one primitive
python3 ${CLAUDE_PLUGIN_ROOT}/helpers/copy_primitive.py --name <primitive-key> [--force-overwrite]
```

Where `<primitive-key>` matches a file under `${CLAUDE_PLUGIN_ROOT}/primitives/workflows/` minus the `.template.json` extension. Currently shipped:

- `lock_acquisition`
- `lock_release`
- `error_handler_lock_cleanup`
- `rate_limit_check`

## Side effects

- Copies `${CLAUDE_PLUGIN_ROOT}/primitives/workflows/<key>.template.json` into `<workspace>/n8n-workflows-template/<key>.template.json`.
- Idempotent: skips if the destination exists, unless `--force-overwrite`. Without the flag, prints:
  ```
  WARNING: <key>.template.json already exists — re-run with --force-overwrite
  to update to the real Redis implementation.
  ```
- Does **NOT** register the primitive in env YAMLs. Run `create_workflow.py --no-template --key <name> --name "<Display Name>"` afterwards (or use `create_lock.py` for the lock pair).
- For lock primitives, prints a note recommending `create_lock.py` for end-to-end setup.

## Examples

```bash
# Drop the rate-limit primitive only
python3 ${CLAUDE_PLUGIN_ROOT}/helpers/copy_primitive.py --name rate_limit_check

# Force-update lock_acquisition after pulling a newer harness
python3 ${CLAUDE_PLUGIN_ROOT}/helpers/copy_primitive.py --name lock_acquisition --force-overwrite

# What's available?
python3 ${CLAUDE_PLUGIN_ROOT}/helpers/copy_primitive.py --list
```

## Pattern

See [`skills/patterns/locking.md`](patterns/locking.md) for what each lock-related primitive does internally and the token-fencing safety model. See [`skills/integrations/redis/lock-pattern.md`](integrations/redis/lock-pattern.md) for the actual node graphs and Redis key namespace.
