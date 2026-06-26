# Changelog

## v1.0.0 — 2026-03-04

Initial release. Built from a real binding loss + gateway crash investigation session.

**Phases:**
- Phase 0: Triage (current state check)
- Phase 1: Evidence (4-source collection — backups, git, session logs, diffs)
- Phase 2: 5 Whys (evidence-backed root cause)
- Phase 3: Restore (merge from backup, verify)
- Phase 4: Prevention (6 patterns: config guard, SOUL.md rule, rules.md, git audit, valid keys guard, chmod)
- Phase 5: Monitor (cron template, auto-escalate logic)
- Phase 6: Document (learnings/rules.md)

**References:**
- `references/checklists.md` — 6 failure type checklists
- `references/prevention-patterns.md` — 6 prevention patterns with code
- `references/cron-template.md` — monitoring cron template

**Versioning:**
- Patch (1.0.x): checklist updates, new failure type, command fixes
- Minor (1.x.0): new prevention pattern, new phase, structural changes
- Major (x.0.0): workflow redesign
