# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.15.9] - 2026-05-01

### Security (ClawScan Findings — All Phases)

**Phase 1 — Per-command --yes only + Pinned dependencies**
- **Removed session-wide `NEXLINK_AUTO_APPROVE`** — `--yes` / `-y` is now strictly **per-command**
  - `utils.confirm_or_die()` no longer checks env var; uses `auto_approved` kwarg only
  - `--yes` must be appended to each individual command; there is no env bypass
  - Nextcloud `run_cli()` uses module-level `_AUTO_APPROVED` instead of env
  - Exit code changed from 1 → 2 on non-confirmation
  - Tests updated for new behavior
- **Pinned all pip dependencies** to exact versions in `SKILL.md` + `requirements.txt`
  - `exchangelib==5.6.0`, `requests-ntlm==1.3.0`, `defusedxml==0.7.1`, `requests==2.31.0`, `lxml==6.0.2`

**Phase 2 — Branding opt-out simplification**
- Removed `--no-branding` global flag and `NEXLINK_NO_BRANDING` env var references from CLI
- Branding is controlled by skill modules at output generation level (not CLI)
- Usage text updated; references to `NEXLINK_NO_BRANDING` removed from security docs

**Phase 3 — Data handling: permissions + disclosure**
- **Config file permissions**: `config.save()` now sets `chmod 0o600` on saved config files
- **Log file permissions**: `logger.py` now creates log directory `0o700` and log files `0o600`
- **Sync state permissions**: `save_sync_state()` sets `0o600` on state file and `0o700` on parent dir
- Added comment in `config.template.yaml` about permission expectations for state file directory
- **Password handling**: config.save() already strips password from written file; added audit comment
- **Logging credentials**: NexLink does NOT log credentials or raw email content to log files

**Phase 4 — Documentation & disclosure**
- `SECURITY.md`: Updated security model, removed `NEXLINK_AUTO_APPROVE` references
- `references/security-best-practices.md`: Removed `NEXLINK_AUTO_APPROVE` docs, kept per-command `--yes`
- `CHANGELOG.md`: This comprehensive entry for audit trail

**Phase 5 — Branding opt-in + env metadata (Privacy-first)**
- `BRAND.md`: Branding is now **OFF by default** (privacy-first). Enable with `NEXLINK_BRANDING=1` (opt-in)
  - `NEXLINK_NO_BRANDING` removed; old opt-out mechanism deprecated
- `SKILL.md`: Added `NEXLINK_BRANDING` to env vars list
- `clawhub.json`: Added `env` field documenting all required variables
  - Full transparency: lists all 9 required/optional env vars for ClawHub security scan
- Closes ClawScan findings #2 (Human-Agent Trust) and #3 (Supply Chain)

## [Unreleased]

## [0.15.0] - 2026-04-30

### Security (ClawScan Audit Remediation)

- **Prompt Approval System** — all destructive operations now require explicit confirmation
  - 29 operations guarded: send, reply, forward, create/delete event, respond meeting, create/complete/trash task, create/update/delete contact, sync, link-calendar, delete/move/copy file, share-revoke, create-tasks-from-file --execute
  - Global `--yes` / `-y` flag for non-interactive bypass
  - `NEXLINK_AUTO_APPROVE=1` environment variable for session-wide bypass
  - Non-TTY fallback: JSON error with clear instructions to use `--yes`
  - 8 new unit tests covering TTY, non-TTY, env var, abort scenarios (all passing)
- **SECURITY.md** — GitHub-standard vulnerability disclosure policy with coordinated disclosure timeline (2 days acknowledgment, 5 days assessment, 30 days fix, 90 days disclosure)
- **references/security-best-practices.md** — comprehensive least-privilege deployment guide (dedicated accounts, credential rotation, network isolation, logging, monitoring)
- **Opt-out controls**:
  - `--no-branding` / `NEXLINK_NO_BRANDING=1` — suppress branding in outputs
  - `--no-memory` / `NEXLINK_NO_MEMORY=1` — opt-out of LCM persistent memory
- **requirements.lock** — fully pinned dependencies for reproducible builds

### Added

- GitHub repository link in SKILL.md description for official branding
- Professional header in README.md with official links table
- `clawhub.json` enhanced with badges, keywords, and full link portfolio
- `BRAND.md` updated with opt-out instructions

### Changed

- **Version**: 0.14.1 → **0.15.0** (minor bump — new security features, backward compatible)
- **Name**: "NexLink — Nextcloud, Exchange & YouTube Connector" → "NexLink — Enterprise Connector for Nextcloud, Exchange & YouTube"

### Verification

