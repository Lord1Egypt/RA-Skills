## Description:

Generates structured behavior plans for OpenClaw agents based on user requirements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[umfl](https://clawhub.ai/user/umfl)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to turn a user goal into a structured OpenClaw behavior plan with goals, prerequisites, executable steps, fallback handling, and completion criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated plans can include shell commands, file writes, or external service actions.

Mitigation: Review each generated plan before execution and require user confirmation for sensitive operations.

Risk: The skill may over-trigger or produce Chinese-language plans when that is not desired.

Mitigation: Install it only for OpenClaw planning workflows where Chinese-language output is acceptable, and adjust or reject generated plans that do not match the task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/umfl/skills/openclaw-behavior-plan)
- [examples.md](artifact/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown behavior plan]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask 1-2 clarification questions when the request is ambiguous; marks sensitive operations as requiring user confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
