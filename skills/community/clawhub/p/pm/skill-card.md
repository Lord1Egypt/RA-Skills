## Description:

PM provides a Chinese-language project management workflow for requirements decomposition, API contract design, task planning, iterative development, test verification, and status updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zengn1](https://clawhub.ai/user/zengn1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to manage software projects through documented architecture, API contracts, small task increments, terminal-based verification, and status tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can create or update planning documents, code, and tests in the repository root.

Mitigation: Review generated plans and repository changes before approving implementation.

Risk: The workflow can run local verification commands while implementing tasks.

Mitigation: Run commands in an appropriate local workspace and inspect command intent before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zengn1/skills/pm)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown guidance with project documents, implementation steps, test commands, and status updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or update repository documents such as ARCHITECTURE.md, TASK_TRACKER.md, and ERROR_LOG.md as part of the workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
