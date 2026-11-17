## Description:

Helps manage Huawei Cloud Flexus L instances by querying servers and traffic packages, controlling instance lifecycle, resetting passwords, and updating server information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to inspect Flexus L instances and traffic packages, start or stop servers, reboot instances, reset passwords, and update server details.

### Deployment Geography for Use:

Global, where Huawei Cloud Flexus L is available

## Known Risks and Mitigations:

Risk: Stop, reboot, update, and password-reset actions can change live servers; some safeguards are documented but not enforced by the scripts.

Mitigation: Verify the target is the intended Flexus L instance and require explicit confirmation before each change; check and report the resulting status.

Risk: Cloud credentials or passwords may be exposed if printed or pasted into chat or logs.

Mitigation: Use least-privilege, preferably temporary Huawei Cloud credentials; do not print environment variables or paste secrets into chat or logs.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-flexus-l-server-ops)
- [IAM policies](references/iam-policies.md)
- [Verification method](references/verification-method.md)
- [Huawei Cloud Flexus L instance documentation](https://support.huaweicloud.com/intl/zh-cn/flexusl_faq/faq_01_0003.html)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with shell commands and operation results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports queried instance details, traffic usage, or operation status as applicable.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
