## Description:

Helps deploy JF store-traffic cameras, configure counting areas, query foot-traffic statistics, and generate visual reports for chain stores.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jftech](https://clawhub.ai/user/jftech)

### License/Terms of Use:

MIT-0

## Use Case:

Store operators and developers use this skill to set up supported JF cameras, configure in-store traffic counting, and review store-level traffic and customer trends.

### Deployment Geography for Use:

Mainland China

## Known Risks and Mitigations:

Risk: The skill can delete remote stores and devices without an enforced confirmation step.

Mitigation: Require explicit human approval before deleting a store or device, and grant access only to accounts authorized for those operations.

Risk: Using live JF API credentials permits changes to store and device resources.

Mitigation: Review the skill before installation with real credentials and restrict its use to authorized accounts.

## Reference(s):

- [JF Store Traffic on ClawHub](https://clawhub.ai/jftech/skills/jf-store-traffic)
- [JF Store Traffic API Reference](references/api-reference.md)

## Skill Output:

**Output Type(s):** [Text, JSON, HTML reports, Configuration instructions]

**Output Format:** [Markdown tables, JSON configuration and statistics, and standalone HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports summarize traffic KPIs, daily trends, customer demographics, and visit-group sizes.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
