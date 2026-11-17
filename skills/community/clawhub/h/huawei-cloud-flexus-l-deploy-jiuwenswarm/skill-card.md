## Description:

Deploy and configure JiuwenSwarm on Huawei Cloud Flexus L instances, including instance setup, model APIs, and messaging channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to deploy JiuwenSwarm or JiuwenClaw on supported Huawei Cloud Flexus L instances, configure model and messaging services, and check deployment status.

### Deployment Geography for Use:

China: cn-north-4, cn-east-3, cn-south-1, and cn-southwest-2.

## Known Risks and Mitigations:

Risk: Credential handling may weaken protection for cloud credentials.

Mitigation: Before use, require fixes that preserve credential encryption, and use scoped temporary credentials in an isolated environment without a normal hcloud profile.

Risk: Deployment records or output may expose model API keys or other secrets.

Mitigation: Require removal of secret output and unnecessary secret copies; rotate keys if deployment output containing them has been shared.

Risk: Automatic renewal may create ongoing cloud charges without clear notice.

Mitigation: Require renewal choices to be disclosed clearly and obtain the user's explicit choice before renewal.

Risk: Updates to an existing installation may overwrite configuration or data.

Mitigation: Back up the existing installation before deployment or configuration changes.

Risk: Opening the web interface can expose it to outside access.

Mitigation: Restrict web access, protect it with TLS, and open the required security-group port only when needed.

## Reference(s):

- [Huawei Cloud IAM FAQ](https://support.huaweicloud.com/iam_faq/iam_01_0620.html)
- [IAM policies](artifact/references/iam-policies.md)
- [Deploying on an existing instance and cleaning up resources](artifact/references/existing-instance-deploy-and-resource-cleanup.md)
- [Deployment checklist](artifact/references/deployment-checklist.md)
- [ClawHub skill page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-flexus-l-deploy-jiuwenswarm)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Deployment status, Guidance]

**Output Format:** [CLI text, JSON status and instance details, YAML and environment configuration, and shell scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify cloud resources and service configuration; instance creation, deployment, and resource changes require user confirmation.]

## Skill Version(s):

1.0.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
