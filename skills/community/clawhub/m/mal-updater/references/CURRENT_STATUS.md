# Current Status

## Repository / packaging state

- The repo is treated as the canonical skill package (`SKILL.md` at repo root).
- Runtime state is externalized to `.MAL-Updater/` by default instead of living under the repo tree.
- The bootstrap/onboarding surface starts with `bootstrap-audit`, which now exposes provider readiness, blocking vs non-blocking onboarding counts, and explicit recommended commands for automation-friendly consumers.
- Repo-owned systemd automation is committed as a portable `mal-updater.service` template and rendered at install time by `scripts/install_user_systemd_units.sh`.
- The unattended model is now user-level systemd **daemon-first**, with internal Python control loops rather than timer-driven one-shot jobs.
- Public-repo hygiene is now part of the project contract: tracked code/references/tests/history should remain anonymized and free of personal identifiers, host-local absolute paths, and real secrets.

## Working today

- Python worker/application exists
- SQLite bootstrap + migrations exist
- Crunchyroll auth bootstrap and live snapshot fetch exist
- MAL OAuth and guarded MAL apply exist
- mapping review / queue triage workflows exist
- exact-title split-bundle auto-resolution now covers conservative same-title TV suffix companions (for example `Title` + `Title (2009)`) when provider episode evidence cleanly fits the combined entry count and no stronger non-bundle rival remains
- long-lived daemon runtime + service manager exist
- service-status now exposes recent daemon loop/task state, API-usage snapshots, health snapshot parsing, and log-tail context for unattended debugging, plus a terse `--format summary` operator view for quick checks
- service task state now persists per-task cadence metadata (`every_seconds`), decision timing, last-run start/finish/duration, next-due timing, budget provider labels, budget backoff level (`warn` vs `critical`), adaptive failure backoff state, and active cooldown countdowns so unattended operators can see when a lane should run next vs when it is intentionally cooling down
- request-event logging / budget awareness scaffolding exists
- daemon budget skips now compute both warn-threshold pacing windows and hard critical recovery windows, persist per-task budget backoff state, and avoid re-check/log spam until the provider budget has room again
- service budget defaults are now provider-generic: non-MAL source lanes can inherit shared source-provider hourly/backoff/auth-failure defaults without being silently treated as Crunchyroll unless an explicit per-provider override exists
- daemon budget policy can now also be overridden per task/lane (`service.task_*` tables), with service state/status surfacing whether a cooldown came from task-level vs provider-level policy so MAL lanes like `sync_apply` no longer have to share one blunt provider-only budget posture
- the repo now ships built-in `sync_apply` task defaults for MAL hourly limit, projected request cost, learned-history depth, conservative learned p90 percentile, and warn/critical/auth-failure cooldown floors so fresh unattended installs inherit a conservative aggregate-apply posture without having to copy those numbers from example config first
- unattended `mal_refresh` now also ships a small explicit cold-start projected request cost plus a shallow learned-history window, so fresh installs no longer treat MAL token refresh as an unknown zero-cost lane before the daemon has seen one real run
- daemon budget gating is now modestly projection-aware: budgeted lanes persist observed request deltas, can optionally take explicit `service.task_projected_request_counts` overrides or fetch-mode-specific `service.task_projected_request_counts_by_mode` overrides, and will pre-emptively warn/skip when the projected post-run hourly ratio would cross warn/critical thresholds instead of only reacting to the current raw count
- observed request-delta projections now keep a short rolling baseline overall and per fetch mode, smoothing incremental/full-refresh fetch budgeting so one unusually expensive run is less likely to dominate the next unattended budget decision
- learned request projections are now tunable per task and per provider: operators can shrink/expand the observed-history window and optionally switch a lane/provider from mean-style smoothing to a conservative percentile baseline when a fetch path is burstier than average; task-specific tuning still wins, and when no explicit task/provider percentile is configured the daemon auto-switches obviously bursty lanes onto a conservative learned p90 baseline instead of blindly trusting the smoothed mean
- the repo now also ships opinionated provider defaults for the current source providers instead of leaving all pacing policy as operator-only examples: Crunchyroll now defaults to a deeper learned-history window plus conservative percentile budgeting/backoff floors, while HIDIVE ships its own quieter hourly/backoff/auth-failure defaults
- provider-task failures now trigger adaptive failure-aware cooldowns with persisted reason / failure class / configured floor / retry countdown / consecutive-failure state so auth-fragile fetch lanes do not thrash every loop after a bad run
- auth-style failure detection is now shared between daemon/runtime and health-check surfaces, so the same residue classes drive both failure cooldown classification and later operator rebootstrap guidance instead of those heuristics drifting apart
- health-check now inspects persisted daemon failure state and can recommend provider auth re-bootstrap when repeated unattended fetch failures look auth-related (not just repeated 401/unauthorized loops, but also refresh/login failure residue, missing-refresh-token / missing-refresh-material residue, malformed-token-payload residue, and provider session-state `auth_failed` phases)
- provider fetch lanes now persist successful fetch-mode state plus a periodic full-refresh anchor so unattended daemon runs can stay incremental by default while still forcing a conservative provider `--full-refresh` sweep on a configurable cadence (`service.full_refresh_every_seconds`, default 24h); failed full-refresh attempts no longer advance the success markers or anchor
- unattended provider fetch lanes now also honor health-check `refresh_full_snapshot` maintenance recommendations, so partial-coverage warnings from the latest health artifact can trigger the next fetch to self-upgrade into a conservative full refresh immediately instead of waiting for the cadence timer
- fresh unattended installs now also ship built-in mode-specific projected-request defaults for both Crunchyroll (`sync_fetch_crunchyroll`: `4` incremental / `55` full refresh) and HIDIVE (`sync_fetch_hidive`: `4` incremental / `71` full refresh) via the fetch-mode task projection table, so cold-start daemon budgeting does not assume either the ordinary fetch path or the heavier resweeps cost zero requests before history exists
- built-in projected-request defaults now consistently act as cold-start seeds rather than permanent hard overrides, so learned request history can take over for `mal_refresh`, `sync_apply`, and provider full-refresh fetches once the daemon has real observed cost data while explicit task-wide overrides still beat the shipped seeds
- overdue provider full-refresh requests no longer have to starve a fetch lane completely when the heavy sweep is temporarily over budget: the daemon now falls back to an incremental fetch when that cheaper mode fits, while leaving the full-refresh anchor/reason intact so the overdue resweep still happens later
- recommendation generation and metadata refresh exist
- tests remain bundled in the repo for third-party auditing

## Open work

- continue tightening daemon orchestration and request-budget behavior (projected per-run request budgeting now uses explicit lane overrides, fetch-mode-specific task overrides, or tunable learned observed-history windows/percentiles, bursty lanes now auto-fallback to a conservative learned p90 when no explicit percentile is configured, `mal_refresh` plus `sync_apply` and Crunchyroll/HIDIVE full-refresh now have shipped built-in task defaults, and budget-blocked overdue full refreshes now degrade gracefully to incremental fetches instead of stalling the lane entirely; next likely step is deciding whether HIDIVE or any future source lanes deserve similarly justified shipped learned-percentile posture)
- continue reducing genuinely ambiguous mapping residue
- continue stabilizing fresh Crunchyroll fetches on hostile/auth-fragile hosts
- continue improving recommendation quality and review UX
- keep encouraging third-party bug reports and feature requests through the authoritative upstream issue tracker: <https://github.com/kklouzal/MAL-Updater/issues>
