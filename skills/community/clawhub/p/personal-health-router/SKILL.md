---
name: personal-health-router
description: 帮助记录每餐摄入、睡眠质量以及运动锻炼恢复情况，并提供全自动飞书持久化与报表引擎。 Track meals, sleep quality, and workouts with automated Feishu persistence and reporting. Use when the user asks to log calories, analyze meal photos, interpret sleep or recovery screenshots, extract workout metrics, bootstrap health tables, or rebuild monthly/weekly health summaries and dashboards.
---

# Health Copilot: Eating, Sleep, and Exercise Tracking

Use this skill as the central hub for personal health tracking, analysis, and Feishu reporting.

## Overview

This skill is for practical personal-health management, not medical diagnosis.
It provides a unified layer for:
- **Recognition**: Analyzing food photos, sleep screenshots, and workout summaries.
- **Persistence**: Mapping and writing results into a structured Feishu Bitable.
- **Reporting**: Rebuilding daily/weekly summary records and monthly dashboards.

## Role & Workflow

1.  **Classify**: Identify if the request is about nutrition, sleep, exercise, or cross-domain reporting.
2.  **Analyze**: Perform domain-specific extraction or analysis (conservative and evidence-based).
3.  **Persist**: Map the results into the target Feishu schema (default English-only).
4.  **Automate**: Run maintenance scripts for monthly/weekly summaries when requested.

## Routing branches

### 1. Nutrition
- Trigger: `log calories`, `nutrition analysis`, meal photos, bento photos.
- Reference: `references/nutrition.md`.
- Behavior: Analyze photo -> Estimate nutrients -> Upsert to Nutrition Meals table.

### 2. Exercise
- Trigger: `log workout`, `exercise analysis`, app screenshots (Garmin, Strava, Apple Health).
- Reference: `references/exercise.md`.
- Behavior: Analyze screenshot -> Extract metrics -> Assess load -> Upsert to Workouts table.

### 3. Sleep
- Trigger: `log sleep`, `sleep analysis`, `recovery status`, app screenshots (AutoSleep, Oura, etc.).
- Reference: `references/sleep.md`.
- Behavior: Analyze screenshot -> Extract stages/HRV -> Upsert to Sleep Recovery table.

### 4. Cross-domain / Reporting
- Trigger: `weekly health review`, `rebuild calendar`, `refresh dashboard`, `monthly summary`.
- Reference: `references/cross-domain.md`.
- Behavior: Rebuild Monthly Health Calendar -> Rebuild Weekly Health Assessment -> Refresh Dashboard.

## Universal rules

- **Internal Schema**: Always target the **English-only** internal schema for persistence to ensure script reliability.
- **Config-Driven**: Use `references/config-template.md` and `scripts/config_loader.py` for all environment variables.
- **Conservative Analysis**: Extract only what is visible; do not fake precision.
- **Separation**: Keep analysis facts separate from interpretive suggestions.

## Output rule

Default response shape:
1. Conclusion (what was analyzed/updated)
2. Evidence (the data points)
3. Uncertainty (missing info)
4. Next step (action or report link)

## Script mapping

- `scripts/bootstrap_health_tables.js`: Create tables/fields.
- `scripts/rebuild_monthly_calendar.py`: Aggregate daily rows.
- `scripts/rebuild_weekly_assessment.py`: Generate weekly reports.
- `scripts/build_monthly_dashboard.js`: Create/refresh dashboards.

## Installation

```bash
clawdhub install personal-health-router
```
