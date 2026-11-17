## Description:

Audits Amazon listings for content quality, indexability, intent coverage, discoverability, and compliance, producing diagnostic scores, critical issues, and prioritized fix guidance without rewriting copy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[buluslan](https://clawhub.ai/user/buluslan)

### License/Terms of Use:

MIT

## Use Case:

External Amazon sellers, ecommerce operators, and agent users use this skill to diagnose listing health from pasted text, URLs, or ASINs and receive structured scores, critical issues, and prioritized remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated responses and reports may include third-party promotional branding that is inappropriate for client-facing or strict output formats.

Mitigation: Review report output and branding requirements before installation or external sharing.

Risk: The optional SellerSprite fetch helper may send an ASIN and SellerSprite API key to SellerSprite.

Mitigation: Prefer pasted or exported listing JSON for local audits; use the helper only when sharing that data and key is acceptable.

## Reference(s):

- [ClawHub listing](https://clawhub.ai/buluslan/skills/listing-doctor)
- [README_EN.md](README_EN.md)
- [rules.json](references/rules.json)
- [new-rules-2026.md](references/new-rules-2026.md)
- [cdq_weights.json](references/cdq_weights.json)
- [indexability_rules.json](references/indexability_rules.json)
- [cosmo_ontology.json](references/cosmo_ontology.json)
- [alexa_lexicon.json](references/alexa_lexicon.json)
- [image_rules.json](references/image_rules.json)
- [report-template.md](assets/report-template.md)
- [output-template.json](assets/output-template.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown reports and structured JSON, with occasional shell commands for running listing audits]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Diagnosis only; does not rewrite listing copy. Missing listing fields reduce scoring coverage rather than blocking output.]

## Skill Version(s):

0.3.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
