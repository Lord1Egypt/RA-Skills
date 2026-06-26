---
name: mal-updater
description: Multi-provider anime → MyAnimeList sync and recommendations skill with guarded auth, review-queue triage, health checks, bootstrap auditing, and user-systemd daemon support. Currently supports Crunchyroll and HIDIVE as source providers. Use when installing, auditing, operating, or troubleshooting MAL-Updater on an OpenClaw host.
metadata: {"openclaw":{"emoji":"📺","homepage":"https://github.com/kklouzal/mal-updater","os":["linux"],"requires":{"anyBins":["python3","python"]},"primaryEnv":"MAL_UPDATER_MAL_CLIENT_ID"}}
---

# MAL-Updater

Treat `{baseDir}` as the skill root. This repository is the skill package.

## Core model

- Keep business logic in the repo-local Python CLI.
- Keep runtime state outside the skill tree under the workspace runtime root `.MAL-Updater/` unless the operator explicitly overrides paths.
- Do not assume host-specific absolute paths, IPs, or preexisting local copies under `~/.openclaw/workspace/skills/`.
- For new installs or portability audits, start with `bootstrap-audit` before doing any live auth or sync work.
- Prefer the long-lived **user-systemd daemon** over timers or OpenClaw cron for unattended operation.

## Bootstrap / onboarding workflow

1. `cd {baseDir}`
2. Run `PYTHONPATH=src python3 -m mal_updater.cli bootstrap-audit`
3. Read `{baseDir}/references/bootstrap-onboarding.md`
4. Use the audit output to:
   - verify required binaries
   - check whether provider-specific optional transport/runtime extras are missing
   - confirm the external runtime layout under `.MAL-Updater/`
   - identify which user-provided secrets/app settings are still missing for MAL and any enabled source providers
   - verify the secrets location is outside version control and suitable for restrictive local permissions
   - decide whether the repo-owned user-systemd daemon can be installed on this host
5. If bootstrap is incomplete, guide the user through the missing steps instead of pretending install is finished.
6. Prompt for provider credentials only when the workflow reaches that provider's bootstrap step; do not request Crunchyroll or HIDIVE secrets preemptively if the user has not chosen or enabled that provider yet.

## How to access backend data / operator surfaces

For the most common operator/data tasks, use the repo-local CLI from `{baseDir}`:

### Read-only inspection
- `PYTHONPATH=src python3 -m mal_updater.cli status`
- `PYTHONPATH=src python3 -m mal_updater.cli bootstrap-audit`
- `PYTHONPATH=src python3 -m mal_updater.cli service-status`
- `PYTHONPATH=src python3 -m mal_updater.cli service-run-once`
- `PYTHONPATH=src python3 -m mal_updater.cli health-check --format summary`

### Recommendations / recommendation-related data
- `PYTHONPATH=src python3 -m mal_updater.cli recommend --limit 20`
- `PYTHONPATH=src python3 -m mal_updater.cli recommend --limit 20 --flat`
- `PYTHONPATH=src python3 -m mal_updater.cli recommend-refresh-metadata`

### Review queue / mapping triage
- `PYTHONPATH=src python3 -m mal_updater.cli list-review-queue --summary`
- `PYTHONPATH=src python3 -m mal_updater.cli review-queue-next --issue-type mapping_review`
- `PYTHONPATH=src python3 -m mal_updater.cli review-queue-worklist --issue-type mapping_review --limit 5`
- `PYTHONPATH=src python3 -m mal_updater.cli list-mappings`

### Sync planning / guarded execution
- `PYTHONPATH=src python3 -m mal_updater.cli dry-run-sync --provider all --limit 20 --approved-mappings-only`
- `PYTHONPATH=src python3 -m mal_updater.cli apply-sync --limit 0 --exact-approved-only --execute`
- `PYTHONPATH=src python3 -m mal_updater.cli provider-fetch-snapshot --provider crunchyroll --out .MAL-Updater/cache/live-crunchyroll-snapshot.json --ingest`
- `PYTHONPATH=src python3 -m mal_updater.cli provider-fetch-snapshot --provider hidive --out .MAL-Updater/cache/live-hidive-snapshot.json --ingest`

## Operational workflow

Prefer read-only inspection before live writes.

Read-only first:
- `status`
- `bootstrap-audit`
- `health-check`
- `service-status`
- `service-run-once`
- `list-mappings`
- `list-review-queue --summary`
- `dry-run-sync`
- `recommend`

Treat these as state-changing:
- `mal-auth-login`
- `mal-refresh`
- `provider-auth-login --provider crunchyroll`
- `provider-auth-login --provider hidive`
- `provider-fetch-snapshot --provider <provider> --ingest`
- `apply-sync --execute`
- `scripts/install_user_systemd_units.sh`
- `install-service`
- `restart-service`

## High-value references

- Read `{baseDir}/references/bootstrap-onboarding.md` for install/onboarding/bootstrap expectations.
- Read `{baseDir}/references/cli-recipes.md` for copy/paste command patterns.
- Read `{baseDir}/references/data-surfaces.md` for a concise map of which backend commands expose recommendations, review-queue state, service/runtime state, and guarded sync surfaces.

## Guardrails

- Keep sync behavior conservative; do not invent broader write scope than the CLI already supports.
- Prefer `dry-run-sync` before `apply-sync --execute` unless the task explicitly asks for a live apply.
- Treat Crunchyroll auth/fetch instability as real residue; document it plainly.
- Treat staged provider credentials and long-lived tokens as sensitive local files; keep them out of version control and prefer restrictive local permissions.
- When a host cannot satisfy the unattended daemon path, say so clearly instead of silently skipping service setup.
- Recommend manual review before enabling unattended daemon operation on a host that matters.
- Keep outputs short and actionable: counts, blockers, next command, and whether user input is needed.
