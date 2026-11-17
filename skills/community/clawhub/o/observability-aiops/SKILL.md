---
name: observability-aiops
slug: observability-aiops
displayName: "Observability AIops"
summary: "Governed Prometheus + Grafana ops: PromQL, alerts, dashboards, RCA; 39 tools."
license: MIT
homepage: https://github.com/AIops-tools/Observability-AIops
tags: [aiops, mcp, governance, observability]
description: >
  Use this skill whenever the user needs to operate a self-hosted observability stack on Prometheus (HTTP API + PromQL), Alertmanager, Grafana, or Grafana Loki (logs) — a one-shot overview, PromQL instant/range queries, label + series metadata, scrape-target health (up/down + why) and dropped targets, recording/alerting rule health, firing/pending alerts, Alertmanager alerts + silences, Grafana dashboards/datasources/folders, bounded Loki LogQL log reads (labels, query, error-tail), five flagship analyses (firing-alert RCA, target-scrape-health, alert-noise/flap, log-error-burst RCA, log-volume/cardinality) plus an alert->log cross-signal, and guarded writes (create/expire silence, create annotation, update/delete dashboard, reload Prometheus config).
  Always use this skill for "Prometheus", "PromQL", "Alertmanager", "Grafana", "Loki", "LogQL", "logs", "which targets are down", "scrape failing", "why is this alert firing", "root cause this alert", "firing alerts", "silence this alert", "noisy alerts", "alert flapping", "recording rule", "alerting rule", "dashboard", "datasource health", "reload prometheus config", "TSDB cardinality", "error burst", "log volume", "log cardinality", "tail errors" when the context is a self-hosted metrics/logs/observability stack.
  Do NOT use when the target is something other than a Prometheus/Grafana observability stack (a hypervisor, storage appliance, backup product, container-orchestrator control plane, network device config, or OT/industrial equipment) — route those to the appropriate other AIops-tools skill. Hosted/SaaS monitoring suites (Datadog, New Relic, enterprise NMS) are out of scope.
  Governed observability operations with a built-in governance harness (audit, policy, token budget, undo, risk-tiers). Beyond the mock suite, the Prometheus/Alertmanager/Grafana surfaces have been exercised against a live Prometheus 3.x + Alertmanager + Grafana 13 stack (RCAs, governed writes, undo); the Loki surface has not (see docs/VERIFICATION.md).
installer:
  kind: uv
  package: observability-aiops
argument-hint: "[a PromQL query, an alert/dashboard uid, or describe your observability task]"
allowed-tools:
  - Bash
