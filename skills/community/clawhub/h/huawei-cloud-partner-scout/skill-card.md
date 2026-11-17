## Description:

Helps Huawei Cloud partners answer read-only questions about sub-customers, balances, billing, coupons, resources, and orders using the BSS SDK.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Huawei Cloud partners and their authorized staff use this skill to inspect partner-scope customer accounts, balances, bills, coupons, resources, and orders without making account changes.

### Deployment Geography for Use:

China (Huawei Cloud partner service fixed to cn-north-1)

## Known Risks and Mitigations:

Risk: Quality reporting may send prompts, results, stack traces, and local agent usage metadata to an external endpoint without full disclosure.

Mitigation: Review reporting before use with real billing data; disable it with SKILL_QUALITY_DISABLE=1 when external reporting is not acceptable, and isolate credentials and agent session files.

Risk: Incomplete or paginated billing queries could be mistaken for whole-account totals.

Mitigation: Identify the queried scope and period, disclose partial results, and avoid claims about unchecked charges.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-partner-scout)
- [Query templates and limits](references/related-commands.md)
- [Semantic query catalog](references/semantic/catalog.yml)
- [Read-only IAM policies](references/iam-policies.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands]

**Output Format:** [Concise conversational summary and facts, with optional Python SDK examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only partner account scope; partial results must be identified as partial.]

## Skill Version(s):

1.0.0 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
