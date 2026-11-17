## Description:

Use this skill when Codex needs gstack-style CEO/product, engineering, design, QA, release, or portfolio-shelf-space review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product owners, designers, QA reviewers, and release reviewers use this skill to apply gstack-style review discipline to Codex and ClawHub decisions. It supports product and portfolio triage, engineering risk review, UI/UX critique, QA gates, and ship/no-ship recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can influence review outcomes and ship/no-ship recommendations, which could lead to publish, unpublish, delete, submit, or similar actions if treated as automatic approval.

Mitigation: Review recommendations before execution and require explicit user approval before any publishing, unpublishing, deletion, submission, or other irreversible action.

Risk: When upstream behavior matters, the skill may read a local gstack clone or inspect the public gstack repository.

Mitigation: Load only task-relevant upstream files, cite the source used, and avoid copying large upstream sections into outputs.

## Reference(s):

- [Design Review](references/design-review.md)
- [Review Rubric](references/review-rubric.md)
- [Ship And QA Gate](references/ship-and-qa.md)
- [Upstream](references/upstream.md)
- [Upstream gstack project](https://github.com/garrytan/gstack)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with structured review sections, recommendations, and occasional inline shell commands or code references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include green/yellow/red classifications, 0-10 design scores, QA evidence, blocker lists, rollback notes, and ship/no-ship recommendations.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
