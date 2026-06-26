# Packaging Checklist — openclaw-memory-canonical

- [x] Package root contains `SKILL.md`
- [x] Package root contains required shipped scripts under `scripts/`
- [x] Package root contains required references used by the skill
- [x] Package root contains `.clawhubignore`
- [x] Package root contains `CHANGELOG.md`
- [x] Package root contains `UPGRADE.md`
- [x] Package root contains publish evidence under `references/verification-evidence.md` and `references/reference-test-log.md`
- [x] `.clawhubignore` excludes local or transient publish noise (`*.tmp`, `*.pending`, `*.lock`, package-local `.clawhub/` metadata)
- [x] Skill heading version matches the intended published version
- [x] Publish-facing docs and shipped script contracts were rechecked together for this release
- [x] Installed-runtime vs packaged-skill re-sync contract is documented for post-update safety
- [x] Frozen tag vocabulary and `health-check.sh` remain synchronized for this release
- [x] No unresolved publish blocker remains from the latest accepted dual-thinking round
