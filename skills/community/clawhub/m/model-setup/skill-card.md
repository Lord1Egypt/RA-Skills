## Description:

Model Setup helps manage OpenClaw model configuration by adding, testing, and assigning model entries with validation and backups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ykaixu](https://clawhub.ai/user/ykaixu)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to configure model providers, test model access, optionally validate tool calling and streaming, set defaults, and attach models to specific agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be exposed through shell command arguments, local configuration files, or backup files.

Mitigation: Use only keys approved for local storage, restrict file permissions, avoid sharing shell history or backups, and rotate keys that were previously passed through command examples.

Risk: Testing against untrusted or plaintext Base URLs can disclose credentials to endpoints the user does not control.

Mitigation: Use trusted HTTPS provider endpoints and review Base URLs before running model accessibility, tool-calling, or streaming tests.

Risk: The server security verdict is suspicious due to risky credential handling.

Mitigation: Review the skill and generated configuration changes before installation or use, especially in shared or production OpenClaw environments.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration snippets and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local OpenClaw configuration files and backups.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
