## Description:

OW Buyer helps agents publish global procurement requests, receive bids, evaluate suppliers with weighted scoring, and guide users to complete transactions through external shops.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qutongyuan](https://clawhub.ai/user/qutongyuan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to publish procurement requests, collect supplier bids, compare offers, and identify preferred suppliers before completing purchases through seller-provided shop links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Procurement details may leave the local machine or be stored locally.

Mitigation: Review the skill before installation and use it only with procurement details you are comfortable storing or transmitting.

Risk: Endpoint configuration could send procurement data to an untrusted service.

Mitigation: Set OW_API_URL only to a trusted HTTPS endpoint before real use.

Risk: Bid, request, supplier, or authenticity evidence may be unsafe or misleading.

Mitigation: Validate bid and request identifiers, confirm bidder identity, and independently verify supplier evidence before selecting a winner.

Risk: Publication or winner selection could happen without enough user review.

Mitigation: Add or require explicit confirmation before publishing procurement requests or accepting a supplier.

Risk: Payment account, payment link, contact, or shop-link data in state files could expose sensitive transaction details.

Mitigation: Remove payment account and payment-link fields from state, and review stored contact or shop-link data regularly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qutongyuan/skills/ow-buyer)
- [OW API endpoint](https://www.owshanghai.com/api)
- [Bid format](artifact/patterns/bid-format.md)
- [Multi-platform publishing format](artifact/patterns/multi-platform-format.md)
- [Payment and transaction flow](artifact/patterns/payment.md)
- [Scoring rules](artifact/patterns/scoring.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local procurement state files and notification records.]

## Skill Version(s):

2.3.4 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
