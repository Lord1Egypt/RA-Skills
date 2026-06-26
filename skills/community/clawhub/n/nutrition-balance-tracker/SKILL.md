---
name: nutrition-balance-tracker
description: Track daily nutrition intake, hydration, and energy balance against fat-loss, maintenance, or muscle-gain goals. Use when the user wants to log meals, water, or exercise, review daily calories and nutrients, and judge whether protein, carbs, fat, fiber, sodium, sugar, and total energy are balanced. Provides estimates and practical guidance, not medical advice.
---

# Nutrition Balance Tracker

## Overview

Use this skill to help the user track daily meals, hydration, exercise burn, and overall nutrition balance for fat loss, maintenance, or muscle gain. Keep the interaction lightweight, estimate conservatively, and focus on practical next-step guidance instead of pseudo-medical certainty.

This skill supports:
- meal, snack, and drink logging
- hydration tracking
- daily energy balance analysis
- macro and key nutrition checks
- actionable next-step guidance

## Workflow

### 1. Clarify the evaluation frame
First determine the minimum context needed for a useful answer:
- user goal: `fat_loss`, `maintain`, or `muscle_gain`
- whether the user wants a partial-day check or full-day review
- what has been eaten, drunk, and exercised so far

If core facts are missing, ask only the 1–3 highest-impact questions first. Use `references/intents-and-prompts.md` for trigger examples, follow-up priority, and low-confidence confirmation strategy.

### 2. Build or update the user profile
If the user wants target-based judgment and profile data is missing, ask for:
- age
- sex
- height in cm
- weight in kg
- activity level
- goal intensity when relevant

If the user already provides their own calorie or macro targets, prefer those over default estimates.

### 3. Estimate daily targets
When no explicit user targets are provided, estimate them with:
- `scripts/calculate_targets.js`
- `references/nutrition-targets.md`

Default principles:
- use BMR + activity multiplier for maintenance estimates
- apply conservative surplus/deficit rules by goal
- prioritize protein adequacy
- treat sodium and sugar as upper-limit checks
- treat water and fiber as minimum-target checks

### 4. Estimate intake
Convert food logs into nutrition totals with:
- `scripts/calculate_intake.js`
- `scripts/food_db.json`

Rules:
- use approximate household units when exact grams are unavailable
- if a food is missing from the built-in database, say so clearly
- if quantity or cooking method is unclear, mark the result as estimated
- do not pretend restaurant or takeout entries are precise

### 5. Estimate burn
Estimate energy burn with:
- `scripts/calculate_burn.js`

Include:
- BMR
- non-exercise activity from activity multiplier
- exercise burn from type, duration, and intensity

Use conservative estimates. Do not over-credit exercise.

### 6. Evaluate balance
Judge the day with:
- `scripts/evaluate_balance.js`

Evaluate at least:
- energy balance versus goal
- protein
- carbs
- fat
- fiber
- water
- sodium
- sugar

Use simple human-readable states such as:
- 合理 / 略低 / 偏低 / 略高 / 偏高
- 赤字合理 / 赤字过大 / 盈余合理 / 盈余过大

### 7. Format the response
Generate a clear result with:
- `scripts/format_report.js`
- `references/output-template.md`

Keep the response compact and useful:
- today summary
- calorie balance
- nutrient status
- top 1–3 issues
- next-step suggestions
- disclaimer

If confidence is low, explicitly label the result as an estimate and name the main uncertainty source.

## Output Rules

- Prefer practical guidance over theory.
- Do not overwhelm the user with every possible metric.
- Highlight the 1–3 most important adjustments.
- Avoid alarmist wording.
- Never present the result as diagnosis, treatment, or medical nutrition therapy.

## Resources

### scripts/
- `calculate_targets.js`: estimate BMR, calorie target, and daily macro targets
- `calculate_intake.js`: total food and hydration intake from simple structured entries
- `calculate_burn.js`: estimate daily burn from profile and exercise entries
- `evaluate_balance.js`: classify balance status and produce alerts/suggestions
- `format_report.js`: render the final user-facing report
- `food_db.json`: small built-in food reference for common foods

### references/
- `intents-and-prompts.md`: trigger examples and missing-info follow-up rules
- `output-template.md`: user-facing output template
- `nutrition-targets.md`: default daily target and balance ranges
- `safety-boundaries.md`: language, safety, and medical-boundary rules

## Disclaimer

This skill provides general nutrition-tracking guidance only. It does not provide medical diagnosis, treatment, or individualized clinical nutrition advice. If the user mentions a medical condition, pregnancy, eating disorders, or other high-risk contexts, keep advice general and recommend professional support.
