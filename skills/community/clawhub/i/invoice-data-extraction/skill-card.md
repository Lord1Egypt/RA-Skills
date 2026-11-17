## Description:

Helps agents extract structured rows from invoices and other financial documents through the Invoice Data Extraction service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[invoicedataextraction](https://clawhub.ai/user/invoicedataextraction)

### License/Terms of Use:

MIT-0

## Use Case:

People handling invoices, receipts, and other financial documents use this skill to obtain consistent, spreadsheet-ready rows, including line items from scans and batches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected financial documents and extraction instructions are sent to an external service.

Mitigation: Send only documents the user has authorized for this service.

Risk: Exposure of the service API key could allow unauthorized access.

Mitigation: Store it in a secret environment variable and restrict it to api.invoicedataextraction.com when possible.

Risk: Extracted values may need human review before bookkeeping use.

Mitigation: Review flagged rows, failed pages, and uncertainty notes before relying on the output.

Risk: Result output is described as available for up to 90 days.

Mitigation: Download needed results within the stated availability window.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/invoicedataextraction/skills/invoice-data-extraction)
- [Agent integration guide](https://invoicedataextraction.com/docs/agents)
- [Agent guide](https://invoicedataextraction.com/docs/agents.md)
- [API documentation](https://invoicedataextraction.com/docs/api.md)
- [Node.js SDK documentation](https://invoicedataextraction.com/docs/node.md)
- [Python SDK documentation](https://invoicedataextraction.com/docs/python.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Configuration guidance]

**Output Format:** [Guidance and commands; structured JSON rows or links to CSV, XLSX, and JSON exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Flags rows needing review and reports failed pages or unanswered questions.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
