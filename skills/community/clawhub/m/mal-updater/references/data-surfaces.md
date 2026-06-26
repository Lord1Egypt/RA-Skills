# Data surfaces / operator map

Use this file when the task is about *what backend data MAL-Updater exposes* and *which CLI surfaces to use*.

## Bootstrap / installation state

Use:

```bash
cd {baseDir}
PYTHONPATH=src python3 -m mal_updater.cli bootstrap-audit
PYTHONPATH=src python3 -m mal_updater.cli bootstrap-audit --summary
PYTHONPATH=src python3 -m mal_updater.cli status
```

These expose:
- resolved workspace/runtime paths
- dependency readiness
- credential/app-setup readiness
- daemon install readiness
- redirect URI / auth-material presence

## Daemon / unattended runtime state

Use:

```bash
cd {baseDir}
PYTHONPATH=src python3 -m mal_updater.cli service-status
PYTHONPATH=src python3 -m mal_updater.cli service-run-once
PYTHONPATH=src python3 -m mal_updater.cli health-check --format summary
```

These expose:
- service install/enable/active state
- one-pass daemon work execution
- health warnings and recommended remediation commands
- automation/runtime drift
- persisted task cadence/backoff details, including provider-floor cooldown provenance when budget pacing was extended on purpose

## Recommendations

Use:

```bash
cd {baseDir}
PYTHONPATH=src python3 -m mal_updater.cli recommend --limit 20
PYTHONPATH=src python3 -m mal_updater.cli recommend --limit 20 --flat
PYTHONPATH=src python3 -m mal_updater.cli recommend-refresh-metadata
```

Use this surface when the user wants:
- recommended anime to resume/watch next
- new season / dubbed-episode style recommendation output
- recommendation metadata refresh

## Review queue / mapping state

Use:

```bash
cd {baseDir}
PYTHONPATH=src python3 -m mal_updater.cli list-review-queue --summary
PYTHONPATH=src python3 -m mal_updater.cli review-queue-next --issue-type mapping_review
PYTHONPATH=src python3 -m mal_updater.cli review-queue-worklist --issue-type mapping_review --limit 5
PYTHONPATH=src python3 -m mal_updater.cli list-mappings
```

Use this surface when the user wants:
- mapping backlog state
- next recommended mapping-review slice
- grouped review worklists
- mapping inventory / approved coverage context

## Guarded sync state / execution

Use:

```bash
cd {baseDir}
PYTHONPATH=src python3 -m mal_updater.cli dry-run-sync --limit 20 --approved-mappings-only
PYTHONPATH=src python3 -m mal_updater.cli apply-sync --limit 0 --exact-approved-only --execute
PYTHONPATH=src python3 -m mal_updater.cli crunchyroll-fetch-snapshot --out .MAL-Updater/cache/live-crunchyroll-snapshot.json --ingest
```

Use this surface when the user wants:
- proposed MAL mutations before live writes
- exact-approved live apply behavior
- snapshot refresh / ingest state

## Auth surfaces

Use:

```bash
cd {baseDir}
PYTHONPATH=src python3 -m mal_updater.cli mal-auth-login
PYTHONPATH=src python3 -m mal_updater.cli mal-refresh
PYTHONPATH=src python3 -m mal_updater.cli crunchyroll-auth-login
```

Use this surface when the user wants:
- MAL OAuth bootstrap
- MAL token refresh
- Crunchyroll staged auth bootstrap

## General rule

Prefer the smallest read-only surface that answers the question before reaching for live auth, snapshot, or apply commands.
