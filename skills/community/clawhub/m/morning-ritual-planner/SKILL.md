---
name: morning-ritual-planner
description: Build a realistic morning routine around the user's real wake time, time budget, reliable anchor, night-before prep, and fallback plan for chaotic or low-sleep mornings. Use when the user wants a calmer, clearer, or more energized start without copying unrealistic influencer routines or relying on app automation.
---

# Morning Ritual Planner

## Overview

Use this skill to turn a vague wish for a better morning into a practical ritual that matches real life. It keeps the routine honest by starting from the user's actual wake time, existing obligations, and one anchor they already perform reliably.

This skill is descriptive only. It does not set alarms, start timers, or connect to calendars, wearables, or reminder apps.

## Trigger

Use this skill when the user wants to:
- design a morning ritual that fits a 10, 20, 30, or 45 minute window
- stop overbuilding a routine they cannot sustain
- adapt a morning plan to family, commute, caregiving, or work constraints
- create a shorter fallback version for late or low-sleep mornings
- add night-before prep so the routine feels easier to start

### Example prompts
- "Help me build a realistic 20 minute morning routine before the school run"
- "I want a calmer morning, but I only have 10 minutes"
- "Create a fallback morning ritual for days when I wake up tired"
- "Design a focused morning routine around coffee and journaling"

## Workflow

1. Capture the user's real wake time, desired morning feeling, and hard constraints.
2. Identify a reliable anchor, such as getting out of bed, brushing teeth, or making coffee.
3. Build the routine in layers: must-do, nice-to-have, and bonus.
4. Fit the sequence to an honest time budget.
5. Add one or more night-before prep steps that reduce friction.
6. Create a fallback version for chaotic or low-energy mornings.
7. End with a short weekly review prompt so the routine can evolve.

## Inputs

The user can provide any mix of:
- wake time or target wake window
- available morning time
- desired feeling, such as calm, focused, grounded, or energized
- existing anchor habit
- family, commute, work, school, or caregiving constraints
- preferred activities, such as stretching, tea, journaling, reading, or movement
- sleep quality or low-energy context

## Outputs

Return a markdown plan with:
- goal summary
- wake-up anchor and honest time budget
- ritual sequence with durations and why each step stays
- night-before prep list
- fallback version for hard mornings
- weekly review questions

## Safety

- Keep the plan realistic for the user's current life, not an aspirational fantasy schedule.
- Protect sleep. If the user sounds chronically sleep deprived, shorten the ritual before adding more activities.
- Prefer interruptible routines for caregivers or chaotic households.
- Do not claim the routine will guarantee productivity, mood, or discipline.

## Acceptance Criteria

- Return markdown text.
- Include one reliable anchor, one night-before prep step, and one fallback version.
- Keep the total duration realistic for the stated time budget.
- Make it obvious what a successful normal morning looks like.
