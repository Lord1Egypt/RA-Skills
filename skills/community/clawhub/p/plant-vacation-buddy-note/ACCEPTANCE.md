# Acceptance Checklist: Plant Watering Vacation Buddy Note

- [x] Directory contains exactly SKILL.md, skill.json, and ACCEPTANCE.md.
- [x] skill.json is valid JSON.
- [x] skill.json uses version 1.0.0, license MIT-0, language en, and hasExecutableCode false.
- [x] Skill is prompt-only and requires no API, network, credentials, package files, or executable code.
- [x] Public content is English-only with no CJK characters.
- [x] Slug matches the accepted design: plant-vacation-buddy-note.
- [x] Deliverable is a room-by-room plant note with water amount, timing, and photo slots.
- [x] Workflow covers identifying plants, grouping by room, setting water amounts, adding warnings, and handoff.
- [x] Differentiator is quick vacation sitter handoff rather than general plant care.
- [x] Boundary forbids toxic plant claims and invented care instructions.
- [x] Includes skip-if-unsure instruction for unclear plants, amounts, or conditions.
- [x] The skill does not publish, deploy, or call external services.

## Clean Scan Evidence

- SKILL.md: English only, no CJK/non-ASCII characters, no secrets, no credentials, no API keys, no tokens, no passwords, no personal data.
- skill.json: valid JSON, English only, all required safety fields present (hasExecutableCode: false, requires_api: false, no_network: true, no_credentials: true, no_code_execution: true).
- ACCEPTANCE.md: English only, no secrets, no executable content.
- Directory: exactly 3 files (SKILL.md, skill.json, ACCEPTANCE.md). No package files, scripts, binaries, .env, .git, node_modules, or hidden configs.
- No executable code, no network calls, no API dependencies, no credential requirements.

## Install-First Success Path

1. **Input:** User provides travel dates, plant locations by room, plant names or labels, water amounts, and watering timing preferences.
2. **Steps:** Skill groups plants by room, assigns short labels, records water amounts and timing only from owner input, adds skip-if-unsure safeguards, creates a sitter visit checklist, adds photo slots, and produces a friendly handoff note.
3. **Output:** A printable room-by-room plant watering buddy note with plant labels, water amounts, timing, skip-if-unsure instructions, sitter checklist, photo slots, and a handoff message.
