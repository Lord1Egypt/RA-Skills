## Description:

Breaks clear requirements into ordered implementation tasks and structured planning outputs for development workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, project managers, and automation users can use this skill to turn specifications or clear requirements into ordered implementation tasks and structured workflow plans. It is not suited for work that requires independent creative judgment without human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad local read and command execution capability while its scope is unclear.

Mitigation: Install only in restricted workspaces, avoid secrets and production systems, and grant read or command execution access only when required for the intended task.

Risk: Task plans or automation guidance could be incomplete, incorrect, or unsuitable for critical decisions.

Mitigation: Review generated plans and commands before use, especially for cross-team coordination, production changes, or long-running operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/planning-and-task-breakdown)
- [Skill homepage](https://skillhub.cn)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown or JSON structured task breakdowns, with command suggestions when relevant]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use local read and command execution tools when the host agent grants them.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
