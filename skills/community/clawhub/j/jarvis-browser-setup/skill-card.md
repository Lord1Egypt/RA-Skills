## Description:

Sets up Jarvis Browser Control for new users by generating a WebSocket authentication token, writing configuration, and preparing server and browser-extension files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evernation](https://clawhub.ai/user/evernation)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to create a new Jarvis Browser Control setup package for configuring or sharing browser control. The skill is intended for setup flows that need a unique token, local server configuration, extension files, and user-facing setup instructions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated setup folder contains an authentication token, and sharing it as-is can expose browser-control access.

Mitigation: Treat generated packages as sensitive, rotate or regenerate tokens when sharing is unintended, and distribute only after confirming the token is required for the recipient.

Risk: The release evidence says the setup relies on unreviewed local server and extension templates.

Mitigation: Use only bundled or integrity-checked templates before installation or execution, and review copied server and extension files before enabling browser control.

Risk: Authentication claims may be misleading if the generated token is not applied consistently to both the server and extension.

Mitigation: Confirm the generated token is configured on both sides before use and limit service exposure to the intended network and user.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/evernation/skills/jarvis-browser-setup)

## Skill Output:

**Output Type(s):** [Files, Configuration, Markdown, Shell commands, Guidance]

**Output Format:** [Generated setup directory with JSON configuration, server and extension files, a Markdown README, and console setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a generated authentication token and local network endpoint; generated packages should be reviewed before sharing.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
