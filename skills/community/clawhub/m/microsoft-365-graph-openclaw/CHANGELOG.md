# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog, and this project follows Semantic Versioning.

## [0.2.2] - 2026-03-06

### Changed
- Clarified documentation so runtime values are described as service-level values loaded from `/etc/default/graph-mail-webhook`, rather than manual install-time environment requirements.
- Marked `OPENCLAW_SESSION_KEY` as optional (`hook:graph-mail` default) and documented minimal-flow `GRAPH_WEBHOOK_CLIENT_STATE` auto-generation behavior.

## [0.2.1] - 2026-03-06

### Changed
- Simplified `SKILL.md` OpenClaw metadata by removing environment-variable gating from `metadata.openclaw.requires.env` and dropping `metadata.openclaw.primaryEnv`.

## [0.2.0] - 2026-03-09

### Added
- **Flattened repository layout:** skill content (`scripts/`, `references/`, `SKILL.md`) moved to repo root so `REPO_ROOT/scripts/` works for both clone and ClawHub install.
- **Minimal guide (6 steps):** [docs/minimal-setup.md](docs/minimal-setup.md) with minimal parameters; e2e setup generates clientState and creates subscription in one run.
- **docs/setup-openclaw-hooks.md:** how to create and configure OPENCLAW_HOOK_TOKEN (generate value, where in openclaw.json, use in setup).
- **docs/app-registration.md:** step-by-step for creating your own Microsoft Entra App Registration (optional; Alitar app is default).
- **generate-client-state:** `python3 scripts/mail_webhook_adapter.py generate-client-state` prints a clientState and exits (non-blocking).

### Changed
- **session-key optional:** `setup_mail_webhook_ec2.sh` and e2e setup no longer require `--session-key`; default `hook:graph-mail` used when omitted.
- **CRLF/LF:** `.gitattributes` forces LF for `*.sh`, `*.py`, `*.md`; scripts use portable `set -eu` + `set -o pipefail 2>/dev/null || true` for dash compatibility.
- **Auth docs:** Alitar app as default path; optional "use your own app" with link to app-registration.md; work/school quickstart uses Alitar client ID by default.
- **All paths:** references to `graph-office-suite/scripts/` and `graph-office-suite/references/` updated to `scripts/` and `references/` across docs, README, SKILL.md, and CI workflows.
- Worker payload `source` set to `microsoft-365-graph-openclaw` for ClawHub alignment.

### Documentation
- README: new "Minimal setup" section linking to `docs/minimal-setup.md`.
- references/auth.md: "Main path" (Alitar), optional own app, link to `docs/app-registration.md`.
- references/mail_webhook_adapter.md: clientState (e2e generates; generate-client-state command; advanced manual).
- Setup documentation links `minimal-setup`, `setup-openclaw-hooks`, and `app-registration`.

## [0.1.3] - 2026-03-06

### Changed
- Updated repository naming references from `openclaw-skills` to `openclaw-graph-office-suite` across docs, metadata, and setup script examples.
- Updated `graph-office-suite/SKILL.md` homepage/repository URLs and OpenClaw metadata homepage to the renamed GitHub repository.

## [0.1.2] - 2026-03-06

### Changed
- Updated `graph-office-suite/SKILL.md` description to a push-first value proposition so ClawHub listing matches repository positioning.
- Fixed CI link checker workflow by removing unsupported Lychee CLI flag (`--exclude-mail`) from `.github/workflows/link-check.yml`.

## [0.1.1] - 2026-03-06

### Changed
- Moved skill runtime requirements to `metadata.openclaw.requires` / `metadata.openclaw.primaryEnv` for registry-aligned capability gating.
- Added explicit privileged-operations boundary documentation in `README.md` and `graph-office-suite/SKILL.md`.
- Added `--dry-run` support to `setup_mail_webhook_ec2.sh` and `run_mail_webhook_e2e_setup.sh` to preview writes and service actions before execution.

## [0.1.0] - 2026-03-06

### Added
- Push-first Microsoft Graph workflow for OpenClaw with webhook adapter, queue, and worker.
- EC2 setup automation, smoke tests, and full pipeline diagnostics scripts.
- Mail subscription lifecycle CLI (`create`, `status`, `renew`, `delete`, `list`).
- Wake-first integration with OpenClaw hooks (`/hooks/wake` default mode).

### Changed
- Default subscription resource updated to `me/messages` for broader delivery coverage.
- Documentation refocused on cost-aware, event-driven operation and self-hosted production setup.
- Diagnostics now include human-readable UTC timestamps for webhook operation logs.

### Security
- Documented secret handling and explicit hook token/clientState validation guidance.
- Added publish-scope controls and release hardening documentation.
