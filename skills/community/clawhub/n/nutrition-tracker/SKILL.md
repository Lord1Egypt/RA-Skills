---
name: nutrition-tracker
description: Track daily calories and macros in Obsidian, with profile initialization (sex/height/weight/goal) and goal-based target checks. Includes i18n (zh-CN/en-US). Use when user logs meals, asks if targets are met, or wants to set/remember nutrition profile.
---

# Nutrition Tracker (Obsidian)

This skill logs meals (kcal + P/C/F) into an Obsidian vault and maintains daily totals. It also stores a lightweight nutrition profile (sex/height/weight/activity/goal) and can evaluate whether today's intake meets targets.

> i18n: scripts support `--lang zh-CN|en-US` (default: `zh-CN`).

## Storage

- Vault (default): `~/Documents/obsidian/yzhai-daily`
- Profile: `health/eat/profile.json`
- Monthly log: `health/eat/YYYY-MM/YYYYMM_calories_macros.md`

## Quick start

### 1) Initialize / update profile

```bash
bash ~/.openclaw/workspace/skills-public/nutrition-tracker/scripts/nutrition_init.sh \
  --sex male \
  --height 175 \
  --weight 75 \
  --activity office \
  --goal cut \
  --kcal 2200 \
  --lang zh-CN
```

### 2) Log a meal

```bash
bash ~/.openclaw/workspace/skills-public/nutrition-tracker/scripts/nutrition_log.sh \
  --date "2026-03-04" --time "19:54" --meal dinner \
  --desc "rice 150g; potato 120g; meat+egg 200g; soup 200g" \
  --kcal 830 --p 45 --c 69 --f 40 \
  --lang zh-CN
```

### 3) Check whether today's targets are met

```bash
bash ~/.openclaw/workspace/skills-public/nutrition-tracker/scripts/nutrition_check_today.sh \
  --date "2026-03-04" \
  --lang zh-CN
```

## Target logic (defaults)

If profile has no explicit macro targets, defaults are computed by goal:

- **cut** (fat loss):
  - Protein: `2.0 g/kg`
  - Fat: `0.8 g/kg`
  - Carbs: remaining calories (based on kcal target)

You can override targets explicitly in profile (see `nutrition_init.sh --pTarget/--cTarget/--fTarget`).

## Notes

- Keep meal macros as estimates; refine later by updating entries.
- This skill is designed to be deterministic via scripts, not free-form editing.
