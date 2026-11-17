## Description:

Creates and quizzes spaced-repetition learning cards in Feishu/Lark Bitable, tracks learning progress, and schedules reviews using an 85% accuracy rule.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guoqunabc](https://clawhub.ai/user/guoqunabc)

### License/Terms of Use:

MIT-0

## Use Case:

External learners and agents use this skill to create flashcards from books, courses, or knowledge bases, then run interactive review sessions that update progress in Feishu/Lark Bitable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bitable read/write authorization can update learning-card records and may affect unrelated data if used against the wrong table or app.

Mitigation: Use a dedicated learning-card Bitable table or app and grant only the Bitable access needed for that workspace.

Risk: The workflow updates quiz progress after each answer, so incorrect card selection or scoring can change review schedules.

Mitigation: Review the selected table and scoring before study sessions, and keep recoverable backups or versioned exports for important card sets.

## Reference(s):

- [System Design](references/system-design.md)
- [OpenClaw Feishu setup docs](https://docs.openclaw.ai/channels/feishu)
- [The Eighty Five Percent Rule for optimal learning](https://doi.org/10.1038/s41467-019-12552-4)
- [Feishu Bitable API documentation](https://open.feishu.cn/document/server-docs/docs/bitable-v1)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Configuration, Guidance]

**Output Format:** [Markdown conversation output with Feishu/Lark Bitable record reads and updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Feishu/Lark Bitable access through the OpenClaw Feishu plugin and user OAuth authorization.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
