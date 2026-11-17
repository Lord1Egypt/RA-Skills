## Description:

Generate interactive chat scripts for NVIDIA NIM models, enabling one-click start, automatic health checks, an OpenAI-compatible API, and local interactive conversation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[romancestarrysky](https://clawhub.ai/user/romancestarrysky)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create scripts for launching, stopping, and chatting with NVIDIA NIM-format model containers through an OpenAI-compatible streaming interface.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated scripts may remove or replace an existing Docker container with the same name.

Mitigation: Review the scripts before execution and back up or rename any existing container that uses the target name.

Risk: The model service may rely on an unpinned or untrusted container image.

Mitigation: Use a pinned, trusted image or digest and confirm the Docker privileges, mounts, ports, and environment variables before running it.

Risk: Chat traffic, API settings, or logs may expose sensitive prompts or credentials.

Mitigation: Avoid entering secrets unless the API path and logging behavior are understood, and stop background services when they are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/romancestarrysky/skills/nim-interactive-chat)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands and generated script guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces start and stop shell scripts plus a Python chat client for a named container and model.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
