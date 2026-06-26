# Architecture

## Shape

MAL-Updater is a **skill-first repository**:

- `SKILL.md` at the repo root is the canonical skill entrypoint
- `src/mal_updater/` contains the Python application, CLI, daemon runtime, and service management code
- `references/` contains agent-facing bootstrap/operation references
- `scripts/` contains deterministic wrappers/install helpers
- `ops/systemd-user/` contains portable systemd templates
- `tests/` remains bundled for auditability

## Runtime boundary

Live runtime state is external to the repo tree by default and resolves under `.MAL-Updater/` in the workspace:

- `.MAL-Updater/config/`
- `.MAL-Updater/secrets/`
- `.MAL-Updater/data/`
- `.MAL-Updater/state/`
- `.MAL-Updater/cache/`

Notable daemon/runtime files inside the external state tree include:

- `.MAL-Updater/state/service-state.json`
- `.MAL-Updater/state/logs/service.log`
- `.MAL-Updater/state/api-request-events.jsonl`
- `.MAL-Updater/state/health/latest-health-check.json`

## Execution model

### CLI

Use the repo-local Python CLI for business logic and operator workflows.

### Daemon

The unattended model is a **long-lived user-level systemd daemon**.

The installed unit runs:

```bash
python3 -m mal_updater.cli --project-root <repo-root> service-run
```

That foreground daemon owns internal recurring lanes for:

- MAL token refresh
- exact-approved sync passes
- recurring health-check/report generation
- API request logging and budget-aware gating

### Transitional wrappers

The daemon currently still reuses:

- `scripts/run_exact_approved_sync_cycle.sh`
- `scripts/run_health_check_cycle.sh`

Those wrappers are subordinate helpers now, not the primary scheduling model.

## Bootstrap model

A new OpenClaw instance should be able to:

1. inspect this repo as a skill package
2. run `bootstrap-audit`
3. detect missing dependencies and user-provided inputs
4. guide the user through MAL app creation / redirect configuration
5. stage secrets into the external runtime tree
6. install the rendered long-lived user daemon when supported
7. verify daemon health via `service-status`, `service-run-once`, and `health-check`

## Guardrails

- keep sync conservative
- keep runtime out of the skill tree
- avoid host-specific assumptions in committed files
- preserve full-repo auditability for third parties
- prefer the daemon-first runtime model over ad-hoc timers or OpenClaw cron
- because this repo is public, keep all tracked artifacts anonymized: no personal identities, personal emails, host-specific absolute paths, private workspace references, real account identifiers, or real secrets in code/references/tests/history
