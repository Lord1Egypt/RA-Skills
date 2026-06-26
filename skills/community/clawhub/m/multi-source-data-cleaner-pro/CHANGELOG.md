# Changelog

All notable changes to this skill will be documented in this file.
The format follows [Keep a Changelog](https://keepachangelog.com/),
and this skill adheres to [Semantic Versioning](https://semver.org/).

## [1.0.0] - 2026-05-26

### Added
- Initial public release.
- End-to-end pipeline script with deterministic test fixtures.
- Bilingual (EN/中文) `SKILL.md` and `README.md`.
- MIT-0 license, `.clawhubignore`, and full audit-trail outputs.
- Privacy-first defaults: no external network calls, PII masking on.
- Unit tests covering core extraction / scoring paths.

### Notes
- This release passes the ClawHub publish format (`docs.openclaw.ai/clawhub/skill-format`).
- Compatible with SkillHub.cn distribution (data sourced from ClawHub).
- Security analysis: no obfuscated code, no external uploads, no credential reads.
