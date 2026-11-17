# observability-aiops capability matrix

> **39 MCP tools** (32 read, 7 write) across Prometheus
> (HTTP API + PromQL, default port 9090, optional bearer token), a companion
> Alertmanager (`/api/v2`, port 9093), Grafana (HTTP API, port 3000, required
> bearer token), and Grafana Loki (HTTP API, port 3100, optional bearer/basic
> auth, optional multi-tenant `X-Scope-OrgID`). Loki is **read-only**. The
> Prometheus/Alertmanager/Grafana surfaces have been exercised against a live Prometheus 3.x + Alertmanager + Grafana 13 stack; the Loki surface has not
> (see docs/VERIFICATION.md).

## Metrics — Prometheus (read)

| Tool | API path | Returns |
|------|----------|---------|
| `instant_query` | `/api/v1/query` | PromQL evaluated at one instant (samples: metric + value + timestamp) |
| `range_query` | `/api/v1/query_range` | PromQL over a time range (per-series point arrays) |
| `label_values` | `/api/v1/label/<name>/values` | distinct values of a label (default `__name__` = all metric names) |
| `series_metadata` | `/api/v1/series` | series (label-set) metadata for a selector |

## Targets & status — Prometheus (read)

| Tool | API path | Returns |
|------|----------|---------|
| `list_targets` | `/api/v1/targets` | active scrape targets (job, instance, health, lastError), optional up/down filter |
| `target_scrape_health` | `/api/v1/targets` | up/down summary + the unhealthy targets |
| `dropped_targets` | `/api/v1/targets` | targets discovered but dropped by relabeling |
| `prometheus_config_status` | `/api/v1/status/config` | running-config fingerprint (sha256) + size — never the raw YAML/secrets |
| `prometheus_tsdb_status` | `/api/v1/status/tsdb` | TSDB head cardinality + top metrics by series count |

## Rules — Prometheus (read)

| Tool | API path | Returns |
|------|----------|---------|
| `list_rules` | `/api/v1/rules` | recording + alerting rules (name, type, expr, health), optional type filter |
| `rule_health` | `/api/v1/rules` | rule-evaluation health summary + erroring rules |

## Alerts — Prometheus + Alertmanager (read)

| Tool | API path | Returns |
|------|----------|---------|
| `firing_alerts` | `/api/v1/alerts` | firing Prometheus rule alerts, grouped by severity |
| `pending_alerts` | `/api/v1/alerts` | pending (not-yet-firing) rule alerts |
| `alertmanager_alerts` | AM `/api/v2/alerts` | alerts as Alertmanager sees them (post grouping/silence/inhibit) |
| `list_silences` | AM `/api/v2/silences` | silences (active, pending, expired) with matchers |

## Grafana (read)

| Tool | API path | Returns |
|------|----------|---------|
| `list_dashboards` | `/api/search?type=dash-db` | dashboards (uid, title, folder, tags), optional title query |
| `get_dashboard` | `/api/dashboards/uid/{uid}` | one dashboard's summary (title, version, panel + tag counts) |
| `list_datasources` | `/api/datasources` | datasources (id, uid, name, type, default flag) |
| `datasource_health` | `/api/datasources/{id}/health` | one datasource's health (status, message) |
| `list_folders` | `/api/folders` | Grafana folders |

## Loki — logs (read)

| Tool | API path | Returns |
|------|----------|---------|
| `loki_labels` | `/loki/api/v1/labels` | distinct label names in the lookback window |
| `loki_label_values` | `/loki/api/v1/label/<name>/values` | distinct values of one label (name percent-encoded) |
| `loki_query` | `/loki/api/v1/query_range` | bounded LogQL passthrough — **requires a stream selector**; lookback capped at `MAX_LOOKBACK_HOURS=24`, lines clamped to `MAX_LINE_LIMIT=1000` (default 100) |
| `loki_tail_errors` | `/loki/api/v1/query_range` | canned error-level read for a selector (line-filter on `(?i)(error\|fatal\|panic\|exception\|traceback\|stacktrace)`) |

