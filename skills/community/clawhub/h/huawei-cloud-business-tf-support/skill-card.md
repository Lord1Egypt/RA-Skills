## Description:

Helps Terraform users query Huawei Cloud billing, balances, orders, resource usage, and prices through read-only scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers using Terraform can look up Huawei Cloud bills, account balances, coupons, orders, refunds, resource usage, and pricing without making cloud changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires Huawei Cloud credentials and can query sensitive billing and resource information.

Mitigation: Use tightly scoped, read-only credentials limited to the billing, pricing, and resource-query APIs needed; protect query output.

Risk: API connections are configured with TLS verification disabled.

Mitigation: Review and fix the TLS-disabled configuration before using the skill with credentials.

Risk: Local dependency setup can bootstrap pip from a remote source.

Mitigation: Review the remote get-pip bootstrap path and dependency setup before installing or running the skill.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-business-tf-support)
- [BSS query usage guide](references/bss/guide.md)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Markdown summaries and JSON query results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may contain sensitive billing and account details.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