metadata: {"openclaw":{"requires":{"anyBins":["observability-aiops","uvx"]},"optional":{"env":["OBSERVABILITY_AIOPS_CONFIG","OBSERVABILITY_AIOPS_MASTER_PASSWORD"]},"homepage":"https://github.com/AIops-tools/Observability-AIops","emoji":"📈","os":["macos","linux"]}}
compatibility: >
  Standalone, self-governed observability operations across Prometheus (HTTP API + PromQL, default port 9090, optional bearer token), a companion Alertmanager (/api/v2, default port 9093), Grafana (HTTP API, default port 3000, required bearer token), and Grafana Loki (HTTP API, default port 3100, optional bearer or basic auth, optional multi-tenant X-Scope-OrgID). Loki is READ-ONLY: bounded LogQL reads only (labels, label values, query_range with a hard lookback + line cap and a stream-selector gate, a canned error-tail), with no write surface. Each target in the config names its own platform, so one config can span the whole stack. The governance harness (audit, policy, token/runaway budget, undo, risk-tiers) is bundled in the package — no external skill-family dependency.
  All write operations are audited to a local SQLite DB under ~/.observability-aiops/ (relocatable via OBSERVABILITY_AIOPS_HOME).
  Credentials: the Grafana service-account/API token (required) or the Prometheus bearer token (optional; self-hosted Prometheus is often unauthenticated) is stored ENCRYPTED in ~/.observability-aiops/secrets.enc (Fernet/AES-128 + scrypt-derived key) — never plaintext on disk. Run 'observability-aiops init' to onboard (it asks for the platform), or 'observability-aiops secret set <target>' to add one. The store is unlocked by a master password from OBSERVABILITY_AIOPS_MASTER_PASSWORD (non-interactive/MCP/CI) or an interactive prompt (CLI on a TTY). A legacy plaintext env var OBSERVABILITY_<TARGET_NAME_UPPER>_TOKEN is still honoured as a fallback with a deprecation warning (migrate with 'observability-aiops secret migrate'). The token is sent as an Authorization: Bearer header and held only in memory; secrets are never logged or echoed.
  PromQL is used only through read endpoints (/api/v1/query, /query_range) — there is no write query path. State-changing operations pass through the @governed_tool decorator (budget guard + audit + risk-tier tagging). The destructive write (delete_dashboard) is high-risk with dry_run and captures the full prior dashboard model BEFORE deleting; reversible writes (update_dashboard, create_silence) capture the real fetched before-state and record an inverse undo descriptor. Silences are TIME-BOXED (create_silence requires a positive duration).
  Webhooks: none — no outbound network calls beyond the configured Prometheus / Alertmanager / Grafana endpoints.
  SSL: verify_ssl defaults to true; disable for self-signed lab certs.
  Transitive dependencies: httpx (HTTP client) and the MCP SDK. No post-install scripts or background services.
  Verification status: the Prometheus/Alertmanager/Grafana surfaces have been exercised against a live Prometheus 3.x + Alertmanager + Grafana 13 stack (reads, the three metric RCAs, silence + dashboard governed writes, and undo replay); the Loki surface is mock-only so far. Prometheus, Grafana and Loki are free/open-source (docker run prom/prometheus, grafana/grafana, grafana/loki) so a live 'doctor' check is easy. docs/VERIFICATION.md records what was and was not covered.
---

# Observability AIops

> **Audit availability:** Real writes require a durable audit intent. Reads and previews can continue if audit storage fails; check the warning and audit health before relying on their audit trail.