- ✅ 48/48 unit tests passing
- ✅ 9 real-world scenarios validated
- ✅ Zero breaking changes
- ✅ ClawScan security audit: 7/7 findings remediated

---

## [0.14.1] - 2026-04-29

### Changed

- Version bump to v0.14.1 for release

## [0.13.0] - 2026-04-29

### Added

- **YouTube Transcript Extraction** — full module with `nexlink youtube transcript` and `nexlink youtube languages` commands
- Supports all URL formats (watch, youtu.be, shorts, embed) and raw video IDs
- Automatic language fallback (e.g. `--lang ro,en`)
- Output formats: text (plain) and JSON (timestamped snippets)
- Save to Nextcloud with `--save` flag (saves to `/Alex's Assistant/YouTube/`)
- Comprehensive test suite: 23 tests covering ID extraction, error handling, formatting, live API, and CLI integration

## [0.12.0] - 2026-04-28

### Added

- **Exchange contacts module** — full CRUD + search via EWS
  - `nexlink contacts list|get|create|update|delete|search`
  - Server-side search with Q() filter (display_name, given_name, surname, company_name, email)
  - Safe delete via `move_to_trash()`
- **Nextcloud contacts module** — CardDAV contacts with auto-discovered principal
  - `nexlink contacts addressbooks|list|get|create|update|delete|search --source nextcloud`
  - vCard ↔ dict conversion
  - Automatic DAV principal discovery (handles GUID-based principals)
  - Cached principal resolution (avoids PROPFIND per call)
- **Integration tests** — 11 Exchange live + 12 Nextcloud live tests

### Fixed

- **`_get_contacts_folder`** was returning `account.contacts.root` (MailFolder) instead of `account.contacts`
- **`ContactPhoneNumbers` removed in exchangelib 5.x** — use `List[PhoneNumber]` with `label` + `phone_number`
- **`EmailAddress` import path** — `email_addresses` accepts `List[EmailAddress]` objects, not dicts
- **`PhysicalAddress` moved to `exchangelib.indexed_properties`** — import from `exchangelib.properties` raised `ImportError`
- **Nextcloud DAV principal mismatch** — `_dav_base_path()` used login username but Nextcloud may use a GUID; now auto-discovers via PROPFIND

## [0.11.0] - 2026-04-25

### Added

- **OWNER_EMAIL config variable** — optional env var for notification recipient
  - Priority chain: `--to` flag > `OWNER_EMAIL` > `account.primary_smtp_address`
  - Defaults to `EXCHANGE_EMAIL` when not set (backward compatible)
  - Documented in SKILL.md env vars list
- **Integration tests for OWNER_EMAIL fallback** — 3 new tests in `TestOwnerEmailFallback`
  - `test_reminder_uses_owner_email` — verifies OWNER_EMAIL is used as recipient
  - `test_reminder_falls_back_to_account_email` — verifies fallback to Exchange account
  - `test_reminder_explicit_to_overrides_owner_email` — verifies `--to` flag priority
- **Integration tests for Exchange sync operations** — 15 new tests covering sync, error handling, and reminder flows

### Changed

- `cmd_reminders` now resolves recipient via `get_connection_config()` instead of `account.primary_smtp_address` directly

## [0.9.0] - 2026-04-22

### Changed

- **Complete rebrand: imm-romania → NexLink**
  - Skill name, CLI command, folder, script, all references updated
  - GitHub repo renamed to `openclaw-nexlink`
  - ClawHub slug: `nexlink`
  - Public name: **NexLink — Exchange & Nextcloud Connector**
  - Built by Firma de AI, supported by Firma de IT

## [0.5.1] - 2026-04-11

### Added

- **Nextcloud document understanding**
  - `extract-text` for supported text, DOCX, and PDF files
  - `summarize` for grounded one-file summaries
  - `ask-file` for extractive Q&A over a single file
- **Nextcloud workflow intelligence**
  - `extract-actions` for grounded action extraction with due-date and owner hints
  - `create-tasks-from-file` to create Exchange tasks from extracted file actions

### Changed

- **Product boundary cleanup**
  - NexLink now focuses on Exchange + Nextcloud only
  - MSP runtime, scripts, tests, and examples were removed from this repo
  - MSP logic now lives in a separate dedicated skill
- **Documentation refresh**
  - README, SKILL, setup guide, and verification docs now describe the current CLI accurately
- **Packaging metadata**
  - version metadata aligned to `0.4.0`
  - setup metadata updated for the current CLI script and recommended PDF dependency

### Fixed

- Unified CLI help now reflects the final Nextcloud command surface after cleanup and integration
- Release metadata inconsistencies across `SKILL.md`, `README.md`, `VERIFICATION.md`, and `setup.py`

## [0.2.0] - 2026-03-30

### Added

