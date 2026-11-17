## Description:

Interactive hiring wizard to set up a new AI team member. Guides the user through role design via conversation, generates agent identity files, and optionally sets up performance reviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[larsderidder](https://clawhub.ai/user/larsderidder)

### License/Terms of Use:


## Use Case:

Developers and agent workspace users use this skill to define and create a new AI team member through a short interview, including role boundaries, personality, model selection, identity files, shared context links, and optional review scheduling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create persistent agent files and link shared user and memory context into the new agent.

Mitigation: Require explicit confirmation before creating shared context links, and confirm whether the new agent should receive shared USER.md and MEMORY.md access.

Risk: The skill can modify OpenClaw gateway configuration and grant the new agent access from the main agent.

Mitigation: Validate the agent name, preview the config.patch changes before applying them, and document how to undo the configuration change.

Risk: The skill may create a scheduled review task.

Mitigation: Confirm the review cadence before creating a schedule and document how to disable or remove the scheduled task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/larsderidder/skills/hire)
- [Publisher profile](https://clawhub.ai/user/larsderidder)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, generated agent files, and configuration patch guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create persistent agent files, shared context links, gateway configuration changes, and optional scheduled review tasks.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
