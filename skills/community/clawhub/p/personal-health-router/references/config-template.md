# Config Template

Use a config file for every environment. Never hardcode private tokens or table IDs into scripts.

## Required shape

```json
{
  "feishu": {
    "active_base": {
      "token": "<base_token>",
      "url": "<optional_base_url>"
    },
    "tables": {
      "nutrition_meal": { "name": "Nutrition Meals", "table_id": "<optional_existing_id>" },
      "nutrition_daily_history": { "name": "Nutrition Daily History", "table_id": "<optional_existing_id>" },
      "sleep_recovery": { "name": "Sleep Recovery", "table_id": "<optional_existing_id>" },
      "exercise_workout": { "name": "Exercise Workouts", "table_id": "<optional_existing_id>" },
      "monthly_health_calendar": { "name": "Monthly Health Calendar", "table_id": "<optional_existing_id>" },
      "weekly_health_assessment": { "name": "Weekly Health Assessment", "table_id": "<optional_existing_id>" }
    }
  },
  "thresholds": {
    "protein_g": { "low": 60, "adequate": 80 },
    "fiber_g": { "low": 12, "adequate": 20 },
    "sodium_mg": { "caution": 1800, "high": 2500 },
    "calories_kcal": { "low": 1200, "high": 2200 },
    "sleep_score": { "low": 75, "good": 80 }
  },
  "weekly_thresholds": {
    "protein_low_ratio": 90,
    "severe_protein_low_ratio": 75,
    "fiber_low_ratio": 80,
    "sodium_high_ratio": 115,
    "sodium_very_high_ratio": 130,
    "energy_low_ratio": 85,
    "severe_energy_low_ratio": 70,
    "short_sleep_minutes": 420,
    "severe_short_sleep_minutes": 360,
    "low_sleep_score": 75,
    "good_sleep_score": 80,
    "weekly_activity_equiv_target": 150,
    "weekly_activity_equiv_high": 300
  }
}
```

## Optional schema override

If a deployment needs different field labels or additional fields, add:

```json
{
  "schemas": {
    "nutrition_meal": {
      "name": "Nutrition Meals",
      "fields": [
        { "name": "Logged At", "type": "datetime", "style": { "format": "yyyy-MM-dd HH:mm" } },
        { "name": "Food Description", "type": "text" }
      ],
      "views": []
    }
  }
}
```

If `schemas.<table_key>.fields` is present, the bootstrap script uses that override instead of the built-in default schema.

## Rules

- `table_id` may be empty before bootstrap.
- Bootstrap scripts should create missing tables, then print the created IDs so the config can be updated.
- Thresholds are defaults, not medical facts.
- If the user already has a Base, preserve their existing names and IDs.
- Use `node scripts/bootstrap_health_tables.js <config.json> --dry-run` to inspect the planned bootstrap without writing anything.

## Common command examples

```bash
# Bootstrap missing tables and fields
node scripts/bootstrap_health_tables.js <config.json>

# Rebuild a narrow monthly date window
python3 scripts/rebuild_monthly_calendar.py <config.json> \
  --identity user \
  --start-date 2026-04-29 \
  --end-date 2026-04-30 \
  --json

# Rebuild one explicit weekly window ending on Sunday
python3 scripts/rebuild_weekly_assessment.py <config.json> \
  --identity user \
  --week-end 2026-05-03 \
  --json

# Build or refresh the monthly dashboard
node scripts/build_monthly_dashboard.js <config.json> \
  --identity user
```

## Optional field alias override

If a deployment uses different labels from the built-in English defaults, add `field_aliases`:

```json
{
  "field_aliases": {
    "monthly_health_calendar": {
      "date": ["Date", "Stat Date"],
      "overall": ["Overall Health Status", "Overall Status"]
    }
  }
}
```

The rebuild scripts resolve fields by trying these aliases first, then falling back to their built-in English defaults.

## Dashboard naming behavior

`build_monthly_dashboard.js` resolves dashboard labels in this order:

1. CLI `--dashboard-name` (dashboard title only)
2. `config.dashboard.monthly_health_calendar.*` overrides
3. Built-in English defaults

Supported override keys for the monthly dashboard are:
...
- `dashboardName`
- `aboutName`
- `aboutText`
- `recordedDays`
- `nutritionOnTargetDays`
- `avgSleepScore`
- `activeWorkoutDays`
- `overallDistribution`
- `sleepTrend`
- `workoutTrend`
- `nutritionTrend`
- `recoveryDistribution`
- `workoutDistribution`

Example:

```json
{
  "dashboard": {
    "locale_labels": {
      "en": {
        "dashboardName": "Monthly Health Calendar Overview"
      },
      "zh": {
        "dashboardName": "月度健康日历总览"
      }
    },
    "monthly_health_calendar": {
      "dashboardName": "Health Dashboard",
      "aboutName": "About",
      "aboutText": "# Health Dashboard\n- Source: Monthly Health Calendar"
    }
  }
}
```

