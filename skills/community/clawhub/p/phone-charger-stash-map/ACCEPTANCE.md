# Acceptance Checklist

- [x] SKILL.md has valid YAML frontmatter.
- [x] skill.json is present and valid JSON.
- [x] Version is 1.0.0 and license is MIT-0.
- [x] Language is English only.
- [x] Prompt-only metadata is present: promptOnly true, hasExecutableCode false, requires_api false, no_code_execution true, execution noExec.
- [x] No executable code, scripts, package files, automation hooks, API requirements, credential needs, or network requirements.
- [x] Directory contains exactly SKILL.md, skill.json, and ACCEPTANCE.md.
- [x] Boundary is physical phone charger organization only.
- [x] Boundary avoids device passwords, account information, private device identifiers, location tracking, monitoring setup, surveillance instructions, and account recovery data.
- [x] Required inputs cover rooms, connector types, charger types, pain point, daily-use spots, backup spots, labels, and reset frequency.
- [x] Workflow covers inventory, connector labels, daily stations, backups, return spots, damaged item flagging, visible map, reset routine, and leaving-home check.
- [x] Deliverable is a room-by-room charger stash map with cable type, return spot, backup location, label plan, reset routine, and do-not-use check.
- [x] Slug matches the accepted design: phone-charger-stash-map.

## Clean Scan Evidence

- [x] No secrets: zero passwords, tokens, API keys, or credentials in any file.
- [x] No executable code: zero scripts, binaries, automation hooks, or package files.
- [x] No network or API: no outbound calls, no fetch, no web requests.
- [x] No unsafe claims: no device tracking, no monitoring setup, no surveillance advice, no account recovery.
- [x] No personal data: no device passwords, no Apple/Google account details, no phone numbers, no serial numbers.
- [x] File count: exactly 3 files (SKILL.md, ACCEPTANCE.md, skill.json).
- [x] English/ASCII only: no non-English content, no Unicode issues.
- [x] Document-only: promptOnly=true, hasExecutableCode=false, execution=noExec.

## Install-First Success Path

**Input:** User says "I need a charger stash map for my house" with rooms, connector types (USB-C/Lightning/etc.), and pain points (missing cables, tangled drawer, travel charger gone).

**Steps:**
1. Agent reads the SKILL.md and inventories chargers: wall plugs, cables, wireless pads, power banks, car chargers, travel chargers.
2. Agent labels each by connector type (not by private owner name) and assigns daily-use stations: bedside, desk, kitchen, entry.
3. Agent assigns backup spots: car, travel pouch, backpack, guest area, emergency drawer.
4. Agent creates return spots: each charger gets a home base (pouch, clip, bin, hook).
5. Agent flags damaged items: frayed, hot, sparking, or unreliable chargers marked do-not-use.
6. Agent builds the room-by-room map and adds a weekly reset routine + leaving-home mini check.

**Output:** A room-by-room phone charger stash map with: household charging goal, room-by-room map (charger type, connector, outlet location, return spot), daily-use stations, backup/travel stash, cable type key, label plan, do-not-use check, weekly reset routine, and leaving-home mini check. No passwords, accounts, tracking, or monitoring.
