## Description:

Diagnoses Huawei Cloud DWS cluster I/O overload by collecting metrics, analyzing root causes, and producing a standardized report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Huawei Cloud DWS operators and database engineers use this read-only skill to investigate cluster I/O alarms and disk I/O anomalies. It gathers available metrics and reports likely causes for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diagnosis reports may contain SQL literals and usernames.

Mitigation: Keep reports in a private workspace, redact them before sharing, and delete them when no longer needed.

Risk: Cloud credentials could be exposed through chat or command history.

Mitigation: Use a dedicated read-only cloud identity and keep keys out of chat and command lines.

Risk: The bundled security review does not establish the runtime safety of external dependencies.

Mitigation: Verify KooCLI and MCP dependencies separately and follow Huawei's current installation instructions.

Risk: Suggestions involving audit settings or index removal could have operational impact.

Mitigation: Require separate operational review before acting on such suggestions.

## Reference(s):

- [I/O Diagnosis Reference](references/IO_DIAGNOSIS_REF.md)
- [I/O Background Knowledge](references/io-background.md)
- [Metric Reference](references/metric-reference.md)
- [Diagnosis JSON Format](references/diagnosis-json-format.md)
- [Report Output Format](references/output-format.md)
- [KooCLI Installation Guide](references/cli-installation-guide.md)
- [DWS Autopilot MCP Installation Guide](references/dws-mcp-installation-guide.md)
- [IAM Policy Requirements](references/iam-policies.md)
- [Huawei Cloud KooCLI installation instructions](https://support.huaweicloud.com/intl/en-us/qs-hcli/hcli_02_003_02.html)

## Skill Output:

**Output Type(s):** [Analysis, Text, HTML]

**Output Format:** [Diagnosis summary and complete HTML report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.2 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
