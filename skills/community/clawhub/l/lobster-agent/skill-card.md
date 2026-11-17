## Description:

A server monitoring agent that collects system metrics and reports them to the Coze Lobster platform, with CPU, memory, disk, network monitoring, alert delivery, and automatic node registration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hdguodada](https://clawhub.ai/user/hdguodada)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to install and manage a Linux systemd monitoring agent that reports host metrics, heartbeat data, and alerts to Coze. It is intended for servers that can reach the Coze API and where the operator accepts root-level installation of a persistent service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for root-level installation of a persistent systemd service without including the installer or generated agent code for review.

Mitigation: Inspect the installer, generated agent code, systemd unit, dependency sources, file permissions, and uninstall behavior before installing on production or sensitive servers.

Risk: The skill uses a Coze API key and reports monitoring data off-host.

Mitigation: Treat the API key as a secret and confirm what host metrics, heartbeat data, and alerts are transmitted before deployment.

## Reference(s):

- [Coze API documentation](https://www.coze.cn/docs/developer-docs/api)
- [Coze Lobster monitoring platform](https://coze.cn/s/7618478715609055278)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with shell command and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes service management commands, configuration paths, alert thresholds, and monitoring data fields.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
