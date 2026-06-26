# Python Worker

## Current model

The Python package under `src/mal_updater/` is the canonical implementation.

Use it from the repo root with:

```bash
PYTHONPATH=src python3 -m mal_updater.cli ...
```

## Runtime / daemon model

MAL-Updater now has a daemon-first unattended model.

The long-lived user-level service runs:

```bash
PYTHONPATH=src python3 -m mal_updater.cli --project-root <repo-root> service-run
```

Useful service-oriented commands:

```bash
PYTHONPATH=src python3 -m mal_updater.cli install-service
PYTHONPATH=src python3 -m mal_updater.cli service-status
PYTHONPATH=src python3 -m mal_updater.cli service-run-once
PYTHONPATH=src python3 -m mal_updater.cli restart-service
```

## Configuration model

Default runtime paths resolve under `.MAL-Updater/` in the workspace, not inside the repo tree.

The loader reads:
- `MAL_UPDATER_SETTINGS_PATH` when provided
- otherwise `.MAL-Updater/config/settings.toml`

`settings.toml` may override:
- runtime path layout
- MAL endpoint/bind/redirect settings
- request pacing
- secret file names
- daemon loop cadence / budget thresholds
- provider-specific hourly limits and warn/critical cooldown floors for budget pacing

Path values in `settings.toml` may be absolute or relative to the settings file location.

## Service runtime artifacts

Default daemon/runtime files under `.MAL-Updater/state/`:
- `logs/service.log`
- `service-state.json`
- `api-request-events.jsonl`
- `health/latest-health-check.json`

## Useful commands

```bash
PYTHONPATH=src python3 -m mal_updater.cli bootstrap-audit
PYTHONPATH=src python3 -m mal_updater.cli status
PYTHONPATH=src python3 -m mal_updater.cli service-status
PYTHONPATH=src python3 -m mal_updater.cli service-run-once
PYTHONPATH=src python3 -m mal_updater.cli health-check
PYTHONPATH=src python3 -m mal_updater.cli crunchyroll-auth-login
PYTHONPATH=src python3 -m mal_updater.cli crunchyroll-fetch-snapshot --out .MAL-Updater/cache/live-crunchyroll-snapshot.json --ingest
PYTHONPATH=src python3 -m mal_updater.cli review-mappings --limit 20 --mapping-limit 5 --persist-review-queue
PYTHONPATH=src python3 -m mal_updater.cli dry-run-sync --limit 20 --approved-mappings-only
PYTHONPATH=src python3 -m mal_updater.cli apply-sync --limit 0 --exact-approved-only --execute
```
