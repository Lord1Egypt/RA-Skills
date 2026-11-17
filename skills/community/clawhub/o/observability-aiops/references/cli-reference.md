# observability-aiops CLI reference

> Covers Prometheus (HTTP API + PromQL), a companion Alertmanager, Grafana
> (HTTP API), and Grafana Loki (LogQL, read-only). The Prometheus/Alertmanager/
> Grafana surfaces have been exercised against a live Prometheus 3.x + Alertmanager + Grafana 13 stack;
> the Loki surface has not (see docs/VERIFICATION.md). The CLI is a convenience
> subset — the full 39-tool surface is via the MCP server
> (`observability-aiops mcp`).

## Setup & diagnostics

```bash
observability-aiops init                      # interactive wizard (asks for the platform: prometheus/grafana/loki)
observability-aiops doctor [--skip-auth]      # config + secret store + connectivity
                                           #   Prometheus: /api/v1/status/buildinfo · Grafana: /api/health
                                           #   Loki: /ready + /loki/api/v1/status/buildinfo
observability-aiops mcp                       # start the MCP server (stdio transport)
```

## Secrets (encrypted store ~/.observability-aiops/secrets.enc)

```bash
observability-aiops secret set <target> [--value <token>]   # store bearer token (hidden prompt if no --value)
observability-aiops secret list                             # names only — secrets never shown
observability-aiops secret rm <target>
observability-aiops secret migrate                          # import legacy plaintext env (OBSERVABILITY_<TARGET>_TOKEN)
observability-aiops secret rotate-password                  # re-encrypt under a new master password
```

## Overview

```bash
observability-aiops overview [--target <t>]   # snapshot: firing alerts + targets up/down + rules erroring (Prometheus)
                                           #   or dashboard/datasource/folder counts (Grafana) / label-name count (Loki)
```

## Query (Prometheus PromQL)

```bash
observability-aiops query instant 'up'                      # PromQL instant query
observability-aiops query range 'rate(x[5m])' --start ... --end ... [--step 60s]
observability-aiops query labels [__name__]                 # distinct label values (default = all metric names)
```

## Logs (Grafana Loki, read-only, bounded)

```bash
observability-aiops logs labels [--hours 1] [--target <t>]              # distinct Loki label names in the window
observability-aiops logs query '{app="api"} |= "error"' [--hours 1] [--limit 100]   # bounded LogQL (stream selector required)
observability-aiops logs errors '{app="api"}' [--hours 1] [--limit 100]  # canned error-level tail for a selector
```

## Alerts

```bash
observability-aiops alert firing [--target <t>]             # firing Prometheus rule alerts, by severity
observability-aiops alert silences [--target <t>]           # Alertmanager silences
observability-aiops alert rca [--target <t>]                # root-cause firing alerts (join to rule expr → cause+action)
```

## Common options

- `--target, -t <name>` — target name from `config.yaml` (omit to use the
  default/first target); each target declares its own `platform`
- `overview`, `query`, `logs`, and `alert` are the CLI subset; the remaining
  metrics, targets, rules, Grafana, Loki analyses (log_error_burst_rca,
  log_volume_analysis, alert_log_context), and governed-write tools
  (create/expire silence, create annotation, update/delete dashboard, reload
  config) are exposed through the MCP server. High-risk MCP writes honour `OBSERVABILITY_AUDIT_APPROVED_BY` /
  `OBSERVABILITY_AUDIT_RATIONALE` and support dry-run.
