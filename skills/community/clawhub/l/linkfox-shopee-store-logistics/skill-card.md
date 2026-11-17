## Description:

Shopee Store Logistics helps agents call LinkFox-mediated Shopee Open Platform logistics APIs for shipping, tracking, shipping documents, addresses, channels, booking, and related store logistics tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and store operators use this skill to manage logistics workflows for authorized Shopee stores, including preparing shipments, retrieving tracking numbers, creating or downloading shipping documents, and managing logistics addresses or channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform live Shopee logistics actions such as shipping, deleting, pausing, or updating store logistics resources.

Mitigation: Require explicit user confirmation before actions that ship orders, delete or pause resources, or change logistics settings.

Risk: The skill handles LinkFox account credentials and may write customer or store logistics data to local response files.

Mitigation: Avoid sharing SMS codes or API keys in agent-visible transcripts, and periodically delete or protect saved LinkFox response files.

Risk: Gateway URL overrides could route logistics requests away from trusted LinkFox services.

Mitigation: Verify LINKFOX_* gateway environment variables point only to trusted LinkFox HTTPS domains before use.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/linkfox-ai/skills/linkfox-shopee-store-logistics)
- [Shopee Open Platform Logistics documentation](https://open.shopee.com/documents/v2/v2.logistics.get_shipping_parameter?module=95&type=1)
- [Logistics API reference](artifact/references/api.md)
- [Authentication and billing onboarding](artifact/references/onboarding.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts save full JSON responses locally and print either the full response or a concise summary for large responses.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