Bounding gate: a LogQL query with **no `{…}` stream selector**, an empty query,
or a lookback beyond the cap is rejected up front with a teaching error — no
unbounded scan is ever issued. Label values interpolated into a selector are
backslash-escaped; label names in a path are percent-encoded. Loki auth is
optional (bearer or, per target, `basic` with a `user:password` secret) and a
multi-tenant `X-Scope-OrgID` header is sent when the target sets `org_id`.

## Overview & flagship analyses (read)

| Tool | Inputs | Returns |
|------|--------|---------|
| `observability_overview` | platform-aware | Prometheus: firing count + targets up/down + rules erroring; Grafana: dashboard/datasource/folder counts; Loki: label-name count |
| `firing_alert_rca` | firing alerts + alerting rules | each firing alert joined to its rule expr, ranked by severity, mapped to a likely **cause + action** |
| `target_scrape_health_analysis` | active targets | down/erroring scrapes ranked, each `lastError` classified (refused/timeout/auth/DNS/TLS) with a fix |
| `alert_noise_and_flap_analysis` | alert instances | alertnames with many instances / exact duplicates flagged with a group_by / inhibition / longer-`for` recommendation |

## Loki — log analyses & cross-signal (read)

| Tool | Inputs | Returns |
|------|--------|---------|
| `log_error_burst_rca` | selector + window (pulls current + baseline error streams) | per-stream error counts vs a baseline window; each burst classified **new_signature** (baseline 0), **volume_spike** (>= `burst_ratio`×baseline), or **single_instance** (localized to one pod/instance), or **no_baseline** (the baseline window had no logs at all — measured with a total-volume probe — so "new" cannot be told from "always there"; `baselineReadable`, `baselineLogLines`) with a cause + action + sample lines |
| `log_volume_analysis` | selector + window (pulls streams + `index/stats`) | top streams by line volume, high-cardinality (high-churn) label warnings, and a retention hint from total ingest bytes |
| `alert_log_context` | firing alertname (Prometheus) + Loki target | maps the alert's labels → a Loki stream selector (intersect with namespace/job/service/app/container/pod/instance/component, first 4 in priority order; values escaped) and returns the correlated error streams. **Best-effort**: only labels the alert and Loki share will match |

## Undo (read)

| Tool | Inputs | Returns |
|------|--------|---------|
| `undo_list` | local undo store (`limit`) | recorded, not-yet-applied reversible writes: undoId, ts, originalTool, inverseTool, note |

## Writes (governed)

| Tool | Risk | API path | Notes |
|------|------|----------|-------|
| `create_silence` | **med** | AM `POST /api/v2/silences` | **time-boxed** (requires minutes > 0); returns silenceId; undo → `expire_silence` |
| `expire_silence` | **med** | AM `DELETE /api/v2/silence/{id}` | inverse of create_silence |
| `create_annotation` | **medium** | `POST /api/annotations` | Grafana event marker |
| `update_dashboard` | **med** | `POST /api/dashboards/db` | GETs the prior model first → captures it for a restore undo |
| `delete_dashboard` | **HIGH** | `DELETE /api/dashboards/uid/{uid}` | `dry_run`; captures prior model **BEFORE** delete; undo → recreate |
| `reload_prometheus_config` | **med** | `POST /-/reload` | records the pre-reload config hash; no undo (re-apply the prior config file) |
| `undo_apply` | **med** | dispatches the recorded inverse tool | executes a recorded inverse; the inverse runs through its own governed tool (its real risk tier applies); single-use token; supports `dry_run` |

**No Loki writes.** Loki exposes no safe operational write surface here (no
silence/annotation analogue), so this tool ships Loki as read-only by design.

## Out of scope (by design)

- **Hosted/SaaS monitoring** — Datadog, New Relic, and enterprise NMS (only
  self-hosted Prometheus + Grafana + Loki here)
- **Loki writes / ingestion / deletes** — read-only LogQL only (no push, no
  delete-series, no ruler/config writes)
- **Creating/editing Prometheus rules or scrape config**, and provisioning
  Grafana datasources/dashboards from scratch (beyond update/delete of an existing
  dashboard)
- **Long-term-storage query fan-out** (Thanos/Cortex/Mimir) — the single
  Prometheus HTTP API only
