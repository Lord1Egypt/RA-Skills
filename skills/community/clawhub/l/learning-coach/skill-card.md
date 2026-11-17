## Description:

Production learning coach for personalized, multi-subject study planning with proactive reminders, curated resources, LLM-generated quizzes, rubric-based grading, and adaptive roadmap updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ravikadam](https://clawhub.ai/user/ravikadam)

### License/Terms of Use:


## Use Case:

Learners and coaching agents use this skill to manage personalized study plans, generate and grade quizzes, track per-subject progress, curate learning resources, and adapt next steps over time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent cron reminders can continue running after setup and may execute recurring coaching or reporting actions.

Mitigation: Review the exact cron entries before applying them, require explicit user approval, and remove or revise jobs when the schedule or scope changes.

Risk: The skill can fetch online resource feeds and process user-provided source inputs.

Mitigation: Use trusted source lists, avoid untrusted subject or source values, and review curated links before relying on them for learning guidance.

Risk: The skill creates and updates local learning records, including per-subject progress, quiz history, and curation files.

Mitigation: Run it in a dedicated workspace or user account and inspect generated records before sharing or reusing them.

Risk: The bootstrap helper can attempt a global npm installation when invoked with install behavior.

Mitigation: Avoid bootstrap install mode unless global package installation is acceptable in the target environment.

## Reference(s):

- [Learning Coach on ClawHub](https://clawhub.ai/ravikadam/skills/learning-coach)
- [Learning Methods](references/learning-methods.md)
- [Scoring Rubric](references/scoring-rubric.md)
- [Source Quality Filter](references/source-quality.md)
- [Source Ingestion](references/source-ingestion.md)
- [Progress Model](references/progress-model.md)
- [Weekly Summary Schema](references/report-schema.md)
- [Per-Subject Cron Templates](references/cron-templates.md)
- [Intervention Policy](references/intervention-policy.md)
- [Quiz JSON Schema Contract](references/quiz-schema.md)
- [Grading JSON Schema Contract](references/grading-schema.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON learning records and shell commands for supporting scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local per-subject learning records, curated-resource files, progress summaries, quiz and grading artifacts, and cron schedules after user approval.]

## Skill Version(s):

0.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
