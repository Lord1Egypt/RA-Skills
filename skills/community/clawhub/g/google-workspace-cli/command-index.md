# Command Index - Google Workspace CLI

This file ensures users can reliably find any available command.

## Important

`gws` is dynamic: it builds resource/method commands from Google Discovery documents at runtime.
That means the source of truth is always live CLI introspection (`--help` + `schema`), not a static hardcoded list.

## Service Alias Inventory (from `src/services.rs`)

| Service alias | Alternate alias | API + version |
|---------------|-----------------|---------------|
| `drive` | - | `drive:v3` |
| `sheets` | - | `sheets:v4` |
| `gmail` | - | `gmail:v1` |
| `calendar` | - | `calendar:v3` |
| `admin` | `directory` | `admin:directory_v1` |
| `admin-reports` | `reports` | `admin:reports_v1` |
| `docs` | - | `docs:v1` |
| `slides` | - | `slides:v1` |
| `tasks` | - | `tasks:v1` |
| `people` | - | `people:v1` |
| `chat` | - | `chat:v1` |
| `vault` | - | `vault:v1` |
| `groupssettings` | - | `groupssettings:v1` |
| `reseller` | - | `reseller:v1` |
| `licensing` | - | `licensing:v1` |
| `apps-script` | `script` | `script:v1` |
| `classroom` | - | `classroom:v1` |
| `cloudidentity` | - | `cloudidentity:v1` |
| `alertcenter` | - | `alertcenter:v1beta1` |
| `forms` | - | `forms:v1` |
| `keep` | - | `keep:v1` |
| `meet` | - | `meet:v2` |
| `events` | - | `workspaceevents:v1` |
| `modelarmor` | - | `modelarmor:v1` |
| `workflow` | `wf` | synthetic workflow service |

## How to Find Any Command

1. List top-level syntax:
```bash
gws --help
```

2. List resources/method branches for one service:
```bash
gws <service> --help
```

3. Inspect required params/body for one method:
```bash
gws schema <service.resource.method>
```

4. Build final command with `--params` and optional `--json`:
```bash
gws <service> <resource> [sub-resource] <method> --params '{...}' --json '{...}'
```

## Exhaustive Service Sweep

Use this to quickly enumerate what exists right now in your installation:

```bash
for s in drive sheets gmail calendar admin admin-reports docs slides tasks people chat vault groupssettings reseller licensing apps-script classroom cloudidentity alertcenter forms keep meet events modelarmor workflow; do
  echo "===== $s ====="
  gws "$s" --help | sed -n '1,120p'
  echo
 done
```

## Helper and Workflow Discovery

For helper/workflow shortcuts (outside raw API branches):
- use the upstream generated index: `docs/skills.md` in `googleworkspace/cli`
- in local runtime, check `gws workflow --help`
- for MCP tools, start narrow and inspect exposed tools per service set

## Safety Reminder

Discovery first, dry-run second, apply last.
Do not execute write commands without resolving stable ids and getting explicit confirmation.
