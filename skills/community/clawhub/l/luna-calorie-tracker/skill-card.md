## Description:

Track daily caloric intake by sending food photos. Luna analyzes images using vision AI, estimates calories and macros, and stores everything in memory for daily/weekly summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sidneyschwartz](https://clawhub.ai/user/sidneyschwartz)

### License/Terms of Use:

MIT

## Use Case:

External OpenClaw users use this skill to log meals from food photos, estimate calories and macronutrients, and retrieve daily or weekly nutrition summaries from memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Food-photo-derived nutrition history and calorie goals are stored in OpenClaw memory files and may reveal sensitive personal habits.

Mitigation: Treat the memory files as sensitive personal data and delete them manually when the user no longer wants the history retained.

Risk: Image-based calorie and macronutrient estimates can be inaccurate, especially when portions or ingredients are unclear.

Mitigation: Ask for clarifying portion details when needed, present estimates with confidence, and treat outputs as approximate nutrition tracking rather than authoritative dietary advice.

## Reference(s):

- [Luna Calorie Tracker on ClawHub](https://clawhub.ai/sidneyschwartz/skills/luna-calorie-tracker)
- [OpenClaw](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Markdown summaries and memory-file updates with structured calorie and macronutrient estimates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a vision-capable model provider and OPENAI_API_KEY or equivalent provider credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
