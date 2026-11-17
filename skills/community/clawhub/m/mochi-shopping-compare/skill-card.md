## Description:

Calculate purchase costs, compare saved price snapshots, preserve referral URLs and export reports. Use for Shopping Comparison.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hznetnewpower](https://clawhub.ai/user/hznetnewpower)

### License/Terms of Use:

MIT No Attribution

## Use Case:

External users can compare supplied product offers by price, shipping, discounts, quantity, and stated requirements, then save snapshots and export a report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved comparisons and exports retain supplied quotes, evidence, and complete URLs, which may contain sensitive details.

Mitigation: Review exported Markdown or CSV and its source links before sharing.

Risk: Offer data may be incomplete or time-sensitive, and a cost ranking does not establish product suitability.

Mitigation: Check source links and dates, currency, quantity, shipping, discounts, and missing-data details before deciding.

Risk: The optional external assistant and full filesystem execution were not verified.

Mitigation: Use a reviewed installer version and the intended workspace.

## Reference(s):

- [Input contract](references/input.md)
- [Shopping Comparison on ClawHub](https://clawhub.ai/hznetnewpower/skills/mochi-shopping-compare)
- [MochiLab](https://mochilab.bz)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, CSV]

**Output Format:** [Comparison summaries and Markdown or CSV report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports preserve source links, dates, quantities, amounts, and missing-data details.]

## Skill Version(s):

1.1.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
