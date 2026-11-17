## Description:

Inspects Huawei Cloud service status and CES metrics after fault drills, compares results with expected steady state, and generates an interactive HTML report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operations engineers use this skill after Huawei Cloud fault drills to review service status and monitoring metrics across regions, identify anomalies against expected steady state, and assess recovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The inspection may collect cloud inventory beyond the selected targets.

Mitigation: Use a dedicated read-only cloud account, separate configurations by region, and confirm target scope before running.

Risk: Text included in generated reports may not be handled safely.

Mitigation: Use trusted configurations, review reports, and keep them private.

Risk: An all-clear report may not independently establish that services have recovered.

Mitigation: Confirm recovery independently rather than relying only on the report conclusion.

Risk: KooCLI installation downloads and manual uninstallation can affect local CLI configuration.

Mitigation: Verify KooCLI downloads and back up its configuration before manual uninstall.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-ces-drill-inspection)
- [Huawei Cloud KooCLI documentation](https://support.huaweicloud.com/wtsnew-hcli/index.html)
- [Supported services and metrics](references/metrics-reference.md)
- [Read-only IAM permissions](references/iam-policies.md)
- [Verification method](references/verification-method.md)
- [KooCLI installation guidance](references/cli-installation-guide.md)

## Skill Output:

**Output Type(s):** [Analysis, Files]

**Output Format:** [Interactive HTML inspection report with status summaries, topology, metric charts, and recovery findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Offline-capable report; keep reports private and independently verify recovery conclusions.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
