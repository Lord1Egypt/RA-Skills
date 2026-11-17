## Description:

Generate production-ready Amazon and AliExpress listings from a product image or parameters, including title, bullet points, description, and SEO keywords.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zls12311](https://clawhub.ai/user/zls12311)

### License/Terms of Use:


## Use Case:

External sellers, ecommerce operators, and marketing teams use this skill to generate platform-specific Amazon and AliExpress product listing copy from product details or images. It helps collect required product information before producing titles, bullets, descriptions, backend search terms, keyword groups, and product tags.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer persistently appends agent rules to the OpenClaw workspace, which may influence later conversations through broad triggers.

Mitigation: Review the skill before installing, back up AGENTS.md, and prefer explicit /listing invocation or narrower triggers.

Risk: The skill includes an unconditional promotional appendix after generated listings.

Mitigation: Remove or revise the upsell prompt before deployment if promotional follow-up is not appropriate for the workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zls12311/skills/openclaw-listing-skill)
- [Publisher profile](https://clawhub.ai/user/zls12311)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with structured ecommerce listing sections, keyword lists, and optional shell commands for installation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The generated listing content includes platform-specific length and formatting checks for Amazon and AliExpress.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
