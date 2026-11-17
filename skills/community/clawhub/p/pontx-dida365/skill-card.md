## Description:

Integrate Dida365 safely through Pontx. Use for credential setup, task or project reads and writes, scheduling, recurrence, completion, moves, or any Dida365 Open API workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pontjs](https://clawhub.ai/user/pontjs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation teams use this skill to integrate Dida365 task and project workflows through Pontx while handling credentials, scheduling, previews, mutations, and returned personal data carefully.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Write, move, completion, recurrence, and deletion actions can affect real Dida365 task data.

Mitigation: Review the exact preview and require explicit approval before executing any non-read action.

Risk: Credentials and returned task content may expose personal or account data.

Mitigation: Keep secrets in environment variables or a secret manager, redact sensitive values, and return only the task data needed for the user request.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pontjs/skills/pontx-dida365)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with inline bash commands and implementation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include request previews, redacted credential handling guidance, and generated integration code.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
