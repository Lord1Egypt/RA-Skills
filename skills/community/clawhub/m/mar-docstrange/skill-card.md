## Description:

DocStrange helps agents use SkillBoss API Hub to convert PDFs and images into markdown, JSON, or CSV with confidence scoring for OCR, document field extraction, receipt parsing, and table conversion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marjoriebroad](https://clawhub.ai/user/marjoriebroad)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to configure and call a third-party document extraction API for invoices, receipts, contracts, bank statements, forms, scanned images, and table extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected documents are transmitted to SkillBoss API Hub for processing.

Mitigation: Review the provider's privacy, retention, and compliance terms before uploading sensitive or regulated documents; test first with non-sensitive samples.

Risk: API keys may be exposed if stored in plaintext configuration, logs, or committed files.

Mitigation: Use environment variables or a secret store for SKILLBOSS_API_KEY, avoid logging secrets, and rotate keys regularly.

Risk: Extracted fields can be incorrect or low confidence.

Mitigation: Request confidence scores when using JSON extraction and manually review fields with low confidence before relying on the output.

## Reference(s):

- [SkillBoss API Hub](https://api.heybossai.com)
- [SkillBoss API Docs](https://api.heybossai.com/v1/pilot)
- [ClawHub Skill Page](https://clawhub.ai/marjoriebroad/skills/mar-docstrange)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, JSON, CSV]

**Output Format:** [Markdown guidance with bash and JSON examples; API results may contain markdown, JSON, or CSV document extraction output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and transmits selected documents to https://api.heybossai.com.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
