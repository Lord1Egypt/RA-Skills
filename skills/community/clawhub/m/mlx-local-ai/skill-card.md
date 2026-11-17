## Description:

MLX Local AI installs and manages local Apple Silicon LLM and Chinese embedding services with OpenAI-compatible endpoints and an OpenClaw gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[saybanet](https://clawhub.ai/user/saybanet)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users on macOS Apple Silicon use this skill to set up local chat, embedding, and OpenClaw gateway services for agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may run local background AI services.

Mitigation: Review the service ports, logs, and startup commands before installation, and start services only when local API exposure is intended.

Risk: The skill may modify shell startup configuration.

Mitigation: Inspect any shell profile changes before sourcing them and keep a backup of existing shell configuration.

Risk: The skill may install unpinned dependencies and download model artifacts from a third-party mirror.

Mitigation: Review dependency and model sources, pin versions where possible, and install only from networks and mirrors approved for the deployment environment.

Risk: The skill may execute model-supplied code.

Mitigation: Review the selected model repository and remote-code requirement before startup, and disable remote-code execution when the model stack allows it.

Risk: The OpenClaw configuration may route requests to a remote Baidu provider unless changed.

Mitigation: Inspect the OpenClaw provider configuration before use and remove or replace remote providers when local-only routing is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/saybanet/skills/mlx-local-ai)
- [Publisher profile](https://clawhub.ai/user/saybanet)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup and service-management instructions for local macOS services; no structured post-processing required.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
