## Description:

Free basic version that extracts actionable tasks from meeting minutes. Reserves premium upgrade hooks for deeper action decomposition and project tracker export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wingogx](https://clawhub.ai/user/wingogx)

### License/Terms of Use:


## Use Case:

External users and teams use this skill to turn meeting notes into a short task list with assignee and due-date hints, while preserving reserved upgrade hooks for deeper task decomposition and tracker export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task output includes a premium-upgrade payment link that can contain the provided user_id.

Mitigation: Review SkillPay payment URL environment configuration before use, especially in shared deployments.

## Reference(s):

- [SkillPay API Contract](references/skillpay-api-contract.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration]

**Output Format:** [JSON from a Python command-line script, with task fields and premium-upgrade metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Free tier returns up to 5 extracted tasks with assignee, due-date, and priority fields.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
