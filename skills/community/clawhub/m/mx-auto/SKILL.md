---
name: mx-auto
description: Local Runtime automation entrypoint for App triggers, read-only browser sandbox inspection, and local script execution. Use when the user wants to list or run Runtime triggers, inspect existing browser sandbox tabs/snapshots, or list/show/run local App scripts.
---

# mx-auto

Use this skill as a lightweight router for local Runtime automation.

## Capabilities

- **Triggers**: list and run callable App triggers.
  - Read [references/triggers.md](references/triggers.md) when the user asks to list, refresh, inspect, or run triggers.
- **Sandbox**: list existing browser sandbox tabs or snapshot an existing tab.
  - Read [references/sandbox.md](references/sandbox.md) when the user asks about browser sandbox tabs, target IDs, snapshots, dashboard text, or URL-matched tab inspection.
- **Scripts**: list, show, or run local scripts/examples.
  - Read [references/scripts.md](references/scripts.md) when the user asks to list scripts, inspect a script schema, or run a script directly.
- For complex mixed requests, read [references/learning-guide.md](references/learning-guide.md).

## Shared Runtime Defaults

Preferences file:

`$OPENCLAW_STATE_DIR/skill-state/mx-auto/preferences.json`

Fallback:

`$HOME/.openclaw/skill-state/mx-auto/preferences.json`

Helper:

```bash
bash {baseDir}/scripts/export_preference.sh show
bash {baseDir}/scripts/export_preference.sh apply-recommended
bash {baseDir}/scripts/export_preference.sh set-key defaultAppHome "/Users/zhym/Library/Application Support/rpa-app-executor"
```

Runtime base URL discovery:

1. `MX_APP_RUNTIME_BASE_URL`
2. `RPA_RUNTIME_BASE_URL`
3. stored `defaultLocalBaseUrl`
4. standard Runtime ports: `8877`, `8878`, `8879`

Runtime app home discovery:

1. `--app-home`
2. `MX_AUTO_APP_HOME`
3. `RPA_APP_HOME`
4. stored `defaultAppHome`
5. platform default app home

Runtime admin token discovery:

1. `MX_APP_RUNTIME_ADMIN_TOKEN`
2. `RPA_RUNTIME_ADMIN_TOKEN`
3. `{resolved app home}/runtime/admin-token.json`

Never store or print the Runtime admin token value. App updates may rotate or recreate it; re-read the token file at runtime.

## Entry Points

Prefer the wrapper:

```bash
bash {baseDir}/scripts/run.sh ...
```

Triggers:

```bash
bash {baseDir}/scripts/run.sh triggers list --format json
bash {baseDir}/scripts/run.sh triggers run --trigger-name "小红书测试"
```

Sandbox:

```bash
bash {baseDir}/scripts/run.sh sandbox tabs --format json
bash {baseDir}/scripts/run.sh sandbox snapshot --url-contains dashboardV4 --url-not-contains /review
```

Scripts:

```bash
bash {baseDir}/scripts/run.sh scripts list --format json
bash {baseDir}/scripts/run.sh scripts show xiaohongshu.note.search.v1.json --format json
bash {baseDir}/scripts/run.sh scripts run xiaohongshu.note.search.v1.json --input-json '{"keyword":"美食探店"}' --wait true --format json
```

Legacy trigger commands remain supported:

```bash
bash {baseDir}/scripts/run.sh --list-triggers
bash {baseDir}/scripts/run.sh --trigger-name "小红书测试"
```
