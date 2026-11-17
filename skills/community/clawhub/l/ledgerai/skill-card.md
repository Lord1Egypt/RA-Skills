## Description:

LedgerAI helps agents use the LedgerAI API for invoice processing, expense categorization, financial report generation, and receipt scanning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jbennett111](https://clawhub.ai/user/jbennett111)

### License/Terms of Use:


## Use Case:

External users and developers can use this skill to route bookkeeping requests through the LedgerAI API for parsing invoices, categorizing expenses, generating financial reports, and scanning receipts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends invoices, receipts, expense data, report inputs, email addresses, and API keys to LedgerAI/Voss Consulting Group endpoints.

Mitigation: Use it only with data approved for that third-party service and apply appropriate financial-data handling controls before deployment.

Risk: The LEDGERAI_API_URL override can redirect requests, including credentials and financial data, to a different endpoint.

Mitigation: Leave LEDGERAI_API_URL unset unless the destination is fully trusted and controlled.

Risk: The auto-signup flow can print a free API key to stderr, which may be captured in shared logs.

Mitigation: Avoid auto-signup in logged or shared environments and provide API keys through a secret manager or private environment variable.

## Reference(s):

- [ClawHub LedgerAI skill page](https://clawhub.ai/jbennett111/skills/ledgerai)
- [ClawHub publisher profile](https://clawhub.ai/user/jbennett111)
- [LedgerAI API base endpoint](https://anton.vosscg.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON API payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce API requests and JSON responses for invoice, expense, report, receipt, and health-check workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
