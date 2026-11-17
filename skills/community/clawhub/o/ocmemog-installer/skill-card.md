## Description:

Install and configure ocmemog, the OpenClaw durable memory plugin and sidecar.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simbimbo](https://clawhub.ai/user/simbimbo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to install, configure, update, and troubleshoot the ocmemog durable memory plugin and sidecar for OpenClaw. It guides package-based installation first, then source checkout installation when needed, and includes configuration and validation steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer can execute mutable remote code and install unpinned dependencies when using the GitHub fallback path.

Mitigation: Prefer the public package install path or a pinned, audited commit before running the source installer.

Risk: The source installer can start persistent or background sidecar components with limited user gating.

Mitigation: Ask the agent to show files, services, configuration changes, logs, and stop or uninstall steps before starting the sidecar or loading LaunchAgents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/simbimbo/skills/ocmemog-installer)
- [ocmemog GitHub repository](https://github.com/simbimbo/ocmemog.git)
- [ocmemog GitHub release v0.1.2](https://github.com/simbimbo/ocmemog/releases/tag/v0.1.2)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include health-check and troubleshooting steps for the local ocmemog sidecar.]

## Skill Version(s):

0.1.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
