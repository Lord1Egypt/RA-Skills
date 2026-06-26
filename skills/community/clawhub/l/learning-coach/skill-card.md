## Description: <br>
Production learning coach for personalized, multi-subject study planning with proactive reminders, curated resources, LLM-generated quizzes, rubric-based grading, and adaptive roadmap updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ravikadam](https://clawhub.ai/user/ravikadam) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External learners and developers use this skill to run structured, multi-subject study programs with planning, quizzes, rubric-based feedback, progress tracking, curated resources, and approved reminder automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores local study plans, quiz history, progress metrics, and curated resources. <br>
Mitigation: Keep output paths inside the intended learning-coach data directory and review local files before sharing them. <br>
Risk: The skill can fetch learning-resource feeds from user-provided URLs. <br>
Mitigation: Use trusted feed URLs and review curated links before relying on them for study decisions. <br>
Risk: The skill can add reminder cron jobs after approval. <br>
Mitigation: Review the exact cron schedules and actions before approving or changing any reminders. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ravikadam/learning-coach) <br>
- [Learning Methods](references/learning-methods.md) <br>
- [Scoring Rubric](references/scoring-rubric.md) <br>
- [Source Quality Filter](references/source-quality.md) <br>
- [Source Ingestion](references/source-ingestion.md) <br>
- [Progress Model](references/progress-model.md) <br>
- [Weekly Summary Schema](references/report-schema.md) <br>
- [Per-Subject Cron Templates](references/cron-templates.md) <br>
- [Intervention Policy](references/intervention-policy.md) <br>
- [Quiz JSON Schema Contract](references/quiz-schema.md) <br>
- [Grading JSON Schema Contract](references/grading-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown coaching guidance with JSON artifacts and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores per-subject learning state locally and proposes cron reminder schedules only after explicit user approval.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
