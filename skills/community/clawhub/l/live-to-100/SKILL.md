---
name: live-to-100
description: 收集用户身体指标、生活习惯、既往病史和目标，生成可执行的长寿行动计划与分阶段复盘机制，并提供风险评分、自动周报/月报、保健品安全检查和每日饮食营养均衡分析（含热量缺口）。Use when users ask for longevity plans, healthy routine optimization, behavior-change schedules, supplement safety review, daily meal/nutrition analysis, calorie deficit tracking, or recurring reminders for hydration, standing breaks, sleep, and exercise.
---

# Live To 100

## Core Rule

Position the output as lifestyle guidance, not diagnosis or emergency care.
If the user reports urgent danger signs (e.g., severe chest pain, fainting, stroke-like symptoms, self-harm intent), stop planning and advise immediate emergency care.

## Workflow

### 1) Collect baseline data

Use `references/intake-template.md` as the intake form.
Ask only for missing high-impact fields first:
- Age, biological sex, height, weight, waist
- Blood pressure (if known), resting heart rate, sleep duration
- Activity level (steps, exercise days/week, sedentary hours)
- Smoking, alcohol, caffeine timing
- Current diseases, medications, supplement list
- Main goal and constraints (time, budget, injuries, shift work)

If data is partial, continue with assumptions and clearly label assumptions.

### 2) Build longevity profile

Produce a concise risk-and-opportunity snapshot:
- `Green`: already solid habits to maintain
- `Yellow`: moderate gaps to improve in 4-12 weeks
- `Red`: possible high-risk items that need clinician follow-up

Prioritize behavior changes by expected impact and feasibility.
Do not overload the plan with more than 3 major behavior goals at once.

Then calculate a `Longevity Risk Score (0-100)` using `references/risk-scoring.md`:
- Show total score and sub-scores (body composition, cardiometabolic, sleep/recovery, activity/sedentary, habits, medical context).
- Explain top 3 contributors and which 2-3 changes can move the score most in 4 weeks.
- If critical data is missing, output a provisional score and list missing fields.

### 3) Generate actionable plan

Return a 12-week plan in 3 phases:
- `Phase 1 (Week 1-2)`: minimum viable routine and reminders
- `Phase 2 (Week 3-6)`: progressive overload and consistency targets
- `Phase 3 (Week 7-12)`: stabilization and relapse prevention

Include these dimensions:
- Hydration
- Standing/mobility breaks
- Sleep timing and wind-down
- Exercise (aerobic + strength + daily movement)
- Nutrition guardrails
- Supplements (after safety screening only)

For each action, specify:
- Trigger (`when`)
- Action (`what`)
- Minimum bar (`minimum version`)
- Upgrade path (`next level`)

### 4) Configure reminders

Use `references/reminder-presets.md` and adapt to user wake/sleep schedule.
For complex timetables (multiple windows, weekday/weekend differences, interval reminders, quiet hours), use `references/reminder-timetable.md`.
Always output a reminder table with:
- Reminder type
- Time or interval
- Message
- Duration
- Completion rule

Support at least these reminders:
- Drink water
- Stand up / move
- Sleep routine
- Workout
- Supplements

If the platform supports recurring automations, generate platform-ready schedules.
If not, output copy-paste reminder text for phone calendar or todo apps.

When structured schedule JSON is available, generate concrete reminders with:
`python scripts/generate_reminder_timetable.py --input schedule.json --output reminders.md`

### 5) Apply supplement safety gate

Use `references/supplement-safety.md` before confirming any supplement advice:
- Check contraindications against existing diseases, meds, allergies, pregnancy/breastfeeding status, kidney/liver flags.
- Check dosage and timing boundaries; avoid adding stacked supplements with overlapping risks.
- Output status per supplement: `Safe to continue`, `Needs clinician review`, or `Avoid for now`.
- If conflict exists, prioritize food-first alternatives and medical follow-up over additional supplements.

### 6) Close the loop with auto reports

Add a lightweight check-in protocol:
- Daily: adherence score (0-100) + 1 blocker
- Weekly: trend on sleep, movement, training sessions, waist/weight
- Every 4 weeks: adjust targets based on adherence and recovery

When adherence is low, reduce plan complexity before increasing intensity.

Generate reports using `references/report-templates.md`:
- Weekly report: adherence, metric deltas, blockers, and next-week focus.
- Monthly report: score trend, behavior consistency, supplement safety events, and plan adjustments.
- Keep each report short and action-oriented.

### 7) Analyze daily meals and calorie deficit

Use `references/daily-nutrition-log.md` for daily food logging input.
Evaluate these outputs every day:
- Total calories and estimated calorie deficit/surplus vs target
- Macro totals (protein/carbs/fat) and ratio balance
- Fiber and hydration adequacy
- Food diversity and ultra-processed food proportion (if available)

Return:
- `Nutrition Balance Score (0-100)`
- `Calorie Deficit Status` (on target / too aggressive / insufficient)
- 2-3 concrete meal adjustments for next day

When structured daily log JSON is available, generate analysis with:
`python scripts/analyze_daily_nutrition.py --input nutrition_day.json --output nutrition_report.md`

## Output Format

Use this order:
1. `Health Snapshot` (Green/Yellow/Red)
2. `Longevity Risk Score` (total + sub-scores + key drivers)
3. `12-Week Longevity Plan`
4. `Reminder Schedule`
5. `Supplement Safety Check`
6. `Daily Nutrition Balance and Calorie Deficit`
7. `Check-in and Auto Report Rules`
8. `Medical Follow-up Flags` (if applicable)

Keep recommendations specific, measurable, and time-bound.
Avoid abstract advice without concrete behaviors.

## Resources

- Intake template: `references/intake-template.md`
- Daily nutrition intake template: `references/daily-nutrition-log.md`
- Reminder defaults: `references/reminder-presets.md`
- Complex timetable schema: `references/reminder-timetable.md`
- Risk model: `references/risk-scoring.md`
- Supplement safety: `references/supplement-safety.md`
- Weekly/monthly report templates: `references/report-templates.md`
- Report generator script: `scripts/generate_health_reports.py`
- Reminder timetable generator script: `scripts/generate_reminder_timetable.py`
- Daily nutrition analyzer script: `scripts/analyze_daily_nutrition.py`

Use the script when structured JSON data is available:
`python scripts/generate_health_reports.py --input user_data.json --output report.md`
