---
name: add-cloud-function
description: Scaffold a Python serverless function / cloud function / serverless API under <workspace>/cloud-functions/.
user-invocable: false
---

# add-cloud-function

> The terms **serverless function**, **cloud function**, and **serverless API** are used interchangeably here. Internally the harness calls them "cloud functions" because the directory is `cloud-functions/`; pick whichever name your team prefers.

## When

The user wants to add a Python function callable over HTTP from n8n nodes (HTTP Request node).

## How

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/helpers/add_cloud_function.py --name <name> [--platform railway|supabase|generic]
```

## Side effects

- Seeds `<workspace>/cloud-functions/{app.py,registry.py,requirements.txt}` if absent.
- Adds platform config (`railway.toml`, `railpack.json` for railway).
- Writes `<workspace>/cloud-functions/functions/<name>.py` from the `hello_world` seed.
- Wires the new function into `registry.py` (adds an import and an `EXPOSED_FUNCTIONS` entry).
- Writes a smoke test stub at `<workspace>/cloud-functions-tests/test_<name>.py`.

## Deployment

The user runs `railway up` (or equivalent) themselves — deploying cloud functions is out of scope for the harness.