> **Disclaimer**: Community-maintained open-source project, **not affiliated with, endorsed by, or sponsored by the Prometheus or Grafana projects, Grafana Labs, or the CNCF.** Prometheus, Alertmanager and Grafana are trademarks of their respective owners. Source at [github.com/AIops-tools/Observability-AIops](https://github.com/AIops-tools/Observability-AIops) under the MIT license.

Governed self-hosted observability operations — **39 MCP tools** across
**Prometheus** (HTTP API + PromQL), **Alertmanager** (alerts + silences),
**Grafana** (dashboards, datasources, folders), and **Grafana Loki** (bounded
LogQL log reads + log RCA, read-only), every one wrapped with the bundled
`@governed_tool` harness: a local unified audit log under
`~/.observability-aiops/`, token/runaway budget guard, undo-token
recording, and descriptive risk-tier labels. One config can span the whole
stack. Bearer tokens are stored **encrypted** (`~/.observability-aiops/secrets.enc`,
Fernet + scrypt) — never plaintext on disk.

This is the **self-hosted-observability** complement to enterprise monitoring
suites: it speaks the open Prometheus/Grafana APIs an SRE actually runs.

> **Standalone**: the governance harness is bundled in the package
> (`observability_aiops.governance`) — no external skill-family dependency.
> Beyond the mock suite, the Prometheus/Alertmanager/Grafana surfaces have been
> exercised against a live Prometheus 3.x + Alertmanager + Grafana 13 stack; the Loki
> surface has not yet been exercised live (see `docs/VERIFICATION.md`).

## What This Skill Does

| Group | Platform | Tools | Count | R/W |
|-------|----------|-------|:-----:|:---:|
| **Metrics** | Prometheus | instant_query, range_query, label_values, series_metadata | 4 | read |
| **Targets & status** | Prometheus | list_targets, target_scrape_health, dropped_targets, prometheus_config_status, prometheus_tsdb_status | 5 | read |
| **Rules** | Prometheus | list_rules, rule_health | 2 | read |
| **Alerts** | Prometheus/Alertmanager | firing_alerts, pending_alerts, alertmanager_alerts, list_silences | 4 | read |
| **Grafana** | Grafana | list_dashboards, get_dashboard, list_datasources, datasource_health, list_folders | 5 | read |
| **Loki** | Loki | loki_labels, loki_label_values, loki_query, loki_tail_errors | 4 | read |
| **Overview + analyses** | all | observability_overview + firing_alert_rca, target_scrape_health_analysis, alert_noise_and_flap_analysis | 4 | read |
| **Log analyses + cross-signal** | Loki (+ Prometheus) | log_error_burst_rca, log_volume_analysis, alert_log_context | 3 | read |
| **Writes** | Alertmanager/Grafana/Prometheus | create_silence, expire_silence (med) · create_annotation (med) · update_dashboard (med) · delete_dashboard (**high**) · reload_prometheus_config (med) | 6 | write |

The three metric flagship analyses are transparent heuristics that report their
numbers: `firing_alert_rca` joins each firing alert to its rule expression and
maps it to a cause + action; `target_scrape_health_analysis` ranks down/erroring
scrape targets and classifies each `lastError`; `alert_noise_and_flap_analysis`
finds noisy/duplicate alerts and recommends a dedup/rollup. The two **log**
analyses mirror this: `log_error_burst_rca` compares per-stream error counts
against a baseline window and classifies each burst (new signature / volume spike
/ single-instance / no baseline when the baseline window had no logs at all); `log_volume_analysis` ranks the highest-volume streams and
warns on high-cardinality (high-churn) labels. `alert_log_context` bridges the two
signals — it maps a firing Prometheus alert's labels to a Loki stream selector and
pulls the correlated logs. **Loki is read-only** (no safe write surface).

## Quick Install

```bash
uv tool install observability-aiops
observability-aiops init       # wizard: pick platform (prometheus/grafana) + encrypted token
observability-aiops doctor
```

Or as an OpenClaw plugin, which installs this skill and its MCP server together:

```bash
openclaw plugins install clawhub:@zw008/observability-aiops
openclaw skills info observability-aiops          # expect: Visible to model: yes
```

Needs `uvx` on `PATH`: the MCP server is fetched with uv, pinned to this release.

## When to Use This Skill

- Get a snapshot (`overview` / `observability_overview`): firing-alert count,
  scrape targets up/down, rules erroring (Prometheus) or dashboard/datasource
  counts (Grafana)
- Run PromQL (`instant_query` / `range_query`), enumerate `label_values` or
  `series_metadata`
- Check scrape health (`target_scrape_health`, `dropped_targets`) and rule health
  (`rule_health`, `list_rules`)
- Triage alerts: `firing_alerts` / `pending_alerts`, the Alertmanager view
  (`alertmanager_alerts`, `list_silences`), then `firing_alert_rca` to root-cause
- Reduce alert noise (`alert_noise_and_flap_analysis`) → group_by / inhibition /
  longer `for`
- Grafana: `list_dashboards`, `get_dashboard`, `list_datasources`,
  `datasource_health`, `list_folders`
- Loki logs: enumerate `loki_labels` / `loki_label_values`, run a bounded
  `loki_query` (LogQL, stream selector required), `loki_tail_errors` for a
  selector; then `log_error_burst_rca` to root-cause an error burst and
  `log_volume_analysis` for volume/cardinality; `alert_log_context` to pull the
  logs behind a firing alert
- Governed writes: silence an alert (`create_silence`, time-boxed), annotate an
  event (`create_annotation`), update/delete a dashboard (`dry_run` first for
  either), or hot-reload Prometheus (`reload_prometheus_config`)

**Do NOT use when** the target is not a Prometheus/Grafana observability stack —
route hypervisor, storage, backup, container-orchestrator, network-device-config,
or OT/industrial work to the appropriate other AIops-tools skill. Hosted/SaaS
monitoring suites (Datadog, New Relic, enterprise NMS) are out of scope.

## Related Skills — Skill Routing

| If the user wants… | Use |
|--------------------|-----|
| Prometheus / Alertmanager / Grafana observability ops | **observability-aiops** (this skill) |
| A different platform (hypervisor, storage, backup, orchestrator, network config, OT edge) | the appropriate **other AIops-tools** skill |
| Hosted/SaaS monitoring (Datadog, New Relic, enterprise NMS) | out of scope for this tool |

## Common Workflows

> The CLI covers the reads and the three RCAs (`alert`, `query`, `logs`,
> `overview`); the guarded **writes** (silences, annotations, dashboards,
> config reload) are MCP tools — those steps name the tool rather than a CLI
> command.

### "Pager went off" — root-cause the firing alerts and time-box the noise

1. `observability-aiops overview` → one-shot stack picture: firing counts, target
   health, rule health — is this one alert or the whole stack?
2. `observability-aiops alert firing` → what is firing right now, grouped by
   severity
3. `observability-aiops alert rca` → each firing alert joined to its rule
   expression with a likely cause and a recommended action (advisory heuristic —
   verify it, do not act on it blind)
4. `observability-aiops query instant '<the rule expr>'` → evaluate the alert's
   own expression yourself and confirm the RCA's reading of it
5. `observability-aiops query range '<expr>' --start <rfc3339> --end <rfc3339> --step 60s`
   → see when it crossed the threshold, which usually names the change that
   caused it
6. Time-box the noise while you fix the cause: the `create_silence` MCP tool on a
   specific matcher (a positive duration is **required** — silences cannot be
   open-ended), then `observability-aiops alert silences` to confirm it landed
7. **Failure branch**: if the silence was too broad, `expire_silence` ends it
   immediately, or `observability-aiops undo apply <id>` replays the recorded
   inverse (`create_silence`'s undo is expire). If `alert rca` returns nothing
   while alerts are visibly firing, the alerts are coming from Alertmanager
   without a matching Prometheus rule — check `alertmanager_alerts` and
   `list_rules` rather than assuming the RCA is broken.

### Investigate a scrape gap ("metrics went missing")

1. `observability-aiops overview` → up/down target counts at a glance
2. `target_scrape_health` → the unhealthy targets with their raw `lastError`
3. `target_scrape_health_analysis` → down targets ranked, each `lastError`
   classified (connection refused / timeout / auth / DNS / TLS) with a concrete fix
4. `dropped_targets` → if a target is missing **entirely** rather than down, it
   was relabeled away; this is where that shows up
5. `observability-aiops query instant 'up{job="<job>"}'` → confirm the gap in the
   metric itself, not just in the target page
6. After fixing scrape config, `reload_prometheus_config` (a governed write) →
   then re-run `target_scrape_health` to confirm the target came back
7. **Failure branch**: if `reload_prometheus_config` succeeds but the target is
   still down, the config on disk was not what you thought — check
   `prometheus_config_status` for what Prometheus actually loaded. A reload with
   a broken config is rejected by Prometheus and leaves the old config running,
   so a failed reload is not an outage.

### Tame a noisy / flapping alert

1. `observability-aiops alert firing` → the volume of what is firing
2. `alert_noise_and_flap_analysis` → alertnames with many instances or exact
   duplicates, each with a `group_by` / inhibition / longer-`for` recommendation
3. `list_rules` and `rule_health` → read the offending rule's current `for`
   duration and confirm it is evaluating cleanly
4. `observability-aiops query range '<rule expr>' --start <rfc3339> --end <rfc3339> --step 60s`
   → see the flapping in the data and pick a `for` window that actually covers it
5. `create_silence` for a time-boxed quiet period while the rule change ships;
   `observability-aiops alert silences` to confirm
6. **Failure branch**: silencing is a stopgap, not a fix — if the silence expires
   and the flapping returns, the rule threshold or `for` window is still wrong.
   Use `observability-aiops undo list` to see exactly which silences this tool
   created, so no stale silence quietly hides a real outage.

### Root-cause a log error burst (Loki, read-only)

1. `alert_log_context <alertname>` → the firing alert's labels mapped to a Loki
   stream selector plus the correlated error logs (or start from a selector directly)
2. `observability-aiops logs errors '{app="api"}' --hours 2 --limit 200` → tail
   the error-level lines for that stream
3. `log_error_burst_rca <selector>` → per-stream error counts against a baseline
   window, each burst classified (new signature / volume spike / single instance /
   no baseline)
4. `observability-aiops logs query '{app="api"} |= "timeout"' --hours 2` → confirm
   the specific signature the RCA named
5. `log_volume_analysis <selector>` → the highest-volume streams and any
   high-cardinality label driving a stream/index explosion
6. **Failure branch**: Loki here is **read-only and bounded** — queries require a
   stream selector and are capped by lookback and line count. A query rejected
   for a missing selector is the guard working, not a bug: narrow it with
   `observability-aiops logs labels` first. There is no write surface for Loki,
   so remediation happens in the emitting service, not through this tool.

### Safely change or retire a Grafana dashboard (reversible)

1. `list_dashboards` / `list_folders` → locate the dashboard and its folder
2. `get_dashboard <uid>` → confirm this is the right dashboard before touching it
3. `update_dashboard` with `dry_run=True` → preview; then for real — it fetches
   and stashes the **prior model** and records a restore undo
4. To retire one: `delete_dashboard <uid>` with `dry_run=True` first. Delete is
   `high` risk — the prior model is captured **before** the delete so the undo
   can recreate it; set `OBSERVABILITY_AUDIT_APPROVED_BY` (and
   `OBSERVABILITY_AUDIT_RATIONALE`) if you want that recorded on the audit row
5. `create_annotation` → mark the change on the timeline so the next responder
   can correlate a metric shift with this edit
6. **Failure branch**: wrong dashboard or a bad edit — `observability-aiops undo list`
   then `observability-aiops undo apply <id>` restores the captured prior model
   (or recreates a deleted dashboard from it). If the write fails outright, that
   is the connecting account's permissions (this tool does not gate it) — check
   the token's role before assuming `observability-aiops doctor` connectivity is
   at fault.

## Governance & Safety

The skill delivers reads and writes and records them; it does **not** decide whether a write is
permitted. That is your agent's judgement, or the permission of the account you connect it with
(give it a Grafana token with only Viewer scope, and a Prometheus/Alertmanager reached without the
admin/write API — writes then fail at the server). There is no read-only switch, policy file, or
approval gate.

- **Audit is the guarantee, and it is not bypassable.** Every operation — MCP and CLI alike — is
  logged to `~/.observability-aiops/audit.db` (relocatable via `OBSERVABILITY_AIOPS_HOME`): params,
  result, status, duration, and the risk tier. The CLI writes the same row the MCP path does.
- `OBSERVABILITY_AUDIT_APPROVED_BY` / `OBSERVABILITY_AUDIT_RATIONALE` are optional annotations
  recorded on the audit row (who/why); they are never required and never block.
- **Runaway guard** — a safety backstop, not authorization: the same call looped in a tight window
  trips a circuit breaker. Disable with `OBSERVABILITY_RUNAWAY_MAX=0`.
- Writes support `--dry-run` / `dry_run=True` and double confirmation at the CLI.
- Silences are **time-boxed** (require a positive duration). Reversible writes
  capture the real fetched before-state and record an inverse descriptor
  (create_silence→expire, update/delete dashboard→restore/recreate).

## References

- `references/capabilities.md` — full tool + platform + API-path reference
- `references/cli-reference.md` — CLI command reference
- `references/setup-guide.md` — onboarding, credentials, and connectivity
- `references/agent-guardrails.md` — running this with a smaller / local model:
  what the harness enforces for you, and a ready-made system prompt for the rest
