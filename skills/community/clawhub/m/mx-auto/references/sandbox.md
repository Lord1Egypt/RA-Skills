# Sandbox Workflow

Use this reference when inspecting existing browser sandbox tabs or snapshotting an existing tab.

## Rules

- Strictly read-only.
- Only list tabs or snapshot an existing target.
- Do not navigate.
- Do not create pages or tabs.
- Do not click, type, or mutate browser state.

## Commands

```bash
bash {baseDir}/scripts/run.sh sandbox tabs
bash {baseDir}/scripts/run.sh sandbox tabs --profile browser-1 --format json
bash {baseDir}/scripts/run.sh sandbox snapshot --target-id <targetId>
bash {baseDir}/scripts/run.sh sandbox snapshot --url-contains dashboardV4 --url-not-contains /review
```

## Runtime API

Call `POST /browser` with Runtime admin auth.

Tabs:

```json
{ "action": "tabs", "profile": "browser-1" }
```

Snapshot:

```json
{
  "action": "snapshot",
  "profile": "browser-1",
  "targetId": "<targetId>",
  "maxChars": 6000
}
```

## Target Resolution

- `--target-id` wins when present.
- Otherwise filter existing tabs by all `--url-contains` values and no `--url-not-contains` values.
- Zero matches is a clear no-match error.
- Multiple matches requires user disambiguation.

## Output

- Tabs: profile, tab count, targetId, title, URL.
- Snapshot: profile, targetId, matched URL, text snapshot or extracted content.
