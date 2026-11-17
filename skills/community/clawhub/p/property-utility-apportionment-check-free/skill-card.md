## Description:

面向物业公共能耗分摊核对表的本地免费核对技能，会逐行复算分摊额、校验合计勾稽、检测重复与空缺，并为结论引用原文依据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Property finance staff, managers, and reviewers use this skill to check monthly public utility apportionment tables before settlement, billing, or reconciliation. It helps recalculate line items, compare totals, identify duplicate or incomplete rows, and state when the material is insufficient for a conclusion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The checker does not replace legal, contract, billing-policy, or accounting review.

Mitigation: Use its findings as table-checking support and route legal, contractual, or policy questions to the appropriate reviewer.

Risk: The free version intentionally omits several advanced checks.

Mitigation: Review the omitted-check list before relying on the result, especially for percentage totals, contract price comparisons, vacant-unit treatment, and repeated-period issues.

Risk: The skill reads user-provided property utility table data from a local input file.

Mitigation: Run it only on data the user is authorized to process and keep sensitive billing or property records within approved environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/property-utility-apportionment-check-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Human-readable console text or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results include cited findings, insufficient-input messages, and the free-tier checks that were omitted.]

## Skill Version(s):

1.0.53 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
