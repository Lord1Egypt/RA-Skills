## Description:

促销活动价格台账逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文。本免费版执行引擎声明的免费检查项。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

E-commerce and retail operations or price-compliance teams use this skill to check promotional price ledger text before and during campaigns. It recalculates row-level prices, checks totals, flags duplicates or missing fields, and cites source rows when it can execute the free checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be mistaken for legal or regulatory review even though it only checks ledger arithmetic, consistency, duplicates, and required fields.

Mitigation: Use the output as a local pre-check and route pricing decisions or suspected violations to qualified compliance or legal reviewers.

Risk: Materials with missing headers, ambiguous discounts, invalid dates, or unsupported source formats can prevent reliable conclusions.

Mitigation: Provide tabular ledger text with required headers and review any insufficient-input report before relying on the result.

Risk: The free package explicitly omits advanced checks such as platform-specific legality, live page prices, original document review, and several paid-tier consistency checks.

Mitigation: Treat omitted checks as out of scope and perform separate review when those determinations matter.

Risk: The runner reads the user-selected input file, which may contain sensitive ledger data.

Mitigation: Run it locally on approved files only and avoid placing unnecessary confidential content in the input.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/promo-price-compliance-check-free)

## Skill Output:

**Output Type(s):** [analysis, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and command output; optional JSON result when run with --json]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local Node.js execution over user-provided ledger text; materials may be insufficient, in which case the skill reports missing inputs instead of producing a compliance conclusion.]

## Skill Version(s):

1.0.1 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
