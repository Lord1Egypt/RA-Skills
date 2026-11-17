## Description:

Triage Issues helps an agent batch-process Gitee repository issues by classifying priority and type, identifying duplicates, producing a triage report, and optionally updating issue metadata or comments after user confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oschina](https://clawhub.ai/user/oschina)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill to organize open issues in a Gitee repository, identify urgent work, spot duplicates, and prepare label, priority, assignment, or comment updates for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confirmed batch updates may change project-visible issue labels, priorities, assignments, or comments in a Gitee repository.

Mitigation: Review the target repository, selected issue batch, proposed labels, priorities, assignments, and comments before approving updates.

Risk: Triage recommendations may misclassify issue type, priority, duplicate status, or missing information.

Mitigation: Review the generated triage report before applying recommendations or approving repository changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oschina/skills/gitee-triage-issues)

## Skill Output:

**Output Type(s):** [markdown, guidance, text]

**Output Format:** [Markdown triage report with issue tables, issue lists, and recommended updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include proposed label, priority, assignment, or comment changes that require user confirmation before project-visible updates.]

## Skill Version(s):

1.0.0 (source: artifact frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
