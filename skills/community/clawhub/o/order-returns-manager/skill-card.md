## Description:

Manage UK-focused Shopify and WooCommerce order operations through chat, including order lookup, tracking links, returns, refunds, exchanges, fulfilment, fraud holds, lost-parcel handling, and reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hussainpatan9](https://clawhub.ai/user/hussainpatan9)

### License/Terms of Use:

MIT-0

## Use Case:

Store operators and support teams use this skill to manage customer order and return workflows from OpenClaw chat channels. It is tailored for UK Shopify and WooCommerce merchants that need approval gates, refund handling, carrier links, and Consumer Rights Act-aware guidance.

### Deployment Geography for Use:

United Kingdom

## Known Risks and Mitigations:

Risk: The skill handles powerful Shopify and WooCommerce credentials and can affect orders, refunds, inventory, and customer messages.

Mitigation: Install only where encrypted secret storage and redaction are available; use least-privilege, rotatable credentials and avoid pasting live credentials into ordinary chat.

Risk: Refunds, cancellations, address changes, fulfilment updates, fraud holds, and customer emails can materially affect customers and store records.

Mitigation: Keep explicit merchant approval required for each sensitive action, especially refunds above the configured value threshold.

Risk: The scanner verdict is suspicious because credential capture is part of normal setup behavior.

Mitigation: Review the skill before installation and confirm the OpenClaw environment stores secrets securely before using production store access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hussainpatan9/skills/order-returns-manager)
- [Publisher profile](https://clawhub.ai/user/hussainpatan9)
- [Artifact README](artifact/README.md)
- [Setup guide](artifact/CONFIG.md)
- [Workflow examples](artifact/EXAMPLES.md)
- [Royal Mail claims](https://www.royalmail.com/help/claims)
- [DPD claims](https://www.dpd.co.uk/content/products_services/claims.jsp)
- [Evri parcel claims](https://www.evri.com/help/claim-for-a-parcel)
- [DHL parcel claim support](https://www.dhl.com/gb-en/home/our-divisions/parcel/customer-service/submit-a-claim.html)
- [Parcelforce compensation claims](https://www.parcelforce.com/help-and-advice/sending/compensation-claims)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Shell commands, Configuration, Guidance]

**Output Format:** [Conversational Markdown with order summaries, approval prompts, API request examples, reports, and customer-message drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses GBP, UK date conventions, approval gates for sensitive store actions, and direct carrier links when live tracking cannot be fetched.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
