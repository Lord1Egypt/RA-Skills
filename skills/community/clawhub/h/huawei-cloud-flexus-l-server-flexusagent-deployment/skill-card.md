## Description:

Deploy and manage a Dify-based AI agent development platform on Huawei Cloud Flexus L, including administrator password changes, MaaS model configuration, and workflow imports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to provision a Huawei Cloud Flexus L instance for Dify, set its administrator password, connect MaaS models, and import agent workflows.

### Deployment Geography for Use:

China (supported regions: Beijing 4, Shanghai 1, Guangzhou, and Guiyang 1)

## Known Risks and Mitigations:

Risk: Deployment can incur charges and enable recurring billing.

Mitigation: Confirm costs before deployment, use a test account, and verify or disable auto-renew and auto-pay when unwanted.

Risk: Deployment can expose services over a public network.

Mitigation: Inspect the security group after deployment and restrict access to trusted sources.

Risk: Administrator passwords may be exposed through command lines, chat logs, or retained cloud operations scripts.

Mitigation: Avoid entering passwords in commands or chat; rotate any password that was printed or embedded in retained scripts.

Risk: Cloud credentials grant permission to create or change resources.

Mitigation: Use tightly scoped temporary credentials and review the requested actions before running them.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-flexus-l-server-flexusagent-deployment)
- [Huawei Cloud Flexus L instance purchase guide](https://support.huaweicloud.com/api-flexusl/create_instance_0001.html)
- [Huawei Cloud Flexus L specifications](https://support.huaweicloud.com/productdesc-flexusl/pd_01_0003.html)
- [Huawei Cloud Python package index](https://repo.huaweicloud.com/repository/pypi/simple)
- [IAM permission policies](artifact/references/iam-policies.md)
- [Verification method](artifact/references/verification-method.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration guidance]

**Output Format:** [Markdown with command examples and deployment status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return instance access details and workflow or model configuration results.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
