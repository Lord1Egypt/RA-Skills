# Operations

Run commands from the repo root.

## Runtime layout

MAL-Updater keeps runtime state outside the skill tree under `.MAL-Updater/` by default.

Because this repository is public, only external runtime state may contain operator-specific secrets or machine-local residue. Anything tracked in git must stay anonymized and safe to publish.

MAL-Updater runtime state lives under:

- `.MAL-Updater/config/`
- `.MAL-Updater/secrets/`
- `.MAL-Updater/data/`
- `.MAL-Updater/state/`
- `.MAL-Updater/cache/`

Use `bootstrap-audit` or `status` to see the resolved paths for the current install.

## First-line inspection

```bash
cd <repo-root>
PYTHONPATH=src python3 -m mal_updater.cli bootstrap-audit
PYTHONPATH=src python3 -m mal_updater.cli bootstrap-audit --summary
PYTHONPATH=src python3 -m mal_updater.cli status
PYTHONPATH=src python3 -m mal_updater.cli service-status
PYTHONPATH=src python3 -m mal_updater.cli service-status --format summary
PYTHONPATH=src python3 -m mal_updater.cli health-check
PYTHONPATH=src python3 -m mal_updater.cli health-check --format summary
```

## Initialize runtime / DB

```bash
cd <repo-root>
PYTHONPATH=src python3 -m mal_updater.cli init
```

## MAL auth

```bash
cd <repo-root>
PYTHONPATH=src python3 -m mal_updater.cli mal-auth-url
PYTHONPATH=src python3 -m mal_updater.cli mal-auth-login
PYTHONPATH=src python3 -m mal_updater.cli mal-refresh
PYTHONPATH=src python3 -m mal_updater.cli mal-whoami
```

## Crunchyroll auth / fetch

```bash
cd <repo-root>
PYTHONPATH=src python3 -m mal_updater.cli crunchyroll-auth-login
PYTHONPATH=src python3 -m mal_updater.cli crunchyroll-fetch-snapshot --out .MAL-Updater/cache/live-crunchyroll-snapshot.json
PYTHONPATH=src python3 -m mal_updater.cli crunchyroll-fetch-snapshot --out .MAL-Updater/cache/live-crunchyroll-snapshot.json --ingest
PYTHONPATH=src python3 -m mal_updater.cli crunchyroll-fetch-snapshot --out .MAL-Updater/cache/live-crunchyroll-snapshot.json --full-refresh
```

## Review / sync

```bash
cd <repo-root>
PYTHONPATH=src python3 -m mal_updater.cli review-mappings --limit 20 --mapping-limit 5 --persist-review-queue
PYTHONPATH=src python3 -m mal_updater.cli list-review-queue --summary --issue-type mapping_review
PYTHONPATH=src python3 -m mal_updater.cli dry-run-sync --limit 20 --approved-mappings-only
PYTHONPATH=src python3 -m mal_updater.cli apply-sync --limit 0 --exact-approved-only --execute
```

## User-systemd daemon

```bash
cd <repo-root>
scripts/install_user_systemd_units.sh
PYTHONPATH=src python3 -m mal_updater.cli install-service
PYTHONPATH=src python3 -m mal_updater.cli service-status
PYTHONPATH=src python3 -m mal_updater.cli service-status --format summary
PYTHONPATH=src python3 -m mal_updater.cli restart-service
PYTHONPATH=src python3 -m mal_updater.cli service-run-once
```

The installer renders the host-specific `mal-updater.service` from the repo template under `ops/systemd-user/`.

## MAL redirect configuration

Use the redirect URI reported by:

```bash
cd <repo-root>
PYTHONPATH=src python3 -m mal_updater.cli status
```

Specifically use the `mal.redirect_uri` value when creating/configuring the MAL app.

## Issue reporting / feedback

If MAL-Updater misbehaves during real usage — whether in the OpenClaw skill flow or the Python back-end daemon/runtime — report it upstream via:

- <https://github.com/kklouzal/MAL-Updater/issues>

Use GitHub issues for bugs, regressions, portability problems, onboarding friction, and feature requests so upstream maintenance stays informed by real-world usage.

## Tests

```bash
cd <repo-root>
PYTHONPATH=src python3 -m unittest discover -s tests -v
```
