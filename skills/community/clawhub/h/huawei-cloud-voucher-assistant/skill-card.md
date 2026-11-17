## Description:

Helps Huawei Cloud buyers check available vouchers and savings options, estimate deductions, and compare lower-cost or voucher-plus-cash alternatives.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Huawei Cloud customers and purchasing assistants use this skill to review account vouchers, estimate purchase savings, and consider cheaper service options or voucher-plus-cash payments. It does not place orders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud-account credentials are used to retrieve voucher information.

Mitigation: Use least-privilege Huawei Cloud credentials and review access before running account lookups.

Risk: The telemetry CLI may be installed from a remote latest-version package and report usage.

Mitigation: Review the installer before use, install only if the remote package is acceptable, and set SKILL_QUALITY_REPORT=0 to disable reporting.

Risk: A confirmed voucher-application action could affect a purchase if supported by the account integration.

Mitigation: Check the preview and obtain operator approval before confirming any application.

## Reference(s):

- [Voucher taxonomy and applicability](references/voucher-taxonomy.md)
- [IAM permissions and credential handling](references/iam-policies.md)
- [Verification method](references/verification-method.md)
- [CLI installation guide](references/cli-installation-guide.md)
- [Huawei Cloud KooCLI documentation](https://support.huaweicloud.com/cli/index.html)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Shell commands]

**Output Format:** [Text and structured JSON from the command-line actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Voucher balance and details, task recommendations, coverage estimates, and discount-plan options; voucher application is preview-only unless explicitly confirmed and supported.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
