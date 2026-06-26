---
name: create-new-workflow
description: Author a brand-new workflow — scaffold template + register IDs in env YAMLs + mint placeholder n8n workflow.
user-invocable: false
---

# create-new-workflow

## When

The user asks to create a new workflow.

## How

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/helpers/create_workflow.py --key <key> --name "<display name>" [--register-in <env1,env2,...>] [--with-error-handler <handler-key>] [--tier <tier-name>]
```

## Side effects

1. Writes `<workspace>/n8n-workflows-template/<key>.template.json` (a Webhook + Set seed).
2. Adds `workflows.<key>: { id: '', name: '<display name>' }` to every targeted env's YAML.
3. POSTs to each env's `/workflows` to mint a placeholder, captures the returned ID, writes it back to the YAML.
4. (Optional) Adds the key to `n8n-config/deployment_order.yml` under the requested tier.
5. (Optional) Calls `register_error_handler.py` to wire `settings.errorWorkflow`.

Idempotent: skips entries that already have a non-placeholder ID; n8n POST is skipped if the ID is already real.

## Next steps

- Edit the new template at `n8n-workflows-template/<key>.template.json` to add the actual nodes.
- `tidy-workflow.md` to clean up node positions after editing.
- `validate.md` to sanity-check.
- `deploy.md` to ship it.

### Code nodes

Any `n8n-nodes-base.code` node must follow `skills/patterns/code-node-discipline.md` — extract the pure function to `n8n-functions/{js,py}/<name>.{js,py}`, inject it via `{{@js:...}}` or `{{@py:...}}` in the Code-node body, and add a paired test under `n8n-functions-tests/`. The validator rejects inlined logic, missing tests, and the deprecated `n8n-nodes-base.function` type.
