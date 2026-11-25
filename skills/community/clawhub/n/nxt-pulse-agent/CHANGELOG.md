# Changelog

All notable changes to NXT Pulse Agent are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/); versioning is [SemVer](https://semver.org/).

## [0.6.0] — 2026-10-24

### Added

- **Hard first-run consent gate**: skill is fully inert (no nudges, no
  analysis, no file reads) until explicit opt-in; `/pulse forget` revokes
  consent and deletes all local state.
- **`/pulse privacy`**: live disclosure of reads, writes, and retention.
- **`/pulse off` / `/pulse on`**: global kill switch.
- **`/pulse now`**: explicit, capped cooldown bypass (the only one).
- **`/pulse help`** and **`/pulse sensitivity 1-5`**.
- **⚪ Unknown state** with hysteresis (two consecutive signals to change
  state) and sensitivity-linked confidence thresholds.
- **Anti-nag backoff**: two consecutive ignored nudges automatically double
  the effective cooldown (announced once); any `/pulse` interaction resets it.
- **`QUIET_HOURS`** config (default `22:00-08:00` local).
- **`MAX_MESSAGES_SCANNED`** config (default 10, current session only).
- **`PULSE_LANGUAGES`** config (`"auto"` default, restrictable).
- **`LOG_HISTORY`** config (`false` disables `pulse-history.jsonl` entirely).
- **State schema versioning** (`"schema": 2`) so future releases migrate
  state instead of silently re-consenting or losing settings.
- `SECURITY.md`: threat model, data disclosure table, full remediation map
  for the v0.5.0 audit (12 findings).
- `TESTING.md`: pre-release acceptance matrix (consent, injection, privacy,
  backoff scenarios).
- `CHANGELOG.md`, `.gitignore`, `.clawhubignore`.

### Upgrade note

> **Upgrading from 0.5.0?** NXT Pulse now asks for consent on first use — that's
> expected. Run `/pulse privacy` to review what it reads and writes, then
> accept. Existing state is migrated to `schema: 2`, not discarded. Cooldowns
> start from the current default (`4h`) unless you configured `PULSE_COOLDOWN`.

### Changed

- **Prompt-only architecture**: `pulse.js` and the
  `temp_deadline_trigger.txt` mechanism are removed; all side effects are
  documented instead of implicit.
- `CONTEXT_SOURCES` default is now empty with an enforced contract:
  relative paths only, deny list, tail-only bounded reads, redaction
  boundary, neutral examples.
- Logs capped at 500 entries and redacted to reason codes (no message
  excerpts, no context content).
- Frontmatter: scoped description, `homepage`, `metadata.openclaw`
  (emoji, homepage), version bump.
- `package.json`: slug-safe `name`, `license: "MIT-0"`, removed fixed
  `language` field.
- README: fixed install command (owner-qualified), broken ClawHub link,
  config typo, complete config table.

### Security

- Resolves all 12 findings from the ClawHub v0.5.0 audit (1 A.I.G T05,
  11 SkillSpector including the High Tp4) — see `SECURITY.md`.
- Cooldowns can no longer be bypassed by message content or trigger files
  (prompt-injection surface closed).
- Medical/mental-health inference explicitly prohibited; "not a medical
  device" disclaimer added.

## [0.5.0] — 2026-04-21

### Added

- `/pulse` transparency command with manual overrides and quiet timers.
- `PULSE_SENSITIVITY` tuning; `MAX_CONTEXT_CHARS` context guardrails.
- Generic Pulse merge (last release to ship `pulse.js`).

## [0.3.1] — 2026-04-21

### Added

- Semantic urgency detection; first security-audit response pass.

## [0.2.0] — 2026-04-19

### Added

- Initial release: energy-state inference and adaptive proactivity.
