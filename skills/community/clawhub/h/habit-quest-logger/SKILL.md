---
name: habit-quest-logger
description: Turn habit building into a quest log with daily mission tiers, streak feedback, fallback actions, and recovery guidance after missed days. Use when the user wants to build or restart 1 to 5 habits with lower friction and more visible progress.
---

# Habit Quest Logger

Chinese name: 习惯养成任务日志

## Purpose
Turn dull habit tracking into a quest log with clear mission tiers, visible streak feedback, and a shame-free reset path.
This skill is descriptive only. It does not create reminders, sync data, or call external APIs.

## Use this skill when
- The user wants to track 1 to 5 habits in a more motivating way.
- The user keeps quitting after one missed day and needs a recovery loop.
- The user wants a daily mission board instead of vague habit intentions.
- The user needs a low-friction way to restart consistency.

## Inputs to collect
- Habit name
- Frequency or cadence
- Target duration or minimum version
- Main difficulty or friction point
- Current streak or recent consistency
- Today's energy, time, or constraints

## Workflow
1. Collect up to 5 habits and clarify frequency, duration, difficulty, and current streak.
2. Rewrite each habit as a main quest, side quest, and minimum fallback quest.
3. Pick only one main quest for today and keep the rest as support or backup actions.
4. Define how experience points are earned, what counts as success, and what the user should do after a miss.
5. If the user has been using the system for several days, add streak protection, difficulty adjustment, and a return-to-game rule.

## Output Format
- Today's quest log with the exact action and completion line.
- Streak status with current days, current level, and next level condition.
- Failure recovery move with the smallest comeback action.
- End-of-day settlement line with short positive reinforcement.

## Quality bar
- Default to one main quest and only a small number of fallback actions.
- Every habit must have a concrete completion standard.
- Always include a recovery mechanism after misses.
- Keep the plan within the user's real capacity for today.

## Edge cases and limits
- If the user lists too many habits, compress scope and keep only the highest-value ones active.
- If the goal is vague, translate it into observable behavior before building the quest log.
- Do not position this skill as therapy, medical care, or hard accountability enforcement.

## Compatibility notes
- Accepts free-form Chinese or English input, plus semi-structured habit details.
- Works for one-off daily planning or repeated day-by-day iteration.
- Can pair conceptually with habit-tracker or daily-dungeon-challenger, but it does not depend on other tools.
