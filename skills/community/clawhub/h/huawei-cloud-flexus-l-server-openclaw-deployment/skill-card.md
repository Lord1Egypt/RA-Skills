## Description:

Deploy OpenClaw on Huawei Cloud Flexus L instances and configure models and messaging channels; Web UI access must be enabled manually in the Huawei Cloud console.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud administrators use this skill to provision OpenClaw on Huawei Cloud Flexus L and configure its language models and messaging channels.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Setup may broaden agent access.

Mitigation: Require owner-selected sender lists and review tool and agent access settings before use.

Risk: Credential values may be exposed in execution output.

Mitigation: Require secret redaction, use narrowly scoped temporary cloud credentials, and rotate any credentials exposed in output.

Risk: Deployment may create recurring charges without clear payment and renewal choices.

Mitigation: Make payment and renewal explicit choices and review billing before creating resources.

Risk: Administrative access may be exposed publicly.

Mitigation: Use private or TLS-protected administrative access.

## Reference(s):

- [IAM Permission Policy](references/iam-policies.md)
- [Verification Method](references/verification-method.md)
- [Huawei Cloud Flexus L Instance Console](https://console.huaweicloud.com/smb/?/resource/list)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown instructions with Python CLI examples and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deployment and configuration guidance that may require cloud credentials and instance details from the user.]

## Skill Version(s):

1.0.3 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
