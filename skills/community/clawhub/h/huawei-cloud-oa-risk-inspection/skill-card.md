## Description:

Inspects Huawei Cloud OA, Config, and SecMaster findings and creates HTML and Excel risk reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud administrators and security engineers use this skill to collect Huawei Cloud tenant findings from OA, Config, and SecMaster and produce an inspection report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks the release suspicious with medium confidence, citing report-generation security weaknesses; scan coverage was partial.

Mitigation: Review the report-generation findings and inspect generated reports before sharing them; restrict access to reports containing tenant data.

Risk: The security guidance calls out automatic dependency installation and access-key handling for review.

Mitigation: Review dependency setup and credential handling before use, and configure only the access the inspection requires.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-oa-risk-inspection)
- [Huawei Cloud Config Service Documentation](https://support.huaweicloud.com/rms/index.html)
- [Huawei Cloud OA Service Documentation](https://support.huaweicloud.com/productdesc-oa/oa_01_0002.html)
- [Huawei Cloud SecMaster Service Documentation](https://support.huaweicloud.com/secmaster/index.html)
- [Huawei Cloud KooCLI Installation Guide](https://support.huaweicloud.com/qs-hcli/hcli_02.html)
- [Huawei Cloud IAM Authentication Guide](https://support.huaweicloud.com/api-iam/iam_01_0001.html)
- [Local verification method](references/verification-method.md)
- [Local acceptance criteria](references/acceptance-criteria.md)
- [Local IAM policies guide](references/iam-policies.md)
- [Local CLI installation guide](references/cli-installation-guide.md)

## Skill Output:

**Output Type(s):** [Analysis, Files, Shell commands]

**Output Format:** [HTML and Excel inspection reports with a text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports summarize tenant risk inspection results across the selected Huawei Cloud services.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
