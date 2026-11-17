## Description:

Convert estimates to invoices, record payment details, calculate balances, and create receipts or credit notes with Pressmark. Built by Moosh Works (https://mooshworks.com).

This skill is ready for commercial/non-commercial use.

## Publisher:

[mooshee](https://clawhub.ai/user/mooshee)

### License/Terms of Use:

MIT-0

## Use Case:

People handling customer or tenant documents use this skill to convert estimates into invoices, record payment details, calculate remaining balances, and prepare receipts or credit notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting Pressmark sends supplied document details to its hosted service; configured customer sync can share contact details and a document summary and start automated follow-up.

Mitigation: Review privacy and customer-sync settings before connecting. For demos, use a guest session and synthetic contact details.

Risk: An incorrect cumulative paid amount can produce an incorrect invoice balance or payment status.

Mitigation: Verify the cumulative payment total before recording a payment.

Risk: Hosted-server behavior was not verified in the release security review.

Mitigation: Review Pressmark's privacy and customer-sync settings and confirm the resulting document details before use.

## Reference(s):

- [Document conversion fields](artifact/references/state-machine.md)
- [Pressmark Studio](https://pressmark.dev)
- [Pressmark MCP server](https://pressmark.dev/mcp)
- [Privacy policy](https://pressmark.dev/privacy)
- [Credit note template](https://pressmark.dev/templates/credit-note)
- [Receipt template](https://pressmark.dev/templates/receipt)
- [Security deposit statement template](https://pressmark.dev/templates/security-deposit-disposition)

## Skill Output:

**Output Type(s):** [Business documents, Payment and balance details, Guidance]

**Output Format:** [Invoices, receipts, or credit notes with payment status and balance fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documents are prepared from supplied details; recording a payment does not move money.]

## Skill Version(s):

1.2.4 (source: frontmatter; release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
