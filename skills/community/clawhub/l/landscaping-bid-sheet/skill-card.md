## Description:

Creates a detailed landscaping bid with materials, labor, equipment, maintenance terms and site notes for US properties. Use when the user asks for landscaping bid, lawn care estimate, landscape quote. For US landscaping contractors bidding on residential and commercial jobs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

US landscaping contractors use the skill to prepare customer-facing estimates for residential and commercial work, organizing job phases, materials, labor, equipment, maintenance, exclusions, and payment terms.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The bid generator produces zero-dollar prices, making its quotes unreliable.

Mitigation: Independently calculate and verify every line item and total before sharing a bid with a customer.

Risk: The optional Windows download is separate from this workflow; the linked release describes a different tool, and its binary was not reviewed.

Mitigation: Assess the download separately and verify its source and contents before running it.

## Reference(s):

- [Landscaping bid considerations](references/landscaping-bids.md)
- [ClawHub skill page](https://clawhub.ai/rapidworker1/skills/landscaping-bid-sheet)

## Skill Output:

**Output Type(s):** [Markdown, Text]

**Output Format:** [Markdown price-tier report (`price-tiers.md`) with bid guardrails]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes tiered prices and written guardrails; verify all calculations independently before sharing bids.]

## Skill Version(s):

1.0.7 (source: SKILL.md frontmatter; ClawHub release 1.0.7)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
