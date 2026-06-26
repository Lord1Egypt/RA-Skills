# Changelog

All notable changes to this skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this skill adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.1] — 2026-06-08

### Added
- **Privacy and Data Handling** section in SKILL.md describing the real network surface (Google Business Profile API v4, Google OAuth token endpoint, configured approval channel), credential storage (operator-owned OAuth credentials per client in `clients_dir`), and hard guardrails (no auto-posting, no PHI in public replies, no credential leakage, no bulk export)
- **Permissions and Privacy** section in README.md so operators see the full network surface, credential storage posture, hard guardrails, and the compliance scope (HIPAA-aware drafting, NOT a HIPAA-certified workflow) before installing

### Changed
- Reworded the `medical` industry profile from "HIPAA-safe" to "HIPAA-aware drafting" to accurately describe the constraint (avoids PHI in public reply text) without implying a regulatory certification this skill cannot provide. CHANGELOG references to "HIPAA-safe" updated in the 2.0.0 entry's description of this profile for consistency
- Narrowed the activation triggers in the `description` frontmatter to require an explicit configured-client workflow (named client, named reviewer, specific approval/post action), with a "do NOT trigger" guardrail for casual review chat, review-writing requests, and marketing-strategy questions
- Unquoted the `version` field in frontmatter (matches updated ClawHub CLI semver requirements)

## [2.0.0] — 2026-05-12

### Added
- Configuration file (`review-responder.config.json`) for centralizing script paths, clients directory, approval channel, default industry, and memory file location
- Per-client configuration overrides for industry, approval channel, and tone notes
- Channel-agnostic approval flow with four supported channels: Telegram, email, webhook, and in-thread chat
- Industry compliance profiles for medical (HIPAA-safe), legal, restaurant, retail, and general business types
- Operator pattern learning layer that logs each approval decision (approved-as-is, edited with diff summary, skipped) per client and surfaces patterns over time
- Periodic insight surfacing to the operator (e.g., "you usually shorten 5-star replies for this client by ~10 words")

### Changed
- **BREAKING**: Hardcoded script paths (`~/review-responder/gbp_reviews.py`) replaced with a configurable `script_path` field
- **BREAKING**: Telegram is no longer the assumed approval channel; `approval_channel` must be set explicitly in config
- HIPAA section promoted from a sub-block under Response Guidelines into a top-level `Industry Compliance Profiles` section with peer profiles for other industries
- SKILL.md now has proper YAML frontmatter (`name`, `version`, `description`, `metadata.openclaw.emoji`)

### Removed
- MIT LICENSE file (license now managed at the ClawHub platform level)

## [1.0.0] — 2026-03-27

### Added
- Initial release
- Scheduled review checks across multiple Google Business Profile clients
- Tone-matched response drafting by star rating (5, 4, 3, 1-2)
- Telegram-based approval flow with OK/edit/skip operator commands
- HIPAA-aware response guidance for medical clients
- Per-client config files for multi-client agency use
- OAuth onboarding helpers (`get_client_token.py`, `oauth_server.py`)
