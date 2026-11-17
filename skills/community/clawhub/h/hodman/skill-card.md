## Description:

Use Hodman to turn useful personal AI work into controlled, auditable company projects: create or select applications and agents, delegate work, publish them, and operate them through the user-authorized CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hodman-ai](https://clawhub.ai/user/hodman-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and developers use this skill to manage authorized Hodman projects, delegate work to project agents, and inspect or operate project applications through the CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project writes, publishing, shell execution, or mutable SQL could change shared applications or data.

Mitigation: Review the exact target and command, obtain explicit approval, and scope writes or mutable queries before execution.

Risk: Revealed credentials or connector grants could expose sensitive project capabilities.

Mitigation: Keep real tokens in the protected UI or a trusted human terminal; review connector grants and never reveal credentials in agent-visible output.

Risk: A different Hodman binary on PATH could receive unintended commands.

Mitigation: Verify the public CLI identity using version and help before authentication or project operations.

## Reference(s):

- [Hodman skill on ClawHub](https://clawhub.ai/hodman-ai/skills/hodman)
- [Hodman Toolkit CLI](https://github.com/hodman-ai/hodman-toolkit)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with CLI examples and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Project actions require an authorized account and appropriate human approval.]

## Skill Version(s):

1.2.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
