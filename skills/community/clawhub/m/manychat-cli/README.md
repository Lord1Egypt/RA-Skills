# ManyChat CLI (Agent-Friendly)

A lightweight CLI wrapper around the ManyChat API for OpenClaw and other AI agents.

## Why this exists
- Consistent JSON output (`{"ok": true|false, ...}`)
- Explicit, automation-safe exit codes
- Prebuilt commands for common automation actions
- `raw` passthrough for any endpoint not yet wrapped
- `playbook-run` for multi-step automations in JSON

## File
- `/Users/danielfoch/manychat-cli/manychat_cli.py`

## Requirements
- Python 3.9+
- A ManyChat API key

## Setup
```bash
cd /Users/danielfoch/manychat-cli
export MANYCHAT_API_KEY='your-manychat-api-key'
./manychat_cli.py ping --pretty
```

Optional:
```bash
export MANYCHAT_BASE_URL='https://api.manychat.com'
```

## Commands
```bash
./manychat_cli.py --help
```

Core commands:
- `ping` -> `/fb/page/getInfo`
- `page-tags` -> `/fb/page/getTags`
- `page-fields` -> `/fb/page/getCustomFields`
- `page-flows` -> `/fb/page/getFlows`
- `sub-info` -> `/fb/subscriber/getInfo`
- `find-system` -> `/fb/subscriber/findBySystemField`
- `find-custom` -> `/fb/subscriber/findByCustomField`
- `tag-add` / `tag-remove`
- `field-set` / `fields-set`
- `flow-send` -> `/fb/sending/sendFlow`
- `content-send` -> `/fb/sending/sendContent`
- `sub-create` / `sub-update`
- `playbook-run` (multi-step automation runner)
- `raw` (generic endpoint caller)

## Examples
Find subscriber by email:
```bash
./manychat_cli.py find-system --field-name email --field-value 'lead@example.com' --pretty
```

Add tag by name:
```bash
./manychat_cli.py tag-add --subscriber-id 123456 --tag-name 'Hot Lead' --pretty
```

Set custom field by id:
```bash
./manychat_cli.py field-set --subscriber-id 123456 --field-id 789 --value 'Toronto' --pretty
```

Send flow:
```bash
./manychat_cli.py flow-send --subscriber-id 123456 --flow-ns 'main_onboarding' --pretty
```

Call any endpoint directly:
```bash
./manychat_cli.py raw /fb/page/getTags --data '{}' --pretty
```

Run playbook:
```bash
./manychat_cli.py playbook-run \
  --file /Users/danielfoch/manychat-cli/sample_playbook.json \
  --vars-json '{"email":"lead@example.com"}' \
  --pretty
```

## Playbook format
A playbook JSON file contains `steps`.
Each step supports:
- `id` (optional; default `stepN`)
- `endpoint` (required)
- `payload` (optional; defaults to `{}`)

Template variables in payload use `{{...}}`:
- `{{vars.some_key}}` from `--vars-json`
- `{{results.step_id.path}}` from earlier API responses

Example reference file:
- `/Users/danielfoch/manychat-cli/sample_playbook.json`

## Agent usage pattern (OpenClaw / other AI)
Use the CLI as the API execution layer:
1. Resolve subscriber(s) with `find-system` or `find-custom`
2. Apply tags/fields (`tag-add`, `field-set`, `fields-set`)
3. Trigger messaging (`flow-send` or `content-send`)
4. Parse machine-safe JSON from stdout
5. Use exit codes for branching logic

## Exit codes
- `0` success
- `2` expected input/API error (validation, HTTP error, bad JSON)
- `1` unexpected runtime error

## Notes
- This CLI intentionally does not hide raw API responses.
- For unsupported or newly released endpoints, use `raw` immediately.
