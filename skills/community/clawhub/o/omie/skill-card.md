## Description:

Omie ERP integrates with the Omie API to manage clients, products, orders, NF-e invoices, financial accounts, stock, and real-time webhook events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jamesbot-agnt](https://clawhub.ai/user/jamesbot-agnt)

### License/Terms of Use:


## Use Case:

Employees, external operators, and developers use this skill to query and manage Omie ERP records for clients, products, sales orders, invoices, accounts payable and receivable, financial summaries, and stock. It also provides a webhook receiver for Omie event notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The webhook receiver is exposed by default and may receive sensitive ERP event data.

Mitigation: Bind the webhook locally or place it behind authenticated HTTPS infrastructure before use in a real Omie environment.

Risk: ERP API credentials grant access to business records and financial data.

Mitigation: Use least-privilege Omie credentials and keep OMIE_APP_KEY and OMIE_APP_SECRET out of logs, prompts, and shared transcripts.

Risk: Webhook payload logging can expose client, invoice, order, or financial details.

Mitigation: Avoid logging full ERP webhook payloads and add request verification and body-size limits before deployment.

## Reference(s):

- [Omie API endpoint](https://app.omie.com.br/api/v1)
- [ClawHub skill page](https://clawhub.ai/jamesbot-agnt/skills/omie)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses OMIE_APP_KEY and OMIE_APP_SECRET environment variables; API calls use a 30-second timeout and paginated results.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
