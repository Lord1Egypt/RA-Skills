## Description:

Automates project inspection and iteration by analyzing projects from user, product, project, and technical perspectives to improve code quality and delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[relunctance](https://clawhub.ai/user/relunctance)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to inspect repositories, prioritize improvements, and manage iterative project changes with review, scheduling, rollback, and learning-history workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated repository changes can modify files and create commits or pushes without sufficient review.

Mitigation: Use dry-run or semi-auto mode by default, keep full-auto execution disabled until repositories and rollback procedures are reviewed, and require human approval for medium- and high-risk changes.

Risk: Project code, context, or agent memory may be sent to configurable LLM endpoints.

Mitigation: Review the configured LLM endpoint and credentials before use, redact private or sensitive code, and define an explicit external-data policy.

Risk: Scheduling, GitHub posting, cross-persona recall, and host test execution expand the operational impact of the skill.

Mitigation: Enable these features only in constrained, trusted environments after validating repository scope, credentials, permissions, and test commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/relunctance/skills/hawk-bridge-v2)
- [Quality Gates](references/QUALITY-GATES.md)
- [Risk Classification](references/RISK-CLASSIFICATION.md)
- [Notification Template](references/NOTIFICATION-TEMPLATE.md)
- [project-standard](https://github.com/relunctance/project-standard)
- [SoulForce](https://github.com/relunctance/soul-force)
- [hawk-bridge](https://github.com/relunctance/hawk-bridge)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce repository inspection reports, pending-review items, suggested code changes, commit or rollback commands, and configuration guidance.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
