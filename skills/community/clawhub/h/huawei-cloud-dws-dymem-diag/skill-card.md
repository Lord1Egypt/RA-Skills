## Description:

Diagnoses high-memory conditions in Huawei Cloud DWS clusters by collecting memory metrics, analyzing likely causes, and producing a standardized report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Huawei Cloud DWS operators and engineers use this skill to investigate memory alarms, high memory use, or OOM events. It analyzes returned cluster metrics and produces a Chinese-language HTML diagnosis report without performing remediation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud credentials could be exposed through chat, shell commands, or command history.

Mitigation: Use a dedicated read-only identity, configure secrets interactively, and never paste credentials into chat or commands.

Risk: Generated reports may contain sensitive cluster and query details.

Mitigation: Keep reports private, exclude them from version control, and delete them when no longer needed.

Risk: The external CLI and MCP implementations have not been audited, and the documented MCP clone example needs correction.

Mitigation: Verify downloads and follow Huawei's installation guidance; check the documented repository's installation instructions before installing.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-dws-dymem-diag)
- [Memory Background Knowledge](artifact/references/memory-background.md)
- [Metric Reference](artifact/references/metric-reference.md)
- [KooCLI Installation Guide](artifact/references/cli-installation-guide.md)
- [DWS Autopilot MCP Server Installation Guide](artifact/references/dws-mcp-installation-guide.md)
- [IAM Policies](artifact/references/iam-policies.md)
- [Huawei Cloud KooCLI Installation Guide](https://support.huaweicloud.com/intl/en-us/qs-hcli/hcli_02_003.html)
- [Documented DWS Autopilot MCP Server Repository](https://github.com/huaweicloud/dws_ai_native/tree/dws_autopilot_mcp_server/hwcloud_dws_mcp_mag)

## Skill Output:

**Output Type(s):** [Text, HTML]

**Output Format:** [Diagnosis summary and Chinese-language HTML report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses returned DWS metrics; report times are shown in UTC+8. Diagnosis only; no remediation actions.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
