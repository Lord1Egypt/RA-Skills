## Description:

Deploys Hermes on Huawei Cloud Flexus L instances and helps configure ModelArts models, robot channels, and gateway operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to provision a Hermes instance on Huawei Cloud, configure its model and messaging channels, and check or restart related services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud credentials can create instances and run remote COC scripts.

Mitigation: Use dedicated, temporary, least-privilege credentials and avoid passing secrets on the command line.

Risk: Provisioned resources and auto-renewal or auto-pay settings can incur charges.

Mitigation: Review pricing and billing settings before deployment; disable auto-renewal or auto-pay if unwanted.

Risk: Messaging-channel access or retained bot secrets may expose deployed services.

Mitigation: Restrict Feishu and WeCom allowed users after setup, and rotate bot secrets previously used with this release.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-flexus-l-server-hermes-deployment)
- [CLI installation guide](artifact/references/cli-installation-guide.md)
- [IAM policies](artifact/references/iam-policies.md)
- [Verification method](artifact/references/verification-method.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration guidance, JSON status reports]

**Output Format:** [Markdown guidance and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes deployment identifiers, operation status, and configuration results.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
