## Description:

Invoice Scan helps agents extract, validate, and export structured invoice and receipt data from images, scanned documents, and PDFs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mr-muddle](https://clawhub.ai/user/mr-muddle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, finance teams, and agent users use this skill to read invoice or receipt documents, classify document type, extract canonical fields, check arithmetic and business rules, and produce exportable invoice data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive invoice documents and CLI mode sends full invoice images and extracted business data to an external AI provider.

Mitigation: Use only approved documents and credentials, review before installing or using on confidential invoices, and confirm external processing is acceptable for the workflow.

Risk: Security evidence identifies flaws around retry merging, CSV export, remote upload scoping, input size limits, endpoint restrictions, and dependency pinning.

Mitigation: Avoid exposing the package as a long-running service until these areas are reviewed and addressed; scan and review the skill before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mr-muddle/skills/invoice-scan)
- [Canonical Invoice Schema](references/canonical-schema.md)
- [Validation Rules](references/validation-rules.md)
- [Anthropic API endpoint](https://api.anthropic.com)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, CSV, Excel files, shell commands, configuration, guidance]

**Output Format:** [Markdown summary with optional JSON, CSV, or Excel export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent-native mode performs local formatting only; CLI mode can send base64 invoice images and sensitive invoice fields to Anthropic.]

## Skill Version(s):

2.2.0 (source: server release evidence and scripts/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
