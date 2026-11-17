## Description:

Set up Myway, a self-hosted personal AI home screen, using OpenClaw as the AI backend.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uchibeke](https://clawhub.ai/user/uchibeke)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and self-hosting users use this skill to install, configure, and troubleshoot a local Myway dashboard connected to an existing OpenClaw gateway.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup uses unpinned npx commands, so the executed package code may change between runs.

Mitigation: Review @uchibeke/myway before use, prefer a pinned reviewed version, and run the install from a low-privilege or sandboxed account when possible.

Risk: The setup can create files, configure a file-browser root, write local environment settings, and start a service.

Mitigation: Confirm the install directory, file-browser root, OpenClaw gateway URL, port, and gateway token before running the command.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/uchibeke/skills/myway-personal-os)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and environment configuration code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.2.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
