## Description:

健康饮食提醒 helps agents provide Chinese-language meal, hydration, exercise, and weekly check-in reminders based on the Chinese Dietary Guidelines (2022), with seasonal meal options, calorie estimates, and follow-up logging prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[azerwang](https://clawhub.ai/user/azerwang)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to configure a Chinese-language wellness assistant that recommends meals, prompts hydration and exercise, follows up after meals, and summarizes weekly diet progress. It is intended for general wellness reminders, not medical or individualized nutrition advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recurring reminders may be installed with schedules, categories, or timezone settings the user did not intend.

Mitigation: Before installation, confirm the desired meal, hydration, exercise, follow-up, and weekly report reminders, and adjust the Asia/Shanghai timezone when needed.

Risk: General diet and calorie guidance may be mistaken for medical or individualized nutrition advice.

Mitigation: Treat the skill as general wellness support only; users with pregnancy, breastfeeding, diabetes, eating-disorder risk, or other medical needs should consult a clinician.

Risk: Preset calorie, hydration, and activity targets may not fit every user.

Mitigation: Review targets before use and adapt them to the user's context; do not use the skill to override clinical guidance.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/azerwang/skills/healthy-meal-reminder)
- [ClawHub publisher profile](https://clawhub.ai/user/azerwang)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with OpenClaw cron command examples and Chinese-language reminder prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Asia/Shanghai in the bundled reminder schedules; no credential requirements were detected.]

## Skill Version(s):

2.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
