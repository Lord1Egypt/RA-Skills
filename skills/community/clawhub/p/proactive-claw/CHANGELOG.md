## 1.2.41
- Convenience: `scripts/setup.sh` now supports `--doctor` (readiness checks) and `--print-install-cmd google|nextcloud` (single copy-paste install command).
- Convenience: added `scripts/quickstart.sh` for a local-safe first run flow (doctor, safe defaults, daemon simulation).
- Trust: added pinned dependency files `requirements-google.txt` and `requirements-nextcloud.txt`.
- Docs: updated `SKILL.md` and `SECURITY.md` to describe literal core behavior (manual daemon only, no daemon installer in core package).
- Ops: added `RELEASE_CHECKLIST.md` with artifact preview, exclusion verification, validation, and publish commands.

## 1.2.40
- Release increment after 1.2.39 publish collision; core hardening profile remains unchanged.

## 1.2.39
- Security/Scanner hardening: core bundle now excludes `voice_bridge.py` and `llm_rater.py` from published artifacts (`.clawhubignore` / `.skillignore`).
- Security/Scanner hardening: removed remaining core cross-skill context references from `orchestrator.py` and switched orchestration payloads to local pattern history only.
- Security/Scanner hardening: core notification channel learning no longer references `telegram`; core channels are `openclaw` + `system`.
- Install hardening: `scripts/setup.sh` no longer auto-runs package installers; it now validates required modules and fails closed with explicit manual install instructions.
- Defaults hardening: interactive config wizard now defaults to `max_autonomy_level=confirm`.
- Docs: updated `SECURITY.md` and `SKILL.md` to match core-only behavior and setup semantics.

## 1.2.37
- Split release model: core bundle is now integration-free by default; third-party/network-heavy helpers moved to the separate `proactive-claw-integrations` add-on.
- Core bundle exclusions: `cross_skill.py`, `team_awareness.py`, `install_daemon.sh`, and `optional/setup_clawhub_oauth.sh` are no longer published in core.
- Privacy hardening: removed Notion outcome upload path from `capture_outcome.py`.
- Core notifications are local-only (`openclaw`, `system`) in shipped defaults.
- Docs/config updated to reflect core vs integrations split.

## 1.2.36
- Security/Privacy: `llm_rater.py` is now local-only. Non-local LLM base URLs are hard-blocked (`localhost` / `127.0.0.1` / `::1` only).
- Security/Privacy: removed cloud LLM backend presets and cloud endpoint references from shipped config/docs.
- Security/Privacy: `team_awareness.py` is excluded from published bundles via `.clawhubignore` and `.skillignore` (kept as optional source only).
- Docs/Config: removed `feature_team_awareness` from shipped defaults and updated security tables accordingly.

## 1.2.35
- Security: hardened `scripts/optional/setup_clawhub_oauth.sh` to fail closed by default.
- Security: remote credential bootstrap now requires explicit opt-in (`clawhub_oauth_allow_remote_fetch=true`) and a valid pinned `clawhub_credentials_sha256` match before writing `credentials.json`.
- Security: added strict payload shape checks and response size limits for clawhub OAuth credential fetch.
- Security: `credentials.json` is written with restrictive file permissions (`0600`).
- Docs/Config: updated `config.example.json`, `scripts/setup.sh`, and `SECURITY.md` to reflect the SHA-256 pin workflow and correct optional script path.

## 1.2.34
- Security: voice command routing now uses an explicit in-process allowlist dispatcher for user intents, removing subprocess execution for routed commands.
- Security: stricter input validation rejects flag-like capture tokens (for example `--dry-run`) to reduce argument-injection risk.
- Fix: policy voice intents now call policy parsing/storage directly in-process.

## 1.2.33
- Bug: `_iso_to_ts()` returned 0 on parse failure — action events no longer fire at Unix epoch; events with unparseable times are skipped with a warning log.
- Bug: Quiet hours (configured in `config.json`) now enforced in daemon — non-critical notifications are suppressed during configured windows. Conflict alerts remain critical and are always delivered.
- Bug: State file write is now atomic (temp file + `os.replace()`) — prevents `daemon_state.json` corruption on crash or kill signal.
- Bug: `notified_events` cleanup is now TTL-based (48h expiry) instead of a 200-key size cap — old entries no longer crowd out new ones after heavy use.
- Fix: CalDAV event parse errors now log the event UID and error reason instead of silently dropping the event.
- Fix: `config_wizard.py` `DEFAULT_CONFIG` feature flags aligned to match `config.example.json` — all features default `False` (opt-in), not `True`.
- Feature: `event_relink_tolerance_sec` configurable via `config.json` (default: 300s). Controls how far a moved recurring event can shift and still be auto-relinked.
- Feature: CalDAV server path configurable via `nextcloud.caldav_path` in `config.json` (default: `/remote.php/dav`). Supports non-Nextcloud CalDAV servers.

## 1.2.31
- Security: Hardened voice command routing to avoid argument/command injection (no string splitting; suspicious metacharacters rejected; captured text passed as single args).
- Docs: Updated SKILL.md description and diagrams.

# Changelog — Proactive Claw

## 1.2.30
- Security hardening: default autonomy is **confirm** even when config is missing (fail-closed defaults).
- Updated SKILL.md: clearer proactive loop (calendar ⇄ engine ⇄ chat), stronger scenarios, and local-first positioning.

## 1.2.29
- Safe defaults: `config_wizard.py --defaults` generates `max_autonomy_level=confirm`.
- Autonomous mode requires explicit opt-in with `--i-accept-risk`.
