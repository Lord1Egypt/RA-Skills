## Description:

物业专项维修资金使用与分摊核对（免费版）对维修资金归集与分摊明细执行6项本地算术和格式检查，并为每条结论引用原文行号与数字。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

External users such as property company project managers, finance staff, and homeowners' committee finance members use this skill to check Chinese maintenance-fund collection, usage, voting-ratio, and per-household apportionment tables before disclosure or after fund use. It helps identify arithmetic, duplicate-apportionment, blank-field, formatting, and insufficient-material issues without treating the result as legal approval, audit, bank verification, or proof that source documents are genuine.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Users may overread arithmetic and formatting checks as legal approval, audit sign-off, bank verification, or proof that source documents are genuine.

Mitigation: Use the output as a checking aid only, and route legal validity, audit conclusions, bank-balance verification, and source-document authenticity to the appropriate professional or authority.

Risk: Maintenance-fund tables may include homeowner identifiers or other sensitive data.

Mitigation: Run the checker locally, minimize shared input and output, and review any unmasked-identifier findings before distributing results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/property-maintenance-fund-check-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [Human-readable CLI text or JSON result report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source line numbers and figures; insufficient input returns missing-material guidance rather than a positive or negative conclusion.]

## Skill Version(s):

1.0.7 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
