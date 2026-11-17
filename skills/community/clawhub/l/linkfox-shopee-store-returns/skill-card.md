## Description:

Helps agents query and process Shopee store return and refund workflows through LinkFox, including return lists, return details, seller confirmation, disputes, offers, proof uploads, and reverse logistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers and commerce operators use this skill to query Shopee return and refund records for authorized shops and prepare seller return actions such as confirmation, offers, disputes, proof uploads, and reverse-logistics lookup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Return, dispute, proof, shop, phone, token, and billing data may be sent through LinkFox services.

Mitigation: Use only LinkFox and Shopee accounts approved for this processing, and avoid sending unnecessary sensitive fields.

Risk: Seller actions and payment-related commands can affect store operations or billing.

Mitigation: Require explicit human confirmation before confirm, dispute, cancel_dispute, offer, accept_offer, upload_proof, order, or payment actions, and verify identifiers and request bodies first.

Risk: API keys and response files may persist in shell profiles or local LinkFox data directories.

Mitigation: Store API keys only on appropriate machines, remove or rotate them when no longer needed, and clean up saved response files that contain customer or business data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-shopee-store-returns)
- [Shopee Returns API documentation](https://open.shopee.com/documents/v2/v2.returns.get_return_list?module=102&type=1)
- [LinkFox returns API reference](references/api.md)
- [LinkFox onboarding reference](references/onboarding.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with shell commands and JSON API responses; full responses may be saved as JSON files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Small responses can be printed in full; larger responses may be summarized while complete JSON is retained in a local LinkFox session data directory.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
