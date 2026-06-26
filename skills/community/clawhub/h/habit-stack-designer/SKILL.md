---
name: habit-stack-designer
description: Design a habit stack by choosing a reliable existing anchor, shrinking the new habit into a tiny first action, and adding friction reduction, reward, and a rescue version for hard days. Use when the user wants to build a habit without relying on memory, motivation spikes, or giant behavior changes.
---

# Habit Stack Designer

## Overview

Use this skill to attach a new habit to an existing routine instead of hoping motivation will carry it. It helps the user find a stable anchor, make the first action tiny enough to start, and design friction removal plus a rescue version for bad days.

This skill is descriptive only. It does not create reminders or automation.

## Trigger

Use this skill when the user wants to:
- build a new habit that actually sticks
- choose a strong anchor habit instead of relying on memory
- shrink a habit into a tiny under-two-minute version
- create an explicit habit stack formula
- add a rescue version for low-energy days

### Example prompts
- "Help me stack a meditation habit onto something I already do"
- "Design a tiny reading habit after dinner"
- "I keep forgetting my new habit, can you attach it to a stable routine?"
- "Turn this big habit goal into a stack formula"

## Workflow

1. Identify the target habit and why it matters.
2. Find an existing routine that already happens predictably.
3. Evaluate whether the anchor is frequent and reliable.
4. Shrink the new habit into a tiny first action.
5. Write the habit stack formula.
6. Add friction reduction, reward, and a rescue version.
7. Scale only after consistency exists.

## Inputs

The user can provide any mix of:
- target habit
- reason or identity behind the habit
- daily routines that already happen
- time or place cues
- schedule constraints
- prior failure patterns
- desired reward or review rhythm

## Outputs

Return a markdown habit stack design with:
- target habit and why it matters
- best anchor and why it is reliable
- explicit stack formula
- friction removal ideas
- reward loop
- rescue version for hard days

## Safety

- Prefer anchors the user already performs several times per week.
- Start tiny enough to avoid negotiation.
- Avoid stacking many new behaviors onto one weak anchor.
- Irregular schedules may need place-based anchors rather than clock-based ones.

## Acceptance Criteria

- Return markdown text.
- Include a clear anchor and explicit stack formula sentence.
- Keep the starting action tiny and realistic.
- Include both friction removal and a rescue version.
