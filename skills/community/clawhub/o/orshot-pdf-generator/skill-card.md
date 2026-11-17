## Description:

Creates designed invoice, certificate, report, and other PDFs from templates and row-based data through Orshot and automation tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[orshot](https://clawhub.ai/user/orshot)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create repeatable PDFs from spreadsheet, CRM, payment, or webhook data, then pass the resulting links to storage or delivery workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Document fields may contain personal or sensitive information, and default PDF links are public and non-expiring.

Mitigation: Send only fields needed in the document; store sensitive PDFs in private storage and share from there, since copying a PDF does not secure its original link.

Risk: Automated renders can incur page costs or route PDFs to unintended recipients.

Mitigation: Review workflow scope, page costs, and recipients before enabling automation or sending email.

## Reference(s):

- [Orshot PDF Generator skill page](https://orshot.com/agents/skills/pdf-generator)
- [Orshot MCP server integration](https://orshot.com/docs/integrations/mcp-server.md)
- [PDF generation guide](https://orshot.com/docs/pdf-generation.md)
- [Credits and usage](https://orshot.com/docs/definitions/credits-usage.md)

## Skill Output:

**Output Type(s):** [Guidance, API calls, Configuration, PDF URLs]

**Output Format:** [Markdown guidance with JSON/API examples and generated PDF links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Typically provides one PDF URL per render; the PDF is generated from a reusable template and supplied data.]

## Skill Version(s):

1.1.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