- **Task Sync Module**: Bidirectional sync with Exchange server
  - `sync sync` - Synchronize tasks with server
  - `sync status` - Show sync statistics
  - `sync reminders` - Email reminders for overdue/upcoming tasks
  - `sync link-calendar` - Create calendar event from task
- **Hardshell Coding Standards**: Applied to all Exchange modules
  - Black formatting (PEP 8)
  - Ruff linting (fixed unused imports)
  - Comprehensive test suite (24 tests passing)
- **Module Organization**: Clean separation of concerns
  - `modules/exchange/` - Email, Calendar, Tasks, Sync
  - `modules/nextcloud/` - File management
  - `scripts/nexlink.py` - Unified CLI entry point
- **Documentation**: Setup guide, skill docs, coding standards

### Fixed

- Test imports for module paths
- CLI execution path in tests
- Duplicate function definitions removed

## [0.1.0] - 2026-03-30

### Added - Initial Release

- Email operations: connect, read, get, send, draft, reply, forward, mark, attachments
- Calendar operations: connect, list, today, week, get, create, update, delete, respond, availability
- Tasks operations: connect, list, get, create, update, complete, delete
- Unified CLI with `nexlink mail|calendar|tasks` commands
- Configuration via environment variables or config file
- Self-signed certificate support via `verify_ssl: false`
- MIT License
- GitHub issue templates and PR template

## [2.0.0-alpha] - 2026-03-30

### Added - Meta-Skill Architecture

**Breaking Change**: Restructured as meta-skill with modular architecture.

- **Modules**: Separated Exchange and Nextcloud into independent modules
- **Exchange Module**: Email, Calendar, Tasks operations (moved from root)
- **Nextcloud Module**: File management via WebDAV (new)
- **Memory Integration**: Documentation for LCM plugin integration
- **Unified CLI**: New orchestrator `nexlink.py` for all modules

### Added - Exchange Module

- All previous email, calendar, and tasks functionality
- Task sync with Exchange server
- Email reminders for overdue/upcoming tasks
- Calendar event creation from tasks
- Logging system with JSON and colored output
- Complete test suite (9 tests passing)

### Added - Nextcloud Module

- File operations: upload, download, list, delete, move, copy
- Directory creation and management
- Automatic user ID resolution for WebDAV paths
- Error handling with specific exit codes

### Added - Memory (LCM Plugin)

- Documentation for Lossless Context Management plugin
- Instructions for persistent conversation history
- Tool descriptions: `lcm_grep`, `lcm_describe`, `lcm_expand_query`

### Added - Workflow Integrations

- Email + Files: Send attachments from Nextcloud
- Email + Files: Save attachments to Nextcloud
- Calendar + Tasks: Create calendar events from tasks
- Memory + All: Context-aware operations

### Changed - Architecture

- **Before**: Single skill with Exchange only
- **After**: Meta-skill orchestrating multiple modules
  - `modules/exchange/` - Email, Calendar, Tasks
  - `modules/nextcloud/` - File management
  - `references/setup.md` - Complete setup guide
  - `assets/config.template.yaml` - Configuration template

### Changed - Documentation

- New SKILL.md as meta-skill documentation
- Per-module SKILL.md files
- Comprehensive setup guide in `references/setup.md`
- Updated README with module structure

### Migration Guide (1.x to 2.0)

If upgrading from 1.x:

1. Update imports:
   ```python
   # Before
   from scripts.mail import MailClient
   
   # After
   from modules.exchange.mail import MailClient
   ```

2. Update CLI commands:
   ```bash
   # Before
   python3 scripts/mail.py connect
   
   # After
   python3 scripts/nexlink.py mail connect
   # Or simply
   nexlink mail connect
   ```

3. New environment variables for Nextcloud:
   ```bash
   export NEXTCLOUD_URL="https://cloud.example.com"
   export NEXTCLOUD_USERNAME="your-username"
   export NEXTCLOUD_APP_PASSWORD="your-app-password"
   ```

---

## [1.0.0] - 2026-03-30

### Added

- Email operations: connect, read, get, send, draft, reply, forward, mark, attachments
- Calendar operations: connect, list, today, week, get, create, update, delete, respond, availability
- Tasks operations: connect, list, get, create, update, complete, delete
- Unified CLI with `nexlink mail|calendar|tasks` commands
- Configuration via environment variables or config file
- Self-signed certificate support via `verify_ssl: false`
- MIT License
- GitHub issue templates and PR template

### Security

- Credentials only from environment variables (never hardcoded)
- SSL verification configurable for self-signed certificates

---

## [Unreleased]

### Planned

- Distribution lists management
- Room booking
- Delegate access support (full)
- Docker deployment