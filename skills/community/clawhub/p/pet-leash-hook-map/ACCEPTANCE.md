# Acceptance Checklist

- [x] SKILL.md has valid YAML frontmatter.
- [x] skill.json is present and valid JSON.
- [x] Version is 1.0.0 and license is MIT-0.
- [x] Language is English only.
- [x] Prompt-only metadata is present: promptOnly true, hasExecutableCode false, requires_api false, no_code_execution true, execution noExec.
- [x] No executable code, scripts, package files, automation hooks, API requirements, credential needs, or network requirements.
- [x] Directory contains exactly SKILL.md, skill.json, and ACCEPTANCE.md.
- [x] Boundary flags secure hooks, chew hazards, and proper harness checks.
- [x] Boundary avoids veterinary advice, medical triage, escape-proof claims, training prescriptions, and product certification claims.
- [x] Deliverable is a hook map plus walk-ready checklist for leash, bags, tag light, towel, backup clip, and reset cues.
- [x] Workflow covers gathering gear, grouping by trip type, mapping hooks, refill cues, chew-hazard controls, pre-walk checks, and one-walk reset testing.
- [x] Slug matches the accepted design: pet-leash-hook-map.

## Clean Scan Evidence

Verify the skill directory contains exactly these files with no unexpected artifacts:

| File | Expected | Check |
|---|---|---|
| SKILL.md | Present, English, YAML frontmatter with name/description/version/tags | ✅ |
| skill.json | Valid JSON, version 1.0.1, license MIT-0, language en, hasExecutableCode false | ✅ |
| ACCEPTANCE.md | Present, English, gate checks documented | ✅ |
| Extras | No executable scripts, package files, .env, credentials, logs, temp files, or network configs | ✅ |

Scan command: `find . -type f | sort` → exactly 3 files.

## Install-First Success Path

1. **Input:** User says "Our dog-walking gear is a mess by the back door. Leashes tangled, poop bags empty, harness missing. I need a hook map and checklist so we're ready to walk in ten seconds."
2. **Steps:** The skill guides the assistant to: (a) gather all walk gear, (b) sort by pet and trip type, (c) inspect condition of straps and clips, (d) choose secure hooks with weight limits in mind, (e) reduce chew hazards by elevating dangling items, (f) add pre-walk fit/condition checks, (g) build a walk-ready checklist with refill cues, (h) deliver the hook map.
3. **Output:** A pet leash hook map with station location, hook assignments by pet/trip type, gear listed per hook, walk-ready checklist, refill cues, chew hazard controls, and return-reset routine.

Expected first-run outcome: The user can grab gear and leave for a walk in under ten seconds without hunting for leashes, bags, or lights — with gear inspected and secure.
