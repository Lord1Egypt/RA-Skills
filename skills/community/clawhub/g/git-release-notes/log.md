# Git Release Notes — Log

## 2026-03-26

### Done
- Created skill with init_skill.py (scripts resource)
- Wrote SKILL.md: workflow, commit categorization table, 4 output formats (GitHub, compact, keepachangelog, Slack)
- Wrote scripts/gather_commits.sh — extracts commits as JSON with hash, author, date, subject, body
- Tested against Express.js repo (8 commits) — clean JSON output with conventional commit subjects
- Validated and packaged to dist/git-release-notes.skill

### Decisions
- Bash + Python hybrid script: bash for git commands, Python for JSON serialization
- Conventional commit prefix recognition for categorization
- 4 format options: GitHub release, compact, Keep a Changelog, Slack/Discord
- Agent does the categorization and formatting (not the script) — more flexible
- Price: $49 (dev tool, straightforward value prop)

### Blockers
- None
