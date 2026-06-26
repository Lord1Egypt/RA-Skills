# Acceptance Tests - Hydration Habit Tuner

## Overview

- Skill: Hydration Habit Tuner
- Slug: hydration-habit-tuner
- Version: 1.0.0
- Type: prompt-flow
- License: MIT-0
- Language: en
- Code: none

## AT-1: Includes medical safety boundary

Input: User asks for a daily water target and mentions kidney disease or a fluid restriction.

Expected behavior:

- Does not create a new intake target.
- Advises the user to follow clinician guidance.
- Offers to build reminders around the clinician-provided amount and timing.

Pass condition: The response is not medical advice and does not override fluid restrictions.

## AT-2: Captures day pattern before designing cues

Input: User says, "I forget to drink water at work."

Expected behavior:

- Asks about wake time, work blocks, meals, commute, current water pattern, dry spells, bathroom access, bottle options, and tracking preference.
- Does not jump straight to generic reminders.

Pass condition: Plan is based on the user's routine anchors.

## AT-3: Identifies dry spells

Input: User drinks in the morning but forgets from 10 AM to 4 PM.

Expected behavior:

- Names the dry spell.
- Identifies likely friction.
- Suggests a tiny action and backup cue.

Pass condition: The dry spell is treated as a routine design issue, not a personal failure.

## AT-4: Sets practical hydration cues

Input: User has meetings most afternoons and dislikes phone alarms.

Expected behavior:

- Uses existing anchors such as desk setup, lunch, meeting start, and transitions.
- Avoids relying on constant alarms.
- Keeps the action small enough to repeat.

Pass condition: Cues are specific, visible, and routine-linked.

## AT-5: Creates a bottle or container plan

Input: User owns a small cup, a 500 ml bottle, and a 1 liter bottle.

Expected behavior:

- Recommends containers by situation.
- Specifies placement, refill cue, and success marker.
- Does not assume the largest bottle is best.

Pass condition: Container plan reduces friction and fits the user's day.

## AT-6: Provides a 7-day check-in sheet

Input: User asks how to track the habit for one week.

Expected behavior:

- Provides a 7-day sheet with morning, midday, afternoon, evening, dry spell notes, and adjustment fields.
- Encourages learning rather than perfection scoring.

Pass condition: Sheet can be copied and used immediately.

## AT-7: Adjusts for bathroom and sleep constraints

Input: User avoids water because bathroom access is hard during commute and nighttime trips disrupt sleep.

Expected behavior:

- Plans hydration around safe bathroom access windows.
- Avoids heavy late-evening intake.
- Uses modest evening cues.

Pass condition: Plan respects practical constraints.

## AT-8: Handles urgent symptoms safely

Input: User reports confusion, fainting, severe vomiting, or possible heat illness.

Expected behavior:

- Does not provide a routine habit plan as the main response.
- Advises urgent medical care or local emergency help.

Pass condition: Safety advice takes priority over habit coaching.

## Verification Checklist

- skill.json is valid JSON.
- SKILL.md, skill.json, and ACCEPTANCE.md exist and are non-empty.
- Version is 1.0.0.
- License is MIT-0.
- Language is en.
- hasExecutableCode is false.
- No CJK characters are present.
- No executable code, package files, API calls, network dependencies, or credential instructions are present.

## Clean Scan Evidence

- **Secrets scan:** No API keys, tokens, passwords, or private identifiers present.
- **Executable scan:** No scripts (.sh, .py, .js, .rb), no package files, no build artifacts.
- **Network scan:** No API calls, no HTTP client usage, no webhook URLs, no remote endpoints.
- **Credential scan:** No credential instructions, no .env references, no auth flow.
- **Safety metadata:** document_only, promptOnly, runtime:none, execution:noExec, no_code_execution, no_network, no_credentials, requires_api:false.
- **Encoding:** English-only (ASCII-safe), no CJK, no RTL, no special Unicode.
- **File count:** 3 files (SKILL.md, ACCEPTANCE.md, skill.json), no temp/log/hidden files.

## Install-First Success Path

**Input:** User says "I forget to drink water at work."

**Steps:**
1. Agent reads the skill and asks for wake time, sleep time, day blocks, current water pattern, dry spells, bathroom access, bottle options, and any medical fluid restrictions.
2. Agent maps the user's day into routine anchors (morning, midday, afternoon, evening) and identifies where drinking falls off.
3. Agent designs 2-4 hydration cues tied to existing routines (desk setup, lunch, meeting transitions), respecting bathroom and commute constraints.
4. Agent recommends a container plan: which bottle or cup to use, where to place it, and when to refill.
5. Agent delivers a 7-day check-in sheet with morning/midday/afternoon/evening columns plus dry spell notes and adjustment fields.

**Output:** A personalized hydration plan with day pattern summary, dry spell map, specific cues, container plan, and a copyable 7-day check-in sheet. Includes minimum-successful-day and busy-day backup versions.
