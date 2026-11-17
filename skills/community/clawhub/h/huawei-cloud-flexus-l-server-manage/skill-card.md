## Description:

Helps manage Huawei Cloud Flexus L servers by finding available regions, images, and specifications and creating, renewing, or unsubscribing instances.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to review available Huawei Cloud Flexus L server options and manage purchases, renewals, and subscription cancellations.

### Deployment Geography for Use:

China mainland, Hong Kong, and Singapore (documented supported regions)

## Known Risks and Mitigations:

Risk: Cloud credentials can authorize server purchases, renewals, payments, and cancellations.

Mitigation: Use dedicated, temporary least-privilege credentials; avoid broad HCSS FullAccess and BSS Administrator policies where possible.

Risk: TLS certificate checks are disabled, making cloud requests unsafe on untrusted networks.

Mitigation: Do not use this release on untrusted networks until TLS verification is fixed.

Risk: Lifecycle actions can incur charges or interrupt subscribed resources.

Mitigation: Preview with dry-run and obtain explicit approval of the action and parameters before execution.

## Reference(s):

- [Flexus L instance purchase API](https://support.huaweicloud.com/api-flexusl/create_instance_0001.html)
- [Huawei Cloud AK/SK authentication](https://support.huaweicloud.com/api-iam/iam_01_0001.html)
- [API reference](references/api-reference.md)
- [IAM policies](references/iam-policies.md)
- [Image and specifications guide](references/image-specs-guide.md)
- [Permission guide](references/permission-guide.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with shell commands and operation results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes dry-run previews and confirmation before billed operations.]

## Skill Version(s):

1.0.2 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
