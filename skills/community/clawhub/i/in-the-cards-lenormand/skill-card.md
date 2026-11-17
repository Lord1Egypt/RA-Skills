## Description:

Interprets Lenormand card spreads, saves readings as structured data and Markdown, and generates A4 PDFs, web pages, social cards, and long images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[locoda](https://clawhub.ai/user/locoda)

### License/Terms of Use:

MIT-0

## Use Case:

People seeking Lenormand readings use the skill to interpret freeform spreads or compatible Stargazer’s Oracle prompts, keep readings for later retrieval, and turn them into shareable visual documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Questions and interpretations are saved locally and remain there until deleted.

Mitigation: Avoid including sensitive details in readings and delete saved files when they are no longer needed.

Risk: Generated HTML contacts external font providers.

Mitigation: Be mindful of external requests when sharing or viewing generated pages, and avoid placing sensitive information in pages intended for sharing.

Risk: Output quality checks may skip browser checks in some environments.

Mitigation: Visually inspect generated documents and images before sharing.

Risk: Browser rendering is less isolated if Chromium runs without its sandbox or under an elevated account.

Mitigation: Keep Chromium’s sandbox enabled and use a regular user account.

## Reference(s):

- [Stargazer’s Oracle](https://lenor.star-oracle.app/)
- [Lenormand card reference](references/lenormand-cards.md)
- [Reading schema](references/reading-schema.md)
- [Spread parsing reference](references/spread-parsing.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, HTML, PDF, PNG images]

**Output Format:** [Structured JSON and Markdown readings, standalone HTML pages, and rendered PDF or PNG products]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports Chinese and English readings; saved readings can be retrieved and regenerated into visual formats.]

## Skill Version(s):

3.5.2 (source: SKILL.md frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
