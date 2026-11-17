## Description:

构建领域业务标签体系，按业务阶段与场景对拆分知识问答进行分类、打标，并指出知识拆分问题。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dluolan](https://clawhub.ai/user/dluolan)

### License/Terms of Use:

MIT-0

## Use Case:

Knowledge operations teams and developers use this skill to build a domain business label taxonomy, label split question-answer knowledge in Excel files, and identify knowledge splits that need correction before retrieval use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided spreadsheets may contain sensitive or regulated source knowledge.

Mitigation: Review and redact source files before sharing them with an agent or before publishing generated labeled outputs.

Risk: Incorrect labels or split-quality judgments could reduce retrieval precision or place knowledge in the wrong business category.

Mitigation: Have a domain reviewer validate the proposed taxonomy, sample labels, and split-correction notes before using them in production retrieval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dluolan/skills/label-system)

## Skill Output:

**Output Type(s):** [text, markdown, spreadsheet, guidance]

**Output Format:** [Markdown guidance and labeled spreadsheet output when spreadsheet tooling is available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May add a business label column to user-provided Excel knowledge exports and provide split-quality review notes.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
