## Description:

Create PDF invoices, estimates, receipts, contracts, and other business documents with PNG previews and optional payment links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mooshee](https://clawhub.ai/user/mooshee)

### License/Terms of Use:

MIT-0

## Use Case:

Business owners and service providers use the skill to prepare invoices, estimates, receipts, orders, and agreements. It gathers the supplied terms, checks totals, previews the document, and returns a PDF and download link.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured customer sync may record contact details and a document summary and start automated follow-up during PDF generation, without a separate approval step.

Mitigation: Before using real contact or business details, confirm whether customer sync is enabled, where information is stored, and how to disable automated follow-up. Review the Pressmark privacy policy for the fields shared.

Risk: The available evidence does not establish that guest mode disables customer-sync effects, and actual server behavior was not verified.

Mitigation: For reviews or demos, use synthetic contact details; verify sync behavior before processing real customer information.

## Reference(s):

- [ClawHub release](https://clawhub.ai/mooshee/skills/pressmark-invoice-generation)
- [Pressmark Studio](https://pressmark.dev)
- [Pressmark MCP server](https://pressmark.dev/mcp)
- [Invoice template](https://pressmark.dev/templates/invoice)
- [Pricing and plans](https://pressmark.dev/pricing)
- [Pressmark document types](references/archetypes.md)

## Skill Output:

**Output Type(s):** [PDF documents, PNG previews, Calculated totals, Download links]

**Output Format:** [PDF documents and PNG previews, with totals and download links presented to the user]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documents use user-supplied parties, items, dates, currency, and terms; payment links are optional.]

## Skill Version(s):

1.2.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
