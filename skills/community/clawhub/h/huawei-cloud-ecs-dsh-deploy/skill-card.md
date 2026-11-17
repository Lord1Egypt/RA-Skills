## Description:

Deploys DeepSeek Harness on Huawei Cloud Flexus X instances and provides region, connection, deployment, and verification guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud engineers use this skill to provision a Huawei Cloud Flexus X instance for DeepSeek Harness and to check regions, connectivity, deployment status, and access. Instance creation can incur charges and requires user confirmation of the deployment settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Failure cleanup may delete a server other than the one created by this deployment.

Mitigation: Avoid production use until rollback targets the exact created server ID; use temporary credentials scoped to an isolated cloud project and inspect existing resources before deployment.

Risk: The implementation's proxy binding and security-group validation do not support the documented network isolation assurances.

Mitigation: Verify the deployed proxy binding and actual inbound security-group rules. Restrict SSH to a trusted source IP and do not assume the web interface or proxy is unreachable from the public network.

Risk: API-key pre-seeding may expose secrets through shell escaping or Cloud Operations Center retention.

Mitigation: Avoid API-key pre-seeding until those issues are addressed. Pass temporary credentials through environment variables, keep secrets out of chat and logs, and retain TLS verification.

## Reference(s):

- [DeepSeek Harness repository](https://github.com/deepseek-ai/deepseek-harness)
- [Huawei Cloud Flexus X documentation](https://support.huaweicloud.com/productdesc-flexusx/pd_01_0002.html)
- [Huawei Cloud AK/SK authentication guide](https://support.huaweicloud.com/api-iam/iam_01_0001.html)
- [IAM policies](references/iam-policies.md)
- [Verification methods](references/verification-method.md)
- [Deployment acceptance criteria](references/acceptance-criteria.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Deployment guidance]

**Output Format:** [Markdown with shell commands, configuration steps, and deployment status details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
