## Description:

Assesses capacity across Huawei Cloud services by comparing monitored peaks and valleys, estimating event traffic ceilings, and recommending scale-out actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud operators and infrastructure engineers use this skill to compare monitored capacity for target and entry instances, estimate event-time headroom, and decide whether to scale out.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The troubleshooting guidance includes a TLS verification bypass and persistent system-wide /etc/hosts changes.

Mitigation: Avoid disabling TLS verification. Verify DNS results before making hosts-file changes, review and back up /etc/hosts first, and remove temporary entries when they are no longer needed.

Risk: The workbook template was not fully inspected by the security scan.

Mitigation: Inspect the workbook and run assessments on a working copy in a controlled location.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-ces-aom-capacity-assessment)
- [KooCLI installation and configuration](references/cli-installation-guide.md)
- [IAM permission notes](references/iam-policies.md)
- [DNS troubleshooting](references/troubleshooting-dns.md)
- [Verification method](references/verification-method.md)
- [Huawei Cloud KooCLI installation guide](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)

## Skill Output:

**Output Type(s):** [Excel workbook, Analysis, Text summary, Shell commands]

**Output Format:** [Excel workbook with assessment results and a concise text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Assessment values and recommendations depend on the supplied instance data, monitoring coverage, and selected time window.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
