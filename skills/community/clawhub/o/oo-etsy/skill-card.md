## Description:

Use the Etsy connector to read shop, listing, inventory, receipt, and transaction data, or record shipments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use the agent to inspect Etsy shops, listings, inventory, and receipts, review receipt transactions, and record shipments through their connected Etsy account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review marks the skill suspicious because its Etsy purpose is paired with instructions to run an externally downloaded installer, and reports that installation is not clearly related to Etsy tasks.

Mitigation: Avoid installation until the installer source, contents, and local changes are independently verified.

Risk: The scan is partial and unresolved local references leave the evidence incomplete.

Mitigation: Review the complete skill and its referenced files before installation or use.

Risk: A successful shipment-recording call notifies the buyer by email.

Mitigation: Confirm the shipment details before making the call.

## Reference(s):

- [Etsy API documentation](https://developers.etsy.com/documentation/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON payloads; Etsy responses are returned as JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Shipment recording notifies the buyer by email after each successful call.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
