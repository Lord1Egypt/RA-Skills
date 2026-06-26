# Changelog — healthy-backup

All notable changes to this skill are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [1.2.5] — setup flow fix

### Fixed
- Space in backup path (e.g. "OpenClaw backups") caused `set -euo pipefail` to kill setup during dry-run, silently skipping the cron question. Config is now written via `jq -n` with proper argument passing — paths with spaces handled correctly throughout.
- Dry-run is now wrapped in `|| { warn... }` — never fatal to setup regardless of exit code.
- `prompt_yn` default changed to `n` everywhere — Enter alone no longer silently accepts; must explicitly type y or n.
- Cron question moved to Phase 1 (all questions upfront) so it can never be skipped by a later failure.
- Cron default changed from `y` to `n` — explicit opt-in required.

### Changed
- Setup flow restructured into 5 explicit phases: Questions → Write config → Install cron → Dry run → Summary.
- Cron recommended time updated to 03:15 (after Total Recall dream cycle at 03:00).
- Summary always shown regardless of dry-run outcome.

---

## [1.2.4] — setup wizard & dedicated config

### Added
- `setup.sh` — interactive first-run configurator: asks questions, writes `~/.openclaw/config/healthy-backup/hb-config.json`, creates encryption key file, runs `--dry-run` automatically, optionally installs cron job. Re-runnable for reconfiguration.
- Dedicated config path `~/.openclaw/config/healthy-backup/hb-config.json` — fully independent of `openclaw.json` structure, works on any OpenClaw rig regardless of how `skills` is organised
- Health audit check 0: warns clearly if setup hasn't been run (no config file found)
- `setup.sh` added to `package.json` bin and files

### Changed
- `cfg()` now reads from `hb-config.json` first, then env vars, then built-in defaults — no longer attempts to parse `openclaw.json` skill entries
- SKILL.md setup section leads with `setup.sh` as the primary install path
- Checksums updated for all three scripts

---

### Added
- `--dry-run` flag: runs full health audit and prints every file that *would* be staged (via `rsync --dry-run`) without writing anything — directly addresses the auditor's recommendation to test before scheduling
- **"What this script reads"** table in SKILL.md: lists every file, directory, and system call the script makes, with sensitivity notes — no surprises before install
- Dry-run usage shown in setup section of SKILL.md

### Fixed
- Stale `END OF FILE` comment still referenced v1.2.1

### Changed
- `--dry-run` recommended as first step in install instructions before scheduling cron

---

### Fixed
- **`openclaw.json` copied verbatim** (critical): config is now staged via `jq walk()` that replaces values of any field whose name contains `password`, `token`, `secret`, or `key` with `"<redacted>"`. Structure and all non-sensitive values are preserved. Live file on disk is never modified.
- **SKILL.md false claim** ("minimal tier never reads secrets file"): the secrets file *is* read at all tiers to extract variable names for the manifest. Docs now accurately describe this: the file is read for key names; values are never written.
- **Inline password in config sample**: removed `"password"` field from the example JSON in SKILL.md. Added explicit warning not to store password inline in `openclaw.json`.

### Added
- Health audit now warns when an inline `password` is detected in `openclaw.json`, recommending migration to `backup.key`.
- Config table marks `password` field as discouraged with explanation.

### Changed
- Secrets policy section in SKILL.md fully rewritten to match code: scrubbing via `jq walk()`, rsync exclusions, manifest behavior, and GPG passphrase handling each documented separately and accurately.

---

## [1.2.2] — secrets correctness

### Fixed
- openclaw.json staged via `jq walk()` scrubbing — sensitive field values replaced with `"<redacted>"`
- SKILL.md false claim corrected: secrets file is read at all tiers (for key names); values never written
- Inline password removed from config sample; warning added

### Added
- Health audit warns when inline password detected in openclaw.json
- Config table marks `password` field as discouraged

---

## [1.2.1] — refactor

### Changed
- Reduced codebase by 44% (625 → 350 lines) with no behavior changes
- `get_config()` → `cfg()` — shorter config resolution helper
- Color variables compressed to single-letter names
- `check_pass/fail/warn` → `chk_ok/fail/warn`; shared `check_perms()` helper eliminates duplicated stat+compare pattern
- All three `rsync` calls unified through a single `sync_dir()` helper; `EXCLUDES` array built once
- Audit checks collapsed to `&&`/`||` one-liners where readable
- `set -e` → `set -euo pipefail` (catches unbound vars and pipe failures)
- `verify-backup.sh` halved (105 → 53 lines), same behavior
- Section banner comments stripped — code is self-explanatory

