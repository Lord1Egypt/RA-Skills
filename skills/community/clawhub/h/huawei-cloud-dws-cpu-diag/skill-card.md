## Description:

Diagnoses high CPU usage in Huawei Cloud DWS clusters from monitoring and host data and produces a standardized report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to investigate DWS CPU alarms, identify likely customer-side or system-side causes, and review the findings in a diagnosis report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Monitoring, host, and SQL diagnostics may expose sensitive operational data.

Mitigation: Grant only the required read permissions and restrict access to generated reports.

Risk: The installation guidance can expose access keys in command history or plaintext configuration.

Mitigation: Do not put keys in shell commands or chat; protect configuration files with restrictive permissions and use least-privilege credentials.

Risk: Incomplete HTML escaping of dynamic report fields may allow unsafe content when a report is opened in a browser.

Mitigation: Escape all dynamic fields before viewing or sharing reports from untrusted clusters, or open them with scripts disabled.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-dws-cpu-diag)
- [DWS Autopilot MCP installation guide](artifact/references/dws-mcp-installation-guide.md)
- [IAM policies](artifact/references/iam-policies.md)
- [Metric reference](artifact/references/metric-reference.md)

## Skill Output:

**Output Type(s):** [Text, HTML report file]

**Output Format:** [HTML diagnosis report with a brief diagnosis summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Saves a local report containing cluster diagnostics and potentially sensitive SQL and host data; report times use Beijing time.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
