## Description:

Use a connected Eagle Doc account to review usage and quotas, inspect request logs, and submit invoices, receipts, or PDFs for finance OCR.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use the skill through their connected Eagle Doc account to monitor usage and quotas, inspect request history, and extract structured data from finance documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A missing dependency can trigger downloaded code execution without separate user approval.

Mitigation: Review and approve dependency installation separately, preferably using a pinned release with verified integrity.

Risk: Finance documents submitted for OCR may contain sensitive financial information.

Mitigation: Connect only the intended Eagle Doc account and confirm which financial documents will be uploaded through OOMOL.

## Reference(s):

- [Eagle Doc Finance OCR API documentation](https://www.eagle-doc.com/en/documentation/finance-ocr/)
- [Eagle Doc API product information](https://www.eagle-doc.com/en/products/eagle-doc-apis/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-eagle-doc)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [Shell commands with JSON payloads and structured JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses include usage counters, quota summaries, request logs, or structured finance document extraction data, depending on the action.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
