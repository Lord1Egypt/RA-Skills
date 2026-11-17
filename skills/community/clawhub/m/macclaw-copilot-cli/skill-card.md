## Description:

Helps developers use GitHub Copilot CLI for AI-assisted code analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[biuyx](https://clawhub.ai/user/biuyx)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to install and run GitHub Copilot CLI prompts for command-line code analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The usage example reads a local GitHub Copilot token into an environment variable, which can expose credentials through shell history, logs, or overly broad file permissions.

Mitigation: Use the skill only when the token file has restrictive permissions, avoid logging command output or environment variables, and prefer the official CLI authentication flow when available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/biuyx/skills/macclaw-copilot-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
