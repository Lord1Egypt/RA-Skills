## Description:

Execute commands on the host machine from inside the OpenClaw container via the HostLink daemon.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jebadiahgreenwood](https://clawhub.ai/user/jebadiahgreenwood)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use HostLink to let an OpenClaw agent run authenticated host-side shell commands for filesystem access, GPU or ML tooling, Docker management, and other host-level tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HostLink provides a host-command channel from inside the OpenClaw container.

Mitigation: Install it only when that access is intentional, restrict socket permissions, and require explicit human approval for filesystem, Docker, service, package, or credential-related commands.

Risk: The setup path can run the daemon with persistent, root-capable host access.

Mitigation: Review and pin the HostLink source before installation, avoid unverified sudo installation, run the daemon as a dedicated unprivileged user where possible, and disable boot persistence unless needed.

Risk: The authentication token protects the host command channel.

Mitigation: Use a strong token and keep it out of source-controlled or broadly readable configuration.

## Reference(s):

- [HostLink ClawHub Skill Page](https://clawhub.ai/jebadiahgreenwood/skills/hostlink)
- [HostLink Setup Guide](references/setup.md)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash, JSON, and YAML snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may execute on the host through an authenticated Unix socket or TCP/WireGuard transport.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
