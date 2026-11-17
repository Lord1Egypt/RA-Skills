## Description:

Visual AI workflow builder - ComfyUI meets n8n for LLM agents, RAG pipelines, and multimodal data flows. Local-first, open source (AGPL-3.0).

This skill is ready for commercial/non-commercial use.

## Publisher:

[georgi](https://clawhub.ai/user/georgi)

### License/Terms of Use:

AGPL-3.0

## Use Case:

Developers and engineers use this skill to install and operate NodeTool for local AI workflow building, workflow execution, package generation, deployment management, model cache administration, chat, and server workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation guidance encourages direct execution of mutable remote scripts and unattended install modes.

Mitigation: Review installer contents before execution, prefer a pinned release or downloaded script with verified checksum or signature, and use unattended modes only in isolated least-privilege environments.

Risk: Command examples include auth token parameters that could be exposed through shell history, logs, or process inspection.

Mitigation: Use environment-specific secret handling and avoid pasting real authentication tokens directly into commands that may be logged.

## Reference(s):

- [NodeTool homepage](https://nodetool.ai)
- [Linux/macOS install script](https://raw.githubusercontent.com/nodetool-ai/nodetool/refs/heads/main/install.sh)
- [Windows install script](https://raw.githubusercontent.com/nodetool-ai/nodetool/refs/heads/main/install.ps1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell, PowerShell, JSON, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance includes CLI command patterns for workflow execution, package creation, deployment, model management, chat, server, proxy, and environment setup tasks.]

## Skill Version(s):

0.6.3 (source: ClawHub release evidence; package.json lists 0.6.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
