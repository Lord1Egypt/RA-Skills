# Smoke Test

## Goal

Confirm that an OA-enabled OpenClaw workspace is minimally operational before public release or deeper UI work.

## Preconditions

- `oa` is installed and on `PATH`
- `config.yaml` exists in the target project
- the `openclaw_home` referenced by `config.yaml` is readable
- if API checks are required, `oa serve` is already running

## Recommended Run

```bash
bash scripts/oa_workspace_smoke_test.sh /path/to/oa-project 3456
```

## Pass Conditions

- `oa collect` exits successfully against the target config
- `/api/health` responds with HTTP 200 and includes `overall`
- `/api/goals` responds with HTTP 200 and includes at least one goal id
- `/api/team-health` responds with HTTP 200

## Notes

- This is a minimal operational smoke test, not a full product or release test.
- If the API server is not running, start it first through the workspace's preferred wrapper instead of inventing a new process model.
