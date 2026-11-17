## Description:

Assists agents with Chinese government procurement and tender-document analysis by extracting structured requirements, risk flags, rejection clauses, price-score scenarios, Excel-ready tables, and compliance citations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chesaram](https://clawhub.ai/user/chesaram)

### License/Terms of Use:

MIT-0

## Use Case:

Procurement, bidding, compliance, and review teams use this skill to interpret Chinese government procurement or enterprise tender documents, identify bid-risk conditions, and prepare structured review outputs. It supports analysis and planning, but its legal and pricing conclusions are review aids rather than final legal, commercial, or bidding decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tender and bid materials may contain sensitive commercial or procurement information.

Mitigation: Use this skill only where the assistant, OCR path, and configured knowledge-base workflow are approved for the data being uploaded.

Risk: Legal, compliance, and pricing outputs may be incorrect or incomplete if source documents are unclear, OCR fails, formulas contain unconfirmed parameters, or regulations require expert interpretation.

Mitigation: Treat outputs as review aids and require qualified human review before legal, commercial, or bidding decisions.

## Reference(s):

- [IMA Knowledge Base Call Strategy](artifact/references/ima-kb.md)
- [Price Score Formula Cookbook](artifact/references/price-formula-cookbook.md)
- [Common Clause Examples](artifact/references/common-clauses.md)
- [Test Cases and Acceptance Criteria](artifact/references/test-cases.md)
- [Project Repository](https://github.com/chesaram/my-skill-hub)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown reports with optional Excel-ready workbook structure and calculation tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include structured tables, price-score scenarios, risk summaries, and compliance citation guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact files declare 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
