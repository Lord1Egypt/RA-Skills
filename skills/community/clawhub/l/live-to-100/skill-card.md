## Description: <br>
Generates lifestyle-oriented longevity plans with risk scoring, staged check-ins, supplement safety checks, reminder schedules, and daily nutrition and calorie-deficit analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rq-wu](https://clawhub.ai/user/rq-wu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to collect baseline wellness information and produce concrete longevity routines, reminders, progress reports, supplement checks, and nutrition adjustments. It is intended for lifestyle coaching support, not diagnosis, emergency care, or a substitute for clinical judgment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can handle sensitive health, medication, and lifestyle details. <br>
Mitigation: Provide only the minimum information needed, omit fields the user does not want handled, and keep generated artifacts in appropriate privacy controls. <br>
Risk: Reminder schedules may be copied into platform automation. <br>
Mitigation: Review all reminder text, timing, quiet hours, and recurrence rules before enabling automation. <br>
Risk: Risk scores and supplement advice could be mistaken for medical care. <br>
Mitigation: Treat scores and supplement checks as coaching prompts, and route urgent symptoms, medication conflicts, or high-risk findings to qualified medical care. <br>


## Reference(s): <br>
- [Longevity Intake Template](references/intake-template.md) <br>
- [Daily Nutrition Log](references/daily-nutrition-log.md) <br>
- [Reminder Presets](references/reminder-presets.md) <br>
- [Complex Reminder Timetable](references/reminder-timetable.md) <br>
- [Longevity Risk Scoring](references/risk-scoring.md) <br>
- [Supplement Safety](references/supplement-safety.md) <br>
- [Auto Report Templates](references/report-templates.md) <br>
- [Health Report Sample](references/health-report-sample.json) <br>
- [Nutrition Day Sample](references/nutrition-day-sample.json) <br>
- [Reminder Schedule Sample](references/reminder-schedule-sample.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional JSON-backed schedules, reports, and nutrition analyses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include risk scores, reminder tables, supplement safety statuses, weekly or monthly reports, and daily nutrition balance summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
