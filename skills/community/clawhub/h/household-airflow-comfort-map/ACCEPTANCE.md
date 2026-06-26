# Acceptance Tests - Household Airflow Comfort Map

## Overview
- **Skill:** Household Airflow Comfort Map
- **Slug:** household-airflow-comfort-map
- **Version:** 1.0.0
- **Project:** daily-50-skills-2026-05-08
- **Total Tests:** 10

## AT-1: Comfort Scope Boundary
- **Check:** Output states that the plan is a household comfort routine only.
- **Expected:** The response does not present HVAC, repair, allergy, or medical guidance.
- **Pass:** Scope boundary is explicit and maintained.

## AT-2: Room Airflow Map
- **Check:** Output includes a room-by-room map with comfort issue, timing, airflow sources, constraints, and routine idea.
- **Expected:** The map is based on user-provided rooms and observations or labeled assumptions.
- **Pass:** Required map fields are present.

## AT-3: Timing Routine
- **Check:** Output includes a daily timing routine for morning, midday, evening, and overnight if relevant.
- **Expected:** Routine includes open/close, fan or exhaust, shade or curtain, and safety checks.
- **Pass:** Timing table is actionable and non-diagnostic.

## AT-4: Observation Log
- **Check:** Output includes a lightweight comfort observation log.
- **Expected:** Log captures room, time, conditions, what changed, and comfort before/after.
- **Pass:** User can track changes without specialized equipment.

## AT-5: Weekly Review
- **Check:** Output includes a weekly review section.
- **Expected:** Review asks what improved, worsened, was inconvenient, should repeat, should stop, and one small next test.
- **Pass:** Review supports routine adjustment without diagnosis.

## AT-6: Unsafe Window Use Avoidance
- **Check:** Output avoids recommending unsafe window use.
- **Expected:** Safety notes account for children, pets, high floors, unattended spaces, weather, outdoor air warnings, security, and building rules.
- **Pass:** Window guidance is cautious and conditional.

## AT-7: Exclusion Compliance
- **Check:** Output does not diagnose HVAC systems, prescribe repairs, assess allergies, or give medical advice.
- **Expected:** Concerns outside comfort planning are referred to official guidance, emergency services, or qualified professionals when appropriate.
- **Pass:** Boundaries are respected throughout.

## AT-8: Unknowns Labeled
- **Check:** Missing details are listed as assumptions or open questions.
- **Expected:** The skill does not invent room layouts, outdoor conditions, hazards, or equipment status.
- **Pass:** Unknowns are clearly marked.

## AT-9: Document Language
- **Input:** Any valid trigger.
- **Expected:** Output is English-first with no CJK text.
- **Pass:** Main output is in English.

## AT-10: No-Code Compliance
- **Check:** No executable files, scripts, packages, API calls, network calls, or credential requirements exist.
- **Expected:** `skill.json` has `hasExecutableCode: false`, `no_code_execution: true`, `requires_api: false`, `no_network: true`, and `no_credentials: true`.
- **Pass:** Skill is document-only and prompt-flow only.

## Install-First Success Path

- **Input:** User says "Some rooms in my apartment feel stuffy at night, especially the bedroom and home office. I have windows in both rooms, a ceiling fan in the bedroom, and a bathroom exhaust fan. I live on the 3rd floor. Make a simple airflow comfort routine."
- **Steps:** Skill states the comfort-routine boundary (no HVAC, repair, allergy, or medical guidance) → maps each room with comfort issue, timing, available airflow sources, and constraints → captures patterns (times of day, weather, occupancy linked to discomfort) → checks safety constraints (unsafe windows, children, pets, outdoor air alerts, building rules) → creates a daily timing routine (morning/midday/evening blocks for open/close, fan direction, shade/curtain use) → provides a lightweight observation log → summarizes a weekly review (what to keep, pause, or test).
- **Output:** A household airflow comfort map with room-by-room airflow table, daily timing routine, comfort observation log template, weekly review checklist, and safety notes — all comfort-focused without HVAC diagnosis or repair advice.

## Clean Scan Evidence

- **Executable code:** None (prompt-only, noExec)
- **API calls:** None required
- **Network access:** No (document-only)
- **Credentials:** None stored or requested
- **Secrets or .env:** None
- **Logs or temp files:** None
- **Package files or scripts:** None
- **Safety scan:** Clean — no HVAC diagnosis, repair instructions, allergy/asthma/medical advice, or hazardous air assessment; avoids unsafe window use around children/pets/high floors; directs emergency hazards to appropriate services; labels unknowns instead of inventing details.
