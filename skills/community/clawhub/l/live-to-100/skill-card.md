## Description:

活百岁 collects health metrics, lifestyle habits, medical context, and goals to produce longevity lifestyle plans, risk scoring, supplement safety checks, reminders, reports, and daily nutrition analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rq-wu](https://clawhub.ai/user/rq-wu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and health coaches can use this skill to collect baseline lifestyle data and turn it into a 12-week longevity plan with reminders, reports, supplement safety checks, and daily nutrition feedback. It is intended for lifestyle coaching rather than diagnosis or emergency care.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process sensitive health information such as conditions, medications, supplements, labs, body metrics, and routines.

Mitigation: Share only necessary fields, keep generated reports and reminders in trusted locations, and avoid storing or forwarding sensitive details beyond the intended workflow.

Risk: Lifestyle plans, risk scores, nutrition feedback, or supplement guidance could be mistaken for medical diagnosis or treatment.

Mitigation: Label outputs as lifestyle guidance, escalate urgent danger signs to emergency care, and recommend clinician review for medical decisions, medication interactions, supplement concerns, or high-risk symptoms.

Risk: Incomplete baseline data can make scores and plans provisional.

Mitigation: State assumptions, list missing high-impact fields, and update plans and scores when vitals, labs, medications, or adherence data become available.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rq-wu/skills/live-to-100)
- [Longevity Intake Template](artifact/references/intake-template.md)
- [Daily Nutrition Log](artifact/references/daily-nutrition-log.md)
- [Longevity Risk Scoring](artifact/references/risk-scoring.md)
- [Supplement Safety Gate](artifact/references/supplement-safety.md)
- [Reminder Presets](artifact/references/reminder-presets.md)
- [Complex Reminder Timetable](artifact/references/reminder-timetable.md)
- [Auto Report Templates](artifact/references/report-templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown plans, tables, reminder schedules, JSON-backed report outputs, and optional shell commands for bundled scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are lifestyle guidance, not medical diagnosis; structured JSON inputs can be used for nutrition reports, reminder timetables, and weekly or monthly health reports.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
