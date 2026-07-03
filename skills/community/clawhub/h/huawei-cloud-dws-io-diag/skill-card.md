## Description: <br>
Diagnoses Huawei Cloud DWS cluster I/O overload by collecting KooCLI or DWS Autopilot MCP metrics, analyzing root causes with a three-stage decision tree, and producing a standardized report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huaweiclouddev](https://clawhub.ai/user/huaweiclouddev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to investigate Huawei Cloud DWS high-I/O alarms and disk I/O anomalies, collect read-only cluster metrics, and generate a diagnosis report for follow-up review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/huaweiclouddev/skills/huawei-cloud-dws-io-diag) <br>
- [CLI Installation Guide](references/cli-installation-guide.md) <br>
- [DWS Autopilot MCP Server Installation Guide](references/dws-mcp-installation-guide.md) <br>
- [IAM Policies](references/iam-policies.md) <br>
- [Metric Reference](references/metric-reference.md) <br>
- [I/O Background Knowledge](references/io-background.md) <br>
- [Output Format](references/output-format.md) <br>
- [diagnosis_json Output Format Reference](references/diagnosis-json-format.md) <br>
- [I/O Diagnosis Reference](references/IO_DIAGNOSIS_REF.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [HTML diagnosis report plus diagnosis_json data and inline shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses read-only DWS diagnostics credentials; generated reports may include SQL text, usernames, query IDs, host/IP data, and workload patterns that should be handled as sensitive operational data.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
