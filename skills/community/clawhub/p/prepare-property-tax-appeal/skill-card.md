## Description:

Triage US residential property-tax assessment disputes, verify jurisdiction-specific rules and value basis, analyze comparable sales, and prepare fact-checked Markdown and PDF appeal packets when market value is a material ground.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mushanyoung](https://clawhub.ai/user/mushanyoung)

### License/Terms of Use:

MIT-0

## Use Case:

External property owners, tax professionals, and agents use this skill to classify US residential assessment disputes, verify the local appeal route, and prepare evidence-led market-value appeal packets from an address and notice value.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The skill may research public property records and create local appeal packet files.

Mitigation: Use a fresh case-specific folder, keep owner documents private, and review generated files before sharing or filing them.

Risk: Private portal links, signed URLs, credential-bearing URLs, or unnecessary owner details could expose sensitive information if placed in case data.

Mitigation: Record only canonical public HTTPS URLs for public sources and represent private owner evidence as attachment references without local paths, private links, or document contents.

Risk: Deadlines, forms, filing rules, valuation dates, and accepted evidence windows vary by jurisdiction and can change.

Mitigation: Independently verify the current official authority, form, deadline, submission method, and filing requirements before filing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mushanyoung/skills/prepare-property-tax-appeal)
- [Property Tax Appeal Methodology](references/methodology.md)
- [US Property Tax Appeal Routes](references/appeal-routes.md)
- [Case Data Schema (v2)](references/case-schema.md)
- [US Jurisdictions Routing Registry](references/us-jurisdictions.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown, PDF, JSON case data, and concise guidance with shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates local appeal packet files with validation gates; PDF output can be disabled when unsupported characters prevent safe PDF generation.]

## Skill Version(s):

3.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
