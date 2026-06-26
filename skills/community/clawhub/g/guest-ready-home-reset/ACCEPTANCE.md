# Acceptance Checklist

- [x] SKILL.md has valid YAML frontmatter.
- [x] skill.json is present and valid JSON.
- [x] Version is 1.0.0 and license is MIT-0.
- [x] Language is English only.
- [x] Prompt-only metadata is present: promptOnly true, hasExecutableCode false, requires_api false, no_code_execution true, execution noExec.
- [x] No executable code, scripts, package files, automation hooks, API requirements, network requirements, or credential requirements.
- [x] Deliverable includes a 60-minute reset plan, supplies list, quick task assignments, guest essentials, and welcome note template.
- [x] Workflow covers choose guest type, prioritize zones, assign quick tasks, prepare essentials, and create welcome note.
- [x] Safety boundary includes privacy, allergy, scent sensitivity, pet exposure, cleaning chemical, and trip-hazard prompts.
- [x] Scope stays on fast visible prep rather than unrealistic deep cleaning.
- [x] Slug matches the accepted design: guest-ready-home-reset.

## Clean Scan Evidence

- [x] No executable code, scripts, binaries, or package files.
- [x] No secrets, credentials, API keys, tokens, or environment variables.
- [x] No network calls, API endpoints, or internet dependencies.
- [x] No CJK characters. Documentation is English/ASCII only.
- [x] `skill.json` is valid JSON with `version=1.0.0`, `license=MIT-0`, `language=en`, `hasExecutableCode=false`.
- [x] File count is exactly 3: `SKILL.md`, `skill.json`, `ACCEPTANCE.md`.
- [x] No temp files, log files, or build artifacts.

## Install-First Success Path

**Input:** "Guests are coming in an hour. Help me make the house look ready."

**Steps:**
1. Skill asks about guest type, arrival time, rooms in use, helpers available, and known allergies/concerns.
2. Skill prioritizes visible zones (entry, bathroom, seating, kitchen), assigns quick surface/clutter/supply tasks.
3. Skill produces a 60-minute reset plan, supplies list, guest essentials list, and welcome note template.

**Output:** A guest-ready home reset plan with zone priorities, 60-minute task timeline, supplies checklist, guest essentials, privacy protection notes, and a welcome note draft.
