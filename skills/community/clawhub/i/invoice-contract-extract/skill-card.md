## Description:

Reads PDF or image invoices, receipts, and contracts, extracts key fields such as amounts, dates, vendors, terms, and signatories, and returns structured JSON plus a readable report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sh2601393743-png](https://clawhub.ai/user/sh2601393743-png)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, legal, and operations teams use this skill to extract invoice, receipt, and contract data from user-provided PDFs or images. It supports single-file and batch extraction with validation checks for amounts, dates, required parties, key terms, and signatures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent must read invoices, receipts, contracts, images, or directories supplied by the user, which may contain sensitive financial, legal, or personal data.

Mitigation: Invoke the skill with explicit file paths and avoid broad directories unless batch processing is intended.

Risk: Extracted amounts, dates, contract terms, or signatures may be incomplete or uncertain.

Mitigation: Review validation warnings and manually confirm important financial or legal fields before using the output for decisions.

Risk: The skill can summarize contract clauses but is not a substitute for legal advice.

Mitigation: Route important contract interpretations or high-impact decisions to qualified legal review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sh2601393743-png/skills/invoice-contract-extract)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [JSON structured data and Markdown report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include validation warnings, extracted field tables, original-text comparisons, and batch summary tables.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
