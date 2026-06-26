# TODO

## Packaging / bootstrap

- [x] Treat the repo root as the canonical skill package
- [x] Externalize default runtime state to `.MAL-Updater/`
- [x] Add `bootstrap-audit` as the first install/onboarding readiness check
- [x] Replace committed absolute-path systemd units with install-time rendered templates
- [x] Replace timer-first unattended automation with a user-level daemon-first model
- [x] Establish public-repo anonymization as an explicit project constraint for tracked code/references/tests/history
- [ ] Keep tightening the bootstrap/onboarding UX for new OpenClaw installs
- [x] Make repo-root test execution work without manual `PYTHONPATH` fiddling so future development turns can validate faster with plain `pytest -q`
- [x] Make bootstrap/install metadata more machine-readable with provider readiness and explicit recommended commands in `bootstrap-audit`

## Daemon / operations

- [ ] Tighten daemon control loops and per-lane state tracking (cadence / decision timing / last-run start-finish-duration / next-due / active-backoff observability now persists in service state, including warn-vs-critical budget backoff plus adaptive failure-aware provider cooldown state; generic source-provider budget defaults now exist so new providers no longer inherit Crunchyroll implicitly, task-level budget override tables now exist for lane-specific limit/floor policy, the repo now ships built-in `sync_apply` task defaults for MAL hourly limit / projected request cost / learned-history depth / conservative learned percentile / cooldown floors instead of leaving that lane purely example-config-driven, budget gating can now use per-lane projected request cost from explicit config, fetch-mode-specific task defaults, or observed history, learned projections are now tunable per task and per provider via observed-history windows plus optional percentile baselines, burstier lanes still auto-upshift to a conservative learned p90 when recent request history is clearly spiky, the repo now ships opinionated Crunchyroll/HIDIVE provider defaults instead of leaving that entirely to examples, Crunchyroll/HIDIVE incremental + full-refresh cold starts now also have shipped mode-specific projected-request defaults, built-in projected-request defaults now behave as cold-start seeds across MAL refresh / apply / full-refresh lanes instead of pinning those lanes to synthetic costs forever, unattended `mal_refresh` now also ships a small explicit cold-start request-cost seed plus a shallow learned-history window so fresh installs do not treat token refresh as a zero-cost mystery lane, overdue full refreshes now degrade gracefully to incremental fetches when only the heavier mode is over budget, and failed provider full-refresh attempts no longer falsely advance the success markers/anchor; next likely step is deciding whether HIDIVE or any future source lanes need equally opinionated shipped learned-percentile posture rather than just more hard-coded request counts)
- [ ] Continue refining request-budget accounting / backoff behavior for MAL and source providers (warn-threshold pacing + recovery-window backoff now exist, plus provider-specific cooldown floors, generic source-provider default hourly/backoff/auth-failure floors, auth-style failure-aware cooldown classification/floors after provider task errors, and health-check auth rebootstrap recommendations after repeated auth-style provider failures; auth-fragility classification now also catches refresh/login residue, missing-refresh-token / missing-refresh-material residue, malformed-token-payload residue, and provider session-state `auth_failed` phases via a shared detector used by both daemon/runtime and health-check surfaces, so next likely step is deciding which auth residues deserve distinct remediation lanes vs plain re-bootstrap)
- [ ] Decide whether to retire the remaining transitional wrapper scripts after more daemon logic moves in-process
- [x] Add richer service-state/observability surfaces for debugging unattended failures
- [x] Add `service-status --format summary` as a terse/operator-summary mode alongside the rich JSON surface

## Product / sync quality

- [ ] Continue reducing genuinely ambiguous mapping residue (the last live Haruhi-style 14+14 same-title split bundle now auto-resolves under heuristics revision `2026-03-22a`; next residue should be genuinely ambiguous season/alias cases rather than obvious same-title bundle suffixes)
- [ ] Continue stabilizing fresh Crunchyroll fetches on auth-fragile hosts (daemon-side periodic provider full-refresh cadence now exists via `service.full_refresh_every_seconds`, the daemon now honors health-check `refresh_full_snapshot` recommendations when partial-coverage warnings persist, and health-check can now recommend provider auth rebootstrap after repeated auth-style daemon failures even when provider state is already partially missing; next likely step is smarter auth-fragility classification/escalation for less-obvious provider-specific failure modes beyond the newly covered missing-token / malformed-token residue)
- [ ] Keep improving recommendation quality and review UX
- [ ] Keep the upstream GitHub issue tracker active as the canonical channel for third-party bug reports and feature requests
