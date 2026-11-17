## Description:

Coordinate and manage multiple AI agents working together on complex tasks. Provides orchestration, communication patterns, and workflow management for multi-agent systems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhuyu28](https://clawhub.ai/user/zhuyu28)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to decompose complex work, delegate subtasks across specialized agents, coordinate communication patterns, and track multi-agent workflow progress.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Coordination tasks and results may be saved locally when the helper script is used.

Mitigation: Avoid placing secrets, credentials, private prompts, or confidential plans in task descriptions or results unless the session file location and cleanup are controlled.

## Reference(s):

- [Multi-Agent Coordination Patterns](references/coordination_patterns.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown guidance with optional shell commands and JSON session data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local coordination session JSON when the helper script is used.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
