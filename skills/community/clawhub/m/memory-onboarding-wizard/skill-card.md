## Description:

Bootstraps an OpenClaw agent memory system by creating starter memory, daily note, heartbeat, and user profile files through an interactive or non-interactive setup command.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stevojarvisai-star](https://clawhub.ai/user/stevojarvisai-star)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to initialize persistent agent memory files when setting up a new workspace or repairing a missing memory system.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated HEARTBEAT.md can persistently prompt an agent to check email and calendar without a clear opt-in.

Mitigation: Review the generated HEARTBEAT.md before enabling the skill with email or calendar tools, and remove or explicitly approve recurring checks.

Risk: The wizard writes persistent memory files that future agent sessions may read.

Mitigation: Run the wizard only in a workspace you control and review generated memory files before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stevojarvisai-star/skills/memory-onboarding-wizard)
- [GetAgentIQ](https://getagentiq.ai)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown files and terminal text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes MEMORY.md, memory/YYYY-MM-DD.md, HEARTBEAT.md, and USER.md in the selected workspace.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
