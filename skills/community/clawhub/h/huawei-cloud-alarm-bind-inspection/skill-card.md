## Description:

Reads Huawei Cloud CES and AOM alarm baselines and rules, analyzes alarm binding coverage, and generates instance-level reports and remediation suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud operations engineers use this skill to compare configured CES and AOM alarm rules with baseline metrics and events, identify instance-level coverage gaps, and prepare reports with remediation suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports disabled certificate checks and persistent system DNS changes; the scan was partial and may not cover all behavior.

Mitigation: Review the relevant scripts and network behavior before execution, keep certificate verification enabled, and avoid persistent DNS changes unless explicitly approved.

Risk: ClawScan reports destructive CLI cleanup commands and an unverified installer download.

Mitigation: Review cleanup commands before running them and verify installer origin and integrity before installation.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-alarm-bind-inspection)
- [KooCLI documentation](https://support.huaweicloud.com/wtsnew-hcli/index.html)
- [Huawei Cloud IAM documentation](https://support.huaweicloud.com/usermanual-iam/iam_01_0001.html)
- [Huawei Cloud CES API documentation](https://support.huaweicloud.com/api-ces/ces_03_0001.html)
- [Huawei Cloud AOM API documentation](https://support.huaweicloud.com/api-aom/aom_04_0001.html)
- [CLI installation guide](references/cli-installation-guide.md)
- [IAM policies](references/iam-policies.md)
- [Verification method](references/verification-method.md)
- [Acceptance criteria](references/acceptance-criteria.md)
- [Design notes](references/design.md)

## Skill Output:

**Output Type(s):** [Analysis, Files, JSON]

**Output Format:** [Excel workbooks and an HTML report, with JSON intermediate data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports show instance-level metric and event binding coverage and remediation suggestions.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
