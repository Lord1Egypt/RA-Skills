# Automation

MAL-Updater now uses a **long-lived user-systemd daemon** rather than timer-driven one-shot jobs as the primary unattended model.

## Daemon model

The installed service runs:

```bash
python3 -m mal_updater.cli --project-root <repo-root> service-run
```

That foreground process owns its own internal loop cadence and recurring lanes for:

- MAL token refresh
- exact-approved sync passes
- recurring health-check/report generation
- API request logging / budget awareness

## User systemd install

Repo-owned templates live in `ops/systemd-user/`.

Install the daemon with:

```bash
cd <repo-root>
scripts/install_user_systemd_units.sh
```

Important:
- the committed `.service` file is a template, not a host-bound final unit
- the installer renders the current repo root and service env path into the installed copy
- this keeps the repo portable while still producing a valid host-specific user daemon

Useful variants:

```bash
scripts/install_user_systemd_units.sh --dry-run
scripts/install_user_systemd_units.sh --no-enable
scripts/install_user_systemd_units.sh --start-service
```

## Direct service commands

```bash
cd <repo-root>
PYTHONPATH=src python3 -m mal_updater.cli install-service
PYTHONPATH=src python3 -m mal_updater.cli service-status
PYTHONPATH=src python3 -m mal_updater.cli service-status --format summary
PYTHONPATH=src python3 -m mal_updater.cli restart-service
PYTHONPATH=src python3 -m mal_updater.cli service-run-once
```

`service-status` is now the main structured observability surface for unattended debugging. In addition to user-systemd enabled/active state, it reports:

- recent daemon loop timing (`last_loop_at`)
- per-lane task summaries from `service-state.json` (including last decision time plus last-run start/finish/duration when available)
- persisted budget backoff details, including whether a lane is cooling down at `warn` or `critical` level, whether the active cooldown policy came from task-level vs provider-level budget settings, and which learned projection source (configured / smoothed / percentile / auto-bursty percentile) the daemon is currently trusting for pre-run request budgeting
- persisted failure-backoff details for task errors, including retry countdown, last failure reason, and consecutive-failure streaks for auth-fragile provider lanes
- health-check-driven auth recovery hints: repeated auth-style provider fetch failures recorded in daemon state now surface as explicit re-bootstrap recommendations (`crunchyroll-auth-login` / `provider-auth-login --provider hidive`) instead of only opaque backoff residue
- health-driven full-refresh escalation: when the latest `latest-health-check.json` artifact recommends `refresh_full_snapshot` for a provider, the next unattended provider fetch lane upgrades itself to `--full-refresh` once so partial-coverage residue is repaired without waiting for the periodic cadence window
- current API-usage snapshot when available
- recent `service.log` tail lines
- parsed `latest-health-check.json` state (or parse errors when the artifact is malformed)
- a terse `service-status --format summary` view for quick operator checks and log-friendly output

## Legacy wrappers still reused by the daemon

The daemon currently reuses these guarded wrapper scripts for some lanes:

- `scripts/run_exact_approved_sync_cycle.sh`
- `scripts/run_health_check_cycle.sh`

Those still write runtime artifacts under `.MAL-Updater/state/` and `.MAL-Updater/cache/`, but they are now subordinate to the daemon-first orchestration model.

## Recommended bootstrap order

1. `bootstrap-audit`
2. `init`
3. MAL / Crunchyroll auth setup
4. `scripts/install_user_systemd_units.sh`
5. `service-status`
6. `service-run-once`
7. `health-check --format summary`

Do not claim unattended automation is installed or healthy until the installer, service-status, and health-check all agree.
