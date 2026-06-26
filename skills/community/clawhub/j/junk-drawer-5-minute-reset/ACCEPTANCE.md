# Acceptance Checklist: Junk Drawer 5-Minute Reset Card

- [x] Directory contains exactly SKILL.md, skill.json, and ACCEPTANCE.md.
- [x] skill.json is valid JSON.
- [x] skill.json uses version 1.0.0, license MIT-0, language en, and hasExecutableCode false.
- [x] Skill is prompt-only and requires no API, network, credentials, package files, or executable code.
- [x] Public content is English-only with no CJK characters.
- [x] Slug matches the accepted design: junk-drawer-5-minute-reset.
- [x] Deliverable is a timer-based reset card with keep, move, trash, and caution micro-zones.
- [x] Workflow covers setting a timer, pulling obvious trash, grouping useful items, assigning micro-zones, and adding a reset date.
- [x] Differentiator is a five-minute visible win, not a major declutter project.
- [x] Boundary keeps the scope to a micro reset only.
- [x] Boundary reminds the user to handle sharp or unknown items carefully.
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

1. **Input:** User says "My kitchen junk drawer won't close. Give me a 5-minute reset card — I need visible progress before dinner."
2. **Steps:** The skill guides the assistant to: (a) set a five-minute timer as the stop rule, (b) scan for sharp, unknown, leaking, broken, battery, chemical, or fragile items before touching, (c) pull only obvious trash and empty packaging, (d) group useful items into a keep zone, (e) place items that belong elsewhere into a move zone, (f) create a small caution zone for items needing later review, (g) assign micro-zones inside the drawer, (h) add a reset date and stop when the timer ends.
3. **Output:** A Junk Drawer 5-Minute Reset Card with drawer location, timer plan (minute-by-minute), micro-zone layout (keep here, move elsewhere, trash, caution review), drawer map, keep/move/trash list, and a reset label the user can tape inside the drawer.

Expected first-run outcome: The user receives a printable one-page timer card that turns an overwhelming junk drawer into a micro-organized space in exactly five minutes — without expanding into a whole-home declutter project.
