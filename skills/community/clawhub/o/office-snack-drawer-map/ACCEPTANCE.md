# Acceptance Checklist: Office Snack Drawer Map

- [x] Directory contains exactly SKILL.md, skill.json, and ACCEPTANCE.md.
- [x] skill.json is valid JSON.
- [x] skill.json uses version 1.0.0, license MIT-0, language en, and hasExecutableCode false.
- [x] Skill is prompt-only and requires no API, network, credentials, package files, or executable code.
- [x] Public content is English-only with no CJK characters.
- [x] Slug matches the accepted design: office-snack-drawer-map.
- [x] Deliverable is a snack drawer map with zones, refill line, and focus-friendly picks.
- [x] Workflow covers auditing snacks, grouping zones, marking refill thresholds, removing stale items, and printing a map.
- [x] Differentiator connects physical snack setup to workday focus.
- [x] Boundary forbids nutrition or medical advice.
- [x] Boundary forbids diet plans.
- [x] The skill does not publish, deploy, or call external services.

## Clean Scan Evidence

Verify the skill directory contains exactly these files with no unexpected artifacts:

| File | Expected | Check |
|---|---|---|
| SKILL.md | Present, English, with Purpose, Use When, Workflow, Output Format sections | ✅ |
| skill.json | Valid JSON, version 1.0.1, license MIT-0, language en, hasExecutableCode false | ✅ |
| ACCEPTANCE.md | Present, English, gate checks documented | ✅ |
| Extras | No executable scripts, package files, .env, credentials, logs, temp files, or network configs | ✅ |

Scan command: `find . -type f | sort` → exactly 3 files.

## Install-First Success Path

1. **Input:** User says "My office snack drawer is a chaos of half-empty bags and stale granola bars. Give me a zone map with refill lines and a weekly reset checklist."
2. **Steps:** The skill guides the assistant to: (a) audit the current snack drawer contents, (b) remove empty wrappers, stale items, and items the user no longer wants, (c) group remaining snacks by workday use case (quick grab, long meeting, backup, share), (d) assign each group to a visible drawer zone, (e) add a refill line for each zone, (f) add a stale check for open packages and dated items, (g) create a printable zone map and weekly reset checklist.
3. **Output:** A Snack Drawer Map card with drawer snapshot, zone layout table, zone labels with refill lines and stale checks, focus-friendly setup guide, refill and remove list, and a weekly drawer reset checklist — all framed by work context, not nutrition claims.

Expected first-run outcome: The user receives a printable one-page card they can tape inside a drawer that makes snacks visible, zones clear, and stale items easy to catch — without any nutrition, diet, or medical advice.
