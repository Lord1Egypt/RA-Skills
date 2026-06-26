## Description: <br>
Monitor LibreNMS network devices and alerts via the LibreNMS REST API to get device status, health sensors, port statistics, and unresolved active alerts in read-only mode. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[florianbeer](https://clawhub.ai/user/florianbeer) <br>

### License/Terms of Use: <br>
MIT License <br>


## Use Case: <br>
Network operators, SREs, and infrastructure engineers use this skill to query LibreNMS for device availability, active alerts, health sensors, and interface statistics during monitoring and triage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a LibreNMS API token for authentication. <br>
Mitigation: Use a least-privileged read-only LibreNMS token and keep the local config file permission-restricted. <br>
Risk: The script disables TLS certificate verification by default for curl requests. <br>
Mitigation: Prefer a valid HTTPS certificate and remove the curl -k behavior when strict TLS validation works in the target environment. <br>
Risk: Monitoring output can expose infrastructure hostnames, IP addresses, device status, and alert details. <br>
Mitigation: Use the skill only in authorized environments and avoid sharing generated monitoring output outside approved operational channels. <br>


## Reference(s): <br>
- [LibreNMS API Documentation](https://docs.librenms.org/API/) <br>
- [ClawHub LibreNMS Skill Page](https://clawhub.ai/florianbeer/librenms) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and tabular terminal output with Markdown setup examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only LibreNMS API queries using a configured base URL and API token.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
