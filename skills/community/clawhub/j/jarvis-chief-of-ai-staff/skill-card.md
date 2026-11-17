## Description:

Deploy Jarvis, your Chief of AI Staff, on OpenClaw, optimized for Dell Pro Max GB10 (NVIDIA DGX Spark) edge devices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gignaati](https://clawhub.ai/user/gignaati)

### License/Terms of Use:

MIT

## Use Case:

Founders, executives, operators, and engineering teams use this skill to deploy a local-first OpenClaw executive agent for operations support, research, project coordination, and system monitoring on GB10-class Linux hardware.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs persistent agent instructions that are hardcoded to serve the publisher's company and principal.

Mitigation: Review and edit the persona templates before installation so they name the intended organization, principal, priorities, and confidentiality boundaries.

Risk: Security claims may overstate what the hardening script changes for network, credentials, and local configuration.

Mitigation: Inspect the shell scripts before execution and treat security-harden.sh as an audit and checklist rather than a complete hardening control.

Risk: Setup examples can encourage unpinned Docker, model, or skill dependencies on a sensitive local machine.

Mitigation: Pin container images, model versions, and installed skills before running the deployment in a production or sensitive environment.

Risk: Credential handling examples can lead users to place API keys in shell startup files.

Mitigation: Use a dedicated secret manager or restricted environment file instead of storing API keys in ~/.bashrc.

Risk: The deployment writes persona and memory files into the OpenClaw workspace.

Mitigation: Back up the workspace before installation and review generated or copied memory files before enabling always-on or heartbeat behavior.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gignaati/skills/jarvis-chief-of-ai-staff)
- [Publisher Profile](https://clawhub.ai/user/gignaati)
- [Gignaati](https://gignaati.com)
- [NVIDIA DGX Spark OpenClaw Playbook](https://build.nvidia.com/spark/openclaw)
- [OpenClaw Documentation](https://docs.openclaw.ai)
- [OpenClaw Gateway Security](https://docs.openclaw.ai/gateway/security)
- [Qwen3.5 and OpenClaw on GB10 Guide](https://github.com/ZengboJamesWang/Qwen3.5-35B-A3B-openclaw-dgx-spark)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash, JSON, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local workspace files and setup instructions for an OpenClaw agent persona.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
