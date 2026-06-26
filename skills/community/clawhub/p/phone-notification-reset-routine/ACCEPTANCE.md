# Acceptance Checklist

- [x] SKILL.md has valid YAML frontmatter.
- [x] skill.json is present and valid JSON.
- [x] Version is 1.0.0 and license is MIT-0.
- [x] Language is English only.
- [x] Prompt-only metadata is present: promptOnly true, hasExecutableCode false, requires_api false, no_code_execution true, execution noExec.
- [x] No executable code, scripts, package files, automation hooks, API requirements, credential needs, or network requirements.
- [x] Directory contains exactly SKILL.md, skill.json, and ACCEPTANCE.md.
- [x] Boundary keeps the skill to attention hygiene only.
- [x] Boundary excludes account handling, credentials, private message review, surveillance, monitoring, tracking, device management, parental controls, and workplace controls.
- [x] Deliverable is a 20-minute notification audit card.
- [x] Workflow covers noisy app listing, keep/mute/batch decisions, notification surfaces, batch windows, simple rules, and review cadence.
- [x] Slug matches the accepted design: phone-notification-reset-routine.

## Clean Scan Evidence

Verify the skill directory contains exactly these files with no unexpected artifacts:

| File | Expected | Check |
|---|---|---|
| SKILL.md | Present, English, YAML frontmatter with name/description/version/type/tags/author | ✅ |
| skill.json | Valid JSON, version 1.0.0, license MIT-0, language en, hasExecutableCode false | ✅ |
| ACCEPTANCE.md | Present, English, gate checks documented | ✅ |
| Extras | No executable scripts, package files, .env, credentials, logs, temp files, or network configs | ✅ |

Scan command: `find . -type f | sort` → exactly 3 files.

## Install-First Success Path

1. **Input:** User says "My phone buzzes constantly and I can't focus during work hours. Help me do a 20-minute notification reset."
2. **Steps:** The skill guides the assistant to: (a) set the reset goal and protect must-ring alerts, (b) list noisy apps by memory, (c) assign each app to keep/mute/batch/badge-only/quiet, (d) reduce notification surfaces, (e) create intentional batch windows, (f) write simple rules, (g) return the reset card with review plan.
3. **Output:** A phone notification reset card with reset goal, do-not-disturb list, noisy app audit, 20-minute reset sequence, notification rules, lock screen cleanup, and review plan — all within attention hygiene, no account or surveillance setup.

Expected first-run outcome: The user completes a 20-minute notification audit, receives a clear reset card, and experiences immediate calm with preserved critical alerts.
