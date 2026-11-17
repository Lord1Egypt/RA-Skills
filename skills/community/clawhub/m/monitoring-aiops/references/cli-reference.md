# monitoring-aiops CLI reference

> Covers SolarWinds Orion (SWIS REST + SWQL), Paessler
> PRTG (web API), and Zabbix 6.x/7.x (JSON-RPC); SWIS/PRTG/Zabbix responses are
> mocked and need live verification.
> The CLI is a convenience subset — the full 42-tool surface is via the MCP
> server (`monitoring-aiops mcp`).

## Setup & diagnostics

```bash
monitoring-aiops init                      # interactive wizard (asks for the platform: solarwinds/prtg/zabbix)
monitoring-aiops doctor [--skip-auth]      # config + secret store + connectivity
                                           #   SolarWinds: a SWQL query · PRTG: /api/status.json
                                           #   Zabbix: apiinfo.version (no auth) + authed host count
monitoring-aiops mcp                       # start the MCP server (stdio transport)
```

## Secrets (encrypted store ~/.monitoring-aiops/secrets.enc)

```bash
monitoring-aiops secret set <target> [--value <secret>]  # store Orion password / PRTG or Zabbix token (hidden prompt if no --value)
monitoring-aiops secret list                             # names only — secrets never shown
monitoring-aiops secret rm <target>
monitoring-aiops secret migrate                          # import legacy plaintext env (MONITORING_<TARGET>_SECRET)
monitoring-aiops secret rotate-password                  # re-encrypt under a new master password
```

## Overview

```bash
monitoring-aiops overview [--target <t>]   # NOC summary: platform + active/unacked alert counts + top rollup
```

## SWQL (SolarWinds)

```bash
monitoring-aiops swql library                    # list the canned queries
monitoring-aiops swql canned <name>              # run a canned query: nodes_down, flapping_interfaces,
                                                 #   muted_report, high_cpu_nodes, volumes_full, unmanaged_scheduled
monitoring-aiops swql query "SELECT ..."         # validated read-only SWQL passthrough (SELECT only)
```

## Alerts (all platforms)

```bash
monitoring-aiops alert list [--target <t>]       # active alerts, deduped/rolled up by message
monitoring-aiops alert ack <alert_id>            # acknowledge an alert / PRTG alarm / Zabbix problem event
```

## Common options

- `--target, -t <name>` — target name from `config.yaml` (omit to use the
  default/first target); each target declares its own `platform`
- `overview`, `swql`, and `alert` are the CLI subset; the remaining SolarWinds
  health, PRTG, Zabbix, and governed-write tools (mute/unmute,
  schedule_maintenance, unmanage/remanage/remove node, PRTG pause/resume,
  Zabbix maintenance create/delete) are exposed through the MCP server.
  High-risk MCP writes use dry-run + double-confirm; `MONITORING_AUDIT_APPROVED_BY`
  / `MONITORING_AUDIT_RATIONALE` are recorded on the audit row when set.