Use `monthly_health_calendar` when you want one deployment-specific naming scheme regardless of auto-detected locale.

## Output copy overrides

You can also override generated text fragments for monthly / weekly summaries without editing the scripts.

```json
{
  "copy": {
    "monthly_health_calendar": {
      "workout_no_records": "No workouts logged.",
      "overview_nutrition": "Nutrition status: {nutrition_status}",
      "overview_workout": "Training: {workout_summary}"
    },
    "weekly_health_assessment": {
      "brief_title": "Weekly review ({start_day} to {end_day})",
      "brief_overall": "Status: {overall}. {cross_text}",
      "suggestion_activity_gap": "Distribute activity across the week instead of compressing it into one day."
    }
  }
}
```

Current supported keys:

- `copy.monthly_health_calendar`
  - `workout_no_records`
  - `workout_fallback_type`
  - `workout_summary`
  - `overview_nutrition`
  - `overview_sleep`
  - `overview_workout`
  - `overview_nutrition_note`
- `copy.weekly_health_assessment`
  - `no_nutrition_records`
  - `nutrition_headline_stable`
  - `nutrition_headline_unstable`
  - `nutrition_summary`
  - `no_sleep_records`
  - `sleep_quality_solid`
  - `sleep_quality_shaky`
  - `sleep_summary`
  - `no_workout_records`
  - `workout_level_met`
  - `workout_level_below`
  - `workout_fallback_types`
  - `workout_summary`
  - `cross_headline_alert`
  - `cross_headline_attention`
  - `cross_headline_stable`
  - `risk_focus_none`
  - `suggestion_sleep`
  - `suggestion_training_fuel`
  - `suggestion_sodium_fiber`
  - `suggestion_activity_gap`
  - `suggestion_keep_current`
  - `brief_title`
  - `brief_overall`
  - `brief_nutrition`
  - `brief_sleep`
  - `brief_workout`
  - `brief_risk_focus`
  - `brief_next_actions`

Template strings are rendered with Python `str.format(...)`, so placeholder names must match the script variables exactly.

## Production-style config example

Use this pattern when you want one deployment config to control schema matching, dashboard naming, and generated summary wording together.

```json
{
  "feishu": {
    "active_base": {
      "token": "<base_token>"
    },
    "tables": {
      "nutrition_daily_history": { "name": "Nutrition Daily History", "table_id": "<tbl_nutrition_daily_history>" },
      "sleep_recovery": { "name": "Sleep Recovery", "table_id": "<tbl_sleep_recovery>" },
      "exercise_workout": { "name": "Exercise Workouts", "table_id": "<tbl_exercise_workout>" },
      "monthly_health_calendar": { "name": "Monthly Health Calendar", "table_id": "<tbl_monthly_health_calendar>" },
      "weekly_health_assessment": { "name": "Weekly Health Assessment", "table_id": "<tbl_weekly_health_assessment>" }
    }
  },
  "field_aliases": {
    "monthly_health_calendar": {
      "date": ["Date", "Stat Date"],
      "overall": ["Overall Health Status", "Overall Status"]
    },
    "weekly_health_assessment": {
      "brief": ["Chat Brief", "Weekly Brief"]
    }
  },
  "dashboard": {
    "monthly_health_calendar": {
      "dashboardName": "Monthly Health Overview",
      "aboutName": "About This Dashboard",
      "aboutText": "# Monthly Health Overview\n- Source table: Monthly Health Calendar\n- Refresh: rebuild monthly rows before dashboard refresh"
    }
  },
  "copy": {
    "monthly_health_calendar": {
      "overview_nutrition": "Nutrition status: {nutrition_status}",
      "overview_sleep": "Sleep summary: {sleep_summary}",
      "overview_workout": "Workout summary: {workout_summary}"
    },
    "weekly_health_assessment": {
      "brief_title": "Weekly review ({start_day} to {end_day})",
      "brief_overall": "Status: {overall}. {cross_text}",
      "brief_next_actions": "Next actions: {next_actions}",
      "suggestion_keep_current": "Keep the current rhythm and focus on data completeness."
    }
  }
}
```

Recommended use of the three layers:

- `field_aliases`: absorb deployment-specific field naming drift without patching scripts
- `dashboard.monthly_health_calendar`: pin dashboard title and block names for one environment
- `copy.*`: control generated monthly/weekly wording without changing business logic

## Recommended config practice

- Pin `feishu.tables.<table_key>.table_id` after bootstrap in any environment where same-name tables may coexist.
- Keep dashboard/chart field labels aligned with the actual deployed monthly table schema.
- Put deployment-specific naming overrides under `schemas`, not in scripts.
