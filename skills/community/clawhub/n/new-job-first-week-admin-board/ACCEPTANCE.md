# Acceptance Checklist

- [x] SKILL.md has valid YAML frontmatter.
- [x] skill.json is present and valid JSON.
- [x] Version is 1.0.0 and license is MIT-0.
- [x] Language is English only.
- [x] Prompt-only metadata is present: promptOnly true, hasExecutableCode false, requires_api false, requiresApi false, no_code_execution true, execution noExec.
- [x] No executable code, scripts, package files, automation hooks, API requirements, credential needs, or network requirements.
- [x] Directory contains exactly SKILL.md, skill.json, and ACCEPTANCE.md.
- [x] Boundary prohibits passwords, passcodes, recovery codes, identity numbers, tax values, bank details, payroll values, medical details, immigration details, background-check details, and sensitive HR data.
- [x] Boundary uses safe metadata only: category, owner, deadline, status, next action, support path, and secure official location.
- [x] Deliverable is a first-week admin board with access, forms, equipment, meetings, questions, deadlines, blockers, and follow-ups.
- [x] Workflow covers privacy rules, safe context collection, first-week lanes, access tracking, forms tracking, equipment tracking, meeting mapping, blocker flagging, question drafting, and final board creation.
- [x] Board supports Before Day 1, Day 1, Days 2-3, Days 4-5, Waiting On, Questions, and Done lanes.
- [x] Slug matches the accepted design: new-job-first-week-admin-board.

## Clean Scan Evidence

- [x] Secrets scan: no API keys, tokens, passwords, or credentials found.
- [x] Executable scan: no scripts, binaries, or executable code present.
- [x] Network scan: no outbound calls, fetch, or API endpoints.
- [x] File audit: only SKILL.md, skill.json, and ACCEPTANCE.md; no temp, logs, or build artifacts.
- [x] Language audit: English only; no CJK or mixed-script content.
- [x] Claims audit: all gate check claims verifiable against file contents.

## Install-First Success Path

- **Input:** User says "Build a first-week admin board for my new job starting Monday."
- **Steps:**
  1. Agent reads SKILL.md, asks for start date, work mode, manager, IT contact, equipment list, access categories, and known first-week schedule.
  2. Agent sorts items into Before Day 1, Day 1, Days 2-3, Days 4-5, Waiting On, Questions, and Done lanes — tracking access, forms, equipment, meetings, and blockers with safe metadata only.
  3. Agent produces the First-Week Snapshot, Board Lanes, Access Tracker, Forms and HR Tasks, Equipment and Workspace, Meetings/Prep, Questions to Ask, Blocker Escalation List, and End-of-Week Reset.
- **Output:** A practical first-week admin board with access requests, form tracking (categories only — no sensitive values), equipment status, meeting prep, a polite question list for HR/IT/manager, and blocker escalation paths — all tracked with owners and deadlines, never storing passwords, IDs, bank details, or sensitive HR data.
