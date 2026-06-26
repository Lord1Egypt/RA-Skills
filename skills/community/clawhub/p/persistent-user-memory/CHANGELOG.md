# Changelog

All notable changes to this project will be documented here.

This project adheres to [Semantic Versioning](https://semver.org/).

---

## [1.0.0] – 2026-03-02

### Added
- Initial release of `persistent-user-memory` skill
- Full user profile schema: identity, preferences, relationships, patterns, episodic log
- Silent read-before-act behavior
- Silent write-after-learning behavior
- Proactive memory surfacing (non-intrusive)
- Episodic log with auto-trim after 180 days (except `important` tagged entries)
- Automatic memory hygiene on startup (dedup, stale flagging, timestamp update)
- Edge case handling:
  - Conflicting preferences → surface conflict, wait for resolution
  - Ambiguous contacts → ask, never guess
  - Sensitive data requests → politely refuse
  - Corrupted memory file → backup + fresh start + recovery offer
  - First run → passive learning, no onboarding questionnaire
  - "What do you know about me?" → human-readable summary
  - "Forget [X]" → surgical deletion with confirmation
- Privacy-first design: local only, no raw data sent to APIs
- Example profile: `examples/user_profile.example.json`

---

## [Unreleased]

### Planned
- Vector store backend support for semantic memory search
- Encrypted memory file option (`user_profile.enc.json`)
- Multi-user profile support for shared machines
- Memory export to portable format (JSON / Markdown)
- ClawHub registry publication
