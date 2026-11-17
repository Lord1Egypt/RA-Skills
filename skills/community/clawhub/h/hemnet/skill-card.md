## Description:

Search and analyse Swedish real estate on hemnet.se — active for-sale listings, sold prices (slutpriser), full listing details, photos, market statistics, address resolution, and a Swedish mortgage calculator. Use when the user asks about Swedish property, Hemnet, bostäder, lägenheter, villor, or slutpriser.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

People researching Swedish property use the skill to find and compare active and sold listings, review local market statistics, look up addresses, and estimate monthly mortgage costs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A browser fallback may be needed when Hemnet's access controls block the normal lookup path.

Mitigation: Review the separately provided Hemnet tools and their browser access before enabling the browser fallback.

Risk: Mortgage estimates depend on the provided financial inputs and the amortisation rules described by the skill.

Mitigation: Check the inputs and confirm current lender terms and applicable requirements before relying on an estimate.

## Reference(s):

- [Hemnet skill release on ClawHub](https://clawhub.ai/chrischall/skills/hemnet)
- [Hemnet](https://www.hemnet.se)

## Skill Output:

**Output Type(s):** [Analysis, Text, Guidance]

**Output Format:** [Markdown or plain text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include listing details, sold-price comparisons, market statistics, and mortgage estimates in SEK and m².]

## Skill Version(s):

1.2.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
