## Description: <br>
Lobster Agent is a Linux server monitoring skill that collects CPU, memory, disk, and network metrics, reports them to the Coze Lobster platform, and supports alerting and automatic node registration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hdguodada](https://clawhub.ai/user/hdguodada) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and server operators use this skill to install and manage a persistent Linux monitoring agent that reports host health metrics and alerts to Coze. It is intended for Linux systems with systemd, root installation access, and approved connectivity to the Coze API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill describes root-level installation of a persistent systemd service without providing reviewable installer or generated agent source artifacts. <br>
Mitigation: Request and review the installer, generated agent code, service unit, dependency list, and uninstall behavior before installing on any real server. <br>
Risk: The agent reports operational metrics and possible log-derived alerts to Coze, but the artifact does not provide enough data-handling detail. <br>
Mitigation: Deploy first on a test Linux host, use a least-privileged Coze API key, and only use it where sending this telemetry to Coze is approved. <br>


## Reference(s): <br>
- [Coze API documentation](https://www.coze.cn/docs/developer-docs/api) <br>
- [Lobster monitoring platform](https://coze.cn/s/7618478715609055278) <br>
- [ClawHub skill page](https://clawhub.ai/hdguodada/lobster-agent) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes service management commands, alert threshold guidance, and the agent configuration schema.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