---

## [1.2.0] — verifiability

### Added
- `verify-backup.sh` — standalone integrity checker; validates SHA256 and GPG envelope of any archive or full backup directory
- SHA256 checksum written alongside every archive on completion (`archive.tgz.gpg.sha256`)
- Script prints its own SHA256 on every successful run for installed-version verification
- Release checksums published in `SKILL.md` for pre-run verification
- `# END OF FILE` marker to confirm script is not truncated
- `set -euo pipefail` (carried forward from patch)

### Changed
- rclone install guidance: replaced `curl|bash` one-liner with package manager commands (`apt`/`dnf`) as primary recommendation; download-inspect-run pattern documented for binary installer
- `package.json` version bump; `verify-backup.sh` added to `bin` and `files`

---

## [1.1.0] — security hardening

### Fixed
- **Secrets staging contradiction**: `~/.openclaw/shared/secrets/` and `credentials/` are now hard-excluded from all `rsync` calls via a top-level `ALWAYS_EXCLUDE` array — no config can override this
- Additional secret-bearing file patterns excluded: `*.key`, `*.pem`, `*.env`, `*.secret`, `.env`
- **GPG passphrase on process list**: switched from `--passphrase` CLI arg to `--passphrase-file` pointing at a `chmod 600` temp file; password `unset` from environment after writing; temp file deleted via `trap EXIT`
- `backup.key` permissions now hard-fail (not warn) if not `600`
- Secrets file permissions now hard-fail if not `600`

### Changed
- `collectCrontab` and `collectNpm` default to `false` (opt-in); when crontab collection is enabled, `VAR=VALUE` patterns are redacted to `VAR=<REDACTED>` before staging
- `collectOllama` remains `true` by default (model names are low-sensitivity)
- `SKILL.md` rewritten to precisely match script behavior: secrets exclusion list quoted verbatim, passphrase-file mechanism documented, health check table distinguishes hard-fail vs warn-only
- `package.json`: removed OS binaries (`gpg`, `jq`, `rsync`) as npm `dependencies`; replaced with informational `systemDependencies` field and `"os": ["linux"]`

---

## [1.0.0] — initial release

### Added
- Health audit gate: backup only proceeds if all critical checks pass (hard block, no override)
- Eight audit categories: binaries, config integrity, key directories, disk space, encryption readiness, secrets file permissions, cloud remote (if rclone), Ollama models
- Three backup tiers: `minimal` (openclaw.json + secrets manifest), `migratable` (+ full `~/.openclaw` + `DEPENDENCIES.md`), `full` (+ workspace + skills)
- `DEPENDENCIES.md` generated at migratable/full tiers: binary versions, OS info, optional npm globals, ollama models, crontab
- AES256 GPG symmetric encryption
- Retention: keeps last N healthy backups (default 5), prunes older archives automatically
- Optional rclone cloud sync
- Config resolution hierarchy: skill config → env var → auto-detect
- Health report (`HEALTH_REPORT.txt`) embedded in every archive
- Inspired by **simple-backup** (VACInc) and **claw-backup** (vidarbrekke)

---

## [1.3.0] — compaction & verify merge

### Changed
- `verify-backup.sh` eliminated — merged into `healthy-backup.sh` as `--verify [path]` subcommand. Now just 2 scripts total.
- `healthy-backup.sh`: 384 → 259 lines. Stage functions collapsed, dry-run and audit loops tightened, variable names shortened, UI helpers deduplicated.
- `setup.sh`: 210 → 170 lines. Same refactor pass applied.
- Total: 647 → 429 lines (-34%) with identical capability.
- Cron default time updated to 05:00 (2hr buffer after Total Recall dream cycle at 03:00).

### New usage
```
healthy-backup.sh             # full backup
healthy-backup.sh --dry-run   # audit + show what would be staged
healthy-backup.sh --verify    # verify all archives in backupRoot
healthy-backup.sh --verify /path/to/archive.tgz.gpg   # verify single file
```
